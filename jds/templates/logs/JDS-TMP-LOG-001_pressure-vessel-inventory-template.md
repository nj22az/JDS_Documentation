# Pressure Vessel Inventory — [Client / Site Name]

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-[NNN] |
| **Revision** | DRAFT |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT |
| **Author** | Nils Johansson |
| **Project** | [JDS-PRJ reference or N/A] |
| **Client** | [Client name or Internal] |
| **Site** | [Physical location / facility name] |
| **Regulatory Basis** | [e.g., AFS 2017:3 (Sweden), PED 2014/68/EU, ASME, etc.] |

---

## 1. Purpose

This inventory is the master register of all pressurised vessels at [site name]. It serves as the foundation for the ongoing maintenance program by providing a single source of truth for:

- What equipment exists
- Where it is located
- What condition it is in
- When it needs inspection

> **If a vessel is not in this inventory, it does not exist in the maintenance program.**

## 2. How to Use This Inventory

1. **Add a new vessel** — one row per vessel, fill all mandatory fields
2. **Update after inspection** — update Last Inspection, Next Inspection, Certificate Ref, and Status
3. **Review quarterly** — check that no vessel has passed its Next Inspection date
4. **Revise the document** — when vessels are added, removed, or reclassified, issue a new revision

## 3. Equipment Inventory

### 3.1 Column Definitions

| Column | Description | Example | Mandatory? |
|--------|-------------|---------|-----------|
| **Vessel ID** | Unique identifier for this vessel | PV-001 | Yes |
| **Tag / KKS** | Plant tag number or KKS code (if applicable) | 1MAA01 BB001 | If available |
| **Description** | Plain language description | Compressed air receiver | Yes |
| **Location** | Physical installation location | Machine hall, bay 3 | Yes |
| **Manufacturer** | From nameplate | Atlas Copco | Yes |
| **Model** | Manufacturer's model/type designation | LT 500 | If available |
| **Year Built** | Year of manufacture (from nameplate) | 2018 | Yes |
| **Serial No.** | Manufacturer's serial number | AC-2018-44521 | Yes |
| **Design Pressure (PS)** | Maximum allowable working pressure | 11 bar | Yes |
| **Design Temp** | Maximum allowable temperature | 200°C | Yes |
| **Volume (V)** | Internal volume | 500 L | Yes |
| **PS × V** | Pressure-volume product (for classification) | 5,500 bar·L | Yes |
| **Medium** | Contents of the vessel | Compressed air | Yes |
| **Medium Group** | Group 1 (dangerous) or Group 2 (other) | Group 2 | Yes |
| **Regulatory Class** | Classification per applicable regulation | Class B | Yes |
| **CE Marked** | Does it carry a CE mark? | Yes / No | Yes |
| **Notified Body** | CE notified body number (from nameplate) | NB 0036 | If CE marked |
| **Safety Devices** | Relief valve, rupture disc, pressure switch | SV set at 11.5 bar | Yes |
| **Last Inspection** | Date of most recent inspection | 2025-06-15 | Yes (after first) |
| **Inspection Type** | What type was performed | External / Internal / Pressure test | Yes (after first) |
| **Next Inspection** | When next inspection is due | 2027-06-15 | Yes |
| **Inspector** | Who performed the last inspection | DEKRA / Kiwa / Internal | Yes (after first) |
| **Certificate Ref** | Inspection certificate reference number | DEKRA-2025-12345 | Yes (after first) |
| **Status** | Current operational status | IN SERVICE | Yes |
| **Condition Rating** | Overall condition assessment | Good / Acceptable / Monitor / Poor | Recommended |
| **Notes** | Important observations, defects, repair history | Minor corrosion on weld seam | As needed |

### 3.2 Status Values

| Status | Meaning |
|--------|---------|
| **IN SERVICE** | Operating normally, inspections current |
| **IN SERVICE — MONITOR** | Operating but with known condition to watch |
| **OUT OF SERVICE** | Temporarily removed from service (not decommissioned) |
| **AWAITING INSPECTION** | Inspection is overdue or pending |
| **DECOMMISSIONED** | Permanently removed from service |
| **NEW — NOT YET COMMISSIONED** | Installed but not yet put into service |

