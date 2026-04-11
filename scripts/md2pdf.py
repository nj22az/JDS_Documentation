#!/usr/bin/env python3
"""JDS PDF Generator — JDS-PRO-007 Information Design Standard (Rev C).

Converts JDS markdown documents to PDF following Japanese information design
principles: thick flat lines, bento compartments, and semantic colour coding.
Every colour carries meaning — red = critical, navy = authority, green = done.

Usage: python3 md2pdf.py <input.md> [output.pdf]
"""

import sys
import os
import re
import base64
import markdown
from weasyprint import HTML

# ---------------------------------------------------------------------------
# Resolve the logo path relative to this script
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, '..', 'jds', 'assets')
LOGO_PATH_PNG = os.path.join(ASSETS_DIR, 'logo.png')
LOGO_PATH_SVG = os.path.join(ASSETS_DIR, 'logo.svg')
LOGO_VARIANTS_DIR = os.path.join(ASSETS_DIR, 'logo-variants')


def get_logo_data_uri(category=None):
    """Encode the logo as a base64 data URI for embedding in HTML.

    If a category is provided (e.g. 'PRO', 'COR', 'RPT') and an SVG colour
    variant exists, use that. Otherwise fall back to the default SVG, then PNG.
    """
    # Use PNG for reliable rendering (SVG path transforms render inconsistently
    # across PDF engines). The PNG is 752x752px which is crisp at 52pt display.
    if os.path.exists(LOGO_PATH_PNG):
        with open(LOGO_PATH_PNG, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
        return f'data:image/png;base64,{data}'

    # Fall back to SVG if PNG not available
    if category:
        variant_path = os.path.join(LOGO_VARIANTS_DIR, 'category', f'logo-{category.lower()}.svg')
        if os.path.exists(variant_path):
            with open(variant_path, 'r', encoding='utf-8') as f:
                data = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
            return f'data:image/svg+xml;base64,{data}'

    if os.path.exists(LOGO_PATH_SVG):
        with open(LOGO_PATH_SVG, 'r', encoding='utf-8') as f:
            data = base64.b64encode(f.read().encode('utf-8')).decode('utf-8')
        return f'data:image/svg+xml;base64,{data}'

    return None


def extract_category(doc_no):
    """Extract the document category code from a JDS document number.

    JDS-PRO-007 → PRO
    JDS-DWG-MEC-003 → DWG
    JDS-BLG-001 → BLG
    """
    if not doc_no:
        return None
    match = re.match(r'JDS-([A-Z]{3})', doc_no)
    return match.group(1) if match else None


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
# JDS-PRO-007 — Information Design Standard Implementation
#
# Design principles (JDS-owned terminology):
#   Active Space       — White space organises information. Every gap is intentional.
#   Compartment Design — Self-contained sections with clear boundaries.
#   Visual Explanation — If you can't diagram it, you don't understand it.
#   Craft Precision    — Alignment, spacing, and precision reflect engineering quality.
#   Colour is Language — Navy = authority, Steel Blue = support, Red = critical.
#   Three-Level Reading — Glance (0.5s), Scan (5s), Read (minutes).
#   6pt Grid           — All spacing in multiples of 6pt.
# ---------------------------------------------------------------------------

CSS = """
/* ═══════════════════════════════════════════════════════════════════════════
   PAGE SETUP
   ═══════════════════════════════════════════════════════════════════════════ */

@page {{
    size: A4;
    margin: 24mm 24mm 22mm 24mm;

    @top-left {{
        content: "{doc_no}";
        font-size: 7.5pt;
        font-weight: 600;
        color: #1B3A5C;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.5pt;
        border-bottom: 0.5pt solid #e8ecf0;
        padding-bottom: 6pt;
    }}
    @top-center {{
        content: string(doc-title);
        font-size: 7pt;
        color: #999;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-bottom: 0.5pt solid #e8ecf0;
        padding-bottom: 6pt;
    }}
    @top-right {{
        content: "UNCONTROLLED COPY";
        font-size: 6.5pt;
        color: #bbb;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        letter-spacing: 0.3pt;
        text-transform: uppercase;
        border-bottom: 0.5pt solid #e8ecf0;
        padding-bottom: 6pt;
    }}

    @bottom-left {{
        content: "Rev {revision}";
        font-size: 7pt;
        color: #999;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.5pt solid #e8ecf0;
        padding-top: 6pt;
    }}
    @bottom-center {{
        content: "Page " counter(page) " of " counter(pages);
        font-size: 7.5pt;
        color: #999;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.5pt solid #e8ecf0;
        padding-top: 6pt;
    }}
    @bottom-right {{
        content: "{date}";
        font-size: 7pt;
        color: #999;
        font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
        border-top: 0.5pt solid #e8ecf0;
        padding-top: 6pt;
    }}
}}

@page :first {{
    @top-center {{ content: none; }}
}}

/* ═══════════════════════════════════════════════════════════════════════════
   BODY — Warm, readable, generous
   ═══════════════════════════════════════════════════════════════════════════ */

body {{
    font-family: 'Noto Sans', 'Inter', 'Calibri', sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1d1d1f;
    text-align: left;
    orphans: 3;
    widows: 3;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   PARAGRAPHS — Active Space between text blocks
   ═══════════════════════════════════════════════════════════════════════════ */

p {{
    margin: 0 0 8pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LOGO HEADER — First page brand identity
   ═══════════════════════════════════════════════════════════════════════════ */

.logo-header {{
    margin-bottom: 6pt;
    line-height: 1;
}}

.logo-header img {{
    width: 52pt;
    height: 52pt;
    vertical-align: middle;
    margin-right: 10pt;
}}

.logo-header .brand-text {{
    font-size: 7.5pt;
    color: #86868b;
    letter-spacing: 1.5pt;
    text-transform: uppercase;
    font-weight: 600;
    vertical-align: middle;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HEADING HIERARCHY — Warm navy, generous spacing
   ═══════════════════════════════════════════════════════════════════════════ */

h1 {{
    font-size: 22pt;
    font-weight: 700;
    color: #1B3A5C;
    border-bottom: 3.5pt solid #1B3A5C;
    padding-bottom: 10pt;
    margin: 6pt 0 14pt 0;
    string-set: doc-title content();
    letter-spacing: -0.3pt;
    line-height: 1.2;
}}

h2 {{
    font-size: 14pt;
    font-weight: 700;
    color: #1B3A5C;
    margin: 30pt 0 12pt 0;
    padding-bottom: 6pt;
    border-bottom: 2pt solid #1B3A5C;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11pt;
    font-weight: 600;
    color: #4A90A4;
    margin: 24pt 0 8pt 0;
    page-break-after: avoid;
}}

h4 {{
    font-size: 10.5pt;
    font-weight: 600;
    font-style: italic;
    color: #555;
    margin: 14pt 0 6pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   METADATA IDENTITY CARD — Rounded, card-like, with soft background
   ═══════════════════════════════════════════════════════════════════════════ */

table:first-of-type {{
    width: auto;
    min-width: 50%;
    max-width: 65%;
    margin: 12pt 0 24pt 0;
    font-size: 9pt;
    border: 1pt solid #e8ecf0;
    border-radius: 8pt;
    overflow: hidden;
    background: #fafbfc;
    border-top: none;
    border-bottom: none;
    border-left: none;
    border-right: none;
    box-decoration-break: clone;
}}

table:first-of-type th,
table:first-of-type td {{
    border: none;
    border-bottom: 0.5pt solid #eef1f4;
    padding: 7pt 14pt;
    background: none;
}}

table:first-of-type th {{
    background: none;
    color: #86868b;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 7pt;
    letter-spacing: 0.5pt;
    width: 28%;
    vertical-align: top;
    border-bottom: 0.5pt solid #eef1f4;
}}

table:first-of-type td {{
    color: #1d1d1f;
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
   DATA TABLES — Rounded card containers, soft headers
   ═══════════════════════════════════════════════════════════════════════════ */

table {{
    border-collapse: separate;
    border-spacing: 0;
    width: 100%;
    margin: 12pt 0 18pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
    border: 1pt solid #e2e6ea;
    border-radius: 8pt;
    overflow: hidden;
}}

th {{
    background-color: #1B3A5C;
    color: #ffffff;
    font-weight: 600;
    font-size: 8pt;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    padding: 9pt 10pt;
    border-bottom: 2pt solid #132d4a;
    border-left: none;
    border-right: none;
    border-top: none;
}}

td {{
    padding: 9pt 10pt;
    border-bottom: 0.5pt solid #eef1f4;
    border-left: none;
    border-right: none;
    vertical-align: top;
    text-align: left;
    min-height: 18pt;
}}

tr:nth-child(even) {{
    background-color: #fafbfc;
}}

tr:last-child td {{
    border-bottom: none;
}}

/* First column of first row — top-left radius */
th:first-child {{
    border-top-left-radius: 7pt;
}}

/* Last column of first row — top-right radius */
th:last-child {{
    border-top-right-radius: 7pt;
}}

/* Bottom-left radius */
tr:last-child td:first-child {{
    border-bottom-left-radius: 7pt;
}}

/* Bottom-right radius */
tr:last-child td:last-child {{
    border-bottom-right-radius: 7pt;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   REVISION HISTORY TABLE — Compact, metadata feel
   ═══════════════════════════════════════════════════════════════════════════ */

div.rev-history table {{
    width: auto;
    min-width: 70%;
    max-width: 100%;
    font-size: 8.5pt;
    background: #fafbfc;
}}

div.rev-history th {{
    background-color: #fafbfc;
    color: #86868b;
    font-size: 7.5pt;
    border-bottom: 0.5pt solid #e2e6ea;
}}

div.rev-history td {{
    font-size: 8.5pt;
    color: #555;
}}

div.rev-history tr:nth-child(even) {{
    background: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HORIZONTAL RULES — Soft dividers
   ═══════════════════════════════════════════════════════════════════════════ */

hr {{
    border: none;
    border-top: 2.5pt solid #1B3A5C;
    margin: 28pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   BLOCKQUOTES — Rounded callout cards
   ═══════════════════════════════════════════════════════════════════════════ */

blockquote {{
    border-left: 4pt solid #4A90A4;
    margin: 18pt 0;
    padding: 14pt 18pt;
    background-color: #f0f6f9;
    border-radius: 0 8pt 8pt 0;
    color: #2c2c2e;
    font-size: 9.5pt;
    line-height: 1.5;
}}

blockquote p {{
    margin: 0 0 6pt 0;
}}

blockquote p:last-child {{
    margin-bottom: 0;
}}

/* Warning bento — red squircle compartment (Compartment Design) */
div.warning blockquote {{
    border: 3pt solid #C0392B;
    border-left: 3pt solid #C0392B;
    border-radius: 16pt;
    background-color: #fff8f7;
    color: #7B1A1A;
    padding: 16pt 22pt;
    margin: 22pt 0;
}}

div.warning blockquote strong {{
    color: #C0392B;
    font-size: 9.5pt;
}}

/* Success bento — green squircle compartment */
div.success blockquote {{
    border: 3pt solid #3D8B6E;
    border-left: 3pt solid #3D8B6E;
    border-radius: 16pt;
    background-color: #f7fdf9;
    color: #1a4a35;
    padding: 16pt 22pt;
    margin: 22pt 0;
}}

div.success blockquote strong {{
    color: #2E7D5A;
    font-size: 9.5pt;
}}

/* Note bento — navy squircle compartment (informational) */
div.note blockquote {{
    border: 3pt solid #1B3A5C;
    border-left: 3pt solid #1B3A5C;
    border-radius: 16pt;
    background-color: #f5f8fb;
    color: #1B3A5C;
    padding: 16pt 22pt;
    margin: 22pt 0;
}}

div.note blockquote strong {{
    color: #1B3A5C;
    font-size: 9.5pt;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   CODE — Rounded pill for inline, rounded block for pre
   ═══════════════════════════════════════════════════════════════════════════ */

code {{
    font-family: 'DejaVu Sans Mono', 'Consolas', monospace;
    background-color: #f2f3f5;
    padding: 1.5pt 5pt;
    font-size: 8.5pt;
    border-radius: 4pt;
    color: #1B3A5C;
}}

pre {{
    background-color: #f8f9fa;
    padding: 12pt 14pt;
    border-left: 3pt solid #d1d5db;
    border-radius: 0 8pt 8pt 0;
    font-size: 8pt;
    line-height: 1.5;
    overflow-x: auto;
    page-break-inside: avoid;
    margin: 8pt 0 14pt 0;
}}

pre code {{
    background: none;
    padding: 0;
    color: #333;
    border-radius: 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LISTS — Generous spacing, warm bullets
   ═══════════════════════════════════════════════════════════════════════════ */

ul, ol {{
    margin: 8pt 0 12pt 0;
    padding-left: 20pt;
}}

li {{
    margin-bottom: 4pt;
    line-height: 1.6;
}}

li > ul, li > ol {{
    margin-top: 4pt;
    margin-bottom: 0;
}}

li input[type="checkbox"] {{
    margin-right: 4pt;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LINKS — Steel Blue, no underline
   ═══════════════════════════════════════════════════════════════════════════ */

a {{
    color: #4A90A4;
    text-decoration: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   PARAGRAPHS
   ═══════════════════════════════════════════════════════════════════════════ */

p {{
    margin: 0 0 8pt 0;
}}

strong {{
    color: #1d1d1f;
    font-weight: 600;
}}

em {{
    color: #333;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   PRINT HELPERS
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

h2 + *, h3 + * {{
    page-break-before: avoid;
}}
"""


def wrap_callout_variants(html_content):
    """Detect blockquotes starting with specific markers and wrap them in
    styled div containers for warning (red) and success (green) callouts.

    Convention:
      > **Warning:** ...   -> red bento (danger, critical notes)
      > **Important:** ... -> red bento
      > **Done:** ...      -> green bento (success, confirmation)
      > **Tip:** ...       -> default blue bento (unchanged)
    """
    warning_markers = ['<strong>Warning:</strong>', '<strong>Important:</strong>',
                       '<strong>Danger:</strong>', '<strong>Dangerous fluids:</strong>',
                       '<strong>Caution:</strong>']
    success_markers = ['<strong>Done.</strong>', '<strong>Done:</strong>',
                       '<strong>Complete:</strong>']
    note_markers = ['<strong>Note:</strong>', '<strong>Ref:</strong>',
                    '<strong>Definition:</strong>']

    # Single-pass: find every <blockquote> and check if it contains a marker
    result = []
    pos = 0
    while pos < len(html_content):
        bq_start = html_content.find('<blockquote>', pos)
        if bq_start == -1:
            result.append(html_content[pos:])
            break
        bq_end = html_content.find('</blockquote>', bq_start)
        if bq_end == -1:
            result.append(html_content[pos:])
            break
        bq_end += len('</blockquote>')
        bq_html = html_content[bq_start:bq_end]

        # Append everything before the blockquote
        result.append(html_content[pos:bq_start])

        # Check if this blockquote contains a warning or success marker
        wrapper = None
        for marker in warning_markers:
            if marker in bq_html:
                wrapper = 'warning'
                break
        if not wrapper:
            for marker in success_markers:
                if marker in bq_html:
                    wrapper = 'success'
                    break
        if not wrapper:
            for marker in note_markers:
                if marker in bq_html:
                    wrapper = 'note'
                    break

        if wrapper:
            result.append(f'<div class="{wrapper}">{bq_html}</div>')
        else:
            result.append(bq_html)

        pos = bq_end

    return ''.join(result)


def wrap_revision_history(html_content):
    """Wrap the last table in a div.rev-history container."""
    last_table_pos = html_content.rfind('<table>')
    if last_table_pos == -1:
        return html_content

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


def inject_logo_header(html_content, logo_uri):
    """Inject a logo + brand name header at the top of the body."""
    if not logo_uri:
        return html_content

    logo_html = (
        '<div class="logo-header">'
        f'<img src="{logo_uri}" alt="Logo">'
        '<span class="brand-text">Johansson Engineering</span>'
        '</div>'
    )

    # Insert before the first <h1> (which may have attributes like id="...")
    h1_match = re.search(r'<h1[\s>]', html_content)
    if h1_match:
        pos = h1_match.start()
        html_content = html_content[:pos] + logo_html + html_content[pos:]
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

    # Post-process: wrap warning/success callout blockquotes
    html_content = wrap_callout_variants(html_content)

    # Post-process: inject logo header (category-coloured SVG if available)
    category = extract_category(doc_no)
    logo_uri = get_logo_data_uri(category=category)
    html_content = inject_logo_header(html_content, logo_uri)

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
