# CV Dataset Tracking

Tracks labeling/training rounds done in an external no-code tool (Roboflow
or similar). See [`../CLAUDE.md`](../CLAUDE.md) for what does and doesn't
belong in this folder — no raw images, exports, or weights get committed.

## Classes

| Class        | Meaning                          | Matches `events.category` |
|--------------|-----------------------------------|----------------------------|
| `trash`      | Trash / scattered objects (clutter) | `trash` |
| `misaligned` | Misaligned seat/table              | `misaligned` |

**`trash` is floor-only, by working decision (2026-09-26)**: an item is
only labeled `trash` if it's on the floor. Clutter sitting on a desk/bed/
chair should be left **unlabeled** (not boxed) rather than counted as
`trash` — that's what teaches the model "floor" specifically rather than
"clutter anywhere," and doubles as a useful negative example (visually
messy-looking, correctly zero boxes). Round 2 is `trash`-only —
`misaligned` labeling is deliberately deferred, not abandoned.

**No "not trash" / "not misaligned" tag** — detection labeling only marks
the positive things you want found; unlabeled regions/images are implicitly
background. To teach the model what a normal scene looks like (so it
doesn't false-positive on things like desk glare/reflections), include a
few **negative examples**: photos with zero boxes drawn — a clean desk/floor,
neatly aligned seats. With a dataset this small, don't spend every image on
positive boxes; a rough 4–5 positive / 2–3 negative split teaches contrast
better than all-positive.

## Round log

Fill in one entry per labeling/training round — this is what makes "how
much data was this actually trained on" checkable later instead of a claim
in the paper nobody can verify.

### Round 1 — 2026-09-25/26

- **Source images**: 7 (not committed — see `.gitignore`)
- **Class split**: **`trash` only** — the exported dataset version's
  `data.yaml` has `nc: 1, names: ['trash']`. `misaligned` was not present in
  this export (either not labeled, or not included when the version was
  generated) — flagging this as a gap, not a decision to drop the class.
- **Negative/background examples**: **none** — all 7 images have at least
  2 labeled boxes (train: 2/4/4 boxes across 3 images; valid: 3/3 boxes
  across 2 images; test: 3/3 boxes across 2 images). No clean/background
  image was included despite the labeling guidance above — worth adding in
  the next round.
- **Tool**: Roboflow (free tier) for labeling/dataset export.
  Weights-export for a Roboflow-*trained* model is paywalled on the free
  plan ("Your current plan does not have weights export included") — worked
  around by exporting the **dataset** (not the trained model) and training
  locally instead. See
  [Knowledge/11 - Decisions/No-Code Tool for Initial CV Proof-of-Concept.md](<../../Knowledge/11%20-%20Decisions/No-Code%20Tool%20for%20Initial%20CV%20Proof-of-Concept.md>).
- **Augmentation applied**: none (per Roboflow's `README.roboflow.txt` —
  only auto-orientation + resize to 640×640 stretch as preprocessing).
- **Train/valid/test split**: 3 / 2 / 2 images.
- **Model**: trained **locally** (RTX 2060, 6GB) via
  `ultralytics` CLI, base checkpoint `yolov8n.pt` (transfer learning, not
  from scratch). Command:
  `yolo detect train data=detection/dataset/data.yaml model=yolov8n.pt epochs=150 patience=30 imgsz=640 batch=4 device=0 cache=True`
- **Result**: early-stopped at epoch 97 (best weights from epoch 67,
  `patience=30`). Validated against the `valid` split (2 images, 8
  instances): **precision 0.0062, recall 0.25, mAP50 0.162, mAP50-95
  0.0863**. These are poor numbers — expected,
  not a claim of a working detector. Directly explained by the dataset gaps
  above (single digit images, one class, zero negative examples, no
  augmentation). **Do not cite this as validated detection accuracy** in
  the paper (see
  [Knowledge/09 - Testing & Evaluation.md](<../../Knowledge/09%20-%20Testing%20&%20Evaluation.md>)) —
  it's a pipeline proof-of-concept only: labeling → local training →
  weights export works end-to-end.
- **Weights**: `detection/runs/train1/weights/best.pt` (local only, not
  committed — see `.gitignore`).
- **Roboflow project link**: `justins-workspace-banrr/bantayaralan`
  (dataset version 1, generated 2026-09-25 1:54am).

### Round 2 — 2026-09-26

- **Source images**: 23 total (19 train / 2 valid / 2 test) — up from 7,
  still short of the 50+ target discussed, but includes both classes and
  real negatives this time. Mix of the fixed IP camera (multiple rooms,
  not just the original bedroom spot) plus some phone photos.
- **Class split**: both classes present in every split this time —
  `misaligned`: 3 train / 2 valid / 2 test (7 boxes total — thin).
  `trash`: 39 train / 7 valid / 7 test (51 boxes total).
  `trash` labeling restricted to floor-only items per the working decision
  above; non-floor clutter left unlabeled on purpose.
- **Negative/background examples**: 5 empty-label images, **all in the
  train split only** — valid and test have zero negatives. This means the
  validation metrics below can't tell us whether the round-1
  false-positive behavior (fixed-location "trash" on a wall outlet and on
  a person) actually improved — that has to be checked against the live
  camera separately (see below), not from these numbers.
- **Train/valid/test split**: 19 / 2 / 2 images — valid/test are still
  very small (10 total instances), so these metrics are noisy; treat as a
  directional signal, not a solid number.
- **Model**: same setup as round 1 — local RTX 2060, `yolov8n.pt`
  transfer learning, `epochs=150 patience=30 imgsz=640 batch=8 device=0
  cache=True`. Early-stopped at epoch 99 (best from epoch 69).
- **Result** (validated on the 2-image valid split, 10 instances):
  overall precision 0.672, recall 0.458, mAP50 0.568, mAP50-95 0.376.
  Per class: `misaligned` P 0.722 / R 0.5 / mAP50 0.662 / mAP50-95 0.529;
  `trash` P 0.622 / R 0.415 / mAP50 0.474 / mAP50-95 0.222. A large jump
  over round 1 (P 0.006, mAP50 0.16) — but from a 2-image validation set,
  so **don't cite this as a reliable accuracy number** in the paper; it's
  a directional improvement, confirmed separately against the live camera
  below, not a statistically meaningful metric on its own.
- **Weights**: `detection/runs/train2/weights/best.pt` (local only, not
  committed).
- **Roboflow project link**: `justins-workspace-banrr/bantayaralan`
  (dataset version 2).

**Next round should**: still grow past 23 (target 50+ remains), add
negative examples to valid/test specifically (not just train), and grow
`misaligned`'s 7 boxes — it's the thinner of the two classes by a wide
margin.

### Live camera test — 2026-09-26 (round 2 model)

Ran `train2/weights/best.pt` against the same live RTSP feed as round 1's
test. Recorded ~1,485 frames, re-analyzed offline at `conf=0.1`.

**Substantial improvement over round 1**: only 36/1,485 frames (~2.4%)
fired any detection at all (vs. 1,119/1,813, ~62%, in round 1), and
confidence reached up to **1.00** (vs. a 0.26 ceiling before). Critically,
the high-confidence detections (`trash 1.00`, `trash 0.87`) landed on
**real floor objects** (a bag/clothing item near the door, a dark object
near the bed) — not the wall outlet or the person, which is what round 1
fixated on. This is genuine signal, not just a confidence-number
improvement.

Still present: a low-confidence (~0.1–0.35) spurious detection clustered
near the bottom edge of frame (`~x0.65, y0.98`, near where a person tends
to sit) — minor next to round 1's near-total false-positive rate, but
worth watching in round 3. `misaligned` wasn't exercised in this clip (no
seats in view).

