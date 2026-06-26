# Equipment Lifetime Journal — [Site Name]

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-[NNN] |
| **Revision** | A |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT |
| **Author** | [Author name] |
| **Project** | JDS-PRJ-MEC-001 |
| **Client** | [Client name] |
| **Site** | [Site name] |

---

## 1. Purpose

This journal tracks the **remaining lifetime** of pressurised vessels at [site name] as required by AFS 2017:3, 4 Kap. §18. It records wall thickness measurements, calculates degradation rates, and estimates remaining service life for each vessel.

> **Regulatory requirement (§18):** The employer shall maintain a journal showing the remaining lifetime for Class A/B equipment with limited lifetime. If parts have different lifetimes, each part must be described separately. Equipment that has reached its documented lifetime may only remain pressurised if an analysis demonstrating extended lifetime has been conducted and documented.

---

## 2. Degradation Mechanisms

Three primary mechanisms limit vessel lifetime. Each vessel must be assessed for which apply:

| Mechanism | What It Is | How It Is Measured | Typical Equipment |
|-----------|-----------|-------------------|-------------------|
| **General corrosion** | Uniform wall thinning from chemical attack | Wall thickness measurement (UTM) | All vessels with corrosive media or environment |
| **Pitting / localised corrosion** | Localised deep attack | Pit depth gauge, UTM grid | Vessels with chlorides, stagnant zones, CUI risk |
| **Fatigue** | Crack initiation from repeated pressure cycling | Cycle counter, operating log | Vessels with frequent pressure changes |
| **Creep** | Slow deformation at sustained high temperature | Operating hours log, dimensional checks | Vessels operating above ~350°C (steel) |

---

## 3. Previous Experience Assessment (AFS 2017:3, 2 Kap. §1)

For each vessel, document whether the following risk factors have been considered:

| Vessel ID | Usage experience considered? | Remaining lifetime data available? | Repairs/modifications considered? | Accidents/incidents considered? | Deviation reports considered? | Continuous monitoring required? |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| PV-001 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |
| PV-002 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |
| PV-003 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |

**Notes on previous experience:**

| Vessel ID | Experience Summary |
|-----------|-------------------|
| PV-001 | [Any known history — prior incidents, recurring issues, modifications, operating anomalies] |
| PV-002 | |
| PV-003 | |

---

## 4. Vessel Lifetime Data

### 4.1 Design Parameters

| Vessel ID | Material | Original Wall (mm) | Min. Required (mm) | Corrosion Allow. (mm) | Design Cycles | Design Temp. (°C) |
|-----------|---------|-------------------|--------------------|--------------------|--------------|------------------|
| PV-001 | | | | | N/A | |
| PV-002 | | | | | N/A | |
| PV-003 | | | | | N/A | |

> **Original wall thickness:** from manufacturer data sheet or first inspection measurement.
> **Minimum required wall thickness:** from design calculation (PED, EN 13445, or equivalent).
> **Corrosion allowance:** original wall minus minimum required = available material for degradation.

### 4.2 Active Degradation Mechanisms

| Vessel ID | General Corrosion | Pitting | CUI Risk | Fatigue | Creep |
|-----------|:----------------:|:-------:|:--------:|:-------:|:-----:|
| PV-001 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |
| PV-002 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |
| PV-003 | Yes / No | Yes / No | Yes / No | Yes / No | Yes / No |

---

## 5. Wall Thickness Measurements

### How to Read This Section

Each measurement entry records:
- **Location:** measurement point on the vessel (use a consistent numbering scheme)
- **Measured:** actual wall thickness in mm (by ultrasonic thickness measurement or similar)
- **Rate:** calculated corrosion rate in mm/year
- **Remaining:** estimated remaining life in years

### Corrosion Rate Calculation

```
Corrosion rate (mm/yr) = (previous measurement - current measurement) / years between measurements

If only one measurement exists:
Corrosion rate (mm/yr) = (original wall - measured) / years in service
```

### Remaining Life Calculation

```
Remaining life (years) = (measured thickness - minimum required) / corrosion rate
```

> **Warning threshold:** When remaining life falls below **twice the inspection interval**, escalate to the program manager for review.

---

### Vessel: [PV-001]

**Measurement history:**

| Date | Location | Measured (mm) | Rate (mm/yr) | Remaining (yr) | Inspector | Method |
|------|----------|:----------:|:----------:|:----------:|-----------|--------|
| YYYY-MM-DD | | | | | | UTM |
| YYYY-MM-DD | | | | | | UTM |
| YYYY-MM-DD | | | | | | UTM |

**Condition trend:** Stable / Declining / Accelerating

**Action required:** None / Monitor / Plan repair / Engineering assessment

---

### Vessel: [PV-002]

**Measurement history:**

| Date | Location | Measured (mm) | Rate (mm/yr) | Remaining (yr) | Inspector | Method |
|------|----------|:----------:|:----------:|:----------:|-----------|--------|
| YYYY-MM-DD | | | | | | UTM |

**Condition trend:** Stable / Declining / Accelerating

**Action required:** None / Monitor / Plan repair / Engineering assessment

---

*(Repeat for each vessel)*

---

## 6. Fatigue Tracking (If Applicable)

| Vessel ID | Design Cycles | Counted Cycles | Remaining | Usage Rate (/yr) | Est. Life (yr) |
|-----------|:------------:|:-------------:|:---------:|:----------------:|:--------------:|
| | | | | | |

```
Remaining cycles = Design cycles - Counted cycles
Estimated remaining life (years) = Remaining cycles / Usage rate per year
```

---

## 7. Creep Tracking (If Applicable)

| Vessel ID | Design Hours | Logged Hours | Remaining | Usage (hr/yr) | Est. Life (yr) |
|-----------|:-----------:|:-----------:|:---------:|:-------------:|:--------------:|
| | | | | | |

```
Remaining hours = Design hours - Logged hours
Estimated remaining life (years) = Remaining hours / Usage rate per year
```

---

## 8. Lifetime Summary

| Vessel ID | Limiting Mechanism | Remaining Life (yr) | Status | Next Measurement |
|-----------|-------------------|:-------------------:|--------|-----------------|
| PV-001 | | | Safe / Monitor / Critical | YYYY-MM-DD |
| PV-002 | | | Safe / Monitor / Critical | YYYY-MM-DD |
| PV-003 | | | Safe / Monitor / Critical | YYYY-MM-DD |

**Status definitions:**

| Status | Remaining Life | Action |
|--------|:-------------:|--------|
| **Safe** | > 2x inspection interval | Continue normal program |
| **Monitor** | 1x — 2x inspection interval | Increase measurement frequency, inform inspection body |
| **Critical** | < 1x inspection interval | Engineering assessment required before next pressurisation |
| **Expired** | ≤ 0 years | Equipment must NOT be pressurised without documented lifetime extension analysis (§18) |

---

## 9. Lifetime Extension (§18, Second Paragraph)

If a vessel has reached its documented lifetime, it may only remain pressurised if:

1. An analysis demonstrating extended lifetime has been conducted
2. The analysis is documented in this journal
3. The analysis considers actual condition data (wall thickness, corrosion rate, inspection history)

| Vessel ID | Original End-of-Life | Extension Analysis | New End-of-Life | Approved By |
|-----------|---------------------|-------------------|----------------|------------|
| | YYYY | [Reference] | YYYY | [Name, role] |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | YYYY-MM-DD | [Author] | Initial journal |
