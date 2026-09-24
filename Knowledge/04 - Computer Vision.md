---
tags: [computer-vision]
status: Not Yet Implemented
---

# Computer Vision

Everything below is the proposal's working-draft description of the intended CV pipeline. **None of it has source code in this repository.** No camera integration, no model files, no inference code, no tracking code exist anywhere in the repo.

## Model version — Changed from proposal (2026-09-24)
The original proposal PDF and this vault previously named **YOLO11m** as the detection model. The project team has since confirmed **YOLOv8** as the current choice (communicated directly, 2026-09-24) — not yet written into the proposal or prototype paper documents. Treat **YOLOv8** as current; **YOLO11m** as superseded proposal text until the source documents are updated to match.

## Intended components (Proposal Requirement)
- **Object/pose detection**: YOLO-based model — **YOLOv8** per the team's current direction (supersedes the proposal PDF's YOLO11m, see above) — detects objects and estimates pose (used to infer behaviors like standing).
- **Tracking**: ByteTrack — tracks detected objects/persons across frames.
- **Behavior logic**: rule-based decisions over tracked poses/objects — standing behavior, trash/clutter presence, seat/table alignment vs. defined reference positions and thresholds.
- **Two camera perspectives**: a ceiling-mounted camera for behavior detection, a top-down camera for clutter and desk/seat alignment, processed as two largely independent pipelines that converge at event logging — see [[System Architecture]].
- **Frame processing loop**: capture → detect → track → decide → log/snapshot → display, repeating continuously (System Flowchart, Figure 3 of the proposal).

## Planned evaluation metrics (Proposal Requirement, not measured)
Accuracy, precision, recall, FPS, latency — see [[Evaluation Standards]] and [[09 - Testing & Evaluation]]. The proposal cites related work achieving up to ~95–97% accuracy and ~39 FPS real-time object detection, but states no target numbers of its own yet.

## Dataset / training data
Not specified in the proposal beyond citing general classroom-behavior-detection literature and a cluttered-object dataset limitation (ZeroWaste dataset, Bashkirova et al. 2021, cited as an example of the clutter-detection challenge, not as a dataset BantayAralan will use). No dataset has been selected or collected for this project as far as this repository shows.

## Detection thresholds
The proposal mentions seat/table alignment is evaluated "against defined thresholds" without specifying values — an open implementation detail.

## Status
**Not Yet Implemented / Proposal Requirement** throughout this note.

## Related
- [[Research Proposal]]
- [[System Architecture]]
- [[08 - Hardware]]
- [[Event Model]]
- [[09 - Testing & Evaluation]]
