# Ongoing Supervision Program (FLT)

Everything you need to perform ongoing supervision of pressurised vessels in one place.

---

## What Is This?

This folder contains the complete documentation package for performing **Ongoing Supervision** (Fortlöpande Tillsyn / FLT) of pressurised vessels under AFS 2017:3. Print these documents, take them to a site, and you have everything needed to build and run a supervision program.

---

## How to Use This Program

### Step 1: Set Up (do once per site)

| # | Action | Document | Print? |
|---|--------|----------|:------:|
| 1 | Read the supervision manual | [Supervision Manual](../03-supervision/JDS-MAN-MEC-002_supervision-program-manual.md) | Optional |
| 2 | Build equipment inventory | [Equipment Inventory Template](../../../jds/templates/logs/JDS-TMP-LOG-008_inventory-template.md) | Yes |
| 3 | Perform risk assessment | [Risk Assessment Template](../../../jds/templates/reports/JDS-TMP-RPT-004_risk-assessment-pressure-vessels.md) | Yes |
| 4 | Create supervision program | [Supervision Program Template](../../../jds/templates/logs/JDS-TMP-LOG-005_supervision-program-template.md) | Yes |
| 5 | Set up lifetime journal | [Lifetime Journal Template](../../../jds/templates/logs/JDS-TMP-LOG-009_lifetime-journal-template.md) | Yes |
| 6 | Build inspection plan | [Inspection Plan Template](../../../jds/templates/logs/JDS-TMP-LOG-004_inspection-plan-template.md) | Yes |

### Step 2: Execute (recurring)

| # | Action | Frequency | Document | Print? |
|---|--------|-----------|----------|:------:|
| 7 | Perform supervision round | Monthly / Quarterly | [Round Record Template](../../../jds/templates/logs/JDS-TMP-LOG-006_supervision-round-template.md) | Yes |
| 8 | Handle findings | As needed | [Corrective Action Procedure](../../../jds/procedures/JDS-PRO-008_corrective-action.md) | No |

### Step 3: Review (annual)

| # | Action | Frequency | Document | Print? |
|---|--------|-----------|----------|:------:|
| 9 | Annual program review | Yearly | [Annual Review Template](../../../jds/templates/logs/JDS-TMP-LOG-007_annual-review-template.md) | Yes |
| 10 | Update inventory and program | Yearly | Repeat steps 2-4 | — |

---

## Document Index

All documents needed for a complete FLT program:

### Templates (blank — fill in per site)

| Doc No. | Title | Purpose |
|---------|-------|---------|
| JDS-TMP-LOG-008 | Equipment Inventory | List all vessels, classify, set inspection intervals |
| JDS-TMP-RPT-004 | Risk Assessment | Probability x Consequence for all vessels |
| JDS-TMP-LOG-005 | Supervision Program | What to check, how often, by whom |
| JDS-TMP-LOG-006 | Supervision Round Record | Record each round: checks, readings, findings |
| JDS-TMP-LOG-007 | Annual Review | Yearly effectiveness review |
| JDS-TMP-LOG-009 | Lifetime Journal | Track wall thickness, corrosion, fatigue, creep |
| JDS-TMP-LOG-004 | Inspection Plan | Schedule formal inspections (accredited body) |
| JDS-TMP-RPT-003 | Inspection Report | Document formal inspection results |

### Procedures and Manuals

| Doc No. | Title | Purpose |
|---------|-------|---------|
| JDS-PRO-010 | Ongoing Maintenance Procedure | Master procedure — the full workflow |
| JDS-MAN-MEC-002 | Supervision Program Manual | How to build and run a supervision program |
| JDS-PRO-011 | Inspection Planning | How to schedule formal inspections |
| JDS-PRO-008 | Corrective Action | How to handle findings |
| JDS-PRO-009 | Competence Management | Personnel qualification requirements |
| JDS-MAN-MEC-001 | Documentation Guide | What records to keep and why |

### Regulatory Reference (Sweden)

| Doc No. | Title | Purpose |
|---------|-------|---------|
| JDS-RPT-MEC-003 | AFS 2017:3 Consolidated | English summary of the regulation |
| — | Regulatory Traceability Matrix | Maps JDS procedures to AFS sections |
| — | AFS 2017:3 (original PDF) | Official regulatory text |
| — | AFS 2019:1, 2020:10, 2022:2 (PDFs) | Amendment texts |

### Examples (Gothenburg Workshop)

| Doc No. | Title | Shows |
|---------|-------|-------|
| JDS-LOG-MEC-006 | Example Inventory | 7 vessels, auto-classified |
| JDS-LOG-MEC-007 | Example Program | Complete supervision program |
| JDS-LOG-MEC-008 | Example Lifetime Journal | Degradation tracking for 4 vessels |
| JDS-LOG-MEC-009 | Example Round Record | Monthly round execution |
| JDS-LOG-MEC-010 | Example Annual Review | Yearly effectiveness review |

### Automation

| Tool | Command | Purpose |
|------|---------|---------|
| Classify vessels | `python3 scripts/jds-classify.py --csv vessels.csv` | Auto-classify and generate inventory |
| Generate program | `python3 scripts/jds-classify.py --program --from inventory.md` | Generate supervision program from inventory |
| Generate round | `python3 scripts/jds-classify.py --round --from program.md` | Generate round record from program |
| Generate review | `python3 scripts/jds-classify.py --review --from program.md` | Generate annual review from program |
| Print to PDF | `python3 scripts/md2pdf.py <document.md>` | Generate JDS-compliant PDF |

---

## The 6 Mandatory Checks (AFS 2017:3, 2 Kap. §6)

Every supervision program must address at minimum:

1. Equipment **functions satisfactorily**
2. **No leaks** have occurred
3. Equipment not subjected to **harmful external or internal impact**
4. **No other faults or deviations** have occurred
5. Equipment, valves, emergency stops are **correctly marked**
6. **Prescribed inspections** have been carried out

These six points are the legal baseline. The supervision program template (TMP-LOG-005) builds on these with additional checks for safety devices, lifetime tracking, and site-specific risks.

---

## Quick Start (New Site)

```
1. Copy example-vessels.csv, fill in your data
2. python3 scripts/jds-classify.py --csv your-vessels.csv --output inventory.md
3. python3 scripts/jds-classify.py --program --from inventory.md
4. Print the supervision program + round record template
5. Go to the site, perform the first round
6. File the completed round record
```
