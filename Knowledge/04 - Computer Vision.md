---
tags: [computer-vision]
status: Partially Implemented
---

# Computer Vision

Most of what's below is still the proposal's working-draft description of
the *intended* pipeline, without source code. **One real exception exists**
as of 2026-09-26: [`detection/monitor_trash.py`](../detection/monitor_trash.py)
runs a trained model against a live camera and writes real events into
`admin-ui`'s database — see "Real implementation" below and
[[Trash Monitoring Integration]]. It covers `trash` only, is a manually-run
script rather than a continuous pipeline, and uses a much simpler
in-memory position-matching approach than ByteTrack. Behavior detection,
`misaligned` detection, and continuous/automatic operation remain
unimplemented.

## Model version — Changed from proposal (2026-09-24)
The original proposal PDF and this vault previously named **YOLO11m** as the detection model. The project team has since confirmed **YOLOv8** as the current choice (communicated directly, 2026-09-24) — not yet written into the proposal or prototype paper documents. Treat **YOLOv8** as current; **YOLO11m** as superseded proposal text until the source documents are updated to match.

## Intended components (Proposal Requirement)
- **Object/pose detection**: YOLO-based model — **YOLOv8** per the team's current direction (supersedes the proposal PDF's YOLO11m, see above) — detects objects and estimates pose (used to infer behaviors like standing).
- **Tracking**: ByteTrack — tracks detected objects/persons across frames. **Not implemented** — `monitor_trash.py`'s position-matching (below) is a much simpler stand-in, not ByteTrack, and doesn't do continuous frame-to-frame tracking, only proximity-based dedup.
- **Behavior logic**: rule-based decisions over tracked poses/objects — standing behavior, trash/clutter presence, seat/table alignment vs. defined reference positions and thresholds. The "reference positions and thresholds" approach for seat/table alignment specifically is discussed as the likely right architecture for `misaligned` in `detection/dataset/README.md`'s round log, but not yet built.
- **Two camera perspectives**: a ceiling-mounted camera for behavior detection, a top-down camera for clutter and desk/seat alignment, processed as two largely independent pipelines that converge at event logging — see [[System Architecture]].
- **Frame processing loop**: capture → detect → track → decide → log/snapshot → display, repeating continuously (System Flowchart, Figure 3 of the proposal). `monitor_trash.py` implements a version of this loop for `trash` only, but as a manually-started/stopped script, not a continuously-running service.

## Real implementation — `detection/monitor_trash.py` (2026-09-26)

The first (and so far only) piece of this pipeline with actual running
code. Summary — full detail in [`detection/CLAUDE.md`](../detection/CLAUDE.md)
and the script's own docstring:

- Loads a locally-trained YOLOv8 `.pt` model and runs it against an RTSP
  camera stream or video file.
- **`trash` only** — `misaligned` isn't wired up (still too little training
  data to trust, see the round log).
- Dedup/lifecycle: matches detections to already-open events by position
  in memory (not ByteTrack), opens a new event for a genuinely new
  position, resolves an event once its item goes unseen for a wall-clock
  grace period. Two confidence thresholds (one to keep tracking, a higher
  one to open a new event) were added after live testing showed a single
  threshold produced a flicker-driven create/resolve loop on a borderline
  detection.
- Writes into `admin-ui`'s real database via `admin-ui/backend/db.py`
  (`insert_event`/`resolve_event`), gated by the new `events.status`
  field — see [[Trash Monitoring Integration]].
- Run manually (`python detection/monitor_trash.py ...`), not started
  automatically with the app — a deliberate scope choice, not a limitation
  to fix immediately; see [[Trash Monitoring Integration]]'s "Alternatives
  considered (integration scope)".

## Planned evaluation metrics (Proposal Requirement, not measured)
Accuracy, precision, recall, FPS, latency — see [[Evaluation Standards]] and [[09 - Testing & Evaluation]]. The proposal cites related work achieving up to ~95–97% accuracy and ~39 FPS real-time object detection, but states no target numbers of its own yet.

## Dataset / training data
Not specified in the proposal beyond citing general classroom-behavior-detection literature and a cluttered-object dataset limitation (ZeroWaste dataset, Bashkirova et al. 2021, cited as an example of the clutter-detection challenge, not as a dataset BantayAralan will use).

**Dataset collection started 2026-09-25** (Planned / in progress, not
Implemented): a first labeling/training round using 7 clutter/misaligned-seat
photos in a no-code tool (Roboflow) — see
[[No-Code Tool for Initial CV Proof-of-Concept]] and
[`detection/dataset/README.md`](../detection/dataset/README.md) for the
round log. This is a pipeline proof-of-concept at single-digit-to-low-tens
image scale, not a trained/validated detector — no accuracy numbers worth
citing exist yet, even though the resulting weights are now genuinely
running in `monitor_trash.py` (above) against a live camera.

## Detection thresholds
The proposal mentions seat/table alignment is evaluated "against defined thresholds" without specifying values — an open implementation detail.

## Status
**Partially Implemented**: `trash` detection + a simple position-based
dedup/resolve loop, run manually via `detection/monitor_trash.py`, writing
real events into `admin-ui`. Everything else in this note — behavior
detection, pose estimation, ByteTrack, `misaligned` detection, the two-camera
setup, continuous/automatic operation — remains **Not Yet Implemented /
Proposal Requirement**.

## Related
- [[Research Proposal]]
- [[System Architecture]]
- [[08 - Hardware]]
- [[Event Model]]
- [[09 - Testing & Evaluation]]
- [[No-Code Tool for Initial CV Proof-of-Concept]]
- [[Trash Monitoring Integration]]
