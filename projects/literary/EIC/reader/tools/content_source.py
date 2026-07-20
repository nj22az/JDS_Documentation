"""Load, validate, parse, and render the manuscript source."""

import json
import re
import struct
from pathlib import Path

import markdown

from content_config import (
    ASSETS_JSON,
    FRONTMATTER_PATTERN,
    HERO_FALLBACK,
    HTML_ASSETS,
    MANUSCRIPT,
    PORTRAIT_ASPECT_RATIO,
    SCENE_BREAK_PATTERN,
)


def image_size(path):
    """Return (width, height) for a PNG/JPEG without external dependencies."""
    try:
        with path.open("rb") as image_file:
            header = image_file.read(26)
            if header[:8] == b"\x89PNG\r\n\x1a\n":
                return struct.unpack(">II", header[16:24])
            if header[:2] != b"\xff\xd8":
                return None
            image_file.seek(2)
            while True:
                marker_bytes = image_file.read(2)
                if len(marker_bytes) < 2:
                    return None
                marker = struct.unpack(">H", marker_bytes)[0]
                segment_size = struct.unpack(">H", image_file.read(2))[0]
                if 0xFFC0 <= marker <= 0xFFCF and marker not in (0xFFC4, 0xFFC8, 0xFFCC):
                    image_file.read(1)
                    height, width = struct.unpack(">HH", image_file.read(4))
                    return width, height
                image_file.seek(segment_size - 2, 1)
    except (OSError, struct.error):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_assets():
    return {asset["id"]: asset for asset in load_json(ASSETS_JSON)}


def asset_public(asset):
    public_asset = {
        "id": asset["id"],
        "file": asset["file"],
        "alt": asset.get("alt", ""),
        "caption": asset.get("caption", ""),
    }
    dimensions = image_size(HTML_ASSETS.parent / asset["file"])
    if dimensions:
        width, height = dimensions
        public_asset["orientation"] = (
            "portrait" if height > width * PORTRAIT_ASPECT_RATIO else "landscape"
        )
    return public_asset


def parse_scalar(value):
    value = value.strip()
    if value.startswith('"') and value.endswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value[1:-1].replace('\\"', '"')
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def parse_frontmatter(text, path):
    match = FRONTMATTER_PATTERN.match(text)
    if not match:
        raise SystemExit(f"{path}: expected YAML front matter")
    metadata = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        key, separator, value = line.partition(":")
        if not separator:
            raise SystemExit(f"{path}: invalid front-matter line: {line}")
        metadata[key.strip()] = parse_scalar(value)
    required = {"id", "kicker", "year", "title", "hero"}
    missing = required.difference(metadata)
    if missing:
        raise SystemExit(f"{path}: missing YAML keys: {', '.join(sorted(missing))}")
    return metadata, text[match.end():]


def split_page(markdown_text, path):
    heading_match = re.search(r"^#\s+(.+?)\s*$", markdown_text, re.MULTILINE)
    if not heading_match:
        raise SystemExit(f"{path}: expected a level-one heading")
    heading = heading_match.group(1).strip()
    remainder = markdown_text[heading_match.end():].lstrip("\n")
    lines = remainder.splitlines(keepends=True)

    cursor = 0
    while cursor < len(lines) and not lines[cursor].strip():
        cursor += 1
    epigraph_markdown = ""
    if cursor < len(lines) and lines[cursor].lstrip().startswith(">"):
        start = cursor
        while cursor < len(lines):
            line = lines[cursor]
            if line.lstrip().startswith(">") or not line.strip():
                cursor += 1
                continue
            break
        epigraph_markdown = "".join(lines[start:cursor]).strip()

    body = "".join(lines[cursor:]).lstrip()
    body = re.sub(r"^\*\*\*\s*\n", "", body, count=1)
    return heading, epigraph_markdown, body


def slugify(value):
    plain = re.sub(r"<[^>]+>", "", value).lower().replace("&amp;", "and")
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-") or "section"


def render_epigraph(epigraph_markdown):
    if not epigraph_markdown:
        return ""
    return markdown.markdown(epigraph_markdown, extensions=["extra"])


