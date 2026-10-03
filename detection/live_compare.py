"""Side-by-side live comparison of two trained models on the SAME camera
frames: one RTSP connection (this camera has a low concurrent-connection
limit), both models run on each frame, each shown in its own window. Visual
only -- no database writes, same spirit as live_view.py.

    python detection/live_compare.py \
        --model-a detection/runs/train5/weights/best.pt --label-a yolov8n \
        --model-b detection/runs/train5_s/weights/best.pt --label-b yolov8s \
        --source "rtsp://user:pass@<camera-ip>:554/stream1"

Press 'q' in either window to quit.
"""
import argparse
import threading
import time

import cv2
from ultralytics import YOLO


class LatestFrame:
    """Reads the stream on its own thread and keeps only the newest frame.
    Without this, running two models per frame is slower than the camera's
    frame rate, the capture buffer backs up, and the view lags further
    behind real time the longer it runs."""

    def __init__(self, cap):
        self.cap = cap
        self.frame = None
        self.seq = 0
        self.lock = threading.Lock()
        self.stopped = False
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            with self.lock:
                self.frame = frame
                self.seq += 1

    def get(self, last_seq):
        with self.lock:
            if self.seq == last_seq:
                return None, last_seq
            return self.frame, self.seq


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model-a", required=True)
    p.add_argument("--model-b", required=True)
    p.add_argument("--label-a", default="A")
    p.add_argument("--label-b", default="B")
    p.add_argument("--source", required=True)
    p.add_argument("--conf", type=float, default=0.3)
    p.add_argument("--iou", type=float, default=0.5)
    p.add_argument("--width", type=int, default=800, help="Display width per window")
    p.add_argument("--height", type=int, default=450, help="Display height per window")
    args = p.parse_args()

    models = [(args.label_a, YOLO(args.model_a)), (args.label_b, YOLO(args.model_b))]

    cap = cv2.VideoCapture(args.source)
    if not cap.isOpened():
        print(f"Could not open {args.source}")
        return

    for i, (label, _) in enumerate(models):
        cv2.namedWindow(label, cv2.WINDOW_AUTOSIZE)
        cv2.moveWindow(label, i * (args.width + 10), 40)

    reader = LatestFrame(cap)
    last_seq = 0

    print("Comparing live -- press 'q' in a window to quit.")
    try:
        while True:
            frame, last_seq = reader.get(last_seq)
            if frame is None:
                if cv2.waitKey(5) & 0xFF == ord("q"):
                    break
                continue
            for label, model in models:
                t0 = time.time()
                result = model.predict(source=frame, conf=args.conf, iou=args.iou, verbose=False)[0]
                ms = (time.time() - t0) * 1000
                img = cv2.resize(result.plot(), (args.width, args.height))
                cv2.putText(img, f"{label}  {ms:.0f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                cv2.imshow(label, img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        reader.stopped = True
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
