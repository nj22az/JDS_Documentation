# JDS — Johansson Documentation System

**Version:** 2.7
**Effective Date:** 2026-03-25
**Owner:** Nils Johansson

---

## What is JDS?

JDS is the in-house documentation and quality management system for all engineering work produced under The Office of Nils Johansson. It defines how documents are created, numbered, reviewed, revised, stored, and retired.

Every document — whether it's a field service report, a 3D model drawing, a timesheet, or a technical manual — follows the same system. This ensures consistency, traceability, and professionalism across all work.

---

## Quick Reference

| What you need | Where to find it |
|---|---|
| How documents are numbered | [Document Numbering Standard](quality-manual/JDS-QMS-001_document-numbering.md) |
| Full quality manual | [Quality Manual](quality-manual/JDS-QMS-000_quality-manual.md) |
| How to create a new document | [Document Creation Procedure](procedures/JDS-PRO-001_document-creation.md) |
| How revisions work | [Revision Control Procedure](procedures/JDS-PRO-002_revision-control.md) |
| How 3D projects are managed | [3D Model Management Procedure](procedures/JDS-PRO-003_3d-model-management.md) |
| How documents are reviewed & audited | [Document Review & Audit Procedure](procedures/JDS-PRO-005_document-review-audit.md) |
| What documents a project needs | [Project Komplekt Standard](procedures/JDS-PRO-006_project-komplekt.md) |
| How documents should look | [Information Design Standard](procedures/JDS-PRO-007_information-design.md) |
| How to handle nonconformances | [Corrective Action Procedure](procedures/JDS-PRO-008_corrective-action.md) |
| How competence is managed | [Competence Management Procedure](procedures/JDS-PRO-009_competence-management.md) |
| How long records are kept | [Document Retention Schedule](quality-manual/JDS-QMS-002_retention-schedule.md) |
| Document templates | [Templates folder](templates/) |
| Master document list | [Document Registry](registry/document-register.md) |
| System change history | [JDS Changelog](CHANGELOG.md) |
| Archived documents | [Archive](archive/) |
| Worked examples | [Examples folder](examples/) |

---

## Document Categories at a Glance

| Code | Category | Examples |
|------|----------|----------|
| **QMS** | Quality Management | Quality manual, policies, system docs |
| **PRO** | Procedures | How-to procedures, workflows, routines |
| **RPT** | Reports | Field service reports, inspection reports, technical reports |
| **MAN** | Manuals | Technical manuals, user guides, reference docs |
| **DWG** | Drawings & Models | Engineering drawings, 3D model documentation |
| **PRJ** | Project Documents | Project plans, specifications, scope of work |
| **TSH** | Timesheets | Time tracking and labour records |
| **EXP** | Expenses | Expense reports, receipts, cost tracking |
| **TMP** | Templates | Blank templates for all document types |
| **LOG** | Logs & Records | Equipment logs, maintenance records, training logs |
| **COR** | Correspondence | Formal letters, proposals, quotations |
| **BLG** | Blog Posts | Published blog articles (tracked and revision-controlled) |

---

## Document Number Format

Technical documents carry an engineering domain code so you can identify the discipline at a glance:

```
JDS-[CATEGORY]-[DOMAIN]-[NUMBER]
Example: JDS-DWG-MEC-003     (3rd mechanical drawing)
Example: JDS-RPT-MAR-001     (1st marine report)
```

System documents (procedures, templates, quality) omit the domain:

```
JDS-[CATEGORY]-[NUMBER]
Example: JDS-PRO-003
```

With revision: `JDS-DWG-MEC-003 Rev B`

## Engineering Domain Codes

| Code | Domain | Typical Work |
|------|--------|-------------|
| **MEC** | Mechanical | Pumps, valves, flanges, brackets |
| **MAR** | Marine | Ship systems, engine room equipment |
| **AUT** | Automation & Controls | PLC, HMI, sensors, wiring |
| **ELE** | Electrical | Power, motors, generators |
| **PIP** | Piping | Pipe systems, fittings, P&IDs |
| **STR** | Structural | Frames, mounts, enclosures |
| **TST** | Testing & Measurement | Test fixtures, calibration tools |
| **FAB** | Fabrication & Prototyping | 3D printed parts, CNC, workshop |
| **THR** | Thermal & HVAC | Heat exchangers, cooling, ventilation |
| **SFW** | Software | Scripts, tools, applications |
| **GEN** | General | Cross-discipline |

Full details: [Document Numbering Standard](quality-manual/JDS-QMS-001_document-numbering.md)

---

## Core Principles

1. **Every document gets a number.** No exceptions. Even drafts get a number with "DRAFT" status.
2. **Revisions are tracked.** Every change is recorded with who, when, and why.
3. **One source of truth.** The version in this repository is the current version. Period.
4. **Keep it simple.** The system serves the work, not the other way around. If a form feels unnecessary, question it.
5. **Write for the next person.** Every document should be understandable by someone who wasn't there when it was written.
