# Mark a Plant as Watered — Plan

Numbered task groups. This is spec-driven development: every task traces back
to the approved spec (`requirements.md`). Each task group is implemented to
match the requirements, and validated before moving on.

## Run checks

- Run tests and linting after each task group to confirm the code matches the
  requirements.

## Task group 1 — Status calculation

1. Replace the `plant_status` stub with real logic:
   - no `last_watered` → "never watered"
   - due date before today → "overdue"
   - due date is today → "due today"
   - due date in the future → "due in X days"
2. Compute the due date as `last_watered + water_every days`.
3. Add a helper to parse `last_watered` (YYYY-MM-DD) and return the number of
   days until the due date.
4. Add tests covering all four statuses and the boundary (due today vs
   overdue vs future).

## Task group 2 — Mark watered action

1. Add a route (POST) that marks a plant as watered and sets `last_watered`
   to today's date.
2. The route looks up the plant by id; missing/invalid ids are handled
   gracefully (e.g. 404).
3. Add a test: posting mark-watered updates `last_watered` in the database.
4. Add a test: a missing plant id does not crash and returns a sensible
   response.

## Task group 3 — UI

1. Add a "Watered" button to each plant row in the list.
2. After marking, redirect back to the home page so the status refreshes.
3. Keep the JavaScript touch minimal (same form-button disable pattern as the
   walking skeleton).
4. Add a test: after marking a plant watered, the page shows the updated
   status.

## Task group 4 — Walk the feature end to end

1. Verify the full loop: add a plant (never watered) → mark watered → status
   updates to "due in 7 days"-style label.
2. Verify with a plant whose `last_watered` is long in the past → shows
   "overdue".
3. Run all tests and lint checks; fix anything failing.