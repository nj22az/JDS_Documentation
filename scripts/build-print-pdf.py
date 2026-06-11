#!/usr/bin/env python3
"""Build the KDP paperback interior PDF for JDS-PRJ-GEN-001.

Produces a print-ready 6x9 in interior (KDP's standard non-fiction trim) from the
same markdown manuscript the EPUB is built from: mirrored margins with a gutter,
running head with the book title, centred page numbers, chapters starting on a
fresh page. Black ink only — the cheap KDP print tier.

Reports the final page count, which determines the paperback spine width
(pages x 0.002252 in for white paper) used by build-print-cover.py.

Usage:
    python3 scripts/build-print-pdf.py                 # English interior
    python3 scripts/build-print-pdf.py --lang sv        # Swedish interior
"""

import html
import re
import sys
from pathlib import Path

import markdown
import weasyprint
from weasyprint.text.fonts import FontConfiguration
from pypdf import PdfReader

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

PROJECT = Path("projects/JDS-PRJ-GEN-001")
MANUSCRIPT = PROJECT / "02-manuscript"
PRODUCTION = PROJECT / "04-production"
IMAGES_DIR = (PROJECT / "03-assets" / "images").resolve()
FONTS_DIR = (PROJECT / "03-assets" / "fonts").resolve()

MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]

LANG_CONFIG = {
    "en": {
        "root": MANUSCRIPT / "en",
        "chapter_glob": "chapter-*.md",
        "title": "The Garage Reset",
        "output": PRODUCTION / "The-Garage-Reset-Interior.pdf",
        # Part-divider pages inserted before these chapter numbers.
        "parts": {
            1: ("Part One", "The Idea"),
            3: ("Part Two", "Clear It Out"),
            6: ("Part Three", "Build the System"),
            9: ("Part Four", "Keep It"),
            12: ("Part Five", "Special Cases"),
        },
    },
    "sv": {
        "root": MANUSCRIPT / "sv",
        "chapter_glob": "kapitel-*.md",
        "title": "Städa i Garaget",
        "output": PRODUCTION / "Stada-i-Garaget-Interior.pdf",
        "parts": {
            1: ("Del 1", "Tanken"),
            3: ("Del 2", "Rensa"),
            6: ("Del 3", "Systemet"),
            9: ("Del 4", "Håll ordning"),
            12: ("Del 5", "Specialfall"),
        },
    },
}

# KDP 5.5x8.5 in (standard how-to trim), no-bleed interior.
# Inside (gutter) margin sized for the 151-300 page band (>= 0.5 in required).
def _font_face_css():
    """@font-face block pointing at the absolute subset-font paths (weasyprint)."""
    weights = [("Regular", 400), ("Medium", 500), ("Bold", 700)]
    blocks = []
    for name, weight in weights:
        uri = (FONTS_DIR / f"MPLUSRounded1c-{name}-subset.ttf").as_uri()
        blocks.append(f"@font-face {{ font-family: 'Rounded'; font-weight: {weight};"
                      f" src: url('{uri}'); }}")
    return "\n".join(blocks)


