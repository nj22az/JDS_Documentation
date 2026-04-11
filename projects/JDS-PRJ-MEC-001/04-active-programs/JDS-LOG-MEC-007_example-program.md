# Supervision Program — Gothenburg Workshop

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-007 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |
| **Project** | JDS-PRJ-MEC-002 |
| **Client** | Example Workshop AB |
| **Site** | Gothenburg Workshop |
| **Program ID** | SP-[NNN] |
| **Source** | JDS-LOG-MEC-006_example-inventory.md |

---

## 1. Document Chain

```
INVENTORY  →  [PROGRAM]  →  ROUND  →  REVIEW
(Step 1)       (you are      (next)
                here)
```

**Source document:** JDS-LOG-MEC-006_example-inventory.md

---

## 2. Regulatory Basis

This program satisfies the requirements of **AFS 2017:3** (consolidated with AFS 2019:1, AFS 2020:10, AFS 2022:2):

| Requirement | AFS 2017:3 | Status |
|------------|-----------|--------|
| Documented supervision routines | 4 Kap. §17 | This document |
| Mandatory minimum checks (6 points) | 2 Kap. §6 | Section 5 |
| Annual evaluation and revision | 4 Kap. §17 | Section 12 |
| Assigned responsible person | 4 Kap. §17 | Section 9 |
| Coordination person | 4 Kap. §14 | Section 9 |
| Equipment register | 4 Kap. §15 | Section 3 |
| Monitoring requirements | 4 Kap. §16 | Section 4 |
| Recurring inspection schedule | 5 Kap., Bilaga 1 | Section 6 |
| Deviation reports | 4 Kap. §19 | Section 10 |
| Lifetime journal | 4 Kap. §18 | Section 11 |

> **Warning:** Non-compliance sanction: **10,000–100,000 SEK** for operating Class A/B equipment without documented supervision routines (4 Kap. §17).

---

## 3. Equipment Register (4 Kap. §15)

Register of all pressurised equipment at Gothenburg Workshop:

| Vessel ID | Description | Location | Class | Medium | Inspector |
|-----------|-------------|----------|-------|--------|-----------|
| PV-001 | Main air receiver | Compressor room | **A** | compressed air | Accredited body (Type A) |
| PV-002 | Workshop air receiver | Workshop B | **Exempt (air/N2)** | compressed air | N/A |
| PV-003 | Steam boiler | Boiler house | **A** | steam | Accredited body (Type A) |
| PV-004 | Refrigeration receiver | Engine room | **A** | ammonia | Accredited body (Type A) |
| PV-005 | Hydraulic accumulator | Workshop A | **B** | hydraulic oil | Accredited body (Type A or B) |
| PV-006 | Expansion vessel | Heating system | **Below threshold** | water | N/A |
| PV-007 | Sandblast receiver | Yard | **Exempt (air/N2)** | compressed air | N/A |

**Class A:** 3 vessels (accredited inspection body required)
**Class B:** 1 vessels
**Exempt (air/N2/refrigerant):** 2 vessels (Class B exempt per 4 Kap. §10)
**Below threshold:** 1 vessels

---

## 4. Monitoring Requirements (4 Kap. §16)

Class A and B vessels must be **continuously monitored** (§16). The operator must be able to immediately reach the vessel and determine if it is safe to remain pressurised.

If periodic monitoring is used instead (per documented risk assessment), the following must be documented:

1. How operators are alerted to safety-related alarms
2. The response time (inställelsetid) for safety-related alarms

| Vessel ID | Monitoring Type | Alarm System | Response Time |
|-----------|----------------|-------------|--------------|
| PV-001 | Continuous / Periodic | [Describe] | [Minutes] |
| PV-003 | Continuous / Periodic | [Describe] | [Minutes] |
| PV-004 | Continuous / Periodic | [Describe] | [Minutes] |
| PV-005 | Continuous / Periodic | [Describe] | [Minutes] |

---

## 5. Mandatory Supervision Checks (2 Kap. §6)

AFS 2017:3 §6 defines **six mandatory minimum checks**. Every supervision round must verify all six points:

| # | §6 Requirement | Check | Method |
|---|--------------|-------|--------|
| 1 | Equipment functions satisfactorily | Pressure/temperature within range, no abnormal noise/vibration | Gauge reading, listening |
| 2 | No leaks have occurred | Check flanges, valves, fittings, weld joints | Visual walk-around |
| 3 | No harmful external or internal impact | Surface condition, insulation, supports, corrosion | Close visual inspection |
| 4 | No other faults or deviations | Safety devices, drainage, general condition | Functional check |
| 5 | Equipment correctly marked | Nameplates, valve tags, emergency stops legible | Visual check |
| 6 | Prescribed inspections carried out | Inspection certificate current, not overdue | Register review |

