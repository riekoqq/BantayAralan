"""One-off script: run the trash detector against a live camera (or a video
file) and write real `trash` events into admin-ui's database, instead of
that database only ever holding synthetic seed data.

Not a persistent background service (see the "Integration scope" decision
in detection/dataset/README.md / detection/CLAUDE.md) -- run it manually
whenever you want a demo or a test, and stop it with Ctrl+C:

    python detection/monitor_trash.py \
        --model detection/runs/train2/weights/best.pt \
        --source "rtsp://user:pass@192.168.100.126:554/stream1"

Only the `trash` class is handled -- `misaligned` is still too data-thin to
trust (see the round log) and isn't wired up here.

Dedup/resolve logic: the same physical item shouldn't create a new event on
every frame, and an item that gets cleaned up should stop showing as open.
This script tracks each active event's last-known position in memory (not
in the database -- see Knowledge/05 - Events & Evidence/Event Model.md on
why no bbox/frame linkage is stored there) and does simple nearest-position
matching per frame: close enough to a tracked item = same item, no new
event; a tracked item unseen for MISS_GRACE_SECONDS of wall-clock time =
resolved. This is deliberately much simpler than the proposal's ByteTrack --
good enough for a mostly-static overhead camera in a one-off script, not a
production tracking solution.

Two thresholds, not one -- found necessary from an actual live test, not
just theory: a detection right at `--conf` will inherently flicker in and
out frame to frame, and a naive single-threshold tracker turns that flicker
into a rapid create/resolve/create/resolve loop for what's really one
(possibly still spurious) signal. `--conf` governs whether an *already
tracked* item still counts as present; `--min-new-conf` (higher) is the bar
for creating a *new* event in the first place, so a borderline flicker
doesn't spam new rows. MISS_GRACE_SECONDS uses wall-clock time rather than
a frame count because RTSP processing speed varies -- a frame-count grace
period was measured at under a second of real time in practice, nowhere
near enough to bridge a brief flicker or occlusion.

Known limitation: tracked positions live only in this process's memory. If
you stop and restart the script while an item is still on the floor, the
restarted script has no record of the earlier event's position, so it will
log a new event for the same physical item rather than recognizing it as
already open. Resolving that would mean persisting bbox/position data on
the event, which is out of scope for this one-off script.

Snapshot evidence: the frame that triggered a new event is saved (with the
detection box drawn on it) to admin-ui's data/snapshots/<event_id>.jpg, and
the event is inserted with snapshot_available=1. admin-ui/backend/app.py's
/api/events/<id>/snapshot route serves this real file when present, falling
back to the existing placeholder-SVG behavior for seeded/mock events that
have no real file. No snapshot is saved for a resolved event (nothing new
to show), and there's no video evidence here at all -- see
Knowledge/05 - Events & Evidence/Evidence System.md for that gap.
"""
import argparse
import sys
import time
from pathlib import Path

import cv2

REPO_ROOT = Path(__file__).resolve().parent.parent
ADMIN_UI_ROOT = REPO_ROOT / "admin-ui"
sys.path.insert(0, str(ADMIN_UI_ROOT))

from backend import db  # noqa: E402

from ultralytics import YOLO  # noqa: E402

SNAPSHOTS_DIR = ADMIN_UI_ROOT / "data" / "snapshots"

# Normalized (0-1) center-distance below which two detections across
# frames are treated as the same physical item rather than a new one.
MATCH_DISTANCE = 0.05

# Wall-clock seconds a tracked item can go undetected before its event is
# marked resolved (absorbs brief occlusion/flicker, not just one bad frame).
MISS_GRACE_SECONDS = 5.0