### 3.3 Condition Ratings

| Rating | Meaning | Action |
|--------|---------|--------|
| **Good** | No defects, within design parameters | Continue normal inspection schedule |
| **Acceptable** | Minor wear/ageing within tolerance | Continue normal inspection schedule |
| **Monitor** | Condition noted that requires tracking | Reduce inspection interval or add specific checks |
| **Poor** | Significant deterioration or defect | Immediate engineering assessment required |

---

## 4. Inventory Register

*Copy the tables below and fill one row per vessel. Add rows as needed. Tables are linked by Vessel ID.*

### 4.1 Identification

| Vessel ID | Description | Location | Manufacturer | Year | Serial No. |
|-----------|-------------|----------|--------------|------|------------|
| PV-001 | *[example]* | *[loc]* | *[mfr]* | *[yr]* | *[s/n]* |
| | | | | | |
| | | | | | |

### 4.2 Technical Data

| Vessel ID | PS (bar) | V (L) | PS×V | Medium | Group | Class |
|-----------|----------|-------|------|--------|-------|-------|
| PV-001 | *[bar]* | *[L]* | *[bar·L]* | *[medium]* | *[1/2]* | *[A/B/C]* |
| | | | | | | |
| | | | | | | |

### 4.3 Inspection Status

| Vessel ID | Last Insp. | Next Insp. | Inspector | Status |
|-----------|------------|------------|-----------|--------|
| PV-001 | *[date]* | *[date]* | *[name]* | *[status]* |
| | | | | |
| | | | | |

---

## 5. Safety Device Register

*Track safety devices (relief valves, rupture discs, pressure switches) separately for test scheduling.*

| Device ID | Type | Protects Vessel | Set Pressure | Test Interval |
|-----------|------|-----------------|-------------|---------------|
| SV-001 | Relief valve | PV-001 | 11.5 bar | 12 months |
| | | | | |

### 5.1 Safety Device Test Records

| Device ID | Last Test | Next Test | Test Result | Tested By |
|-----------|-----------|-----------|-------------|-----------|
| SV-001 | *[date]* | *[date]* | Pass / Fail | *[name]* |
| | | | | |

---

## 6. Inspection Calendar — Annual Overview

*Fill in planned inspection dates for each vessel. Mark completed inspections with ✓.*

| Vessel ID | Q1 (Jan–Mar) | Q2 (Apr–Jun) | Q3 (Jul–Sep) | Q4 (Oct–Dec) |
|-----------|-------------|-------------|-------------|-------------|
| PV-001 | — | EXT (Jun) | — | — |
| | | | | |

**Inspection type codes:** EXT = External, INT = Internal, PT = Pressure test, SV = Safety valve test

---

## 7. Decommissioned Vessels

*Vessels removed from service are moved here for historical record.*

| Vessel ID | Description | Date Decommissioned | Reason | Disposition |
|-----------|-------------|---------------------|--------|-------------|
| | | | | Scrapped / Sold / Relocated |

---

## 8. Document References

| Document | JDS Reference | Description |
|----------|--------------|-------------|
| Regulatory reference | [link to regulations] | Applicable regulations and classification rules |
| Documentation guide | [link to guide] | What records to keep per vessel |
| Inspection planning | [link to planning] | How to plan and schedule inspections |

---

## 9. Komplekt Status (Per Vessel)

For each vessel in service, verify these documents exist:

- [ ] Vessel registered in this inventory (all fields filled)
- [ ] Manufacturer's data sheet / nameplate data recorded
- [ ] CE Declaration of Conformity on file (if applicable)
- [ ] Regulatory classification confirmed
- [ ] Safety devices identified and test schedule established
- [ ] Most recent inspection report on file
- [ ] Next inspection date in the future (not overdue)

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| DRAFT | YYYY-MM-DD | [Author] | Initial draft |
