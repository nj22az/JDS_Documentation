# Document Numbering Standard

| | |
|---|---|
| **Document No.** | JDS-QMS-001 |
| **Revision** | C |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how every document in JDS is identified with a unique, permanent number. The numbering system tells you three things at a glance:

1. **What type** of document it is (report, drawing, procedure...)
2. **What engineering domain** it belongs to (mechanical, marine, automation...)
3. **Which specific document** it is (sequential number)

## 2. Number Format

### 2.1 Technical Documents (with domain code)

Documents that relate to a specific engineering discipline carry a domain code:

```
JDS - [CAT] - [DOM] - [NNN]
  │      │       │       │
  │      │       │       └── Sequential number (001-999)
  │      │       └────────── Engineering domain (3 letters)
  │      └────────────────── Document category (3 letters)
  └───────────────────────── System prefix (always JDS)
```

**Examples:**
```
JDS-DWG-MEC-001    Drawing, Mechanical, #001 (e.g. a flange adapter)
JDS-RPT-MAR-003    Report, Marine, #003 (e.g. engine room inspection)
JDS-DWG-AUT-002    Drawing, Automation, #002 (e.g. sensor bracket)
JDS-PRJ-FAB-001    Project, Fabrication, #001 (e.g. 3D printing project)
```

### 2.2 System Documents (without domain code)

Documents that govern the system itself (procedures, templates, quality manual) don't need a domain code:

```
JDS - [CAT] - [NNN]
```

**Examples:**
```
JDS-QMS-001    Quality system document
JDS-PRO-003    Procedure
JDS-TMP-005    Template
```

### 2.3 When to Use a Domain Code

| Uses domain code | No domain code |
|---|---|
| DWG (Drawings & Models) | QMS (Quality Management) |
| RPT (Reports) | PRO (Procedures) |
| MAN (Manuals) | TMP (Templates) |
| PRJ (Project Documents) | |
| LOG (Logs & Records) | |
| COR (Correspondence) | |
| BLG (Blog Posts) | |
| TSH (Timesheets) — optional | |
| EXP (Expenses) — optional | |

For timesheets and expenses, the domain code is optional. Use it if the time/expense is project-specific, omit it for general records.

### 2.4 With Revision

Append the revision letter when referencing a specific version:

```
JDS-DWG-MEC-001 Rev B
```

## 3. Engineering Domain Codes

These codes identify which engineering discipline a document belongs to. Just by reading the code, you know the context.

| Code | Domain | Typical Work |
|------|--------|-------------|
| **MEC** | Mechanical | Pumps, valves, flanges, brackets, mechanical assemblies, general mechanical parts |
| **MAR** | Marine | Ship systems, engine room equipment, maritime regulations, vessel maintenance |
| **AUT** | Automation & Controls | PLC, HMI, sensors, control panels, wiring, instrumentation |
| **ELE** | Electrical | Power distribution, wiring, motors, generators, electrical panels |
| **PIP** | Piping | Pipe systems, fittings, P&IDs, flow diagrams |
| **STR** | Structural | Frames, supports, mounts, enclosures, load-bearing structures |
| **TST** | Testing & Measurement | Test fixtures, calibration tools, measurement setups, test reports |
| **FAB** | Fabrication & Prototyping | 3D printed parts, CNC parts, proof-of-concept builds, workshop projects |
| **THR** | Thermal & HVAC | Heat exchangers, cooling systems, ventilation, insulation |
| **SFW** | Software | Software tools, scripts, applications, code documentation |
| **GEN** | General | Cross-discipline or doesn't fit a specific domain |

### 3.1 Choosing the Right Domain

Pick the domain that best describes the **primary subject** of the document. If a report covers both mechanical and electrical work, choose the one that's the main focus. Use GEN only when it truly spans multiple domains equally.

### 3.2 Reading a Full Document Number

```
JDS - DWG - MEC - 005
 │     │     │     │
 │     │     │     └── 5th drawing in the Mechanical domain
 │     │     └──────── Mechanical engineering
 │     └────────────── It's a drawing/model document
 └──────────────────── Johansson Documentation System
```

At a glance: *"This is Nils's 5th mechanical engineering drawing."*

## 4. Document Categories

