# Track Other Care Types — Requirements

## Feature

Let each plant optionally have fertilize and repot schedules, and show the
next-due status for all care types.

This is the third feature, building on the walking skeleton and the
mark-as-watered feature.

## Scope

In scope:

- Each plant can optionally have a fertilize schedule and a repot schedule,
  each with its own interval (days).
- The add-plant form collects the fertilize and repot intervals along with the
  watering interval.
- The plant list shows a next-due status for each care type the plant has a
  schedule for: water, fertilize, and repot.
- Reuse the status vocabulary and logic: "never done", "overdue",
  "due today", "due in X days".

Out of scope for this feature (later roadmap items):

- Marking a plant as fertilized or repotted (buttons that update the
  last-done date). Only the watering mark action exists today.
- Editing a plant's schedules after it is created.
- The "due soon" / "overdue" summary list section on the main page.

## Decisions

- Schema uses flat columns on the `plants` table (Option A): one pair of
  columns per care type (interval + last-done date).
- Fertilize and repot schedules are optional. A plant may have only a watering
  schedule; the other intervals may be blank.
- The add-plant form collects all three intervals at once. Simpler than a
  separate edit page, which is not part of this feature.
- A care type with no interval set is not tracked and shows no status.
- "Today" still comes from the server date (no timezone handling).
- This feature only tracks schedules and shows status. Mark-fertilized /
  mark-repotted actions are a later feature.

## Context

The watering status logic already exists. This feature generalises the
"interval + last-done date" pattern to fertilize and repot, without duplicating
the status code (DRY).

## Schema

This feature changes the authoritative schema in `SPECS/TECH.md`. The `plants`
table becomes:

```
Table: plants
- id:                INTEGER PRIMARY KEY AUTOINCREMENT
- name:              TEXT     # the name of the plant
- water_every:       INTEGER  # how many days between watering (required)
- last_watered:      TEXT     # date last watered; may be empty/never
- fertilize_every:   INTEGER  # how many days between fertilizing; may be empty if not tracked
- last_fertilized:   TEXT     # date last fertilized; may be empty/never
- repot_every:       INTEGER  # how many days between repotting; may be empty if not tracked
- last_repotted:     TEXT     # date last repotted; may be empty/never
```