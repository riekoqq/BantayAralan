---
tags: [decision, computer-vision]
status: Working Decision (2026-09-25)
---

# No-Code Tool for Initial CV Proof-of-Concept

## Decision
The first CV training pass (starting from 7 clutter/misaligned-seat photos)
uses a browser-based no-code tool (Roboflow, or an equivalent such as
Ultralytics HUB) for labeling, augmentation, and training — not a local
Python training script. See [[detection/dataset/README|CV Dataset
Tracking]] for the round-by-round log.

## Reason
At this stage there's no training code, no labeled dataset, and only 7
source images. A no-code tool gets from raw photos to a first exported
model with the least setup, and its built-in augmentation step is the only
practical way to get useful variation out of a single-digit image count.
This is about proving the labeling → training → export shape of the
pipeline works, not producing a usable detector.

## What this does *not* mean
- It does not mean YOLOv8 (the confirmed model per [[04 - Computer
  Vision]]) is being replaced — Roboflow/Ultralytics HUB export in YOLOv8
  format, so the model architecture stays the same; only *how* training is
  run (no-code UI vs. a local script) differs for this first round.
- It does not mean 7 images (or even the post-augmentation count) is
  treated as a sufficient training set. See the "Honest scale caveat" in
  [`detection/CLAUDE.md`](../../detection/CLAUDE.md).

## Alternatives
- A local Ultralytics YOLOv8 Python training script — rejected for round 1
  only because it adds environment setup (Python, CUDA/GPU or a Colab
  notebook) before there's even a labeled dataset to train on. Worth
  revisiting once the dataset is large enough that no-code labeling UIs
  become the bottleneck rather than a shortcut.

## May Change?
Yes — once the dataset grows past what's comfortable to label in a
browser UI, or once real inference code is being built (at which point a
reproducible local/scripted training pipeline matters more than no-code
convenience).

## Change Trigger
Moving from proof-of-concept to a dataset/training setup that needs to be
reproducible in CI or documented as a repeatable pipeline in the thesis
write-up.

## Related
- [[04 - Computer Vision]]
- [[Camera Model and Detection Model Version Confirmed]]
- [[Event Model]]
