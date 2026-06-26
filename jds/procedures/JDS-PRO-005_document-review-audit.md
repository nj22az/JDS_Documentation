# Document Review & Audit Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-005 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how documents are reviewed for continued accuracy, how the documentation system is audited for health, and how improvements are tracked. It draws on the Japanese 5S methodology applied to document management and the ISO 9001 periodic review concept.

## 2. The 5S Document Audit

Every quarter, perform a 5S audit of the documentation system. The five steps are:

### 2.1 Sort (Seiri) — Eliminate Unnecessary Documents

- Are there documents that are no longer relevant?
- Are there drafts that were never completed?
- **Action:** Retire or archive anything not actively needed.

### 2.2 Set in Order (Seiton) — Verify Organisation

- Are all files named according to JDS conventions?
- Is the folder structure consistent?
- Are all documents registered in the Document Registry?
- **Action:** Fix any naming or filing inconsistencies.

### 2.3 Shine (Seiso) — Check for Accuracy

- Are active documents still technically accurate?
- Are links and cross-references working?
- Are templates still suitable for current work?
- **Action:** Update or flag documents that need revision.

### 2.4 Standardise (Seiketsu) — Enforce Consistency

- Are templates being used consistently?
- Do all documents have proper headers and revision history?
- Are revision letters and dates current?
- **Action:** Bring non-conforming documents into compliance.

### 2.5 Sustain (Shitsuke) — Schedule the Next Audit

- Record the audit date and findings.
- Schedule the next quarterly audit.
- Track improvement actions to completion.

## 3. Quarterly Audit Checklist

Use this checklist during each quarterly 5S audit:

- [ ] All documents in registry match actual files on disk
- [ ] No orphan files (files without registry entries)
- [ ] No phantom entries (registry entries without files)
- [ ] All active documents have status APPROVED (not stale DRAFTs)
- [ ] All file names follow JDS conventions
- [ ] All cross-references and links are valid
- [ ] Templates are current and usable
- [ ] No documents overdue for periodic review

## 4. Annual Document Review

All Tier 1 and Tier 2 documents (Quality Manual, Procedures) must be reviewed annually. During review:

### 4.1 Review Process

1. Read the document in full
2. Ask: *"Is this still accurate? Is this still needed? Is anything missing?"*
3. If changes needed → revise per JDS-PRO-002
4. If no changes needed → record the review:
   - Add a Git commit: `Annual review of JDS-XXX-NNN: confirmed current, no changes`
   - Update the review date in the Document Registry

### 4.2 Review Schedule by Document Type

| Document Type | Review Frequency | Review Trigger |
|---|---|---|
| Quality Manual (QMS) | Annual | Calendar or significant business change |
| Procedures (PRO) | Annual | Calendar or process change |
| Standards (QMS-001 etc.) | Annual | Calendar or when issues found |
| Templates (TMP) | Annual | Calendar or when issues found |
| Manuals (MAN) | Annual | Calendar or regulatory change |
| Active project docs (PRJ) | At project milestones | Milestone completion |
| Reports (RPT) | No review needed | Records are point-in-time |
| Timesheets/Expenses | No review needed | Records are point-in-time |
| Blog posts (BLG) | No review needed | Published content is historical |

### 4.3 Event-Based Review Triggers

In addition to scheduled reviews, documents must be reviewed when:

- A nonconformance or error is discovered
- A regulatory change affects the document's scope
- Client or collaborator feedback identifies an issue
- An audit finding relates to the document
- The business or workflow changes significantly

## 5. Audit Records

### 5.1 Recording Audit Results

After each quarterly audit, record findings as a Git commit with a summary:

```
git commit --allow-empty -m "JDS 5S Audit Q1 2026: [summary of findings and actions]"
```

For significant audits, create a brief audit report (JDS-RPT series).

### 5.2 Tracking Improvement Actions

Improvements identified during audits are tracked using the **Before/After** method (from the continuous-improvement tradition):

1. Document the **current state** (what needs to change)
2. Document the **target state** (what it should look like after)
3. Implement the change
4. Record the **result** in the revision history and CHANGELOG

## 6. Controlled vs. Uncontrolled Copies

| Aspect | Controlled Copy | Uncontrolled Copy |
|--------|----------------|-------------------|
| **What** | The Git repository (main branch) | Exported PDFs, emailed files, printed copies |
| **Updates** | Always current when pulled | Snapshot — no guarantee of currency |
| **Use for** | Active work, official reference | Client handouts, external sharing |
| **Marking** | No marking needed (repo IS the controlled copy) | Mark as "UNCONTROLLED COPY" or "FOR REFERENCE ONLY" |

**Rule:** The main branch of the repository is always the single source of truth. Anything outside the repository is an uncontrolled copy.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — 5S audit cycle, periodic review, controlled/uncontrolled copies |
