# Track Other Care Types — Plan

Numbered task groups. This is spec-driven development: every task traces back
to the approved spec (`requirements.md`). Each task group is implemented to
match the requirements, and validated before moving on.

## Run checks

- Run tests and linting after each task group to confirm the code matches the
  requirements.

## Task group 1 — Schema update

1. Update `schema.sql` to add `fertilize_every`, `last_fertilized`,
   `repot_every`, and `last_repotted` to the `plants` table.
2. Handle the existing database: the app should still start with a pre-existing
   `plants` table that lacks the new columns. Decide and apply a simple
   migration strategy (e.g. `ALTER TABLE` idempotent strategy, or note a clean
   rebuild is acceptable for a dev app).
3. Update the authoritative schema block in `SPECS/TECH.md`.
4. Add a test confirming the new columns exist in the created database.

## Task group 2 — Store fertilize/repot schedules

1. Update `add_new_plant` so the add-plant form can optionally provide
   fertilize and repot intervals.
2. Blank intervals are stored as NULL (not tracked); invalid values (non-numeric
   or < 1) are rejected like the watering interval already is.
3. Add tests: a plant with all three schedules stores correctly; a plant with
   only watering stores NULL for the other two; invalid intervals are rejected.

## Task group 3 — Generalised status logic

1. Generalise the existing `days_until_due` / `plant_status` pattern so it works
   for any care type (water, fertilize, repot) without repeating the logic.
2. For each care type the plant tracks:
   - no last-done date → "never done"
   - due date before today → "overdue"
   - due date today → "due today"
   - due date in future → "due in X days"
3. A care type with no interval is not tracked and shows no status.
4. Keep the existing watering status text ("never watered" for water).
5. Add tests for each care type's status, including a plant with fertilize
   schedule but never fertilized, and a plant with no fertilize schedule.

## Task group 4 — UI

1. Add fertilize and repot interval fields (optional) to the add-plant form.
2. The plant list shows the status per care type. Keep it simple and readable.
3. Keep the JS touch minimal.
4. Add a test: a plant with a fertilize schedule shows its fertilize status on
   the page.

## Task group 5 — Walk the feature end to end

1. Verify: add a plant with all three schedules → the page shows water,
   fertilize, and repot statuses. Add one with only watering → only the water
   status shows.
2. Run all tests and lint checks; fix anything failing.