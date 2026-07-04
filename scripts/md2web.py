#!/usr/bin/env python3
"""md2web.py — compile a manuscript folder into a multi-page, navigable HTML site.

Usage:
    python3 scripts/md2web.py <manuscript_dir> <output_dir>

Produces one readable HTML page per source file (frontmatter, chapters, appendices)
plus an index.html contents page, wired together with Contents / Prev / Next
navigation and a shared stylesheet. Intended for quick reading and review during
development — the published artifact is still the PDF from md2book.py.

Layout expected (same as md2book.py):
    00-frontmatter.md      title block + book epigraph
    NN-YEAR-slug.md        chapters in filename order; a leading
                           "<!-- interlude -->" marks an interlude
    appendix-*.md          back matter, in filename order
"""

import argparse
import html
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- config ---

BOOK_TITLE = "The Front-Row Seat"
INTERLUDE_MARKER = "<!-- interlude -->"

# Spelled-out numbers for numbered (non-interlude) chapters.
CHAPTER_NUMBER_WORDS = [
    "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
    "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
    "Seventeen", "Eighteen", "Nineteen", "Twenty",
]

STYLESHEET = """\
:root {
  --fg: #211d18; --bg: #faf7f1; --muted: #6f6a60; --rule: #ddd6c9;
  --link: #7c3a2c; --card: #fffdf9;
}
@media (prefers-color-scheme: dark) {
  :root {
    --fg: #e8e2d5; --bg: #15130e; --muted: #9c9484; --rule: #38332a;
    --link: #dd9c80; --card: #1c1a14;
  }
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font: 1.125rem/1.68 Georgia, "Liberation Serif", "Times New Roman", serif;
  -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility;
}
nav.bar {
  position: sticky; top: 0; z-index: 10;
  background: color-mix(in srgb, var(--bg) 92%, transparent);
  border-bottom: 1px solid var(--rule); backdrop-filter: blur(8px);
}
nav.bar .inner {
  max-width: 46rem; margin: 0 auto; display: flex; align-items: baseline;
  justify-content: space-between; gap: 1rem; padding: .55rem 1.25rem;
  font: .8rem/1.4 -apple-system, system-ui, sans-serif;
}
nav.bar a { color: var(--link); text-decoration: none; white-space: nowrap; }
nav.bar a:hover { text-decoration: underline; }
nav.bar .spacer { flex: 1; }
nav.bar .disabled { color: var(--muted); opacity: .5; }
main { max-width: 34rem; margin: 0 auto; padding: 2.5rem 1.25rem 4rem; }
.kicker {
  text-transform: uppercase; letter-spacing: .16em;
  font: .72rem/1.4 -apple-system, system-ui, sans-serif;
  color: var(--muted); margin: 0 0 .4rem;
}
h1 { font-size: 1.95rem; line-height: 1.14; font-weight: 600; margin: 0 0 1.6rem; }
h2 {
  font-size: 1rem; letter-spacing: .04em; text-transform: uppercase;
  font-family: -apple-system, system-ui, sans-serif; color: var(--muted);
  margin: 2.6rem 0 1rem;
}
p { margin: 0 0 1.1rem; }
em { font-style: italic; }
blockquote {
  margin: 1.6rem 0; padding: .1rem 0 .1rem 1.1rem;
  border-left: 3px solid var(--rule); color: var(--muted); font-style: italic;
}
blockquote p { margin: 0 0 .5rem; }
hr { border: 0; margin: 2.2rem 0; text-align: center; }
hr::before { content: "\\002A \\00A0 \\002A \\00A0 \\002A"; color: var(--muted); letter-spacing: .1em; }
a { color: var(--link); }
/* Contents page */
.book-title { text-align: center; margin: 1rem 0 .2rem; font-size: 2.4rem; }
.book-sub { text-align: center; color: var(--muted); font-style: italic; margin: 0 0 2.4rem; }
ol.toc { list-style: none; margin: 0; padding: 0; }
ol.toc li { border-bottom: 1px solid var(--rule); }
ol.toc a {
  display: flex; align-items: baseline; gap: .75rem;
  padding: .7rem .2rem; text-decoration: none; color: var(--fg);
}
ol.toc a:hover { background: var(--card); }
ol.toc .num {
  flex: 0 0 6.5rem; font: .72rem/1.5 -apple-system, system-ui, sans-serif;
  text-transform: uppercase; letter-spacing: .1em; color: var(--muted);
}
ol.toc .ttl { flex: 1; }
ol.toc .yr { color: var(--muted); font-variant-numeric: tabular-nums; }
"""

# ------------------------------------------------------------- parsing ---


def ordered_files(manuscript_dir):
    """Frontmatter, then NN- chapters, then appendices — filename order."""
    return sorted(manuscript_dir.glob("*.md"))


