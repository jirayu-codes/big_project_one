# Mark a Plant as Watered — Requirements

## Feature

Let the user mark a plant as watered today, and show each plant's real
watering status: never watered, overdue, due today, or due in X days.

This is the second feature built on the walking skeleton.

## Scope

In scope:

- Mark a plant as watered, setting its `last_watered` to today's date.
- Show the next due date for each plant, computed from `last_watered` plus
  `water_every` days.
- Show a status label for each plant:
  - never watered — the plant has no `last_watered` date.
  - overdue — the due date is before today.
  - due today — the due date is today.
  - due in X days — the due date is in the future (X is the number of days).

Out of scope for this feature (later roadmap items):

- Track other care types (fertilize, repot).
- A "due soon" / "overdue" summary list section on the main page.

## Decisions

- "Mark watered" sets `last_watered` to the server's current date (via
  Python's date, no timezone handling).
- The UI is a per-plant button in the list. After marking, the page reloads and
  the plant's status updates.
- "Today" comes from the server date, not the browser.
- The status calculation replaces the current stub (`plant_status` always
  returned "never watered" or "due today").

## Context

Previously, no plant could be watered, so all plants showed "never watered".
Now that a plant can be watered, the status logic becomes real and visible.

## Schema

Uses the `plants` table from `SPECS/TECH.md` (the single source of truth):

```
Table: plants
- id:            INTEGER PRIMARY KEY AUTOINCREMENT
- name:          TEXT     # the name of the plant
- water_every:   INTEGER  # how many days between watering
- last_watered:  TEXT     # may be empty/never if not watered yet
```

`last_watered` stores a date string in YYYY-MM-DD format. No new columns are
needed for this feature.