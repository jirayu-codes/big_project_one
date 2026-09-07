from datetime import date, timedelta

from app import days_until_due, plant_status


def _add(client, name, water_every):
    return client.post("/add", data={"name": name, "water_every": str(water_every)})


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_submitting_plant_stores_it(client, db):
    client.post("/add", data={"name": "Monstera", "water_every": "7"})

    row = db.execute(
        "SELECT name, water_every, last_watered FROM plants WHERE name = ?",
        ("Monstera",),
    ).fetchone()

    assert row is not None
    assert row["name"] == "Monstera"
    assert row["water_every"] == 7
    assert row["last_watered"] is None


def test_saved_plant_appears_on_page(client):
    client.post("/add", data={"name": "Fern", "water_every": "5"})

    response = client.get("/")

    assert b"Fern" in response.data


def test_plant_with_no_last_watered_shows_never_watered(client):
    client.post("/add", data={"name": "Cactus", "water_every": "14"})

    response = client.get("/")

    assert b"never watered" in response.data


def test_plant_status_never_watered():
    plant = {"id": 1, "name": "Monstera", "water_every": 7, "last_watered": None}
    assert plant_status(plant) == "never watered"


def test_invalid_plant_form_is_rejected_with_400(client, db):
    response = client.post("/add", data={"name": "   ", "water_every": "3"})

    assert response.status_code == 400
    row = db.execute("SELECT COUNT(*) AS n FROM plants").fetchone()
    assert row["n"] == 0


def test_plant_status_overdue():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=10)).isoformat(),
    }
    assert plant_status(plant) == "overdue"


def test_plant_status_due_today():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=7)).isoformat(),
    }
    assert plant_status(plant) == "due today"


def test_plant_status_due_in_x_days():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=2)).isoformat(),
    }
    assert plant_status(plant) == "due in 5 days"


def test_days_until_due_negative_is_overdue():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=10)).isoformat(),
    }
    assert days_until_due(plant) < 0


def test_days_until_due_zero_is_due_today():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=7)).isoformat(),
    }
    assert days_until_due(plant) == 0


def test_days_until_due_positive_is_future():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=2)).isoformat(),
    }
    assert days_until_due(plant) > 0


def test_mark_watered_updates_last_watered(client, db):
    client.post("/add", data={"name": "Pothos", "water_every": "5"})
    plant_id = db.execute("SELECT id FROM plants WHERE name = ?", ("Pothos",)).fetchone()["id"]

    response = client.post(f"/watered/{plant_id}")

    assert response.status_code == 302
    row = db.execute("SELECT last_watered FROM plants WHERE id = ?", (plant_id,)).fetchone()
    assert row["last_watered"] == date.today().isoformat()


def test_mark_watered_missing_plant_returns_404(client):
    response = client.post("/watered/999")

    assert response.status_code == 404


def test_page_shows_updated_status_after_marking(client, db):
    client.post("/add", data={"name": "Basil", "water_every": "7"})
    plant_id = db.execute("SELECT id FROM plants WHERE name = ?", ("Basil",)).fetchone()["id"]

    client.post(f"/watered/{plant_id}")

    response = client.get("/")
    assert b"due in 7 days" in response.data
    assert b"never watered" not in response.data
