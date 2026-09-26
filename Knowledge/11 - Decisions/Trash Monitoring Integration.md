---
tags: [decision, computer-vision, events]
status: Working Decision (2026-09-26)
---

# Trash Monitoring Integration

## Decision
A new script, [`detection/monitor_trash.py`](../../detection/monitor_trash.py),
runs a trained `trash` detector against a live camera (or video file) and
writes real events into `admin-ui`'s database — the first time any code in
this repo connects a detection model to the admin UI's data. Two scope
decisions were made explicitly with the user before building this:

1. **Add a real `events.status` field** (`active`/`resolved`) — this
   reverses [[No Event-Status Field]], not works around it. The user chose
   this over (a) leaving events as permanent historical records with no
   removal indication, or (b) appending removal notes to the free-text
   description without a schema change.
2. **One-off script, not a persistent service** — run manually, not
   started automatically with the app (unlike the head-count scheduler).
   The user chose this over building a proper always-on background service
   with its own restart/error-handling story.

## Reason
The user asked to "mark only the same trash placed in the same place once,
and once removed, maybe mark it as resolved" — i.e., deduplicate by
position and track a lifecycle, which the existing schema had no field for.
Rather than silently reversing the documented no-status-field decision or
silently picking a lighter workaround, both options (and the integration
scope) were presented to the user directly; see the conversation this
decision came from for the exact choices offered.

## What changed
- `admin-ui/backend/db.py` — `events.status` column (schema + migration for
  pre-existing DBs, backfilled to `'resolved'`), `insert_event()`,
  `resolve_event()`, `list_active_events()`.
- `admin-ui/backend/seed.py` — all seeded/historical events explicitly
  `status='resolved'` (closed-out mock history, never "still open").
- `admin-ui/backend/app.py` — `_serialize_event()` includes `status`.
- `admin-ui/frontend/js/components.js` (+ `icons.js`, `styles.css`,
  `eventDetail.js`) — `statusTagHtml()` badge, active=warning/
  resolved=success tokens (both already had dark-mode variants).
- `detection/monitor_trash.py` — new script; see its own docstring and
  [`detection/CLAUDE.md`](../../detection/CLAUDE.md) for the dedup/resolve
  design (position-based matching in memory, wall-clock miss-grace, two
  confidence thresholds to avoid a flicker-driven create/resolve loop —
  all three found necessary from actually running it against the live
  camera, not decided upfront).
- **Snapshot capture** (same day, follow-up): the user noticed real events
  had no real screenshot evidence — `monitor_trash.py` now saves the
  triggering frame (box drawn on it) to `admin-ui/data/snapshots/<id>.jpg`
  on each new event, and `app.py`'s snapshot route (renamed from
  `/snapshot.svg` to `/snapshot`) serves the real file when present, falling
  back to the placeholder SVG otherwise. **Known gap, flagged not fixed**:
  no face/identity redaction — a raw camera frame can include an
  identifiable person. See [[Evidence System]] and
  [.claude/rules/privacy-and-ethics.md](../../.claude/rules/privacy-and-ethics.md).
  Left as-is for now at the user's implicit priority (fixing the missing
  evidence first); revisit before any real classroom use.
- **Live polling** (same day, follow-up): the user asked that the admin UI
  not require a manual refresh to see new/resolved events. Added
  `startPolling()`/`stopPolling()` in `frontend/js/app.js` (4s interval),
  used by the Dashboard, Events list, and Event Detail views — silent
  background refresh, not push (no WebSocket/SSE), to keep this project's
  existing "reviewed periodically, not instant alerts" UI framing intact.
  See `admin-ui/CLAUDE.md`'s "Live polling" section for the per-view detail.

## Alternatives considered (events.status)
- No status field, events stay permanent records — rejected by the user in
  favor of a real status field.
- Append removal notes to the description text, no schema change — same,
  rejected in favor of a real field.

## Alternatives considered (integration scope)
- A real always-on background service (like the head-count scheduler) —
  rejected for now in favor of a manual one-off script; bigger addition
  (restart behavior, error handling, its own subsystem docs) than the
  current model maturity justifies. Revisit once the detector itself is
  more trustworthy (see the round log's ongoing gaps — `misaligned`,
  dataset size, chair/trash confusion).

## May Change?
Yes — once the model is more mature, moving `monitor_trash.py`'s logic into
a real background service (started with `create_app()`, like the
scheduler) is the natural next step. The position-tracking approach may
also need to change if it starts covering `misaligned` too, since that
class needs the seat/reference-position architecture discussed separately
(see `detection/dataset/README.md`), not the same by-position dedup used
for `trash`.

## Change Trigger
Model maturity improving enough to trust an always-on service, or
`misaligned` monitoring being added (which needs different tracking logic
than position-based dedup).

## Related
- [[No Event-Status Field]]
- [[Event Model]]
- [[04 - Computer Vision]]
- [[06 - Database]]
