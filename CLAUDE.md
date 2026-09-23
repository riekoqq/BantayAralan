# BantayAralan — Claude Code Guide

## What this is

BantayAralan: Real-Time Student Behavior and Classroom Orderliness System —
a BSCpE thesis project at Holy Angel University (Jose, Santos, Tolentino)
proposing a computer-vision system to help teachers detect disruptive
classroom behavior and classroom disorder (clutter, misaligned seats/desks),
log events, and alert the teacher — without identifying individual students.

**The project's broader knowledge — research, requirements, architecture,
decisions, open questions — now lives in the Obsidian-compatible vault at
[`Knowledge/`](Knowledge/00%20-%20Project%20Overview.md).** Start there for
anything beyond immediate coding instructions. This file, `.claude/rules/`,
and any subsystem `CLAUDE.md` hold only the instructions Claude Code must
actively follow while working in this repo — they intentionally do not
restate the knowledge base.

## Read this first

- The research proposal (`Team8_BantayAralan-Proposal.docx.pdf`) is a
  **working draft** — see
  [Knowledge/01 - Research/Research Proposal.md](<Knowledge/01 - Research/Research Proposal.md>).
  Requirements, design, and technical decisions may change after adviser
  consultation. Never treat a proposal statement as final, or as evidence
  that it's implemented.
- Only two subsystems have actual source code: [`admin-ui/`](admin-ui/)
  (Flask + vanilla JS web/webview admin UI, mock data) and
  [`desktop-app/`](desktop-app/) (PySide6 native admin UI, mock data,
  current primary prototype). Neither has a camera, a model, or a connection
  to any detection backend — each consumes mock SQLite data it generates
  itself. See their own `CLAUDE.md` files and
  [Knowledge/03 - Architecture/Two Admin UI Prototypes.md](<Knowledge/03 - Architecture/Two Admin UI Prototypes.md>).
- [`anti-ai-slop/`](anti-ai-slop/) is a separate third-party tool (its own
  git repo), not BantayAralan code — never edit it as part of this project.
- The CV pipeline (YOLO11m, ByteTrack, camera capture) described in the
  proposal has **no source code anywhere in this repo**.

When more source code is added, update this file, the relevant `Knowledge/`
notes, and add a scoped subsystem `CLAUDE.md` — don't let any of them go
stale.

## Knowledge map

```text
Knowledge/
├── 00 - Project Overview.md          entry point — start here
├── 01 - Research/                    proposal, research questions, methodology, standards
├── 02 - Requirements/                functional / non-functional / privacy / UI requirements
├── 03 - Architecture/                system architecture, the two admin-UI prototypes
├── 04 - Computer Vision.md           proposed CV pipeline (not implemented)
├── 05 - Events & Evidence/           event model, evidence system
├── 06 - Database.md                  SQLite schema, both implementations
├── 07 - UI UX/                       UI direction, admin-ui, desktop-app
├── 08 - Hardware.md                  cameras, processing PC
├── 09 - Testing & Evaluation.md      proposal metrics vs. actual testing done
├── 10 - Privacy & Ethics.md          privacy-first constraints
├── 11 - Decisions/                   working decisions with reasons + change triggers
├── 12 - Open Questions.md            unresolved items — check before assuming an answer
└── 13 - Meeting Notes/               (empty — add notes here as meetings happen)
```

## How to work in this repo

1. **Source code is authoritative for "implemented."** Before stating a
   feature exists, point to the file/function that implements it — see
   [Knowledge/00 - Project Overview.md](<Knowledge/00 - Project Overview.md>)
   and each subsystem's own `CLAUDE.md`.
2. **Use status labels** from
   [.claude/rules/proposal-vs-implementation.md](.claude/rules/proposal-vs-implementation.md)
   whenever discussing a proposal-derived feature: Implemented / Partially
   implemented / Planned / Proposal requirement / Expected by current
   working draft / Not yet implemented / Under consideration / Unclear /
   Deprecated / Changed from proposal.
3. **Preserve privacy/ethics constraints** in any code — see
   [.claude/rules/privacy-and-ethics.md](.claude/rules/privacy-and-ethics.md)
   and [Knowledge/10 - Privacy & Ethics.md](<Knowledge/10 - Privacy & Ethics.md>).
4. **Don't silently resolve contradictions or make decisions on the project
   owners' behalf.** If the proposal, the code, and existing docs disagree
   (several such conflicts are already logged in
   [Knowledge/12 - Open Questions.md](<Knowledge/12 - Open Questions.md>)),
   document both sides and ask rather than picking one.
5. Don't modify the proposal PDF. Don't invent code, commands, or file paths
   that don't exist in this repo. Don't copy large chunks of the proposal or
   of source code into context files — summarize and point at the real file.
6. When a real subsystem is added (detection/, tracking/, etc.), give it its
   own scoped `CLAUDE.md` (see `admin-ui/CLAUDE.md` / `desktop-app/CLAUDE.md`
   as examples) and add matching notes under `Knowledge/`.

## Commands

Native desktop admin UI (primary prototype — see [desktop-app/CLAUDE.md](desktop-app/CLAUDE.md)):

```bash
cd desktop-app
pip install -r requirements.txt
python run.py            # opens a native window directly, no browser
```

Browser-based admin UI (earlier prototype, kept as reference — see [admin-ui/CLAUDE.md](admin-ui/CLAUDE.md)):

```bash
cd admin-ui
pip install -r requirements.txt
python run_web.py       # web app mode, http://127.0.0.1:5057
python run_desktop.py   # webview window mode, needs `pip install pywebview`
```

There is no build/run/test tooling for the CV detection pipeline (YOLO/ByteTrack/
camera capture) — that part of the proposal has no source code yet. Do not fabricate
commands for it.
