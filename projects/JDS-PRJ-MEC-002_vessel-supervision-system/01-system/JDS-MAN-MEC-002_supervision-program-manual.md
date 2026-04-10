# Supervision Program Manual — Pressurised Vessels

| | |
|---|---|
| **Document No.** | JDS-MAN-MEC-002 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## 1. Purpose

This manual defines **how to create, implement, and maintain an ongoing supervision program** for pressurised vessels. It is the complete methodology reference for the Vessel Supervision System (JDS-PRJ-MEC-002).

A supervision program is the documented system that ensures every pressurised vessel under your responsibility is regularly monitored between formal inspections. Swedish regulation AFS 2017:3 (Chapter 2, Section 3) requires every operator to have such a program. This manual tells you how to build one.

> **In plain language:** This manual teaches you to build a supervision program from scratch, run it day-to-day, and improve it year after year.

---

## 2. Scope

This manual covers:
- Pressure vessels (tanks, receivers, heat exchangers, autoclaves)
- Safety accessories (safety valves, rupture discs, pressure switches)
- Pressurised piping systems where included in the regulatory scope

It does **not** cover:
- Formal recurring inspections by accredited bodies (see JDS-PRO-004)
- Equipment design, manufacture, or commissioning (see PED 2014/68/EU)
- Equipment repair or modification procedures

---

## 3. Definitions

| Term | Meaning |
|------|---------|
| **Supervision program** | A documented system defining what checks are performed, how often, by whom, and how results are recorded |
| **Supervision round** | A single execution of scheduled checks — a walk-around, instrument reading, or functional test |
| **Ongoing supervision** | The continuous responsibility of the operator to ensure safe operation between formal inspections |
| **Formal inspection** | Periodic inspection by an accredited body (Class A) or competent person (Class B) — external, internal, or pressure test |
| **Operator** | The person or organisation responsible for the equipment in service |
| **Competent person** | A person with documented training and experience to perform the assigned supervision tasks |

---

## 4. Regulatory Foundation

### 4.1 Base Regulation

**AFS 2017:3** — Use and Inspection of Pressurised Equipment — is the primary Swedish regulation. Chapter 2 establishes that the operator must ensure ongoing supervision is performed and documented.

### 4.2 Amendments (Consolidated)

| Amendment | Key Changes |
|-----------|------------|
| **AFS 2019:1** | Clarified supervision scope for piping systems, refined competence provisions |
| **AFS 2020:10** | Extended inspection deadlines during extraordinary circumstances, accepted digital documentation and remote verification |
| **AFS 2022:2** | Updated classification thresholds, revised competence requirements for supervision personnel |

### 4.3 Key Regulatory Requirements

The regulation requires the operator to:

1. **Have a supervision program** — documented, site-specific, covering all equipment in scope
2. **Define check intervals** — based on equipment type, operating conditions, and risk
3. **Assign competent personnel** — with documented qualifications
4. **Document every round** — records must be retained for the life of the equipment
5. **Act on findings** — deviations must trigger corrective action
6. **Review the program** — at least annually, update as needed

> For the full regulatory summary and paragraph references, see JDS-RPT-MEC-003.

---

## 5. Building a Supervision Program

### 5.1 Overview

Building a supervision program follows five steps:

```
SURVEY → ASSESS → DESIGN → DOCUMENT → APPROVE
  │         │        │          │          │
Identify   Risk    Check     TMP-LOG-005  Operator
equipment  level   types     (program     sign-off
           per     and       document)
           vessel  intervals
```

### 5.2 Step 1 — Survey the Site

Walk the entire site and identify every pressurised vessel. For each vessel, record:

| Data Point | Source |
|-----------|--------|
| Vessel ID (tag number) | Nameplate or P&ID |
| Description | Visual identification |
| Location | Physical location on site |
| Design pressure (PS) | Nameplate |
| Volume (V) | Nameplate or data sheet |
| Medium | Operational knowledge |
| Operating conditions | Normal pressure, temperature, cycles |
| Safety devices | What protects this vessel |
| Accessibility | Can it be inspected? Any obstructions? |

> If an equipment register already exists (from JDS-PRJ-MEC-001), use it as the starting point. Do not duplicate work.

### 5.3 Step 2 — Assess Risk Level

For each vessel, determine the supervision intensity:

