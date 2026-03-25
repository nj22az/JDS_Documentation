# JDS Automation Tools

Python scripts that power the Johansson Documentation System.

## Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `jds-validate.py` | Automated 5S audit (100+ checks) | `python3 scripts/jds-validate.py` |
| `md2pdf.py` | JDS document to PDF | `python3 scripts/md2pdf.py <file.md> [output.pdf]` |
| `md2letter.py` | Letter template to PDF | `python3 scripts/md2letter.py <file.md> [output.pdf]` |
| `office2pdf.py` | Excel workbook to PDF | `python3 scripts/office2pdf.py <file.xlsx> [output.pdf]` |
| `generate-office-docs.py` | Generate Excel workbooks | `python3 scripts/generate-office-docs.py timesheet\|expense\|mileage\|all` |
| `logo-variants.py` | Generate SVG logo colour variants | `python3 scripts/logo-variants.py` |

## Dependencies

```bash
pip3 install openpyxl weasyprint markdown
```

## Validation Modes

```bash
python3 scripts/jds-validate.py           # Full audit (run before ending a session)
python3 scripts/jds-validate.py --quick    # Registry check only (run before every commit)
python3 scripts/jds-validate.py --fix      # Show suggested fixes for errors
```

## Logo Swapping

Set `JDS_LOGO_PATH` environment variable to use a client logo instead of the default Johansson Engineering stamp:

```bash
JDS_LOGO_PATH=/path/to/client-logo.png python3 scripts/generate-office-docs.py timesheet
```