**Still not citable as validated accuracy** (see round 2's numbers above —
2-image validation set) — but this is the first round where the live
camera test shows the model responding to actual scene content instead of
a memorized fixed location.

### Live camera test 2 — 2026-09-26 (round 2 model, rearranged/novel items)

Re-tested `train2/weights/best.pt` after physically rearranging items in
the room, including some never used in training — a real generalization
check, not just a repeat of the same scene.

**Methodology note/correction**: the first attempt at this re-test
re-analyzed the already-annotated output video from a `save=True` run
(boxes/labels burned into the pixels), which contaminates a second pass —
it found almost nothing, contradicting what was visibly detected live.
Fixed by running `save=True save_txt=True save_conf=True` together in one
clean pass instead of two. Do this in one pass going forward, not
record-then-reanalyze.

**Result**: strong generalization. Across 1,299 frames, 7,484 detections
(all `trash`, `misaligned` not exercised — no seats in view), confidence
up to 0.95, with 661 detections ≥0.9 and 2,082 more in 0.7–0.9. Visually
confirmed (see round log frame captures) these land on real floor items
clustered near the door — including items not in the training set — not
the wall outlet or the person. One negligible low-confidence (~0.11)
blip at a different location in only 10/1,299 frames — not a real
pattern. First test where the model responds to a genuinely new object
arrangement rather than a memorized position — the clearest evidence yet
that round 2's changes (more data, negatives, position variety,
floor-only labeling) are working, not just improving numbers on a tiny
validation set.