> **Important:** These six points are the **legal minimum** per 2 Kap. §6 and must be traceable in every supervision record.

---

## 6. Recurring Inspection Schedule (Bilaga 1)

### 6.1 Driftprov (Operational Test)

Base intervals per Bilaga 1, §1.4.1. Actual interval determined by accredited inspection body at each inspection.

| Vessel ID | Class | Medium | Base Interval | Max |
|-----------|-------|--------|-------------|-----|
| PV-001 | A | compressed air | 4 years | 4 years |
| PV-003 | A | steam | 2 years | 4 years |
| PV-004 | A | ammonia | 2 years | 4 years |
| PV-005 | B | hydraulic oil | 2 years | 4 years |

**Extended interval (§1.4.2):** Possible if safety equipment functioned at the two previous tests. Max 4 years.

**Shortened interval (§1.4.3):** If safety equipment did NOT function, next interval is **halved**.

### 6.2 Internal/External Examination (Class A only)

Condition-based interval determined by inspection body per Bilaga 1, §2.2:

| Interval | Conditions |
|----------|-----------|
| 4 years | Base: not fire-affected, >5yr life, low crack risk, mild environment |
| 2 years | 4-year not met, but stable condition |
| 1 year | 2-year not met, but safe for 1 year |
| 6 months | 1-year not met, but safe for 6 months |
| 6 years | After clean 4-year, no fatigue/creep |
| 8 years | After 2 clean 4/6-year inspections |
| 10 years | After 2 progressively longer, clean |
| 12 years | Cisterns only, after clean 6-year |

| Vessel ID | Current Interval | Next Due |
|-----------|-----------------|----------|
| PV-001 | [Per inspection body] | [Expiry month] |
| PV-003 | [Per inspection body] | [Expiry month] |
| PV-004 | [Per inspection body] | [Expiry month] |

---

## 7. Supervision Round Schedule

### 7.1 Daily / Per-Shift Checks

**Applies to:** PV-001, PV-003, PV-004, PV-005

| # | Check (§6 ref) | Method |
|---|---------------|--------|
| 1 | Pressure gauge within normal range | Visual reading |
| 2 | Temperature within design limits | Visual reading |
| 3 | No audible leaks or unusual noise | Listening |
| 4 | Control system: no standing alarms | Control panel check |

**Performed by:** [Name / role]
**Record:** Shift log

### 7.2 Weekly Checks

**Applies to:** PV-001, PV-003, PV-004, PV-005

| # | Check (§6 ref) | Method |
|---|---------------|--------|
| 1 | No visible leaks at flanges, valves, fittings | Walk-around visual |
| 2 | Safety valves not gagged or blocked | Visual check |
| 3 | Drain valves functional (operate drain) | Manual operation |
| 4 | Condensate drainage working | Visual / operate trap |

**Performed by:** [Name / role]
**Record:** Weekly check sheet

### 7.3 Monthly Checks (Formal Supervision Round)

**Applies to:** PV-001, PV-003, PV-004, PV-005, PV-002, PV-007

| # | Check (§6 ref) | Method |
|---|---------------|--------|
| 1 | External surface: no corrosion, dents, cracks | Close visual |
| 2 | Insulation intact, no moisture indicators | Visual check |
| 3 | Support and foundation integrity | Visual check |
| 4 | Safety valve seal intact | Visual check |
| 5 | Vessel access clear and safe | Visual check |

**Performed by:** [Name / role]
**Record:** Supervision round record (JDS-TMP-LOG-006)

### 7.4 Quarterly Checks

**Applies to:** PV-001, PV-003, PV-004, PV-005

| # | Check (§6 ref) | Method |
|---|---------------|--------|
| 1 | Nameplate legible and not obscured | Visual check |
| 2 | Pressure switch function test | Simulate / trip test |
| 3 | Paint / coating condition | Visual check |
| 4 | Review open findings from previous rounds | Register review |

**Performed by:** [Name / role]
**Record:** Supervision round record (JDS-TMP-LOG-006)

### 7.5 Annual Checks

**Applies to:** all vessels

| # | Check | Method |
|---|-------|--------|
| 1 | Safety valve function test (lift test) | On-line or bench test |
| 2 | Equipment register accuracy verification | Compare to physical |
| 3 | Competence records current | Record review |
| 4 | Formal inspection schedule review | Inspection plan review |

