# Maintenance Report

| | |
|---|---|
| **Document No.** | JDS-RPT-MEC-003 |
| **Revision** | A |
| **Date** | 2026-03-26 |
| **Status** | CURRENT |
| **Author** | N. Johansson |
| **Project** | JDS-PRJ-MEC-001 |
| **Client** | Scandinavian Process Industries AB |
| **Site** | Industrivägen 45, Gothenburg |

---

## 1. Summary

| | |
|---|---|
| **Equipment** | Cooling Water Circulation Pump — P-201A |
| **Maintenance Type** | Corrective — unplanned seal replacement |
| **Date Performed** | 18–19 March 2026 |
| **Performed By** | N. Johansson (Johansson Engineering), T. Eriksson (SPI Maintenance) |
| **Work Order** | WO-2026-0147 |
| **Result** | Equipment returned to service |

---

## 2. Equipment Data

| Parameter | Value |
|-----------|-------|
| **Equipment ID** | P-201A |
| **Description** | Centrifugal cooling water pump, horizontal single-stage |
| **Manufacturer** | Grundfos |
| **Model** | NK 80-200/211 |
| **Serial No.** | 96107638 |
| **Year Built** | 2016 |
| **Location** | Pump room, Level 0, Bay 3 |
| **Operating Hours** | 42,350 h (at time of failure) |

---

## 3. Scope of Work

Pump P-201A was reported leaking from the mechanical seal on 17 March 2026 by the site operator. Visible drip rate exceeded acceptable limits (approximately 2 drops/second). The decision was made to replace the mechanical seal assembly. This is a corrective maintenance action — the pump was not due for scheduled seal replacement until Q4 2026.

### 3.1 Planned Tasks

- [x] Isolate pump and drain cooling water circuit
- [x] Remove coupling guard and disconnect motor coupling
- [x] Remove bearing housing and impeller assembly
- [x] Remove and inspect mechanical seal
- [x] Install new mechanical seal assembly
- [x] Reassemble pump and reconnect coupling
- [x] Perform alignment check (dial indicator)
- [x] Refill system, vent, and perform leak test
- [x] Run test at full speed — vibration and temperature check

---

## 4. Findings

### 4.1 Condition Assessment

| Component | Condition | Notes |
|-----------|-----------|-------|
| Mechanical seal (old) | Failed | O-ring cracked, carbon face scored. Cause: age + thermal cycling. |
| Impeller | Good | No erosion or cavitation damage. Clearances within spec. |
| Wear rings | Acceptable | Minor wear. Clearance 0.35mm (max allowable 0.50mm). |
| Bearings (DE/NDE) | Good | No play detected. Grease condition normal. |
| Shaft | Good | No scoring under seal seat. Surface finish acceptable. |
| Coupling | Acceptable | Rubber elements showing age but functional. |

### 4.2 Measurements

| Parameter | Measured Value | Acceptable Range | Status |
|-----------|--------------|-----------------|--------|
| Shaft runout at seal seat | 0.02 mm | < 0.05 mm | OK |
| Wear ring clearance (suction) | 0.35 mm | 0.20 – 0.50 mm | OK |
| Coupling alignment (angular) | 0.03 mm | < 0.05 mm | OK |
| Coupling alignment (offset) | 0.04 mm | < 0.05 mm | OK |
| Vibration — DE bearing (radial) | 1.8 mm/s RMS | < 4.5 mm/s | OK |
| Vibration — NDE bearing (radial) | 1.4 mm/s RMS | < 4.5 mm/s | OK |
| Bearing temperature (DE) after 30 min | 48 °C | < 80 °C | OK |

---

## 5. Work Performed

Pump was isolated and drained on 18 March. The mechanical seal was removed and inspected — the stationary O-ring was cracked and the carbon face was scored, likely due to thermal cycling over 42,000 operating hours. A new Grundfos replacement seal kit (part no. 96525458) was installed. The pump was reassembled, aligned, and tested on 19 March.

The wear ring clearance is approaching the service limit (0.35mm of 0.50mm max). This does not require immediate action but should be checked at the next planned maintenance.

### 5.1 Parts Replaced

| Part | Part Number | Old Condition | New Part Source |
|------|------------|---------------|----------------|
| Mechanical seal assembly | 96525458 | Failed — cracked O-ring, scored face | Grundfos Sweden (stock) |
| Gasket set — pump casing | GK-NK80-SET | Replaced as preventive measure | Stock |

### 5.2 Materials Used

| Material | Quantity | Purpose |
|----------|---------|---------|
| Loctite 243 (thread lock) | 5 ml | Impeller nut |
| Shell Gadus S2 V220 grease | 50 g | Bearing repack |

---

## 6. Test Results

| Test | Acceptance Criteria | Result | Status |
|------|-------------------|--------|--------|
| Leak test (30 min at operating pressure) | Zero visible leakage | No leakage observed | Pass |
| Vibration check (full speed, 30 min) | < 4.5 mm/s RMS all bearings | Max 1.8 mm/s (DE) | Pass |
| Temperature check (DE bearing, 30 min) | < 80 °C | 48 °C | Pass |
| Flow rate at rated duty point | 80 m³/h ± 5% | 79 m³/h | Pass |

---

## 7. Recommendations

| Priority | Recommendation | Responsible | Due Date |
|----------|---------------|------------|----------|
| Medium | Monitor wear ring clearance at next planned maintenance (Q4 2026) | SPI Maintenance | 2026-Q4 |
| Low | Consider replacing coupling rubber elements at next opportunity | SPI Maintenance | 2027-Q1 |
| Low | Add seal replacement to preventive schedule at 35,000 h intervals | SPI Maintenance | Ongoing |

---

## 8. Sign-Off

| Role | Name | Date |
|------|------|------|
| Maintenance Engineer | N. Johansson | 2026-03-19 |
| Reviewed By | — | — |
| Client Acceptance | T. Eriksson | 2026-03-19 |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-26 | N. Johansson | Example maintenance report for JDS demonstration |