def convert_embedded_figures(rendered_html):
    """Convert exported image-plus-caption pairs back into semantic figures."""
    pattern = re.compile(
        r'<p><img alt="([^"]*)" src="([^"]+)"\s*/?></p>\s*'
        r'<p><em>(.*?)</em></p>',
        re.S,
    )

    def replacement(match):
        alt_text, source, caption = match.groups()
        figure_id = slugify(Path(source).stem)
        return (
            f'<figure class="fig" id="fig-{figure_id}">'
            f'<img src="{source}" alt="{alt_text}" loading="lazy" decoding="async">'
            f"<figcaption>{caption}</figcaption></figure>"
        )

    return pattern.sub(replacement, rendered_html)


def render_body(body_markdown):
    rendered = markdown.markdown(body_markdown, extensions=["extra", "sane_lists"])
    rendered = SCENE_BREAK_PATTERN.sub('<hr class="scene">', rendered)

    def add_section_id(match):
        heading = match.group(1)
        return f'<h2 id="{slugify(heading)}">{heading}</h2>'

    rendered = re.sub(r"<h2>(.*?)</h2>", add_section_id, rendered)
    return convert_embedded_figures(rendered)


def extract_hero_id(raw_hero):
    if not raw_hero or str(raw_hero).lower() == "none":
        return None
    match = re.search(r'(?:^|[,{])\s*id\s*:\s*["\']?([^,"\'}]+)', str(raw_hero))
    return match.group(1).strip() if match else None


def ordered_specs(manifest):
    specs = []
    for item in manifest["front_matter"]:
        specs.append({**item, "book": None})
    for book in manifest["books"]:
        for item in book["pages"]:
            specs.append({**item, "book": book["numeral"]})
    for item in manifest["back_matter"]:
        specs.append({**item, "book": None})
    return specs


def validate_manifest(specs):
    declared = [spec["path"] for spec in specs]
    if len(declared) != len(set(declared)):
        raise SystemExit("publishing-manifest.json contains duplicate paths")
    actual = {
        str(path.relative_to(MANUSCRIPT))
        for path in MANUSCRIPT.rglob("*.md")
        if not path.name.startswith(".")
    }
    declared_set = set(declared)
    if actual != declared_set:
        missing = sorted(actual - declared_set)
        absent = sorted(declared_set - actual)
        details = []
        if missing:
            details.append("unlisted files: " + ", ".join(missing))
        if absent:
            details.append("missing files: " + ", ".join(absent))
        raise SystemExit("manifest mismatch — " + "; ".join(details))


def build_pages(manifest, assets):
    specs = ordered_specs(manifest)
    validate_manifest(specs)
    pages = []
    source_by_id = {}
    for spec in specs:
        path = MANUSCRIPT / spec["path"]
        source = path.read_text(encoding="utf-8")
        metadata, page_markdown = parse_frontmatter(source, path)
        heading, epigraph_markdown, body_markdown = split_page(page_markdown, path)
        page_id = metadata["id"]
        if page_id in source_by_id:
            raise SystemExit(f"duplicate page id: {page_id}")
        source_by_id[page_id] = source

        hero_id = extract_hero_id(metadata["hero"]) or HERO_FALLBACK.get(page_id)
        hero = asset_public(assets[hero_id]) if hero_id in assets else None
        pages.append({
            "id": page_id,
            "kicker": metadata["kicker"],
            "year": metadata["year"],
            "title": metadata["title"] or heading,
            "epigraph": render_epigraph(epigraph_markdown),
            "hero": hero,
            "body": render_body(body_markdown),
            "hidden": bool(spec.get("hidden")),
            "role": spec["role"],
            "book": spec["book"],
            "words": len(source.split()),
            "tagline": spec.get("tagline", ""),
        })
    return pages, source_by_id


def build_credits(assets):
    credits = []
    for asset in assets.values():
        credits.append({
            "id": asset["id"],
            "file": asset["file"],
            "alt": asset.get("alt", ""),
            "title": asset.get("title", ""),
            "caption": asset.get("caption", ""),
            "source_url": asset.get("source_url", ""),
            "source_note": asset.get("source_note", ""),
            "creator": asset.get("creator", ""),
            "date": asset.get("date", ""),
            "license": asset.get("license", "") or asset.get("usage_terms", ""),
        })
    return credits


def book_pages(book, pages):
    page_ids = {
        Path(spec["path"]).stem
        for spec in book["pages"]
        if not spec.get("hidden")
    }
    return [page for page in pages if page["id"] in page_ids]