PAGE_CSS = """
@page {
    size: 5.5in 8.5in;
    margin: 0.7in 0.55in 0.65in 0.55in;
    @bottom-center { content: counter(page); font-family: Georgia, serif; font-size: 9pt; }
}
@page :left  { margin-right: 0.8in; @top-left  { content: "BOOK_TITLE_TOKEN"; font-family: Georgia, serif; font-size: 8.5pt; letter-spacing: 0.08em; color: #444; } }
@page :right { margin-left: 0.8in; @top-right { content: string(chaptitle); font-family: Georgia, serif; font-size: 8.5pt; font-style: italic; color: #444; } }
@page front { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }
@page divider { @top-left { content: none; } @top-right { content: none; } @bottom-center { content: none; } }

body { font-family: Georgia, 'Liberation Serif', serif; font-size: 11pt; line-height: 1.55; }
section.front { page: front; }
section { page-break-before: always; }
section.chapter, section.divider { page-break-before: right; }
section.divider { page: divider; text-align: center; }
section.divider .partnum {
    margin-top: 2.6in; font-size: 13pt; letter-spacing: 0.25em;
    text-transform: uppercase; color: #555;
}
section.divider .partname { font-size: 24pt; font-weight: 700; margin-top: 0.3in;
    font-family: 'Rounded', Georgia, sans-serif; }
section.divider .partnum { font-family: 'Rounded', Georgia, sans-serif; }
h1, h2, h3, h4 { font-family: 'Rounded', Georgia, sans-serif; }
h1 {
    string-set: chaptitle content();
    font-size: 20pt; line-height: 1.15; margin: 1.4in 0 0.4in;
    page-break-after: avoid; font-weight: 700;
}
section.front h1 { margin-top: 1.1in; }
h2 { font-size: 13pt; margin: 1.3em 0 0.4em; page-break-after: avoid; font-weight: 700; }
h3 { font-size: 11.5pt; margin: 1.1em 0 0.3em; page-break-after: avoid; font-weight: 500; }
h4 { font-size: 10.5pt; font-style: italic; }
p { margin: 0 0 0.65em; text-align: left; orphans: 2; widows: 2; }
blockquote {
    background: #f2f2f0; border-left: 3pt solid #555;
    margin: 0.9em 0; padding: 0.5em 0.8em;
    page-break-inside: avoid; text-align: left;
}
blockquote p { text-align: left; }
blockquote strong:first-child { display: block; margin-bottom: 0.25em; }

/* Colour-coded boxes (JDS-PRO-007 §6). Bold "candy-panel" style: a solid
   saturated header bar (white icon + label) on a white card with a chunky
   rounded border. In B&W the header prints as a dark bar with white text, so
   the icon + label + bar still carry the meaning (§6.2 redundant encoding). */
.box { background: #fff; border: 1pt solid #ccc; margin: 0.95em 0;
    page-break-inside: avoid; text-align: left; border-radius: 12pt; overflow: hidden; }
.box-head { margin: 0; padding: 1.3mm 2.6mm; color: #fff;
    font-family: 'Rounded', sans-serif; font-weight: 700; font-size: 11pt; }
.box-icon { margin-right: 1.4mm; font-size: 9.5pt; }
/* The whole box is white with a single coloured outline; the text and bullets
   take a darkened shade of that colour (a blue bento has blue text). Items
   inside are separated by thin divider lines (rows) in a lighter shade. */
.box-body { background: #fff; padding: 1.6mm 2.8mm 2mm; }
.box-body p { text-align: left; margin: 0; }
.box-body ul, .box-body ol { margin: 0; padding-left: 4.5mm; }
.box-body li { margin: 0; }
.box-body > * + *, .box-body li + li { border-top: 0.5pt solid #ddd;
    margin-top: 1.6mm; padding-top: 1.6mm; }
.box.box-safety { border-color: #cf3127; }
.box.box-safety .box-head { background: #cf3127; }
.box.box-safety .box-body { color: #b3271e; }
.box.box-safety .box-body > * + *, .box.box-safety .box-body li + li { border-top-color: #ecc0bc; }
.box.box-do { border-color: #2f8f5b; }
.box.box-do .box-head { background: #2f8f5b; }
.box.box-do .box-body { color: #236b44; }
.box.box-do .box-body > * + *, .box.box-do .box-body li + li { border-top-color: #b8ddca; }
.box.box-rule { border-color: #1b3a5c; }
.box.box-rule .box-head { background: #1b3a5c; }
.box.box-rule .box-body { color: #1b3a5c; }
.box.box-rule .box-body > * + *, .box.box-rule .box-body li + li { border-top-color: #b9c5d3; }
.box.box-specs { border-color: #2e7fa6; }
.box.box-specs .box-head { background: #2e7fa6; }
.box.box-specs .box-body { color: #235f7e; }
.box.box-specs .box-body > * + *, .box.box-specs .box-body li + li { border-top-color: #b5d1e1; }
.box.box-soft { border-color: #a9741c; }
.box.box-soft .box-head { background: #a9741c; }
.box.box-soft .box-body { color: #7d5413; }
.box.box-soft .box-body > * + *, .box.box-soft .box-body li + li { border-top-color: #e0cda6; }

/* Chapter-opener dashboard (JDS-PRO-007 §5.3). Rounded 2x2 bento; the wrapper
   rounds + clips the table corners. */
.chapter-card-wrap { border: 0.75pt solid #9fb0bf; border-radius: 11pt;
    overflow: hidden; margin: 0.3em 0 1.4em; page-break-inside: avoid; }
table.chapter-card { width: 100%; border-collapse: collapse; font-size: 10pt; }
table.chapter-card td.cc-cell { width: 50%; border: 0.5pt solid #9fb0bf;
    padding: 2mm 3mm; vertical-align: top; background: #f4f7f9; }
.cc-k { display: block; font-size: 7.5pt; letter-spacing: 0.12em;
    text-transform: uppercase; color: #3f7e96; margin-bottom: 0.8mm;
    font-family: 'Rounded', sans-serif; font-weight: 500; }
.cc-v { display: block; color: #1b3a5c; line-height: 1.25;
    font-family: 'Rounded', Georgia, sans-serif; font-weight: 700; }

/* Compartment legend ("how this book is laid out" bento). */
.legend { border: 0.75pt solid #9fb0bf; border-radius: 11pt; overflow: hidden;
    padding: 0; margin: 5mm 0; page-break-inside: avoid; }
.legend table { font-size: 9.5pt; margin: 0; width: 100%; border-collapse: collapse; }
.legend td { border: none; border-bottom: 0.4pt solid #ddd; padding: 2mm 3mm;
    vertical-align: top; }
.legend tr:last-child td { border-bottom: none; }
.legend td:first-child { white-space: nowrap; width: 42mm;
    font-family: 'Rounded', Georgia, sans-serif; font-weight: 700; }
.legend th { background: #1b3a5c; color: #fff; text-align: left; padding: 2mm 3mm;
    font-family: 'Rounded', sans-serif; font-weight: 500; }
ul, ol { margin: 0 0 0.7em 1.1em; }
li { margin-bottom: 0.2em; }
table { border-collapse: collapse; width: 100%; font-size: 8.5pt; margin: 0.8em 0; }
th, td { border: 0.5pt solid #888; padding: 3pt 4pt; text-align: left; }
th { background: #e8e8e6; }
img { max-width: 100%; margin: 0.8em auto; display: block; }
img.qr { width: 24mm; display: block; margin: 2mm 0; }
figure.fig { margin: 5mm 0; text-align: center; page-break-inside: avoid; }
figure.fig figcaption { font-size: 8.5pt; color: #555; margin-top: 1.5mm; }
.figph { border: 1pt dashed #9aa7b4; background: #f4f6f8; padding: 6mm; margin: 5mm 0;
    text-align: center; color: #33475b; page-break-inside: avoid; }
hr { border: none; border-top: 0.5pt solid #999; margin: 1.2em 0; }
.titlepage { text-align: center; }
.titlepage h1 { margin-top: 2.4in; font-size: 26pt; string-set: none; }
"""


