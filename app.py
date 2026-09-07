import logging
import os
import sqlite3
from datetime import date, timedelta

from flask import Flask, abort, g, redirect, render_template, request, url_for

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("plantpal")


def _add_column(db, table, column, definition):
    """Add a single column to a table if it is not already present."""
    columns = [row["name"] for row in db.execute(f"PRAGMA table_info({table})")]
    if column not in columns:
        db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def ensure_schema(db):
    """Make sure the plants table has all the columns this app needs.

    With an old database the table may predate the fertilize/repot columns,
    so we add any missing ones. This is safe to run every time.
    """
    _add_column(db, "plants", "fertilize_every", "INTEGER")
    _add_column(db, "plants", "last_fertilized", "TEXT")
    _add_column(db, "plants", "repot_every", "INTEGER")
    _add_column(db, "plants", "last_repotted", "TEXT")
    db.commit()


def mark_plant_watered(db, plant_id):
    """Set the plant's last_watered to today's date. Return the plant or None."""
    plant = get_plant(db, plant_id)
    if plant is None:
        return None
    db.execute(
        "UPDATE plants SET last_watered = ? WHERE id = ?",
        (date.today().isoformat(), plant_id),
    )
    db.commit()
    return get_plant(db, plant_id)


PLANT_COLUMNS = (
    "id, name, water_every, last_watered, "
    "fertilize_every, last_fertilized, repot_every, last_repotted"
)


def get_plant(db, plant_id):
    """Return the plant with the given id, or None if it does not exist."""
    return db.execute(
        f"SELECT {PLANT_COLUMNS} FROM plants WHERE id = ?",
        (plant_id,),
    ).fetchone()


def get_all_plants(db):
    """Return every plant in the database, oldest first."""
    return db.execute(
        f"SELECT {PLANT_COLUMNS} FROM plants ORDER BY id"
    ).fetchall()


def _interval_value(form, key):
    """Return the validated interval for a form key, or None if left blank."""
    raw = form.get(key, "").strip()
    if raw == "":
        return None
    value = int(raw)
    if value < 1:
        raise ValueError(f"{key} must be at least 1")
    return value


def add_new_plant(db, form):
    """Create a plant from a submitted form and return the saved row."""
    name = form["name"].strip()
    try:
        water_every = int(form["water_every"])
    except (KeyError, ValueError):
        raise ValueError("water_every must be a whole number") from None
    if not name or water_every < 1:
        raise ValueError("name must not be empty and water_every must be at least 1")

    try:
        fertilize_every = _interval_value(form, "fertilize_every")
        repot_every = _interval_value(form, "repot_every")
    except ValueError:
        raise ValueError("fertilize_every and repot_every must be blank or at least 1") from None

    cursor = db.execute(
        "INSERT INTO plants (name, water_every, last_watered, "
        "fertilize_every, last_fertilized, repot_every, last_repotted) "
        "VALUES (?, ?, NULL, ?, NULL, ?, NULL)",
        (name, water_every, fertilize_every, repot_every),
    )
    db.commit()
    return get_plant(db, cursor.lastrowid)


def days_until_due(plant, every_col, last_col):
    """Return the days until a care type is due, given its last-done date.

    `every_col` is the name of the interval column (e.g. "water_every") and
    `last_col` the last-done column (e.g. "last_watered"). A negative result
    means overdue; 0 means due today. Returns None if the stored date is not
    in YYYY-MM-DD format.
    """
    last_done = plant[last_col]
    try:
        last_done_date = date.fromisoformat(last_done)
    except (TypeError, ValueError):
        return None
    due_date = last_done_date + timedelta(days=plant[every_col])
    return (due_date - date.today()).days


def care_type_status(plant, every_col, last_col, never_word):
    """Return the status text for one care type, e.g. "due in 3 days"."""
    if not plant[every_col]:
        return None
    if not plant[last_col]:
        return never_word
    days = days_until_due(plant, every_col, last_col)
    if days is None:
        return never_word
    if days < 0:
        return "overdue"
    if days == 0:
        return "due today"
    return f"due in {days} days"


def plant_status(plant):
    """Return the watering status text shown for a plant."""
    return care_type_status(plant, "water_every", "last_watered", "never watered")


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
        ensure_schema(get_db())

    with app.app_context():
        init_db()
    logger.info("PlantPal ready, database: %s", app.config["DATABASE"])

    @app.context_processor
    def inject_helpers():
        def plant_statuses(plant):
            """Return a list of (label, status) tuples for each tracked care type."""
            care_types = (
                ("Water", "water_every", "last_watered", "never watered"),
                ("Fertilize", "fertilize_every", "last_fertilized", "never done"),
                ("Repot", "repot_every", "last_repotted", "never done"),
            )
            rows = []
            for label, every_col, last_col, never_word in care_types:
                status = care_type_status(plant, every_col, last_col, never_word)
                if status is not None:
                    rows.append((label, status))
            return rows

        return {"plant_statuses": plant_statuses}

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
