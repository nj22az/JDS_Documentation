# Ongoing Maintenance Program — Pressurised Vessels

| | |
|---|---|
| **Document No.** | JDS-PRO-010 |
| **Revision** | B |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how to set up, run, and maintain an **Ongoing Maintenance Program** for pressurised vessels. It is the master procedure for pressure vessel supervision within JDS.

It turns the JDS system into an operational tool: every step of the maintenance cycle produces a JDS document, every inspection is tracked, and every finding is closed.

> **In plain language:** This is the master procedure for running a pressure vessel maintenance program. Follow it from top to bottom for a new client. Follow the annual cycle for ongoing work.

---

## 2. Scope

This procedure applies to:
- Pressure vessels classified under applicable national regulations
- Safety devices (relief valves, rupture discs, pressure switches) protecting those vessels
- Piping systems under the same regulatory scope, where applicable

It covers the full lifecycle:

```
SET UP → INVENTORY → CLASSIFY → PLAN → INSPECT → REPORT → UPDATE → REPEAT
```

---

## 3. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| **Operator** | Ensure the maintenance program is in place, fund inspections, act on findings |
| **Program Manager** | Run the program day-to-day — this role uses JDS |
| **Accredited Inspector** | Perform Class A inspections (accredited inspection bodies) |
| **Competent Person** | Perform Class B inspections (documented competence per JDS-PRO-009) |

---

## 4. Setting Up a New Program

### Step 1 — Create the Client Folder

Create a new client folder under `03-active-programs/`:

```
03-active-programs/
└── [client-name]/
    ├── JDS-LOG-MEC-NNN_inventory.md       ← Equipment register (from TMP-LOG-002)
    ├── JDS-LOG-MEC-NNN_inspection-plan.md ← Annual inspection plan (from TMP-LOG-004)
    ├── inspections/                        ← Inspection reports (JDS-RPT-MEC-NNN)
    ├── supervision/                        ← Supervision checklists (JDS-LOG-MEC-NNN)
    ├── certificates/                       ← Scanned certificates from inspectors
    └── vessel-files/                       ← One subfolder per vessel
        ├── PV-001/                         ← Manufacturer docs, drawings, history
        ├── PV-002/
        └── ...
```

### Step 2 — Build the Equipment Register

1. Use template **JDS-TMP-LOG-002** (Supervision Inventory Template)
2. Walk the site and record every pressure vessel
3. Photograph every nameplate
4. Fill in all mandatory fields (marked M)
5. Register the document in `jds/registry/document-register.md`

### Step 3 — Classify Every Vessel

For each vessel, determine:

| Decision | How |
|---|---|
| Is it in scope? | Maximum allowable pressure > 0.5 bar AND pressure-volume product > 50 bar·L |
| What is the fluid group? | Group 1 (dangerous) or Group 2 (other) |
| What is the risk class? | Class A (higher risk, requires accredited inspector) or Class B (lower risk) |
| What PED category? | I, II, III, IV, or Art. 4.3 |

Record the classification in the equipment register.

### Step 4 — Build the Inspection Plan

1. Use template **JDS-TMP-LOG-004** (Annual Inspection Plan Template)
2. For each vessel, enter the inspection intervals:

| Risk Class | External | Internal | Pressure Test |
|---|---|---|---|
| Class A | 2 years | 6 years | 12 years |
| Class B | 2 years | 6 years | — |

3. Calculate next due dates from the last inspection (or commissioning date for new vessels)
4. Book accredited inspectors for Class A items **at least 3 months ahead**

### Step 5 — Establish Supervision Routines

1. Use template **JDS-TMP-LOG-003** (Supervision Checklist Template)
2. Define a monthly or quarterly walk-around checklist
3. Assign responsible person for each walk-around
4. File completed checklists in the `supervision/` folder

---

## 5. Annual Maintenance Cycle

Once set up, the program runs on an annual cycle:

### Q1 (January–March) — Planning

| Task | Document | Template |
|---|---|---|
| Review inspection plan for the year | JDS-LOG-MEC-NNN | TMP-LOG-004 |
| Book inspectors for planned inspections | — | — |
| Review overdue items from previous year | Inspection plan | — |
| Update equipment register if vessels added/removed | JDS-LOG-MEC-NNN | TMP-LOG-002 |

