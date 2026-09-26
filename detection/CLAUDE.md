# detection — BantayAralan CV Dataset, Training & Trash Monitoring

Status: **Partially implemented**. Dataset/training work is still a
proof-of-concept (see the round log), but real inference code now exists:
[`monitor_trash.py`](monitor_trash.py) runs a trained model against a live
camera (or video file) and writes real `trash` events into admin-ui's
database, and [`live_view.py`](live_view.py) is a standalone real-time
viewer independent of admin-ui. See root [`CLAUDE.md`](../CLAUDE.md) for
the project-wide working-draft/status-label rules; this file assumes
you've read those.

## Setup

```bash
pip install -r detection/requirements.txt
```
See that file's comments for GPU (CUDA) torch install notes — a plain
`pip install` gets you a working CPU-only setup, but you want the CUDA
build first if you have an NVIDIA GPU (see `detection/requirements.txt`).
This is separate from `admin-ui/requirements.txt` — installing one doesn't
install the other; you need both if you're running `monitor_trash.py`
alongside the web app.

Also needs a trained model's `.pt` weights and, if you want to
retrain/relabel, the labeled dataset itself — **neither is in git**
(`*.pt` and the dataset image folders are gitignored on purpose, see
`.gitignore`). A fresh clone of this repo has no trained model and no
training data; both have to be transferred separately (not via git) from
wherever they were trained, or retrained from scratch via a new Roboflow
export — see `dataset/README.md`.

## What actually exists here

- [`dataset/README.md`](dataset/README.md) — class taxonomy and a log of
  labeling/training rounds done in an external no-code tool (Roboflow).
- `dataset/` (gitignored) — the current round's exported images/labels once
  you've unzipped a Roboflow export here.
- `runs/` (gitignored) — local training output (`yolo detect train`) and
  ad-hoc camera-test recordings/analysis.
- [`monitor_trash.py`](monitor_trash.py) — runs a trained model against a
  live camera and writes real `trash` events into admin-ui's database
  (dedup/resolve lifecycle). See its own docstring for full detail;
  summary below.
- [`live_view.py`](live_view.py) — standalone real-time viewer, no
  database, no admin-ui dependency at all. Opens an OpenCV window showing
  every class the model detects, live, with an FPS counter. Deliberately
  **not** a GUI application (no Tkinter/PyQt) — the proposal leaves "which
  GUI framework for the integrated CV + GUI system" as an explicit open
  question ([12 - Open Questions.md](<../Knowledge/12%20-%20Open%20Questions.md>));
  a plain `cv2.imshow` window sidesteps that decision rather than silently
  answering it. **Must be run in a terminal with a real display attached**
  — `cv2.imshow` opens a native window and won't work headless/remote:
  ```bash
  python detection/live_view.py \
      --model detection/runs/train2/weights/best.pt \
      --source "rtsp://user:pass@<camera-ip>:554/stream1"
  ```
  Press `q` in the window to quit.

## monitor_trash.py

A **one-off script**, not a persistent background service (see
[Knowledge/11 - Decisions/Trash Monitoring Integration.md](<../Knowledge/11%20-%20Decisions/Trash%20Monitoring%20Integration.md>)
for why that scope was chosen). Run it manually:

```bash
python detection/monitor_trash.py \
    --model detection/runs/train2/weights/best.pt \
    --source "rtsp://user:pass@<camera-ip>:554/stream1"
```

- Only handles `trash` — `misaligned` is still too data-thin to trust (7
  training boxes as of round 2) and isn't wired up.
- Imports `admin-ui/backend/db.py` directly (adds `admin-ui/` to
  `sys.path`) rather than duplicating schema/DB logic — the two subsystems
  now share that module.
- **Dedup + resolve**: tracks each active event's last-known position in
  memory (not in the database) and matches new detections to it by
  proximity. A genuinely new position opens a new event; a tracked item
  unseen for `MISS_GRACE_SECONDS` (wall-clock, not frame count — see the
  script's docstring for why frame-count grace measured under a second of
  real time in testing) gets marked resolved. This is a simple
  nearest-position match, **not** the proposal's ByteTrack.
