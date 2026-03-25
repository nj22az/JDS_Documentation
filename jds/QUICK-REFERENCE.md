# JDS Quick Reference

One-page cheat sheet. For full details, see the [Quality Manual](quality-manual/JDS-QMS-000_quality-manual.md).

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

Skip: I, O, Q, S, X, Z (avoid confusion with numbers and other letters)

---

## New Document Checklist

1. **Pick a number** — next available in [document-register.md](registry/document-register.md)
2. **Copy the template** — from [templates/](templates/) for your document type
3. **Fill the status block** — Doc No, Rev A, DRAFT, Date, Author
4. **Register it** — add a row to [document-register.md](registry/document-register.md)
5. **Commit** — run `python3 scripts/jds-validate.py --quick` first

## Status Block Format

Every JDS document starts with this:

```markdown
| **Document No.** | JDS-RPT-MEC-001 |
| **Revision**     | A                |
| **Status**       | DRAFT            |
| **Date**         | 2026-03-25       |
| **Author**       | Nils Johansson   |
```

Valid statuses: **DRAFT** → **CURRENT** → **SUPERSEDED** / **VOID**

---

## Where Things Go

| Document type | Folder |
|---------------|--------|
| Engineering projects | `projects/JDS-PRJ-[DOM]-NNN_name/` |
| 3D models & drawings | `3d-modeling/JDS-DWG-[DOM]-NNN_name/` |
| Blog posts | `blog/_posts/YYYY-MM-DD-slug.md` |
| System procedures | `jds/procedures/` |
| Templates | `jds/templates/[type]/` |
| Examples | `jds/examples/[type]/` |
| Timesheets & expenses | Generated on demand (not stored in Git) |

---

## Common Commands

```bash
# Generate a PDF from markdown
python3 scripts/md2pdf.py <input.md> [output.pdf]

# Generate a letter PDF
python3 scripts/md2letter.py <input.md> [output.pdf]

# Generate office documents (timesheet, expense, mileage)
python3 scripts/generate-office-docs.py timesheet|expense|mileage|all [output]

# Generate PDF from Excel workbook
python3 scripts/office2pdf.py <input.xlsx> [output.pdf]

# Run system audit (do this before every commit)
python3 scripts/jds-validate.py

# Quick registry check only
python3 scripts/jds-validate.py --quick
```

---

## 3D Model Mandatory Exports

Every 3D project must export all three: **STEP + 3MF + STL**

Folder structure: `source/` `exports/` `references/` `renders/`

---

*Full system reference: [jds/README.md](README.md) | Quality Manual: [QMS-000](quality-manual/JDS-QMS-000_quality-manual.md) | Document Register: [registry](registry/document-register.md)*
