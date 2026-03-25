# Corrective Action Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-008 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how nonconformances, errors, and improvement opportunities are identified, investigated, corrected, and prevented from recurring. It satisfies ISO 9001:2015 clause 10.2 (Nonconformity and corrective action).

## 2. Scope

Applies to all nonconformances found in:

- Engineering deliverables (reports, drawings, models, software)
- Documentation system (JDS procedures, templates, registry)
- Project execution (missed deadlines, scope issues, client complaints)
- Audit findings (quarterly 5S audits, annual reviews)

## 3. Definitions

| Term | Meaning |
|------|---------|
| **Nonconformance (NC)** | Any deviation from a requirement, standard, procedure, or client expectation |
| **Correction** | Immediate action to fix the specific problem |
| **Corrective Action** | Action to eliminate the root cause so the problem does not recur |
| **Root Cause** | The underlying reason why the nonconformance occurred |

## 4. Procedure

### 4.1 Identify and Record

When a nonconformance is discovered:

1. **Stop** — do not continue work that may compound the error
2. **Record** the nonconformance in a Git commit or issue:
   - What was found
   - Where it was found (document, project, deliverable)
   - When it was found
   - Who found it
   - Severity: **Critical** / **Major** / **Minor**

**Severity definitions:**

| Severity | Definition | Response time |
|----------|-----------|---------------|
| **Critical** | Affects safety, regulatory compliance, or client deliverable accuracy | Immediate — stop and fix before continuing |
| **Major** | Affects quality, completeness, or professional standard | Within 5 working days |
| **Minor** | Administrative error, formatting, or cosmetic issue | Next scheduled review or audit |

### 4.2 Contain

Take immediate correction to limit the impact:

- If a document has been issued with an error → notify anyone who received it
- If an uncontrolled copy is in circulation → mark it as superseded
- If a deliverable is affected → quarantine until corrected

### 4.3 Investigate Root Cause

Ask **why** the nonconformance occurred. Use the **5 Whys** method:

```
NC: Drawing issued with wrong material specification
Why? → The material was copied from an old drawing
Why? → The old drawing was not marked as superseded
Why? → The revision control procedure was not followed
Why? → The procedure was unclear about marking superseded drawings
Why? → The procedure lacked a specific step for this
ROOT CAUSE: Procedure gap in JDS-PRO-002
```

For complex issues, also consider:

- Was a template or procedure missing or unclear?
- Was training or knowledge insufficient?
- Was the workload or time pressure a factor?
- Is this a one-off or has it happened before? (Check horizontal deployment — Samsung principle)

### 4.4 Implement Corrective Action

Define and implement actions that address the root cause:

1. **What** specific action will prevent recurrence
2. **Who** is responsible for implementation
3. **When** it must be completed by
4. **Evidence** — how you will verify the action was effective

Common corrective actions in JDS:

| Root cause type | Typical corrective action |
|----------------|--------------------------|
| Procedure gap | Revise the procedure (JDS-PRO-002) |
| Template missing/inadequate | Create or update template |
| Knowledge gap | Add to project Knowledge Gaps section |
| Checklist incomplete | Update komplekt checklist (JDS-PRO-006) |
| Review missed | Adjust review triggers (JDS-PRO-005) |

### 4.5 Verify Effectiveness

After implementation, verify the corrective action works:

- Did the same or similar problem recur? (Check at next audit)
- Is the corrective action sustainable?
- Were there any unintended side effects?

Record verification in the corrective action log or as a Git commit.

### 4.6 Horizontal Deployment

After resolving a nonconformance, ask: **"Where else could this same problem occur?"**

Review other documents, projects, or processes that might have the same vulnerability. Apply preventive action where needed. This Samsung-inspired practice turns every problem into a system-wide improvement.

## 5. Corrective Action Log

Track all corrective actions using this format in a Git issue or markdown file:

```markdown
### CA-[YYYY]-[NNN]: [Brief description]

| Field | Detail |
|-------|--------|
| **Date raised** | YYYY-MM-DD |
| **Raised by** | [Name] |
| **Source** | [Audit / Client feedback / Self-identified / Other] |
| **Severity** | Critical / Major / Minor |
| **Description** | [What was found] |
| **Root cause** | [Result of 5 Whys analysis] |
| **Correction** | [Immediate fix applied] |
| **Corrective action** | [Action to prevent recurrence] |
| **Due date** | YYYY-MM-DD |
| **Status** | Open / In progress / Closed |
| **Verified** | [Date and evidence of effectiveness] |
| **Horizontal deployment** | [Other areas checked/updated] |
```

For a sole-proprietor practice, a single corrective action log file (`jds/registry/corrective-action-log.md`) is sufficient. Create individual entries as nonconformances arise.

## 6. Integration with Other JDS Procedures

| Procedure | Integration point |
|-----------|-------------------|
| JDS-PRO-002 (Revision Control) | Corrective actions that change documents trigger a revision |
| JDS-PRO-005 (Review & Audit) | Audit findings feed into corrective action process |
| JDS-PRO-006 (Komplekt) | Missing komplekt items may be raised as nonconformances |
| Quality Manual §16 (Tiered Change Control) | Severity determines the change control tier |
| Quality Manual §17 (Knowledge Gaps) | Unknown root causes documented as knowledge gaps |

## 7. Records

All corrective action records are retained indefinitely in the Git repository. They provide:

- Evidence of systematic problem resolution (ISO 9001:2015 clause 10.2.2)
- Input for management review (ISO 9001:2015 clause 9.3)
- A failure memory register (Indian Railways principle) consulted at project starts

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release — ISO 9001:2015 clause 10.2 alignment |
