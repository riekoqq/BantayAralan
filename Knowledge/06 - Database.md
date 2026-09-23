---
tags: [database]
status: Implemented
---

# Database

SQLite, used identically (same schema) by both admin-UI prototypes — but as **two separate database files and two separate code copies**, not a shared database.

## Implementation
| | `admin-ui` | `desktop-app` |
|---|---|---|
| File | `admin-ui/backend/db.py` (schema/connection) + `backend/seed.py` (mock data) | `desktop-app/app/data.py` (schema, connection, seeding, and query functions all in one module) |
| DB location | `admin-ui/data/bantayaralan.db` | `desktop-app/data/bantayaralan.db` |
| Access pattern | `sqlite3` via Flask route handlers (`backend/app.py`) | `sqlite3` called directly, in-process, from Qt views (`app/views.py`) |

## Schema
One table, `events` — see [[Event Model]] for the full column list and category values.

## Lifecycle
- `init_db()` creates the table if missing (idempotent, `CREATE TABLE IF NOT EXISTS`).
- `seed()` populates ~42 synthetic rows **only if the table is empty** — editing the seed generator has no visible effect until the `.db` file is deleted and the app is re-run.
- No migrations system — schema changes require manually updating both copies (`admin-ui/backend/db.py` and `desktop-app/app/data.py`) and deleting existing `.db` files.

## Proposed extensions (Not Yet Implemented)
Real video evidence would need at least a `video_path`/`video_url` column (see [[Evidence System]]). No other schema changes are specified in current docs.

## Status
**Implemented** (mock schema, both prototypes). **Not Yet Implemented**: any write path from real detection, any schema for confidence scores, camera source, or video/audio file references beyond the flags already present.

## Related
- [[Event Model]]
- [[Two Admin UI Prototypes]]
- [[Evidence System]]
