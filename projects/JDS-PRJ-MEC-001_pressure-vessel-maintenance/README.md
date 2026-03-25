# Pressure Vessel Ongoing Maintenance Program

| | |
|---|---|
| **Document No.** | JDS-PRJ-MEC-001 |
| **Revision** | C |
| **Date** | 2026-03-25 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A complete, reusable service for managing **ongoing maintenance and inspection of pressurised vessels**. Built on Swedish regulations (AFS 2017:3) as the foundation, designed to be adapted to any country's requirements.

This is a service you can offer to clients: *"I will set up and manage your pressure vessel maintenance program, ensuring regulatory compliance and full documentation traceability."*

The JDS system drives the entire workflow — every inventory, inspection plan, supervision round, and inspection report is a JDS document with full traceability.

---

## The Maintenance Cycle

```
SET UP → INVENTORY → CLASSIFY → PLAN → INSPECT → REPORT → UPDATE → REPEAT
  │         │           │         │        │         │         │
  │     TMP-LOG-002  Reg.Ref   TMP-LOG-004  Accredited  TMP-RPT-003  Equipment
  │     (inventory)            (plan)        Inspector   (report)     Register
  │                                                                   Update
  └── JDS-PRO-010 (master procedure) governs every step
```

---

## How This Program Is Organised

```
JDS-PRJ-MEC-001_pressure-vessel-maintenance/
│
├── 01-framework/                         ← UNIVERSAL (works in any country)
│   ├── JDS-LOG-MEC-001_equipment-register.md   ← Master register template
│   ├── JDS-PRO-004_inspection-planning.md      ← How to schedule inspections
│   └── JDS-MAN-MEC-001_documentation-guide.md  ← What records you must keep
│
├── 02-regulations/                       ← COUNTRY-SPECIFIC rules
│   └── SE-sweden/
│       ├── regulatory-reference.md       ← AFS 2017:3 practical reference
│       └── regulatory-traceability-matrix.md ← Maps JDS procedures to AFS 2017:3
│
├── 03-active-programs/                   ← CLIENT WORK (real data)
│   ├── JDS-LOG-MEC-002_*.md              ← AFS 2017:3 inventory guide
│   └── [client-name]/                    ← One folder per client
│       ├── JDS-LOG-MEC-NNN_inventory.md  ← Client equipment register
│       ├── JDS-LOG-MEC-NNN_inspection-plan.md ← Annual inspection plan
│       ├── inspections/                  ← JDS-RPT-MEC-NNN reports
│       ├── supervision/                  ← JDS-LOG-MEC-NNN checklists
│       ├── certificates/                 ← Inspector certificates
│       └── vessel-files/                 ← Per-vessel documentation
│
└── CHANGELOG.md                          ← Master log of ALL changes
```

---

## How to Run a Maintenance Program

Follow **JDS-PRO-010** (Ongoing Maintenance Program Procedure) for the complete workflow. Quick reference:

| Step | What to Do | JDS Template |
|------|-----------|-------------|
| 1. Create client folder | Set up `03-active-programs/[client]/` | — |
| 2. Build equipment register | Walk the site, record every vessel | JDS-TMP-LOG-002 |
| 3. Classify vessels | Determine risk class A/B, PED category | Regulatory reference |
| 4. Build inspection plan | Schedule all inspections for the year | JDS-TMP-LOG-004 |
| 5. Perform supervision | Regular supervision walk-arounds | JDS-TMP-LOG-003 |
| 6. Perform inspections | Accredited inspector (Class A) or own (Class B) | JDS-TMP-RPT-003 |
| 7. Report and update | Document findings, update register | JDS-PRO-008 |

---

## Related Documents

### Procedures

| Doc No. | Title |
|---------|-------|
| JDS-PRO-010 | Ongoing Maintenance Program Procedure |
| JDS-PRO-004 | Inspection Planning Procedure |
| JDS-PRO-008 | Corrective Action Procedure |
| JDS-PRO-009 | Competence Management Procedure |

### Templates

| Doc No. | Title | Use |
|---------|-------|-----|
| JDS-TMP-LOG-002 | Supervision Inventory Template | Equipment register |
| JDS-TMP-LOG-003 | Supervision Checklist Template | Supervision checklists |
| JDS-TMP-LOG-004 | Annual Inspection Plan Template | Annual inspection plan |
| JDS-TMP-RPT-003 | Inspection Report Template | Post-inspection reports |

### Framework

| Doc No. | Title |
|---------|-------|
| JDS-LOG-MEC-001 | Equipment Register (Framework) |
| JDS-MAN-MEC-001 | Documentation Guide |
| JDS-LOG-MEC-002 | Pressure Vessel Inventory Guide |

---

## How to Expand to a New Country

1. Create a new folder under `02-regulations/` (e.g., `NO-norway/`)
2. Document that country's pressure vessel regulations
3. Create a traceability matrix mapping JDS procedures to those regulations
4. The templates and procedures still apply — only the regulatory reference changes

**You never touch the Swedish files to add another country.**

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — project structure and framework |
| B | 2026-03-25 | N. Johansson | Added maintenance workflow, linked to PRO-010, templates, and active program structure |
| C | 2026-03-25 | N. Johansson | Language authority update — all terminology now JDS English. Added regulatory traceability matrix. |
