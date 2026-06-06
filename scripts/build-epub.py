#!/usr/bin/env python3
"""Build a KDP-ready EPUB for JDS-PRJ-GEN-001.

The book is English-first (master: 'The Garage Reset') with a Swedish edition
('Städa i Garaget'). Pass --lang to choose; English is the default. Assembles the
front matter, all chapters and the back matter into a valid EPUB 3 that uploads
directly to Amazon KDP.

Usage:
    python3 scripts/build-epub.py                 # English EPUB
    python3 scripts/build-epub.py --lang sv        # Swedish EPUB
    python3 scripts/build-epub.py --check          # list section order
"""

import sys
from pathlib import Path

import markdown
from ebooklib import epub

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

PROJECT = Path("projects/JDS-PRJ-GEN-001")
MANUSCRIPT = PROJECT / "02-manuscript"
PRODUCTION = PROJECT / "04-production"

MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]

LANG_CONFIG = {
    "en": {
        "root": MANUSCRIPT / "en",
        "chapter_glob": "chapter-*.md",
        "title": "The Garage Reset",
        "subtitle": "A 10-Step Program to Declutter, Organize, and Keep Order "
                    "in Your Garage and Workshop",
        "language": "en",
        "identifier": "the-garage-reset-2026",
        "output": PRODUCTION / "The-Garage-Reset.epub",
        "cover": PRODUCTION / "cover-en.jpg",
        "no_toc": {"00-title", "01-copyright"},
    },
    "sv": {
        "root": MANUSCRIPT / "sv",
        "chapter_glob": "kapitel-*.md",
        "title": "Städa i Garaget",
        "subtitle": "Rensa, organisera och håll ordning i verkstad och förråd",
        "language": "sv",
        "identifier": "stada-i-garaget-2026",
        "output": PRODUCTION / "Stada-i-Garaget.epub",
        "cover": PRODUCTION / "cover.jpg",
        "no_toc": {"00-titelsida", "01-copyright"},
    },
}

AUTHOR = "Nils Johansson"

STYLESHEET = """
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55; }
h1 { font-size: 1.6em; line-height: 1.2; margin: 1.2em 0 0.6em; page-break-before: always; }
h2 { font-size: 1.2em; margin: 1.4em 0 0.4em; }
h3 { font-size: 1.05em; margin: 1.2em 0 0.3em; }
h4 { font-size: 1em; font-style: italic; margin: 1em 0 0.3em; }
p { margin: 0 0 0.8em; text-align: justify; }
blockquote {
    background: #f3f3f1; border-left: 4px solid #4a4a4a;
    margin: 1.2em 0; padding: 0.6em 1em; border-radius: 2px;
}
blockquote p { text-align: left; }
blockquote strong:first-child { display: block; margin-bottom: 0.3em; }
ul, ol { margin: 0 0 0.9em 1.2em; }
li { margin-bottom: 0.3em; }
hr { border: none; border-top: 1px solid #ccc; margin: 1.5em 0; }
""".strip()


def read_md(path):
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("<!--")]
    text = "\n".join(lines).strip()
    title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")),
                 path.stem)
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    return title, body


def ordered_sections(cfg):
    sections = []
    for path in sorted((cfg["root"] / "frontmatter").glob("*.md")):
        sections.append(("front", path.stem, path))
    for path in sorted((cfg["root"] / "chapters").glob(cfg["chapter_glob"])):
        sections.append(("chapter", path.stem, path))
    for path in sorted((cfg["root"] / "backmatter").glob("*.md")):
        sections.append(("back", path.stem, path))
    return sections


def build(cfg):
    book = epub.EpubBook()
    book.set_identifier(cfg["identifier"])
    book.set_title(cfg["title"])
    book.set_language(cfg["language"])
    book.add_author(AUTHOR)
    book.add_metadata("DC", "description", cfg["subtitle"])

    cover = cfg["cover"]
    if cover.exists():
        book.set_cover("cover.jpg", cover.read_bytes())

    css = epub.EpubItem(uid="style", file_name="style/main.css",
                        media_type="text/css", content=STYLESHEET)
    book.add_item(css)

    html_items, toc = [], []
    for index, (kind, slug, path) in enumerate(ordered_sections(cfg)):
        title, body = read_md(path)
        item = epub.EpubHtml(title=title, file_name=f"{index:02d}_{slug}.xhtml",
                             lang=cfg["language"])
        item.content = f"<html><head></head><body>{body}</body></html>"
        item.add_item(css)
        book.add_item(item)
        html_items.append(item)
        if slug not in cfg["no_toc"]:
            toc.append(item)

    book.toc = toc
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = (["cover", "nav"] if cover.exists() else ["nav"]) + html_items

    cfg["output"].parent.mkdir(parents=True, exist_ok=True)
    epub.write_epub(str(cfg["output"]), book)
    return len(html_items)


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    cfg = LANG_CONFIG[lang]

    if "--check" in args:
        for index, (kind, slug, path) in enumerate(ordered_sections(cfg)):
            title, _ = read_md(path)
            print(f"  {index:02d}  [{kind:7}] {title}")
        return 0

    count = build(cfg)
    size_kb = cfg["output"].stat().st_size / 1024
    note = "" if cfg["cover"].exists() else "  (no cover yet — run build-cover.py)"
    print(f"Built {cfg['output']} [{lang}] — {count} sections, {size_kb:.0f} KB{note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
