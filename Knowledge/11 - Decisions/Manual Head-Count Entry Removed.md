---
tags: [decision, head-count]
status: Working Decision (2026-09-24)
---

# Manual Head-Count Entry Removed

## Decision
The manual head-count entry workflow has been removed from `admin-ui`.
Head counts are now recorded **exclusively** by the automated scheduler
([[Automated Head-Count Scheduler]]) — there is no manual-entry form, and
the `POST /api/headcounts` route no longer exists (`GET /api/headcounts`,
read-only, still exists to list history).

## Reason
Explicit user instruction: the manual-entry workflow was to be replaced by
"the existing automated head-count system so the count is generated from
the system's actual detection process," and the UI/backend/database/APIs
should no longer *require* manual head-count input.

Note the honest caveat: the automated scheduler's captured value
(`scheduler._capture_head_count()`) is still a simulated placeholder
(`random.randint(24, 32)`), not a real detection — there is no camera or
detection pipeline in this repo yet (see [[04 - Computer Vision]]). "The
system's actual detection process" does not yet exist; what exists is the
*scheduling and storage* architecture that a real detector would plug into
later, per [[Automated Head-Count Scheduler]]'s "Placeholder capture value"
section. This decision removes the manual fallback, it does not add real
detection.

## What changed
- `admin-ui/backend/app.py` — removed the `POST /api/headcounts` route
  (`record_headcount()`) and its now-unused `db` import.
- `admin-ui/backend/db.py` — `upsert_head_count()`'s default `source`
  changed from `'manual'` to `'scheduled'` (every real caller already
  passed `source` explicitly, so this is just a safer default). Schema
  still allows `source = 'manual'` in the `CHECK` constraint — narrowing
  that would require a full table rebuild in SQLite for no functional
  benefit, and pre-existing historical rows created before the `source`
  column existed are correctly backfilled as `'manual'` by
  `_migrate_head_counts_source_column()` (that migration's default is
  intentionally left as `'manual'` since those really were pre-scheduler,
  effectively-manual rows).
- `admin-ui/backend/seed.py` — `seed_headcounts()` now writes
  `source='scheduled'` explicitly for its synthetic historical sessions,
  so seeded demo history reads the same way real history now would.
- `admin-ui/frontend/js/views/headcount.js` — removed the "Manual Entry"
  form section (inputs, Record buttons, validation/feedback) and its event
  handler. The page now shows only "Today's Scheduled Head Counts" and
  "Recent Sessions."
- `admin-ui/frontend/js/api.js` — removed `Api.recordHeadcount()`.
- `admin-ui/frontend/css/styles.css` — removed the now-unused
  `.headcount-form`/`.headcount-field`/`.headcount-input-row`/`.form-error`
  rules.

## Alternatives
- Keep the manual form as a correction/override mechanism alongside the
  scheduler (this was the design right after the scheduler was first
  built) — rejected per explicit instruction to remove it, not merely
  demote it.

## May Change?
Possibly, if the project owners decide a manual override/correction
mechanism is still needed for real-world use (e.g. the automated capture
fails or is visibly wrong) — nothing currently in the repo provides a way
to correct a bad automated reading short of direct DB editing. This is a
new, real gap introduced by this decision; flagged here rather than in
[[12 - Open Questions]] since it's a direct consequence of this decision,
not a pre-existing ambiguity.

## Change Trigger
Explicit user/adviser direction to reintroduce a correction mechanism.

## Related
- [[Automated Head-Count Scheduler]]
- [[06 - Database]]
- [[Web Application as Sole Admin UI]]
