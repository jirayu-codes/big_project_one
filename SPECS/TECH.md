# PlantPal — Technology

## Stack

- Vanilla HTML, CSS, and JavaScript.
- Basic Python (Flask) to serve the site.
- SQLite for storing plant data.
- No frameworks or libraries like React. Keep it simple.

## Database Schema

This is the single place the schema lives. The `feature-specification` skill
reads it when producing canonical requirements.

```
Table: plants
- id:            INTEGER PRIMARY KEY AUTOINCREMENT
- name:          TEXT     # the name of the plant
- water_every:   INTEGER  # how many days between watering
- last_watered:  TEXT     # the date last watered; may be empty/never if not watered yet
```

## Engineering Standards

These are the rules we follow when building PlantPal.

### Spec-Driven Development
All work starts from a written spec (requirements, plan, validation). Every
piece of code must trace back to an approved spec before it is written.

### Simplicity Over Complexity
Always pick the simplest solution that works. Prefer the most obvious
approach over clever tricks.

### DRY (Don't Repeat Yourself)
If you find yourself copying the same code, pull it out into one shared spot
instead of repeating it.

### Walking Skeleton
Build the thinnest working version of the app first, then grow features on
top of it. Never try to build everything at once.
