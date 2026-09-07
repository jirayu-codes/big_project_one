# Project Brainstorming

## Idea 1 — Plant Care Tracker
- **Problem:** It is easy to forget when to water, fertilize, or repot your plants. Each plant has different needs and there is no easy way to keep track of them all.
- **Who experiences this:** People who own houseplants or garden plants and have more than a couple to look after.
- **Why it matters:** A tracker helps keep plants healthy and alive by reminding you of each plant's care schedule, so you do not have to rely on memory.

## Idea 2 — Study Habit Tracker
- **Problem:** Students often do not know how much time they actually spend studying, or how consistent their study habits are.
- **Who experiences this:** Students who want to build better study routines and see their progress over time.
- **Why it matters:** Tracking study sessions makes habits visible, which helps students stay motivated and see what is working.

## Idea 3 — Book Borrowing Log
- **Problem:** When you lend books to friends or family, it is easy to lose track of who has which book or when it was borrowed.
- **Who experiences this:** People who lend books and want to remember who borrowed what and when it should come back.
- **Why it matters:** A log keeps track of borrowed books so nothing gets lost and you know who to ask to return a book.

---

## Selected Project
- **App Name:** PlantPal
- **Target User:** People who own houseplants or garden plants and want to keep track of their care needs.
- **Core Problem:** It is easy to forget when to water, fertilize, or repot each plant, especially when you have several with different needs.
- **Purpose:** PlantPal lets you store a list of your plants and track when each one needs care, so nothing gets forgotten and your plants stay healthy.

---

## Core Requirements
- Add a plant (name and how often it needs water) and see it listed.
- See when each plant is next due to be watered.
- Mark a plant as watered so its due date updates.

---

## Non-Goals
- No sharing or exporting data.
- No user accounts or login — it's a single-user app.
- No care history log — only the last watered date is tracked.

---

## Database Questions

For each core requirement, write the specific question your database must be able to answer to make it work.

- Requirement 1 (Add a plant) → What is each plant's name, and how often does it need water?
- Requirement 2 (Next due date) → What was the last date each plant was watered, and how often does it need water?
- Requirement 3 (Mark watered) → Which plant was just watered, and what is today's date?

---

## Schema

```
Table: plants
- id:            INTEGER PRIMARY KEY AUTOINCREMENT
- name:          TEXT     # the name of the plant
- water_every:   INTEGER  # how many days between watering
- last_watered:  TEXT     # the date the plant was last watered; may be empty/never if not watered yet
```

<!-- Add a second table block here if your app needs one. -->

