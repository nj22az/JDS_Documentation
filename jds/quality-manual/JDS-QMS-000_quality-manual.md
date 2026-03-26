# JDS Quality Manual

| | |
|---|---|
| **Document No.** | JDS-QMS-000 |
| **Revision** | F |
| **Date** | 2026-03-26 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |
| **Approved by** | Nils Johansson |

---

## 1. Purpose

This Quality Manual is the top-level governing document of the Johansson Documentation System (JDS). It defines the rules, standards, and responsibilities that control all documentation and deliverables produced under The Office of Nils Johansson.

**This document is the authority.** Every procedure, template, and record in JDS traces back to a requirement defined here. If a procedure contradicts this manual, this manual wins.

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
| **Approver** | Authorises the document for use. In small organisations, one person may hold multiple roles. |

### 3.2 Authority

The system owner holds all three roles by default. When collaborators are involved, review and approval responsibilities must be explicitly assigned and recorded on the document. The document header always shows who owns, reviewed, and approved it.

### 3.3 Quality Responsibility

Every document has a named owner who is personally responsible for its accuracy and currency. This is always documented in the document header. No document exists without clear ownership — if a document has no owner, it is treated as a nonconformance and assigned one immediately.

## 4. Quality Policy

> We produce engineering work that is accurate, traceable, and professionally documented. Every document is written clearly enough for someone unfamiliar with the project — and unfamiliar with engineering — to understand its purpose and content. We maintain our documentation system not because it's required, but because good documentation is good engineering.

**Plain language requirement:** JDS documents must be readable by anyone. If a concept requires specialist knowledge, explain it in the document. Never assume the reader shares your background. This system is built to survive being handed to someone with no context — that is the test of good documentation.

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

### 6.4 Supported File Formats

JDS documents may exist in multiple formats depending on purpose:

| Format | Extension | Use | Controlled Copy? |
|--------|-----------|-----|-----------------|
| **Markdown** | `.md` | Primary format for all JDS documents | Yes (Git) |
| **Excel** | `.xlsx` | Timesheets, expense reports, mileage logs — any document requiring formulas | Working copy; markdown template is reference |
| **PDF** | `.pdf` | Client deliverables, printed copies | No (always marked UNCONTROLLED COPY) |
| **Word** | `.docx` | Client-facing documents when required | No (markdown is source of truth) |

**Rules:**
1. Every document type has a **markdown template** in JDS as the reference specification
2. Excel workbooks are generated by `scripts/generate-office-docs.py` following JDS visual standards
3. PDFs are generated by `scripts/md2pdf.py` or `scripts/md2letter.py`
4. The **Git repository** is always the controlled copy — all other formats are uncontrolled
5. Excel/Word files are tracked in Git but the markdown template defines the structure

### 6.5 Storage

All current documents are stored in this Git repository. Git provides:
- Full version history of every change
- Traceability of who changed what and when
- Ability to recover any previous version
- Branching for draft work before approval

### 6.6 Backup

The repository is hosted on GitHub, providing remote backup. Local copies should also be maintained.

### 6.7 Archive

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

## 8. Complete Document Sets

Every project type has a defined **Complete Document Set** — the full list of documents that must exist for the project to be considered finished. The set is defined at the start of the project, not discovered at the end.

The full definitions are in [JDS-PRO-006](../procedures/JDS-PRO-006_project-komplekt.md).

**The principle:** A project with missing documents is not a finished project, no matter how good the design or code is. If the documentation is incomplete, the work is incomplete.

## 9. 5S Document Management

The documentation system is maintained using the 5S methodology adapted for document management:

| Step | Application to JDS |
|------|--------------------|
| **Sort** | Remove unnecessary documents. Retire what's unused. |
| **Set in order** | Every document has a defined place and naming convention. |
| **Shine** | Review documents for accuracy. Fix errors and broken links. |
| **Standardise** | Use templates consistently. Enforce header and format standards. |
| **Sustain** | Quarterly audits and annual reviews to maintain discipline. |

The full audit procedure is in [JDS-PRO-005](../procedures/JDS-PRO-005_document-review-audit.md).

## 10. Before/After Change Documentation

When making significant changes to any document, record both the previous state and the new state. This continuous improvement practice makes changes visible and reviewable.

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

## 13. Corrective Action

