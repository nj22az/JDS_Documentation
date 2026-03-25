# Johansson Documentation System (JDS)

**The Office of Nils Johansson** — Marine, Mechanical & Industrial Engineering

**Version 3.1** | Effective 2026-03-25 | Owner: Nils Johansson

---

> **One repository. One system. One source of truth.**

This repository **is** the Johansson Documentation System. Every project, document, drawing, blog post, and record lives here under one unified system. JDS governs how work is created, numbered, revised, and found.

---

## I need to...

| Task | Go here |
|------|---------|
| **Create a new document** | [Document Creation Procedure](jds/procedures/JDS-PRO-001_document-creation.md) + [Templates](jds/templates/) |
| **Start an engineering project** | [Project Komplekt Standard](jds/procedures/JDS-PRO-006_project-komplekt.md) + [Project Template](jds/templates/projects/JDS-TMP-PRJ-001_project-template.md) |
| **Write a report** | [Report Template](jds/templates/reports/JDS-TMP-RPT-001_report-template.md) + [Examples](jds/examples/) |
| **Submit a timesheet** | `python3 scripts/generate-office-docs.py timesheet` |
| **Submit expenses or mileage** | `python3 scripts/generate-office-docs.py expense` or `mileage` |
| **Send a formal letter** | [Letter Template](jds/templates/correspondence/JDS-TMP-COR-001_cold-letter-template.md) + `python3 scripts/md2letter.py` |
| **Add a 3D model** | [3D Model Management](jds/procedures/JDS-PRO-003_3d-model-management.md) |
| **Write a blog post** | [Blog Post Template](jds/templates/blog-posts/JDS-TMP-BLG-001_blog-post-template.md) |
| **Generate a PDF** | `python3 scripts/md2pdf.py <file.md>` or `python3 scripts/office2pdf.py <file.xlsx>` |
| **Run a system audit** | `python3 scripts/jds-validate.py` |
| **Find an existing document** | [Master Document Register](jds/registry/document-register.md) |
| **Look up the numbering system** | [Numbering Standard](jds/quality-manual/JDS-QMS-001_document-numbering.md) |
| **Read the full quality manual** | [Quality Manual](jds/quality-manual/JDS-QMS-000_quality-manual.md) |
| **Quick reference (cheat sheet)** | [JDS Quick Reference](jds/QUICK-REFERENCE.md) |

---

## Core Principles

1. **Every document gets a number.** No exceptions — even drafts.
2. **Revisions are tracked.** Every change records who, when, and why.
3. **Git is the controlled copy.** The version in this repository is the current version. Period.
4. **Write for the next person.** Every document must be understandable by someone who wasn't there.
5. **Keep it simple.** The system serves the work, not the other way around.

---

## Repository Map

### System Governance

| Folder | Purpose |
|--------|---------|
| [`jds/`](jds/) | Quality manual, procedures, templates, examples, registry, brand assets |
| [`scripts/`](scripts/) | Automation tools — PDF generation, validation, office documents |

### Work Areas

| Folder | Purpose |
|--------|---------|
| [`projects/`](projects/) | Engineering projects (`JDS-PRJ-[DOM]-NNN`) |
| [`3d-modeling/`](3d-modeling/) | 3D CAD projects (`JDS-DWG-[DOM]-NNN`) |
| [`blog/`](blog/) | Engineering blog — [Live site](https://nj22az.github.io/theofficeofnilsjohansson/) |
| [`documents/`](documents/) | Personal documents (CV, cover letters, notes) |
| [`collections/`](collections/) | Personal collections (JDS principles, not JDS-numbered) |
| [`archive/`](archive/) | Archived past work |

---

## Active Work

| JDS No. | Title | Status |
|---------|-------|--------|
| [JDS-PRJ-MEC-001](projects/JDS-PRJ-MEC-001_pressure-vessel-maintenance/) | Pressure Vessel Ongoing Maintenance Program | Active |

### Published Blog

| JDS No. | Title |
|---------|-------|
| [JDS-BLG-001](blog/_posts/2026-03-25-why-i-started-this-blog.md) | Why I Started This Blog |
| [JDS-BLG-002](blog/_posts/2026-03-25-what-the-engine-room-teaches-you.md) | What the Engine Room Teaches You About Problem-Solving |
| [JDS-BLG-003](blog/_posts/2026-03-25-why-i-chose-build123d.md) | Why I Chose build123d for Parametric CAD |

---

*For the full system reference, see [jds/README.md](jds/README.md). For the quick cheat sheet, see [Quick Reference](jds/QUICK-REFERENCE.md).*
