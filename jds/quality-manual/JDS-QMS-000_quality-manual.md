# JDS Quality Manual

| | |
|---|---|
| **Document No.** | JDS-QMS-000 |
| **Revision** | C |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |
| **Approved by** | Nils Johansson |

---

## 1. Purpose

This Quality Manual defines the quality management system (QMS) for The Office of Nils Johansson. It establishes the policies, standards, and responsibilities that govern all engineering documentation and deliverables.

## 2. Scope

This system applies to all work produced under The Office of Nils Johansson, including but not limited to:

- Engineering reports and technical documents
- 3D models and engineering drawings
- Software projects and source code documentation
- Field service records
- Project management documents
- Financial records (timesheets, expenses)
- Client correspondence and proposals

## 3. Organisation

### 3.1 Roles

| Role | Responsibility |
|------|---------------|
| **Document Owner** | The person who creates and maintains a document. Responsible for accuracy and timely updates. |
| **Reviewer** | Checks a document for technical accuracy and completeness before approval. |
| **Approver** | Authorises the document for use. For sole-proprietor operations, this is the owner. |

### 3.2 Authority

As a sole-proprietor engineering practice, Nils Johansson holds all three roles by default. When collaborators are involved, review and approval responsibilities should be explicitly assigned and recorded on the document.

### 3.3 Quality Responsibility

Every document has a named owner who is personally responsible for its accuracy and currency. This is always documented in the document header. This explicit personal accountability (drawn from Chinese quality practice) ensures no document exists without clear ownership.

## 4. Quality Policy

> We produce engineering work that is accurate, traceable, and professionally documented. Every document is written clearly enough for someone unfamiliar with the project to understand. We maintain our documentation system not because it's required, but because good documentation is good engineering.

## 5. Documentation Hierarchy

The JDS documentation is organised in four tiers:

```
Tier 1: Quality Manual (this document)
   ↓    Defines the overall system, policies, and principles

Tier 2: Procedures & Standards (JDS-PRO, JDS-QMS series)
   ↓    Step-by-step instructions for system processes

Tier 3: Templates (JDS-TMP series)
   ↓    Standardised forms and document formats

Tier 4: Records (RPT, TSH, EXP, LOG, etc.)
         Completed documents — the actual work output
```

## 6. Document Control

### 6.1 Numbering

All documents are assigned a unique number following the JDS numbering standard ([JDS-QMS-001](JDS-QMS-001_document-numbering.md)). Numbers are never reused, even if a document is retired.

### 6.2 Revision Control

Documents follow a controlled revision process ([JDS-PRO-002](../procedures/JDS-PRO-002_revision-control.md)):

- **Rev A** = First approved release
- **Rev B, C, D...** = Subsequent approved revisions
- **DRAFT** = Not yet approved for use
- **SUPERSEDED** = Replaced by a newer revision
- **RETIRED** = No longer in use

### 6.3 Document Classification

Every document falls into one of three classification tiers:

| Tier | Meaning | Examples |
|------|---------|---------|
| **Public** | May be shared externally without restriction | Blog posts, published articles, open-source code |
| **Internal** | For internal use only; not for external distribution | Procedures, templates, project documents, quality manual |
| **Confidential** | Sensitive; restricted distribution | Client-specific data, pricing, personal financial records |

**Default classification:** Internal. Documents are Internal unless explicitly marked otherwise.

**Controlled vs. Uncontrolled Copies:** The Git repository (main branch) is always the controlled copy. Anything exported, emailed, or printed is an uncontrolled copy and should be marked accordingly. See [JDS-PRO-005](../procedures/JDS-PRO-005_document-review-audit.md) for details.

### 6.4 Storage

All current documents are stored in this Git repository. Git provides:
- Full version history of every change
- Traceability of who changed what and when
- Ability to recover any previous version
- Branching for draft work before approval

### 6.5 Backup

The repository is hosted on GitHub, providing remote backup. Local copies should also be maintained.

### 6.6 Archive

Retired and superseded documents are moved to the `jds/archive/` folder. They are never deleted — Git never forgets.

## 7. Document Lifecycle

```
DRAFT → REVIEW → APPROVED → [IN USE] → REVISION → APPROVED
                                    ↓
                              SUPERSEDED / RETIRED → ARCHIVE
```

