CREATE TABLE IF NOT EXISTS plants (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    name         TEXT    NOT NULL,
    water_every  INTEGER NOT NULL,
    last_watered TEXT
);