# JDS System Changelog

All changes to the JDS documentation system itself are recorded here. This provides a single place to see how the system has evolved over time.

---

## [3.3] — 2026-04-11

### Changed — Project Restructure & Consolidation
- **JDS-PRJ-MEC-002 merged into JDS-PRJ-MEC-001** — the Vessel Supervision System is now a subfolder (`03-supervision/`) inside the Pressure Vessel Ongoing Maintenance Program. One project, one folder, one changelog.
- **Project folder naming simplified** — folders now use JDS codes only (`JDS-PRJ-MEC-001/`) without descriptive suffixes. CLAUDE.md updated accordingly.
- **Templates centralised** — JDS-TMP-LOG-005 through 009 moved from project folder to `jds/templates/logs/` alongside all other system templates.
- **Older templates superseded** — JDS-TMP-LOG-001 (replaced by TMP-LOG-008), JDS-TMP-LOG-002 (replaced by TMP-LOG-008), JDS-TMP-LOG-003 (replaced by TMP-LOG-006). All marked SUPERSEDED with pointers to replacements.
- **AFS PDFs consolidated** — duplicate regulatory PDFs removed from `projects/` root; single copies now in `JDS-PRJ-MEC-001/02-regulations/SE-sweden/`.
- **JDS-PRO-010 updated** — template references changed from superseded TMP-LOG-001/002/003 to current TMP-LOG-005/006/008. Supervision workflow now includes program creation, round records, and annual reviews.
- **Document register updated** — all paths corrected for new folder structure. JDS-PRJ-MEC-002 marked SUPERSEDED. TMP-LOG-001/002/003 marked SUPERSEDED.

### Added
- **`projects/index.md`** — project index listing all JDS projects by document number with status.
- **JDS-TMP-RPT-004**: Risk Assessment Template for Pressurised Vessels — 5x5 P×C matrix with pre-populated risk scenarios for accumulators, boilers, cisterns, heat exchangers, piping, and cryogenic vessels. Translated from AH_Automation.xlsm "Risker" sheet.
- **`05-flt-program/`** folder in JDS-PRJ-MEC-001 — complete document index for performing ongoing supervision. Links all templates, procedures, manuals, regulatory references, examples, and automation tools.

### Enhanced
- **JDS-TMP-LOG-005 Rev B**: Added coordination person sign-off block per AFS 2017:3 4 Kap. §14 (physical person responsible for supervision).
- **JDS-TMP-LOG-008 Rev B**: Added placement and environmental risk checklist per AFS 2017:3 2 Kap. §2-3 (accessibility, blast zone, temperature, structural risk).
- **JDS-TMP-LOG-009 Rev B**: Added previous experience assessment per AFS 2017:3 2 Kap. §1 (usage history, repairs, incidents, deviations, monitoring need).

### Improved — Image Asset Organization
- **Logo variants reorganized** — 24 SVG logo variants moved from flat `logo-variants/` into `logo-variants/category/` (13 document category variants) and `logo-variants/domain/` (11 engineering domain variants).
- **All scripts updated** — `logo-variants.py`, `md2pdf.py`, `md2letter.py`, `office2pdf.py`, and `jds-validate.py` now use the new subfolder paths.
- **Blog image infrastructure** — created `projects/blog/assets/images/posts/` and `projects/blog/assets/images/shared/` for future blog post images.
- **Project image infrastructure** — created `projects/JDS-PRJ-MEC-001/assets/images/` for engineering project visuals.

---

## [3.2] — 2026-04-10

### Added — Vessel Supervision System (JDS-PRJ-MEC-002)
- **JDS-PRJ-MEC-002**: Vessel Supervision System — complete project for creating, managing, and performing ongoing supervision programs for pressurised vessels. Built on AFS 2017:3 consolidated with all amendments (AFS 2019:1, AFS 2020:10, AFS 2022:2).
- **JDS-MAN-MEC-002**: Supervision Program Manual — full methodology for building and running supervision programs: site survey, risk assessment, check design, documentation, annual review.
- **JDS-LOG-MEC-005**: Supervision Program Register — master tracker for all active supervision programs.
- **JDS-RPT-MEC-003**: AFS 2017:3 Consolidated Supervision Requirements — English-language summary of the base regulation and all three amendments, focused on ongoing supervision requirements.
- **JDS-TMP-LOG-005**: Supervision Program Template — complete template for creating site-specific supervision programs with daily/weekly/monthly/quarterly/annual check schedules.
- **JDS-TMP-LOG-006**: Supervision Round Record Template — execution record for supervision rounds with per-vessel checks, findings management, and sign-off.
- **JDS-TMP-LOG-007**: Annual Supervision Program Review Template — structured annual review covering execution summary, equipment changes, regulatory changes, personnel review, and effectiveness assessment.
- **Regulatory Traceability Matrix** — maps every supervision program element to specific AFS 2017:3 sections, including amendment-specific impacts.
- **JDS-TMP-LOG-008**: Equipment Inventory Template — blank inventory with auto-classification reference and CSV quick-start instructions.
- **JDS-LOG-MEC-006**: Example inventory (Gothenburg Workshop) — 7 vessels auto-classified: 4 Class A, 2 Class B, 1 Simple PV, with overdue inspections flagged.

