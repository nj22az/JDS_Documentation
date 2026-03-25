# Document Numbering Standard

| | |
|---|---|
| **Document No.** | JEDS-QMS-001 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This standard defines how every document in JEDS is identified with a unique, permanent number. Consistent numbering makes documents easy to find, reference, and track.

## 2. Number Format

```
JEDS - [CAT] - [NNN]
  │      │       │
  │      │       └── Sequential number (001-999)
  │      └────────── Category code (3 letters)
  └───────────────── System prefix (always JEDS)
```

**Example:** `JEDS-RPT-003` = the 3rd report in the system.

### 2.1 With Revision

When referencing a specific revision, append the revision letter:

```
JEDS-RPT-003 Rev B
```

### 2.2 File Naming Convention

Files on disk follow this pattern:

```
JEDS-RPT-003_short-description.md
JEDS-RPT-003_short-description.pdf
```

**Rules for the short description:**
- Lowercase
- Hyphens instead of spaces
- Keep it brief (3-5 words max)
- No special characters

**Examples:**
```
JEDS-RPT-001_site-inspection-malmo.md
JEDS-TSH-012_march-2026-timesheet.md
JEDS-DWG-005_flange-adapter-dn50.md
JEDS-PRO-001_document-creation.md
```

## 3. Category Codes

| Code | Category | Use for |
|------|----------|---------|
| **QMS** | Quality Management System | Quality manual, policies, standards, audit docs |
| **PRO** | Procedures | Step-by-step work procedures and routines |
| **RPT** | Reports | Field service reports, inspection reports, technical reports, management reviews |
| **MAN** | Manuals | Technical manuals, user guides, reference documents |
| **DWG** | Drawings & Models | Engineering drawings, 3D model specs, BOMs |
| **PRJ** | Project Documents | Project plans, scope of work, specifications, meeting notes |
| **TSH** | Timesheets | Weekly/monthly time records, labour summaries |
| **EXP** | Expenses | Expense reports, travel claims, purchase records |
| **TMP** | Templates | Blank templates for any document type |
| **LOG** | Logs & Records | Equipment logs, maintenance records, calibration records, training logs |
| **COR** | Correspondence | Formal letters, proposals, quotations, contracts |
| **BLG** | Blog Posts | Published blog articles, tracked and revision-controlled |

## 4. Number Assignment Rules

### 4.1 Sequential Numbering

Numbers are assigned sequentially within each category, starting from 001:

```
JEDS-RPT-001  (first report)
JEDS-RPT-002  (second report)
JEDS-RPT-003  (third report)
```

### 4.2 Numbers Are Permanent

- A number is assigned **once** and **never reused**, even if the document is retired
- If a document is cancelled before approval, the number is marked as "VOID" in the registry
- This prevents confusion and ensures every reference points to exactly one document

### 4.3 Where to Get the Next Number

Check the [Document Registry](../registry/document-register.md) for the last used number in your category, then use the next one. Update the registry immediately when assigning a new number.

## 5. Revision Identifiers

| Identifier | Meaning |
|-----------|---------|
| **DRAFT** | Work in progress, not approved |
| **Rev A** | First approved release |
| **Rev B** | Second approved release |
| **Rev C** | Third approved release |
| *...and so on* | |

### 5.1 Revision Rules

- Skip letters **I**, **O**, **Q**, **S**, **X**, **Z** to avoid confusion with numbers (1, 0) or ambiguity
- The revision sequence is: A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T, U, V, W, Y
- If you reach Y, continue with AA, AB, AC... (this is unlikely for most documents)

## 6. Special Numbering

### 6.1 Templates

Templates use the TMP category with a suffix indicating what type of document they're a template for:

```
JEDS-TMP-001_report-template.md
JEDS-TMP-002_timesheet-template.md
JEDS-TMP-003_expense-template.md
```

### 6.2 Blog Posts

Blog posts live in `blog/_posts/` and follow Jekyll's naming convention for the filename, but carry a JEDS number in the front matter and as a visible header on the published page:

```yaml
---
layout: post
title: "Article Title"
date: 2026-03-25
jeds_no: JEDS-BLG-001
revision: A
---
```

The JEDS number links the published article back to the registry so every post is traceable and revision-controlled like any other document.

### 6.3 Project-Specific Documents

For large projects, you may optionally add a project code after the document number:

```
JEDS-RPT-015-PROJ01_commissioning-report.md
```

This is optional and should only be used when a project generates many documents that benefit from grouping.

## 7. Quick Decision Guide

| I need to... | Category |
|---|---|
| Write up what happened on a job | RPT (Report) |
| Describe how to do something step by step | PRO (Procedure) |
| Track my hours | TSH (Timesheet) |
| Claim expenses | EXP (Expense) |
| Document a design/model | DWG (Drawing) |
| Write a reference guide | MAN (Manual) |
| Plan a project | PRJ (Project) |
| Record equipment maintenance | LOG (Log) |
| Write a client letter or quote | COR (Correspondence) |
| Create a blank form | TMP (Template) |
| Define a system rule | QMS (Quality) |
| Publish a blog article | BLG (Blog Post) |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
