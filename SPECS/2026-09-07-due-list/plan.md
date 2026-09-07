# Due Soon / Overdue Summary List — Plan

Numbered task groups. This is spec-driven development: every task traces back
to the approved spec (`requirements.md`). Each task group is implemented to
match the requirements, and validated before moving on.

## Run checks

- Run tests and linting after each task group to confirm the code matches the
  requirements.

## Task group 1 — Summary computation

1. Add a helper that, given a list of plants, returns the summary entries:
   each (plant, care type, status) where the status is "overdue", "due today",
   or "due soon".
2. Reuse `CARE_TYPES` and `care_type_status`/`days_until_due` from app.py —
   don't duplicate the logic.
3. Define the "due soon" threshold as a named constant (3 days), used once.
4. Sort entries: overdue first, then due today, then due soon; within each
   bucket soonest first, then plant name.
5. Add tests: an overdue plant appears; a due-today plant appears; a due-soon
   plant appears; a never-done plant does NOT appear; an untracked care type
   does NOT appear; sorting order is correct.

## Task group 2 — Page display

1. Pass the computed summary entries to the index template.
2. Render a summary section at the top of the page (shown only when there is
   at least one entry; hidden otherwise).
3. Each entry shows plant name, care type label, and status.
4. Keep the main plant list unchanged.
5. Add tests: the page shows an entry when a plant is overdue; the page shows
   no summary when nothing is due.

## Task group 3 — Walk the feature end to end

1. Verify: add a plant, water it with a long-past date scenario → "overdue"
   appears in summary; add a never-done plant → not in summary.
2. Run all tests and lint checks; fix anything failing.