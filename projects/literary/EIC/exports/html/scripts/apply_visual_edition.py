#!/usr/bin/env python3
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data" / "archive-assets.json"


CHAPTERS = [
    ("00-frontmatter.html", "Front Matter", "The Front-Row Seat", "", "front-row-seat-cover"),
    ("01-1603-the-boy-who-signed.html", "Chapter One", "The Boy Who Signed", "1603", "east-indiaman-cirencester"),
    ("02-1626-the-man-who-came-back-wrong.html", "Chapter Two", "The Man Who Came Back Wrong", "1626", "amboyna-massacre"),
    ("03-1696-the-price-of-a-man.html", "Chapter Three", "The Price of a Man", "1696", "every-ganj-i-sawai"),
    ("04-1701-good-for-business.html", "Chapter Four", "Good for Business", "1701", "wapping-old-stairs"),
    ("05-1757-a-soldiers-arithmetic.html", "Chapter Five", "A Soldier's Arithmetic", "1757", "plassey-clive-mir-jafar"),
    ("06-1770-what-mulvey-saw.html", "Chapter Six", "What Mulvey Saw", "1770", "bengal-map-1776"),
    ("07-1774-too-big-to-sink.html", "Chapter Seven", "Too Big to Sink", "1774", "boston-tea-party"),
    ("08-1790-forty-seven-days.html", "Interlude", "Forty-Seven Days", "1790", "bligh-open-boat"),
    ("09-1839-what-pemberton-called-trade.html", "Chapter Eight", "What Pemberton Called Trade", "1839", "opium-destruction"),
    ("10-1858-what-harding-would-not-say.html", "Chapter Nine", "What Harding Would Not Say", "1858", "east-india-house-1796"),
    ("11-1880-the-hell-ship.html", "Interlude", "The Hell Ship", "1880", "cutty-sark-1871"),
    ("12-1888-the-watchmans-daughter.html", "Interlude", "The Watchman's Daughter", "1888", "whitechapel-murders-map"),
    ("13-1940-a-wardens-watch.html", "Chapter Ten", "A Warden's Watch", "1940-1945", "london-blitz"),
    ("14-2019-what-the-suit-didnt-see.html", "Chapter Eleven", "What the Suit Didn't See", "2019", "canary-wharf-west-india-docks"),
    ("appendix-0-authors-note.html", "Appendix", "Author's Note", "", "eic-coat-of-arms"),
    ("appendix-1-timeline.html", "Appendix", "Timeline: The East India Company at Wapping", "", "east-india-dock-1806"),
    ("appendix-2-bibliography.html", "Appendix", "Select Bibliography", "", "east-india-house-1726"),
]


INLINE_FIGURES = {
    "01-1603-the-boy-who-signed.html": [
        ("III. The Boy with the Paper", "eic-coat-of-arms", "artifact"),
    ],
    "02-1626-the-man-who-came-back-wrong.html": [
        ("VIII. Cotton", "surat-map-1730", "map"),
        ("IX. The Walls Get Higher", "surat-warehouse", "archive"),
    ],
    "03-1696-the-price-of-a-man.html": [
        ("IV. The Odd Gold", "mughal-gold", "artifact"),
    ],
    "04-1701-good-for-business.html": [
        ("V. The Sound of It", "captain-kidd-hanging", "archive"),
    ],
    "05-1757-a-soldiers-arithmetic.html": [
        ("V. Spitalfields", "gin-lane", "archive"),
    ],
    "06-1770-what-mulvey-saw.html": [
        ("III. Ten Million", "famine-relief-engraving", "archive"),
    ],
    "07-1774-too-big-to-sink.html": [
        ("IV. The Scheme", "tea-chest-caddies", "artifact"),
        ("VI. The Marks", "east-india-export-dock", "archive"),
    ],
    "08-1790-forty-seven-days.html": [
        ("VII. What the Bread Was For", "breadfruit-tree", "artifact"),
        ("VIII. The Flower", "fuchsia-denticulata", "artifact"),
    ],
    "09-1839-what-pemberton-called-trade.html": [
        ("IV. The Shaking Man", "cinchona-bark", "artifact"),
    ],
    "10-1858-what-harding-would-not-say.html": [
        ("II. Gin", "gin-lane", "archive"),
        ("VI. Ten Point Five", "east-india-house-1726", "archive"),
    ],
    "11-1880-the-hell-ship.html": [
        ("VI. Two Old Company Men", "fighting-temeraire", "archive"),
    ],
    "12-1888-the-watchmans-daughter.html": [
        ("I. The Watch Committees", "booth-whitechapel", "map"),
        ("XII. What the River Kept", "fuchsia-botanical", "artifact"),
    ],
    "13-1940-a-wardens-watch.html": [
        ("III. The Ledger of Destruction", "bombing-density-map", "map"),
    ],
    "14-2019-what-the-suit-didnt-see.html": [
        ("I. Authentic", "prospect-of-whitby-night-author", "archive"),
        ("II. The Student of the Company", "east-india-company-docks-1844", "archive"),
        ("IV. Tea", "tea-chest-met", "artifact"),
        ("VII. The Same River", "mughal-gold", "artifact"),
    ],
}