When nonconformances are found — whether in deliverables, documentation, or processes — they are systematically investigated and corrected using [JDS-PRO-008](../procedures/JDS-PRO-008_corrective-action.md). This procedure satisfies ISO 9001:2015 clause 10.2 and ensures:

- Immediate containment of the problem
- Root cause analysis using the 5 Whys method
- Corrective action to prevent recurrence
- Horizontal deployment (Samsung principle) — checking where else the same problem could occur
- Tracking in the [Corrective Action Log](../registry/corrective-action-log.md)

## 14. Continuous Improvement

**JDS is a self-improving system.** Every session of work must leave the system at least as good as it was found — preferably better. This is not optional. It is enforced by the validator, tracked in the changelog, and audited quarterly.

### 14.1 Improvement Sources

Improvements come from seven defined channels:

1. **Lessons learned** — during or after any project
2. **Errors and near-misses** — found in deliverables or documentation
3. **Feedback** — from clients, collaborators, or anyone using the system
4. **5S audits** — quarterly automated checks (see §9)
5. **Management review** — annual system review (see §12)
6. **Corrective actions** — findings from nonconformance investigations (see §13)
7. **Technology absorption** — study of external tools, methods, and standards (see §14.2)

### 14.2 Technology Absorption

When new tools, methods, or standards are studied, the decision is documented:

| Question | Required answer |
|----------|----------------|
| What was studied? | Name, source, purpose |
| What was adopted? | Specific elements and why |
| What was adapted for JDS? | How it was modified to fit |
| What was rejected? | What didn't fit and why |

This builds a compounding knowledge base. Decisions are recorded in the [JDS CHANGELOG](../CHANGELOG.md).

### 14.3 Self-Improvement Enforcement

Every work session must follow this cycle:

1. **Before starting work:** Run `python3 scripts/jds-validate.py` to check system health
2. **During work:** If you find something broken, fix it now — don't leave it for later
3. **Before committing:** Run `python3 scripts/jds-validate.py --quick` to catch regressions
4. **Before ending:** Run the full validator again. Fix any errors. If you improved the system, update the version and changelog.

**The enforcement chain:**
- The **validator** catches structural problems automatically
- The **corrective action log** tracks problems that need investigation
- The **changelog** records what changed and why
- The **management review** ensures the whole system is working
- **CLAUDE.md** instructs AI assistants to follow these same rules

If an issue is found that the validator should have caught, the validator must be updated. If a template caused a problem, the template must be fixed. The system never makes the same mistake twice.

### 14.4 How to Propose Changes to JDS

Anyone — including future collaborators — can propose changes to JDS itself:

1. **Small fixes** (typos, broken links, formatting): Fix directly. Commit with a descriptive message.
2. **Procedure changes** (new rules, modified workflows): Create a draft revision of the affected document. Record the rationale in the revision history.
3. **New procedures or templates**: Follow [JDS-PRO-001](../procedures/JDS-PRO-001_document-creation.md). Register in the document registry. Log in the changelog.
4. **Structural changes** (new categories, new folder layouts): Require a Quality Manual revision (this document). Record the rationale here.

**No change to JDS is too small to track.** Every change — even a typo fix — gets a Git commit with a clear message.

## 15. Language Policy

JDS is written entirely in **English**. JDS defines its own terminology and is the authority on how concepts are named within this system.

### 15.1 Rules

1. **All JDS documents are in English.** No exceptions.
2. **JDS owns its terminology.** Where JDS has adopted concepts from other traditions (Swedish regulation, Japanese design, Russian documentation), the JDS English term is the primary term.
3. **Foreign terms are never primary labels.** If a concept originated from a foreign source, the English JDS term comes first. The foreign origin may be noted in parentheses for traceability, but only in reference documents — never in working procedures.
4. **Regulatory traceability is separate.** When JDS procedures implement regulatory requirements, the regulatory source is documented in a separate traceability matrix, not embedded in the working document.

### 15.2 Terminology Map

| JDS Term (authoritative) | Origin | Foreign Term (reference only) |
|---|---|---|
| Active Space | Japanese information design | Ma (間) |
| Compartment Design | Japanese information design | Bento |
| Visual Explanation | Japanese information design | Zukai (図解) |
| Craft Precision | Japanese manufacturing | Monozukuri |
| Complete Document Set | Russian ESKD | Komplekt |
| Ongoing Maintenance Program | Swedish regulation AFS 2017:3 | Fortlöpande Tillsyn (FLT) |
| Supervision Checklist | Swedish regulation AFS 2017:3 | Tillsynsprotokoll |
| Inspection Plan | Swedish regulation AFS 2017:3 | Kontrollplan |

