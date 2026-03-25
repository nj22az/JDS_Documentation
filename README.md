# Johansson Documentation System (JDS)

**The Office of Nils Johansson** — Marine · Mechanical · Industrial Engineering

**JDS Version:** 2.9 | **Effective Date:** 2026-03-25 | **Owner:** Nils Johansson

---

This repository **is** the Johansson Documentation System. Every project, document, drawing, blog post, and record lives here under one unified system. JDS governs how work is created, numbered, revised, and found.

> **One repository. One system. One source of truth.**

---

## Find What You Need

| What you're looking for | Where it lives |
|---|---|
| **Active engineering projects** | [`projects/`](projects/) |
| **3D models & drawings** | [`3d-modeling/`](3d-modeling/) |
| **Engineering blog** | [`blog/`](blog/) — [Live site](https://nj22az.github.io/theofficeofnilsjohansson/) |
| **Document templates** | [`jds/templates/`](jds/templates/) |
| **Worked examples** | [`jds/examples/`](jds/examples/) |
| **Master document register** | [`jds/registry/document-register.md`](jds/registry/document-register.md) |
| **Quality manual & procedures** | [`jds/`](jds/) |
| **Personal documents (CV, etc.)** | [`documents/`](documents/) |
| **Collections** | [`collections/`](collections/) |
| **Archived work** | [`archive/`](archive/) |

---

## Repository Structure

```
theofficeofnilsjohansson/          ← This IS the JDS
│
├── jds/                            ← System governance
│   ├── quality-manual/             QMS-000 Quality Manual, QMS-001 Numbering, QMS-002 Retention
│   ├── procedures/                 PRO-001 through PRO-009 (creation, revision, 3D, audit, design…)
│   ├── templates/                  Blank templates for every document type
│   ├── examples/                   Worked examples (reports, inventories, letters)
│   ├── registry/                   Master document register + corrective action log
│   ├── assets/                     Logo, fonts
│   └── archive/                    Retired/superseded system documents
│
├── projects/                       ← Engineering project work
│   └── JDS-PRJ-MEC-001_pressure-vessel-maintenance/
│       ├── 01-framework/           Universal building blocks
│       ├── 02-regulations/         Country-specific (AFS 2017:3, PED)
│       └── 03-active-programs/     Active client inventories
│
├── 3d-modeling/                    ← 3D CAD projects (JDS-DWG-[DOM]-NNN)
│   └── _shared-references/         Shared datasheets, standards
│
├── blog/                           ← Jekyll engineering blog (GitHub Pages)
│   └── _posts/                     JDS-BLG tracked articles
│
├── documents/                      ← Personal documents (CV, notes)
│
├── collections/                    ← Personal collections
│   └── rom-archive/                Classical video game preservation
│
├── software-projects/              ← Software development projects
│
├── scripts/                        ← JDS automation tools
│   ├── md2pdf.py                   PDF generator (JDS-PRO-007 compliant)
│   ├── md2letter.py                Old-world stationery letter generator
│   └── jds-validate.py             Automated 5S audit (70+ checks)
│
├── archive/                        ← Archived past projects
│
└── safe-to-delete/                 ← Temporary review files
```

---

## How JDS Works

### Document Numbers

Every document gets a unique JDS number. No exceptions.

```
Technical:  JDS-[CAT]-[DOM]-[NNN]    → JDS-DWG-MEC-003 (3rd mechanical drawing)
System:     JDS-[CAT]-[NNN]          → JDS-PRO-007 (Information Design Standard)
With rev:   JDS-RPT-MAR-001 Rev B
```

### Categories

| Code | Category | What goes here |
|------|----------|---------------|
| **QMS** | Quality Management | Quality manual, policies |
| **PRO** | Procedures | How-to procedures, routines |
| **RPT** | Reports | Inspection reports, technical reports |
| **MAN** | Manuals | Technical manuals, guides |
| **DWG** | Drawings & Models | 3D models, engineering drawings |
| **PRJ** | Project Documents | Project plans, scope of work |
| **LOG** | Logs & Records | Equipment logs, maintenance records |
| **COR** | Correspondence | Formal letters, proposals |
| **BLG** | Blog Posts | Published articles |
| **TSH** | Timesheets | Time tracking |
| **EXP** | Expenses | Expense reports |
| **TMP** | Templates | Blank templates |

### Engineering Domains

| Code | Domain | Code | Domain |
|------|--------|------|--------|
| **MEC** | Mechanical | **ELE** | Electrical |
| **MAR** | Marine | **PIP** | Piping |
| **AUT** | Automation & Controls | **STR** | Structural |
| **TST** | Testing & Measurement | **THR** | Thermal & HVAC |
| **FAB** | Fabrication & Prototyping | **SFW** | Software |
| **GEN** | General | | |

---

## Core Principles

1. **Every document gets a number.** No exceptions — even drafts.
2. **Revisions are tracked.** Every change records who, when, and why.
3. **Git is the controlled copy.** The version in this repo is the current version. Period.
4. **Write for the next person.** Every document must be understandable by someone who wasn't there.
5. **Keep it simple.** The system serves the work, not the other way around.

---

## Quick Start

| Task | How |
|------|-----|
| Create a new document | Follow [JDS-PRO-001](jds/procedures/JDS-PRO-001_document-creation.md) and register in [document-register.md](jds/registry/document-register.md) |
| Start a new project | Use [JDS-TMP-PRJ-001](jds/templates/projects/JDS-TMP-PRJ-001_project-template.md), create folder in `projects/` |
| Add a 3D model | Follow [JDS-PRO-003](jds/procedures/JDS-PRO-003_3d-model-management.md), create folder in `3d-modeling/` |
| Write a blog post | Use [JDS-TMP-BLG-001](jds/templates/blog-posts/JDS-TMP-BLG-001_blog-post-template.md), save in `blog/_posts/` |
| Write a letter | Use [JDS-TMP-COR-001](jds/templates/correspondence/JDS-TMP-COR-001_cold-letter-template.md) |
| Run a system audit | `python3 scripts/jds-validate.py` |
| Generate a PDF | `python3 scripts/md2pdf.py <input.md> [output.pdf]` |

---

## Current Projects

| JDS No. | Title | Status |
|---------|-------|--------|
| [JDS-PRJ-MEC-001](projects/JDS-PRJ-MEC-001_pressure-vessel-maintenance/) | Pressure Vessel Ongoing Maintenance Program | Active |

## Published Blog

| JDS No. | Title |
|---------|-------|
| [JDS-BLG-001](blog/_posts/2026-03-25-why-i-started-this-blog.md) | Why I Started This Blog |
| [JDS-BLG-002](blog/_posts/2026-03-25-what-the-engine-room-teaches-you.md) | What the Engine Room Teaches You About Problem-Solving |
| [JDS-BLG-003](blog/_posts/2026-03-25-why-i-chose-build123d.md) | Why I Chose build123d for Parametric CAD |

---

*For the full system reference, see [jds/README.md](jds/README.md). For system governance details, see the [Quality Manual](jds/quality-manual/JDS-QMS-000_quality-manual.md).*
