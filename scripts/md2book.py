#!/usr/bin/env python3
"""md2book.py — compile a markdown manuscript folder into a publishable book PDF.

Usage:
    python3 scripts/md2book.py <manuscript_dir> [output.pdf]
        [--title T] [--subtitle S] [--author A]

Expects a manuscript folder laid out like projects/literary/EIC/manuscript/:
    00-frontmatter.md      title block + book epigraph (blockquote reused here)
    NN-YEAR-slug.md        chapters, in filename order; each may open with a
                           dated epigraph blockquote separated from the body
                           by a standalone --- line
    appendix-*.md          back matter, in filename order

Unlike md2pdf.py (JDS technical documents, PRO-007), this produces trade-book
typography: 6x9 in pages, mirrored margins, justified and hyphenated serif
text, chapters opening on right-hand pages, running heads, and a contents
page with real page numbers.
"""

import argparse
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- config ---

PAGE_SIZE = "6in 9in"                    # US trade paperback
MARGIN_TOP = "0.8in"
MARGIN_BOTTOM = "0.85in"
MARGIN_INNER = "0.85in"
MARGIN_OUTER = "0.7in"

BODY_FONT = '"Liberation Serif", "DejaVu Serif", serif'
BODY_SIZE = "10.5pt"
BODY_LEADING = "1.45"
LANGUAGE = "en-GB"                       # drives hyphenation

CHAPTER_KICKER_SIZE = "10.5pt"           # "Chapter One" / "Interlude" label
CHAPTER_TITLE_SIZE = "26pt"              # the chapter's name — the dominant heading
CHAPTER_DATELINE_SIZE = "11.5pt"         # the year, now a subtitle under the title
SUBHEAD_SIZE = "10.5pt"
RUNNING_HEAD_SIZE = "8.5pt"
FOLIO_SIZE = "9.5pt"

# Spelled-out numbers for the 11 non-interlude chapters ("Chapter One", not
# "Chapter 1") — interludes get the "Interlude" kicker instead of a number,
# so this only needs to run as far as the book has numbered chapters.
CHAPTER_NUMBER_WORDS = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen", "Twenty",
]

SCENE_BREAK_MARK = "*&#8195;*&#8195;*"   # em-space separated asterisks

# A chapter file opening with this marker is styled as an interlude:
# a labelled, smaller opener and an italic contents entry.
INTERLUDE_MARKER = "<!-- interlude -->"

# A file opening with this marker is a part divider: a right-hand part-title
# page ("Part One — The Venture", a year range, a short orienting note) that
# groups the chapters after it. Parts are never counted as chapters.
PART_MARKER = "<!-- part -->"

# The foreword file: front matter, rendered between the contents page and
# the first part, with its own contents entry.
FOREWORD_FILENAME = "00a-foreword.md"

# Book-only editorial cut: working notes that don't belong in a printed copy.
BIBLIOGRAPHY_CUT_MARKER = "## Suggested additions"

# ------------------------------------------------------------- stylesheet ---

