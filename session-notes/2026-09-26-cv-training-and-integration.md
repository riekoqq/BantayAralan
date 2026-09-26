# Session notes — 2026-09-26: CV training rounds + trash monitoring integration

Local-only context dump of a long working session. Not pushed to GitHub
(see `.gitignore`) — this is raw working narrative, not curated project
documentation. The durable, curated version of everything here already
lives in the repo itself (Knowledge vault, `CLAUDE.md` files,
`detection/dataset/README.md`'s round log) and was committed/pushed as
part of this session — read those first if you just want current project
state. This file is for reconstructing *how* we got there and *why*,
including dead ends, in case that context is useful later.

## Starting point

Repo had `detection/CLAUDE.md` + `detection/dataset/README.md` scaffolding
from an earlier session (dataset tracking docs only, no real code). Goal
for this session, set incrementally by the user: train a YOLO model on a
tiny hand-collected dataset, test it against a real IP camera, and
eventually wire it into `admin-ui`.

## Round 1 (7 images) — confirmed as a failure, but a useful one

- 7 screenshots from the VIGI camera, all `trash` class, zero negative
  examples, no augmentation. Trained `yolov8n.pt` locally on the user's
  RTX 2060.
- Validation metrics were bad (precision 0.006) but the *real* diagnostic
  came from testing against the live camera: the model had memorized a
  fixed screen location (a wall outlet) and fired "trash" there in ~62% of
  frames regardless of scene content, plus a second fixed false-positive
  on a person's neck/collar. Confidence never exceeded 0.26.
- Root cause: single-digit images, one class, zero negatives → the model
  had nothing to contrast against, so it learned "something's usually
  around this pixel" instead of "what clutter looks like."
- This became the concrete argument for round 2's changes, documented in
  `detection/dataset/README.md`.

## Round 2 (23 images) — real improvement, new specific failure modes

Changes made based on round 1's diagnosis: added `misaligned` class (7
boxes, thin), added negative examples (5, all in train split only — gap:
none in valid/test), varied item position/scene across shots, restricted
`trash` labeling to floor-only items (working decision), mixed rooms +
phone photos for variety.

Result: validation metrics improved a lot (P 0.672 vs 0.006) but more
importantly, live-camera testing showed the model reacting to real scene
content — high-confidence (up to 1.00) detections on actual floor items,
including items never seen in training, not fixed positions. Confirmed
this was real generalization, not luck, by testing twice: once on the
original arrangement, once after the user deliberately moved items
around (including items not in the training set) — same real detections.

New failure modes found, all documented in the round log because they're
specific and actionable, not just "needs more data":
1. **Chair/trash confusion**: an unlabeled chair sitting in the same
   floor region as real trash started getting weakly flagged as `trash`
   (~0.3-0.4 conf). No `seat` class exists, so the model has no signal
   that furniture in that zone isn't clutter.
2. **Occlusion inconsistency**: partially covering items with a foot —
   some (a belt) still detected, others (a powerbank, a small box) not.
   Not a bug, just insufficient data to have learned real occlusion
   robustness.
3. **Person/clothing false positives**: this is the pattern worth
   remembering most. Round 1 had a false positive on a neck/collar.
   Round 2, tested live via `monitor_trash.py`, produced a false positive
   directly on a shirt's chest graphic (`trash 0.56`) while the person was
   crouching near floor level. Two independent rounds, two different
   people-related false positives — the dataset has never included a
   deliberate negative example of "a person near/at floor level, no
   clutter present." This is the clearest concrete ask for round 3.

## Architecture tangent: `misaligned` probably needs a different design

Realized partway through that `trash` and `misaligned` aren't the same
kind of problem. `trash` is a property of the object's appearance —
context-independent. `misaligned` is inherently relational ("is this
chair where it should be") — the proposal's own original description
("seat/table alignment vs. defined reference positions and thresholds",
`04 - Computer Vision.md`) implies a two-stage design: detect `seat`/
`table` as plain objects, then a **separate rule-based** position/distance
check against a stored reference — not a single end-to-end visual
`misaligned` class. Recommended, not yet built. See
`detection/dataset/README.md` for the full reasoning and the practical
relabeling plan (existing `misaligned` boxes become generic `seat` boxes).

## Live camera testing — operational gotchas worth remembering

- **Testing methodology bug I made and fixed**: re-analyzing an
  already-`save=True`-annotated output video (boxes burned into the
  pixels) as if it were a fresh source contaminates the second pass —
  found almost nothing where the live run had clearly detected things.
  Fix: always do `save=True save_txt=True save_conf=True` together in one
  clean pass, never record-then-reanalyze.
- **Ultralytics' default `project=`/`runs_dir` behavior nests oddly** with
  a relative `project=` path — landed output at
  `runs/detect/detection/runs/...` at repo root more than once. Use an
  **absolute** `project=` path to avoid it. Also, plain `model.predict()`
  saves annotated output **by default** even without asking — pass
  `save=False` explicitly if you don't want that (this is what created a
  stray root-level `runs/` folder once, cleaned up).
