# detection — BantayAralan CV Dataset & Training Tracking

Status: **Planned / dataset collection started** — this folder holds no
runnable code. It tracks the training dataset and labeling work for the
proposal's CV pipeline (YOLOv8, per
[Knowledge/04 - Computer Vision.md](<../Knowledge/04%20-%20Computer%20Vision.md>)),
which otherwise has zero source code anywhere in this repo. See root
[`CLAUDE.md`](../CLAUDE.md) for the project-wide working-draft/status-label
rules; this file assumes you've read those.

## What actually exists here

- [`dataset/README.md`](dataset/README.md) — class taxonomy and a log of
  labeling/training rounds done in an external no-code tool.
- Nothing else. No inference code, no camera integration, no ByteTrack, no
  training scripts. Training itself happens outside this repo (a no-code
  tool — Roboflow, or similar — chosen for the first proof-of-concept; see
  [Knowledge/11 - Decisions/No-Code Tool for Initial CV Proof-of-Concept.md](<../Knowledge/11%20-%20Decisions/No-Code%20Tool%20for%20Initial%20CV%20Proof-of-Concept.md>)).

## Do not commit

- Raw or labeled classroom photos, exported dataset archives, or trained
  model weights (`.pt`, `.onnx`, etc.). See `.gitignore` — these are
  excluded on purpose. They're large binary/derived artifacts that don't
  belong in git history, not (as far as this dataset goes) identity-bearing
  content — but treat any future image that happens to include a
  recognizable student the same way regardless: don't commit it, and see
  [.claude/rules/privacy-and-ethics.md](../.claude/rules/privacy-and-ethics.md).
- Any Roboflow/cloud-tool API key or credential — those are secrets, not
  project config.

## Class taxonomy

Reuses the `events.category` values already defined in
`admin-ui/backend/db.py` / [[Event Model]] rather than inventing new label
names, so a future real detector's output maps onto the existing schema
without a translation layer:

- `trash` — "Trash / Scattered Objects" (clutter)
- `misaligned` — "Misaligned Seat" / Table

Only these two are in scope for the top-down/clutter camera dataset. The
`standing` category belongs to the separate behavior-detection camera
pipeline (ceiling-mounted) and is out of scope here.

## Honest scale caveat

Any dataset here starting in the single digits to low tens of images is a
**pipeline proof-of-concept**, not a usable detector — don't let a
successfully-exported model from a tiny dataset be described in the paper
as validated or production-ready. Log the actual image count per class in
`dataset/README.md`'s round log so this stays checkable later.

## When this becomes real code

If/when actual training code, inference code, or model weights land (e.g. a
Python training script, an exported `.pt` wired into an inference loop),
update this file's Status line and expand it the way `admin-ui/CLAUDE.md`
documents that subsystem — architecture, commands, common failure modes —
rather than leaving this dataset-tracking doc as the only source of truth.