def _center_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _save_snapshot(frame, event_id, box_norm, conf):
    """Draw the triggering box on a copy of `frame` and save it as this
    event's snapshot. Best-effort: a failure here just means the event ends
    up without a real snapshot (falls back to the placeholder, same as any
    seeded event) -- not worth crashing the whole monitor over."""
    try:
        SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        h, w = frame.shape[:2]
        cx, cy, bw, bh = box_norm
        x1, y1 = int((cx - bw / 2) * w), int((cy - bh / 2) * h)
        x2, y2 = int((cx + bw / 2) * w), int((cy + bh / 2) * h)
        annotated = frame.copy()
        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.putText(annotated, f"trash {conf:.2f}", (x1, max(0, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imwrite(str(SNAPSHOTS_DIR / f"{event_id}.jpg"), annotated)
    except Exception as exc:  # best-effort -- see docstring
        print(f"[warn] could not save snapshot for #{event_id}: {exc}")


class TrashTracker:
    def __init__(self, category: str, label: str, min_new_conf: float):
        self.category = category
        self.label = label
        self.min_new_conf = min_new_conf
        # event_id -> {"center": (x, y), "last_seen": float (time.time())}.
        # Starts empty every run -- see "Known limitation" in this file's
        # docstring.
        self.tracked = {}

    def update(self, detections, frame=None):
        """detections: list of (cx, cy, bw, bh, conf) normalized boxes for
        this frame's `trash` detections (already filtered to >= --conf by
        the caller). Matches to an existing tracked item regardless of its
        confidence (once real, still count it even if it dips); only
        requires `min_new_conf` to START a new event, so a borderline
        flicker doesn't spam new rows. Resolves events unseen for
        MISS_GRACE_SECONDS. `frame` (a raw BGR image) is used to save a
        snapshot when a new event is created -- optional so tests/other
        callers can still call this without one."""
        now = time.time()
        matched_ids = set()
        for cx, cy, bw, bh, conf in detections:
            best_id, best_dist = None, None
            for event_id, state in self.tracked.items():
                if event_id in matched_ids:
                    continue
                dist = _center_distance((cx, cy), state["center"])
                if dist <= MATCH_DISTANCE and (best_dist is None or dist < best_dist):
                    best_id, best_dist = event_id, dist

            if best_id is not None:
                self.tracked[best_id]["center"] = (cx, cy)
                self.tracked[best_id]["last_seen"] = now
                matched_ids.add(best_id)
            elif conf >= self.min_new_conf:
                event_id = db.insert_event(
                    category=self.category,
                    title=self.label,
                    description=f"{self.label} detected (confidence {conf:.2f})",
                    snapshot_available=1 if frame is not None else 0,
                )
                if frame is not None:
                    _save_snapshot(frame, event_id, (cx, cy, bw, bh), conf)
                self.tracked[event_id] = {"center": (cx, cy), "last_seen": now}
                matched_ids.add(event_id)
                print(f"[new event] #{event_id} at ({cx:.2f}, {cy:.2f}) conf={conf:.2f}")
            # else: below min_new_conf and doesn't match anything tracked --
            # too weak/borderline to start a new event, silently dropped.

        for event_id in list(self.tracked):
            if event_id in matched_ids:
                continue
            if now - self.tracked[event_id]["last_seen"] >= MISS_GRACE_SECONDS:
                db.resolve_event(event_id)
                print(f"[resolved] #{event_id}")
                del self.tracked[event_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="Path to trained .pt weights")
    parser.add_argument("--source", required=True, help="RTSP URL or video file path")
    parser.add_argument("--conf", type=float, default=0.3, help="Threshold to keep tracking an already-open item")
    parser.add_argument("--min-new-conf", type=float, default=0.5, help="Higher threshold required to open a NEW event")
    parser.add_argument("--iou", type=float, default=0.5)
    args = parser.parse_args()

    db.init_db()

    model = YOLO(args.model)
    tracker = TrashTracker(category="trash", label=db.CATEGORY_LABELS["trash"], min_new_conf=args.min_new_conf)

    print(f"Watching {args.source} -- writing events into admin-ui's database. Ctrl+C to stop.")
    try:
        stream = model.predict(source=args.source, conf=args.conf, iou=args.iou, stream=True, verbose=False, save=False)
        for result in stream:
            detections = []
            for box in result.boxes:
                if result.names[int(box.cls[0])] != "trash":
                    continue
                cx, cy, bw, bh = box.xywhn[0].tolist()
                detections.append((cx, cy, bw, bh, float(box.conf[0])))
            tracker.update(detections, frame=result.orig_img)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
