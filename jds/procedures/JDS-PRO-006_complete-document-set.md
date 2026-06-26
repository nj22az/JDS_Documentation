# Complete Document Set Standard

| | |
|---|---|
| **Document No.** | JDS-PRO-006 |
| **Revision** | B |
| **Date** | 2026-03-26 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines the **complete document set** — the required collection of documents — for each type of project. No project is considered finished until its document set is complete.

> **Origin:** This concept is adapted from the Russian ESKD (Unified System of Design Documentation) tradition, where every product must have a defined, complete set of documents sufficient for its manufacture, operation, and maintenance. JDS adopts the principle under its own terminology per QMS-000 §15.

## 2. How It Works

1. When starting a project, identify the project type from the table below
2. The document set lists every document that must exist when the project is done
3. Check off each document as it is created
4. Before closing a project, verify the document set is 100% complete
5. If a document is genuinely not applicable, note "N/A — [reason]" in the project README

## 3. Document Set Definitions

### 3.1 Engineering Design Project (DWG)

For any 3D model or engineering drawing project:

| # | Document | JDS Category | Required? |
|---|----------|-------------|-----------|
| 1 | Project README (project card) | — | **Mandatory** |
| 2 | Source files (.blend, .shapr, .py) | — | **Mandatory** |
| 3 | STEP export | — | **Mandatory** |
| 4 | 3MF export | — | **Mandatory** |
| 5 | STL export | — | **Mandatory** |
| 6 | Reference images/datasheets | — | If applicable |
| 7 | Renders or screenshots | — | **Mandatory** (at least 1) |
| 8 | Design rationale (why this design?) | RPT or README | Recommended |
| 9 | BOM / parts list (for assemblies) | LOG | If multi-part |

**Completion check:** All mandatory exports exist, README describes the design, at least one render shows the result.

### 3.2 Engineering Service Project (PRJ)

For field service, maintenance programs, or consulting projects:

| # | Document | JDS Category | Required? |
|---|----------|-------------|-----------|
| 1 | Project README (scope & overview) | — | **Mandatory** |
| 2 | Project CHANGELOG | — | **Mandatory** |
| 3 | Framework / reference documents | MAN, RPT | **Mandatory** |
| 4 | Regulatory references | — | If applicable |
| 5 | Equipment register or inventory | LOG | If equipment-based |
| 6 | Inspection calendar / schedule | LOG | If inspection-based |
| 7 | Client-specific documentation | — | If client work |
| 8 | Lessons learned / A3 summary | RPT | Recommended |

**Completion check:** README describes scope, all framework documents are complete, regulatory basis is documented.

### 3.3 Software Project (SFW)

For software tools, scripts, or applications:

| # | Document | JDS Category | Required? |
|---|----------|-------------|-----------|
| 1 | Project README (what, why, how to use) | — | **Mandatory** |
| 2 | Source code | — | **Mandatory** |
| 3 | Requirements / specification | PRJ or README | Recommended |
| 4 | Installation / setup instructions | MAN or README | **Mandatory** |
| 5 | Test evidence (manual or automated) | RPT | Recommended |
| 6 | Licence file | — | **Mandatory** |
| 7 | CHANGELOG | — | **Mandatory** |

**Completion check:** Code works, README explains usage, installation steps documented, licence present.

### 3.4 Report / Inspection (RPT)

For standalone reports, inspections, or technical analyses:

| # | Document | JDS Category | Required? |
|---|----------|-------------|-----------|
| 1 | Report document (using JDS-TMP-RPT-001) | RPT | **Mandatory** |
| 2 | Supporting evidence (photos, data) | — | If applicable |
| 3 | Equipment register entry (if equipment-related) | LOG | If applicable |
| 4 | Follow-up actions documented | RPT or LOG | If actions required |

**Completion check:** Report complete, evidence attached, actions documented if any.

### 3.5 Blog Post (BLG)

For published blog articles:

| # | Document | JDS Category | Required? |
|---|----------|-------------|-----------|
| 1 | Blog post markdown file | BLG | **Mandatory** |
| 2 | JDS number in front matter | — | **Mandatory** |
| 3 | Registry entry | — | **Mandatory** |
| 4 | Featured image or illustration | — | Recommended |

**Completion check:** Post published, JDS number assigned, registry updated.

## 4. Using the Document Set Checklist

### 4.1 At Project Start

Add a document set checklist to the project README:

```markdown
## Document Set Status

- [x] Project README
- [x] Source files
- [ ] STEP export
- [ ] 3MF export
- [ ] STL export
- [ ] Render / screenshot
- [ ] Design rationale
```

### 4.2 At Project Close

Before marking a project as complete:

1. Review the document set checklist — all mandatory items must be checked
2. For any "N/A" items, document the reason
3. Update the project status in the registry

### 4.3 The Golden Rule

> **A project with an incomplete document set is not a finished project.** It is work-in-progress, regardless of whether the design or code is done.

## 5. Custom Document Sets

For project types not listed above, define a custom document set in the project README at the start. The minimum document set for any JDS project is:

1. Project README
2. At least one deliverable document
3. Registry entry

## 6. Relationship to Other Procedures

| Procedure | Relationship |
|---|---|
| JDS-PRO-001 (Document Creation) | Each document set item is created following PRO-001 |
| JDS-PRO-002 (Revision Control) | Document set items follow the revision process |
| JDS-PRO-003 (3D Model Management) | DWG document set aligns with PRO-003 export requirements |
| JDS-PRO-005 (Review & Audit) | Quarterly audit checks document set completeness |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — document set definitions for DWG, PRJ, SFW, RPT, and BLG project types |
| B | 2026-03-26 | Nils Johansson | Language policy compliance: renamed from "Komplekt" to "Complete Document Set" per QMS-000 §15 |
