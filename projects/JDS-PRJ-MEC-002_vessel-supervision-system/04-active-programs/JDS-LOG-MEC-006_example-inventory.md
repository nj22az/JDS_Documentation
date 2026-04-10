# Equipment Inventory — Gothenburg Workshop

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-006 |
| **Revision** | A |
| **Date** | 2026-04-10 |
| **Status** | CURRENT |
| **Author** | N. Johansson |
| **Project** | JDS-PRJ-MEC-002 |
| **Client** | Example Workshop AB |
| **Site** | Gothenburg Workshop |

---

## 1. Purpose

This register is the master inventory of all pressurised vessels at Gothenburg Workshop. Classification, risk class, and inspection intervals have been **automatically calculated** per AFS 2017:3 (consolidated) using `jds-classify.py`.

---

## 2. Classification Summary

| Risk Class | Count | Inspection Regime |
|-----------|-------|-------------------|
| **Class A** | 4 | Accredited body: ext. 24 mo, int. 72 mo, press. test 144 mo |
| **Class B** | 2 | Accredited (int.) / own (ext.): ext. 36 mo, int. 72 mo |
| **Below B** | 0 | Own inspection: ext. 72 mo |
| **Simple PV** | 1 | No mandatory periodic inspection |
| **Not classified** | 0 | Below regulatory threshold |
| **Total** | **7** | |

---

## 3. Vessel Identification

| Vessel ID | Description | Location | Manufacturer | Year | Serial No. |
|-----------|-------------|----------|-------------|------|-----------|
| PV-001 | Main air receiver | Compressor room | Atlas Copco | 2015 | AC-2015-4521 |
| PV-002 | Workshop air receiver | Workshop B | Kaeser | 2018 | KS-2018-7892 |
| PV-003 | Steam boiler | Boiler house | Bosch | 2010 | BO-2010-3341 |
| PV-004 | Refrigeration receiver | Engine room | Bitzer | 2019 | BZ-2019-0087 |
| PV-005 | Hydraulic accumulator | Workshop A | Parker | 2020 | PK-2020-1155 |
| PV-006 | Expansion vessel | Heating system | Flamco | 2021 | FL-2021-6629 |
| PV-007 | Sandblast receiver | Yard | Clemco | 2012 | CL-2012-9944 |

---

## 4. Technical Data

| Vessel ID | PS (bar) | TS max (°C) | Volume (L) | PS×V (bar·L) | Medium |
|-----------|---------|-------------|-----------|--------------|--------|
| PV-001 | 11.0 | 40 | 1000 | 11,000 | compressed air |
| PV-002 | 8.0 | 50 | 250 | 2,000 | compressed air |
| PV-003 | 13.0 | 180 | 2000 | 26,000 | steam |
| PV-004 | 25.0 | 60 | 200 | 5,000 | ammonia |
| PV-005 | 250.0 | 80 | 10 | 2,500 | hydraulic oil |
| PV-006 | 3.0 | 90 | 25 | 75 | water |
| PV-007 | 10.0 | 50 | 500 | 5,000 | compressed air |

---

## 5. Regulatory Classification (Auto-Generated)

> Classification calculated automatically by `jds-classify.py` per AFS 2017:3.

| Vessel ID | Fluid Grp | PED Cat. | Risk Class | Inspector | CE | DoC |
|-----------|----------|----------|-----------|-----------|----|----|
| PV-001 | 2 | IV | **A** | Accredited body | Yes | Yes |
| PV-002 | 2 | II | **B** | Accredited body (int.) / Own (ext.) | Yes | Yes |
| PV-003 | 2 | IV | **A** | Accredited body | Yes | Yes |
| PV-004 | 1 | IV | **A** | Accredited body | Yes | Yes |
| PV-005 | 2 | II | **B** | Accredited body (int.) / Own (ext.) | Yes | Yes |
| PV-006 | 2 | Art. 4.3 | **Simple PV** | N/A | Yes | Yes |
| PV-007 | 2 | III | **A** | Accredited body | Yes | No |

---

## 6. Inspection Schedule (Auto-Generated)

> Intervals and next due dates calculated automatically from classification and last inspection.

| Vessel ID | Ext. (mo) | Int. (mo) | Press. (mo) | Last Insp. | Next Ext. | Next Int. |
|-----------|----------|----------|------------|-----------|----------|----------|
| PV-001 | 24 | 72 | 144 | 2024-06-15 | 2026-06-15 | 2030-06-15 |
| PV-002 | 36 | 72 | — | 2025-01-20 | 2028-01-20 | 2031-01-20 |
| PV-003 | 24 | 72 | 144 | 2023-09-01 | 2025-09-01 | 2029-09-01 |
| PV-004 | 24 | 72 | 144 | 2025-03-10 | 2027-03-10 | 2031-03-10 |
| PV-005 | 36 | 72 | — | 2024-11-30 | 2027-11-30 | 2030-11-30 |
| PV-006 | — | — | — | — | — | — |
| PV-007 | 24 | 72 | 144 | 2023-04-22 | 2025-04-22 | 2029-04-22 |


### OVERDUE INSPECTIONS

| Vessel ID | Type | Was Due | Days Overdue |
|-----------|------|---------|-------------|
| PV-003 | External | 2025-09-01 | **221** |
| PV-007 | External | 2025-04-22 | **353** |


---

## 7. Safety Devices

| Device ID | Type | Protects | Set Pressure (bar) | Last Test | Next Test |
|-----------|------|----------|------------------- |-----------|-----------|
| SV-001 | Safety valve | PV-001 | | | |
| SV-002 | Safety valve | PV-002 | | | |
| SV-003 | Safety valve | PV-003 | | | |
| SV-004 | Safety valve | PV-004 | | | |
| SV-005 | Safety valve | PV-005 | | | |
| SV-007 | Safety valve | PV-007 | | | |

---

## 8. Documentation Checklist

### Vessels PV-001 to PV-004

| Check | PV-001 | PV-002 | PV-003 | PV-004 |
|-------|--------|--------|--------|--------|
| Registered in inventory | | | | |
| Nameplate photo on file | | | | |
| EU DoC on file | | | | |
| Risk class confirmed | | | | |
| Safety devices documented | | | | |
| Current certificate on file | | | | |

### Vessels PV-005 to PV-007

| Check | PV-005 | PV-006 | PV-007 |
|-------|--------|--------|--------|
| Registered in inventory | | | |
| Nameplate photo on file | | | |
| EU DoC on file | | | |
| Risk class confirmed | | | |
| Safety devices documented | | | |
| Current certificate on file | | | |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-10 | N. Johansson | Initial inventory — 7 vessels classified |
