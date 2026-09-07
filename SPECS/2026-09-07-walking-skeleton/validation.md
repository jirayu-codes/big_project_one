# Walking Skeleton — Validation

How we know this feature is done and can be merged.

## Functional checks

- I can open the home page in a browser.
- I can add a plant with a name and a watering interval.
- After adding, the plant appears in the list.
- The plant shows the status "never watered".

## Test checks

- All automated tests pass (Red/Green: tests written first, then code to pass).
- There is a test for: adding a plant stores it.
- There is a test for: a saved plant appears on the page.
- There is a test for: a plant with no last watered date shows "never watered".

## Lint / checks

- Lint and any configured checks pass.
- The JavaScript touch stays minimal and simple.

## Spec alignment

Before merging, compare what was built against `SPECS/TECH.md` and this
feature spec. Report any differences and update the spec files only with the
user's approval.

## Scope guard

Marking a plant as watered, other care types, and a due-soon/overdue list are
NOT part of this feature. Do not implement them here; they belong in later
features on the roadmap.
