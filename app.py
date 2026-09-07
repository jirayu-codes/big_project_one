import logging
import os
import sqlite3
from datetime import date, timedelta

from flask import Flask, abort, g, redirect, render_template, request, url_for

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("plantpal")


def mark_plant_watered(db, plant_id):
    """Set the plant's last_watered to today's date. Return the plant or None."""
    db.execute(
        "UPDATE plants SET last_watered = ? WHERE id = ?",
        (date.today().isoformat(), plant_id),
    )
    db.commit()
    return get_plant(db, plant_id)


def get_plant(db, plant_id):
    """Return the plant with the given id, or None if it does not exist."""
    return db.execute(
        "SELECT id, name, water_every, last_watered FROM plants WHERE id = ?",
        (plant_id,),
    ).fetchone()


def get_all_plants(db):
    """Return every plant in the database, oldest first."""
    return db.execute(
        "SELECT id, name, water_every, last_watered FROM plants ORDER BY id"
    ).fetchall()


def add_new_plant(db, form):
    """Create a plant from a submitted form and return the saved row."""
    name = form["name"].strip()
    try:
        water_every = int(form["water_every"])
    except (KeyError, ValueError):
        raise ValueError("water_every must be a whole number") from None
    if not name or water_every < 1:
        raise ValueError("name must not be empty and water_every must be at least 1")
    cursor = db.execute(
        "INSERT INTO plants (name, water_every, last_watered) VALUES (?, ?, NULL)",
        (name, water_every),
    )
    db.commit()
    return get_plant(db, cursor.lastrowid)


def days_until_due(plant):
    """Return the number of days until the plant is due, given it has been watered.

    A negative result means the plant is overdue; 0 means it is due today.
    """
    last_watered = date.fromisoformat(plant["last_watered"])
    due_date = last_watered + timedelta(days=plant["water_every"])
    return (due_date - date.today()).days


def plant_status(plant):
    """Return the watering status text shown for a plant."""
    if not plant["last_watered"]:
        return "never watered"
    days = days_until_due(plant)
    if days < 0:
        return "overdue"
    if days == 0:
        return "due today"
    return f"due in {days} days"


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, "plantpal.db")
    )
    if test_config is not None:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    def init_db():
        with app.open_resource("schema.sql") as f:
            get_db().executescript(f.read().decode("utf-8"))
        get_db().commit()

    with app.app_context():
        init_db()
    logger.info("PlantPal ready, database: %s", app.config["DATABASE"])

    @app.context_processor
    def inject_helpers():
        return {"plant_status": plant_status}

    @app.route("/")
    def index():
        plants = get_all_plants(get_db())
        logger.info("Rendered home page with %d plant(s)", len(plants))
        return render_template("index.html", plants=plants)

    @app.route("/add", methods=["POST"])
    def add_plant():
        try:
            plant = add_new_plant(get_db(), request.form)
        except (KeyError, ValueError) as exc:
            logger.warning("Rejected invalid add-plant form: %s", exc)
            return "Please give the plant a name and how many days between watering.", 400
        logger.info(
            "Added plant %r (water every %s days)", plant["name"], plant["water_every"]
        )
        return redirect(url_for("index"))

    @app.route("/watered/<int:plant_id>", methods=["POST"])
    def mark_watered(plant_id):
        plant = mark_plant_watered(get_db(), plant_id)
        if plant is None:
            logger.warning("Tried to water a plant that does not exist (id=%s)", plant_id)
            abort(404)
        logger.info("Marked plant %r (id=%s) as watered", plant["name"], plant_id)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", "3000"))
    debug = os.environ.get("FLASK_DEBUG", "").lower() in {"1", "true", "yes"}
    app.run(host="0.0.0.0", port=port, debug=debug)