- **RTSP stream stalls happened for real, more than once** — Ultralytics
  logs repeated `WARNING Waiting for stream 0` when this happens (that's
  its own internal source-list index, unrelated to the camera's own
  `/stream1` URL path naming — confirmed this misunderstanding directly
  with the user). Two real causes found by elimination (checked: not my
  tracker's logic, not a leftover local process, not the camera's own web
  Live View tab left open — though that's still worth closing as a first
  check): most likely a low concurrent-RTSP-connection limit on this
  camera, compounded by **repeated rapid kill/restart cycles during
  troubleshooting leaving stale half-open sessions on the camera's own
  side** that need real time (tens of seconds+) to time out. Power-cycling
  the camera fixed it that time. No auto-reconnect exists in
  `monitor_trash.py` — this is a documented, not fixed, limitation.

## Trash monitoring integration (the actual feature work)

User wanted: don't re-log the same physical trash item repeatedly, and
mark it resolved once it's gone. This required two real decisions,
surfaced explicitly rather than picked silently, because both touched
existing documented decisions:

1. **`events.status` (`active`/`resolved`)** — reverses the earlier "No
   Event-Status Field" decision. User explicitly chose a real schema
   field over (a) permanent no-status records or (b) free-text-only
   removal notes.
2. **One-off manual script, not an always-on service** — user chose this
   over building a proper background service (like the head-count
   scheduler) with restart/error-handling. Revisit once the model is more
   trustworthy.

Built `detection/monitor_trash.py`:
- In-memory position-based dedup (nearest-match within a normalized
  distance), **not** ByteTrack — deliberately simpler, fine for a
  mostly-static overhead camera.
- **Two confidence thresholds, added after finding a real bug from live
  testing**: a single shared threshold let a borderline (~0.3) flickering
  detection spam create/resolve cycles within seconds. Fixed with
  `--conf` (keep-tracking threshold, lower) vs. `--min-new-conf`
  (new-event threshold, higher).
- **Miss-grace switched from frame-count to wall-clock seconds** — a
  frame-count grace period measured at under a second of real time in
  practice (RTSP processing speed varies), nowhere near enough to bridge
  a brief flicker.
- **Known, documented limitation**: tracked positions live only in the
  running process's memory. Restarting the script loses track of
  everything open — orphans old `active` events (had to manually
  `db.resolve_event()` a batch of these — ids 95-98 — after confirming
  with the user the physical items were actually gone).

Then, follow-up features added same day after the user noticed gaps:
- **Real snapshot capture**: saves the triggering frame (box drawn on it)
  to `admin-ui/data/snapshots/<event_id>.jpg`, served by a renamed
  `/api/events/<id>/snapshot` route (falls back to the old placeholder
  SVG for mock events). **Flagged, not fixed**: no face/identity
  redaction on these raw captures — a real privacy gap given the whole
  project's premise is not capturing identifiable content. User was asked
  to choose between crop-tighter / face-blur / leave-as-known-gap and
  hadn't picked by the time we moved on — worth following up.
- **Live polling** in `admin-ui` (`app.js`'s `startPolling`/`stopPolling`,
  4s interval) so Dashboard/Events/Event-Detail don't need a manual
  refresh. Deliberately polling, not push (WebSocket/SSE), to keep the
  existing "reviewed periodically, not instant alerts" UI framing intact.
  Verified this actually works by instrumenting `window.fetch` in the
  browser and measuring real request timestamps — first measurement
  looked broken (12 requests in 10s) but that was noise from a messy
  multi-navigate test sequence, not a real bug; a clean retest showed
  correct ~4000ms spacing.

## Git / GitHub state at end of session

- Everything committed in one commit (`9d38aca`, "Add live trash
  detection integration and round 2 CV dataset work") and pushed to
  `origin/master` (`riekoqq/BantayAralan`).
- Checked carefully before committing that the camera's real RTSP
  password never leaked into any tracked file (it appeared constantly in
  raw Bash commands throughout this session, but never in a file) —
  `git grep` for the password and for `rtsp://admin:` both came back
  clean/redacted.
- Added two GitHub collaborators with push access: `Chloe-Lane` and
  `RaynierRonnSantos` (invites sent via `gh api`, pending acceptance as of
  end of session).

## Open items for next session

- Round 3 dataset: still short of the 50+ image target; add `seat` class
  (relabel existing `misaligned` boxes as `seat`, add more chair photos in
  varied positions); add person-near-floor negative examples specifically
  (the clearest actionable finding from round 2); add negatives to
  valid/test splits, not just train.
- Decide and implement the snapshot face/redaction approach.
- Consider moving `monitor_trash.py` into a real background service once
  the model is trustworthy enough to justify it.
- Real video evidence capture, retention policy decision, and test
  coverage are all still fully open (see `Knowledge/12 - Open
  Questions.md`).
