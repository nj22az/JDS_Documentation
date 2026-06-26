# Corrective Action Log

**Last updated:** 2026-06-26

This log tracks all nonconformances and corrective actions raised under [JDS-PRO-008](../procedures/JDS-PRO-008_corrective-action.md).

---

## Open Actions

*No open corrective actions.*

## Closed Actions

### CA-2026-010 — Whole-repo review sweep (6 parallel agents) | CLOSED

| | |
|---|---|
| **Date** | 2026-06-26 |
| **Source** | Whole-repo self-enhancement sweep (6 review agents over 108 docs + 7 scripts) |
| **Description** | A full-repo review found ~50 issues. The highest-impact class was **stale cross-references from earlier renumbers/merges**: the JDS-PRO-004→PRO-011 renumber (CA-2026-008) and the JDS-PRJ-MEC-002→MEC-001 merge were never propagated, so README/index/manual references pointed at the wrong documents. Also: a broken doc cross-ref (PRO-008 → wrong QMS section), a duplicate section number, a wrong risk count, example status/revision-block mismatches, language-policy violations (Japanese 5S headings, Swedish picklists, "Komplekt"), script dead code, and a register-vs-file Status drift the validator never checked. |
| **Root Cause** | Renumber/merge operations fixed the primary document but not the inbound references; the validator compared register Rev to file Rev but never the Status column, and had no check for stale prose references. |

**Corrective Action:**
1. Propagated JDS-PRO-004→PRO-011 and JDS-PRJ-MEC-002→MEC-001 across all stale references (README, FLT index, supervision manual, example Project fields, PRO-010).
2. Fixed cross-ref/structural faults: PRO-008 §16/§17→§18/§19, TMP-LOG-008 duplicate "## 9", TMP-RPT-005 maintenance-report pointer, RPT-MEC-002 risk count, example status/revision blocks.
3. Language policy: 5S headings now English-first (Sort (Seiri)…), "kaizen"→continuous improvement, TMP-RPT-003 Swedish picklists→English, TMP-LOG-001 "Komplekt"→Complete Document Set.
4. Scripts: removed dead code (unused imports/vars/function), simplified a redundant validator clause, hoisted the mileage rate to a named constant.
5. **Validator hardened** — added a register-vs-file **Status** check (immediately surfaced 10 further drifts, all fixed) and added RETIRED to the valid-status set.
6. Doc-list accuracy: root README now lists PRO-001–012 and jds-classify.py; register Status column reconciled to the files; project CHANGELOG records the renumber.

**Held for owner sign-off (regulatory/domain — not auto-edited):** several MEC-001 documents carry inspection-interval regimes, AFS section numbers, amendment descriptions, and classification thresholds that the agents flagged as contradicting the authoritative consolidated doc (JDS-RPT-MEC-003 Rev B). These are compliance statements and were left for engineering review rather than rewritten. See the session report.

### CA-2026-009 — Root README version check was a silent no-op | CLOSED

| | |
|---|---|
| **Date** | 2026-06-26 |
| **Source** | Self-enhancement QA sweep |
| **Description** | The validator's root-README version check searched for `**JDS Version:**`, which never appears (the root README writes `**Version 3.x**`). The check matched nothing and silently passed, so the root README version drifted to 3.2 while the system reached 3.7 — undetected. |
| **Root Cause** | A guard was written against an assumed format that differs from the file's actual format; with no "could not parse" branch, a non-match looked identical to a pass. |

**Corrective Action:**
1. Fixed the regex to `\*\*Version (\d+\.\d+)\*\*` (matches the real format); verified it now flags the 3.2≠3.7 drift.
2. Added a "could not parse" warning branch so a future format change surfaces instead of silently passing.
3. Synced the root README to v3.8 and refreshed its dashboard (added PRO-012 and Document Studio).
4. Consolidated duplicated app code (JDS-number regex ×3, `today()` ×2) into `config`, and hardened the PDF route's path — found during the same sweep.


### CA-2026-008 — JDS number collisions (PRO-004 + example/template family) | CLOSED

| | |
|---|---|
| **Date** | 2026-06-25 |
| **Source** | Validator audit (orphan + numbering check) |
| **Description** | Several distinct documents shared JDS numbers already assigned to other documents: (1) **JDS-PRO-004** was double-booked — `code-audit.md` (Software Code Quality Standard, canonical per CLAUDE.md) and `inspection-planning.md` (with a stray duplicate copy in `jds/procedures/`). (2) `maintenance-report-example` reused RPT-MEC-003 (AFS 2017:3 Consolidated). (3) `field-service-logbook-example` reused LOG-MEC-005 (Supervision Program Register). (4) `maintenance-report-template` reused TMP-RPT-004 (Risk Assessment Template). (5) `field-service-logbook-template` reused TMP-LOG-005 (Supervision Program Template). |
| **Root Cause** | A maintenance-report + field-service-logbook document family was added (≈v3.3) reusing numbers already in use; CA-2026-006's PRO-004 move left a duplicate, then a new code-audit doc took the PRO-004 number. The registry parser keys on doc number, so duplicate rows were silently overwritten and the collisions were never flagged as errors — only surfaced indirectly as orphans. |

**Corrective Action (resolved with owner approval):**
1. **PRO-004 = Software Code Quality Standard** confirmed canonical; registry corrected (was double-listed). Stray duplicate `jds/procedures/JDS-PRO-004_inspection-planning.md` deleted.
2. **Inspection Planning Procedure** renumbered JDS-PRO-004 → **JDS-PRO-011** (Rev B), content unchanged.
3. Example/template family renumbered to next-free numbers: maintenance-report example RPT-MEC-003 → **RPT-MEC-005**; field-service-logbook example LOG-MEC-005 → **LOG-MEC-011**; maintenance-report template TMP-RPT-004 → **TMP-RPT-006**; field-service-logbook template TMP-LOG-005 → **TMP-LOG-010**. All registered; internal cross-reference in the logbook template updated.
4. **Validator hardened** — added `check_duplicate_numbers()` to `jds-validate.py`: errors on any doc number appearing twice in the registry OR shared by two files on disk. This collision class is now caught automatically.

---

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

**Next number:** CA-2026-011
