# Risk Assessment — Pressure Vessel Maintenance Programme

| | |
|---|---|
| **Document No.** | JDS-RPT-MEC-002 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | EXAMPLE |
| **Author** | Nils Johansson |
| **Project** | JDS-PRJ-MEC-001 |

---

## 1. Summary

This risk assessment identifies and evaluates hazards associated with the ongoing maintenance and inspection of pressure vessels at the Göteborg Workshop. It covers normal operations, inspection activities, and foreseeable failure modes. Controls are proposed following the hierarchy of elimination, substitution, engineering controls, administrative controls, and PPE.

## 2. Scope

- All pressure vessels registered in JDS-LOG-MEC-003
- Inspection and maintenance activities per AFS 2017:3
- Contractor and in-house maintenance personnel
- Normal operation, shutdown, start-up, and emergency scenarios

## 3. Methodology

Risk is assessed using a 5×5 matrix per ISO 31000 and SS-EN 16991:

**Likelihood (L):**

| Score | Description | Frequency |
|-------|-------------|-----------|
| 1 | Rare | Less than once per 20 years |
| 2 | Unlikely | Once per 10–20 years |
| 3 | Possible | Once per 5–10 years |
| 4 | Likely | Once per 1–5 years |
| 5 | Almost certain | More than once per year |

**Consequence (C):**

| Score | Description | Impact |
|-------|-------------|--------|
| 1 | Negligible | No injury, minor repair |
| 2 | Minor | First aid, localised damage |
| 3 | Moderate | Medical treatment, partial shutdown |
| 4 | Major | Serious injury, extended shutdown |
| 5 | Catastrophic | Fatality, facility loss |

**Risk Rating = L × C**

| Rating | Category | Action Required |
|--------|----------|----------------|
| 1–4 | Low | Monitor, no immediate action |
| 5–9 | Medium | Controls required within 3 months |
| 10–15 | High | Controls required within 1 month |
| 16–25 | Critical | Stop work, immediate action |

## 4. Risk Register

### 4.1 Hazard Identification — Operational

| ID | Hazard | Cause | Consequence |
|----|--------|-------|-------------|
| R-001 | Overpressure event | Relief valve failure, blocked outlet | Vessel rupture, projectiles, blast |
| R-002 | Corrosion-induced wall thinning | Internal corrosion, condensate accumulation | Leak or burst at weakened point |
| R-003 | Steam boiler dry firing | Low water level, level gauge failure | Boiler tube failure, steam release |
| R-004 | Hydraulic accumulator bladder failure | Fatigue, over-cycling | Sudden pressure loss, press malfunction |
| R-005 | Nitrogen cylinder bank leak | Fitting failure, impact damage | Oxygen displacement in confined gas store |

### 4.1b Risk Evaluation & Controls — Operational

| ID | L | C | Risk | Controls | Residual |
|----|---|---|------|----------|----------|
| R-001 | 2 | 5 | 10 HIGH | Relief valve testing per schedule, pressure switch backup (PS-001), operator training | 4 MED |
| R-002 | 3 | 4 | 12 HIGH | Internal revision inspections per AFS 2017:3, UT thickness measurements, drain condensate weekly | 6 MED |
| R-003 | 2 | 5 | 10 HIGH | Low water cutoff device, daily water level checks, annual boiler inspection by DNV | 4 MED |
| R-004 | 3 | 3 | 9 MED | Pre-charge pressure checks quarterly, bladder replacement at 5-year interval | 4 LOW |
| R-005 | 2 | 4 | 8 MED | O₂ monitoring alarm in gas store, ventilation, restricted access, cylinder restraints | 4 LOW |

### 4.2 Hazard Identification — Maintenance Activities

| ID | Hazard | Cause | Consequence |
|----|--------|-------|-------------|
| R-006 | Stored energy release during maintenance | Incomplete depressurisation, isolation failure | Burns, impact injury |
| R-007 | Confined space entry (vessel internal inspection) | Oxygen depletion, toxic atmosphere | Asphyxiation, poisoning |
| R-008 | Lifting injury during safety valve removal | Heavy components, awkward access | Musculoskeletal injury |
| R-009 | Chemical exposure during cleaning | Descaling agents, degreasing solvents | Skin/eye irritation, fume inhalation |

### 4.2b Risk Evaluation & Controls — Maintenance Activities

| ID | L | C | Risk | Controls | Residual |
|----|---|---|------|----------|----------|
| R-006 | 2 | 4 | 8 MED | Lock-out/tag-out procedure, double block and bleed, pressure gauge verification at zero | 3 LOW |
| R-007 | 2 | 5 | 10 HIGH | Confined space permit, gas testing, standby person, rescue plan, ventilation | 4 MED |
| R-008 | 3 | 2 | 6 MED | Mechanical lifting aids, two-person lift policy, pre-task briefing | 2 LOW |
| R-009 | 3 | 2 | 6 MED | SDS review, PPE (gloves, goggles, respirator), local exhaust ventilation | 2 LOW |

## 5. Risk Matrix Summary

| | Negligible (1) | Minor (2) | Moderate (3) | Major (4) | Catastrophic (5) |
|---|---|---|---|---|---|
| **Almost certain (5)** | | | | | |
| **Likely (4)** | | | | | |
| **Possible (3)** | | R-008, R-009 | R-004 | R-002 | |
| **Unlikely (2)** | | | | R-005, R-006 | R-001, R-003, R-007 |
| **Rare (1)** | | | | | |

## 6. Conclusions

- **3 high risks** identified (R-001, R-002, R-003, R-007) — all related to catastrophic pressure release or confined space work
- All high risks have been reduced to medium or low through existing and proposed controls
- **No critical (stop work) risks** identified
- The maintenance programme as designed in JDS-PRJ-MEC-001 adequately addresses the identified risks

## 7. Recommendations

| Priority | Action | Responsible | Target Date |
|----------|--------|-------------|-------------|
| High | Install O₂ depletion alarm in gas store (R-005) | Facility manager | 2026-Q2 |
| High | Develop confined space rescue plan (R-007) | Safety officer | 2026-Q2 |
| Medium | Establish UT thickness baseline for PV-001 and PV-004 (R-002) | Inspection contractor | 2026-Q3 |
| Medium | Procure mechanical lifting aid for valve workshop (R-008) | Workshop supervisor | 2026-Q3 |
| Low | Review and update SDS file for all maintenance chemicals (R-009) | Nils Johansson | 2026-Q4 |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Example risk assessment for JDS demonstration |
