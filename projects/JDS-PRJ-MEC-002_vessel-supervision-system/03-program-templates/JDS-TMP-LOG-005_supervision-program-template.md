# Supervision Program — [Site Name]

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-[NNN] |
| **Revision** | DRAFT |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT |
| **Author** | [Author name] |
| **Project** | JDS-PRJ-MEC-002 |
| **Client** | [Client name] |
| **Site** | [Site name / address] |
| **Program ID** | SP-[NNN] |

---

## 1. Purpose and Scope

This document is the **supervision program** for all pressurised vessels at [site name]. It defines what checks are performed, how often, by whom, and how results are documented. It satisfies the ongoing supervision requirement of AFS 2017:3 Chapter 2, Section 3.

### 1.1 Equipment in Scope

This program covers all pressurised equipment at the site with PS > 0.5 bar and PS x V > 50 bar-L, including:
- Pressure vessels (Class A and Class B)
- Safety accessories protecting those vessels
- Pressurised piping systems above the classification threshold

### 1.2 Equipment Not in Scope

- Equipment below the classification threshold (PS x V < 50 bar-L)
- Portable fire extinguishers (separate maintenance contract)
- [Add any other exclusions]

---

## 2. Equipment Register Summary

| Vessel ID | Description | PS (bar) | V (L) | PS x V | Class | Medium |
|-----------|-------------|---------|-------|--------|-------|--------|
| PV-001 | | | | | A / B | |
| PV-002 | | | | | A / B | |
| PV-003 | | | | | A / B | |

> Full equipment details are in the site equipment register (JDS-LOG-MEC-[NNN]).

---

## 3. Safety Devices

| Device ID | Type | Protects | Set Pressure (bar) |
|-----------|------|----------|-------------------|
| SV-001 | Safety valve | PV-001 | |
| SV-002 | Safety valve | PV-002 | |

---

## 4. Supervision Schedule

### 4.1 Daily / Per-Shift Checks

| # | Check | Applies To | Method |
|---|-------|-----------|--------|
| 1 | Pressure gauge within normal range | All vessels | Visual reading |
| 2 | Temperature within design limits | All vessels | Visual reading |
| 3 | No audible leaks or unusual noise | All vessels | Listening |
| 4 | Control system: no standing alarms | All vessels | Control panel check |
| 5 | Level indicators correct | Where fitted | Visual reading |

**Performed by:** [Role / name]
**Record method:** Shift log entry

### 4.2 Weekly Checks

| # | Check | Applies To | Method |
|---|-------|-----------|--------|
| 1 | No visible leaks at flanges, valves, fittings | All vessels | Walk-around visual |
| 2 | Safety valves not gagged or blocked | All vessels | Visual check |
| 3 | Drain valves functional (operate drain) | All vessels | Manual operation |
| 4 | Condensate drainage working | Air receivers | Visual / operate trap |

**Performed by:** [Role / name]
**Record method:** Weekly check sheet (filed in supervision rounds)

### 4.3 Monthly Checks

| # | Check | Applies To | Method |
|---|-------|-----------|--------|
| 1 | External surface condition — corrosion, dents, cracks | All vessels | Close visual inspection |
| 2 | Insulation condition — damage, moisture | Insulated vessels | Visual check |
| 3 | Support and foundation integrity | All vessels | Visual check |
| 4 | Safety valve seal intact | All vessels | Visual check |
| 5 | Rupture disc condition (no bulging) | Where fitted | Visual check |
| 6 | Vessel access clear and safe | All vessels | Visual check |

**Performed by:** [Role / name]
**Record method:** Supervision round record (JDS-TMP-LOG-006)

### 4.4 Quarterly Checks

| # | Check | Applies To | Method |
|---|-------|-----------|--------|
| 1 | Nameplate legible and not obscured | All vessels | Visual check |
| 2 | Pressure switch function test | Where fitted | Simulate / trip test |
| 3 | Paint / coating condition | All vessels | Visual check |
| 4 | Review open findings from previous rounds | All | Register review |

**Performed by:** [Role / name]
**Record method:** Supervision round record (JDS-TMP-LOG-006)

### 4.5 Annual Checks

| # | Check | Applies To | Method |
|---|-------|-----------|--------|
| 1 | Safety valve function test (lift test) | All safety valves | On-line or bench test |
| 2 | Full supervision program review | Program | JDS-TMP-LOG-007 |
| 3 | Equipment register accuracy verification | All vessels | Compare register to physical equipment |
| 4 | Competence records current | All supervision personnel | Record review |
| 5 | Formal inspection schedule review | All vessels | Inspection plan review |

**Performed by:** [Program manager / competent person]
**Record method:** Annual review record (JDS-TMP-LOG-007) + safety valve test records

---

## 5. Personnel and Competence

### 5.1 Supervision Roles

| Role | Name | Tasks | Competence Ref |
|------|------|-------|---------------|
| Supervisor (daily/weekly) | [Name] | Daily/weekly checks | PRO-009 record |
| Supervisor (monthly/quarterly) | [Name] | Monthly/quarterly rounds | PRO-009 record |
| Program Manager | [Name] | Annual review, program updates, findings management | PRO-009 record |

### 5.2 Minimum Competence

All personnel performing supervision checks must meet the requirements defined in JDS-MAN-MEC-002, Section 7.

---

## 6. Findings Management

### 6.1 Severity Classification

| Severity | Definition | Action | Timeline |
|----------|-----------|--------|----------|
| **Critical** | Immediate safety risk | Out of service, escalate | Immediate |
| **Major** | Will deteriorate to critical | Plan repair, close monitoring | Within 30 days |
| **Minor** | Noted, no immediate risk | Monitor, plan maintenance | Within 90 days |
| **Observation** | Worth monitoring | Note, observe trend | Next round |

### 6.2 Escalation

- **Critical findings:** Notify operator immediately (phone + written record within 24 hours)
- **Major findings:** Written notification to operator within 48 hours
- **Minor findings and observations:** Included in next supervision round report

### 6.3 Corrective Actions

All findings classified Major or above shall be managed per JDS-PRO-008 (Corrective Action Procedure).

---

## 7. Documentation

### 7.1 Records Produced

| Record | Frequency | Template | Filed In |
|--------|-----------|----------|----------|
| Shift log entries | Daily/shift | Operator's log | Operator's records |
| Weekly check sheets | Weekly | [Site form] | `rounds/` |
| Supervision round records | Monthly/quarterly | JDS-TMP-LOG-006 | `rounds/` |
| Annual review | Annually | JDS-TMP-LOG-007 | `reviews/` |
| Safety valve test records | Annually | Test certificate | `rounds/` |
| Finding records | As needed | JDS-PRO-008 | `findings/` |

### 7.2 Retention

All records retained for the life of the equipment plus 5 years, per AFS 2017:3 Chapter 2, Section 5.

---

## 8. Program Review

This program shall be reviewed at least **annually** or sooner if:
- Equipment is added, removed, or modified
- Operating conditions change significantly
- Regulatory requirements change
- A significant finding or incident occurs

---

## 9. Approval

| | |
|---|---|
| **Prepared by** | [Name, role] |
| **Reviewed by** | [Name, role] |
| **Approved by** | [Operator representative, role] |
| **Approval date** | YYYY-MM-DD |
| **Next review due** | YYYY-MM-DD |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| DRAFT | YYYY-MM-DD | [Author] | Initial draft |
