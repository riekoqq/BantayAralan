"""Real-time monitor: runs ONE trained detector against a live camera (or
video file) and writes real `trash` and `standing` events into admin-ui's
database.

    python detection/monitor.py \
        --model detection/runs/train4/weights/best.pt \
        --source "rtsp://user:pass@192.168.100.126:554/stream1"

Add `--show` to open a live window with detections drawn (trash in red,
standing in green), each with its confidence -- same as live_view.py,
this needs a real display attached and won't work over a headless/remote
shell. Detection and event-writing behave identically with or without
`--show`; it's purely a visual layer on top. Stop with Ctrl+C.

**Both classes come from the same model file as of round 4 (2026-09-30)**
-- see detection/dataset/README.md's round 4 entry. This replaces two
earlier, separate approaches that both lived in this file at different
points in its history (see git log if you need either):

1. Originally trash-only (one model, one class).
2. Briefly combined trash (trained detector) + standing (a *second*,
   pretrained pose model + head-height heuristic, no training data of its
   own) -- removed 2026-09-30 after being found structurally broken (a
   seated person on a raised surface could read as "more standing" than
   someone actually standing at floor level elsewhere in the room; see
   git history for the full calibration writeup).

Round 4's dataset labels `standing` as a directly-boxed class in the same
Roboflow project as `trash`, trained the same way -- so a single
`model.predict()` call now returns both classes, split by name below into
two independent CategoryTracker instances. No second model load, no pose
estimation. **Caveat, not yet resolved**: round 4's `standing` numbers
(mAP50 0.995) come from a 2-image, 6-instance validation split -- strong
on paper, unconfirmed live. The pose heuristic it replaces also looked
fine on paper before live testing found its structural flaw; give this
the same live-camera scrutiny before trusting it, per detection/dataset/
README.md's round 4 "next round should" note.

Dedup/resolve/snapshot/toggle behavior mirrors monitor_trash.py exactly --
see that file's docstring for the full reasoning (position-based matching,
wall-clock miss-grace, two confidence thresholds, admin-ui Detection
toggle respected, known limitation about restart losing tracked state).
Not repeated here to avoid the two docstrings drifting out of sync in
different words -- if you change this behavior, check monitor_trash.py's
docstring still describes its own copy accurately.
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

MATCH_DISTANCE = 0.05
MISS_GRACE_SECONDS = 5.0

# BGR draw colors per category, used only when --show is passed.
DRAW_COLORS = {"trash": (0, 0, 255), "standing": (0, 255, 0)}


def _center_distance(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def _save_snapshot(frame, event_id, box_norm, label_text, color):
    """Draw the triggering box on a copy of `frame` and save it as this
    event's snapshot. Best-effort -- see monitor_trash.py's identical
    helper for why failures here don't crash the monitor."""
    try:
        SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        h, w = frame.shape[:2]
        cx, cy, bw, bh = box_norm
        x1, y1 = int((cx - bw / 2) * w), int((cy - bh / 2) * h)
        x2, y2 = int((cx + bw / 2) * w), int((cy + bh / 2) * h)
        annotated = frame.copy()
        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
        cv2.putText(annotated, label_text, (x1, max(0, y1 - 8)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv2.imwrite(str(SNAPSHOTS_DIR / f"{event_id}.jpg"), annotated)
    except Exception as exc:
        print(f"[warn] could not save snapshot for #{event_id}: {exc}")


class CategoryTracker:
    """Position-based dedup/resolve tracker, generalized from
    monitor_trash.py's TrashTracker so `trash` and `standing` share the
    same logic instead of two copies drifting apart. See
    monitor_trash.py's docstring for the full reasoning behind this
    design (position matching instead of ByteTrack, two thresholds, wall-
    clock miss-grace).

    Matching (continuing an already-open event) only checks position,
    never `conf`. Only *creating a new* event checks
    `conf >= min_new_conf`."""

    def __init__(self, category: str, label: str, min_new_conf: float, match_distance: float = MATCH_DISTANCE):
        self.category = category
        self.label = label
        self.min_new_conf = min_new_conf
        self.match_distance = match_distance
        self.tracked = {}  # event_id -> {"center": (x, y), "last_seen": float}

    def update(self, detections, frame=None):
        """detections: list of (cx, cy, bw, bh, conf) normalized boxes,
        already filtered to this category's class name by the caller."""
        now = time.time()
        matched_ids = set()
        for cx, cy, bw, bh, conf in detections:
            best_id, best_dist = None, None
            for event_id, state in self.tracked.items():
                if event_id in matched_ids:
                    continue
                dist = _center_distance((cx, cy), state["center"])
                if dist <= self.match_distance and (best_dist is None or dist < best_dist):
                    best_id, best_dist = event_id, dist

            if best_id is not None:
                self.tracked[best_id]["center"] = (cx, cy)
                self.tracked[best_id]["last_seen"] = now
                matched_ids.add(best_id)
            elif conf >= self.min_new_conf:
                if not db.is_category_detection_enabled(self.category):
                    continue
                event_id = db.insert_event(
                    category=self.category,
                    title=self.label,
                    description=f"{self.label} detected (confidence {conf:.2f})",
                    snapshot_available=1 if frame is not None else 0,
                )
                if frame is not None:
                    _save_snapshot(frame, event_id, (cx, cy, bw, bh), f"{self.category} {conf:.2f}",
                                    DRAW_COLORS.get(self.category, (0, 0, 255)))
                self.tracked[event_id] = {"center": (cx, cy), "last_seen": now}
                matched_ids.add(event_id)
                print(f"[new {self.category}] #{event_id} at ({cx:.2f}, {cy:.2f}) conf={conf:.2f}")

        for event_id in list(self.tracked):
            if event_id in matched_ids:
                continue
            if now - self.tracked[event_id]["last_seen"] >= MISS_GRACE_SECONDS:
                db.resolve_event(event_id)
                print(f"[resolved {self.category}] #{event_id}")
                del self.tracked[event_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="Path to trained .pt weights (must have both 'trash' and 'standing' classes -- see detection/dataset/README.md round 4)")
    parser.add_argument("--source", required=True, help="RTSP URL or video file path")
    parser.add_argument("--conf", type=float, default=0.3, help="Threshold to keep tracking an already-open item")
    parser.add_argument("--min-new-conf", type=float, default=0.5, help="Higher threshold to open a NEW trash event")
    parser.add_argument("--standing-min-new-conf", type=float, default=0.5, help="Higher threshold to open a NEW standing event")
    parser.add_argument("--standing-match-distance", type=float, default=0.1,
                         help="Looser than trash's default (0.05) -- a standing person moves around more than a static object")
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--show", action="store_true",
                         help="Open a live window showing detections (needs a real display -- see live_view.py's notes on headless/remote shells)")
    parser.add_argument("--display-width", type=int, default=1024,
                         help="Window width in pixels when --show is used; detection still runs at full resolution")
    args = parser.parse_args()

    db.init_db()

    model = YOLO(args.model)
    trash_tracker = CategoryTracker(category="trash", label=db.CATEGORY_LABELS["trash"], min_new_conf=args.min_new_conf)
    standing_tracker = CategoryTracker(category="standing", label=db.CATEGORY_LABELS["standing"],
                                        min_new_conf=args.standing_min_new_conf, match_distance=args.standing_match_distance)
    trackers = {"trash": trash_tracker, "standing": standing_tracker}

    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"Could not open {args.source}")
        return

    print(f"Watching {args.source} -- trash + standing, writing into admin-ui's database. Ctrl+C to stop.")
    consecutive_failures = 0
    # Roughly 60s of continuous failure at ~0.5s between retries before
    # giving up -- a single dropped/corrupted h264 frame (confirmed to
    # happen in practice with this camera) shouldn't kill the whole
    # monitor, but a truly dead connection shouldn't spin forever either.
    max_consecutive_failures = 120
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                consecutive_failures += 1
                print(f"[warn] dropped/failed frame read ({consecutive_failures}/{max_consecutive_failures}) -- retrying")
                if consecutive_failures >= max_consecutive_failures:
                    print("Stream unrecoverable after repeated failures; stopping.")
                    break
                time.sleep(0.5)
                continue
            consecutive_failures = 0

            display_frame = frame.copy() if args.show else None
            h, w = frame.shape[:2]

            result = model.predict(source=frame, conf=args.conf, iou=args.iou, verbose=False)[0]
            detections_by_class = {"trash": [], "standing": []}
            for box in result.boxes:
                cls_name = result.names[int(box.cls[0])]
                if cls_name not in trackers:
                    continue
                cx, cy, bw, bh = box.xywhn[0].tolist()
                conf = float(box.conf[0])
                detections_by_class[cls_name].append((cx, cy, bw, bh, conf))
                if display_frame is not None:
                    color = DRAW_COLORS.get(cls_name, (0, 0, 255))
                    x1, y1 = int((cx - bw / 2) * w), int((cy - bh / 2) * h)
                    x2, y2 = int((cx + bw / 2) * w), int((cy + bh / 2) * h)
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(display_frame, f"{cls_name} {conf:.2f}", (x1, max(0, y1 - 8)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            for cls_name, tracker in trackers.items():
                tracker.update(detections_by_class[cls_name], frame=frame)

            if display_frame is not None:
                if w > args.display_width:
                    scale = args.display_width / w
                    display_frame = cv2.resize(display_frame, (args.display_width, int(h * scale)))
                cv2.imshow("BantayAralan -- trash + standing (press q to quit)", display_frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        cap.release()
        if args.show:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
