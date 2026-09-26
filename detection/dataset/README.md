# CV Dataset Tracking

Tracks labeling/training rounds done in an external no-code tool (Roboflow
or similar). See [`../CLAUDE.md`](../CLAUDE.md) for what does and doesn't
belong in this folder — no raw images, exports, or weights get committed.

## Classes

| Class        | Meaning                          | Matches `events.category` |
|--------------|-----------------------------------|----------------------------|
| `trash`      | Trash / scattered objects (clutter) | `trash` |
| `misaligned` | Misaligned seat/table              | `misaligned` |

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

### Round 1 — 2026-09-25

- **Source images**: 7 (not committed — see `.gitignore`)
- **Class split**: TBD (fill in after labeling — how many boxes per class)
- **Tool**: Roboflow (free tier)
- **Augmentation applied**: TBD
- **Train/valid/test split**: TBD
- **Model**: TBD (Roboflow "Fast"/auto model, or exported YOLOv8 via
  Ultralytics HUB)
- **Result**: TBD — proof-of-concept only; not a claim of working
  detection accuracy until real evaluation numbers exist (see
  [Knowledge/09 - Testing & Evaluation.md](<../../Knowledge/09%20-%20Testing%20&%20Evaluation.md>))
- **Roboflow project link**: TBD
