# Vessel Supervision System

| | |
|---|---|
| **Document No.** | JDS-PRJ-MEC-002 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A complete system for **creating, managing, and performing ongoing supervision programs** for pressurised vessels. Built on Swedish regulations (AFS 2017:3, consolidated with AFS 2019:1, AFS 2020:10, and AFS 2022:2) as the regulatory foundation, designed so a competent engineer can build a supervision program for any site and execute it systematically.

This project delivers what AFS 2017:3 Chapter 2 requires: a documented supervision program that ensures every pressurised vessel is monitored between formal inspections by accredited bodies.

> **Relationship to JDS-PRJ-MEC-001:** The Pressure Vessel Maintenance Program (PRJ-MEC-001) covers the full maintenance cycle — inventory, classification, inspection planning, and reporting. This project (PRJ-MEC-002) focuses specifically on the **ongoing supervision** element: the day-to-day and periodic monitoring that the operator performs between formal inspections.

---

## The Supervision Cycle

```
BUILD PROGRAM → EQUIP PERSONNEL → EXECUTE ROUNDS → RECORD FINDINGS → ACT → REVIEW → IMPROVE
      │               │                │                 │            │       │          │
  TMP-LOG-005     PRO-009         TMP-LOG-006       LOG register   PRO-008  TMP-LOG-007  Update
  (program)     (competence)     (round record)      (findings)   (action)  (annual)    program
```

---

## How This Project Is Organised

```
JDS-PRJ-MEC-002_vessel-supervision-system/
│
├── 01-system/                                    ← SYSTEM FRAMEWORK
│   ├── JDS-MAN-MEC-002_supervision-program-manual.md   ← How to build & run programs
│   └── JDS-LOG-MEC-005_program-register.md             ← Master register of all active programs
│
├── 02-regulations/                               ← REGULATORY FOUNDATION
│   └── SE-sweden/
│       ├── JDS-RPT-MEC-003_afs2017-3-consolidated.md  ← English summary (all amendments)
│       └── regulatory-traceability-matrix.md            ← Maps program requirements to AFS 2017:3
│
├── 03-program-templates/                         ← TEMPLATES FOR BUILDING PROGRAMS
│   ├── JDS-TMP-LOG-005_supervision-program-template.md ← The main program document
│   ├── JDS-TMP-LOG-006_supervision-round-template.md   ← Round execution record
│   └── JDS-TMP-LOG-007_annual-review-template.md       ← Annual program review
│
└── 04-active-programs/                           ← WHERE REAL PROGRAMS LIVE
    └── README.md                                 ← How to create a new program
```

---

## How to Use This System

### Creating a New Supervision Program

1. **Start with the manual** — Read JDS-MAN-MEC-002 for the complete methodology
2. **Survey the site** — Identify all pressurised vessels requiring supervision
3. **Build the program** — Use JDS-TMP-LOG-005 to create a site-specific supervision program
4. **Define check intervals** — Set daily, weekly, monthly, and quarterly tasks
5. **Assign personnel** — Ensure competence per JDS-PRO-009
6. **Register the program** — Add it to JDS-LOG-MEC-005

### Performing Supervision Rounds

1. **Prepare** — Review the program for today's required checks
2. **Execute** — Use JDS-TMP-LOG-006 to record the round
3. **Document findings** — Record any deviations or concerns
4. **Act on findings** — Follow JDS-PRO-008 for corrective actions
5. **File the record** — Store in the client's supervision folder

### Annual Review

1. **Review program effectiveness** — Use JDS-TMP-LOG-007
2. **Update the program** — Incorporate lessons learned, regulatory changes, equipment changes
3. **Verify compliance** — Check against regulatory traceability matrix
4. **Approve for next year** — Sign off and issue updated program

---

## Related Documents

### Within This Project

| Doc No. | Title | Purpose |
|---------|-------|---------|
| JDS-MAN-MEC-002 | Supervision Program Manual | How to build and run programs |
| JDS-LOG-MEC-005 | Program Register | Track all active programs |
| JDS-RPT-MEC-003 | AFS 2017:3 Consolidated Summary | Regulatory foundation (English) |
| JDS-TMP-LOG-005 | Supervision Program Template | Create new programs |
| JDS-TMP-LOG-006 | Supervision Round Record | Execute and record rounds |
| JDS-TMP-LOG-007 | Annual Review Template | Review program annually |

### JDS System Documents

| Doc No. | Title | Purpose |
|---------|-------|---------|
| JDS-PRO-008 | Corrective Action Procedure | Handle findings |
| JDS-PRO-009 | Competence Management | Personnel qualifications |
| JDS-PRO-010 | Ongoing Maintenance Program | Master maintenance procedure |
| JDS-PRJ-MEC-001 | Pressure Vessel Maintenance Program | Parent maintenance system |

---

## Regulatory Basis

This system is built on AFS 2017:3 (Use and Inspection of Pressurised Equipment), consolidated with all published amendments:

| Regulation | What It Changes |
|-----------|----------------|
| **AFS 2017:3** | Base regulation — defines ongoing supervision requirements |
| **AFS 2019:1** | Clarified supervision scope, adjusted interval provisions |
| **AFS 2020:10** | Extended inspection deadlines (pandemic provisions), digital documentation |
| **AFS 2022:2** | Revised competence requirements, updated classification thresholds |

The consolidated regulatory summary (JDS-RPT-MEC-003) translates all relevant requirements to English. The traceability matrix maps every program element to a specific regulatory paragraph.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial release — complete vessel supervision system |
