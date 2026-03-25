# Corrective Action Log

**Last updated:** 2026-03-25

This log tracks all nonconformances and corrective actions raised under [JDS-PRO-008](../procedures/JDS-PRO-008_corrective-action.md).

---

## Open Actions

*No open corrective actions.*

## Closed Actions

| CA No. | Date | Source | Description | Root Cause | Corrective Action | Status |
|--------|------|--------|-------------|-----------|-------------------|--------|
| CA-2026-001 | 2026-03-25 | Self-audit | Wide tables (>7 columns) in templates and documents cause unreadable PDFs on A4 | No automated check existed; PRO-007 max 7-column rule was not enforced | 1. Split all wide tables to ≤7 columns. 2. Added table width check to jds-validate.py. 3. Added Table Design Rules to CLAUDE.md. | CLOSED |
| CA-2026-002 | 2026-03-25 | Self-audit | Logo too small (38pt) and squished (border-radius: 50% on square stamp) in PDF output | CSS written for generic circular logo, not tested with actual stamp artwork | 1. Increased logo to 52pt. 2. Removed border-radius: 50%. 3. Verified rendering. | CLOSED |
| CA-2026-003 | 2026-03-25 | Self-audit | Repo identity unclear — JDS treated as subfolder, not the repository's core identity | README.md written as personal workspace overview, not as JDS landing page | 1. Rewrote root README.md as the definitive JDS entry point. 2. Added navigation, structure, categories, quick start. | CLOSED |

---

**Next number:** CA-2026-004
