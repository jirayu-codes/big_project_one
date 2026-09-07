# Mark a Plant as Watered — Validation

How we know this feature is done and can be merged.

## Functional checks

- I can click a "Watered" button on a plant and it marks the plant as watered
  today.
- After marking, the plant's status updates on the page after reload.
- A plant with no `last_watered` date shows "never watered".
- A plant whose due date is before today shows "overdue".
- A plant whose due date is today shows "due today".
- A plant whose due date is in the future shows "due in X days".

## Test checks

- Automated tests pass, confirming the implementation matches the requirements.
- There is a test for: each of the four statuses (never watered, overdue, due
  today, due in X days).
- There is a test for: the due-today boundary (due today vs overdue vs future).
- There is a test for: posting mark-watered updates `last_watered`.
- There is a test for: a missing/invalid plant id returns a sensible response.
- There is a test for: after marking, the page shows the updated status.

## Lint / checks

- Lint and any configured checks pass.
- The JavaScript touch stays minimal and simple.

## Spec alignment

Before merging, compare what was built against `SPECS/TECH.md` and this
feature spec. Report any differences and update the spec files only with the
user's approval.

## Scope guard

Tracking other care types (fertilize, repot) and the "due soon"/"overdue"
summary list section are NOT part of this feature. Do not implement them here;
they belong in later features on the roadmap.