FIGURES_DIR = IMAGES_DIR / "figures"


def _resolve_image(name):
    for cand in (IMAGES_DIR / name, IMAGES_DIR / "qr" / name):
        if cand.exists():
            return cand
    return IMAGES_DIR / name


def _figure_file(n):
    for ext in ("png", "jpg", "jpeg"):
        p = FIGURES_DIR / f"fig-{int(n):02d}.{ext}"
        if p.exists():
            return p
    return None


def _figure_html(m):
    n, cap = m.group(1), m.group(2).strip()
    f = _figure_file(n)
    if f:
        return (f'<figure class="fig"><img src="{f.as_uri()}"/>'
                f'<figcaption><strong>Figure {n}.</strong> {cap}</figcaption></figure>')
    return (f'<div class="figph"><strong>FIGURE {n} — image to come</strong><br/>{cap}<br/>'
            f'<em>Place fig-{int(n):02d}.jpg in 03-assets/images/figures/ and rebuild.</em></div>')


def _card_html(m):
    """Render a chapter-opener dashboard from a [[CARD ...]] token (see build-epub.py)."""
    fields = {}
    for part in m.group(1).split("|"):
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip()] = value.strip()
    cells = [("Step", fields.get("step", "")), ("Time", fields.get("time", "")),
             ("This weekend", fields.get("task", "")), ("You'll need", fields.get("need", ""))]
    rows = ""
    for i in (0, 2):
        rows += "<tr>"
        for label, value in cells[i:i + 2]:
            rows += (f'<td class="cc-cell"><span class="cc-k">{label}</span>'
                     f'<span class="cc-v">{value}</span></td>')
        rows += "</tr>"
    return (f'<div class="chapter-card-wrap">'
            f'<table class="chapter-card"><tbody>{rows}</tbody></table></div>')


# Colour-coded box system (JDS-PRO-007 §6: colour is language, always with a label).
BOX_MAP = [("Weekend Project", "box-do"), ("Helgprojektet", "box-do"),
           ("Workshop Rule", "box-rule"), ("Verkstadsregeln", "box-rule"),
           ("Safety", "box-safety"), ("Säkerhet", "box-safety"),
           ("Specs", "box-specs"), ("Mått & fakta", "box-specs"),
           ("Inherited & Hard", "box-soft"), ("Ärvt & svårt", "box-soft")]


BOX_ICON = {"box-safety": "▲", "box-do": "▶", "box-rule": "●",
            "box-specs": "◆", "box-soft": "◇"}