| Factor | Higher Intensity | Lower Intensity |
|--------|-----------------|----------------|
| Risk class | Class A | Class B / Simple PV |
| Medium | Group 1 (dangerous) | Group 2 (non-dangerous) |
| Operating conditions | Cyclic, high temperature, corrosive | Steady-state, ambient, clean |
| Age | Old, approaching design life | New, within design life |
| History | Previous findings, repairs | Clean record |
| Consequence of failure | Personnel exposure, environmental | Contained, no exposure |

The risk assessment drives how often and how thoroughly each vessel is supervised.

### 5.4 Step 3 — Design Check Types and Intervals

Define what checks to perform and how often. The table below provides baseline intervals — adjust based on risk assessment:

#### Visual and External Checks

| Check | Baseline Interval | What to Look For |
|-------|-------------------|-----------------|
| External surface condition | Monthly | Corrosion, dents, cracks, paint blistering |
| Insulation condition | Monthly | Damage, moisture ingress, CUI indicators |
| Support and foundation | Monthly | Settlement, cracking, corrosion of supports |
| Nameplate legibility | Quarterly | Readable, not obscured |
| Pressure gauge reading | Daily/shift | Within normal operating range |
| Temperature reading | Daily/shift | Within design limits |
| Leak detection | Weekly | Flanges, valves, fittings, weld joints |

#### Safety Device Checks

| Check | Baseline Interval | What to Look For |
|-------|-------------------|-----------------|
| Safety valve not gagged or blocked | Weekly | No physical obstruction, no unauthorised isolation |
| Safety valve seal intact | Monthly | Lead seal or tag present and undisturbed |
| Safety valve function test | Annually | Lifts at set pressure, reseats cleanly |
| Rupture disc condition | Monthly | No bulging, corrosion, or damage visible |
| Pressure switch function | Quarterly | Trips at correct pressure, signal reaches control system |

#### Operational Checks

| Check | Baseline Interval | What to Look For |
|-------|-------------------|-----------------|
| Drain operation | Weekly | Condensate drainage, no blockage |
| Level indicators | Daily/shift | Correct reading, no stuck indication |
| Vibration / unusual noise | Daily/shift | Change from baseline |
| Control system alarms | Daily/shift | No standing alarms, correct setpoints |

### 5.5 Step 4 — Document the Program

Use **JDS-TMP-LOG-005** (Supervision Program Template) to create the program document. The template contains all required sections:

1. **Scope** — which equipment is covered
2. **Equipment list** — with risk classification and check assignments
3. **Check schedule** — daily, weekly, monthly, quarterly, annual tasks
4. **Personnel** — who performs what, competence requirements
5. **Documentation** — how rounds are recorded
6. **Findings management** — how deviations are handled
7. **Review schedule** — when the program is reviewed and by whom

### 5.6 Step 5 — Approve and Issue

The completed supervision program must be:

1. **Reviewed** by a competent person (technical review)
2. **Approved** by the operator (management approval)
3. **Communicated** to all personnel who perform supervision
4. **Filed** in the active programs folder (04-active-programs)
5. **Registered** in JDS-LOG-MEC-005 (Program Register)

---

## 6. Performing Supervision Rounds

### 6.1 Before the Round

1. Review the supervision program for today's scheduled checks
2. Gather equipment: torch, notebook/tablet, PPE, camera
3. Check for any recent findings that need follow-up
4. Prepare a blank round record (JDS-TMP-LOG-006)

### 6.2 During the Round

1. Follow the check sequence defined in the program
2. For each vessel, work through the assigned checks
3. Record the result of every check: OK, Not OK, or N/A
4. Photograph any findings
5. If a finding is critical (immediate safety concern), stop and escalate

### 6.3 After the Round

1. Complete the round record — all fields, sign, and date
2. If findings exist:
   - **Critical** — vessel out of service, notify operator immediately, raise corrective action
   - **Non-critical** — log the finding, set a follow-up date, raise corrective action per JDS-PRO-008
   - **Observation** — note for monitoring, no immediate action required
3. File the completed record in the client's supervision folder
4. Update the program register (next round date)

### 6.4 Finding Severity Classification

| Severity | Definition | Action | Timeline |
|----------|-----------|--------|----------|
| **Critical** | Immediate risk to personnel or equipment integrity | Take out of service, escalate to operator | Immediate |
| **Major** | Condition will deteriorate to critical if not addressed | Plan repair/remediation, monitor closely | Within 30 days |
| **Minor** | Condition noted, no immediate risk | Monitor at next round, plan maintenance | Within 90 days |
| **Observation** | Not a deficiency, but worth monitoring | Note in record, observe trend | Next round |

