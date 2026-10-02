---
tags: [decision, computer-vision]
status: Working Decision (2026-09-29)
---

# Prototype Scope — Trash and Standing, Misaligned Deprioritized

## Decision
For the near-term prototype, active CV development focuses on **`trash`
detection** (continuing to grow, per the round log) and **`standing`
detection** (new — pose-estimation based, not yet built), plus getting
the admin UI genuinely working end-to-end with both. **`misaligned` is
deprioritized, not abandoned** — no further labeling/training effort
goes toward it for now.

## Reason
Stated directly by the user. Consistent with the round log's own findings:
`misaligned` has been the most data-starved, least reliable class since
round 2 (7 boxes total, worse mAP50 than `trash` in every experiment,
including getting *worse* rather than better when the `yolov8s` model-size
experiment gave it more capacity to work with — see
`detection/dataset/README.md`'s round log). Rather than keep sinking
labeling effort into a class that also needs a different architecture
entirely (seat detection + rule-based reference-position check, discussed
at length in the round log, not yet built either), the user chose to
redirect effort toward `trash` (which is showing real, measurable
progress) and `standing` (a new capability, off-the-shelf pose estimation,
no custom training data needed the way `trash`/`misaligned` did).

## What this means practically
- Round 4+ dataset work: no more `misaligned` boxes being added. Existing
  `misaligned` labels/weights aren't being deleted, just not grown further.
- `detection/monitor_trash.py` already only handles `trash` — no change
  needed there.
- New work: a `standing` detection path — reuses the existing
  `insert_event`/`resolve_event`/`events.status` infrastructure for a
  `standing` event category, same as `trash`.
- Admin UI: get it genuinely reflecting both `trash` and `standing` events
  well, not just technically functional.

**Update (2026-09-29, same day)**: the original plan — pretrained
`yolov8n-pose.pt` + a hand-built keypoint heuristic, no custom training
needed — was tried first since it's cheaper, and built into
`detection/monitor.py`. Found genuinely broken by live testing, not just
imprecise: multiple real sitting poses (leaning back, sitting upright on
the raised bed) misclassify as standing, and the root cause (a single
fixed head-height threshold can't account for furniture at different
physical elevations in the same room) isn't fixable by better tuning or a
bigger pose model — both were tried. See `detection/monitor.py`'s
docstring for the full calibration history and evidence. **Revised plan**:
train `standing` directly from labeled photos, same box-labeling workflow
as `trash` (not pose/keypoint labeling — a full pose-model retrain would
be much more labor-intensive and might not even fix the core ambiguity).
The pretrained-pose-model path is not being pursued further for now.

**Update (2026-09-30)**: the revised plan above was executed — round 4
(`detection/dataset/README.md`) trained `standing` as a directly-labeled
box class alongside `trash`, both from the same model file, wired into
`detection/monitor.py`. Validation numbers looked strong (`standing`
mAP50 0.995), but a first live-camera test the same day (via
`detection/live_view.py`) found real gaps, most seriously that **people
other than the one in the training photos aren't detected as `standing`
at all** — a possible sign the model learned one person's proportions
rather than a general posture, not yet confirmed as the root cause. Also:
`trash` still false-positives on a person's shirt (unresolved since round
1), and `standing` degrades from a side-on view. Full detail in
`detection/dataset/README.md`'s round 4 live-camera-test entry. **Not yet
a settled outcome** — same "validation numbers looked fine before too"
pattern that killed the pose-heuristic approach; round 5 should
deliberately test with multiple people of different heights/builds
before `standing` is trusted for anyone but the one person it's been
tested on so far.

## Alternatives
- Keep splitting effort three ways (trash/misaligned/standing) — rejected;
  `misaligned` needs a fundamentally different architecture to fix
  properly (see above), and diluting effort across three fronts fits
  neither the timeline nor what's already showing traction.

## May Change?
Yes — `misaligned` could return to active scope later, especially once
someone builds the seat-detection + reference-position architecture (a
good candidate for a groupmate contribution, discussed separately). This
is a prioritization choice for now, not a removal of the feature from the
proposal.

## Change Trigger
Explicit user direction to resume `misaligned` work, or a groupmate
picking up the seat/reference-position architecture as their own
contribution.

## Related
- [[04 - Computer Vision]]
- [[Trash Monitoring Integration]]
- [[Event Model]]
