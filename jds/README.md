# JDS — Johansson Documentation System

**Version:** 3.2
**Effective Date:** 2026-03-26
**Owner:** Nils Johansson

---

## What is JDS?

JDS is a complete documentation and quality management system. It defines how documents are created, numbered, reviewed, revised, stored, and retired. Every document — whether it's a field report, a 3D model, a timesheet, or a technical manual — follows the same system.

JDS is designed to be:
- **Reusable** — any organisation can adopt or adapt it
- **Offline-first** — everything lives in the repository; no cloud services required
- **Self-improving** — the system enforces its own maintenance through automated validation and mandatory review cycles
- **Plain-language** — readable by anyone, regardless of technical background

## Why This System Exists

Documentation is often treated as an afterthought. JDS treats it as engineering. When documentation is inconsistent, incomplete, or hard to find, work gets repeated, mistakes recur, and knowledge is lost. JDS prevents this by defining clear rules for every document type and enforcing them automatically.

The goal is simple: **any document can be found in under 60 seconds, and understood by someone who wasn't there when it was written.**

---

## Quick Reference

| What you need | Where to find it |
|---|---|
| How documents are numbered | [Document Numbering Standard](quality-manual/JDS-QMS-001_document-numbering.md) |
| Full quality manual | [Quality Manual](quality-manual/JDS-QMS-000_quality-manual.md) |
| How to create a new document | [Document Creation Procedure](procedures/JDS-PRO-001_document-creation.md) |
| How revisions work | [Revision Control Procedure](procedures/JDS-PRO-002_revision-control.md) |
| How 3D projects are managed | [3D Model Management Procedure](procedures/JDS-PRO-003_3d-model-management.md) |
| How documents are reviewed | [Document Review & Audit Procedure](procedures/JDS-PRO-005_document-review-audit.md) |
| What documents a project needs | [Complete Document Set Standard](procedures/JDS-PRO-006_project-komplekt.md) |
| How documents should look | [Information Design Standard](procedures/JDS-PRO-007_information-design.md) |
| How to handle problems | [Corrective Action Procedure](procedures/JDS-PRO-008_corrective-action.md) |
| How competence is managed | [Competence Management Procedure](procedures/JDS-PRO-009_competence-management.md) |
| How long records are kept | [Document Retention Schedule](quality-manual/JDS-QMS-002_retention-schedule.md) |
| Document templates | [Templates folder](templates/) |
| Master document list | [Document Registry](registry/document-register.md) |
| System change history | [JDS Changelog](CHANGELOG.md) |
| Archived documents | [Archive](archive/) |
| Worked examples | [Examples folder](examples/) |
| One-page cheat sheet | [Quick Reference Card](QUICK-REFERENCE.md) |
| Repository structure rules | [Quality Manual §21](quality-manual/JDS-QMS-000_quality-manual.md) |
| How to improve this system | [Quality Manual §14](quality-manual/JDS-QMS-000_quality-manual.md) |

---

## Document Categories

| Code | Category | What it covers |
|------|----------|----------------|
| **QMS** | Quality Management | Quality manual, policies, system-level standards |
| **PRO** | Procedures | Step-by-step instructions for how things are done |
| **RPT** | Reports | Inspection reports, field reports, technical reports |
| **MAN** | Manuals | User guides, reference documents, technical manuals |
| **DWG** | Drawings & Models | Engineering drawings, 3D model documentation |
| **PRJ** | Project Documents | Project plans, specifications, scope of work |
| **TSH** | Timesheets | Time tracking and labour records |
| **EXP** | Expenses | Expense reports, mileage logs, cost tracking |
| **TMP** | Templates | Blank templates for creating new documents |
| **LOG** | Logs & Records | Equipment logs, maintenance records, training logs |
| **COR** | Correspondence | Formal letters, proposals, quotations |
| **BLG** | Blog Posts | Published articles (tracked and revision-controlled) |

---

## Document Number Format

**Technical documents** include a domain code identifying the engineering discipline:

```
JDS-[CATEGORY]-[DOMAIN]-[NUMBER]
Example: JDS-DWG-MEC-003     → 3rd mechanical drawing
Example: JDS-RPT-ELE-001     → 1st electrical report
```

**System documents** (procedures, templates, quality) omit the domain:

```
JDS-[CATEGORY]-[NUMBER]
Example: JDS-PRO-003          → 3rd procedure
```

With revision: `JDS-DWG-MEC-003 Rev B`

## Domain Codes

| Code | Domain | Typical Work |
|------|--------|-------------|
| **MEC** | Mechanical | Pumps, valves, flanges, brackets |
| **MAR** | Marine | Ship systems, vessel equipment |
| **AUT** | Automation & Controls | PLC, HMI, sensors, wiring |
| **ELE** | Electrical | Power, motors, generators |
| **PIP** | Piping | Pipe systems, fittings, flow diagrams |
| **STR** | Structural | Frames, mounts, enclosures |
| **TST** | Testing & Measurement | Test fixtures, calibration tools |
| **FAB** | Fabrication & Prototyping | 3D printed parts, CNC, workshop |
| **THR** | Thermal & HVAC | Heat exchangers, cooling, ventilation |
| **SFW** | Software | Scripts, tools, applications |
| **GEN** | General | Cross-discipline or general-purpose |

Full details: [Document Numbering Standard](quality-manual/JDS-QMS-001_document-numbering.md)

---

## Core Principles

1. **Every document gets a number.** No exceptions. Even drafts get a number with "DRAFT" status.
2. **Revisions are tracked.** Every change is recorded with who, when, and why.
3. **One source of truth.** The Git repository main branch is the current version. Everything else is an uncontrolled copy.
4. **Write for the next person.** Every document must be understandable by someone who wasn't there when it was written — and who may not share your technical background.
5. **The system improves itself.** Every work session leaves JDS at least as good as it was found. The validator enforces this automatically.
6. **Offline-first.** Everything needed to use this system lives in the repository. No internet required for daily use.

---

## Using JDS Offline

JDS is designed to work without an internet connection. Clone the repository, and you have the complete system:

- All procedures and templates in `jds/`
- All automation tools in `scripts/`
- Run `python3 scripts/jds-validate.py` to check system health
- Run `python3 scripts/md2pdf.py <file.md>` to generate PDFs
- Commit and push when connectivity is restored

See [Quality Manual §22](quality-manual/JDS-QMS-000_quality-manual.md) for the full offline resilience policy.
