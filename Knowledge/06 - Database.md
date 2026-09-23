---
tags: [database]
status: Implemented
---

# Database

SQLite, used by `admin-ui/` (the sole admin UI). A separate `desktop-app/`
prototype had its own copy of this schema/data layer through 2026-09-23,
when it was removed — see [[Web Application as Sole Admin UI]].

## Implementation
| | `admin-ui` |
|---|---|
| File | `admin-ui/backend/db.py` (schema/connection) + `backend/seed.py` (mock data) |
| DB location | `admin-ui/data/bantayaralan.db` |
| Access pattern | `sqlite3` via Flask route handlers (`backend/app.py`) |

## Schema
Three tables:
- `events` — see [[Event Model]] for the full column list and category values.
- `head_counts` — aggregate student head counts at the beginning/end of a
  class session (`class_date`, `point` IN `start`/`end`, `count`,
  `recorded_at`). Aggregate only, no per-student data.
- `detection_state` — single row (`id = 1`) persisting whether
  detection/event-generation is enabled (`enabled`, `updated_at`). Gates
  event generation only, independent of cameras/monitoring/head counting.

## Lifecycle
- `init_db()` creates all tables if missing (idempotent, `CREATE TABLE IF NOT EXISTS`), and ensures a default `detection_state` row exists.
- `seed()` populates ~42 synthetic events and ~10 synthetic head-count sessions **only if those tables are empty** — editing the seed generator has no visible effect until the `.db` file is deleted and the app is re-run.
- No migrations system — schema changes require manually updating `admin-ui/backend/db.py` and deleting the existing `.db` file.

## Proposed extensions (Not Yet Implemented)
Real video evidence would need at least a `video_path`/`video_url` column (see [[Evidence System]]). No other schema changes are specified in current docs.

## Status
**Implemented** (mock schema). **Not Yet Implemented**: any write path from
real detection, any schema for confidence scores, camera source, or
video/audio file references beyond the flags already present. Head-count
duplicate-handling and detection-toggle's real backend scope remain open —
see [[12 - Open Questions]].

## Related
- [[Event Model]]
- [[Two Admin UI Prototypes]]
- [[Evidence System]]
