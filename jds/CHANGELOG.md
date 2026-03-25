# JDS System Changelog

All changes to the JDS documentation system itself are recorded here. This provides a single place to see how the system has evolved over time.

---

## [2.3] — 2026-03-25

### Added
- **JDS-PRO-008**: Corrective Action Procedure — systematic nonconformance handling with 5 Whys root cause analysis, severity classification, horizontal deployment, and corrective action log (ISO 9001:2015 clause 10.2)
- **JDS-TMP-RPT-002**: Management Review Record Template — structured template covering all ISO 9001:2015 clause 9.3 review inputs and outputs (quality performance, corrective actions, audit results, resource adequacy, risk/opportunity)
- **Corrective Action Log** (`jds/registry/corrective-action-log.md`) — central tracker for all nonconformances and corrective actions

### Changed
- **JDS-QMS-000** Quality Manual updated to Rev D — added Corrective Action section (§13) referencing JDS-PRO-008, renumbered subsequent sections
- **Document Registry** updated with PRO-008, TMP-RPT-002, QMS-000 Rev D
- **JDS README** updated with corrective action procedure reference

### ISO 9001:2015 Alignment
Closed identified gaps: corrective action procedure (clause 10.2), management review records (clause 9.3). JDS now provides documented coverage for all core ISO 9001:2015 requirements.

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
