# Pressure Vessel Ongoing Maintenance Program

| | |
|---|---|
| **Document No.** | JDS-PRJ-MEC-001 |
| **Revision** | D |
| **Date** | 2026-04-11 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A complete, reusable system for managing **ongoing maintenance, supervision, and inspection of pressurised vessels**. Built on Swedish regulations (AFS 2017:3) as the foundation, designed to be adapted to any country's requirements.

This project covers two integrated workflows:

1. **Maintenance Program** — the full lifecycle (inventory, classify, plan, inspect, report, update)
2. **Ongoing Supervision Program** — the day-to-day/monthly supervision between formal inspections (AFS 2017:3 2 Kap. §6, 4 Kap. §17)

The JDS system drives the entire workflow — every inventory, supervision program, round record, inspection report, and lifetime journal is a JDS document with full traceability.

---

## The Complete Cycle

```
SET UP → INVENTORY → CLASSIFY → PLAN → SUPERVISE → INSPECT → REPORT → REVIEW → REPEAT
  │         │           │         │        │           │         │         │
  │     TMP-LOG-008  jds-classify  TMP-LOG-004  TMP-LOG-005  Accredited  TMP-RPT-003  TMP-LOG-007
  │     (inventory)  (.py)         (plan)       TMP-LOG-006  Inspector   (report)     (annual review)
  │                                             (round)
  └── JDS-PRO-010 (master procedure) governs every step
```

---

## How This Project Is Organised

```
JDS-PRJ-MEC-001/
│
├── 01-framework/                         ← UNIVERSAL (works in any country)
│   ├── JDS-LOG-MEC-001                   ← Master equipment register (framework)
│   ├── JDS-PRO-011                       ← How to schedule inspections
│   └── JDS-MAN-MEC-001                   ← What records you must keep
│
├── 02-regulations/                       ← COUNTRY-SPECIFIC rules
│   └── SE-sweden/
│       ├── JDS-RPT-MEC-003              ← AFS 2017:3 consolidated (English)
│       ├── regulatory-reference.md       ← Practical regulatory reference
│       ├── regulatory-traceability-matrix.md ← Maps JDS procedures to AFS 2017:3
│       └── *.pdf                         ← Original AFS regulation PDFs
│
├── 03-supervision/                       ← ONGOING SUPERVISION SYSTEM
│   ├── JDS-MAN-MEC-002                   ← Supervision program manual
│   └── JDS-LOG-MEC-005                   ← Master register of active programs
│
├── 04-active-programs/                   ← CLIENT WORK & EXAMPLES
│   ├── JDS-LOG-MEC-002                   ← AFS 2017:3 inventory guide
│   ├── JDS-LOG-MEC-006..010             ← Gothenburg Workshop examples
│   └── example-vessels.csv               ← Example data for automation
│
├── 05-flt-program/                       ← COMPLETE FLT PACKAGE (start here)
│   └── README.md                         ← Document index for performing FLT
│
├── AH_Automation.xlsm                    ← Reference Excel (heritage)
└── CHANGELOG.md                          ← Master log of ALL changes
```

---

## How to Run a Maintenance & Supervision Program

Follow **JDS-PRO-010** (Ongoing Maintenance Program Procedure) for the complete workflow.

### Setup

| Step | What to Do | JDS Template |
|------|-----------|-------------|
| 1 | Build equipment inventory | JDS-TMP-LOG-008 |
| 2 | Classify vessels (auto or manual) | `jds-classify.py` or regulatory reference |
| 3 | Build inspection plan | JDS-TMP-LOG-004 |
| 4 | Create supervision program | JDS-TMP-LOG-005 |

### Execution

| Step | What to Do | JDS Template |
|------|-----------|-------------|
| 5 | Perform supervision rounds | JDS-TMP-LOG-006 |
| 6 | Perform formal inspections | JDS-TMP-RPT-003 |
| 7 | Track equipment lifetime | JDS-TMP-LOG-009 |
| 8 | Report findings, corrective actions | JDS-PRO-008 |

### Review

| Step | What to Do | JDS Template |
|------|-----------|-------------|
| 9 | Annual program review | JDS-TMP-LOG-007 |
| 10 | Update inventory and plan | Repeat from step 1 |

---

## Related Documents

### Procedures

| Doc No. | Title |
|---------|-------|
| JDS-PRO-010 | Ongoing Maintenance Program Procedure |
| JDS-PRO-011 | Inspection Planning Procedure |
| JDS-PRO-008 | Corrective Action Procedure |
| JDS-PRO-009 | Competence Management Procedure |

### Templates

| Doc No. | Title | Use |
|---------|-------|-----|
| JDS-TMP-LOG-005 | Supervision Program Template | Build a supervision program |
| JDS-TMP-LOG-006 | Supervision Round Record Template | Record each supervision round |
| JDS-TMP-LOG-007 | Annual Review Template | Annual program effectiveness review |
| JDS-TMP-LOG-008 | Equipment Inventory Template | Equipment register with auto-classification |
| JDS-TMP-LOG-009 | Lifetime Journal Template | Track remaining equipment lifetime |
| JDS-TMP-LOG-004 | Annual Inspection Plan Template | Schedule formal inspections |
| JDS-TMP-RPT-003 | Inspection Report Template | Post-inspection reports |

### Superseded Templates

| Doc No. | Replaced By | Reason |
|---------|-------------|--------|
| JDS-TMP-LOG-001 | JDS-TMP-LOG-008 | Auto-classification, richer fields |
| JDS-TMP-LOG-002 | JDS-TMP-LOG-008 | Same coverage, better version |
| JDS-TMP-LOG-003 | JDS-TMP-LOG-006 | Per-vessel checks, severity, sign-off |

---

## How to Expand to a New Country

1. Create a new folder under `02-regulations/` (e.g., `NO-norway/`)
2. Document that country's pressure vessel regulations
3. Create a traceability matrix mapping JDS procedures to those regulations
4. The templates and procedures still apply — only the regulatory reference changes

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — project structure and framework |
| B | 2026-03-25 | N. Johansson | Added maintenance workflow, linked to PRO-010, templates, and active program structure |
| C | 2026-03-25 | N. Johansson | Language authority update — all terminology now JDS English. Added regulatory traceability matrix. |
| D | 2026-04-11 | N. Johansson | Merged JDS-PRJ-MEC-002 (Vessel Supervision System) into this project. Restructured folders: added 03-supervision/ and 04-active-programs/. Updated template references to TMP-LOG-005-009. Consolidated AFS PDFs. |