| Code | Category | Use for |
|------|----------|---------|
| **QMS** | Quality Management System | Quality manual, policies, standards, audit docs |
| **PRO** | Procedures | Step-by-step work procedures and routines |
| **RPT** | Reports | Field service reports, inspection reports, technical reports |
| **MAN** | Manuals | Technical manuals, user guides, reference documents |
| **DWG** | Drawings & Models | Engineering drawings, 3D model specs, BOMs |
| **PRJ** | Project Documents | Project plans, scope of work, specifications |
| **TSH** | Timesheets | Weekly/monthly time records, labour summaries |
| **EXP** | Expenses | Expense reports, travel claims, purchase records |
| **TMP** | Templates | Blank templates for any document type |
| **LOG** | Logs & Records | Equipment logs, maintenance records, calibration records |
| **COR** | Correspondence | Formal letters, proposals, quotations, contracts |
| **BLG** | Blog Posts | Published blog articles, tracked and revision-controlled |

## 5. File Naming Convention

Files on disk follow this pattern:

```
JDS-DWG-MEC-001_flange-adapter-dn50.md
JDS-RPT-MAR-003_engine-room-inspection.md
JDS-PRO-001_document-creation.md
```

**Rules for the short description:**
- Lowercase
- Hyphens instead of spaces
- Keep it brief (3-5 words max)
- No special characters

## 6. Number Assignment Rules

### 6.1 Sequential Numbering

Numbers are assigned sequentially **within each category-domain combination**, starting from 001:

```
JDS-DWG-MEC-001  (first mechanical drawing)
JDS-DWG-MEC-002  (second mechanical drawing)
JDS-DWG-AUT-001  (first automation drawing — separate sequence)
```

### 6.2 Numbers Are Permanent

- A number is assigned **once** and **never reused**, even if the document is retired
- If a document is cancelled before approval, the number is marked as "VOID" in the registry
- This prevents confusion and ensures every reference points to exactly one document

### 6.3 Where to Get the Next Number

Check the [Document Registry](../registry/document-register.md) for the last used number in your category-domain, then use the next one. Update the registry immediately.

## 7. Revision Identifiers

| Identifier | Meaning |
|-----------|---------|
| **DRAFT** | Work in progress, not approved |
| **Rev A** | First approved release |
| **Rev B** | Second approved release |
| **Rev C, D, E...** | Subsequent approved releases |

### 7.1 Revision Rules

- Skip letters **I**, **O**, **Q**, **S**, **X**, **Z** to avoid confusion with numbers or ambiguity
- The revision sequence is: A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T, U, V, W, Y
- If you reach Y, continue with AA, AB, AC...

## 8. Special Numbering

### 8.1 Templates

Templates use the TMP category with a **target category code** instead of a domain code. The target code identifies what type of document the template produces:

```
JDS-TMP-[TARGET]-[NNN]

JDS-TMP-RPT-001    Template for Reports
JDS-TMP-TSH-001    Template for Timesheets
JDS-TMP-LOG-001    Template for Logs & Records
JDS-TMP-DWG-001    Template for Drawings
JDS-TMP-PRJ-001    Template for Project Documents
```

This way you can tell at a glance what kind of document a template creates. Numbering is sequential within each target category (RPT-001, RPT-002, etc.).

### 8.2 Blog Posts

Blog posts carry a JDS number in the front matter:

```yaml
---
layout: post
title: "Article Title"
date: 2026-03-25
jds_no: JDS-BLG-MEC-001
revision: A
---
```

The domain code tells readers which engineering area the post covers.

### 8.3 Project-Specific Documents

For large projects, you may optionally add a project code:

```
JDS-RPT-MEC-015-PROJ01_commissioning-report.md
```

## 9. Quick Decision Guide

| I need to... | Category | Example domain |
|---|---|---|
| Document a 3D model or drawing | DWG | MEC, STR, FAB |
| Write up a field service job | RPT | MAR, TST, MEC |
| Describe how to do something | PRO | *(no domain)* |
| Track my hours | TSH | *(optional domain)* |
| Claim expenses | EXP | *(optional domain)* |
| Write a reference guide | MAN | AUT, ELE, SFW |
| Plan a project | PRJ | MEC, FAB, SFW |
| Record maintenance | LOG | MAR, MEC |
| Write a client letter | COR | GEN, MEC |
| Create a blank form | TMP | *(target category code, e.g. TMP-RPT)* |
| Define a system rule | QMS | *(no domain)* |
| Publish a blog article | BLG | MEC, MAR, SFW |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
| B | 2026-03-25 | Nils Johansson | Renamed JEDS to JDS. Added engineering domain codes. Restructured numbering format. |
| C | 2026-03-25 | Nils Johansson | Templates now use target category codes (JDS-TMP-RPT-001 instead of JDS-TMP-001). |
