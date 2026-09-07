import sqlite3

import pytest

import app as app_module


@pytest.fixture()
def app(tmp_path):
    return app_module.create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.db")})


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_plant_stores_it(app, client):
    client.post("/add", data={"name": "Monstera", "water_every": "7"})

    with app.app_context():
        db = sqlite3.connect(app.config["DATABASE"])
        row = db.execute(
            "SELECT name, water_every, last_watered FROM plants WHERE name = ?",
            ("Monstera",),
        ).fetchone()
        db.close()

    assert row == ("Monstera", 7, None)


def test_added_plant_appears_on_page(client):
    client.post("/add", data={"name": "Fern", "water_every": "5"})
    response = client.get("/")
    assert b"Fern" in response.data


def test_never_watered_plant_shows_never_watered(client):
    client.post("/add", data={"name": "Cactus", "water_every": "14"})
    response = client.get("/")
    assert b"Never watered" in response.data