### Added — Vessel Classification Script & Document Chain
- **`scripts/jds-classify.py`**: Automatic vessel classification per AFS 2017:3 (consolidated). Six modes: interactive, quick, CSV batch, `--program` (from inventory), `--round` (from program), `--review` (from program). Each document is self-contained and links to the next step in the chain: INVENTORY → PROGRAM → ROUND → REVIEW.
- **CLAUDE.md** updated with all jds-classify.py modes in automation tools table.

---

## [3.1] — 2026-03-25

### Changed — Repository Restructure for Authority
- **Root reduced to 4 folders**: `jds/` (system), `projects/` (work), `scripts/` (tools), `personal/` (non-JDS). Down from 12 top-level folders.
- **`blog/` moved to `projects/blog/`** — JDS owns the repo structure; Jekyll adapts. GitHub Actions workflow updated.
- **`3d-modeling/` moved to `projects/3d-modeling/`** — all work output under one roof.
- **`collections/`, `documents/`, `archive/` moved to `personal/`** — non-JDS content consolidated.
- **Root README.md** rewritten as JDS authority page — action-oriented "I need to..." task table replaces folder tour.
- **`jds/QUICK-REFERENCE.md`** created — one-page cheat sheet for document numbering, category/domain codes, revision sequence, common commands.
- **`scripts/README.md`** created — tool reference with usage examples for all 7 scripts.
- **All path references updated** — PRO-003, PRO-009, TMP-DWG-001, TMP-BLG-001, document register, CLAUDE.md.
- **Empty placeholder folders removed** — `software-projects/`, `documents/cv/`, `documents/notes/`.
- **CLAUDE.md §Structure** now defines the 4-folder root formally.

### Added — Office Document PDF Converter
- **`scripts/office2pdf.py`**: Reads JDS Excel workbooks (timesheet, expense, mileage) and renders as proper JDS-PRO-007 compliant PDFs using weasyprint. Same design language as `md2pdf.py` — logo header band, metadata card, navy headings, alternating rows, computed totals, running header/footer.

---

## [3.0] — 2026-03-25

### Added — Office Document Generation
- **`scripts/generate-office-docs.py`**: Excel workbook generator for timesheets, expense reports, and mileage logs. JDS-compliant styling (Navy Blue headers, alternating row shading, portrait A4, white background, no gridlines, logo embedding).
- **JDS-TMP-EXP-002**: Mileage Log Template — distance tracking with SEK/km rate calculations and monthly summary.
- **QMS-000 §6.4**: Supported File Formats — formalises Excel, PDF, and Word alongside Markdown as JDS document formats.
- Excel workbooks include: formulas, data validation (expense categories), print setup, UNCONTROLLED COPY footer, logo support.
- Logo is swappable via `JDS_LOGO_PATH` environment variable for client-branded documents.

### Added — Language Policy & Authority
- **JDS-QMS-000 Rev E** — Added §15 Language Policy. JDS is 100% English. All foreign loan words replaced with JDS-owned English terminology. Terminology map established.
- **Regulatory Traceability Matrix** — New supplemental document mapping every JDS-PRO-010 requirement to AFS 2017:3 sections. Working procedures are clean; compliance evidence is separate.

