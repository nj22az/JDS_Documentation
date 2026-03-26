# JDS Quick Reference

One-page cheat sheet for daily use. For full details, see the [Quality Manual](quality-manual/JDS-QMS-000_quality-manual.md).

---

## Document Number Format

```
Technical:  JDS-[CAT]-[DOM]-[NNN]    e.g. JDS-DWG-MEC-003  (3rd mechanical drawing)
System:     JDS-[CAT]-[NNN]          e.g. JDS-PRO-007      (Information Design Standard)
With rev:   JDS-RPT-MAR-001 Rev B
```

## Category Codes

| QMS | PRO | RPT | MAN | DWG | PRJ | LOG | COR | BLG | TSH | EXP | TMP |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Quality | Procedures | Reports | Manuals | Drawings | Projects | Logs | Letters | Blog | Timesheets | Expenses | Templates |

## Domain Codes

| MEC | MAR | AUT | ELE | PIP | STR | TST | FAB | THR | SFW | GEN |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| Mechanical | Marine | Automation | Electrical | Piping | Structural | Testing | Fabrication | Thermal | Software | General |

## Revision Sequence

```
A  B  C  D  E  F  G  H  J  K  L  M  N  P  R  T  U  V  W  Y
```

**Why these letters are skipped:** I (looks like 1), O (looks like 0), Q (looks like O), S (looks like 5), X (used as a cancel/void symbol), Z (looks like 2). This prevents misreading when printed or handwritten.

---

## New Document Checklist

1. **Pick a number** — next available in [document-register.md](registry/document-register.md)
2. **Copy the template** — from [templates/](templates/) for your document type
3. **Fill the status block** — Doc No, Rev A, DRAFT, Date, Author
4. **Register it** — add a row to [document-register.md](registry/document-register.md)
5. **Validate** — run `python3 scripts/jds-validate.py --quick` before committing

## Status Block Format

Every JDS document starts with this header:

```markdown
| **Document No.** | JDS-RPT-MEC-001 |
| **Revision**     | A                |
| **Status**       | DRAFT            |
| **Date**         | 2026-03-25       |
| **Author**       | [Author Name]    |
```

Valid statuses: **DRAFT** → **CURRENT** → **SUPERSEDED** / **VOID**

---

## Project Folder Pattern

Every project follows this structure (adapt as needed):

```
project-name/
├── README.md           ← Always required — describes the project
├── source/             ← Working files, source code, editable formats
├── exports/            ← Generated output (PDFs, STL, etc.)
├── references/         ← Input materials (datasheets, standards)
├── documentation/      ← Guides, specifications, manuals
└── CHANGELOG.md        ← Change history (for versioned projects)
```

Full rules: [Quality Manual §21](quality-manual/JDS-QMS-000_quality-manual.md)

## Where Things Go

| What | Where |
|------|-------|
| Engineering projects | `projects/JDS-PRJ-[DOM]-NNN_name/` |
| 3D models & drawings | `projects/3d-modeling/JDS-DWG-[DOM]-NNN_name/` |
| Blog posts | `projects/blog/_posts/YYYY-MM-DD-slug.md` |
| System procedures | `jds/procedures/` |
| Templates | `jds/templates/[type]/` |
| Examples | `jds/examples/` |
| Personal content | `personal/` (not document-numbered) |

---

## Common Commands

```bash
# Validate the system (run before every commit)
python3 scripts/jds-validate.py --quick

# Full system audit (run before ending a work session)
python3 scripts/jds-validate.py

# Generate a PDF from markdown
python3 scripts/md2pdf.py <input.md> [output.pdf]

# Generate a letter PDF
python3 scripts/md2letter.py <input.md> [output.pdf]

# Generate office documents (timesheet, expense, mileage)
python3 scripts/generate-office-docs.py timesheet|expense|mileage|all [output]

# Generate PDF from Excel workbook
python3 scripts/office2pdf.py <input.xlsx> [output.pdf]
```

**Why validate?** The validator checks folder structure, registry consistency, document metadata, naming conventions, internal links, and more. It catches problems automatically so you don't have to remember every rule.

---

## 3D Model Exports

Every 3D project must export all three formats:

| Format | Purpose |
|--------|---------|
| **STEP** (.step) | CAD interchange — preserves exact geometry for use in other CAD software |
| **STL** (.stl) | Universal 3D printing format — surface mesh of triangles |
| **3MF** (.3mf) | Modern 3D printing format — supports colours, materials, metadata |

---

## Key Terms

| Term | Meaning |
|------|---------|
| **JDS** | Johansson Documentation System |
| **Revision** | A controlled update (A, B, C...) |
| **Registry** | Master list of all documents |
| **Validator** | Automated system health checker |
| **Controlled copy** | The Git main branch (the truth) |
| **Uncontrolled copy** | Any PDF, printout, or email (may be outdated) |

---

*Full system reference: [jds/README.md](README.md) | Quality Manual: [QMS-000](quality-manual/JDS-QMS-000_quality-manual.md) | Document Register: [registry](registry/document-register.md)*