### 15.3 Rationale

JDS draws on the best practices of many engineering traditions worldwide. By adopting these concepts into English under JDS authority, the system becomes universally accessible while preserving full traceability to its sources.

## 16. Information Design

Documents are not just carriers of information — they are engineered artifacts. The visual presentation of a document is inseparable from its content. JDS follows world-class information design principles, codified in [JDS-PRO-007](../procedures/JDS-PRO-007_information-design.md).

**Core visual principles:**
- **Active Space** — meaningful white space that organises information
- **Compartment Design** — self-contained sections forming a complete whole
- **Visual Explanation** — if you can't diagram it, you don't understand it
- **Colour is Language** — every colour means something, used consistently, never decoratively
- **Three-level reading** — every document works at glance (0.5s), scan (5s), and read (minutes) levels

> *The quality of your documentation is the visible surface of the quality of your engineering.* — Craft Precision principle

## 17. Heritage and Reuse

When starting a new project, explicitly identify what is reused from previous work versus what is new. Only fully document new elements. Reference previous project documentation for heritage items. This practice, drawn from ISRO's frugal engineering tradition, can reduce documentation effort by 50–70% on repeat projects.

Implementation: every project README should include a "Heritage" section listing reused elements and their source.

## 18. Tiered Change Control

Not all changes deserve the same documentation overhead. JDS uses three tiers, adapted from Embraer's aerospace practice:

| Tier | Scope | Process |
|------|-------|---------|
| **Safety-Critical** | Changes affecting safety, structural integrity, or regulatory compliance | Full revision process (JDS-PRO-002), review, registry update |
| **Quality-Affecting** | Changes to technical content, calculations, or specifications | Revision with documented rationale |
| **Administrative** | Typos, formatting, broken links | Git commit with descriptive message, same revision letter |

## 19. Knowledge Gaps and Documentation Confidence

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

## 20. Design Principles

JDS is built on 21 principles drawn from the best documentation practices worldwide. Each principle is explained in plain language so anyone can understand and apply it.

| # | Principle | What it means | How JDS enforces it |
|---|-----------|---------------|---------------------|
| 1 | **One page per topic** | Keep documents focused. If it's too long, split it. | Templates enforce structure. |
| 2 | **Complete document sets** | Define all required documents at project start, not at the end. | [JDS-PRO-006](../procedures/JDS-PRO-006_project-komplekt.md) |
| 3 | **5S for documents** | Regularly sort, organise, clean, standardise, and maintain documents. | Quarterly audits via [JDS-PRO-005](../procedures/JDS-PRO-005_document-review-audit.md) |
| 4 | **Single source of truth** | One place, one version. The Git main branch is the truth. | §6.3 Controlled copies |
| 5 | **Self-describing codes** | Document numbers tell you the type, domain, and sequence at a glance. | [JDS-QMS-001](JDS-QMS-001_document-numbering.md) |
| 6 | **Before/after tracking** | Every change is documented with what it was and what it became. | Git diffs + revision history tables |
| 7 | **Personal accountability** | Every document has a named owner. No orphan documents. | Document header (mandatory) |
| 8 | **Risk-based control** | Important documents get thorough review. Minor docs get lighter treatment. | §18 Tiered Change Control |
| 9 | **Craft precision** | The document itself reflects professional pride. Presentation matters. | [JDS-PRO-007](../procedures/JDS-PRO-007_information-design.md) |
| 10 | **Right amount** | Not too much documentation, not too little. Just enough to be complete. | Management review (§12) |
| 11 | **Thorough once** | Document it once, document it completely. Don't leave gaps to fill later. | Complete document sets (§8) |
| 12 | **Heritage reuse** | Only fully document what is new. Reference previous work for the rest. | Project README "Heritage" section |
| 13 | **Clear intent** | Every project starts with a clear statement of what success looks like. | Project README scope statement |
| 14 | **Reference projects** | Designate the best project as a model. For similar work, document only deviations. | Golden project pattern |
| 15 | **Design vs. as-found** | Always document both what was intended and what was actually found. | Inspection reports, field logs |
| 16 | **Zero ambiguity** | A specification should leave nothing to interpretation. | Templates + review process |
| 17 | **Horizontal deployment** | When something goes wrong, ask: where else could this happen? | Corrective action process (§13) |
| 18 | **Active space** | White space organises information. Never fill space for the sake of filling it. | [JDS-PRO-007](../procedures/JDS-PRO-007_information-design.md) |
| 19 | **Lifecycle documentation** | Documents follow equipment or projects from start to retirement. | Archive process (§6.7) |
| 20 | **Knowledge gaps** | Explicitly document what you don't know. Uncertainty is not weakness — hiding it is. | §19 Knowledge Gaps |
| 21 | **Failure memory** | Maintain a failure register. Consult it before starting every new project. | [Corrective Action Log](../registry/corrective-action-log.md) |

