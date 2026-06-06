#!/usr/bin/env python3
"""Build a KDP-ready EPUB for 'Städa i Garaget' (JDS-PRJ-GEN-001).

Assembles the front matter, all 15 chapters and the back matter into a single
valid EPUB 3 file that can be uploaded directly to Amazon KDP (the recommended
reflowable format). Markdown is converted to XHTML; a Kindle-safe stylesheet
renders the boxes and headings.

Usage:
    python3 scripts/build-epub.py            # build the EPUB
    python3 scripts/build-epub.py --check     # list the section order, build nothing
"""

import re
import sys
from pathlib import Path

import markdown
from ebooklib import epub

# --- Configuration (JDS-PRO-004 §3: no magic values in logic) ------------------

PROJECT = Path("projects/JDS-PRJ-GEN-001")
MANUSCRIPT = PROJECT / "02-manuscript"
CHAPTERS_DIR = MANUSCRIPT / "chapters"
FRONT_DIR = MANUSCRIPT / "frontmatter"
BACK_DIR = MANUSCRIPT / "backmatter"
OUTPUT = PROJECT / "04-production" / "Stada-i-Garaget.epub"
COVER = PROJECT / "04-production" / "cover.jpg"

BOOK_TITLE = "Städa i Garaget"
BOOK_SUBTITLE = "Rensa, organisera och håll ordning i verkstad och förråd"
BOOK_AUTHOR = "Nils Johansson"
BOOK_LANGUAGE = "sv"
BOOK_IDENTIFIER = "stada-i-garaget-2026"

MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]

# Sections that are front matter (not listed in the reading-order table of contents).
FRONT_NO_TOC = {"00-titelsida", "01-copyright"}

STYLESHEET = """
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55; }
h1 { font-size: 1.6em; line-height: 1.2; margin: 1.2em 0 0.6em; page-break-before: always; }
h2 { font-size: 1.2em; margin: 1.4em 0 0.4em; }
h3 { font-size: 1.05em; margin: 1.2em 0 0.3em; }
h4 { font-size: 1em; font-style: italic; margin: 1em 0 0.3em; }
p { margin: 0 0 0.8em; text-align: justify; }
blockquote {
    background: #f3f3f1;
    border-left: 4px solid #4a4a4a;
    margin: 1.2em 0;
    padding: 0.6em 1em;
    border-radius: 2px;
}
blockquote p { text-align: left; }
blockquote strong:first-child { display: block; margin-bottom: 0.3em; }
ul, ol { margin: 0 0 0.9em 1.2em; }
li { margin-bottom: 0.3em; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.5em 0; }
""".strip()


def read_md(path):
    """Return (title, xhtml_body) for a markdown file, stripping HTML comments."""
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("<!--")]
    text = "\n".join(lines).strip()
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    return title, body


def ordered_sections():
    """Return the full ordered list of (kind, slug, path) sections of the book."""
    sections = []
    for path in sorted(FRONT_DIR.glob("*.md")):
        sections.append(("front", path.stem, path))
    for path in sorted(CHAPTERS_DIR.glob("kapitel-*.md")):
        sections.append(("chapter", path.stem, path))
    for path in sorted(BACK_DIR.glob("*.md")):
        sections.append(("back", path.stem, path))
    return sections


def build():
    book = epub.EpubBook()
    book.set_identifier(BOOK_IDENTIFIER)
    book.set_title(BOOK_TITLE)
    book.set_language(BOOK_LANGUAGE)
    book.add_author(BOOK_AUTHOR)
    book.add_metadata("DC", "description", BOOK_SUBTITLE)

    if COVER.exists():
        book.set_cover("cover.jpg", COVER.read_bytes())

    css = epub.EpubItem(uid="style", file_name="style/main.css",
                        media_type="text/css", content=STYLESHEET)
    book.add_item(css)

    html_items = []
    toc = []
    for index, (kind, slug, path) in enumerate(ordered_sections()):
        title, body = read_md(path)
        item = epub.EpubHtml(title=title, file_name=f"{index:02d}_{slug}.xhtml",
                             lang=BOOK_LANGUAGE)
        item.content = f"<html><head></head><body>{body}</body></html>"
        item.add_item(css)
        book.add_item(item)
        html_items.append(item)
        if slug not in FRONT_NO_TOC:
            toc.append(item)

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["cover", "nav"] + html_items if COVER.exists() else ["nav"] + html_items

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(OUTPUT), book)
    return len(html_items)


def main():
    if "--check" in sys.argv[1:]:
        for index, (kind, slug, path) in enumerate(ordered_sections()):
            title, _ = read_md(path)
            print(f"  {index:02d}  [{kind:7}] {title}")
        return 0
    count = build()
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Built {OUTPUT} — {count} sections, {size_kb:.0f} KB"
          + ("" if COVER.exists() else "  (no cover.jpg yet — run build-cover.py)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
