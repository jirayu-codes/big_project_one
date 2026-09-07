import os
import sqlite3

from flask import Flask, g, redirect, render_template, request, url_for


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

    @app.route("/")
    def index():
        db = get_db()
        plants = db.execute(
            "SELECT id, name, water_every, last_watered FROM plants ORDER BY id"
        ).fetchall()
        return render_template("index.html", plants=plants)

    @app.route("/add", methods=["POST"])
    def add_plant():
        name = request.form["name"].strip()
        water_every = int(request.form["water_every"])
        db = get_db()
        db.execute(
            "INSERT INTO plants (name, water_every, last_watered) VALUES (?, ?, NULL)",
            (name, water_every),
        )
        db.commit()
        return redirect(url_for("index"))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)