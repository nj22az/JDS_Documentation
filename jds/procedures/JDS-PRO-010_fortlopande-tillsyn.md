# Fortlöpande Tillsyn (FLT) — Ongoing Maintenance Program Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-010 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how to set up, run, and maintain a **Fortlöpande Tillsyn** (FLT) — ongoing maintenance and supervision program — for pressurised vessels under Swedish regulation **AFS 2017:3**.

It turns the JDS system into an operational tool: every step of the FLT cycle produces a JDS document, every inspection is tracked, and every finding is closed.

> **In plain language:** This is the master procedure for running a pressure vessel maintenance program. Follow it from top to bottom for a new client. Follow the annual cycle for ongoing work.

---

## 2. Scope

This procedure applies to:
- Pressure vessels (tryckkärl) classified under AFS 2017:3
- Safety devices (säkerhetsanordningar) protecting those vessels
- Piping (rörledningar) under AFS 2017:3 where applicable

It covers the full FLT lifecycle:

```
SET UP → INVENTORY → CLASSIFY → PLAN → INSPECT → REPORT → UPDATE → REPEAT
```

---

## 3. Regulatory Basis

| Regulation | What It Covers |
|---|---|
| **AFS 2017:3** | Use and inspection of pressurised equipment |
| **AFS 2016:2** | Pressure equipment (PED implementation) |
| **PED 2014/68/EU** | Pressure Equipment Directive |

---

## 4. Roles and Responsibilities

| Role | Responsibility |
|---|---|
| **Brukare (Operator)** | Ensure FLT is in place, fund inspections, act on findings |
| **FLT-ansvarig (FLT Manager)** | Run the program — this role uses JDS |
| **Ackrediterat kontrollorgan** | Perform Klass A inspections (DEKRA, Kiwa, DNV, etc.) |
| **Kompetent person** | Perform Klass B own inspections (documented competence per PRO-009) |

---

## 5. Setting Up a New FLT Program

### Step 1 — Create the Client Folder

Create a new client folder under `03-active-programs/`:

```
03-active-programs/
└── [client-name]/
    ├── JDS-LOG-MEC-NNN_inventory.md       ← Equipment register (from TMP-LOG-002)
    ├── JDS-LOG-MEC-NNN_kontrollplan.md    ← Annual inspection plan (from TMP-LOG-004)
    ├── inspections/                        ← Inspection reports (JDS-RPT-MEC-NNN)
    ├── tillsyn/                            ← Supervision checklists (JDS-LOG-MEC-NNN)
    ├── certificates/                       ← Scanned certificates from inspectors
    └── vessel-files/                       ← One subfolder per vessel
        ├── PV-001/                         ← Manufacturer docs, drawings, history
        ├── PV-002/
        └── ...
```

### Step 2 — Build the Equipment Register

1. Use template **JDS-TMP-LOG-002** (FLT Inventory Template)
2. Walk the site and record every pressure vessel
3. Photograph every nameplate
4. Fill in all mandatory fields (marked M)
5. Register the document in `jds/registry/document-register.md`

### Step 3 — Classify Every Vessel

For each vessel, determine:

| Decision | How | Reference |
|---|---|---|
| Is it in scope of AFS 2017:3? | PS > 0.5 bar AND PS×V > 50 bar·L | AFS 2017:3 §4 |
| What is the fluid group? | Group 1 (dangerous) or Group 2 (other) | PED Art. 13 |
| What is the AFS Klass? | A (higher risk) or B (lower risk) | AFS 2017:3 Bilaga 2 |
| What PED category? | I, II, III, IV, or Art. 4.3 | PED Annex II |

Record the classification in the equipment register.

### Step 4 — Build the Kontrollplan (Inspection Plan)

1. Use template **JDS-TMP-LOG-004** (Kontrollplan Template)
2. For each vessel, enter the inspection intervals from AFS 2017:3:

| AFS Klass | Utvändig | Invändig | Tryckprov |
|---|---|---|---|
| Klass A | 2 years | 6 years | 12 years |
| Klass B | 2 years | 6 years | — |

3. Calculate next due dates from the last inspection (or commissioning date for new vessels)
4. Book accredited inspectors for Klass A items **at least 3 months ahead**

### Step 5 — Establish Tillsyn Routines

1. Use template **JDS-TMP-LOG-003** (Tillsynsprotokoll Template)
2. Define a monthly or quarterly walk-around checklist
3. Assign responsible person for each walk-around
4. File completed checklists in the `tillsyn/` folder

---

