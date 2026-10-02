---
date: 2026-10-01
purpose: Short recorded demo script — admin UI + live CV detection
status: Prototype demo, not thesis-final results
---

# BantayAralan — Short Demo Script

Narration notes for a short recorded demo, focused on showing what
currently works. Roughly 3–4 minutes read at a normal pace. Pulls only
from what's actually implemented and tested as of 2026-10-01 — see
[detection/dataset/README.md](detection/dataset/README.md) and
[Knowledge/04 - Computer Vision.md](<Knowledge/04 - Computer Vision.md>)
for the full detail behind every number here.

## 1. What this is (30s)

"BantayAralan is a computer-vision system that helps teachers catch
classroom disruption and disorder — right now, specifically a student
**standing up** and **trash/clutter on the floor** — without doing any
facial recognition or identifying individual students. It logs each
detection as an event the teacher can review, instead of trying to make
disciplinary decisions on its own."

## 2. What's actually built today (1 min)

Two working pieces, both real, running code — not mockups:

- **Admin UI** (`admin-ui/`): the dashboard, event log, filters, evidence
  viewer, detection toggle. This is the system of record a teacher would
  actually use.
- **Detection pipeline** (`detection/monitor.py`): a trained YOLOv8n
  model watching a live camera feed, writing real `trash` and `standing`
  events straight into the same database the admin UI reads from — not
  synthetic seed data.

"As of yesterday, both `trash` and `standing` come from **one trained
model**, both trained the same way, both writing real events."

## 3. Latest training round — round 4 (1 min)

"We just finished round 4 of training: 47 labeled images (43 train / 2
valid / 2 test), `yolov8n`, trained locally on an RTX 2060, 150 epochs,
about 2 minutes.

Validation numbers on the held-out split:

| Class | Precision | Recall | mAP50 | mAP50-95 |
|---|---|---|---|---|
| `trash` | 0.70 | 0.50 | 0.615 | 0.38 |
| `standing` | 0.97 | 1.00 | 0.995 | 0.896 |

`trash` improved over our last documented round (mAP50 0.47 → 0.62).
`standing` is brand new as a trained class this round."

## 4. Live demo (1–2 min)

Run `detection/live_view.py` against the real camera (visual-only, writes
nothing to the database — safe to demo without creating fake events):

```bash
python detection/live_view.py --model detection/runs/train4/weights/best.pt --source "rtsp://..."
```

"This is the model running live, not a recording. Red boxes are `trash`,
and you'll see `standing` boxes appear when I stand up."

Then switch to `detection/monitor.py`, and pull up the admin UI dashboard
in a browser tab to show a real event actually appearing after standing
up or placing an item on the floor — the same detection, now writing into
the system a teacher would actually use.