## 21. Repository Structure

JDS defines not only how documents are written, but how they are stored. The repository is the physical implementation of the system. Its structure is not arbitrary — it is a design decision enforced by the validator.

### 21.1 Four Root Folders

Everything in the repository lives in one of four folders:

| Folder | Purpose | Contains |
|--------|---------|----------|
| `jds/` | **System** — The rules | Quality manual, procedures, templates, registry, assets, examples |
| `projects/` | **Work** — The output | Engineering projects, 3D models, blog, software |
| `scripts/` | **Tools** — The automation | Validators, PDF generators, document generators |
| `personal/` | **Personal** — Non-system content | CV, collections, archive (not document-numbered) |

### 21.2 Rules

1. **No files at root** except `README.md`, `CLAUDE.md`, `.gitignore`, and configuration files.
2. **Every folder has a README.md** explaining its purpose. An unexplained folder is a defect.
3. **New project types** must fit into the four-folder structure. If they don't, propose a structural change via §14.4.
4. **The validator checks this.** Folder structure violations are flagged automatically by `scripts/jds-validate.py`.

### 21.3 Universal Project Folder Rules

Every project — whether it's an engineering project, a 3D model, a software tool, or a personal collection — follows the same structural principles:

1. **One folder per project.** Every distinct piece of work gets its own folder.
2. **Every folder has a README.md.** The README is the project card. It describes what this is, what's inside, and how to use it.
3. **Subfolders by purpose, not by file type.** Organise by what the files do, not what format they are in.
4. **No loose files.** Every file lives in a named subfolder or is documented in the README.
5. **Shared resources get a `_shared-references/` folder.** Cross-project materials go here, prefixed with underscore so they sort first.

### 21.4 Standard Project Folder Pattern

This is the generic pattern. Adapt it to your project type — not every project needs every subfolder, but the pattern stays the same.

```
project-name/
├── README.md               ← Project card (always required)
├── source/                  ← Working files, source code, editable formats
├── exports/                 ← Generated output (PDFs, STL, compiled binaries)
├── references/              ← Input materials (datasheets, standards, research)
├── documentation/           ← Manuals, guides, specifications
├── notes/                   ← Working notes, decisions, meeting records
└── CHANGELOG.md             ← Change history (for projects with revisions)
```

### 21.5 Project Type Locations

| Project type | Location pattern |
|-------------|-----------------|
| Engineering projects | `projects/JDS-PRJ-[DOM]-NNN_name/` |
| 3D models | `projects/3d-modeling/JDS-DWG-[DOM]-NNN_name/` |
| Blog | `projects/blog/` |
| Software | `projects/software/project-name/` |
| Personal collections | `personal/collections/collection-name/` |

### 21.6 Collection Folder Pattern

Collections (archives, libraries, curated sets) follow a two-level structure:

```
collection-name/
├── README.md               ← Collection overview, naming conventions, rules
├── _shared-references/      ← Cross-item resources
└── category/                ← Group by logical category
    └── item-name/           ← One folder per item
        ├── README.md        ← Item card (metadata, status, notes)
        ├── [content]/       ← The actual files, organised by purpose
        └── ...
```

Every item gets its own folder and README. The README is the source of truth for that item — even if the actual files are stored elsewhere (too large for Git, external storage), the README documents what exists and where to find it.

## 22. Offline Resilience

JDS is designed to work without an internet connection. The repository is the system — not a website, not a cloud service.

### 22.1 Principles