---

## 7. Personnel Competence

### 7.1 Minimum Requirements

Personnel performing supervision rounds must have:

| Requirement | Evidence |
|------------|---------|
| Understanding of pressurised vessel hazards | Training record |
| Knowledge of the specific equipment supervised | Site familiarisation record |
| Ability to read and interpret nameplates, gauges, and instruments | Practical assessment |
| Understanding of the supervision program and check procedures | Program briefing record |
| Knowledge of emergency procedures | Emergency drill participation |

### 7.2 Competence Records

Competence is managed per **JDS-PRO-009** (Competence Management Procedure). Each person performing supervision must have a current competence record on file.

---

## 8. Documentation Requirements

### 8.1 What Must Be Documented

| Document | Template | Retention |
|----------|----------|-----------|
| Supervision program (the plan) | JDS-TMP-LOG-005 | Life of equipment + 5 years |
| Supervision round records | JDS-TMP-LOG-006 | Life of equipment + 5 years |
| Annual program reviews | JDS-TMP-LOG-007 | Life of equipment + 5 years |
| Corrective action records | JDS-PRO-008 | Life of equipment + 5 years |
| Competence records | JDS-PRO-009 | Duration of employment + 5 years |
| Program register | JDS-LOG-MEC-005 | Maintained continuously |

### 8.2 Filing Structure

Each active program in `04-active-programs/` should follow this structure:

```
04-active-programs/
└── [client-name]/
    ├── JDS-LOG-MEC-NNN_supervision-program.md   ← The program document
    ├── rounds/                                   ← Completed round records
    │   ├── YYYY-MM-DD_round-record.md
    │   └── ...
    ├── reviews/                                  ← Annual reviews
    │   ├── YYYY_annual-review.md
    │   └── ...
    └── findings/                                 ← Open and closed findings
        ├── F-001_description.md
        └── ...
```

---

## 9. Annual Program Review

### 9.1 Purpose

The supervision program must be reviewed at least annually to ensure it remains effective and compliant. Use **JDS-TMP-LOG-007** (Annual Review Template).

### 9.2 Review Checklist

| Review Item | What to Check |
|------------|--------------|
| Equipment changes | Any vessels added, removed, or modified? |
| Operating condition changes | Any changes in pressure, temperature, medium, or duty cycle? |
| Regulatory changes | Any new amendments or guidance from the authority? |
| Finding trends | Are the same issues recurring? Does the program catch them? |
| Personnel changes | Are all supervision personnel still competent and current? |
| Round completion rate | Were all scheduled rounds performed? |
| Corrective action closure | Are all findings from the year closed? |
| Interval adequacy | Are the check intervals appropriate, or should they be adjusted? |

### 9.3 Review Output

The annual review produces:
1. An updated supervision program (new revision) if changes are needed
2. A completed review record (filed in the client's reviews folder)
3. Updated program register entry

---

## 10. Integration with JDS-PRJ-MEC-001

This supervision system is designed to work alongside the Pressure Vessel Maintenance Program:

| Activity | System |
|----------|--------|
| Equipment inventory and classification | JDS-PRJ-MEC-001 |
| Formal inspection planning and scheduling | JDS-PRJ-MEC-001 |
| **Ongoing supervision between inspections** | **JDS-PRJ-MEC-002 (this project)** |
| Inspection report management | JDS-PRJ-MEC-001 |
| Corrective actions | JDS-PRO-008 (shared) |
| Competence management | JDS-PRO-009 (shared) |

---

## 11. References

| Document | Purpose |
|----------|---------|
| JDS-RPT-MEC-003 | AFS 2017:3 Consolidated Summary |
| JDS-PRO-008 | Corrective Action Procedure |
| JDS-PRO-009 | Competence Management Procedure |
| JDS-PRO-010 | Ongoing Maintenance Program Procedure |
| JDS-PRJ-MEC-001 | Pressure Vessel Maintenance Program |
| JDS-TMP-LOG-005 | Supervision Program Template |
| JDS-TMP-LOG-006 | Supervision Round Record Template |
| JDS-TMP-LOG-007 | Annual Review Template |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial release — complete supervision program methodology |
