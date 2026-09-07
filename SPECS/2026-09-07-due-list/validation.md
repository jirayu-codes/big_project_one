# Due Soon / Overdue Summary List — Validation

How we know this feature is done and can be merged.

## Functional checks

- The main page shows a summary section when any plant is overdue, due today,
  or due soon for a tracked care type.
- Overdue entries are listed first, then due today, then due soon (soonest
  first).
- Each entry shows the plant name, care type label, and status.
- A never-done plant (no last-done date) does not appear in the summary.
- A care type with no interval does not appear in the summary.
- When nothing is overdue/due today/due soon, the summary section is hidden.
- The main plant list still works as before.

## Test checks

- Automated tests pass, confirming the implementation matches the requirements.
- There is a test for: an overdue plant appears in the summary.
- There is a test for: a due-today plant appears in the summary.
- There is a test for: a due-soon plant appears in the summary.
- There is a test for: a never-done plant does NOT appear.
- There is a test for: an untracked care type does NOT appear.
- There is a test for: sorting order (overdue → due today → due soon).
- There is a test for: the page renders no summary when nothing is due.
- Existing tests (walking skeleton + mark-as-watered + care types) still pass.

## Lint / checks

- Lint and any configured checks pass.
- The JavaScript touch stays minimal and simple (likely unchanged).

## Spec alignment

Before merging, compare what was built against `SPECS/TECH.md` and this
feature spec. Report any differences and update the spec files only with the
user's approval.

## Scope guard

Marking a plant as fertilized or repotted, editing a plant's schedules, and
configurable "due soon" thresholds are NOT part of this feature. Do not
implement them here.