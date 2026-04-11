# Equipment Lifetime Journal — Gothenburg Workshop

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-008 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |
| **Project** | JDS-PRJ-MEC-002 |
| **Client** | Example Workshop AB |
| **Site** | Gothenburg Workshop |

---

## 1. Purpose

This journal tracks the **remaining lifetime** of pressurised vessels at Gothenburg Workshop as required by AFS 2017:3, 4 Kap. §18. It records wall thickness measurements, calculates degradation rates, and estimates remaining service life.

> This is an **example document** demonstrating realistic corrosion tracking for the Gothenburg Workshop vessel set. The measurement data is illustrative.

---

## 2. Vessel Lifetime Data

### 2.1 Design Parameters

| Vessel ID | Description | Material | Orig. Wall (mm) | Min. Req. (mm) | Corr. Allow. (mm) |
|-----------|-------------|---------|:---------------:|:--------------:|:-----------------:|
| PV-001 | Main air receiver | P265GH | 8.0 | 5.2 | 2.8 |
| PV-003 | Steam boiler | 16Mo3 | 12.0 | 8.5 | 3.5 |
| PV-004 | Refrigeration receiver | P355N | 10.0 | 7.0 | 3.0 |
| PV-005 | Hydraulic accumulator | P265GH | 6.0 | 4.2 | 1.8 |

> PV-002 and PV-007 (air receivers, Class B exempt) and PV-006 (below threshold) are not tracked in this journal per §18 scope (Class A and B with limited lifetime only).

### 2.2 Active Degradation Mechanisms

| Vessel ID | Gen. Corrosion | Pitting | CUI Risk | Fatigue | Creep |
|-----------|:--------------:|:-------:|:--------:|:-------:|:-----:|
| PV-001 | Yes | No | No | No | No |
| PV-003 | Yes | No | Yes | No | Yes |
| PV-004 | Yes | Yes | No | No | No |
| PV-005 | No | No | No | Yes | No |

**Notes:**
- **PV-001:** General internal corrosion from moisture in compressed air. External corrosion minimal (indoor, dry).
- **PV-003:** Fire-side corrosion + CUI risk on insulated sections. Creep tracking required (operating >110°C).
- **PV-004:** Ammonia stress corrosion cracking risk. Pitting possible at weld zones.
- **PV-005:** Hydraulic cycling fatigue (not corrosion-limited). Approx. 50 cycles/day.

---

## 3. Wall Thickness Measurements

### PV-001 — Main Air Receiver (Class A, Compressed Air)

**Measurement history:**

| Date | Location | Measured (mm) | Rate (mm/yr) | Remaining (yr) | Inspector | Method |
|------|----------|:------------:|:------------:|:--------------:|-----------|--------|
| 2015-06-01 | Bottom shell | 8.0 | — | — | DEKRA | UTM (baseline) |
| 2019-06-15 | Bottom shell | 7.6 | 0.10 | 24.0 | DEKRA | UTM |
| 2019-06-15 | Top shell | 7.8 | 0.05 | 52.0 | DEKRA | UTM |
| 2019-06-15 | Drain nozzle | 7.4 | 0.15 | 14.7 | DEKRA | UTM |
| 2024-06-15 | Bottom shell | 7.1 | 0.10 | 19.0 | DEKRA | UTM |
| 2024-06-15 | Top shell | 7.6 | 0.04 | 60.0 | DEKRA | UTM |
| 2024-06-15 | Drain nozzle | 6.7 | 0.14 | 10.7 | DEKRA | UTM |

**Limiting location:** Drain nozzle (highest corrosion rate)
**Current corrosion rate:** 0.14 mm/year
**Remaining life:** 10.7 years (from 2024 measurement)
**Condition trend:** Stable
**Action required:** Monitor — drain nozzle rate is elevated but within acceptable range. Ensure condensate drain is operated regularly.

---

### PV-003 — Steam Boiler (Class A, Steam)

**Measurement history:**

| Date | Location | Measured (mm) | Rate (mm/yr) | Remaining (yr) | Inspector | Method |
|------|----------|:------------:|:------------:|:--------------:|-----------|--------|
| 2010-09-01 | Fire-side shell | 12.0 | — | — | Kiwa | UTM (baseline) |
| 2014-09-01 | Fire-side shell | 11.2 | 0.20 | 13.5 | Kiwa | UTM |
| 2014-09-01 | Water-side shell | 11.6 | 0.10 | 31.0 | Kiwa | UTM |
| 2014-09-01 | Tube plate | 11.0 | 0.25 | 10.0 | Kiwa | UTM |
| 2018-09-01 | Fire-side shell | 10.4 | 0.20 | 9.5 | Kiwa | UTM |
| 2018-09-01 | Water-side shell | 11.2 | 0.10 | 27.0 | Kiwa | UTM |
| 2018-09-01 | Tube plate | 10.0 | 0.25 | 6.0 | Kiwa | UTM |
| 2023-09-01 | Fire-side shell | 9.4 | 0.20 | 4.5 | Kiwa | UTM |
| 2023-09-01 | Water-side shell | 10.7 | 0.10 | 22.0 | Kiwa | UTM |
| 2023-09-01 | Tube plate | 8.8 | 0.24 | 1.3 | Kiwa | UTM |

