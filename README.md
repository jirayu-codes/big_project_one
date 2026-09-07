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

Building PlantPal was a masterclass in **discipline over cleverness**. A few things that stuck:

**Specs prevent scope creep.** Writing requirements/plan/validation before code forced me to define "done" upfront. When I wanted to add "mark as fertilized" mid-feature, the validation.md said "out of scope" — so I didn't. That feature is now a deliberate future item, not a half-baked distraction.

**Simple tools are underrated.** Vanilla HTML/CSS/JS + Flask + SQLite is *plenty* for a real app. No webpack, no ORM, no migrations library — just code I can read and understand in one sitting. The `ensure_schema()` pattern (check PRAGMA table_info, ALTER TABLE if missing) is 20 lines and handles migrations better than many frameworks.

**DRY is a design tool, not just a cleanup rule.** The `CARE_TYPES` constant drives the schema, the form, the status logic, the summary, and the tests. When I added "repot", I changed one tuple and everything else worked. That only happened because I resisted the urge to copy-paste water logic for fertilize.

**Tests as executable spec.** The validation.md checklist became the test names. `test_due_summary_never_done_plant_does_not_appear` isn't just a test — it's a requirement you can run. When the verifier agent checked off every validation row, it was running the same mental model.

**Lint rules should have reasons, not just exceptions.** The `ruff.toml` DTZ disable isn't "we don't care about timezones" — it's "we decided dates are local on purpose, documented in TECH.md, and here's the comment pointing to it." That's the difference between technical debt and a conscious tradeoff.

**Iterative delivery beats big bang.** Four PRs, each merging a thin vertical slice, meant the app was deployable after PR #1. Every merge was a working product. That's the walking skeleton philosophy in action.

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