| Stage | Description |
|-------|-------------|
| **DRAFT** | Document is being written. Not for official use. |
| **REVIEW** | Document is complete and being checked for accuracy. |
| **APPROVED** | Document is authorised for use. This is the "live" version. |
| **SUPERSEDED** | A newer revision exists. Kept for reference only. |
| **RETIRED** | Document is no longer relevant. Moved to archive. |

## 8. Komplekt — Complete Document Sets

Every project type has a defined **komplekt** — the complete set of documents that must exist for the project to be considered finished. This concept, drawn from the Russian ESKD tradition, ensures documentation completeness is defined upfront, not discovered after the fact.

The full komplekt definitions are in [JDS-PRO-006](../procedures/JDS-PRO-006_project-komplekt.md).

**The principle:** A project with an incomplete komplekt is not a finished project, regardless of whether the design or code is done.

## 9. 5S Document Management

The documentation system is maintained using the 5S methodology adapted for document management:

| Step | Japanese | Application to JDS |
|------|----------|--------------------|
| **Sort** | Seiri | Remove unnecessary documents. Retire what's unused. |
| **Set in order** | Seiton | Every document has a defined place and naming convention. |
| **Shine** | Seiso | Review documents for accuracy. Fix errors and broken links. |
| **Standardise** | Seiketsu | Use templates consistently. Enforce header and format standards. |
| **Sustain** | Shitsuke | Quarterly audits and annual reviews to maintain discipline. |

The full audit procedure is in [JDS-PRO-005](../procedures/JDS-PRO-005_document-review-audit.md).

## 10. Before/After Change Documentation

When making significant changes to any document, record both the previous state and the new state. This kaizen-inspired practice makes changes visible and reviewable.

In JDS, this is achieved through:
1. **Git diffs** — every change is automatically tracked with before/after
2. **Revision history tables** — the "Description" column explains what changed and why
3. **CHANGELOG** — system-level changes are recorded in `jds/CHANGELOG.md`

## 11. Quality Objectives

| Objective | Measure |
|-----------|---------|
| All deliverables are documented | Every project has a corresponding document trail |
| Documents are findable | Any document can be located in under 60 seconds via the registry |
| Revisions are traceable | Every change has a recorded reason, date, and author |
| Templates are used consistently | All recurring document types use the standard template |
| System is reviewed regularly | Quarterly 5S audits, annual review of QMS procedures |
| Komplekts are complete | Every finished project has a 100% complete komplekt |
| Documents reflect craftsmanship | Documents are professionally formatted and clear |

## 12. Management Review

The documentation system itself shall be reviewed annually (or after significant changes to the business) to ensure it remains:

- Practical and not overly bureaucratic
- Aligned with the type of work being produced
- Up to date with current tools and workflows
- Complete in its coverage of document types

Review findings are recorded in a Management Review Report (JDS-RPT series) or as a Git commit.

## 13. Continuous Improvement

Improvements to the system can come from:

- Lessons learned during projects
- Document errors or near-misses
- Feedback from clients or collaborators
- Quarterly 5S audits
- Annual management review
- Study of external best practices (technology absorption)

All improvement actions are tracked through the revision control process and recorded in the [JDS CHANGELOG](../CHANGELOG.md).

### 13.1 Technology Absorption

When new tools, methods, or standards are studied and adopted, the learning process is documented:
- What was studied
- What was adopted and why
- What was adapted for JDS
- What was rejected and why

This practice, drawn from Chinese engineering tradition, builds a compounding knowledge base over time.

## 14. Information Design

Documents are not just carriers of information — they are engineered artifacts. The visual presentation of a document is inseparable from its content. JDS follows the Japanese information design tradition, codified in [JDS-PRO-007](../procedures/JDS-PRO-007_information-design.md).

**Core visual principles:**
- **Ma (間)** — meaningful white space that organises information
- **Bento box layout** — self-contained compartments forming a complete whole
- **Zukai (図解)** — if you can't diagram it, you don't understand it
- **Colour is language** — every colour means something, used consistently, never decoratively
- **Three-level reading** — every document works at glance (0.5s), scan (5s), and read (minutes) levels

> *The quality of your documentation is the visible surface of the quality of your engineering.* — Monozukuri principle