### Changed — Language Authority Cleanup
- **JDS-PRO-010 Rev B** — Complete English rewrite. All Swedish terms removed from working procedure. Renamed from `fortlopande-tillsyn` to `ongoing-maintenance`.
- **JDS-PRO-007 Rev D** — All Japanese terms replaced with JDS English terms: Active Space (was Ma), Compartment Design (was Bento), Visual Explanation (was Zukai), Craft Precision (was Monozukuri).
- **JDS-PRJ-MEC-001 Rev C** — Project README cleaned of all Swedish terminology.
- **JDS-TMP-LOG-002** renamed to `supervision-inventory-template` — English rewrite
- **JDS-TMP-LOG-003** renamed to `supervision-checklist-template` — English rewrite
- **JDS-TMP-LOG-004** renamed to `inspection-plan-template` — English rewrite
- **Document Registry** updated with new filenames, titles, and revision numbers
- **Design Principles table** in QMS-000 now uses JDS English terms throughout

### Language Authority
- JDS defines its own terminology. Foreign sources (Swedish regulation, Japanese design, Russian documentation) are acknowledged influences, but JDS English terms are always primary.

---

## [2.9] — 2026-03-25

### Added — Ongoing Maintenance Program
- **JDS-PRO-010**: Ongoing Maintenance Program Procedure — complete workflow for AFS 2017:3 ongoing maintenance programs. Covers setup, annual cycle, inspection handling, findings management.
- **JDS-TMP-LOG-002**: Supervision Inventory Template — equipment register for client sites
- **JDS-TMP-LOG-003**: Supervision Checklist Template — routine supervision checklist
- **JDS-TMP-LOG-004**: Annual Inspection Plan Template — annual inspection plan with quarterly tracking
- **JDS-TMP-RPT-003**: Inspection Report Template — post-inspection documentation with findings, wall thickness, and sign-off

### Changed
- **JDS-PRJ-MEC-001** updated to Rev B — Maintenance workflow integrated, active program folder structure documented, all templates and procedures linked

---

## [2.8] — 2026-03-25

### Added
- **SVG logo** — Johansson Engineering stamp converted from PNG to scalable SVG vector
- **Logo colour variants** — 24 category- and domain-specific SVG variants auto-generated by `scripts/logo-variants.py`
- **JDS-PRO-007 Rev C** — Added §6.4 Logo Colour Variants (category-specific logo colours for glance-level identification)
- **Colour-per-category system** — Navy (QMS/PRO), Teal (RPT/MAN), Steel Blue (DWG), Green (LOG), Heritage Red (COR/BLG), Bronze (TSH/EXP)

### Changed
- **md2pdf.py** — Auto-selects category-coloured SVG logo based on document number; falls back to SVG then PNG
- **md2letter.py** — Defaults to Heritage Red (COR) logo for letters; SVG-first with PNG fallback

### Added (Validator — now 10 checks, 100+ validations)
- **Internal markdown link validation** — checks all `[text](path)` links resolve to existing files
- **Blog post structure validation** — Jekyll front matter, required fields, JDS-BLG metadata
- **Script consistency checks** — logo sizes (52pt docs / 72pt letters), UNCONTROLLED COPY marking, border-radius prohibition, page numbering, running headers
- **Logo asset integrity** — PNG, SVG, and colour variants existence checks
- **Document status validation** — warns on non-standard status values
- **Revision letter validation** — catches use of JDS skip-letters (I, O, Q, S, X, Z)
- **Corrective action log** structure and next-number tracker checks
- **CLAUDE.md** consistency — verifies key system references are present
- **Safe file reading** — all file operations wrapped in try/except for robustness
- **--fix mode** — shows suggested fixes for each error type

---

## [2.7] — 2026-03-25

### Fixed
- **Root README.md** version synced to 2.6 → 2.7 (was showing 2.5)
- **JDS-QMS-001** Rev D — BLG domain code changed from required to optional (aligns with actual blog posts)
- **JDS-RPT-MEC-002** bumped to Rev B with revision history entry for table split
- **Project framework files** renamed to JDS convention: `JDS-PRO-004_`, `JDS-MAN-MEC-001_`, `JDS-LOG-MEC-001_`
- **Corrective action log** restructured from unreadable 7-column table to one CA per section

### Added (Validator)
- **Registry Rev vs file Rev** check — catches mismatches between document-register.md and actual file metadata
- **Root README version** sync check — ensures root README matches CHANGELOG version

---

## [2.6] — 2026-03-25