1. **Everything lives in the repo.** Procedures, templates, examples, tools — all stored locally. No external dependencies for core system operation.
2. **Markdown is the primary format** because it is readable in any text editor, on any operating system, without special software.
3. **Scripts are self-contained.** Automation tools use Python standard libraries where possible. External dependencies are documented and installable offline.
4. **PDFs are generated locally.** The PDF generators run on the local machine. No cloud rendering services.

### 22.2 How to Use JDS Offline

1. Clone the repository to your local machine
2. All procedures, templates, and references are in `jds/`
3. Create documents using templates from `jds/templates/`
4. Run validation with `python3 scripts/jds-validate.py`
5. Generate PDFs with `python3 scripts/md2pdf.py <file.md>`
6. Commit and push when connectivity is restored

### 22.3 What Requires Connectivity

Only these operations require an internet connection:
- Pushing commits to GitHub (backup and collaboration)
- GitHub Pages blog deployment
- Installing Python packages (one-time setup)

Everything else — reading, writing, validating, generating PDFs — works offline.

## 23. Glossary

JDS uses terms that may not be familiar to every reader. This glossary defines them in plain language.

| Term | Meaning |
|------|---------|
| **JDS** | Johansson Documentation System — the documentation and quality management system defined in this repository |
| **QMS** | Quality Management System — the set of policies and processes that ensure consistent quality |
| **Repository (repo)** | A folder tracked by Git version control. Contains all files, their history, and their relationships |
| **Git** | Version control software that tracks every change to every file, who made it, and when |
| **Markdown (.md)** | A plain-text format that can be read in any text editor. Headings use `#`, bold uses `**`, links use `[text](url)` |
| **Revision** | A controlled update to a document. Tracked with letters: A, B, C, D... |
| **Registry** | The master list of all documents in the system (`jds/registry/document-register.md`) |
| **Validator** | A script that automatically checks the system for errors (`scripts/jds-validate.py`) |
| **STEP (.step)** | A file format for 3D models that preserves exact geometry. Used for CAD interchange between different software |
| **STL (.stl)** | A file format for 3D models that stores the surface as triangles. Universal format for 3D printing |
| **3MF (.3mf)** | A modern 3D printing file format that supports colours, materials, and metadata |
| **PDF** | Portable Document Format — a fixed-layout format for viewing and printing. In JDS, PDFs are always uncontrolled copies |
| **Controlled copy** | The authoritative version of a document (always the Git repository main branch) |
| **Uncontrolled copy** | Any export, printout, or emailed version. May be outdated. Marked "UNCONTROLLED COPY" |
| **Complete document set** | The defined list of all documents that must exist for a project to be considered finished |
| **5S** | A five-step maintenance method: Sort, Set in order, Shine, Standardise, Sustain |
| **Corrective action** | A formal process to investigate a problem, find its root cause, and prevent it from happening again |
| **Nonconformance** | Anything that doesn't meet the requirements — a missing document, a broken link, a wrong revision |
| **Domain code** | A three-letter code identifying the engineering discipline (MEC=Mechanical, ELE=Electrical, etc.) |
| **Category code** | A three-letter code identifying the document type (PRO=Procedure, RPT=Report, DWG=Drawing, etc.) |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
| B | 2026-03-25 | Nils Johansson | Added Komplekt concept, 5S document management, classification tiers, before/after tracking, design principles from global best practices, technology absorption, archive structure |
| C | 2026-03-25 | Nils Johansson | Added Information Design (Japanese), Heritage & Reuse (ISRO), Tiered Change Control (Embraer), Knowledge Gaps & Documentation Confidence (Petrobras/Baikonur), expanded design principles table with 21 principles from 15+ global traditions |
| D | 2026-03-25 | Nils Johansson | Added Corrective Action section (§13) with reference to JDS-PRO-008, ISO 9001:2015 clause 10.2 alignment |
| E | 2026-03-25 | Nils Johansson | Added Language Policy (§15). All foreign loan words replaced with JDS-owned English terms. Added Supported File Formats (§6.4) — Excel, PDF, Word alongside Markdown. Sections renumbered. |
| F | 2026-03-26 | Nils Johansson | Strengthened self-improvement enforcement (§14). Added Repository Structure (§21), Offline Resilience (§22), Glossary (§23). Plain language requirement added to Quality Policy (§4). Removed company-specific language for reusability. Design principles rewritten with enforcement links. How to Propose Changes (§14.4) added. |