def parse_meta(path, text):
    """Return kicker/title/year for navigation and the contents page."""
    is_interlude = INTERLUDE_MARKER in text
    heading_match = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    heading = heading_match.group(1).strip() if heading_match else path.stem

    year, title = "", heading
    ym = re.match(r"^\s*([0-9]{4}(?:[–-][0-9]{2,4})?)\s*:\s*(.+)$", heading)
    if ym:
        year, title = ym.group(1), ym.group(2).strip()

    stem = path.stem
    if stem.startswith("00-") or stem == "00-frontmatter":
        role = "frontmatter"
    elif stem.startswith("appendix"):
        role = "appendix"
    elif is_interlude:
        role = "interlude"
    else:
        role = "chapter"
    return {"role": role, "year": year, "title": title, "heading": heading}


def assign_kickers(metas):
    """Walk the book once to number the non-interlude chapters."""
    chapter_no = 0
    for m in metas:
        if m["role"] == "chapter":
            word = (
                CHAPTER_NUMBER_WORDS[chapter_no]
                if chapter_no < len(CHAPTER_NUMBER_WORDS)
                else str(chapter_no + 1)
            )
            m["kicker"] = f"Chapter {word}"
            chapter_no += 1
        elif m["role"] == "interlude":
            m["kicker"] = "Interlude"
        elif m["role"] == "appendix":
            m["kicker"] = "Appendix"
        else:
            m["kicker"] = "Front Matter"
    return metas


def render_body(text):
    import markdown

    cleaned = text.replace(INTERLUDE_MARKER, "").lstrip()
    return markdown.markdown(cleaned, extensions=["extra"])


# ------------------------------------------------------------ templates ---


def nav_bar(prev_item, next_item):
    def link(item, label, klass=""):
        if not item:
            return f'<span class="disabled">{label}</span>'
        return f'<a href="{item["href"]}"{f" class={klass}" if klass else ""}>{label}</a>'

    prev_html = link(prev_item, "‹ Previous")
    next_html = link(next_item, "Next ›")
    return (
        '<nav class="bar"><div class="inner">'
        f'{prev_html}'
        '<a href="index.html">Contents</a>'
        f'{next_html}'
        "</div></nav>"
    )


def page_html(meta, body, prev_item, next_item):
    kicker = html.escape(meta["kicker"])
    title = html.escape(meta["heading"])
    bar = nav_bar(prev_item, next_item)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {html.escape(BOOK_TITLE)}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
{bar}
<main>
<p class="kicker">{kicker}</p>
{body}
</main>
{bar}
</body>
</html>
"""


def index_html(metas):
    rows = []
    for m in metas:
        if m["role"] == "frontmatter":
            continue  # the title lives on this page already
        num = html.escape(m["kicker"])
        ttl = html.escape(m["title"])
        yr = html.escape(m["year"])
        rows.append(
            f'<li><a href="{m["href"]}">'
            f'<span class="num">{num}</span>'
            f'<span class="ttl">{ttl}</span>'
            f'<span class="yr">{yr}</span></a></li>'
        )
    front = next((m for m in metas if m["role"] == "frontmatter"), None)
    front_link = (
        f'<p style="text-align:center"><a href="{front["href"]}">Title page</a></p>'
        if front
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(BOOK_TITLE)} — Contents</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<main>
<h1 class="book-title">{html.escape(BOOK_TITLE)}</h1>
<p class="book-sub">Five Centuries of History from the Banks of the Thames</p>
<ol class="toc">
{chr(10).join(rows)}
</ol>
{front_link}
</main>
</body>
</html>
"""


# ---------------------------------------------------------------- main ---


def main():
    parser = argparse.ArgumentParser(description="Manuscript folder to multi-page HTML")
    parser.add_argument("manuscript_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    files = ordered_files(args.manuscript_dir)
    if not files:
        sys.exit(f"No .md files found in {args.manuscript_dir}")

    items = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        meta = parse_meta(path, text)
        meta["href"] = path.stem + ".html"
        meta["body"] = render_body(text)
        items.append(meta)

    assign_kickers(items)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "style.css").write_text(STYLESHEET, encoding="utf-8")

    for i, meta in enumerate(items):
        prev_item = items[i - 1] if i > 0 else None
        next_item = items[i + 1] if i < len(items) - 1 else None
        out = args.output_dir / meta["href"]
        out.write_text(page_html(meta, meta["body"], prev_item, next_item), encoding="utf-8")

    (args.output_dir / "index.html").write_text(index_html(items), encoding="utf-8")

    print(f"HTML site written: {args.output_dir}/index.html  ({len(items)} pages + contents)")


if __name__ == "__main__":
    main()
