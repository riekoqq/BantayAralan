---
tags: [research, proposal]
status: Proposal Requirement
---

# Research Proposal

Source: `Team8_BantayAralan-Proposal.docx.pdf` (working draft, dated March 29, 2026). Authors: Chloe Lane B. Jose, Raynier Ronn G. Santos, Justin Rieko S. Tolentino — BSCpE, School of Engineering and Architecture, Holy Angel University.

This note summarizes the proposal's framing; it does not reproduce it. Read the PDF for exact wording, figures (Conceptual Framework, Block Diagram, System Flowchart), and full citations — see [[References]].

## Problem being addressed
Teachers must simultaneously deliver instruction and monitor student behavior and classroom cleanliness. Cited literature (Ćali et al. 2024; Hamidi et al. 2024; Dilabayan & Sambo 2024) links effective classroom management — including handling disruptive behavior and maintaining cleanliness — to academic performance, and finds Philippine teachers report managing misbehavior as a frequent, difficult, ongoing task. Prior computer-vision classroom-behavior systems (Lin et al. 2021; Yang 2024; Sheng et al. 2025) demonstrate feasibility of real-time behavior detection (reported accuracies up to ~95–97% in cited studies), and cluttered-object detection research (Bashkirova et al. 2021; Liu et al. 2024) establishes both promise and known difficulty (overlapping/ambiguous objects) for the clutter-detection half of the problem.

## Significance framing
The proposal frames impact using the **Triple Bottom Line** (social/economic/environmental) and alignment with **SDG 4** (Quality Education) and **SDG 9** (Industry, Innovation and Infrastructure).

## Conceptual framework (Figure 1, IPO model)
- **Input**: ceiling-mounted + top-down cameras; Python, OpenCV, YOLO11m, supporting libraries.
- **Process**: capture video → pose estimation + object detection → tracking → seat/table alignment analysis against thresholds.
- **Output**: real-time annotated video in the GUI, logged events (standing behavior, trash detection, misaligned furniture), saved snapshots.

## Block diagram (Figure 2) and system flowchart (Figure 3)
Ceiling camera feeds OpenCV → YOLO11m → tracking → behavior detection; top-down camera independently feeds the alignment-detection module. Both converge into SQLite event logging and the desktop GUI. The flowchart describes a continuous capture → detect → track → decide → log/snapshot → display loop. See [[System Architecture]] for how this maps (or doesn't yet map) onto anything in the repository.

## Status
**Proposal Requirement** — none of this pipeline exists as code in this repository. See [[04 - Computer Vision]] and [[System Architecture]].

## Related
- [[Research Questions & Objectives]]
- [[Scope and Limitations]]
- [[Methodology]]
- [[Evaluation Standards]]
- [[References]]
