# Walking Skeleton — Plan

Numbered task groups. Red/Green style: write failing tests first, then the
minimal code to make them pass.

## Run checks

- Run tests and linting after each task group. There is a minimal JavaScript
  touch, so ensure the JS stays small and simple.

## Task group 1 — Project setup

1. Create a Flask app (`app.py`) that serves a home page.
2. Set up an empty SQLite database with the `plants` table (per the schema in
   `SPECS/TECH.md`).
3. Add a basic test that the home page loads.
4. Add a test config for tests that use a temporary database.

## Task group 2 — Add a plant

1. Add a route to receive a new plant (name + water_every).
2. Insert the new plant into the `plants` table.
3. Add a test: submitting a plant stores it in the database.
4. Keep the form simple, with a minimal JavaScript touch.

## Task group 3 — List plants with status

1. Add a route that reads all plants and shows them on the page.
2. Show the watering status for each plant. In this feature every plant is
   "never watered", so that is the status shown.
3. Add a test: a saved plant appears on the page.
4. Add a test: a plant with no last watered date shows "never watered".

## Task group 4 — Walk the skeleton end to end

1. Verify the full loop: add a plant via the form, then see it listed with its
   status.
2. Run all tests and lint checks; fix anything failing.

## Notes / known next steps

- Marking a plant as watered is a separate feature. Once it lands, the status
  logic ("overdue", "due today", "due in X days") will become visible.
