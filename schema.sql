CREATE TABLE IF NOT EXISTS plants (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    name             TEXT    NOT NULL,
    water_every      INTEGER NOT NULL,
    last_watered     TEXT,
    fertilize_every  INTEGER,
    last_fertilized  TEXT,
    repot_every      INTEGER,
    last_repotted    TEXT
);
