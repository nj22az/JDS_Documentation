# Equipment Inventory — [Site Name]

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

---

## 1. Purpose

This register is the master inventory of all pressurised vessels at [site name]. It provides the complete equipment record required for regulatory compliance and serves as the foundation for the supervision program.

> **Auto-classification available:** Run `python3 scripts/jds-classify.py --csv [data.csv]` to generate this inventory automatically from a CSV file. The script calculates classification, risk class, and inspection intervals per AFS 2017:3.

---

## 2. Classification Summary

| Risk Class | Count | Inspection Regime |
|-----------|-------|-------------------|
| **Class A** | | Accredited body: ext. 24 mo, int. 72 mo, press. test 144 mo |
| **Class B** | | Accredited (int.) / own (ext.): ext. 36 mo, int. 72 mo |
| **Below B** | | Own inspection: ext. 72 mo |
| **Simple PV** | | No mandatory periodic inspection |
| **Not classified** | | Below regulatory threshold |
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
> **Group 2 (non-dangerous):** Class A if PS x V > 10,000 | Class B if > 1,000 | Below B if > 200 | Simple PV if > 50
>
> **Group 1 (dangerous):** Class A if PS x V > 3,000 | Class B if > 200 | Simple PV if > 50

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

**Interval reference:**

| Risk Class | External | Internal | Pressure Test |
|-----------|----------|----------|--------------|
| Class A | 24 months | 72 months | 144 months |
| Class B | 36 months | 72 months | — |
| Below B | 72 months | — | — |
| Simple PV | — | — | — |

---

## 7. Safety Devices

| Device ID | Type | Protects | Set Pressure (bar) | Last Test | Next Test |
|-----------|------|----------|-------------------|-----------|-----------|
| SV-001 | Safety valve | PV-001 | | | |
| SV-002 | Safety valve | PV-002 | | | |

**Type codes:** Safety valve (SV) / Rupture disc (BD) / Pressure switch (PS)

---

## 8. Documentation Checklist

| Check | PV-001 | PV-002 | PV-003 |
|-------|--------|--------|--------|
| Registered in inventory | | | |
| Nameplate photo on file | | | |
| EU DoC on file | | | |
| Risk class confirmed | | | |
| Safety devices documented | | | |
| Current certificate on file | | | |

---

## 9. CSV Quick-Start

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
| DRAFT | YYYY-MM-DD | [Author] | Initial inventory |
