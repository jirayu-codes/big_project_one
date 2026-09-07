import logging
import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("plantpal")


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
    water_every = int(form["water_every"])
    if not name or water_every < 1:
        raise ValueError("name must not be empty and water_every must be at least 1")
    cursor = db.execute(
        "INSERT INTO plants (name, water_every, last_watered) VALUES (?, ?, NULL)",
        (name, water_every),
    )
    db.commit()
    return get_plant(db, cursor.lastrowid)


def plant_status(plant):
    """Return the watering status text shown for a plant.

    In this feature no plant has been watered yet, so every plant shows
    "never watered". Later features will make the "overdue", "due today",
    and "due in X days" statuses appear once plants can be marked watered.
    """
    if not plant["last_watered"]:
        return "never watered"
    return "due today"


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

    return app


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "3000"))
    app.run(host="0.0.0.0", port=port, debug=True)