## 6. Annual FLT Cycle

Once set up, the program runs on an annual cycle:

### Q1 (January–March) — Planning

| Task | Document | Template |
|---|---|---|
| Review kontrollplan for the year | JDS-LOG-MEC-NNN | TMP-LOG-004 |
| Book inspectors for planned inspections | — | — |
| Review overdue items from previous year | Kontrollplan | — |
| Update equipment register if vessels added/removed | JDS-LOG-MEC-NNN | TMP-LOG-002 |

### Q2–Q3 (April–September) — Execution

| Task | Document | Template |
|---|---|---|
| Perform scheduled inspections | JDS-RPT-MEC-NNN | TMP-RPT-003 |
| Perform routine tillsyn (supervision) | JDS-LOG-MEC-NNN | TMP-LOG-003 |
| Test safety devices per schedule | Safety device register | — |
| Document findings and corrective actions | JDS-RPT-MEC-NNN | — |

### Q4 (October–December) — Review & Close Out

| Task | Document | Template |
|---|---|---|
| Verify all planned inspections were completed | Kontrollplan | — |
| Close out all findings and corrective actions | CA log | PRO-008 |
| Update equipment register with latest results | JDS-LOG-MEC-NNN | — |
| Prepare kontrollplan for next year | JDS-LOG-MEC-NNN | TMP-LOG-004 |
| Archive completed inspection reports | `inspections/` | — |

---

## 7. Performing an Inspection

### Before the Inspection

1. Prepare the vessel: isolate, depressurise, drain/clean if internal
2. Gather previous inspection reports for the inspector
3. Prepare access (scaffolding, lighting, ventilation for confined spaces)
4. Complete a pre-inspection risk assessment

### During the Inspection

1. The accredited inspector (Klass A) or competent person (Klass B) performs the inspection
2. Document all findings in real-time
3. Photograph significant findings

### After the Inspection

1. Receive the inspection certificate (kontrollintyg) from the inspector
2. Create an inspection report: **JDS-RPT-MEC-NNN** (use TMP-RPT-003)
3. Update the equipment register:
   - Last Inspection → today's date
   - Next Due → calculated from interval
   - Result → GODKÄND / GODKÄND MED ANMÄRKNING / UNDERKÄND
   - Certificate Ref → new certificate number
4. File the certificate in `certificates/`
5. If findings require action: create corrective actions per JDS-PRO-008
6. Log the update in the project CHANGELOG

---

## 8. Handling Findings

| Result | Swedish | Action |
|---|---|---|
| **Approved** | Godkänd | Update register, file certificate, no further action |
| **Approved with remarks** | Godkänd med anmärkning | Update register, create monitoring actions, set follow-up date |
| **Rejected** | Underkänd | Take vessel OUT OF SERVICE immediately, create corrective action, do not return to service until re-inspected and approved |

All findings follow JDS-PRO-008 (Corrective Action Procedure).

---

## 9. Document Map — What JDS Produces for FLT

| FLT Activity | JDS Document Type | Template |
|---|---|---|
| Equipment inventory | LOG (register) | JDS-TMP-LOG-002 |
| Annual inspection plan | LOG (plan) | JDS-TMP-LOG-004 |
| Routine supervision | LOG (checklist) | JDS-TMP-LOG-003 |
| Inspection report | RPT (report) | JDS-TMP-RPT-003 |
| Risk assessment | RPT (assessment) | JDS-TMP-RPT-001 |
| Corrective action | CA log entry | JDS-PRO-008 |
| Competence records | Training log | JDS-PRO-009 |

---

## 10. JDS Tools for FLT

| Task | Command |
|---|---|
| Validate all FLT documents | `python3 scripts/jds-validate.py` |
| Generate inspection report PDF | `python3 scripts/md2pdf.py <report.md>` |
| Generate letter to inspector/client | `python3 scripts/md2letter.py <letter.md>` |
| Check all links and registrations | `python3 scripts/jds-validate.py --fix` |

---

## 11. References

| Document | Purpose |
|---|---|
| JDS-PRO-004 | Inspection Planning Procedure |
| JDS-PRO-008 | Corrective Action Procedure |
| JDS-PRO-009 | Competence Management Procedure |
| JDS-MAN-MEC-001 | Documentation Guide — What Records to Keep |
| JDS-LOG-MEC-001 | Equipment Register (Framework Template) |
| JDS-LOG-MEC-002 | AFS 2017:3 Inventory Guide |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — complete FLT procedure for AFS 2017:3 ongoing maintenance programs |
