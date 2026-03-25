#!/usr/bin/env python3
"""JDS PDF Generator — JDS-PRO-007 Information Design Standard (Rev B).

Converts JDS markdown documents to PDF with Japanese information design
principles: Ma (meaningful space), Bento (compartmented layout), Zukai
(visual clarity), Monozukuri (visible craftsmanship), and Ku (emptiness
as receptive potential).

Design references:
  - Apple: optical hierarchy, dynamic tracking, weight discipline
  - Toyota A3: constraint-driven clarity, no information waste
  - Bauhaus: grid system, geometric precision, form follows function
  - Kenya Hara / MUJI: emptiness over minimalism, white as structure
  - Bosch: WCAG accessibility, systematic design tokens
  - DNV: classification document hierarchy, formal page architecture
  - Instron: engineering report structure, sequential numbering

Usage: python3 md2pdf.py <input.md> [output.pdf]
"""

import sys
import os
import re
import markdown
from weasyprint import HTML

# ---------------------------------------------------------------------------
# Extract document metadata from the markdown header table
# ---------------------------------------------------------------------------

def extract_metadata(md_text):
    """Pull Doc No, Rev, Status, Date, Author from the JDS header table."""
    meta = {}
    patterns = {
        'doc_no': r'\*\*Document No\.\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'revision': r'\*\*Revision\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'status': r'\*\*Status\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'date': r'\*\*Date\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'author': r'\*\*Author\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, md_text, re.MULTILINE)
        if match:
            meta[key] = match.group(1).strip()
    return meta


# ---------------------------------------------------------------------------
# JDS-PRO-007 Rev B — World-Class Stylesheet
#
# Design philosophy:
#   Ma (間)        — Space has meaning. Every gap is a 6pt multiple.
#   Bento (弁当)   — Compact compartments. Each section self-contained.
#   Zukai (図解)   — Visual clarity through structure, not decoration.
#   Monozukuri     — Precision visible in every alignment choice.
#   Ku (空)        — Emptiness is not absence. It is receptive potential.
#
# Design tokens (6pt baseline grid):
#   1 unit = 6pt   |   2 units = 12pt   |   3 units = 18pt
#   4 units = 24pt  |   5 units = 30pt
#
# Colour tokens:
#   Navy     #1B3A5C  — Authority, primary headings
#   Steel    #4A90A4  — Supporting, subheadings
#   Dark     #222222  — Body text (16.8:1 contrast)
#   Gray600  #444444  — H4, secondary text
#   Warm     #8C8C8C  — Metadata, annotations
#   Light    #AAAAAA  — Uncontrolled copy watermark
#   Tint     #f0f3f6  — Table header background
#   Subtle   #fafbfc  — Alternating row tint
#   Divider  #e0e0e0  — Table cell borders
#   Rule     #cccccc  — Section dividers
#   BgBlock  #f7f9fb  — Blockquote background
#   BgCode   #f5f5f5  — Inline code background
#
# References: PRO-007 §3–§14
# ---------------------------------------------------------------------------

CSS = """
/* ═══════════════════════════════════════════════════════════════════════════
   PAGE SETUP — §5.1, §10.1 Page Architecture
   ═══════════════════════════════════════════════════════════════════════════ */

@page {{
    size: A4;
    margin: 22mm 22mm 20mm 22mm;

    /* --- Header zone ---------------------------------------------------- */
    @top-left {{
        content: "{doc_no}";
        font-size: 7.5pt;
        font-weight: 600;
        color: #1B3A5C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.5pt;
        border-bottom: 0.25pt solid #e0e0e0;
        padding-bottom: 4pt;
    }}
    @top-center {{
        content: string(doc-title);
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-bottom: 0.25pt solid #e0e0e0;
        padding-bottom: 4pt;
    }}
    @top-right {{
        content: "UNCONTROLLED COPY";
        font-size: 6.5pt;
        color: #aaa;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.3pt;
        text-transform: uppercase;
        border-bottom: 0.25pt solid #e0e0e0;
        padding-bottom: 4pt;
    }}

    /* --- Footer zone ---------------------------------------------------- */
    @bottom-left {{
        content: "Rev {revision}";
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.25pt solid #e0e0e0;
        padding-top: 4pt;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 7.5pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.25pt solid #e0e0e0;
        padding-top: 4pt;
    }}
    @bottom-right {{
        content: "{date}";
        font-size: 7pt;
        color: #8C8C8C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.25pt solid #e0e0e0;
        padding-top: 4pt;
    }}
}}

/* First page: title visible in body, so suppress running title in header */
@page :first {{
    @top-center {{ content: none; }}
}}

/* ═══════════════════════════════════════════════════════════════════════════
   BODY — §4.2, §9.1 Baseline Grid (6pt)
   ═══════════════════════════════════════════════════════════════════════════ */

body {{
    font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    font-size: 10pt;
    line-height: 1.5;
    color: #222;
    text-align: left;
    orphans: 3;
    widows: 3;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HEADING HIERARCHY — §4.1 (4 levels max), §11.1 Tracking, §11.2 Weights
   ═══════════════════════════════════════════════════════════════════════════ */

h1 {{
    font-size: 20pt;
    font-weight: 700;
    color: #1B3A5C;
    border-bottom: 2pt solid #1B3A5C;
    padding-bottom: 6pt;
    margin: 0 0 6pt 0;
    string-set: doc-title content();
    letter-spacing: -0.3pt;
    line-height: 1.2;
}}

h2 {{
    font-size: 14pt;
    font-weight: 700;
    color: #1B3A5C;
    border-bottom: 0.5pt solid #ccc;
    padding-bottom: 3pt;
    margin: 24pt 0 12pt 0;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11.5pt;
    font-weight: 600;
    color: #4A90A4;
    margin: 18pt 0 6pt 0;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10.5pt;
    font-weight: 600;
    font-style: italic;
    color: #444;
    margin: 12pt 0 6pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   METADATA IDENTITY STRIP — §10.2 Title Page Zone (Bento)
   Compact, refined. Not a data table — an identity strip.
   ═══════════════════════════════════════════════════════════════════════════ */

table:first-of-type {{
    width: auto;
    min-width: 50%;
    max-width: 70%;
    margin: 6pt 0 18pt 0;
    font-size: 8.5pt;
    border: none;
    border-top: 2pt solid #1B3A5C;
    border-bottom: 1pt solid #ccc;
}}

table:first-of-type th,
table:first-of-type td {{
    border: none;
    border-bottom: 0.5pt solid #e0e0e0;
    padding: 3pt 10pt 3pt 8pt;
    background: none;
}}

table:first-of-type th {{
    background: none;
    color: #8C8C8C;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 7pt;
    letter-spacing: 0.5pt;
    width: 28%;
    vertical-align: top;
}}

table:first-of-type td {{
    color: #222;
    font-weight: 500;
}}

table:first-of-type tr:nth-child(even) {{
    background: none;
}}

table:first-of-type tr:last-child th,
table:first-of-type tr:last-child td {{
    border-bottom: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   DATA TABLES — §7.3, §12.1 Sequential Numbering
   Light header, clean lines. Refined precision, not heavy blocks.
   ═══════════════════════════════════════════════════════════════════════════ */

table {{
    border-collapse: collapse;
    width: 100%;
    margin: 6pt 0 12pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
    border-top: 1.5pt solid #1B3A5C;
    border-bottom: 1pt solid #1B3A5C;
}}

th {{
    background-color: #f0f3f6;
    color: #1B3A5C;
    font-weight: 600;
    font-size: 8.5pt;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    padding: 6pt 8pt;
    border-bottom: 1pt solid #1B3A5C;
    border-left: none;
    border-right: none;
}}

td {{
    padding: 5pt 8pt;
    border-bottom: 0.5pt solid #e0e0e0;
    border-left: none;
    border-right: none;
    vertical-align: top;
    text-align: left;
}}

tr:nth-child(even) {{
    background-color: #fafbfc;
}}

tr:last-child td {{
    border-bottom: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   REVISION HISTORY TABLE — §12.2 Distinct from data tables
   Last table in document uses identity strip style (compact, metadata feel)
   ═══════════════════════════════════════════════════════════════════════════ */

/* We target "Revision History" via the last table heuristic. Since CSS
   cannot reliably select "last table", we style all tables the same but
   provide a .rev-history class for HTML post-processing. The md2pdf.py
   script wraps the last table in a div.rev-history container. */

div.rev-history table {{
    width: auto;
    min-width: 70%;
    max-width: 100%;
    font-size: 8.5pt;
    border-top: 1.5pt solid #1B3A5C;
    border-bottom: 1pt solid #ccc;
}}

div.rev-history th {{
    background-color: transparent;
    color: #8C8C8C;
    font-size: 7.5pt;
    border-bottom: 0.5pt solid #ccc;
}}

div.rev-history td {{
    font-size: 8.5pt;
    color: #444;
}}

div.rev-history tr:nth-child(even) {{
    background: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HORIZONTAL RULES — Ma Dividers (§9.1 baseline unit)
   ═══════════════════════════════════════════════════════════════════════════ */

hr {{
    border: none;
    border-top: 0.5pt solid #ddd;
    margin: 18pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   BLOCKQUOTES — Callout Strips (§13 Emptiness)
   ═══════════════════════════════════════════════════════════════════════════ */

blockquote {{
    border-left: 2.5pt solid #4A90A4;
    margin: 12pt 0;
    padding: 8pt 14pt;
    background-color: #f7f9fb;
    color: #333;
    font-size: 9.5pt;
}}

blockquote p {{
    margin: 0 0 6pt 0;
}}

blockquote p:last-child {{
    margin-bottom: 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   CODE — §4.3 Monospace
   ═══════════════════════════════════════════════════════════════════════════ */

code {{
    font-family: 'DejaVu Sans Mono', 'Consolas', monospace;
    background-color: #f5f5f5;
    padding: 1pt 3pt;
    font-size: 8.5pt;
    border-radius: 1.5pt;
    color: #1B3A5C;
}}

pre {{
    background-color: #f8f8f8;
    padding: 10pt 12pt;
    border-left: 2.5pt solid #ccc;
    border-radius: 0;
    font-size: 8pt;
    line-height: 1.45;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 6pt 0 12pt 0;
}}

pre code {{
    background: none;
    padding: 0;
    color: #333;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LISTS — §9.1 Baseline spacing
   ═══════════════════════════════════════════════════════════════════════════ */

ul, ol {{
    margin: 6pt 0 6pt 0;
    padding-left: 20pt;
}}

li {{
    margin-bottom: 3pt;
    line-height: 1.5;
}}

li > ul, li > ol {{
    margin-top: 3pt;
    margin-bottom: 0;
}}

li input[type="checkbox"] {{
    margin-right: 4pt;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LINKS — Steel Blue, no underline (clean precision)
   ═══════════════════════════════════════════════════════════════════════════ */

a {{
    color: #4A90A4;
    text-decoration: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   PARAGRAPHS — §4.2 Body text, §9.1 baseline grid
   ═══════════════════════════════════════════════════════════════════════════ */

p {{
    margin: 0 0 6pt 0;
}}

strong {{
    color: #111;
    font-weight: 600;
}}

em {{
    color: #333;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   PRINT HELPERS — Page break control
   ═══════════════════════════════════════════════════════════════════════════ */

h2, h3 {{
    page-break-after: avoid;
}}

h1, h2, h3, h4 {{
    page-break-inside: avoid;
}}

table, pre, blockquote {{
    page-break-inside: avoid;
}}

/* Keep heading with at least 3 lines of following content */
h2 + *, h3 + * {{
    page-break-before: avoid;
}}
"""


def wrap_revision_history(html_content):
    """Wrap the last table in a div.rev-history container.

    The last table in a JDS document is always the revision history.
    This allows CSS to style it distinctly from data tables.
    """
    # Find the last <table> ... </table> block and wrap it
    last_table_pos = html_content.rfind('<table>')
    if last_table_pos == -1:
        return html_content

    # Check if the preceding heading contains "Revision History"
    preceding = html_content[:last_table_pos]
    if 'Revision History' in preceding[max(0, len(preceding)-200):]:
        closing_pos = html_content.find('</table>', last_table_pos)
        if closing_pos != -1:
            closing_pos += len('</table>')
            table_html = html_content[last_table_pos:closing_pos]
            html_content = (
                html_content[:last_table_pos]
                + '<div class="rev-history">'
                + table_html
                + '</div>'
                + html_content[closing_pos:]
            )
    return html_content


def md_to_pdf(input_path, output_path=None):
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Extract metadata for page headers/footers
    meta = extract_metadata(md_content)
    doc_no = meta.get('doc_no', '')
    revision = meta.get('revision', '')
    date = meta.get('date', '')

    # Format CSS with metadata
    formatted_css = CSS.format(
        doc_no=doc_no,
        revision=revision,
        date=date,
    )

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )

    # Post-process: wrap revision history table
    html_content = wrap_revision_history(html_content)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>{formatted_css}</style></head>
<body>{html_content}</body>
</html>"""

    HTML(string=full_html).write_pdf(output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 md2pdf.py <input.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = md_to_pdf(input_file, output_file)
    print(f"PDF created: {result}")
