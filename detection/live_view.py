"""Standalone real-time viewer: runs a trained model against a live camera
(or video file) and shows annotated detections in a window as they happen.

Independent of admin-ui -- no database writes, no event logging, no
dedup/resolve lifecycle. For that, see monitor_trash.py. This script is
just a live visual check: "what is the model seeing right now."

Deliberately not a GUI application (no Tkinter/PyQt/buttons/menus) -- the
proposal explicitly leaves "which GUI framework for the integrated CV + GUI
system" as an open question (Knowledge/12 - Open Questions.md). Building a
real GUI here would silently answer that question; a plain OpenCV window
sidesteps it instead. This is a lightweight viewer/demo tool, not the
proposal's full integrated system.

Must be run locally, in a terminal with a real display attached --
cv2.imshow opens a native window, which will not work over a headless or
remote shell:

    python detection/live_view.py \
        --model detection/runs/train2/weights/best.pt \
        --source "rtsp://user:pass@<camera-ip>:554/stream1"

Shows every class the model detects (including misaligned, low-confidence
as it currently is) -- unlike monitor_trash.py, nothing here gets written
down, so there's no cost to seeing an untrustworthy detection on screen.
Press 'q' in the window to quit.
"""
import argparse
import time

import cv2
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--model", required=True, help="Path to trained .pt weights")
    parser.add_argument("--source", required=True, help="RTSP URL or video file path")
    parser.add_argument("--conf", type=float, default=0.3)
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--display-width", type=int, default=1024,
                         help="Window width in pixels -- the camera's native resolution (e.g. 2304x1296) is too large for most screens, so the displayed frame is downscaled to this width (aspect ratio kept). Does not affect detection, which still runs on the full-resolution frame.")
    args = parser.parse_args()

    model = YOLO(args.model)
    window_name = "BantayAralan -- Live Detection (press q to quit)"

    prev_time = time.time()
    print(f"Opening {args.source} -- press 'q' in the window to quit.")
    stream = model.predict(source=args.source, conf=args.conf, iou=args.iou, stream=True, verbose=False, save=False)
    try:
        for result in stream:
            frame = result.plot()  # full-resolution frame with boxes/labels/confidences drawn

            h, w = frame.shape[:2]
            if w > args.display_width:
                scale = args.display_width / w
                frame = cv2.resize(frame, (args.display_width, int(h * scale)))

            now = time.time()
            fps = 1.0 / max(now - prev_time, 1e-6)
            prev_time = now
            cv2.putText(frame, f"{fps:.1f} FPS", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

            cv2.imshow(window_name, frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
