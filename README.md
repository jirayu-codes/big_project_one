# PlantPal

**PlantPal helps people stop forgetting when to water, fertilize, or repot their plants.** You add your plants with their care schedules, and PlantPal shows you at a glance what needs attention today.

---

## The Problem

People who own more than a couple of plants know the struggle: each plant has different watering, fertilizing, and repotting needs, and it's easy to lose track. Forgetting to water leads to crispy leaves; forgetting to repot leads to root-bound plants. Relying on memory or scattered notes doesn't scale.

---

## The Solution

PlantPal is a simple, single-user web app where you:

1. **Add a plant** with its name and care intervals (water every X days, fertilize every Y days, repot every Z days).
2. **See all your plants** in one list with their current status for each care type.
3. **Mark a plant as watered** — its "last watered" date updates to today, and the due date recalculates.
4. **Get a "Needs Attention" summary** at the top of the page showing any plants that are overdue, due today, or due soon (within 3 days) for any tracked care type.

No accounts, no sharing, no history logs — just a straightforward tool you actually use.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Add plants** | Name + required watering interval; optional fertilize/repot intervals |
| **Status per care type** | Water, Fertilize, Repot each show: "never done", "overdue", "due today", or "due in X days" |
| **Mark as watered** | One click updates `last_watered` to today |
| **Due-soon / Overdue summary** | Top-of-page list: overdue first, then due today, then due soon (≤3 days); sorted by urgency then plant name |
| **Idempotent schema migration** | Existing databases auto-upgrade to new columns on startup |
| **Spec-driven development** | Every feature traced from written spec → plan → validation → implementation |

---

## Tech Stack

- **Backend**: Python 3 + Flask (minimal, no extensions)
- **Database**: SQLite (via Python's built-in `sqlite3` module)
- **Frontend**: Vanilla HTML, CSS, JavaScript — no frameworks, no build step
- **Testing**: pytest with temporary DB fixtures
- **Linting**: ruff (with DTZ rules disabled — intentional, see ADR below)

---

## Database Design

Single table: `plants`

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER PRIMARY KEY AUTOINCREMENT | Unique identifier |
| `name` | TEXT NOT NULL | Plant's display name |
| `water_every` | INTEGER NOT NULL | Days between waterings (required) |
| `last_watered` | TEXT | ISO date of last watering; NULL = never |
| `fertilize_every` | INTEGER | Days between fertilizing; NULL = not tracked |
| `last_fertilized` | TEXT | ISO date of last fertilizing; NULL = never |
| `repot_every` | INTEGER | Days between repotting; NULL = not tracked |
| `last_repotted` | TEXT | ISO date of last repotting; NULL = never |

**Schema is the single source of truth** — defined in `SPECS/TECH.md` and kept in sync with `schema.sql`. Migrations are handled by `ensure_schema()` which idempotently adds missing columns.

---

## How to Run

```bash
cd /home/codio/workspace/big_project_one
python3 app.py
```

The server starts on `http://0.0.0.0:3000`. In a Codio box, the public URL is:
```
https://${CODIO_HOSTNAME}-3000.codio.io/
```

---

## Running Tests

```bash
python3 -m pytest -q
# 38 tests pass
ruff check .
# All checks passed
```

---

## Architecture Decisions

### Spec-Driven Development (Not TDD)

We write a feature spec (requirements, plan, validation) first, then implement to match it, then write tests that confirm the spec is met. This keeps scope clear and avoids over-engineering.

### No Timezone Handling

All dates use `date.today()` (server local date) and are stored as `YYYY-MM-DD` strings. This is intentional for a single-user app — the user and server share a date context. `ruff.toml` disables DTZ lints with a comment pointing to this decision.

### DRY Status Logic

The core status computation (`care_type_status`, `days_until_due`, `_summary_bucket`) is shared between the plant list and the summary section. Adding a new care type means adding one line to `CARE_TYPES` — no new functions.

### Walking Skeleton First

We built the thinnest working version (add plant, list, "never watered" status) before any other features. Each subsequent feature (mark watered, care types, due-soon list) grew on a stable base.

---

## What I Learned

This was the first project I built by writing down *what I was going to do before doing it*, and honestly it was a very different experience from just opening an editor and hacking away. Some things that surprised me along the way:

**Writing the spec first made me realize I didn't know what I wanted.** I thought "a plant tracker" was obvious, but sitting down to write requirements/plan/validation forced me to answer questions like *what does "overdue" even mean*, *should never-watered plants show up in the summary*, and *which care types should count*. Defining "done" on paper prevented me from half-adding a million ideas halfway through.

**Saying "no" was actually the easiest part.** Several times I caught myself wanting to add features. The validation file for each feature explicitly said what was out of scope, so I had a concrete reason to say "not this time" instead of a vague "maybe later." It felt weird to write down what I *wouldn't* build, but it made the project much more focused.

**Simple tools were a huge confidence boost.** We used vanilla HTML/CSS/JS, Flask, and SQLite. No React, no ORM, no build tools. When something broke, I could actually read the whole codebase in one sitting and understand it. I was a bit nervous at the start that the project would "need" a fancier stack, but it really didn't.

**The DRY thing finally clicked for me.** My first instinct with the fertilize and repot features was to copy the watering code and paste it for each. But we had a `CARE_TYPES` constant, so I added one line there instead. When I later added the summary list feature, the same constant was driving *that* too. It felt a bit magical that changing one tuple updated the form, the status logic, and the summary all at once — the result of remembering "don't repeat yourself" on the first try instead of after copy-pasting the same bug three times.

**Tests and specs turned out to be two sides of the same thing.** The checklist in each validation file became the test names. When the tests say `test_due_summary_never_done_plant_does_not_appear`, that's a requirement I can run. I found that way more approachable than "red/green testing" — I never got the hang of writing tests before the code, but writing them to confirm what the spec promised made sense.

**Lint is not a nag, it's a memory aid.** I thought ruff was just being pedantic until it flagged the timezone stuff. We disabled those rules, but only because we made a real decision about dates (stored as local dates, no timezone handling) — and we documented why. Now I get that a lint rule is either "this is a problem" or "we decided not to care, here's why." Both are useful.

**Small merges, often, was better than one big unveiling.** The app was usable after the very first tiny slice: add a plant, see it listed, see "never watered." That was a real, working product even though it was tiny, and every feature after that just built on it without breaking it. Big-bang "build everything then show me" would have been way more stressful and buggy.

---

## Project Constitution

The durable foundation lives in `SPECS/`:

- [`SPECS/MISSION.md`](SPECS/MISSION.md) — purpose, audience, non-negotiables
- [`SPECS/TECH.md`](SPECS/TECH.md) — stack, schema, engineering standards
- [`SPECS/ROADMAP.md`](SPECS/ROADMAP.md) — current state and planned features

Each feature has a dated spec folder under `SPECS/` with `requirements.md`, `plan.md`, `validation.md`:

- `2026-09-07-walking-skeleton` — add plant, list, never-watered status
- `2026-09-07-mark-watered` — mark plant watered, status updates
- `2026-09-07-care-types` — fertilize/repot schedules with shared status logic
- `2026-09-07-due-list` — overdue/due-soon summary section