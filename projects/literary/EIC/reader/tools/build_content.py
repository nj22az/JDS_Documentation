#!/usr/bin/env python3
"""build_content.py — manuscript markdown -> content.json for the React reader.

Keeps the manuscript the single source of truth. Emits one entry per page
(frontmatter, chapters, appendices) with kicker, year, title, epigraph HTML,
hero image, and body HTML (scene breaks styled, section ids, inline figures
injected). Also copies the referenced images into the app's public/assets.

Run:  python3 tools/build_content.py
"""
import json
import re
import shutil
import struct
from pathlib import Path

import markdown


def image_size(path: Path):
    """Return (w, h) for PNG/JPEG without external deps, or None."""
    try:
        with open(path, "rb") as f:
            head = f.read(26)
            if head[:8] == b"\x89PNG\r\n\x1a\n":  # PNG: IHDR at offset 16
                w, h = struct.unpack(">II", head[16:24])
                return w, h
            if head[:2] == b"\xff\xd8":  # JPEG: walk segments
                f.seek(2)
                while True:
                    marker, = struct.unpack(">H", f.read(2))
                    size, = struct.unpack(">H", f.read(2))
                    if 0xFFC0 <= marker <= 0xFFCF and marker not in (0xFFC4, 0xFFC8, 0xFFCC):
                        f.read(1)
                        h, w = struct.unpack(">HH", f.read(4))
                        return w, h
                    f.seek(size - 2, 1)
    except Exception:
        return None
    return None

# This script lives at  projects/literary/EIC/reader/tools/build_content.py
#   parents[0] = tools,  parents[1] = reader,  parents[2] = EIC project root.
APP = Path(__file__).resolve().parents[1]
EIC = Path(__file__).resolve().parents[2]
MANUSCRIPT = EIC / "manuscript"
HTML_ASSETS = EIC / "exports" / "html" / "assets"
ASSETS_JSON = HTML_ASSETS / "data" / "archive-assets.json"

OUT_DATA = APP / "src" / "data" / "content.json"
OUT_PUBLIC = APP / "public" / "assets"

INTERLUDE = "<!-- interlude -->"
CHAPTER_WORDS = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight",
                 "Nine", "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen"]

# Hero image per page (curated), reused from the illustrated edition.
HERO = {
    "00-frontmatter": "front-row-seat-cover",
    "01-1603-the-boy-who-signed": "east-indiaman-cirencester",
    "02-1626-the-man-who-came-back-wrong": "amboyna-massacre",
    "03-1696-the-price-of-a-man": "every-ganj-i-sawai",
    "04-1701-good-for-business": "wapping-old-stairs",
    "05-1757-a-soldiers-arithmetic": "plassey-clive-mir-jafar",
    "06-1770-what-mulvey-saw": "bengal-map-1776",
    "07-1774-too-big-to-sink": "boston-tea-party",
    "08-1790-forty-seven-days": "bligh-open-boat",
    "09-1839-what-pemberton-called-trade": "opium-destruction",
    "10-1858-what-harding-would-not-say": "east-india-house-1796",
    "11-1880-the-hell-ship": "cutty-sark-1871",
    "12-1888-the-watchmans-daughter": "liz-su-laundry",
    "13-1940-a-wardens-watch": "london-blitz",
    "14-2019-what-the-suit-didnt-see": "canary-wharf-west-india-docks",
    "appendix-0-authors-note": "eic-coat-of-arms",
    "appendix-1-timeline": "east-india-dock-1806",
    "appendix-2-bibliography": "east-india-house-1726",
}

INLINE = {
    "01-1603-the-boy-who-signed": [("III. The Boy with the Paper", "eic-coat-of-arms")],
    "02-1626-the-man-who-came-back-wrong": [("VIII. Cotton", "surat-map-1730"), ("IX. The Walls Get Higher", "surat-warehouse")],
    "03-1696-the-price-of-a-man": [("IV. The Odd Gold", "mughal-gold")],
    "04-1701-good-for-business": [("V. The Sound of It", "captain-kidd-hanging")],
    "05-1757-a-soldiers-arithmetic": [("V. Spitalfields", "gin-lane")],
    "06-1770-what-mulvey-saw": [("III. Ten Million", "famine-relief-engraving")],
    "07-1774-too-big-to-sink": [("IV. The Scheme", "tea-chest-caddies"), ("VI. The Marks", "east-india-export-dock")],
    "08-1790-forty-seven-days": [("VII. What the Bread Was For", "breadfruit-tree"), ("VIII. The Flower", "fuchsia-denticulata")],
    "09-1839-what-pemberton-called-trade": [("IV. The Shaking Man", "cinchona-bark")],
    "10-1858-what-harding-would-not-say": [("II. Gin", "gin-lane"), ("VI. Ten Point Five", "east-india-house-1726")],
    "11-1880-the-hell-ship": [("VI. Two Old Company Men", "fighting-temeraire")],
    "12-1888-the-watchmans-daughter": [("I. The Watch Committees", "booth-whitechapel"), ("IX. The Alley", "su-cray-alley"), ("XII. What the River Kept", "fuchsia-botanical")],
    "13-1940-a-wardens-watch": [("III. The Ledger of Destruction", "bombing-density-map")],
    "14-2019-what-the-suit-didnt-see": [("I. Authentic", "prospect-of-whitby-night-author"), ("IV. Tea", "tea-chest-met"), ("VII. The Same River", "mughal-gold")],
}


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower().replace("&amp;", "and")
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-") or "section"