### Changed
- **Root README.md** rewritten — repo is now THE JDS, not "a repo with JDS in a subfolder"
- **Repository identity**: "The Office of Nils Johansson" is now the Johansson Documentation System
- Root README serves as the definitive landing page: find-what-you-need table, full structure, categories, domains, quick start guide
- All wide tables split to ≤7 columns for A4 readability (TMP-LOG-001, LOG-MEC-002, LOG-MEC-003, RPT-MEC-002)
- **jds-validate.py** — added table column width check (max 7), fixed naming pattern for examples/
- **md2pdf.py** — logo increased to 52pt, removed border-radius: 50%
- **Corrective action log** — first 3 CAs raised and closed (CA-2026-001 to 003)

---

## [2.5] — 2026-03-25

### Added
- **JDS-TMP-COR-001**: Cold Introduction Letter Template — old-world stationery design with Johansson Engineering 1983 stamp letterhead
- **md2letter.py**: Dedicated letter PDF generator — serif typography (Noto Serif Display), engraved-style letterhead, ornamental dividers, "Est. 1983" footer
- **jds/assets/logo.png**: Johansson Engineering 1983 circular stamp logo (sailor, anchor, girl with wrench) — cropped to square, replaces old text logo
- **jds/assets/fonts/**: Bundled M PLUS Rounded 1c font for consistent rendering
- **jds/templates/correspondence/**: New template category for business letters
- **jds-validate.py**: Automated JDS 5S audit script (70+ checks)
- **Example documents**: RPT-MEC-002, LOG-MEC-003, LOG-MEC-004, COR-GEN-001
- **.gitignore** — added `*.pdf` rule (PRO-005 §6: Git is controlled copy)

### Changed
- **md2pdf.py** redesigned with Apple-style warmth — rounded corners, card containers, soft table headers, warmer colour temperature (#1d1d1f warm black), logo integration via base64 data URI
- **Document Registry** updated with all new documents

---

## [2.4] — 2026-03-25

### Changed
- **JDS-PRO-007** Information Design Standard updated to Rev B — expanded from 8 to 14 sections
- **md2pdf.py** stylesheet upgraded to world-class level with design tokens, baseline grid, and accessibility compliance

### Added (PRO-007 New Sections)
- **§9 Grid System & Vertical Rhythm** — 6pt baseline unit, horizontal grid rules, content density (Toyota A3-inspired)
- **§10 Page Architecture** — five-zone page model with header/footer separator lines, first-page title block, continuation page rules
- **§11 Micro-Typography** — letter-spacing table, font weight discipline, WCAG 2.1 Level AA contrast ratios
- **§12 Figure & Table Conventions** — sequential numbering, revision history distinct styling
- **§13 Emptiness & Receptivity (Ku)** — Kenya Hara/MUJI philosophy codified: white space as active structure
- **§14 Automation & Consistency** — what the system enforces vs. what authors verify

### Stylesheet Improvements (md2pdf.py)
- Header/footer separator lines (0.25pt rules framing content zone)
- H1 increased to 20pt with 2pt bottom rule for authority
- All spacing aligned to 6pt baseline grid (24pt above H2, 18pt above H3, 12pt above H4)
- Improved table cell padding (6pt/8pt headers, 5pt/8pt cells)
- Revision history table gets distinct compact styling via HTML post-processing
- Blockquotes no longer force italic (better readability for long passages)
- Design token documentation in CSS comments
- Complete CSS comment structure referencing PRO-007 section numbers

### Design Research
- Analysed corporate document design from: Apple (San Francisco, optical hierarchy), Toyota (A3 one-page thinking), Bauhaus (grid systems, form follows function), Kenya Hara/MUJI (emptiness over minimalism), Bosch (WCAG accessibility, Red Dot Award design system), DNV (classification document architecture), Instron (engineering quality manual format)
- Synthesised 15 world-class design principles into JDS standards

---

## [2.3] — 2026-03-25

### Added
- **JDS-PRO-008**: Corrective Action Procedure — systematic nonconformance handling with 5 Whys root cause analysis, severity classification, horizontal deployment, and corrective action log (ISO 9001:2015 clause 10.2)
- **JDS-PRO-009**: Competence Management Procedure — personal qualifications, training records, certificate management, CPD tracking (ISO 9001:2015 clause 7.2, DNV-ST-0035)
- **JDS-QMS-002**: Document Retention Schedule — minimum retention periods for all document categories with legal/regulatory rationale (ISO 15489-1:2016)
- **JDS-TMP-RPT-002**: Management Review Record Template — structured template covering all ISO 9001:2015 clause 9.3 review inputs and outputs
- **Corrective Action Log** (`jds/registry/corrective-action-log.md`) — central tracker for all nonconformances and corrective actions

### Changed
- **JDS-QMS-000** Quality Manual updated to Rev D — added Corrective Action section (§13) referencing JDS-PRO-008, renumbered subsequent sections
- **Document Registry** updated with QMS-002, PRO-008, PRO-009, TMP-RPT-002, QMS-000 Rev D
- **JDS README** updated with references to new procedures and retention schedule

### Standards Alignment
- **ISO 9001:2015**: Closed all identified gaps — corrective action (clause 10.2), management review records (clause 9.3), competence (clause 7.2), retention of documented information (clause 7.5.3)
- **ISO 15489-1:2016**: Document retention schedule with defined periods and disposal process
- **ISO 10013:2021**: JDS exceeds all guidelines for QMS documentation
- **DNV-ST-0035**: Competence management procedure aligned with service supplier requirements
- **IEC 82045**: Document numbering and metadata compatible

---

## [2.2] — 2026-03-25

### Added
- **JDS-PRO-007**: Information Design Standard — Japanese-inspired visual design principles for all JDS documents (Ma, Bento layout, colour system, typography, three-level reading, Monozukuri)
- **Heritage & Reuse** principle in quality manual — from ISRO's frugal engineering (only document what's new)
- **Tiered Change Control** in quality manual — from Embraer (3 tiers: safety-critical, quality-affecting, administrative)
- **Knowledge Gaps & Documentation Confidence** in quality manual — from Petrobras/Baikonur (explicitly document unknowns and data reliability)
- **21 design principles** in quality manual from 15+ global traditions including: Lagom (Swedish), Grundlichkeit (German), Golden Project (Taiwan/TSMC), Commander's Intent (Israeli IDF), Design vs. As-Found (DNV), Horizontal Deployment (Samsung Korea), Lifecycle Documentation (NORSOK Norway), Failure Memory (Indian Railways)

### Changed
- **JDS-QMS-000** Quality Manual updated to Rev C — added information design, heritage reuse, tiered change control, knowledge gaps, expanded design principles table
- **Document Registry** updated with PRO-007 and QMS-000 Rev C

### Research Basis
Compared JDS against documentation systems from: Taiwan (TSMC), South Korea (Hyundai Heavy/Samsung), Norway (NORSOK/DNV), Germany (DIN/Mittelstand/VDI), Switzerland (CERN/watchmaking), Israel (IDF/defense), India (ISRO/Railways), Brazil (Embraer/Petrobras), Kazakhstan (Baikonur), Ukraine (Antonov), Belarus (BelAZ)

---

## [2.1] — 2026-03-25

### Added
- **JDS-PRO-005**: Document Review & Audit Procedure — defines 5S-based quarterly audits and annual reviews
- **JDS-PRO-006**: Project Komplekt Standard — defines required complete document sets per project type
- **JDS CHANGELOG** (this file) — system-level change tracking
- **Archive structure** (`jds/archive/`) for retired and superseded documents
- Document classification tiers (Public, Internal, Confidential) added to quality manual
- Komplekt (complete document set) concept added to quality manual
- 5S document management principles added to quality manual
- Hyperlinks added to document registry

### Changed
- **JDS-QMS-000** Quality Manual updated to Rev B — added Komplekt, 5S, classification, and visual management concepts
- **Document Registry** updated with hyperlinks to all documents and corrected blog post entries
- **JDS README** updated with references to new procedures

### Fixed
- Blog post numbering inconsistency in registry (now consistently uses domain-free format per system doc convention)

---

## [2.0] — 2026-03-25

### Added
- Engineering domain codes (MEC, MAR, AUT, ELE, PIP, STR, TST, FAB, THR, SFW, GEN)
- Renamed JEDS to JDS (3-letter system prefix)
- Mandatory 3D export standard: STEP + 3MF + STL
- 3D Model Management Procedure (JDS-PRO-003 Rev B)
- Document Numbering Standard updated with domain codes (JDS-QMS-001 Rev B)
- Blog post integration into JDS
- Pressure vessel maintenance project (JDS-PRJ-MEC-001)

---

## [1.0] — 2026-03-25

### Added
- Initial JDS system release
- Quality Manual (JDS-QMS-000)
- Document Numbering Standard (JDS-QMS-001)
- Document Creation Procedure (JDS-PRO-001)
- Revision Control Procedure (JDS-PRO-002)
- 7 document templates (JDS-TMP-001 through JDS-TMP-007)
- Document Registry
- Example inspection report (JDS-RPT-001)
