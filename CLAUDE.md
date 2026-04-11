# Project Instructions for Claude

## Repository Purpose
This repository IS the Johansson Documentation System (JDS). Every project, document, drawing, blog post, and record lives here under one unified system. JDS governs how work is created, numbered, revised, and found.

## Repository Structure (JDS-QMS-000 §21)

Four root folders. Everything lives in one of them.

- `jds/` - System governance (quality manual, procedures, templates, registry, assets, quick reference)
- `projects/` - All work output
  - Engineering projects: `projects/JDS-PRJ-[DOM]-NNN/`
  - 3D models: `projects/3d-modeling/JDS-DWG-[DOM]-NNN/`
  - Blog: `projects/blog/` (Jekyll, GitHub Pages)
  - Software projects: `projects/software/` (created on demand)
- `scripts/` - JDS automation tools (PDF generation, validation, office documents)
- `personal/` - Non-JDS content (not document-numbered)
  - `personal/collections/` - Personal collections (ROM archive, etc.)
  - `personal/documents/` - CV, cover letters, notes
  - `personal/archive/` - Archived past work

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
- Each 3D project gets a DWG number with domain: `projects/3d-modeling/JDS-DWG-MEC-001/`
- Standard subfolders: `source/`, `exports/`, `references/`, `renders/`
- Mandatory exports: STEP + 3MF + STL (always all three)
- Every project folder has a README.md project card
- See JDS-PRO-003 for full procedure

## Engineering Projects
- Each project gets a PRJ number with domain: `projects/JDS-PRJ-[DOM]-NNN/`
- Every project has a README.md and CHANGELOG.md (master change log)
- All document changes within a project are logged in CHANGELOG.md
- Every document has a status block at the top: Doc No | Rev | CURRENT/SUPERSEDED | Date | Author

## Guidelines
- Keep files organized in the appropriate directories
- Use descriptive names for project folders
- Software projects go in `projects/software/` (created on demand, each in its own subfolder)

## Self-Improvement & Automation

JDS is a living system. Every session should leave the repo better than it was found.

### Mandatory: While Writing Software Code (JDS-PRO-004)
All software code under JDS must follow these 7 rules from the first line:
1. **No dead code** — Don't write functions "for later." Every function must be called.
2. **Clean structure** — Each feature in its own module. No file over 500 lines (GUI exempt up to 1500).
3. **No hardcoded values** — All constants (numbers, colours, URLs, timeouts) in the config module. Zero magic numbers in logic.
4. **Clear names** — Every variable, function, and file name must describe what it holds. No `r`, `p`, `temp`, `data`, `thing`.
5. **Scale-safe** — Thread-safe, memory-safe. Lazy imports for heavy ML libraries.
6. **Keep files clean** — Refactor as you go. Shared helpers (used 3+ times) go in one module, imported everywhere.
7. **Document as you build** — README + CHANGELOG updated every revision. Comments only where logic is non-obvious.

### Mandatory: Before Every Commit
1. **Validate** — Run `python3 scripts/jds-validate.py --quick` before committing
2. **Code audit** — Quick check: no unused imports, no hardcoded values, no dead code (JDS-PRO-004 §3.1)
3. **Register** — Every new JDS document must be added to `jds/registry/document-register.md`
4. **Log** — System-level changes must be recorded in `jds/CHANGELOG.md`
5. **No orphans** — Never leave files unregistered or unlinked

### Mandatory: Before Ending a Session
1. Run `python3 scripts/jds-validate.py` (full audit)
2. Fix any errors found
3. If improvements were made to the system itself, bump the JDS version in:
   - `jds/README.md` (version number)
   - `jds/CHANGELOG.md` (new version entry)
4. If a software project was modified, run a full 7-point code audit every 5 revisions (JDS-PRO-004 §3.2)

### Slash Commands
- `/audit` — Run the full JDS 5S audit (JDS-PRO-005)
- `/new-doc` — Create a new document following all JDS procedures
- `/pdf` — Generate a JDS-compliant PDF from markdown

### Language Policy
- JDS is 100% English. JDS owns its terminology — foreign terms are never primary labels.
- Japanese design terms: Active Space (not Ma), Compartment Design (not Bento), Visual Explanation (not Zukai), Craft Precision (not Monozukuri)
- Swedish regulatory terms: Ongoing Maintenance Program (not Fortlöpande Tillsyn), Supervision Checklist (not Tillsynsprotokoll), Inspection Plan (not Kontrollplan)
- Regulatory traceability goes in separate matrix documents, never embedded in working procedures
- See QMS-000 §15 for the full policy

### Continuous Improvement Cycle
When you notice something that could be improved:
1. **Fix it now** if small (< 5 min)
2. **Log it** in `jds/registry/corrective-action-log.md` if larger
3. **Improve the validator** — if a new check would have caught the issue, add it to `scripts/jds-validate.py`
4. **Improve the templates** — if a template led to the issue, update it
5. **Improve CLAUDE.md** — if instructions were unclear, clarify them

