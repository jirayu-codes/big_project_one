import sqlite3

import pytest

import app as app_module


@pytest.fixture()
def app(tmp_path):
    return app_module.create_app(
        {"TESTING": True, "DATABASE": str(tmp_path / "test.db")}
    )


@pytest.fixture()
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture()
def db(app):
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()