### Live camera test — 2026-09-26

Ran `train1/weights/best.pt` against the actual TP-Link VIGI camera over
RTSP (`rtsp://admin:***@192.168.100.126:554/stream1`), same physical
room/POV the 7 training screenshots came from. Confirms the pipeline itself
(RTSP → Ultralytics → output) works end-to-end — see
[`detection/CLAUDE.md`](../CLAUDE.md) for the setup once this needs to
become real inference code rather than a manual test.

Recorded ~1,813 frames and re-ran offline at `conf=0.1` for analysis
(default `conf=0.25` showed nothing on manual spot-checks). Result:
**1,119/1,813 frames (~62%) fired a `trash` prediction, but at a fixed
screen location (~x0.775, y0.329) regardless of scene content, and
confidence never exceeded 0.26.** This is overfitting, not detection — the
model memorized a spurious location from the 3 training images rather than
learning what clutter looks like, consistent with the 0.0062 precision
from validation above. **Not evidence of working detection** — same "wait
for round 2" conclusion as above, now confirmed against a live feed instead
of just held-out validation images.

### Live camera test 3 — 2026-09-26 (round 2 model, chair confusion + occlusion)

Two more findings from continued live testing of `train2/weights/best.pt`,
both worth carrying into round 3 planning:

**Furniture/clutter confusion**: with the chair sitting in the same floor
region as real `trash` items, it started getting weakly flagged as `trash`
itself (~0.31–0.39 confidence) — visible directly on the chair's frame,
not on any item near it. Root cause: there's no `seat` class yet and no
negative example of "just the chair, no clutter," so the model has no
signal that furniture in that zone isn't automatically trash. Confirms the
plan from the `misaligned`/architecture discussion above — a `seat` class
needs to exist not just for alignment-checking later, but to stop this
leakage into `trash`'s false positives now.

**Partial occlusion — mixed results**: covered parts of several placed
items with a foot. A belt that was partially cut off out of view was still
detected; a powerbank and a small box, also partially covered, were not
detected independently. Not a sign of a specific occlusion bug — with only
23 training images, whatever visual signature survives partial occlusion
is down to chance per-object, not learned robustness. If partially-hidden
items are realistic for the actual deployment scenario, round 3 should
deliberately include some partially-occluded training examples rather than
only fully-exposed items.