GENERATED_BRIEFS = [
    {
        "slot": "Bounty interlude chapter plate",
        "prompt": "Painted historical illustration of nineteen exhausted sailors in a twenty-three-foot open boat on a grey ocean, no named portrait likeness, restrained popular-history style, no text.",
    },
    {
        "slot": "Cutty Sark chapter plate",
        "prompt": "Painted historical illustration of a tea clipper becalmed on the Java Sea at dawn, seen from a distance, no identifiable people, muted maritime palette, no text.",
    },
    {
        "slot": "1888 object study",
        "prompt": "Painted object study of a folded wooden fan, laundry linen, fog-damp cobbles, and a fuchsia cutting; no people, no violence, restrained historical realism.",
    },
    {
        "slot": "1770 famine ledger",
        "prompt": "Painted still life of a Bengal revenue ledger, empty rice bowl, monsoon-dark sky seen through a window, no bodies, no text, serious popular-history tone.",
    },
]


def load_assets():
    assets = json.loads(DATA.read_text(encoding="utf-8"))
    return {asset["id"]: asset for asset in assets}


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower().replace("&amp;", "and")
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "section"


def strip_generated(html):
    html = re.sub(r"\n?<!-- visual-edition:start -->.*?<!-- visual-edition:end -->\n?", "\n", html, flags=re.S)
    html = re.sub(r"\s+id=\"[^\"]+\"", "", html) if False else html
    return html


def ensure_head(html):
    if "reading.js" not in html:
        html = html.replace(
            '<link rel="stylesheet" href="style.css">',
            '<link rel="stylesheet" href="style.css">\n<script src="reading.js" defer></script>',
        )
    return html


def ensure_body_main(html, body_class):
    html = re.sub(r"<body(?: class=\"[^\"]*\")?>", f'<body class="{body_class}">', html, count=1)
    html = html.replace("<main>", '<main class="chapter">', 1)
    return html


def figure(asset, kind="plate", eager=False):
    loading = "eager" if eager else "lazy"
    return f'''<!-- visual-edition:start -->
<figure class="visual {kind}" id="fig-{asset['id']}">
  <div class="visual-media"><img src="{asset['file']}" alt="{asset['alt']}" loading="{loading}" decoding="async"></div>
  <figcaption><span class="fig-kicker">{label_for(asset)}</span> {asset['caption']} <a href="visual-credits.html#{asset['id']}">Credit</a>.</figcaption>
</figure>
<!-- visual-edition:end -->'''


def label_for(asset):
    license_name = asset.get("license", "")
    if license_name == "Generated image":
        return "Generated plate"
    if license_name in {"Public domain", "CC0", "No restrictions"}:
        return "Archive plate"
    return "Archive plate"


def add_section_ids(html):
    seen = set()

    def repl(match):
        attrs = match.group(1) or ""
        text = match.group(2)
        if " id=" in attrs:
            return match.group(0)
        base = slugify(text)
        slug = base
        i = 2
        while slug in seen:
            slug = f"{base}-{i}"
            i += 1
        seen.add(slug)
        return f'<h2 id="{slug}"{attrs}>{text}</h2>'

    return re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, html)


def section_list(html):
    headings = re.findall(r'<h2 id="([^"]+)">([^<]+)</h2>', html)
    if not headings:
        return ""
    items = "\n".join(f'<li><a href="#{hid}">{text}</a></li>' for hid, text in headings)
    return f'''<!-- visual-edition:start -->
<details class="section-list">
  <summary>Chapter Sections</summary>
  <ol>
{items}
  </ol>
</details>
<!-- visual-edition:end -->'''


def insert_after_h1(html, insert):
    return re.sub(r"(</h1>)", r"\1\n" + insert, html, count=1)


def insert_after_heading(html, heading_text, insert):
    escaped = re.escape(heading_text)
    pattern = rf'(<h2 id="[^"]+">{escaped}</h2>)'
    return re.sub(pattern, r"\1\n" + insert, html, count=1)


def enhance_page(page, plate_id, assets):
    path = ROOT / page
    html = strip_generated(path.read_text(encoding="utf-8"))
    html = ensure_head(html)
    html = ensure_body_main(html, "reader-page")
    html = add_section_ids(html)
    plate = figure(assets[plate_id], "plate", eager=True)
    html = insert_after_h1(html, plate + "\n" + section_list(html))
    for heading, asset_id, kind in INLINE_FIGURES.get(page, []):
        if asset_id in assets:
            html = insert_after_heading(html, heading, figure(assets[asset_id], kind))
    path.write_text(html, encoding="utf-8")