def load_assets():
    return {a["id"]: a for a in json.loads(ASSETS_JSON.read_text(encoding="utf-8"))}


def asset_public(asset):
    """Return the asset dict with a web path under assets/ (copies happen separately)."""
    out = {"id": asset["id"], "file": asset["file"], "alt": asset.get("alt", ""),
           "caption": asset.get("caption", "")}
    size = image_size(HTML_ASSETS.parent / asset["file"])
    if size:
        out["orientation"] = "portrait" if size[1] > size[0] * 1.15 else "landscape"
    return out


def figure_html(asset):
    return (f'<figure class="fig" id="fig-{asset["id"]}">'
            f'<img src="{asset["file"]}" alt="{asset["alt"]}" loading="lazy" decoding="async">'
            f'<figcaption>{asset["caption"]} '
            f'<a class="fig-credit" href="#/credits">Credit</a></figcaption></figure>')


def split_page(text):
    text = text.replace(INTERLUDE, "").lstrip("\n")
    m = re.search(r"^#\s+(.+?)\s*$", text, re.MULTILINE)
    if not m:
        return "", text, ""
    heading = m.group(1).strip()
    before = text[: m.start()]
    body = text[m.end():]
    return heading, body, before


def render_epigraph(before):
    quote = "\n".join(l for l in before.splitlines() if l.startswith(">"))
    if not quote.strip():
        return ""
    return markdown.markdown(quote, extensions=["extra"])


def render_body(body_md, page_key, assets):
    html = markdown.markdown(body_md, extensions=["extra"])
    html = re.sub(r"<hr\s*/?>", '<hr class="scene">', html)

    # add ids to section headings
    def add_id(match):
        text = match.group(1)
        return f'<h2 id="{slugify(text)}">{text}</h2>'
    html = re.sub(r"<h2>(.*?)</h2>", add_id, html)

    # inject inline figures after matching headings
    for heading, asset_id, *_ in INLINE.get(page_key, []):
        if asset_id in assets:
            hid = slugify(heading)
            fig = figure_html(asset_public(assets[asset_id]))
            html = html.replace(f'<h2 id="{hid}">{heading}</h2>',
                                f'<h2 id="{hid}">{heading}</h2>\n{fig}', 1)
    return html


def meta(page_key, heading):
    if page_key.startswith("00-"):
        return "Front Matter", "", heading
    if page_key.startswith("appendix"):
        return "Appendix", "", heading
    year, title = "", heading
    ym = re.match(r"^\s*([0-9]{4}(?:[–-][0-9]{2,4})?)\s*:\s*(.+)$", heading)
    if ym:
        year, title = ym.group(1), ym.group(2).strip()
    return None, year, title  # kicker filled by caller (chapter/interlude counter)


def main():
    assets = load_assets()
    files = sorted(p for p in MANUSCRIPT.glob("*.md") if not p.name.startswith("."))
    pages = []
    chapter_no = 0
    for path in files:
        key = path.stem
        text = path.read_text(encoding="utf-8")
        is_interlude = INTERLUDE in text
        heading, body_md, before = split_page(text)
        kicker, year, title = meta(key, heading)
        if kicker is None:
            if is_interlude:
                kicker = "Interlude"
            else:
                word = CHAPTER_WORDS[chapter_no] if chapter_no < len(CHAPTER_WORDS) else str(chapter_no + 1)
                kicker = f"Chapter {word}"
                chapter_no += 1
        hero_id = HERO.get(key)
        hero = asset_public(assets[hero_id]) if hero_id in assets else None
        pages.append({
            "id": key,
            "kicker": kicker,
            "year": year,
            "title": title,
            "epigraph": render_epigraph(before),
            "hero": hero,
            "body": render_body(body_md, key, assets),
        })

    # credits list (from assets) for the credits view
    credits = []
    for a in assets.values():
        credits.append({
            "id": a["id"], "file": a["file"], "alt": a.get("alt", ""),
            "title": a.get("title", ""), "caption": a.get("caption", ""),
            "source_url": a.get("source_url", ""), "source_note": a.get("source_note", ""),
            "creator": a.get("creator", ""), "date": a.get("date", ""),
            "license": a.get("license", "") or a.get("usage_terms", ""),
        })

    cover = assets.get("front-row-seat-cover")
    out = {
        "title": "The Front-Row Seat",
        "subtitle": "Five Centuries of History from the Banks of the Thames",
        "cover": asset_public(cover) if cover else None,
        "pages": pages,
        "credits": credits,
    }
    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_DATA.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # copy images (skip the private-source folder)
    OUT_PUBLIC.mkdir(parents=True, exist_ok=True)
    for sub in ("img", "generated"):
        src = HTML_ASSETS / sub
        if src.is_dir():
            dst = OUT_PUBLIC / sub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("._*"))
    print(f"content.json: {len(pages)} pages, {len(credits)} credits")


if __name__ == "__main__":
    main()