**Overlapping-box fix confirmed**: separately, re-running at `conf=0.3
iou=0.5` (instead of the `conf=0.1` used for earlier diagnostic passes)
eliminated the duplicate/overlapping boxes on the same object seen in
initial testing — distinct floor items now get exactly one box each. Use
`conf=0.3 iou=0.5` (not `conf=0.1`) for any future test meant to look like
realistic output rather than low-threshold diagnostic analysis.

### Live camera test 4 — 2026-09-26 (via `detection/monitor_trash.py`)

Running the round-2 model continuously through the new monitoring script
(see [Knowledge/11 - Decisions/Trash Monitoring Integration.md](<../../Knowledge/11%20-%20Decisions/Trash%20Monitoring%20Integration.md>))
surfaced a **third person-related false positive**, same category of issue
as round 1's neck/collar detection: `trash 0.56` boxed directly on the
graphic print of a worn t-shirt's chest, not any floor object. See event
#101's snapshot (`admin-ui/data/snapshots/101.jpg`).

This makes a clear pattern across every round of live testing so far:
**a person's body/clothing, when it ends up in the same vertical
frame-zone where floor clutter usually appears (crouching, bending down,
sitting on the floor), gets mistaken for trash.** Round 1 had this on a
neck/collar; now a shirt's graphic print. The dataset has never included a
deliberate negative example of "a person near/at floor level, no clutter
present" — every positive example implicitly also lacks this specific
contrast case.

**Round 3 should explicitly add**: a handful of negative examples with a
person crouching, bending, or sitting near the floor and *no* trash
present, so the model gets a direct signal that human bodies/clothing in
that zone aren't clutter — not just more generic "clean floor" negatives,
which don't cover this specific confusion.

### Model size experiment — 2026-09-26 (yolov8n vs. yolov8s, same round 2 data)

Trained `yolov8s.pt` on the identical round 2 dataset/hyperparameters as
`train2` (`yolov8n`), to test whether a bigger model helps on this data —
prompted by a question about whether more training data would slow down
live inference (it doesn't; model variant does, addressed separately) and
then whether a bigger variant would just be more accurate on the same
data (tested here rather than assumed).

**Validation numbers were mixed and not very meaningful**: `yolov8s` had
higher precision/recall and `trash` mAP50 (0.608 vs 0.474), but lower
`misaligned` mAP50 (0.495 vs 0.662) and roughly flat overall mAP50 — on a
2-image, 10-instance validation set, none of these differences are
statistically meaningful in either direction.

**Live camera testing was more informative, though confounded**: this
happened to run at night, which put the camera into IR/grayscale mode —
something **zero training images cover** (all 23 are daytime/color), so
this tests an unseen visual domain on top of everything else. Result: widespread,
low-confidence (0.11-0.27), scattered false positives across the frame
with `yolov8s` (confirmed via a saved frame — not just numbers), and the
user separately observed a new false positive during live viewing (via
`live_view.py`) that `yolov8n` had never shown: the bed's wooden legs
flagged as `trash`.

**Conclusion so far**: no evidence found that `yolov8s` earns its ~3x
parameter count on this dataset size — some evidence (the new bed-leg
false positive, the `misaligned` mAP50 drop) that it's overfitting more,
not less. **Decision deliberately deferred, not closed**: the user wants
to expand the dataset (round 3) before picking a model size, rather than
decide on today's small/confounded comparison. **Both trained weight sets
are being kept** (`detection/runs/train2/weights/` = `yolov8n`,
`detection/runs/train_s/weights/` = `yolov8s`, both gitignored/local-only)
so both can be re-compared once round 3's data exists, instead of
re-training `yolov8s` from scratch later. Separately, this experiment
surfaced a real finding worth acting on regardless of model choice, not
confounded by the night-mode issue: **the dataset has zero night/IR
examples**, and behavior after dark is currently unvalidated and likely
unreliable. Relevant only if the actual deployment scenario includes
low-light conditions — worth a deliberate decision either way, not a
silent gap.