def render_index(assets):
    rows = []
    for file, label, title, year, plate_id in CHAPTERS[1:]:
        asset = assets[plate_id]
        year_html = f'<span class="yr">{year}</span>' if year else '<span class="yr"></span>'
        rows.append(
            f'''<li>
  <a href="{file}">
    <img src="{asset['file']}" alt="" loading="eager" decoding="async">
    <span class="toc-copy"><span class="num">{label}</span><span class="ttl">{title}</span></span>
    {year_html}
  </a>
</li>'''
        )
    rows.append(
        '''<li>
  <a href="visual-credits.html">
    <img src="assets/img/eic-coat-of-arms.png" alt="" loading="eager" decoding="async">
    <span class="toc-copy"><span class="num">Appendix</span><span class="ttl">Visual Credits</span></span>
    <span class="yr"></span>
  </a>
</li>'''
    )
    toc = "\n".join(rows)
    cover = assets["front-row-seat-cover"]
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="The Front-Row Seat: Five Centuries of History from the Banks of the Thames.">
<meta property="og:title" content="The Front-Row Seat">
<meta property="og:description" content="Five Centuries of History from the Banks of the Thames">
<meta property="og:image" content="{cover['file']}">
<title>The Front-Row Seat — Contents</title>
<link rel="stylesheet" href="style.css">
</head>
<body class="contents">
<main class="contents-page">
<section class="cover-hero">
  <img src="{cover['file']}" alt="{cover['alt']}" loading="eager" decoding="async">
  <div class="cover-copy">
    <p class="kicker">Illustrated Web Edition</p>
    <h1 class="book-title">The Front-Row Seat</h1>
    <p class="book-sub">Five Centuries of History from the Banks of the Thames</p>
    <p class="cover-link"><a href="00-frontmatter.html">Start Reading</a></p>
  </div>
</section>
<ol class="toc visual-toc">
{toc}
</ol>
</main>
</body>
</html>
'''
    (ROOT / "index.html").write_text(html, encoding="utf-8")


def render_credits(assets):
    rows = []
    for asset in assets.values():
        url = asset.get("source_url") or ""
        if url.startswith(("https://", "http://")):
            label = html.escape(str(asset.get("commons_title") or asset["title"]))
            source = f'<a href="{html.escape(url, quote=True)}" rel="noopener noreferrer">{label}</a>'
        else:
            source = html.escape(str(asset.get("source_note", "Generated for this edition")))
        rows.append(
            f'''<article class="credit-item" id="{asset['id']}">
  <img src="{asset['file']}" alt="{asset['alt']}" loading="lazy" decoding="async">
  <div>
    <h2>{asset['title']}</h2>
    <p>{asset['caption']}</p>
    <p><strong>Source:</strong> {source}</p>
    <p><strong>Creator:</strong> {asset.get('creator') or 'Unknown'}<br>
    <strong>Date:</strong> {asset.get('date') or 'Unknown'}<br>
    <strong>License:</strong> {asset.get('license') or asset.get('usage_terms') or 'See source'}</p>
  </div>
</article>'''
        )
    briefs = "\n".join(
        f"<li><strong>{brief['slot']}:</strong> {brief['prompt']}</li>" for brief in GENERATED_BRIEFS
    )
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Visual Credits — The Front-Row Seat</title>
<link rel="stylesheet" href="style.css">
<script src="reading.js" defer></script>
</head>
<body class="reader-page">
<nav class="bar"><div class="inner"><a href="appendix-2-bibliography.html">‹ Previous</a><a href="index.html">Contents</a><span class="disabled">Next ›</span></div></nav>
<main class="chapter credits-page">
<p class="kicker">Appendix</p>
<h1>Visual Credits</h1>
<p>The edition uses local copies of public-domain, CC0, no-restrictions, and selected Creative Commons archival images, plus one generated cover illustration. Credits are retained here so chapter captions can stay readable.</p>
<section class="credit-list">
{''.join(rows)}
</section>
<h2>Generated Illustration Expansion Briefs</h2>
<p>Future generated illustrations should stay object- or scene-led unless a fixed character reference sheet is created first.</p>
<ul>
{briefs}
</ul>
</main>
<nav class="bar"><div class="inner"><a href="appendix-2-bibliography.html">‹ Previous</a><a href="index.html">Contents</a><span class="disabled">Next ›</span></div></nav>
</body>
</html>
'''
    (ROOT / "visual-credits.html").write_text(html, encoding="utf-8")


def fix_bibliography_next():
    path = ROOT / "appendix-2-bibliography.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace('<span class="disabled">Next ›</span>', '<a href="visual-credits.html">Next ›</a>')
    path.write_text(html, encoding="utf-8")


def main():
    assets = load_assets()
    for page, _, _, _, plate_id in CHAPTERS:
        enhance_page(page, plate_id, assets)
    render_index(assets)
    render_credits(assets)
    fix_bibliography_next()


if __name__ == "__main__":
    main()