**Performed by:** Program manager / competent person
**Record:** Annual review record (JDS-TMP-LOG-007)

---

## 8. Per-Vessel Check Assignment

| Vessel ID | Class | Daily | Weekly | Monthly | Quarterly | Annual |
|-----------|-------|-------|--------|---------|-----------|--------|
| PV-001 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-002 | **Exempt (air/N2)** | — | — | Yes | — | Yes |
| PV-003 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-004 | **A** | Yes | Yes | Yes | Yes | Yes |
| PV-005 | **B** | Yes | Yes | Yes | Yes | Yes |
| PV-006 | **Below threshold** | — | — | Yes | — | Yes |
| PV-007 | **Exempt (air/N2)** | — | — | Yes | — | Yes |

---

## 9. Personnel and Responsibilities (4 Kap. §14, §17)

### 9.1 Assigned Roles

| Role | AFS Ref | Name | Responsibility |
|------|---------|------|---------------|
| **Coordination person** | 4 Kap. §14 | [Name] | Plans and coordinates all work on Class A/B equipment |
| **Supervision responsible** | 4 Kap. §17 | [Name] | Ensures supervision is carried out and documented |
| Daily/weekly supervisor | 2 Kap. §6 | [Name] | Performs daily and weekly checks |
| Monthly supervisor | 2 Kap. §6 | [Name] | Performs monthly formal rounds |
| Program manager | 4 Kap. §17 | [Name] | Annual evaluation, revision, findings management |

### 9.2 Competence Requirements

All personnel must have documented competence per JDS-PRO-009. Competence records must be maintained and refreshed.

---

## 10. Deviation Reports (4 Kap. §19)

When Class A/B equipment is found to be damaged or deteriorated, a **deviation report** must be created containing:

| # | Required Content | Description |
|---|-----------------|-------------|
| 1 | Damage/deterioration | What was found |
| 2 | How discovered | Which observation or check |
| 3 | Date of discovery | When it was found |
| 4 | Action needed | What must be done |
| 5 | Cause | Root cause (if not obvious) |
| 6 | Date of action | When the repair/fix was completed |
| 7 | Reporter | Who made the report |

Deviation reports are managed per **JDS-PRO-008** (Corrective Action Procedure) and filed in the client's `findings/` folder.

### Severity Classification

| Severity | Definition | Action | Timeline |
|----------|-----------|--------|----------|
| **Critical** | Immediate safety risk | Out of service, escalate | Immediate |
| **Major** | Will deteriorate to critical | Plan repair, close monitoring | 30 days |
| **Minor** | Noted, no immediate risk | Monitor, plan maintenance | 90 days |
| **Observation** | Worth monitoring | Note, observe trend | Next round |

---

## 11. Lifetime Journal (4 Kap. §18)

Class A/B equipment with limited lifetime must have a **journal showing remaining lifetime**. If parts have different lifetimes, each part must be tracked separately.

| Vessel ID | Limited Lifetime | Journal Ref | Notes |
|-----------|-----------------|-------------|-------|
| PV-001 | Yes / No / Unknown | [Ref] | |
| PV-003 | Yes / No / Unknown | [Ref] | |
| PV-004 | Yes / No / Unknown | [Ref] | |
| PV-005 | Yes / No / Unknown | [Ref] | |

> **Warning:** Equipment that has reached its documented lifetime **may not remain pressurised** unless an analysis demonstrating extended lifetime has been conducted and documented by an accredited body.

---

## 12. Program Review (4 Kap. §17)

This program must be **evaluated and revised at least once per year** (4 Kap. §17). Additional review triggers:

- Equipment added, removed, or modified
- Operating conditions changed significantly
- Regulatory requirements changed
- Significant finding or incident occurred
- Revision inspection (revisionskontroll) performed

**Next review due:** 2027-01-31

---

## 13. Approval

| | |
|---|---|
| **Prepared by** | [Name, role] |
| **Reviewed by** | [Name, role] |
| **Approved by** | [Operator/employer, role] |
| **Approval date** | 2026-04-10 |
| **Next review due** | 2027-01-31 |

---

## 14. Next Step

```
INVENTORY  →  [PROGRAM]  →  ROUND  →  REVIEW
                (done)      (next)
```

To generate a supervision round record:

```
python3 scripts/jds-classify.py --round --from [this-file.md] --output [round-YYYY-MM-DD.md]
```

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial program — 7 vessels, compliant with AFS 2017:3 (verified against official PDF). Auto-generated from JDS-LOG-MEC-006_example-inventory.md |