**Limiting location:** Tube plate (highest corrosion rate + lowest remaining life)
**Current corrosion rate:** 0.24 mm/year (tube plate)
**Remaining life:** **1.3 years** (from 2023 measurement) �� **CRITICAL**
**Condition trend:** Declining �� tube plate degrading faster than predicted

> **Warning:** Engineering assessment required. Tube plate approaching minimum thickness. Must not be pressurised beyond Q1 2025 without documented lifetime extension analysis or repair. Escalate to operator immediately.

---

### PV-004 — Refrigeration Receiver (Class A, Ammonia)

**Measurement history:**

| Date | Location | Measured (mm) | Rate (mm/yr) | Remaining (yr) | Inspector | Method |
|------|----------|:------------:|:------------:|:--------------:|-----------|--------|
| 2019-03-01 | Shell body | 10.0 | — | — | RISE | UTM (baseline) |
| 2022-03-10 | Shell body | 9.9 | 0.03 | 96.7 | RISE | UTM |
| 2022-03-10 | Weld seam A | 9.8 | 0.07 | 40.0 | RISE | UTM |
| 2025-03-10 | Shell body | 9.8 | 0.03 | 93.3 | RISE | UTM |
| 2025-03-10 | Weld seam A | 9.7 | 0.05 | 54.0 | RISE | UTM |

**Pitting inspection (visual + MPI at weld zones):**

| Date | Location | Findings | Max Pit Depth (mm) |
|------|----------|----------|:-----------------:|
| 2022-03-10 | Weld seam A | No pitting found | — |
| 2025-03-10 | Weld seam A | Minor surface indications, not measured as pitting | — |

**Limiting location:** Weld seam A
**Current corrosion rate:** 0.05 mm/year (very low — ammonia systems typically clean)
**Remaining life:** 54 years
**Condition trend:** Stable
**Action required:** None — continue standard program. Monitor weld seam indications at next examination.

---

### PV-005 — Hydraulic Accumulator (Class B, Hydraulic Oil)

**This vessel is fatigue-limited, not corrosion-limited.** Wall thickness is not the primary degradation mechanism.

**Fatigue tracking:**

| Parameter | Value |
|-----------|-------|
| Design cycles (manufacturer) | 500,000 |
| Estimated usage | ~50 cycles/day, 250 days/year = 12,500/year |
| Service start | 2020 |
| Cycles to date (est.) | 75,000 (6 years x 12,500) |
| Remaining cycles | 425,000 |
| Estimated remaining life | **34 years** |

**Condition trend:** Stable — well within fatigue design limit
**Action required:** None — continue standard program. Verify cycle estimate if operating pattern changes.

---

## 4. Creep Tracking — PV-003

Steam boiler operates above 110°C — creep tracking required.

| Parameter | Value |
|-----------|-------|
| Design temperature | 180°C |
| Creep design hours (manufacturer) | 200,000 hours |
| Operating hours to date | ~105,000 hours (2010-2026, ~75% duty) |
| Remaining hours | 95,000 |
| Estimated usage rate | ~6,500 hours/year |
| Estimated remaining creep life | **14.6 years** |

> **Note:** Creep life is estimated. Actual remaining life is limited by the **tube plate corrosion** (1.3 years) — see Section 3.

---

## 5. Lifetime Summary

| Vessel ID | Limiting Mechanism | Remaining Life | Status | Next Measurement |
|-----------|-------------------|:--------------:|--------|-----------------|
| PV-001 | General corrosion (drain nozzle) | **10.7 years** | Safe | 2028-06 |
| PV-003 | General corrosion (tube plate) | **1.3 years** | **Critical** | **Immediate** |
| PV-004 | General corrosion (weld seam) | 54 years | Safe | 2029-03 |
| PV-005 | Fatigue cycling | 34 years | Safe | 2030 (review) |

### Status Legend

| Status | Remaining Life | Action |
|--------|:-------------:|--------|
| **Safe** | > 2x inspection interval | Continue normal program |
| **Monitor** | 1x — 2x inspection interval | Increase measurement frequency |
| **Critical** | < 1x inspection interval | Engineering assessment before next pressurisation |
| **Expired** | ≤ 0 years | Must NOT be pressurised without lifetime extension analysis (§18) |

> **Warning:** A vessel with status **Critical** or **Expired** must not continue in normal operation. Expired vessels must be depressurised immediately. Critical vessels require an engineering assessment before the next pressurisation cycle.

---

## 6. Lifetime Extension — PV-003 Tube Plate

> **This section demonstrates what §18 second paragraph requires when equipment approaches end of life.**

| | |
|---|---|
| **Vessel** | PV-003 — Steam boiler |
| **Component** | Tube plate |
| **Original end-of-life** | Q1 2025 (based on 2023 measurement) |
| **Extension analysis** | [To be performed — fitness-for-service assessment per EN 13445-3 Annex B or API 579-1] |
| **New end-of-life** | [Pending analysis] |
| **Approved by** | [Name, role] |

**Required actions before continued pressurisation:**
1. Commission fitness-for-service assessment by competent engineer
2. Consider repair options (weld overlay, tube plate replacement)
3. If extended: document the analysis, update this journal, inform inspection body
4. If not extendable: take PV-003 out of service, plan replacement

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial journal — 4 vessels tracked. PV-003 tube plate flagged CRITICAL (1.3 yr remaining). |
