---
tags: [computer-vision]
status: Partially Implemented
---

# Computer Vision

Most of what's below is still the proposal's working-draft description of
the *intended* pipeline, without source code. **Real exceptions exist**:
as of 2026-09-26, [`detection/monitor_trash.py`](../detection/monitor_trash.py)
ran a trained model against a live camera and wrote real `trash` events
into `admin-ui`'s database; as of 2026-09-30,
[`detection/monitor.py`](../detection/monitor.py) supersedes it as **the
script to run going forward** (`monitor_trash.py` stays only for
reference/history) and covers both `trash` and `standing` — see "Real
implementation" below and [[Trash Monitoring Integration]]. Both are
manually-run scripts rather than a continuous pipeline, and use a much
simpler in-memory position-matching approach than ByteTrack. Behavior
detection beyond `standing`, `misaligned` detection, and continuous/
automatic operation remain unimplemented.

## Model version — Changed from proposal (2026-09-24)
The original proposal PDF and this vault previously named **YOLO11m** as the detection model. The project team has since confirmed **YOLOv8** as the current choice (communicated directly, 2026-09-24) — not yet written into the proposal or prototype paper documents. Treat **YOLOv8** as current; **YOLO11m** as superseded proposal text until the source documents are updated to match.

## Intended components (Proposal Requirement)
- **Object/pose detection**: YOLO-based model — **YOLOv8** per the team's current direction (supersedes the proposal PDF's YOLO11m, see above) — detects objects and estimates pose (used to infer behaviors like standing).
- **Tracking**: ByteTrack — tracks detected objects/persons across frames. **Not implemented** — `monitor_trash.py`'s position-matching (below) is a much simpler stand-in, not ByteTrack, and doesn't do continuous frame-to-frame tracking, only proximity-based dedup.
- **Behavior logic**: rule-based decisions over tracked poses/objects — standing behavior, trash/clutter presence, seat/table alignment vs. defined reference positions and thresholds. The "reference positions and thresholds" approach for seat/table alignment specifically is discussed as the likely right architecture for `misaligned` in `detection/dataset/README.md`'s round log, but not yet built.
- **Two camera perspectives**: a ceiling-mounted camera for behavior detection, a top-down camera for clutter and desk/seat alignment, processed as two largely independent pipelines that converge at event logging — see [[System Architecture]].
- **Frame processing loop**: capture → detect → track → decide → log/snapshot → display, repeating continuously (System Flowchart, Figure 3 of the proposal). `monitor_trash.py` implements a version of this loop for `trash` only, but as a manually-started/stopped script, not a continuously-running service.

## Real implementation — `detection/monitor.py` (2026-09-26, updated 2026-09-30)

The first pieces of this pipeline with actual running code. Summary —
full detail in [`detection/CLAUDE.md`](../detection/CLAUDE.md) and the
scripts' own docstrings:

- Loads a locally-trained YOLOv8 `.pt` model and runs it against an RTSP
  camera stream or video file.
- **As of round 4 (2026-09-30)**: `monitor.py` handles both `trash` and
  `standing` from a **single trained model** — `standing` moved from a
  pretrained-pose-model + head-height heuristic (tried 2026-09-29, found
  structurally broken by live testing the same day, removed) to a
  directly-labeled box class trained the same way `trash` is. See
  "Prototype scope decision" below and
  `detection/dataset/README.md`'s round 4 entry for the training numbers
  and a first live-camera test's findings (real gaps found — not yet
  trustworthy, see below). `misaligned` still isn't wired up (deprioritized,
  see below).
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
- Run manually (`python detection/monitor.py ...`), not started
  automatically with the app — a deliberate scope choice, not a limitation
  to fix immediately; see [[Trash Monitoring Integration]]'s "Alternatives
  considered (integration scope)". `detection/monitor_trash.py` is the
  original `trash`-only version, kept for reference/history only.

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

## Prototype scope decision (2026-09-29, updated 2026-09-30)
Active near-term work is **`trash`** (continuing) and **`standing`** (new —
see [Knowledge/11 - Decisions/Prototype Scope — Trash and Standing, Misaligned Deprioritized.md](<11%20-%20Decisions/Prototype%20Scope%20—%20Trash%20and%20Standing%2C%20Misaligned%20Deprioritized.md>)).
**`misaligned` is deprioritized, not abandoned** — no further labeling
effort for now. `standing`'s approach changed mid-flight: first tried as
pose-estimation (pretrained `yolov8n-pose.pt` + a hand-built head-height
heuristic), found structurally broken by live testing 2026-09-29 and
removed; **revised to a directly-labeled box class**, trained the same
way `trash` is, as of round 4 (2026-09-30) — see
`detection/dataset/README.md`. Strong validation numbers (mAP50 0.995),
but a first live-camera test the same day found real gaps — most
seriously, other people besides the one in the training photos aren't
detected as `standing` at all, a possible sign of overfitting to one
person's proportions rather than a general posture. **Not yet a settled,
trustworthy approach** — see the decision doc's 2026-09-30 update and the
round 4 live-camera-test entry for full detail.

## Status
**Partially Implemented**: `trash` detection + a simple position-based
dedup/resolve loop, run manually via `detection/monitor.py`, writing real
events into `admin-ui`. `standing` is also **Partially Implemented** as of
round 4 (trained, wired into `monitor.py`, writing real events) but
**round 4 live-testing found it unreliable for anyone but the one
person it had been tested on**. Round 5 (2026-10-03, 145 images, more
people added, `yolov8n`) improved this in live use — a person not in the
training data was detected — but the user's own assessment is the dataset
still lacks diversity, and other body compositions, side views, and low
light haven't been tested. Treat as a working pipeline with an improving,
not yet validated, detector. `trash` has its own open reliability gap too: a 2026-10-01
live test (via `monitor.py --show`, writing real events end-to-end) found
a cast shadow misread as `trash`, a different false-positive mode than
the person's-clothing confusion logged in every earlier round — see
`detection/dataset/README.md`'s 2026-10-01 entry. Everything else in this
note — ByteTrack, `misaligned` detection (paused, see above), the
two-camera setup, continuous/automatic operation — remains **Not Yet
Implemented / Proposal Requirement**.

## Related
- [[Research Proposal]]
- [[System Architecture]]
- [[08 - Hardware]]
- [[Event Model]]
- [[09 - Testing & Evaluation]]
- [[No-Code Tool for Initial CV Proof-of-Concept]]
- [[Trash Monitoring Integration]]
- [[Prototype Scope — Trash and Standing, Misaligned Deprioritized]]