BOOK_CSS = f"""
@page {{
    size: {PAGE_SIZE};
    margin-top: {MARGIN_TOP};
    margin-bottom: {MARGIN_BOTTOM};
}}
@page :left {{
    margin-left: {MARGIN_OUTER};
    margin-right: {MARGIN_INNER};
    @top-center {{
        content: string(booktitle);
        font-size: {RUNNING_HEAD_SIZE};
        letter-spacing: 0.14em;
        font-variant: small-caps;
        color: #444;
    }}
    @bottom-center {{ content: counter(page); font-size: {FOLIO_SIZE}; }}
}}
@page :right {{
    margin-left: {MARGIN_INNER};
    margin-right: {MARGIN_OUTER};
    @top-center {{
        content: string(chaptertitle);
        font-size: {RUNNING_HEAD_SIZE};
        letter-spacing: 0.14em;
        font-variant: small-caps;
        color: #444;
    }}
    @bottom-center {{ content: counter(page); font-size: {FOLIO_SIZE}; }}
}}
@page front {{
    @top-center {{ content: none; }}
    @bottom-center {{ content: none; }}
}}
@page chapter-opener {{
    @top-center {{ content: none; }}
}}

html {{ font-family: {BODY_FONT}; font-size: {BODY_SIZE}; }}
body {{ margin: 0; }}

p {{
    line-height: {BODY_LEADING};
    text-align: justify;
    hyphens: auto;
    margin: 0;
    text-indent: 1.4em;
    orphans: 2;
    widows: 2;
}}

/* no indent on openings: after headings, epigraphs, and scene breaks */
h1 + p, h2 + p, .epigraph + p, .scene-break + p, .chapter-start + p {{
    text-indent: 0;
}}

/* ------------------------------------------------------- front matter -- */
.front {{ page: front; }}
.title-page {{ page-break-after: always; text-align: center; }}
.title-page .spacer {{ height: 2.2in; }}
.title-page .book-title {{
    font-size: 30pt; letter-spacing: 0.04em; line-height: 1.15;
    margin: 0 0 0.35in 0;
}}
.title-page .book-subtitle {{
    font-size: 12pt; font-style: italic; color: #333; margin: 0 0 1.5in 0;
}}
.title-page .book-author {{
    font-size: 14pt; letter-spacing: 0.22em; font-variant: small-caps;
}}
.copyright-page {{
    page-break-after: always;
    font-size: 8.5pt; color: #444; text-align: center;
}}
.copyright-page .spacer {{ height: 5.6in; }}
.copyright-page p {{ text-align: center; text-indent: 0; line-height: 1.5; }}
.book-epigraph-page {{ page-break-after: always; }}
.book-epigraph-page .spacer {{ height: 2.4in; }}
.book-epigraph-page blockquote {{
    margin: 0 0.5in; font-style: italic; text-align: center;
    font-size: 11pt; line-height: 1.6; border: none;
}}
/* the global p rule justifies; epigraph paragraphs must stay centered */
.book-epigraph-page blockquote p {{ text-align: center; text-indent: 0; hyphens: none; }}
.contents {{ page-break-after: always; }}
.contents h1 {{
    font-size: 15pt; text-align: center; font-variant: small-caps;
    letter-spacing: 0.18em; font-weight: normal; margin: 0.9in 0 0.5in 0;
}}
.contents ol {{ list-style: none; margin: 0 0.25in; padding: 0; }}
.contents li {{ margin-bottom: 0.55em; font-size: 10.5pt; }}
.contents a {{ text-decoration: none; color: black; }}
.contents .toc-num {{
    display: inline-block; width: 4.9em; padding-right: 0.4em;
    color: #555; font-size: 9.5pt; font-variant: small-caps;
    letter-spacing: 0.06em;
}}
.contents a::after {{
    content: leader(" . ") target-counter(attr(href), page);
}}

/* ----------------------------------------------------------- chapters -- */
section.chapter {{ page-break-before: right; }}
section.chapter > .chapter-head {{ page: chapter-opener; }}
.chapter-kicker {{
    text-align: center; font-variant: small-caps; letter-spacing: 0.28em;
    font-size: {CHAPTER_KICKER_SIZE}; color: #666; margin: 1.15in 0 0.5in 0;
}}
h1.chapter-title {{
    text-align: center; font-size: {CHAPTER_TITLE_SIZE}; font-weight: normal;
    letter-spacing: 0.01em; margin: 0 0 0.2in 0; line-height: 1.2;
    string-set: chaptertitle content();
}}
.chapter-dateline {{
    text-align: center; font-size: {CHAPTER_DATELINE_SIZE}; font-style: italic;
    color: #666; margin: 0 0 0.55in 0; letter-spacing: 0.04em;
}}
.epigraph {{
    margin: 0 0.55in 0.55in 0.55in; font-size: 9.5pt; line-height: 1.55;
    font-style: italic; color: #333;
}}
.epigraph p {{ text-align: center; text-indent: 0; }}
.epigraph .attribution {{ font-style: normal; font-size: 8.5pt; color: #555; }}

h2 {{
    text-align: center; font-size: {SUBHEAD_SIZE}; font-weight: normal;
    font-variant: small-caps; letter-spacing: 0.2em;
    margin: 1.6em 0 0.9em 0; page-break-after: avoid;
}}
.scene-break {{
    text-align: center; margin: 1.1em 0; text-indent: 0;
    letter-spacing: 0.3em; color: #555;
}}
em {{ line-height: inherit; }}

/* ------------------------------------------------------------- parts -- */
section.part {{ page-break-before: right; page: chapter-opener; }}
.part-kicker {{
    text-align: center; font-variant: small-caps; letter-spacing: 0.3em;
    font-size: {CHAPTER_KICKER_SIZE}; color: #666; margin: 2.1in 0 0.45in 0;
}}
h1.part-title {{
    text-align: center; font-size: {CHAPTER_TITLE_SIZE}; font-weight: normal;
    letter-spacing: 0.01em; margin: 0 0 0.2in 0; line-height: 1.2;
}}
.part-dateline {{
    text-align: center; font-size: {CHAPTER_DATELINE_SIZE}; font-style: italic;
    color: #666; margin: 0 0 0.6in 0; letter-spacing: 0.04em;
}}
.part-note {{ margin: 0 0.55in; }}
.part-note p {{
    text-align: center; text-indent: 0; font-style: italic;
    font-size: 10pt; line-height: 1.6; color: #333;
}}
.contents li.toc-part {{
    margin: 1.1em 0 0.55em 0; font-variant: small-caps;
    letter-spacing: 0.12em;
}}

/* -------------------------------------------------------- back matter -- */
section.backmatter {{ page-break-before: right; }}
section.backmatter h1 {{
    text-align: center; font-size: 15pt; font-weight: normal;
    font-variant: small-caps; letter-spacing: 0.15em;
    margin: 1.1in 0 0.5in 0; string-set: chaptertitle content();
}}
section.backmatter h2 {{ margin-top: 1.4em; }}
section.backmatter p {{
    text-align: left; text-indent: 0; margin-bottom: 0.55em;
    font-size: 9.5pt; line-height: 1.5;
}}
"""

