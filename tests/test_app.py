from datetime import date, timedelta

from app import care_type_status, days_until_due, plant_status


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
    assert days_until_due(plant, "water_every", "last_watered") < 0


def test_days_until_due_zero_is_due_today():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=7)).isoformat(),
    }
    assert days_until_due(plant, "water_every", "last_watered") == 0


def test_days_until_due_positive_is_future():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": (date.today() - timedelta(days=2)).isoformat(),
    }
    assert days_until_due(plant, "water_every", "last_watered") > 0


def test_plant_status_with_malformed_date_is_never_watered():
    plant = {
        "id": 1,
        "name": "Monstera",
        "water_every": 7,
        "last_watered": "not-a-date",
    }
    assert plant_status(plant) == "never watered"


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


def test_schema_contains_new_columns(app, db):
    columns = [row["name"] for row in db.execute("PRAGMA table_info(plants)")]
    for column in ("fertilize_every", "last_fertilized", "repot_every", "last_repotted"):
        assert column in columns


def test_plant_with_all_three_schedules_stores_correctly(client, db):
    client.post(
        "/add",
        data={
            "name": "Monstera",
            "water_every": "7",
            "fertilize_every": "14",
            "repot_every": "30",
        },
    )

    row = db.execute(
        "SELECT water_every, fertilize_every, repot_every FROM plants WHERE name = ?",
        ("Monstera",),
    ).fetchone()

    assert row is not None
    assert row["water_every"] == 7
    assert row["fertilize_every"] == 14
    assert row["repot_every"] == 30


def test_plant_with_only_watering_stores_null_for_others(client, db):
    client.post("/add", data={"name": "Cactus", "water_every": "14"})

    row = db.execute(
        "SELECT fertilize_every, last_fertilized, repot_every, last_repotted "
        "FROM plants WHERE name = ?",
        ("Cactus",),
    ).fetchone()

    assert row["fertilize_every"] is None
    assert row["last_fertilized"] is None
    assert row["repot_every"] is None
    assert row["last_repotted"] is None


def test_invalid_fertilize_interval_is_rejected(client, db):
    response = client.post(
        "/add", data={"name": "Fern", "water_every": "5", "fertilize_every": "0"}
    )

    assert response.status_code == 400
    row = db.execute("SELECT COUNT(*) AS n FROM plants").fetchone()
    assert row["n"] == 0


def test_non_numeric_repot_interval_is_rejected(client, db):
    response = client.post(
        "/add", data={"name": "Fern", "water_every": "5", "repot_every": "abc"}
    )

    assert response.status_code == 400
    row = db.execute("SELECT COUNT(*) AS n FROM plants").fetchone()
    assert row["n"] == 0


def test_care_type_status_never_done():
    plant = {
        "id": 1,
        "name": "Rose",
        "water_every": 7,
        "last_watered": None,
        "fertilize_every": 14,
        "last_fertilized": None,
        "repot_every": None,
        "last_repotted": None,
    }
    assert care_type_status(plant, "fertilize_every", "last_fertilized", "never done") == "never done"


def test_care_type_status_overdue():
    plant = {
        "id": 1,
        "name": "Rose",
        "water_every": 7,
        "last_watered": None,
        "fertilize_every": 14,
        "last_fertilized": (date.today() - timedelta(days=20)).isoformat(),
        "repot_every": None,
        "last_repotted": None,
    }
    assert care_type_status(plant, "fertilize_every", "last_fertilized", "never done") == "overdue"


def test_care_type_status_due_today():
    plant = {
        "id": 1,
        "name": "Rose",
        "water_every": 7,
        "last_watered": None,
        "fertilize_every": 14,
        "last_fertilized": (date.today() - timedelta(days=14)).isoformat(),
        "repot_every": None,
        "last_repotted": None,
    }
    assert care_type_status(plant, "fertilize_every", "last_fertilized", "never done") == "due today"


def test_care_type_status_due_in_x_days():
    plant = {
        "id": 1,
        "name": "Rose",
        "water_every": 7,
        "last_watered": None,
        "fertilize_every": 14,
        "last_fertilized": (date.today() - timedelta(days=4)).isoformat(),
        "repot_every": None,
        "last_repotted": None,
    }
    assert care_type_status(plant, "fertilize_every", "last_fertilized", "never done") == "due in 10 days"


def test_care_type_status_hidden_when_no_interval():
    plant = {
        "id": 1,
        "name": "Rose",
        "water_every": 7,
        "last_watered": None,
        "fertilize_every": None,
        "last_fertilized": None,
        "repot_every": 30,
        "last_repotted": None,
    }
    assert care_type_status(plant, "fertilize_every", "last_fertilized", "never done") is None


def test_page_shows_fertilize_and_repot_statuses(client):
    client.post(
        "/add",
        data={
            "name": "Monstera",
            "water_every": "7",
            "fertilize_every": "14",
            "repot_every": "30",
        },
    )

    response = client.get("/")

    assert b"Fertilize:" in response.data
    assert b"never done" in response.data
    assert b"Repot:" in response.data


def test_plant_with_only_watering_shows_no_fertilize_status(client):
    client.post("/add", data={"name": "Cactus", "water_every": "14"})

    response = client.get("/")

    assert b"never watered" in response.data
    assert b"Fertilize:" not in response.data
    assert b"Repot:" not in response.data
