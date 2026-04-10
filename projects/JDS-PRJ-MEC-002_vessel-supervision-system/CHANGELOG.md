# Changelog — Vessel Supervision System

> **JDS-PRJ-MEC-002** | Master Change Log

This file logs **every change** to every document in this project. Open this file to see the complete history of what happened, when, and why.

---

## How to Read This Log

Each entry shows:
- **Date** — when the change was made
- **Document** — which document was changed
- **Rev** — what revision it became
- **Author** — who made the change
- **What changed** — plain description of the change

---

## Change Log

| Date | Document | Rev | Author | What Changed |
|------|----------|-----|--------|-------------|
| 2026-04-10 | JDS-PRJ-MEC-002 (README) | A | N. Johansson | Initial release — project overview and structure |
| 2026-04-10 | JDS-MAN-MEC-002 (Supervision Program Manual) | A | N. Johansson | Initial release — complete methodology for building and running supervision programs |
| 2026-04-10 | JDS-LOG-MEC-005 (Program Register) | A | N. Johansson | Initial release — master register for tracking active supervision programs |
| 2026-04-10 | JDS-RPT-MEC-003 (AFS 2017:3 Consolidated) | A | N. Johansson | Initial release — English summary of AFS 2017:3 with all amendments (2019:1, 2020:10, 2022:2) |
| 2026-04-10 | Regulatory Traceability Matrix | A | N. Johansson | Initial release — maps supervision program elements to AFS 2017:3 sections |
| 2026-04-10 | JDS-TMP-LOG-005 (Supervision Program Template) | A | N. Johansson | Initial release — template for creating site-specific supervision programs |
| 2026-04-10 | JDS-TMP-LOG-006 (Supervision Round Record) | A | N. Johansson | Initial release — template for recording supervision round execution |
| 2026-04-10 | JDS-TMP-LOG-007 (Annual Review Template) | A | N. Johansson | Initial release — template for annual supervision program review |
| 2026-04-10 | JDS-TMP-LOG-008 (Inventory Template) | A | N. Johansson | Initial release — equipment inventory template with auto-classification support |
| 2026-04-10 | JDS-LOG-MEC-006 (Example Inventory) | A | N. Johansson | Example: 7 vessels auto-classified by jds-classify.py — Gothenburg Workshop |
| 2026-04-10 | jds-classify.py (Script) | — | N. Johansson | New automation tool — classifies vessels per AFS 2017:3, calculates intervals, generates inventories |
| 2026-04-10 | jds-classify.py --program | — | N. Johansson | Document chain: reads inventory, generates pre-filled supervision program with risk-based check schedules |
| 2026-04-10 | jds-classify.py --round | — | N. Johansson | Document chain: reads program, generates pre-filled supervision round record with per-vessel checks |
| 2026-04-10 | jds-classify.py --review | — | N. Johansson | Document chain: reads program, generates pre-filled annual review with equipment register and metrics |