# ------------------------------------------------------------- rendering ---


def markdown_to_html(text):
    import markdown
    return markdown.markdown(text, extensions=["smarty"])


def split_epigraph(chapter_text):
    """Return (epigraph_markdown_or_None, body_markdown)."""
    if not chapter_text.lstrip().startswith(">"):
        return None, chapter_text
    parts = re.split(r"\n---\n", chapter_text, maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    return None, chapter_text


def style_scene_breaks(html):
    return html.replace("<hr />", f'<div class="scene-break">{SCENE_BREAK_MARK}</div>')


def render_epigraph(epigraph_markdown):
    """Chapter epigraphs: drop the bold year (the chapter head shows it),
    keep the quote and attribution."""
    lines = [ln.lstrip("> ").rstrip() for ln in epigraph_markdown.splitlines()]
    kept = [ln for ln in lines if ln and not re.fullmatch(r"\*\*\d{4}(–\d{4})?\*\*", ln)]
    quote = "\n\n".join(kept)
    html = markdown_to_html(quote)
    html = re.sub(r"<p>(—[^<]*)</p>", r'<p class="attribution">\1</p>', html)
    return f'<div class="epigraph">{html}</div>'


def render_chapter(index, chapter_text, chapter_number):
    """chapter_number is the spelled-out ordinal (e.g. "One") for a numbered
    chapter, or None for an interlude, which gets the "Interlude" kicker
    instead of a number."""
    text = chapter_text.lstrip()
    is_interlude = text.startswith(INTERLUDE_MARKER)
    if is_interlude:
        text = text[len(INTERLUDE_MARKER):].lstrip()
    epigraph, body = split_epigraph(text)
    heading = re.match(r"#\s+(\d{4}):\s+(.+)", body)
    if not heading:
        sys.exit(f"chapter {index}: expected '# YEAR: Title' heading")
    year, title = heading.group(1), heading.group(2).strip()
    body_html = style_scene_breaks(markdown_to_html(body.split("\n", 1)[1]))
    epigraph_html = render_epigraph(epigraph) if epigraph else ""
    section_class = "chapter interlude" if is_interlude else "chapter"
    kicker = "Interlude" if is_interlude else f"Chapter {chapter_number}"
    return year, title, is_interlude, (
        f'<section class="{section_class}" id="ch-{index}">'
        f'<div class="chapter-head">'
        f'<div class="chapter-kicker">{kicker}</div>'
        f'<h1 class="chapter-title">{title}</h1>'
        f'<div class="chapter-dateline">{year}</div>'
        f"{epigraph_html}"
        f'</div><div class="chapter-start"></div>'
        f"{body_html}</section>"
    )


def render_part(part_index, text):
    """A part-divider page. Expects '# Part N — Title', an italic year-range
    line, then the orienting note."""
    text = text.lstrip()[len(PART_MARKER):].lstrip()
    heading = re.match(r"#\s+(Part [A-Za-z]+)\s+—\s+(.+)", text)
    if not heading:
        sys.exit(f"part {part_index}: expected '# Part N — Title' heading")
    kicker, title = heading.group(1), heading.group(2).strip()
    rest = text.split("\n", 1)[1].strip()
    dateline = ""
    dateline_match = re.match(r"\*([^*]+)\*\s*\n", rest + "\n")
    if dateline_match:
        dateline = dateline_match.group(1)
        rest = rest[dateline_match.end():].strip()
    note_html = markdown_to_html(rest)
    return kicker, title, (
        f'<section class="part" id="part-{part_index}">'
        f'<div class="part-kicker">{kicker}</div>'
        f'<h1 class="part-title">{title}</h1>'
        f'<div class="part-dateline">{dateline}</div>'
        f'<div class="part-note">{note_html}</div>'
        f"</section>"
    )


def render_backmatter(index, text):
    cut = text.find(BIBLIOGRAPHY_CUT_MARKER)
    if cut != -1:
        text = text[:cut].rstrip()
    return f'<section class="backmatter" id="bm-{index}">{markdown_to_html(text)}</section>'


def extract_book_epigraph(frontmatter_text):
    quotes = re.findall(r"((?:^>.*\n?)+)", frontmatter_text, flags=re.MULTILINE)
    return markdown_to_html("\n".join(quotes[0].splitlines())) if quotes else ""


def build_html(manuscript_dir, title, subtitle, author):
    files = sorted(manuscript_dir.glob("*.md"))
    frontmatter = [f for f in files if f.name.startswith("00-")]
    foreword = [f for f in files if f.name == FOREWORD_FILENAME]
    parts = [f for f in files if f.read_text().lstrip().startswith(PART_MARKER)]
    chapters = [f for f in files if re.match(r"\d\d-\d{4}-", f.name)]
    appendices = [f for f in files if f.name.startswith("appendix-")]

    book_epigraph = extract_book_epigraph(frontmatter[0].read_text()) if frontmatter else ""

    toc_rows, chapter_html = [], []

    foreword_html = ""
    if foreword:
        foreword_html = render_backmatter("foreword", foreword[0].read_text())
        toc_rows.append(
            '<li><span class="toc-num">&nbsp;</span>'
            '<a href="#bm-foreword">Foreword</a></li>'
        )

    # Chapters and part dividers interleave in filename order.
    body_files = sorted(parts + chapters, key=lambda f: f.name)
    numbered_count = 0
    part_count = 0
    index = 0
    for body_file in body_files:
        raw = body_file.read_text()
        if raw.lstrip().startswith(PART_MARKER):
            part_count += 1
            kicker, part_title, html = render_part(part_count, raw)
            toc_rows.append(
                f'<li class="toc-part">'
                f'<a href="#part-{part_count}">{kicker} — {part_title}</a></li>'
            )
            chapter_html.append(html)
            continue
        index += 1
        is_interlude = raw.lstrip().startswith(INTERLUDE_MARKER)
        chapter_number = None
        if not is_interlude:
            numbered_count += 1
            if numbered_count > len(CHAPTER_NUMBER_WORDS):
                sys.exit("chapter count exceeds CHAPTER_NUMBER_WORDS — extend the list")
            chapter_number = CHAPTER_NUMBER_WORDS[numbered_count - 1]
        year, chapter_title, is_interlude, html = render_chapter(
            index, raw, chapter_number)
        toc_title = f"<em>{chapter_title}</em>" if is_interlude else chapter_title
        toc_kicker = "Interlude" if is_interlude else chapter_number
        toc_rows.append(
            f'<li><span class="toc-num">{toc_kicker}</span>'
            f'<a href="#ch-{index}">{toc_title}</a></li>'
        )
        chapter_html.append(html)

    backmatter_html = []
    for index, appendix_file in enumerate(appendices, start=1):
        backmatter_html.append(render_backmatter(index, appendix_file.read_text()))
        heading = re.match(r"#\s+(.+)", appendix_file.read_text())
        label = heading.group(1).split(":")[0] if heading else appendix_file.stem
        toc_rows.append(
            f'<li><span class="toc-num">&nbsp;</span>'
            f'<a href="#bm-{index}">{label}</a></li>'
        )

    return f"""<!DOCTYPE html>
<html lang="{LANGUAGE}">
<head><meta charset="utf-8"><title>{title}</title>
<style>{BOOK_CSS}</style></head>
<body>
<div style="string-set: booktitle '{title}'">
<div class="front">
  <div class="title-page">
    <div class="spacer"></div>
    <div class="book-title">{title}</div>
    <div class="book-subtitle">{subtitle}</div>
    <div class="book-author">{author}</div>
  </div>
  <div class="copyright-page">
    <div class="spacer"></div>
    <p>Copyright &#169; 2026 {author}. All rights reserved.</p>
    <p>This is a work of fiction built on historical events. Where real
    persons appear, their private words and thoughts are invented.
    The resolution of the 1888 Whitechapel murders is entirely imagined.</p>
  </div>
  <div class="book-epigraph-page">
    <div class="spacer"></div>
    <blockquote>{book_epigraph}</blockquote>
  </div>
  <div class="contents">
    <h1>Contents</h1>
    <ol>{''.join(toc_rows)}</ol>
  </div>
</div>
{foreword_html}
{''.join(chapter_html)}
{''.join(backmatter_html)}
</div>
</body></html>"""


def main():
    parser = argparse.ArgumentParser(description="Markdown manuscript folder to book PDF")
    parser.add_argument("manuscript_dir", type=Path)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--title", default="The Front-Row Seat")
    parser.add_argument("--subtitle",
                        default="Five Centuries of History from the Banks of the Thames")
    parser.add_argument("--author", default="Nils Johansson")
    args = parser.parse_args()

    output = args.output or args.manuscript_dir.parent / "exports" / "book.pdf"
    output.parent.mkdir(parents=True, exist_ok=True)

    html = build_html(args.manuscript_dir, args.title, args.subtitle, args.author)

    from weasyprint import HTML
    HTML(string=html).write_pdf(str(output))
    print(f"Book PDF written: {output}")


if __name__ == "__main__":
    main()
