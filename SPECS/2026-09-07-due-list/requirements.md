# Due Soon / Overdue Summary List — Requirements

## Feature

Show a summary section at the top of the main page listing plants that need
attention: plants that are overdue, due today, or due soon, for any tracked
care type (water, fertilize, repot).

This is the fourth feature, building on the walking skeleton, mark-as-watered,
and care-types features.

## Scope

In scope:

- A summary section at the top of the main page.
- The summary lists each plant+care-type combination that is overdue, due
  today, or due soon.
- "Due soon" means the due date is within the next 3 days (including today
  onwards, excluding overdue which has its own bucket).
- All three care types count: water, fertilize, repot.
- The main plant list stays unchanged below.

Out of scope for this feature:

- Marking a plant as fertilized or repotted (still not implemented).
- Editing a plant's schedules.
- Configurable "due soon" thresholds.

## Decisions

- Buckets:
  - overdue — due date is before today.
  - due today — due date is today.
  - due soon — due date is 1 to 3 days from today.
  (Due today and due soon are computed from the same `days_until_due` value.)
- "Due soon" threshold is a constant 3 days, stored once so it is easy to
  change.
- Never-done plants (no last-done date) have no due date, so they never appear
  in the summary. They only show in the main list as "never watered"/"never
  done".
- A care type with no interval is not tracked and never appears in the summary.
- The summary is a flat list ordered by severity: overdue first, then due
  today, then due soon (soonest first). Within a bucket, order by soonest due
  date, then by plant name.
- Each entry shows: plant name, care type label, and status text
  (e.g. "Monstera — Water: overdue").

## Context

The status logic (`care_type_status`, `days_until_due`) already exists and is
reused for the summary. No schema changes are needed; the summary is computed
in Python from the plants already loaded for the main page.

## Schema

Unchanged. Uses the `plants` table from `SPECS/TECH.md` (the single source of
truth). No new columns or tables.