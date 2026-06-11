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

import html
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
FONTS_DIR = PROJECT / "03-assets" / "fonts"

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
/* Rounded maru-gothic display font (M PLUS Rounded 1c, OFL; subset to Latin +
   the five box icons by build-fonts.py). Used for headings and the compartment
   "bento" furniture — the friendly, Japanese-information-design look. */
@font-face { font-family: 'Rounded'; font-weight: 400;
    src: url('../fonts/MPLUSRounded1c-Regular-subset.ttf'); }
@font-face { font-family: 'Rounded'; font-weight: 500;
    src: url('../fonts/MPLUSRounded1c-Medium-subset.ttf'); }
@font-face { font-family: 'Rounded'; font-weight: 700;
    src: url('../fonts/MPLUSRounded1c-Bold-subset.ttf'); }
body { font-family: Georgia, 'Times New Roman', serif; line-height: 1.55; }
h1, h2, h3, h4 { font-family: 'Rounded', Georgia, sans-serif; }
h1 { font-size: 1.6em; line-height: 1.2; margin: 1.2em 0 0.6em; page-break-before: always;
    font-weight: 700; }
h2 { font-size: 1.2em; margin: 1.4em 0 0.4em; font-weight: 700; }
h3 { font-size: 1.05em; margin: 1.2em 0 0.3em; font-weight: 500; }
h4 { font-size: 1em; font-style: italic; margin: 1em 0 0.3em; }
p { margin: 0 0 0.8em; text-align: left; }
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

/* Colour-coded boxes (JDS-PRO-007 §6: colour is language, never colour alone).
   Bold "candy-panel" style (Japanese packaging influence): a solid saturated
   header bar with a white icon + label, on a clean white card with a chunky
   rounded border. The header colour + icon + label survive greyscale (§6.2). */
.box { background: #fff; border: 1.5px solid #ccc;
    margin: 1.3em 0; border-radius: 14px; overflow: hidden; }
.box-head { margin: 0; padding: 0.42em 0.9em; color: #fff;
    font-family: 'Rounded', sans-serif; font-weight: 700; font-size: 1.04em;
    letter-spacing: 0.01em; }
.box-icon { margin-right: 0.5em; font-size: 0.9em; vertical-align: 0.04em; }
/* The body is a coloured "tray"; each paragraph / list item becomes its own
   white compartment, and the tray colour shows between them as the dividers. */
.box-body { padding: 4px; }
.box-body p { text-align: left; }
.box-body ul, .box-body ol { margin: 0; padding: 0; list-style-position: inside; }
.box-body > p, .box-body li { background: #fff; border-radius: 7px;
    margin: 4px; padding: 0.4em 0.7em; }
.box-body li { margin-left: 4px; }
.box.box-safety { border-color: #cf3127; }
.box.box-safety .box-head { background: #cf3127; } .box.box-safety .box-body { background: #f6ddda; }
.box.box-do { border-color: #2f8f5b; }
.box.box-do .box-head { background: #2f8f5b; } .box.box-do .box-body { background: #dcefe4; }
.box.box-rule { border-color: #1b3a5c; }
.box.box-rule .box-head { background: #1b3a5c; } .box.box-rule .box-body { background: #dde4ee; }
.box.box-specs { border-color: #2e7fa6; }
.box.box-specs .box-head { background: #2e7fa6; } .box.box-specs .box-body { background: #daeaf3; }
.box.box-soft { border-color: #a9741c; }
.box.box-soft .box-head { background: #a9741c; } .box.box-soft .box-body { background: #f2e6cd; }

/* Chapter-opener dashboard (JDS-PRO-007 §5.3). A rounded 2x2 "bento": small-caps
   label + value, so the reader sees the shape of the chapter at a glance. The
   wrapper rounds + clips the table's square corners. */
.chapter-card-wrap { border: 1px solid #c9d2db; border-radius: 12px;
    overflow: hidden; margin: 0.4em 0 1.5em; }
table.chapter-card { width: 100%; border-collapse: collapse; }
table.chapter-card td.cc-cell { width: 50%; border: 1px solid #c9d2db;
    padding: 0.5em 0.7em; vertical-align: top; background: #f6f8fa; }
.cc-k { display: block; font-size: 0.68em; letter-spacing: 0.12em;
    text-transform: uppercase; color: #3f7e96; margin-bottom: 0.15em;
    font-family: 'Rounded', sans-serif; font-weight: 500; }
.cc-v { display: block; color: #1b3a5c; line-height: 1.3;
    font-family: 'Rounded', Georgia, sans-serif; font-weight: 700; }

/* Compartment legend (the "how this book is laid out" bento). */
.legend { border: 1px solid #d4d4d0; border-radius: 12px; overflow: hidden;
    padding: 0; margin: 1.2em 0; background: #fafafa; }
.legend table { width: 100%; border-collapse: collapse; }
.legend td { padding: 0.45em 0.7em; vertical-align: top; font-size: 0.95em;
    border-bottom: 1px solid #eee; }
.legend tr:last-child td { border-bottom: none; }
.legend td:first-child { white-space: nowrap; width: 11em;
    font-family: 'Rounded', Georgia, sans-serif; font-weight: 700; }
.legend th { background: #1b3a5c; color: #fff; text-align: left; padding: 0.45em 0.7em;
    font-family: 'Rounded', sans-serif; font-weight: 500; }
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


def _card_html(m):
    """Render a chapter-opener dashboard from [[CARD step=.. | time=.. | task=.. | need=..]].

    A four-cell compartment (JDS-PRO-007 §5.3) the reader scans before the prose:
    where this chapter sits, how long it takes, the one task, and what to gather.
    """
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
# Each recognised box label maps to a class; the CSS pairs the colour with a
# greyscale-safe icon + the bold label so it reads on e-ink and photocopies.
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
            # Split the label off its own header; the rest becomes the card body.
            head = re.match(r'\*\*(.+?)\*\*[ \t]*(.*)', inner, flags=re.S)
            label, body_md = head.group(1).strip(), head.group(2).strip()
            # A top-level list needs a blank line above it to parse; wrapped/indented
            # sub-bullets (Specs boxes) are left intact.
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
    text = "\n".join(lines).strip()
    title = next((ln[2:].strip() for ln in text.splitlines() if ln.startswith("# ")),
                 path.stem)
    text = re.sub(r'\[\[FIGURE:(\d+)\|(.+?)\]\]', _figure_html, text, flags=re.S)
    text = re.sub(r'\[\[CARD\s+(.+?)\]\]', _card_html, text, flags=re.S)
    text = _render_box_blocks(text)
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

    # Embed the subset rounded display font (built by build-fonts.py).
    for font_path in sorted(FONTS_DIR.glob("*-subset.ttf")) if FONTS_DIR.exists() else []:
        book.add_item(epub.EpubItem(uid=f"font_{font_path.stem}",
                                    file_name=f"fonts/{font_path.name}",
                                    media_type="font/ttf",
                                    content=font_path.read_bytes()))

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
