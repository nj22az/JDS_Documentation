# Revision Control Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-002 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how documents are revised, what triggers a revision, and how to maintain a clear history of changes.

## 2. When to Revise a Document

A document must be revised when:

| Trigger | Action |
|---------|--------|
| Error found (factual, technical, or calculation) | **Mandatory** revision |
| Scope of work changed | **Mandatory** revision |
| Process or procedure changed | **Mandatory** revision |
| Clarification needed (feedback from users) | Revision recommended |
| Formatting or editorial improvements only | Minor update (see Section 5) |
| Periodic scheduled review | Revise if needed, or re-approve as-is |

## 3. Revision Process

### Step 1: Identify the Change

Before editing, document what needs to change and why. This goes into the revision history table.

### Step 2: Create a Working Copy

In Git, create a branch for the revision work:
```
git checkout -b revision/JDS-RPT-004-revB
```

This keeps the current approved version intact while you work on the update.

### Step 3: Make the Changes

Edit the document content as needed. Mark significant changes clearly — you can use **bold** text temporarily during review to highlight what changed.

### Step 4: Update the Header

```markdown
| **Revision** | B |
| **Date** | 2026-04-15 |
| **Status** | APPROVED |
```

### Step 5: Update the Revision History

Add a new row to the revision history table at the bottom of the document:

```markdown
| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
| B | 2026-04-15 | Nils Johansson | Updated Section 4 to reflect new calibration method |
```

**The description must explain WHY the change was made**, not just what was changed.

### Step 6: Review and Approve

Same review process as a new document (see JDS-PRO-001).

### Step 7: Update the Registry

Update the document's entry in the [Document Registry](../registry/document-register.md) with the new revision letter and date.

### Step 8: Merge and Commit

Merge the revision branch back to main. The Git history provides an additional layer of traceability.

## 4. Revision Levels

| Level | Letter | Meaning |
|-------|--------|---------|
| Draft | DRAFT | Not yet approved. Work in progress. |
| First release | Rev A | First approved version. |
| Subsequent | Rev B, C, D... | Each approved update increments one letter. |

**Skip these letters:** I, O, Q, S, X, Z (to avoid confusion with numbers or ambiguity).

**Full sequence:** A, B, C, D, E, F, G, H, J, K, L, M, N, P, R, T, U, V, W, Y, AA, AB...

## 5. Minor Updates vs. Full Revisions

Not every change warrants a full revision. Here's the distinction:

### Full Revision (new letter)
- Technical content changed
- Data, calculations, or conclusions changed
- Scope or applicability changed
- Procedure steps added, removed, or reordered

### Minor Update (same letter, note in Git commit)
- Typo corrections that don't affect meaning
- Formatting improvements
- Fixing broken links or references

For minor updates, keep the same revision letter but note the change in the Git commit message. This keeps the revision history focused on meaningful changes.

## 6. Superseding and Retiring Documents

### Superseded
When a document is replaced by a newer document (not just a new revision, but an entirely new document):

1. Mark the old document status as `SUPERSEDED`
2. Add a note at the top: `Superseded by JDS-XXX-NNN on [date]`
3. Update the registry
4. The old file stays in the repository for reference

### Retired
When a document is no longer relevant to any current work:

1. Mark the status as `RETIRED`
2. Add a note at the top: `Retired on [date]. Reason: [brief reason]`
3. Update the registry
4. Move to an `archive/` subfolder if desired

## 7. Periodic Review Schedule

All active documents should be reviewed on a regular schedule to ensure they remain current:

| Document type | Review frequency |
|---|---|
| Quality Manual (QMS-000) | Annually |
| Procedures (PRO series) | Annually |
| Templates (TMP series) | Annually or when issues are found |
| Active project documents | At project milestones |
| Reports | No periodic review needed (point-in-time records) |
| Timesheets / Expenses | No periodic review needed (records) |

During review, either:
- Revise the document if changes are needed
- Re-approve as-is (update the review date in the registry)

## 8. Traceability Summary

Every change to a JDS document is traceable through three layers:

1. **Revision history table** (in the document itself) — what changed and why
2. **Document registry** (central log) — current status and revision of every document
3. **Git history** (repository) — exact file changes, timestamps, and commit messages

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
