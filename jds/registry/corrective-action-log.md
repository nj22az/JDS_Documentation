# Corrective Action Log

**Last updated:** 2026-06-25

This log tracks all nonconformances and corrective actions raised under [JDS-PRO-008](../procedures/JDS-PRO-008_corrective-action.md).

---

## Open Actions

### CA-2026-008 — JDS number collisions (PRO-004 + example/template family) | OPEN

| | |
|---|---|
| **Date** | 2026-06-25 |
| **Source** | Validator audit (orphan + numbering check) |
| **Description** | Several distinct documents share JDS numbers already assigned to other documents: (1) **JDS-PRO-004** is double-booked — `code-audit.md` (Software Code Quality Standard, the number CLAUDE.md treats as canonical) and `inspection-planning.md` (still registered at register line 24, with a stray duplicate copy in `jds/procedures/`). (2) `JDS-RPT-MEC-003_maintenance-report-example.md` collides with the registered RPT-MEC-003 (AFS 2017:3 Consolidated). (3) `JDS-LOG-MEC-005_field-service-logbook-example.md` collides with the registered LOG-MEC-005 (Supervision Program Register). (4) `JDS-TMP-RPT-004_maintenance-report-template.md` collides with registered TMP-RPT-004 (Risk Assessment Template). (5) `JDS-TMP-LOG-005_field-service-logbook-template.md` collides with registered TMP-LOG-005 (Supervision Program Template). |
| **Root Cause** | A maintenance-report + field-service-logbook document family was added (≈v3.3) reusing numbers already in use; CA-2026-006's PRO-004 move left a duplicate, then a new code-audit doc took the PRO-004 number. The validator detected the orphans but renumbering was deferred. |

**Status:** Held pending owner direction. Renumbering changes document identity and traceability, so it is not done unilaterally. Proposed resolution (on approval): assign the new maintenance-report/logbook family the next free numbers in each category, renumber the project Inspection Planning procedure off PRO-004 (code-audit keeps PRO-004 per CLAUDE.md), delete the stray duplicate, and register all of them. A validator check for duplicate JDS numbers should be added so this is caught automatically in future.



## Closed Actions

### CA-2026-001 — Wide tables overflow A4 | CLOSED

| | |
|---|---|
| **Date** | 2026-03-25 |
| **Source** | Self-audit |
| **Description** | Wide tables (>7 columns) in templates and documents cause unreadable PDFs on A4 |
| **Root Cause** | No automated check existed; PRO-007 max 7-column rule was not enforced |

**Corrective Action:**
1. Split all wide tables to ≤7 columns
2. Added table width check to `jds-validate.py`
3. Added Table Design Rules to CLAUDE.md

---

### CA-2026-002 — Logo squished and too small in PDFs | CLOSED

| | |
|---|---|
| **Date** | 2026-03-25 |
| **Source** | Self-audit |
| **Description** | Logo too small (38pt) and squished (border-radius: 50% on square stamp) in PDF output |
| **Root Cause** | CSS written for generic circular logo, not tested with actual stamp artwork |

**Corrective Action:**
1. Increased logo to 52pt
2. Removed `border-radius: 50%`
3. Verified rendering in all PDF generators

---

### CA-2026-003 — Repo identity unclear | CLOSED

| | |
|---|---|
| **Date** | 2026-03-25 |
| **Source** | Self-audit |
| **Description** | Repo identity unclear — JDS treated as subfolder, not the repository's core identity |
| **Root Cause** | README.md written as personal workspace overview, not as JDS landing page |

**Corrective Action:**
1. Rewrote root README.md as the definitive JDS entry point
2. Added navigation, structure, categories, quick start

---

### CA-2026-004 — Version mismatch, naming violations, missing Rev bumps | CLOSED

| | |
|---|---|
| **Date** | 2026-03-25 |
| **Source** | Deep audit |
| **Description** | Multiple system hygiene issues: root README showed v2.5 (actual v2.6), project files didn't follow JDS naming, blog numbering standard inconsistent, RPT-MEC-002 missing Rev B, validator lacked Rev consistency check |
| **Root Cause** | No automated check for version sync across all READMEs; no Rev match check between registry and files |

**Corrective Action:**
1. Fixed root README version to 2.6
2. Updated QMS-001 Rev D: blog domain code now optional (aligns with practice)
3. Renamed project framework files to JDS convention (JDS-PRO-004_, JDS-MAN-MEC-001_, JDS-LOG-MEC-001_)
4. Bumped RPT-MEC-002 to Rev B with revision history entry
5. Added registry Rev vs file Rev check to validator
6. Added root README version sync check to validator
7. Restructured this CA log for readability (was 7-column table)

---

### CA-2026-005 — Language policy violation: "Komplekt" used as primary label | CLOSED

| | |
|---|---|
| **Date** | 2026-03-26 |
| **Source** | Full repo audit |
| **Description** | QMS-000 §15 defines "Complete Document Set" as the JDS term, with "Komplekt" as reference only. However, "Komplekt" was the primary label in PRO-006 filename, title, and ~40 occurrences across 11 files. |
| **Root Cause** | Term adopted from ESKD tradition before language policy was formalised. Validator only checked md2pdf.py CSS, not document content. |

**Corrective Action:**
1. Renamed PRO-006 file from `project-komplekt` to `complete-document-set`
2. Replaced all ~40 "Komplekt" occurrences with "Complete Document Set" / "document set"
3. Updated all internal links across README, registry, QMS-000, templates, and procedures
4. Bumped PRO-006 to Rev B with language policy compliance note
5. Only retained "Komplekt" in QMS-000 §15.2 glossary (reference column) and PRO-006 revision history

---

### CA-2026-006 — PRO-004 stored in project folder instead of procedures | CLOSED

| | |
|---|---|
| **Date** | 2026-03-26 |
| **Source** | Full repo audit |
| **Description** | JDS-PRO-004 (Inspection Planning) was located in `projects/JDS-PRJ-MEC-001.../01-framework/` instead of `jds/procedures/`. All other procedures are in `jds/procedures/`. |
| **Root Cause** | PRO-004 was created as part of the project setup before the single-location principle was enforced. |

**Corrective Action:**
1. Moved PRO-004 to `jds/procedures/`
2. Updated registry link to new location
3. Updated project README to note the move

---

### CA-2026-007 — Repo hygiene: stray PDFs + H1 font-size + Guide Note callout | CLOSED

| | |
|---|---|
| **Date** | 2026-06-25 |
| **Source** | Self-audit / session cleanup |
| **Description** | (1) `safe-to-delete/` held 4 stray PDF exports under version control. (2) `md2pdf.py` H1 font-size was 22pt while PRO-007 §4 and the validator's CSS-compliance check require 20pt. (3) Dense technical docs lacked a defined cognitive-relief callout. |
| **Root Cause** | (1) Temporary export folder never pruned. (2) Stylesheet drifted from the standard before the CSS-compliance check was added. (3) No documented mascot/companion callout existed. |

**Corrective Action:**
1. Removed `safe-to-delete/` from version control (Git is the controlled copy — PRO-005 §6)
2. Corrected `md2pdf.py` H1 font-size 22pt → 20pt
3. Added the **Guide Note** callout (`Doc says:` → `div.guide`) in `md2pdf.py`, documented it in PRO-007 §15 (Rev E) and CLAUDE.md, in JDS English per QMS-000 §15
4. Bumped JDS to v3.4

---

**Next number:** CA-2026-009
