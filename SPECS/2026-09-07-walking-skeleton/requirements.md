# Walking Skeleton — Requirements

## Feature

Add a plant (name and how often it needs water), see it listed on the page,
and see its watering status.

This is the thinnest working slice of PlantPal, per the roadmap.

## Scope

In scope:

- Add a plant with a name and a watering interval (days).
- See every plant listed on the page.
- See a watering status for each plant.

Out of scope for this feature (later roadmap items):

- Marking a plant as watered.
- Tracking other care types (fertilize, repot).
- A "due soon" / "overdue" list section.

## Context

Because marking a plant as watered is a later feature, every plant that is
added in this feature has never been watered. So the status shown for a new
plant is always "never watered". The "overdue / due today / due in X days"
logic becomes visible only after the watering feature exists, but this feature
still records the `water_every` interval needed for that later logic.

## Decisions

- A newly added plant has no last watered date — it is "never watered".
- The status view will use: "never watered", "overdue", "due today", or
  "due in X days".
- Only water care info is handled now.
- A minimal JavaScript touch is allowed for the add-plant form, kept simple.

## Schema

Uses the `plants` table from `SPECS/TECH.md` (the single source of truth):

```
Table: plants
- id:            INTEGER PRIMARY KEY AUTOINCREMENT
- name:          TEXT     # the name of the plant
- water_every:   INTEGER  # how many days between watering
- last_watered:  TEXT     # may be empty/never if not watered yet
```

For this feature, `last_watered` is always empty because watering is not yet
implemented.