- **Two confidence thresholds, found necessary from live testing**:
  `--conf` (default 0.3) keeps tracking an already-open item; `--min-new-conf`
  (default 0.5, higher) is required to open a *new* event. A single shared
  threshold produced a rapid create/resolve/create/resolve loop for a
  borderline (~0.3) flickering detection during testing — see the round log
  for that finding.
- **Known limitation**: tracked positions live only in this process's
  memory. Restarting the script mid-session loses track of what was already
  open, so a still-present item gets logged as a new event rather than
  recognized as already active — and, conversely, an item removed while the
  script *wasn't* running leaves its old event permanently `active` with
  nothing watching to resolve it (has to be resolved manually via
  `db.resolve_event()`). Documented, not fixed — fixing it would mean
  persisting position data on the event, out of scope for a one-off script.
- **Snapshot capture**: on each new event, saves the triggering frame (with
  the detection box drawn on it) to `admin-ui/data/snapshots/<event_id>.jpg`
  and passes `snapshot_available=1`. `admin-ui/backend/app.py`'s
  `/api/events/<id>/snapshot` route serves this real file when present,
  falling back to the placeholder SVG otherwise (same route, same URL,
  either way — see [[Evidence System]]). **No face/redaction is applied** —
  a raw camera frame can include an identifiable person; flagged as a known
  gap in [Knowledge/11 - Decisions/Trash Monitoring Integration.md](<../Knowledge/11%20-%20Decisions/Trash%20Monitoring%20Integration.md>),
  not fixed yet. Revisit before pointing this at a real classroom.
- **RTSP reliability, found from actually running this against a real
  camera**: the stream can stall (`ultralytics` logs repeated "Waiting for
  stream 0") for reasons outside this script's control — most likely a low
  concurrent-connection limit on consumer IP cameras (a second RTSP client,
  e.g. the camera's own Live View left open in a browser tab, can starve
  this script's connection) or a stuck session from a previous ungraceful
  kill of this same script needing time to time out on the camera's side.
  No auto-reconnect logic exists — if the stream stalls, kill and restart
  the script (and close any other client connected to the camera first).

## Do not commit

- Raw or labeled classroom photos, exported dataset archives, or trained
  model weights (`.pt`, `.onnx`, etc.). See `.gitignore` — these are
  excluded on purpose. They're large binary/derived artifacts that don't
  belong in git history, not (as far as this dataset goes) identity-bearing
  content — but treat any future image that happens to include a
  recognizable student the same way regardless: don't commit it, and see
  [.claude/rules/privacy-and-ethics.md](../.claude/rules/privacy-and-ethics.md).
- Any Roboflow/cloud-tool API key or credential, or a camera RTSP URL with
  real credentials embedded — those are secrets, not project config. Never
  hardcode one into a script or commit it; pass it via `--source` at
  runtime.

## Class taxonomy

Reuses the `events.category` values defined in `admin-ui/backend/db.py` /
[[Event Model]] rather than inventing new label names, so the detector's
output maps onto the existing schema without a translation layer:

- `trash` — "Trash / Scattered Objects" (clutter), **floor-only** by
  working decision (2026-09-26) — see `dataset/README.md`'s Classes section.
- `misaligned` — "Misaligned Seat" / Table. Per the architecture discussion
  in the round log, this likely needs a separate `seat` object class plus a
  rule-based reference-position check, not a single end-to-end visual
  class — see `dataset/README.md` before adding more `misaligned` boxes.

Only these two are in scope for the top-down/clutter camera dataset. The
`standing` category belongs to the separate behavior-detection camera
pipeline (ceiling-mounted) and is out of scope here.

## Honest scale caveat

Any dataset here starting in the single digits to low tens of images is a
**pipeline proof-of-concept**, not a usable detector — don't let a
successfully-exported model from a tiny dataset be described in the paper
as validated or production-ready. Log the actual image count per class in
`dataset/README.md`'s round log so this stays checkable later. The same
caveat applies to any event `monitor_trash.py` writes into admin-ui's
database — they're real detections from a real (if immature) model, not
synthetic seed data, but the model's own accuracy is still unproven at
scale. Don't present a `monitor_trash.py` demo as validated detection
accuracy for the same reason.
