# Equipment Inventory — [Site Name]

| | |
|---|---|
| **Document No.** | JDS-LOG-MEC-[NNN] |
| **Revision** | A |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT |
| **Author** | [Author name] |
| **Project** | JDS-PRJ-MEC-001 |
| **Client** | [Client name] |
| **Site** | [Site name / address] |

---

## 1. Purpose

This register is the master inventory of all pressurised vessels at [site name]. It provides the complete equipment record required for regulatory compliance and serves as the foundation for the supervision program.

> **Auto-classification available:** Run `python3 scripts/jds-classify.py --csv [data.csv]` to generate this inventory automatically from a CSV file. The script calculates classification, risk class, and inspection intervals per AFS 2017:3.

---

## 2. Classification Summary

| Risk Class | Count | Inspection Regime |
|-----------|-------|-------------------|
| **Class A** | | Driftprov base 2–4 yr; internal/external **condition-based** per Bilaga 1 (accredited body) |
| **Class B** | | Driftprov only — 2–4 yr (accredited int. / own ext. where approved) |
| **Exempt (air/N₂/refrig.)** | | No periodic inspection — Class B exemption (4 Kap. §10) |
| **Below threshold** | | Not classified under AFS 2017:3 |
| **Total** | | |

---

## 3. Vessel Identification

| Vessel ID | Description | Location | Manufacturer | Year | Serial No. |
|-----------|-------------|----------|-------------|------|-----------|
| PV-001 | | | | | |
| PV-002 | | | | | |
| PV-003 | | | | | |

---

## 4. Technical Data

| Vessel ID | PS (bar) | TS max (deg C) | Volume (L) | PS x V (bar-L) | Medium |
|-----------|---------|-------------|-----------|--------------|--------|
| PV-001 | | | | | |
| PV-002 | | | | | |
| PV-003 | | | | | |

---

## 5. Regulatory Classification

> To auto-generate this section, use `jds-classify.py`. Manual classification reference:
>
> **Group 2a (non-dangerous) gases:** Class A if PS×V > 10,000 | Class B if PS×V ≤ 10,000 (V > 1 L, p > 0.5 bar). Air/N₂ that would be Class B are exempt (no class).
>
> **Group 1a (dangerous) gases:** Class A if PS×V > 1,000 | Class B if PS×V ≤ 1,000 (V > 1 L, p > 0.5 bar).
>
> *(Per 4 Kap. §10 — see JDS-RPT-MEC-003 §4.1.)*

| Vessel ID | Fluid Grp | PED Cat. | Risk Class | Inspector | CE | DoC |
|-----------|----------|----------|-----------|-----------|----|----|
| PV-001 | 1 / 2 | I-IV / Art.4.3 | A / B | | Yes / No | Yes / No |
| PV-002 | 1 / 2 | I-IV / Art.4.3 | A / B | | Yes / No | Yes / No |
| PV-003 | 1 / 2 | I-IV / Art.4.3 | A / B | | Yes / No | Yes / No |

---

## 6. Inspection Schedule

> To auto-generate next due dates, use `jds-classify.py` with `last_inspection` in CSV.

| Vessel ID | Ext. (mo) | Int. (mo) | Press. (mo) | Last Insp. | Next Ext. | Next Int. |
|-----------|----------|----------|------------|-----------|----------|----------|
| PV-001 | | | | | | |
| PV-002 | | | | | | |
| PV-003 | | | | | | |

**Interval reference (per AFS 2017:3 Bilaga 1 — see JDS-RPT-MEC-003 §6):**

| Risk Class | Driftprov (operational test) | Internal/external examination |
|-----------|------------------------------|-------------------------------|
| Class A | 2 yr base (4 yr for air/N₂/refrigeration/LPG); max 4 yr | **Condition-based**, set by inspection body — 1 to 10 yr |
| Class B | 2 yr base (4 yr for air/N₂ etc.) | Not required (driftprov only) |
| Exempt / below threshold | — | — |

---

## 7. Safety Devices

| Device ID | Type | Protects | Set Pressure (bar) | Last Test | Next Test |
|-----------|------|----------|-------------------|-----------|-----------|
| SV-001 | Safety valve | PV-001 | | | |
| SV-002 | Safety valve | PV-002 | | | |

**Type codes:** Safety valve (SV) / Rupture disc (BD) / Pressure switch (PS)

---

## 8. Placement and Environmental Risk (AFS 2017:3, 2 Kap. §2-3)

For each vessel, assess whether placement meets regulatory requirements. Mark OK / Not OK / N/A.

| Check | PV-001 | PV-002 | PV-003 |
|-------|--------|--------|--------|
| Accessible for maintenance, repair, and inspection | | | |
| Protected from damage by nearby activities | | | |
| Personnel can shut off equipment if needed | | | |
| Personnel can evacuate if needed | | | |
| Pressure waves would not harm personnel | | | |
| Load-bearing structures not at risk | | | |
| Ambient temperature within design range | | | |
| Not exposed to frost below design minimum | | | |

**Findings:**

| Vessel ID | Issue | Proposed Action | Status |
|-----------|-------|----------------|--------|
| | | | |

---

## 9. Documentation Checklist

| Check | PV-001 | PV-002 | PV-003 |
|-------|--------|--------|--------|
| Registered in inventory | | | |
| Nameplate photo on file | | | |
| EU DoC on file | | | |
| Risk class confirmed | | | |
| Safety devices documented | | | |
| Current certificate on file | | | |

---

## 10. CSV Quick-Start

To generate this inventory automatically, create a CSV file with this header:

```
vessel_id,description,location,manufacturer,year,serial,ps_bar,ts_max_c,volume_l,medium,ce_marked,eu_doc,last_inspection,last_type
PV-001,Main air receiver,Compressor room,Atlas Copco,2015,AC-2015-4521,11,40,1000,compressed air,yes,yes,2024-06-15,external
```

Then run:

```
python3 scripts/jds-classify.py --csv vessels.csv --client "Client Name" --site "Site Name" --doc-no "JDS-LOG-MEC-NNN" --output inventory.md
```

The script will calculate PS x V, determine fluid group, assign risk class, and compute inspection intervals and next due dates automatically.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | YYYY-MM-DD | [Author] | Initial inventory |
