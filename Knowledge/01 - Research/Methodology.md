---
tags: [research, methodology]
status: Proposal Requirement
---

# Methodology

## Research design
Developmental Research Design (DDR / Design and Development Research), combined with a Quantitative Experimental Evaluation component — chosen because the study builds and evaluates a system rather than only observing a phenomenon (Richey & Klein, 2005; Wang, 2025).

## Procedure — four phases
1. **System development** — design/build hardware+software integration (cameras, CV models, event-based imaging, alerts, DB logging, GUI).
2. **System testing** — controlled scenarios (normal, disruptive, unclean classroom conditions) measuring detection accuracy, response time, stability, reliability across multiple runs with refinement.
3. **System implementation** — deployment in actual or simulated classrooms with optimized camera positioning, plus teacher orientation.
4. **Evaluation** — pre-implementation survey (teachers' existing classroom-management challenges/needs) and post-implementation survey (usability/effectiveness), supplemented by system-generated logs/timestamps/images/metrics.

## Instruments/tools
- **Hardware**: ceiling-mounted camera, top-down camera, computer/laptop — see [[08 - Hardware]].
- **Software**: Python, OpenCV, YOLO-based model (e.g. YOLO11m), ByteTrack, SQLite, a GUI framework (Tkinter or PyQt — explicitly **undecided** in the proposal) — see [[04 - Computer Vision]], [[06 - Database]].
- **Survey questionnaire**, two parts, 5-point Likert scale (Strongly Disagree 1 → Strongly Agree 5): pre-use (classroom-management difficulties) and post-use (usability, clarity, detection accuracy, promptness, usefulness). To be reviewed by expert teachers/IT professionals before administration.
- **System-generated data**: detected behavior/objects, alert timestamps, event logs, captured images, and performance metrics (accuracy, precision, recall, FPS, latency).

## Participants
Public grade-school teachers, selected via **purposive sampling** — they are the ones managing the classroom and will judge the system's ability to observe behavior and support decision-making. Participants will be informed to keep the design ethical and helpful.

## Data sources
- Primary: qualitative interviews/surveys with teachers (classroom-management experience, system usability/effectiveness).
- Secondary: system-generated logs/metrics (accuracy, speed), and related literature.

## Data analysis plan
Survey/interview responses grouped by recurring themes (functionality, usability, reliability, performance); Likert responses analyzed for patterns and response frequency; system-generated behavior/tracking/event data reviewed alongside survey results to determine overall acceptability and whether objectives were met.

## Status
**Proposal Requirement.** No phase of this procedure (development beyond the admin-UI prototypes, testing, implementation, or evaluation with real teachers) has been carried out in this repository yet — see [[09 - Testing & Evaluation]] for what has actually been done (informal manual UI testing only).

## Related
- [[Research Proposal]]
- [[Evaluation Standards]]
- [[09 - Testing & Evaluation]]