### Automation Tools
| Tool | Purpose | Usage |
|------|---------|-------|
| `scripts/jds-validate.py` | Automated 5S audit (10 checks, 100+) | `python3 scripts/jds-validate.py` |
| `scripts/jds-validate.py --quick` | Quick registry check only | Pre-commit validation |
| `scripts/jds-validate.py --fix` | Show suggested fixes for errors | Post-audit remediation |
| `scripts/md2pdf.py` | JDS document → PDF (auto-coloured logo) | `python3 scripts/md2pdf.py <file.md>` |
| `scripts/md2letter.py` | Letter template → PDF (Heritage Red logo) | `python3 scripts/md2letter.py <file.md>` |
| `scripts/generate-office-docs.py` | Excel workbook generator (timesheet, expense, mileage) | `python3 scripts/generate-office-docs.py timesheet\|expense\|mileage\|all [output]` |
| `scripts/office2pdf.py` | Excel workbook → JDS-compliant PDF | `python3 scripts/office2pdf.py <file.xlsx> [output.pdf]` |
| `scripts/logo-variants.py` | Generate SVG logo colour variants | `python3 scripts/logo-variants.py` |
| `scripts/jds-classify.py` | Vessel classification & inventory generator (AFS 2017:3) | `python3 scripts/jds-classify.py` (interactive) |
| `scripts/jds-classify.py --quick` | Quick single-vessel classification | `python3 scripts/jds-classify.py --quick --ps 11 --volume 1000` |
| `scripts/jds-classify.py --csv` | Generate inventory from CSV data | `python3 scripts/jds-classify.py --csv vessels.csv --output inventory.md` |
| `scripts/jds-classify.py --program` | Generate supervision program from inventory | `python3 scripts/jds-classify.py --program --from inventory.md` |
| `scripts/jds-classify.py --round` | Generate supervision round from program | `python3 scripts/jds-classify.py --round --from program.md` |
| `scripts/jds-classify.py --review` | Generate annual review from program | `python3 scripts/jds-classify.py --review --from program.md` |

## PDF Generation (JDS-PRO-007 Compliance)

All PDFs exported from JDS documents MUST follow JDS-PRO-007 (Information Design Standard). Use `/pdf <filepath>` to generate compliant PDFs.

### Mandatory PDF Requirements
- **Documents**: `python3 scripts/md2pdf.py <input.md> [output.pdf]`
- **Letters**: `python3 scripts/md2letter.py <input.md> [output.pdf]`
- **Office documents**: `python3 scripts/office2pdf.py <input.xlsx> [output.pdf]`
- **Dependencies**: `pip3 install openpyxl weasyprint markdown` (if not installed)

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

### Table Design Rules
- **Maximum 7 columns per table** on A4 portrait — wider tables get truncated and are unreadable
- If data needs more columns, **split into multiple related tables** linked by a shared ID column
- The validator (`jds-validate.py`) will flag tables with >7 columns as errors
- For very wide data sets, consider landscape orientation or restructuring as card layouts

### Logo & Brand Rules
- The Johansson Engineering 1983 stamp logo exists in two formats:
  - **SVG (vector)**: `jds/assets/logo.svg` — scalable, crisp at any size, preferred
  - **PNG (bitmap)**: `jds/assets/logo.png` — 752×752px, fallback
- **Colour variants**: `jds/assets/logo-variants/category/` (13 category) and `jds/assets/logo-variants/domain/` (11 domain) — auto-generated per PRO-007 §6.4
- The logo is a circular stamp — **never squish, crop to circle, or apply border-radius**
- Minimum display size: **52pt** in documents, **72pt** in letterheads
- The logo is Nils Johansson's brand and image — it must be clearly readable at all times
- PDF generators auto-select the correct category colour variant based on document number
- To regenerate variants: `python3 scripts/logo-variants.py`

### Craft Precision Self-Check (§8.1 — before issuing)
- Headings follow 4-level hierarchy consistently
- Active space separates sections clearly
- Status block is complete and accurate
- Document works at all three reading levels: glance (0.5s), scan (5s), read (minutes)

### Preventing Recurring Issues (Self-Improvement Protocol)
When any formatting, styling, layout, or content issue is found:
1. **Fix the immediate instance** — correct the document
2. **Fix the root cause** — update the template, script, or stylesheet that produced it
3. **Add automated detection** — add a check to `jds-validate.py` so it's caught automatically
4. **Update CLAUDE.md** — add the rule here so it's never repeated
5. **Log the corrective action** — record in `jds/registry/corrective-action-log.md`
6. **Bump the version** — update `jds/README.md` and `jds/CHANGELOG.md`

This is the JDS continuous improvement cycle. The system must get better every session, never worse.
