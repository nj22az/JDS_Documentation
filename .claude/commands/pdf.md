Generate a JDS-compliant PDF from a markdown document.

## Input

The user will provide a file path: $ARGUMENTS

If no file path is provided, ask which document to convert.

## Pre-flight Checks

Before generating the PDF, verify the markdown document complies with JDS:

1. **Document header** — Must have the standard JDS metadata table at the top:
   - Document No., Revision, Date, Status, Author (all mandatory)
   - Verify the document number follows JDS-QMS-001 format: `JDS-[CAT]-[DOM]-[NNN]` or `JDS-[CAT]-[NNN]`

2. **Heading hierarchy (PRO-007 §4.1)** — Check that:
   - Only one H1 (the document title)
   - No heading level is skipped (no H1 → H3 without H2)
   - Maximum 4 heading levels used (H1–H4). If H5+ exists, flag it.

3. **Revision history** — Must have a revision history table at the end

4. **Visual content (PRO-007 §7.1)** — For reports (RPT) over 3 pages, check that at least one diagram, table, or visual element exists

5. **Colour usage (PRO-007 §6.2)** — If the document contains HTML colour codes, verify they use only the JDS palette:
   - Navy Blue: #1B3A5C
   - Steel Blue: #4A90A4
   - Signal Red: #C0392B
   - Amber: #D4A017
   - Forest Green: #2E7D32
   - Warm Gray: #8C8C8C

## PDF Generation

Run the JDS PDF generator:

```bash
python3 scripts/md2pdf.py "<file_path>"
```

This script applies the JDS-PRO-007 compliant stylesheet:
- **Typography**: H1 20pt, H2 14pt, H3 12pt, H4 11pt italic, body 10pt (§4.1–4.2)
- **Fonts**: Source Sans Pro / Calibri / Inter + Consolas mono (§4.3)
- **Layout**: A4, margins 25mm L/R, 20mm top, 25mm bottom (§5.1)
- **Colours**: Navy Blue headings, Steel Blue subheadings, Warm Gray metadata (§6.1)
- **Headers**: Document title running header on page 2+, "UNCONTROLLED COPY" top-right (PRO-005 §6)
- **Footer**: Page N of M centred
- **Tables**: Navy Blue headers, alternating row shading, generous padding (§7.3)

## Post-generation

After generating:

1. Report the output file path and size
2. Confirm it is marked as UNCONTROLLED COPY (per JDS-PRO-005 §6 — any PDF outside Git is an uncontrolled copy)
3. Note any PRO-007 compliance issues found during pre-flight

## Monozukuri Check (PRO-007 §8.1)

Before reporting success, mentally verify:
- [ ] Headings follow the 4-level hierarchy consistently
- [ ] White space (ma) separates sections clearly
- [ ] Status block is complete
- [ ] The document works at all three reading levels (glance, scan, read)

## If dependencies are missing

If `weasyprint` or `markdown` are not installed:
```bash
pip3 install weasyprint markdown
```
