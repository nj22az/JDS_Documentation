# JDS Document Studio — Local Document Creator

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-002 |
| **Revision** | D |
| **Date** | 2026-06-26 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A local web app that creates JDS-compliant documents. Pick a template, give it a
title and category, and Studio reserves the next free JDS number, fills the
metadata block, writes the file into the repository, and adds it to the master
register — then renders the PDF and runs the audit, all from one page.

It is a **thin UI over the existing JDS engine**. PDF rendering, validation, and
Excel generation are NOT reimplemented here — Studio shells out to the scripts in
`scripts/` (`md2pdf.py`, `jds-validate.py`, `generate-office-docs.py`), which stay
the single source of truth. **Git remains the controlled copy.**

> **Doc says:** I do the bookkeeping you'd otherwise do by hand — numbering,
> metadata, registry rows — so a new document is correct the moment it's born.

## Why Web, Not Native (Swift)

The whole document engine already exists in Python. A web app reuses it directly;
a native app would have to shell out to Python anyway or duplicate the entire
pipeline. Web also runs anywhere and keeps one codebase. See the project
CHANGELOG for the full rationale.

## Quick Start

| Step | Command |
|------|---------|
| Install + run (macOS) | Double-click `run.command` |
| Install + run (any OS) | `pip3 install -r requirements.txt` then `python3 -m studio.server` |
| Open | http://127.0.0.1:8731 |
| Run tests | `python3 tests/test_core.py` |

The server finds the repository root automatically (or set `JDS_REPO_ROOT`).

## What It Does

| Action | Behind the scenes |
|--------|-------------------|
| **Next number** | Scans the register **and** the files on disk so a number is never reused |
| **Create document** | Instantiates the chosen template, writes the `.md`, appends one registry row under the right section |
| **Generate PDF** | Calls `scripts/md2pdf.py` (full PRO-007 styling) |
| **Validate** | Calls `scripts/jds-validate.py` and shows the result, Doc's closing line included |
| **Suggest folder** | Pre-fills the target folder where Studio is confident (QMS, PRO, TMP); editable, never guesses wrong |
| **Office documents** | Generates timesheet / expense / mileage Excel workbooks via `scripts/generate-office-docs.py` |

## Architecture

```
web/ (browser UI)  ──HTTP──►  studio/server.py  (FastAPI, thin)
                                     │ delegates to
                                     ▼
        studio/creator.py ── numbering.py · registry.py · templates.py   (pure core, unit-tested)
                                     │ shells out to
                                     ▼
        studio/engine.py ──►  scripts/md2pdf.py · jds-validate.py · generate-office-docs.py
```

## Project Structure

| Path | Purpose |
|------|---------|
| `studio/config.py` | All constants & paths (no hardcoded values elsewhere) |
| `studio/numbering.py` | Next-free JDS number resolution (prefix-anchored) |
| `studio/registry.py` | Parse register, append one row under the correct section |
| `studio/templates.py` | Discover templates, fill title + metadata |
| `studio/creator.py` | Orchestrates create: number → instantiate → write → register |
| `studio/placement.py` | Suggests the target folder by category (confident defaults only) |
| `studio/engine.py` | Subprocess wrappers around the JDS scripts |
| `studio/server.py` | FastAPI routes (HTTP ⇄ core) |
| `web/` | `index.html`, `style.css`, `app.js` (PRO-007-styled UI) |
| `tests/test_core.py` | 8 unit + integration tests for the core |

## HTTP API

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/api/taxonomy` | Categories, domains, statuses for the form |
| GET | `/api/templates` | Available templates |
| GET | `/api/next-number?category=&domain=&template_type=` | Preview the next number + suggested folder |
| GET | `/api/registry` | Parsed register entries |
| POST | `/api/documents` | Create a numbered, registered document |
| POST | `/api/validate?quick=` | Run the audit |
| POST | `/api/pdf` | Render a document to PDF |
| POST | `/api/office?kind=` | Generate a timesheet / expense / mileage workbook |

## Standards Compliance

**JDS-PRO-004 (Code).** Built to the software code standard from the first line:
constants live in `config.py`; every module is small and single-purpose (largest
is well under the 500-line limit); no dead code; clear names throughout; the core
is unit-tested and side-effect-free except the two writes in
`creator.create_document`.

**JDS-PRO-012 (Interface), incl. §12 Apple HIG.** This app is the reference
implementation of the Interface Design Standard: JDS palette and **system
typography** (§6–§7, §12), **adaptive light & dark appearance**, **44pt hit
targets**, status never by colour alone, WCAG-AA contrast with **visible focus
indicators** and **reduced-motion** support (§8), invalid actions **prevented**
rather than just reported — empty title, bad revision letter, and out-of-repo
paths are rejected before any write (§5.3). Section headers carry **SF
Symbol-equivalent inline-SVG icons** paired with their labels per the §12.4
mapping (decorative-redundant, `aria-hidden`). No safety-critical/HMI surfaces
here, so the Doc Guide Note is permitted (§11) and HIG materials are fine (§12.3).

## Status & Limitations (Rev B)

- Creates documents from templates, numbers, registers, renders PDF, validates,
  generates office workbooks, and suggests the target folder by category.
- Folder suggestions cover the confident cases (QMS, PRO, TMP); for other
  categories the field is left for the user to fill.
- Editing existing documents and automated revision bumps remain out of scope
  (planned for a later revision).
