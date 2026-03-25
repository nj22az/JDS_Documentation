# Corrective Action Log

**Last updated:** 2026-03-25

This log tracks all nonconformances and corrective actions raised under [JDS-PRO-008](../procedures/JDS-PRO-008_corrective-action.md).

---

## Open Actions

*No open corrective actions.*

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

**Next number:** CA-2026-005
