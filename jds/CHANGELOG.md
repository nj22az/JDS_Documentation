# JDS System Changelog

All changes to the JDS documentation system itself are recorded here. This provides a single place to see how the system has evolved over time.

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
