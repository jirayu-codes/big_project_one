from app import plant_status


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
