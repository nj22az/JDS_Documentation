# Equipment Inventory — Göteborg Workshop

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-003 |
| **Revision** | B |
| **Date** | 2026-03-25 |
| **Status** | EXAMPLE |
| **Author** | Nils Johansson |

---

## 1. Purpose

This inventory provides a complete register of pressure vessels and pressurised equipment at the Göteborg Workshop facility. It fulfils the requirements of AFS 2017:3 (Användning och kontroll av trycksatta anordningar) and serves as the master reference for inspection planning.

## 2. Equipment Register

### 2.1 Identification

| Vessel ID | Description | Location | Manufacturer | Year | Serial No. |
|-----------|-------------|----------|-------------|------|------------|
| PV-001 | Compressed air receiver | Compressor room | Atlas Copco | 2018 | AC-2018-4472 |
| PV-002 | Compressed air receiver | Workshop south | Pneumatech | 2015 | PT-15-882 |
| PV-003 | Hydraulic accumulator | Press station 1 | Hydac | 2020 | HY-20-1193 |
| PV-004 | Steam boiler | Boiler house | Bosch | 2012 | BSH-12-5561 |
| HE-001 | Shell & tube heat exchanger | Engine room | Alfa Laval | 2019 | AL-19-7034 |
| AR-001 | Nitrogen cylinder bank | Gas store | AGA | 2021 | AGA-21-0044 |

### 2.2 Technical Data

| Vessel ID | PS (bar) | V (L) | PS×V | Medium | Class |
|-----------|----------|-------|------|--------|-------|
| PV-001 | 11 | 500 | 5500 | Air | A |
| PV-002 | 10 | 250 | 2500 | Air | B |
| PV-003 | 250 | 50 | 12500 | N₂/Oil | A |
| PV-004 | 6 | 800 | 4800 | Steam | A |
| HE-001 | 16 | 120 | 1920 | Glycol | B |
| AR-001 | 200 | 50×6 | 60000 | N₂ | A |

## 3. Inspection Status

| Vessel ID | Last Inspection | Type | Next Due | Inspector | Certificate Ref | Status |
|-----------|----------------|------|----------|-----------|----------------|--------|
| PV-001 | 2025-06-15 | Revision (internal) | 2027-06-15 | Kiwa Inspecta | KI-2025-44721 | IN SERVICE |
| PV-002 | 2025-03-20 | External | 2027-03-20 | DEKRA | DK-2025-8823 | IN SERVICE |
| PV-003 | 2024-11-10 | Revision (internal) | 2026-11-10 | Kiwa Inspecta | KI-2024-39102 | IN SERVICE — MONITOR |
| PV-004 | 2025-09-01 | Revision (internal) | 2026-09-01 | DNV | DNV-2025-SE-1147 | IN SERVICE |
| HE-001 | 2025-01-22 | External | 2027-01-22 | DEKRA | DK-2025-1205 | IN SERVICE |
| AR-001 | 2025-08-30 | Periodic test | 2035-08-30 | Kiwa Inspecta | KI-2025-50091 | IN SERVICE |

## 4. Safety Device Register

| Device ID | Type | Protected Vessel | Set Pressure (bar) | Last Test | Next Test | Status |
|-----------|------|-----------------|-------------------|-----------|-----------|--------|
| SV-001 | Relief valve | PV-001 | 11.5 | 2025-06-15 | 2027-06-15 | OK |
| SV-002 | Relief valve | PV-002 | 10.5 | 2025-03-20 | 2027-03-20 | OK |
| SV-003 | Relief valve | PV-003 | 260 | 2024-11-10 | 2026-11-10 | OK |
| SV-004 | Relief valve + rupture disc | PV-004 | 6.5 | 2025-09-01 | 2026-09-01 | OK |
| PS-001 | Pressure switch (high) | PV-004 | 5.8 | 2025-09-01 | 2026-09-01 | OK |

## 5. Annual Inspection Calendar 2026

| Vessel | Q1 (Jan–Mar) | Q2 (Apr–Jun) | Q3 (Jul–Sep) | Q4 (Oct–Dec) |
|--------|-------------|-------------|-------------|-------------|
| PV-001 | — | — | — | — |
| PV-002 | — | — | — | — |
| PV-003 | — | — | — | R (Nov) |
| PV-004 | — | — | R (Sep) | — |
| HE-001 | — | — | — | — |
| AR-001 | — | — | — | — |

R = Revision (internal), E = External, P = Pressure test

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Example inventory for JDS demonstration |
| B | 2026-03-25 | Nils Johansson | Split wide tables to ≤7 columns for A4 readability |