def _box_class(label):
    return next((c for k, c in BOX_MAP if label.startswith(k)), None)


def _render_box_blocks(text):
    """Turn each '>' block that opens with **Label** into a colour-panel div.

    Each box becomes a card with a solid header bar (icon + label) and a body.
    Done before markdown so adjacent boxes never merge and the class/label come
    from the raw text. Unrecognised quoted blocks are left for normal rendering.
    """
    lines = text.split("\n")
    out, i, n = [], 0, len(lines)
    while i < n:
        m = re.match(r'^>\s?\*\*([^*]+)\*\*', lines[i])
        cls = _box_class(m.group(1)) if m else None
        if cls:
            block = []
            while i < n and lines[i].startswith(">"):
                block.append(re.sub(r'^>\s?', "", lines[i]))
                i += 1
            inner = "\n".join(block)
            head = re.match(r'\*\*(.+?)\*\*[ \t]*(.*)', inner, flags=re.S)
            label, body_md = head.group(1).strip(), head.group(2).strip()
            # Blank line above a top-level list so it parses; indented sub-bullets
            # (Specs boxes) are left intact.
            body_md = re.sub(r'(?m)^(?P<p>(?![ \t])(?![-*+]\s)(?!\d+\.\s).*\S)\n'
                             r'(?=(?:[-*+]|\d+\.)\s)', r'\g<p>\n\n', body_md)
            icon = BOX_ICON.get(cls, "")
            out += [
                f'<div class="box {cls}" markdown="1">',
                f'<p class="box-head"><span class="box-icon">{icon}</span>'
                f'{html.escape(label)}</p>',
                '<div class="box-body" markdown="1">', "", body_md, "", "</div>",
                "</div>",
            ]
        else:
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def read_md(path):
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("<!--")]
    text = re.sub(r'\[\[FIGURE:(\d+)\|(.+?)\]\]', _figure_html, "\n".join(lines).strip(), flags=re.S)
    text = re.sub(r'\[\[CARD\s+(.+?)\]\]', _card_html, text, flags=re.S)
    text = _render_box_blocks(text)
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    # Point any manuscript-relative image path at the absolute asset (handles qr/ subdir).
    body = re.sub(r'src="[^"]*?/([^"/]+\.png)"',
                  lambda m: f'src="{_resolve_image(m.group(1)).as_uri()}"', body)
    return body


def ordered_sections(cfg):
    sections = []
    for path in sorted((cfg["root"] / "frontmatter").glob("*.md")):
        sections.append(("front", path))
    for path in sorted((cfg["root"] / "chapters").glob(cfg["chapter_glob"])):
        sections.append(("chapter", path))
    for path in sorted((cfg["root"] / "backmatter").glob("*.md")):
        sections.append(("back", path))
    return sections


def build(cfg):
    parts = []
    chapter_no = 0
    for kind, path in ordered_sections(cfg):
        if kind == "chapter":
            chapter_no += 1
            if chapter_no in cfg["parts"]:
                part_num, part_name = cfg["parts"][chapter_no]
                parts.append(f'<section class="divider">'
                             f'<p class="partnum">{part_num}</p>'
                             f'<p class="partname">{part_name}</p></section>')
            css_class = "chapter"
        elif kind == "front":
            css_class = "front"
        else:
            css_class = "main"
        if path.stem.startswith(("00-title", "00-titelsida")):
            css_class += " titlepage"
        parts.append(f'<section class="{css_class}">{read_md(path)}</section>')

    html = ("<html><head><meta charset='utf-8'></head><body>"
            + "\n".join(parts) + "</body></html>")
    font_config = FontConfiguration()
    page_css = _font_face_css() + "\n" + PAGE_CSS.replace("BOOK_TITLE_TOKEN", cfg["title"])
    css = weasyprint.CSS(string=page_css, font_config=font_config)
    cfg["output"].parent.mkdir(parents=True, exist_ok=True)
    weasyprint.HTML(string=html).write_pdf(str(cfg["output"]), stylesheets=[css],
                                           font_config=font_config)
    return len(PdfReader(str(cfg["output"])).pages)


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    cfg = LANG_CONFIG[lang]
    pages = build(cfg)
    size_kb = cfg["output"].stat().st_size / 1024
    spine_in = pages * 0.002252
    print(f"Built {cfg['output']} [{lang}] — {pages} pages, {size_kb:.0f} KB")
    print(f"Spine width (white paper): {pages} x 0.002252 = {spine_in:.4f} in")
    return 0


if __name__ == "__main__":
    sys.exit(main())
