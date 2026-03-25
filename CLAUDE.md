# Project Instructions for Claude

## Repository Purpose
Personal workspace for Nils Johansson's project files, including 3D modeling and software projects.

## Structure
- `jds/` - Johansson Documentation System (quality manual, procedures, templates, registry)
- `blog/` - Jekyll engineering blog (GitHub Pages)
- `3d-modeling/` - 3D modeling projects, each in its own JDS-DWG-[DOM]-NNN folder (Blender, Shapr3D, build123d)
- `projects/` - Engineering projects, each in its own JDS-PRJ-[DOM]-NNN folder
- `software-projects/` - Software development projects
- `scripts/` - JDS tooling (md2pdf.py for document PDFs, md2letter.py for correspondence)
- `collections/` - Personal collections (ROM archive, etc.) — uses JDS principles but not JDS document numbers
- `documents/` - CV, cover letters, notes
- `archive/` - Archived past projects (e.g., previous website)

## JDS Documentation System
- Technical documents: `JDS-[CAT]-[DOM]-[NNN]` (e.g., JDS-DWG-MEC-003)
- System documents: `JDS-[CAT]-[NNN]` (e.g., JDS-PRO-001)
- Categories: QMS, PRO, RPT, MAN, DWG, PRJ, TSH, EXP, TMP, LOG, COR, BLG
- Domain codes: MEC, MAR, AUT, ELE, PIP, STR, TST, FAB, THR, SFW, GEN
- Always use the appropriate template from `jds/templates/`
- Always register new documents in `jds/registry/document-register.md`
- Revisions follow letter sequence: A, B, C, D... (skip I, O, Q, S, X, Z)
- Blog posts are tracked as BLG category with domain code (e.g., JDS-BLG-MEC-001)
- See `jds/README.md` for full documentation system reference

## 3D Modeling Projects
- Each 3D project gets a DWG number with domain: `3d-modeling/JDS-DWG-MEC-001_name/`
- Standard subfolders: `source/`, `exports/`, `references/`, `renders/`
- Mandatory exports: STEP + 3MF + STL (always all three)
- Every project folder has a README.md project card
- See JDS-PRO-003 for full procedure

## Engineering Projects
- Each project gets a PRJ number with domain: `projects/JDS-PRJ-MEC-001_name/`
- Every project has a README.md and CHANGELOG.md (master change log)
- All document changes within a project are logged in CHANGELOG.md
- Every document has a status block at the top: Doc No | Rev | CURRENT/SUPERSEDED | Date | Author

## Guidelines
- Keep files organized in the appropriate directories
- Use descriptive names for project folders
- Each software project should have its own subfolder under `software-projects/`

## PDF Generation (JDS-PRO-007 Compliance)

All PDFs exported from JDS documents MUST follow JDS-PRO-007 (Information Design Standard). Use `/pdf <filepath>` to generate compliant PDFs.

### Mandatory PDF Requirements
- **Documents**: `python3 scripts/md2pdf.py <input.md> [output.pdf]`
- **Letters**: `python3 scripts/md2letter.py <input.md> [output.pdf]`
- **Dependencies**: `pip3 install weasyprint markdown` (if not installed)

### JDS-PRO-007 Visual Standards (enforced in stylesheet)
- **Typography (§4)**: H1=20pt, H2=14pt, H3=12pt, H4=11pt bold italic, body=10pt, line-height=1.5x
- **Fonts (§4.3)**: Source Sans Pro / Calibri / Inter (sans-serif) + Consolas (monospace). Max 2 families.
- **Layout (§5.1)**: A4, margins 25mm L/R, 20mm top, 25mm bottom
- **Alignment (§5.2)**: Left-align text, right-align numbers. Never justify.
- **Colours (§6.1)**: Navy Blue (#1B3A5C) headings, Steel Blue (#4A90A4) subheadings, Warm Gray (#8C8C8C) metadata. Max 3 colours per page.
- **Tables (§7.3)**: Navy Blue headers, alternating row shading, generous cell padding, units in header only
- **Uncontrolled copy (PRO-005 §6)**: Every PDF is marked "UNCONTROLLED COPY" top-right — PDFs are never the controlled copy, Git is.
- **Running header**: Document title on page 2+ for glance-level identification (§3)
- **Page numbers**: "Page N of M" centred at bottom

### Pre-flight Check (before generating any PDF)
1. Document has JDS metadata header (Doc No, Rev, Date, Status, Author)
2. Only one H1, no skipped heading levels, max 4 levels
3. Revision history table present at end
4. Reports (RPT) over 3 pages have at least one visual element (§7.1)
5. Only JDS palette colours used (§6.1)

### Monozukuri Self-Check (§8.1 — before issuing)
- Headings follow 4-level hierarchy consistently
- White space (ma) separates sections clearly
- Status block is complete and accurate
- Document works at all three reading levels: glance (0.5s), scan (5s), read (minutes)