## 15. Heritage and Reuse

When starting a new project, explicitly identify what is reused from previous work versus what is new. Only fully document new elements. Reference previous project documentation for heritage items. This practice, drawn from ISRO's frugal engineering tradition, can reduce documentation effort by 50–70% on repeat projects.

Implementation: every project README should include a "Heritage" section listing reused elements and their source.

## 16. Tiered Change Control

Not all changes deserve the same documentation overhead. JDS uses three tiers, adapted from Embraer's aerospace practice:

| Tier | Scope | Process |
|------|-------|---------|
| **Safety-Critical** | Changes affecting safety, structural integrity, or regulatory compliance | Full revision process (JDS-PRO-002), review, registry update |
| **Quality-Affecting** | Changes to technical content, calculations, or specifications | Revision with documented rationale |
| **Administrative** | Typos, formatting, broken links | Git commit with descriptive message, same revision letter |

## 17. Knowledge Gaps and Documentation Confidence

For projects at the edge of proven experience, explicitly document what you do NOT know. This practice, drawn from Petrobras' deepwater engineering, prevents the dangerous illusion of complete knowledge.

**Knowledge Gaps section:** Mandatory for complex or novel projects. Must be non-empty. Lists uncertainties, assumptions, and areas requiring further investigation.

**Documentation Confidence Levels** (from Baikonur Cosmodrome practice):

| Level | Meaning |
|-------|---------|
| **Verified** | Based on direct measurement or physical confirmation |
| **Calculated** | Based on engineering analysis with verified inputs |
| **Estimated** | Based on engineering judgment or analogous experience |
| **Assumed** | Based on assumptions that have not been verified |

Use these to mark critical data points in reports and specifications.

## 18. Design Principles

JDS incorporates the best principles from global documentation traditions:

| Principle | Origin | Application |
|-----------|--------|-------------|
| **One page per topic** | Toyota A3 / Korean Bogoser | Keep documents focused; split if too long |
| **Komplekt completeness** | Russian ESKD | Define required documents upfront |
| **5S for documents** | Japanese Lean | Quarterly audit cycle for system health |
| **Single source of truth** | ISO 9001 / Apple DRI | Main branch = the truth. One owner per document. |
| **Self-describing codes** | Siemens KKS / ESKD | Document numbers encode type, domain, and sequence |
| **Before/After tracking** | Japanese Kaizen | Every change documented with previous and new state |
| **Personal accountability** | Chinese quality practice | Named owner on every document |
| **Risk-based control** | ISO 9001:2015 | Safety-critical docs get rigorous review; notes get lighter treatment |
| **Craftsmanship** | Japanese Monozukuri | The document itself reflects professional pride |
| **Lagom** | Swedish tradition | Just the right amount of documentation — not too much, not too little |
| **Grundlichkeit** | German Mittelstand | Document it once, document it completely |
| **Heritage reuse** | ISRO India | Only fully document what is new; reference previous work |
| **Commander's Intent** | Israeli IDF | Every project starts with a clear statement of what success looks like |
| **Golden Project** | Taiwan TSMC | Designate reference projects; document only deviations for similar work |
| **Design vs. As-Found** | DNV Classification | Always document both intended state and actual state |
| **Zero ambiguity** | Swiss precision | A specification should leave nothing to interpretation |
| **Horizontal deployment** | Samsung Korea | When something goes wrong, ask: where else could this happen? |
| **Ma — meaningful space** | Japanese information design | White space organises; never fill space for the sake of filling it |
| **Lifecycle documentation** | NORSOK Norway | Documents follow equipment from cradle to grave |
| **Knowledge gaps** | Petrobras Brazil | Explicitly document what you don't know |
| **Failure memory** | Indian Railways | Maintain a failure register; consult it at every project start |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
| B | 2026-03-25 | Nils Johansson | Added Komplekt concept, 5S document management, classification tiers, before/after tracking, design principles from global best practices, technology absorption, archive structure |
| C | 2026-03-25 | Nils Johansson | Added Information Design (Japanese), Heritage & Reuse (ISRO), Tiered Change Control (Embraer), Knowledge Gaps & Documentation Confidence (Petrobras/Baikonur), expanded design principles table with 21 principles from 15+ global traditions |
