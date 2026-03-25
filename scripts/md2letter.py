#!/usr/bin/env python3
"""JDS Letter PDF Generator — Elegant letterhead with rounded font.

Converts JDS correspondence markdown to PDF with a warm, distinctive
letterhead featuring the Johansson Engineering stamp logo and Varela Round
(a rounded sans-serif in the spirit of Gothic Maru Pro).

Usage: python3 md2letter.py <input.md> [output.pdf]
"""

import sys
import os
import re
import base64
import markdown
from weasyprint import HTML

# ---------------------------------------------------------------------------
# Resolve paths relative to this script
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, '..', 'jds', 'assets', 'logo.png')
FONTS_DIR = os.path.join(SCRIPT_DIR, '..', 'jds', 'assets', 'fonts')


def get_logo_data_uri():
    """Encode the logo as a base64 data URI for embedding in HTML."""
    if not os.path.exists(LOGO_PATH):
        return None
    with open(LOGO_PATH, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    ext = os.path.splitext(LOGO_PATH)[1].lower()
    mime = 'image/png' if ext == '.png' else 'image/jpeg'
    return f'data:{mime};base64,{data}'


def get_font_face_css():
    """Generate @font-face rules for locally bundled fonts."""
    faces = []
    font_files = {
        'Varela Round': 'VarelaRound-Regular.ttf',
        'M PLUS Rounded 1c': 'MPLUSRounded1c-Regular.ttf',
    }
    for family, filename in font_files.items():
        path = os.path.join(FONTS_DIR, filename)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = base64.b64encode(f.read()).decode('utf-8')
            faces.append(
                f"@font-face {{\n"
                f"  font-family: '{family}';\n"
                f"  src: url('data:font/truetype;base64,{data}');\n"
                f"  font-weight: normal;\n"
                f"  font-style: normal;\n"
                f"}}"
            )
    return '\n'.join(faces)


# ---------------------------------------------------------------------------
# Extract metadata
# ---------------------------------------------------------------------------

def extract_metadata(md_text):
    meta = {}
    patterns = {
        'doc_no': r'\*\*Document No\.\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'revision': r'\*\*Revision\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
        'date': r'\*\*Date\*\*\s*\|\s*(.+?)(?:\s*\||\s*$)',
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, md_text, re.MULTILINE)
        if match:
            meta[key] = match.group(1).strip()
    return meta


# ---------------------------------------------------------------------------
# Letter CSS — Elegant letterhead, rounded font, generous whitespace
# ---------------------------------------------------------------------------

LETTER_CSS = """
{font_faces}

@page {{
    size: A4;
    margin: 20mm 25mm 25mm 25mm;

    @bottom-center {{
        content: "Johansson Engineering  ·  Est. 1983";
        font-size: 6.5pt;
        color: #b0b0b0;
        font-family: 'Varela Round', 'M PLUS Rounded 1c', 'Rounded Mplus 1c', sans-serif;
        letter-spacing: 0.5pt;
        border-top: 0.5pt solid #e8ecf0;
        padding-top: 8pt;
    }}
}}

body {{
    font-family: 'Varela Round', 'M PLUS Rounded 1c', 'Rounded Mplus 1c', 'Noto Sans', sans-serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #2c2c2e;
    text-align: left;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LETTERHEAD — Logo + brand, centred, elegant
   ═══════════════════════════════════════════════════════════════════════════ */

.letterhead {{
    text-align: center;
    padding-bottom: 10pt;
    margin-bottom: 12pt;
    border-bottom: 1.5pt solid #1B3A5C;
}}

.letterhead img {{
    width: 52pt;
    height: 52pt;
    border-radius: 50%%;
    margin-bottom: 4pt;
    display: block;
    margin-left: auto;
    margin-right: auto;
}}

.letterhead .company-name {{
    font-size: 12pt;
    font-weight: 700;
    color: #1B3A5C;
    letter-spacing: 2.5pt;
    text-transform: uppercase;
    margin: 0;
    padding: 0;
}}

.letterhead .tagline {{
    font-size: 7pt;
    color: #8c8c8c;
    letter-spacing: 1.5pt;
    text-transform: uppercase;
    margin-top: 2pt;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HIDE THE MARKDOWN H1 AND METADATA TABLE — replaced by letterhead
   ═══════════════════════════════════════════════════════════════════════════ */

h1 {{
    display: none;
}}

/* First table (metadata) — hidden in letter mode */
table:first-of-type {{
    display: none;
}}

/* First HR after metadata — hidden */
hr:first-of-type {{
    display: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   ADDRESS BLOCK & DATE
   ═══════════════════════════════════════════════════════════════════════════ */

strong {{
    color: #1d1d1f;
    font-weight: 700;
}}

p {{
    margin: 0 0 6pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HEADINGS — Only h2 (section breaks) should appear in a letter
   ═══════════════════════════════════════════════════════════════════════════ */

h2 {{
    font-size: 11pt;
    font-weight: 700;
    color: #1B3A5C;
    margin: 20pt 0 8pt 0;
    padding-bottom: 3pt;
    border-bottom: 0.75pt solid #e8ecf0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   HORIZONTAL RULES — Soft dividers between letter sections
   ═══════════════════════════════════════════════════════════════════════════ */

hr {{
    border: none;
    border-top: 0.75pt solid #e8ecf0;
    margin: 10pt 0;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   REVISION HISTORY TABLE — Small, metadata feel at bottom
   ═══════════════════════════════════════════════════════════════════════════ */

div.rev-history {{
    margin-top: 14pt;
    page-break-before: avoid;
}}

div.rev-history table {{
    display: table;
    width: auto;
    min-width: 60%%;
    font-size: 7.5pt;
    border: 1pt solid #e8ecf0;
    border-radius: 6pt;
    border-collapse: separate;
    border-spacing: 0;
    overflow: hidden;
    background: #fafbfc;
}}

div.rev-history th {{
    background: transparent;
    color: #86868b;
    font-size: 6.5pt;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    font-weight: 600;
    padding: 5pt 8pt;
    border-bottom: 0.5pt solid #e2e6ea;
    border-left: none;
    border-right: none;
    border-top: none;
    text-align: left;
}}

div.rev-history td {{
    color: #555;
    padding: 4pt 8pt;
    border-bottom: 0.5pt solid #eef1f4;
    border-left: none;
    border-right: none;
    text-align: left;
}}

div.rev-history tr:last-child td {{
    border-bottom: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   GENERAL TABLE (non-first, non-rev-history)
   ═══════════════════════════════════════════════════════════════════════════ */

table {{
    border-collapse: separate;
    border-spacing: 0;
    width: 100%%;
    margin: 8pt 0 14pt 0;
    font-size: 9pt;
    page-break-inside: avoid;
    border: 1pt solid #e2e6ea;
    border-radius: 8pt;
    overflow: hidden;
}}

th {{
    background-color: #f5f7f9;
    color: #1B3A5C;
    font-weight: 600;
    font-size: 8pt;
    text-align: left;
    text-transform: uppercase;
    letter-spacing: 0.3pt;
    padding: 6pt 10pt;
    border-bottom: 1pt solid #e2e6ea;
    border-left: none;
    border-right: none;
    border-top: none;
}}

td {{
    padding: 5pt 10pt;
    border-bottom: 0.5pt solid #eef1f4;
    border-left: none;
    border-right: none;
    vertical-align: top;
    text-align: left;
}}

tr:last-child td {{
    border-bottom: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LINKS
   ═══════════════════════════════════════════════════════════════════════════ */

a {{
    color: #4A90A4;
    text-decoration: none;
}}

/* ═══════════════════════════════════════════════════════════════════════════
   LISTS
   ═══════════════════════════════════════════════════════════════════════════ */

ul, ol {{
    margin: 6pt 0 8pt 0;
    padding-left: 18pt;
}}

li {{
    margin-bottom: 3pt;
    line-height: 1.7;
}}
"""


def wrap_revision_history(html_content):
    """Wrap the last table in a div.rev-history container."""
    last_table_pos = html_content.rfind('<table>')
    if last_table_pos == -1:
        return html_content
    preceding = html_content[:last_table_pos]
    if 'Revision History' in preceding[max(0, len(preceding) - 200):]:
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


def inject_letterhead(html_content, logo_uri):
    """Inject a centred letterhead with logo above the content."""
    logo_img = ''
    if logo_uri:
        logo_img = f'<img src="{logo_uri}" alt="Johansson Engineering">'

    letterhead_html = (
        '<div class="letterhead">'
        f'{logo_img}'
        '<div class="company-name">Johansson Engineering</div>'
        '<div class="tagline">Marine · Mechanical · Industrial</div>'
        '</div>'
    )

    # Insert at very beginning of body content
    h1_match = re.search(r'<h1[\s>]', html_content)
    if h1_match:
        pos = h1_match.start()
        html_content = html_content[:pos] + letterhead_html + html_content[pos:]
    else:
        html_content = letterhead_html + html_content

    return html_content


def md_to_letter_pdf(input_path, output_path=None):
    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".pdf"

    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    meta = extract_metadata(md_content)
    font_faces = get_font_face_css()

    formatted_css = LETTER_CSS.format(font_faces=font_faces)

    html_content = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
    )

    html_content = wrap_revision_history(html_content)

    logo_uri = get_logo_data_uri()
    html_content = inject_letterhead(html_content, logo_uri)

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>{formatted_css}</style></head>
<body>{html_content}</body>
</html>"""

    HTML(string=full_html).write_pdf(output_path)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 md2letter.py <input.md> [output.pdf]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    result = md_to_letter_pdf(input_file, output_file)
    print(f"Letter PDF created: {result}")
