# Track Other Care Types — Validation

How we know this feature is done and can be merged.

## Functional checks

- I can add a plant with an optional fertilize interval and an optional repot
  interval, alongside the required watering interval.
- A plant with all three schedules shows a next-due status for water,
  fertilize, and repot.
- A plant with only a watering schedule shows only the watering status.
- A tracked care type with no last-done date shows "never done".
- A tracked care type whose due date is before today shows "overdue".
- A tracked care type whose due date is today shows "due today".
- A tracked care type whose due date is in the future shows "due in X days".
- The watering status still reads "never watered" when not yet watered.

## Test checks

- Automated tests pass, confirming the implementation matches the requirements.
- There is a test for: the schema contains the new columns.
- There is a test for: a plant with all three schedules stores correctly.
- There is a test for: a plant with only watering stores NULL for the others.
- There is a test for: invalid intervals are rejected.
- There is a test for: each care type's status (never done / overdue / due
  today / due in X days).
- There is a test for: a plant with no fertilize schedule shows no fertilize
  status.
- There is a test for: the page shows fertilize/repot statuses.
- Existing tests (walking skeleton + mark-as-watered) still pass.

## Lint / checks

- Lint and any configured checks pass.
- The JavaScript touch stays minimal and simple.

## Spec alignment

Before merging, compare what was built against `SPECS/TECH.md` and this
feature spec. Report any differences and update the spec files only with the
user's approval.

## Scope guard

Marking a plant as fertilized or repotted, editing a plant's schedules after
creation, and the "due soon"/"overdue" summary list section are NOT part of
this feature. Do not implement them here; they belong in later features on the
roadmap.