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

import re
import sys
from pathlib import Path

import markdown
from ebooklib import epub

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

PROJECT = Path("projects/JDS-PRJ-GEN-001")
MANUSCRIPT = PROJECT / "02-manuscript"
PRODUCTION = PROJECT / "04-production"
IMAGES_DIR = PROJECT / "03-assets" / "images"
FIGURES_DIR = IMAGES_DIR / "figures"

MD_EXTENSIONS = ["extra", "sane_lists", "smarty"]

LANG_CONFIG = {
    "en": {
        "root": MANUSCRIPT / "en",
        "chapter_glob": "chapter-*.md",
        "title": "The Garage Reset",
        "subtitle": "A 10-Step Programme to Declutter, Organise, and Keep Order "
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
img { max-width: 100%; height: auto; margin: 1em auto; display: block; }
img.qr { width: 120px; display: block; margin: 0.4em 0; }
figure.fig { margin: 1.2em 0; text-align: center; }
figure.fig figcaption { font-size: 0.85em; color: #555; margin-top: 0.3em; }
.figph { border: 2px dashed #9aa7b4; background: #f4f6f8; padding: 1em; margin: 1.2em 0;
    text-align: center; color: #33475b; border-radius: 3px; line-height: 1.5; }
""".strip()


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
        return (f'<figure class="fig"><img src="images/{f.name}" alt="Figure {n}"/>'
                f'<figcaption><strong>Figure {n}.</strong> {cap}</figcaption></figure>')
    return (f'<div class="figph"><strong>FIGURE {n} — image to come</strong><br/>{cap}<br/>'
            f'<em>Place fig-{int(n):02d}.jpg in 03-assets/images/figures/ and rebuild.</em></div>')


def read_md(path):
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines()
             if not ln.strip().startswith("<!--")]
    text = "\n".join(lines).strip()
    title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")),
                 path.stem)
    text = re.sub(r'\[\[FIGURE:(\d+)\|(.+?)\]\]', _figure_html, text, flags=re.S)
    body = markdown.markdown(text, extensions=MD_EXTENSIONS)
    # Flatten any manuscript-relative image path to the EPUB-internal images/ folder.
    body = re.sub(r'src="[^"]*?/([^"/]+\.png)"', r'src="images/\1"', body)
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

    # Embed only this edition's images (diagrams + QR codes). SV files end in "-sv".
    images = sorted(IMAGES_DIR.glob("*.png")) + sorted((IMAGES_DIR / "qr").glob("*.png"))
    for image_path in images:
        is_sv = image_path.stem.endswith("-sv")
        if (cfg["language"] == "sv") != is_sv:
            continue
        book.add_item(epub.EpubItem(uid=f"img_{image_path.stem}",
                                    file_name=f"images/{image_path.name}",
                                    media_type="image/png",
                                    content=image_path.read_bytes()))
    # Embed any supplied figure images (fig-01.jpg/png …) — numbered for automation.
    for fp in sorted(FIGURES_DIR.glob("fig-*")) if FIGURES_DIR.exists() else []:
        if fp.suffix.lower() in (".png", ".jpg", ".jpeg"):
            mt = "image/png" if fp.suffix.lower() == ".png" else "image/jpeg"
            book.add_item(epub.EpubItem(uid=f"fig_{fp.stem}", file_name=f"images/{fp.name}",
                                        media_type=mt, content=fp.read_bytes()))

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