### Q2–Q3 (April–September) — Execution

| Task | Document | Template |
|---|---|---|
| Perform scheduled inspections | JDS-RPT-MEC-NNN | TMP-RPT-003 |
| Perform routine supervision | JDS-LOG-MEC-NNN | TMP-LOG-003 |
| Test safety devices per schedule | Safety device register | — |
| Document findings and corrective actions | JDS-RPT-MEC-NNN | — |

### Q4 (October–December) — Review & Close Out

| Task | Document | Template |
|---|---|---|
| Verify all planned inspections were completed | Inspection plan | — |
| Close out all findings and corrective actions | CA log | JDS-PRO-008 |
| Update equipment register with latest results | JDS-LOG-MEC-NNN | — |
| Prepare inspection plan for next year | JDS-LOG-MEC-NNN | TMP-LOG-004 |
| Archive completed inspection reports | `inspections/` | — |

---

## 6. Performing an Inspection

### Before the Inspection

1. Prepare the vessel: isolate, depressurise, drain/clean if internal
2. Gather previous inspection reports for the inspector
3. Prepare access (scaffolding, lighting, ventilation for confined spaces)
4. Complete a pre-inspection risk assessment

### During the Inspection

1. The accredited inspector (Class A) or competent person (Class B) performs the inspection
2. Document all findings in real-time
3. Photograph significant findings

### After the Inspection

1. Receive the inspection certificate from the inspector
2. Create an inspection report: **JDS-RPT-MEC-NNN** (use TMP-RPT-003)
3. Update the equipment register:
   - Last Inspection → today's date
   - Next Due → calculated from interval
   - Result → APPROVED / APPROVED WITH REMARKS / REJECTED
   - Certificate Ref → new certificate number
4. File the certificate in `certificates/`
5. If findings require action: create corrective actions per JDS-PRO-008
6. Log the update in the project CHANGELOG

---

## 7. Handling Findings

| Result | Action |
|---|---|
| **Approved** | Update register, file certificate, no further action |
| **Approved with remarks** | Update register, create monitoring actions, set follow-up date |
| **Rejected** | Take vessel OUT OF SERVICE immediately, create corrective action, do not return to service until re-inspected and approved |

All findings follow JDS-PRO-008 (Corrective Action Procedure).

---

## 8. Document Map — What JDS Produces

| Activity | JDS Document Type | Template |
|---|---|---|
| Equipment inventory | LOG (register) | JDS-TMP-LOG-002 |
| Annual inspection plan | LOG (plan) | JDS-TMP-LOG-004 |
| Routine supervision | LOG (checklist) | JDS-TMP-LOG-003 |
| Inspection report | RPT (report) | JDS-TMP-RPT-003 |
| Risk assessment | RPT (assessment) | JDS-TMP-RPT-001 |
| Corrective action | CA log entry | JDS-PRO-008 |
| Competence records | Training log | JDS-PRO-009 |

---

## 9. JDS Tools

| Task | Command |
|---|---|
| Validate all documents | `python3 scripts/jds-validate.py` |
| Generate inspection report PDF | `python3 scripts/md2pdf.py <report.md>` |
| Generate letter to inspector/client | `python3 scripts/md2letter.py <letter.md>` |
| Check all links and registrations | `python3 scripts/jds-validate.py --fix` |

---

## 10. References

| Document | Purpose |
|---|---|
| JDS-PRO-004 | Inspection Planning Procedure |
| JDS-PRO-008 | Corrective Action Procedure |
| JDS-PRO-009 | Competence Management Procedure |
| JDS-MAN-MEC-001 | Documentation Guide — What Records to Keep |
| JDS-LOG-MEC-001 | Equipment Register (Framework Template) |
| JDS-LOG-MEC-002 | Pressure Vessel Inventory Guide |

> **Regulatory traceability:** For a full mapping of how this procedure satisfies specific regulatory requirements, see the [Regulatory Traceability Matrix](../../projects/JDS-PRJ-MEC-001_pressure-vessel-maintenance/02-regulations/SE-sweden/regulatory-traceability-matrix.md).

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — complete ongoing maintenance procedure |
| B | 2026-03-25 | N. Johansson | Language authority update — all terminology now JDS English. Regulatory traceability separated to dedicated matrix document. |
