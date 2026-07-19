#!/usr/bin/env python3
"""Inject canonical Markdown pages into the compiled Front-Row Seat reader.

The deployed reader currently carries its page records in a compiled JavaScript
bundle. This tool replaces a controlled set of page bodies while preserving the
application code, page order, hero metadata and epigraph metadata around them.
It is the inverse companion to ``extract_live_reader.py`` until the reader has a
first-class Markdown build pipeline.
"""

from __future__ import annotations

import argparse
import html
import re
import unicodedata
from pathlib import Path


PAGE_IDS = (
    "part-one-the-venture",
    "01-1603-the-boy-who-signed",
    "02-1603-dutch-courage",
    "03-1612-the-return",
    "02-1626-the-man-who-came-back-wrong",
    "04-1629-the-south-land",
    "05-1635-last-orders",
    "book-one-character-bible",
)

PAGE_PATTERN = re.compile(
    r'\{id:"([^"]+)",kicker:"([^"]+)",year:"([^"]*)",'
    r'title:"([^"]+)",epigraph:(?:""|`(.*?)`),'
    r'hero:(?:null|\{.*?\}),body:`(.*?)`\}',
    re.DOTALL,
)


def inline_markup(text: str) -> str:
    rendered = html.escape(text, quote=False)
    rendered = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{match.group(1)}</a>"
        ),
        rendered,
    )
    rendered = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", rendered)
    rendered = re.sub(r"\*(.+?)\*", r"<em>\1</em>", rendered)
    return rendered


def heading_id(text: str) -> str:
    plain = re.sub(r"[*_`]", "", html.unescape(text))
    plain = unicodedata.normalize("NFKD", plain).encode("ascii", "ignore").decode()
    plain = re.sub(r"['’]", "", plain.lower())
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


def markdown_body(source: str) -> str:
    source = re.sub(r"^---\r?\n[\s\S]*?\r?\n---\r?\n", "", source, count=1)
    source = re.sub(r"^#\s+.*?\r?\n", "", source, count=1).lstrip()

    # Narrative epigraphs are already stored separately in the reader object.
    # Strip only a leading blockquote and its following scene divider. Reference
    # pages have no leading blockquote, so their first divider remains in-body.
    if source.startswith(">"):
        parts = re.split(r"\r?\n\*{3}\r?\n", source, maxsplit=1)
        if len(parts) != 2:
            raise ValueError("Leading epigraph has no following scene divider")
        source = parts[1].lstrip()

    blocks = re.split(r"\r?\n\s*\r?\n", source.strip())
    rendered: list[str] = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue
        if block in {"***", "---"}:
            rendered.append('<hr class="scene">')
            continue

        heading = re.fullmatch(r"(#{2,5})\s+(.+)", block)
        if heading:
            level = len(heading.group(1))
            text = inline_markup(heading.group(2))
            rendered.append(f'<h{level} id="{heading_id(heading.group(2))}">{text}</h{level}>')
            continue

        image = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", block)
        if image:
            alt = html.escape(image.group(1), quote=True)
            src = html.escape(image.group(2), quote=True)
            rendered.append(f'<p><img src="{src}" alt="{alt}"></p>')
            continue

        if all(line.startswith(">") for line in block.splitlines()):
            quote = "\n".join(line.removeprefix(">").lstrip() for line in block.splitlines())
            rendered.append(f"<blockquote>\n<p>{inline_markup(quote)}</p>\n</blockquote>")
            continue

        paragraph = "\n".join(line.strip() for line in block.splitlines())
        rendered.append(f"<p>{inline_markup(paragraph)}</p>")

    return "\n".join(rendered)


def template_literal(markup: str) -> str:
    return markup.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def inject_page(bundle: str, page_id: str, body: str) -> str:
    pattern = re.compile(
        rf'(\{{id:"{re.escape(page_id)}",.*?,body:`)(.*?)(`\}})(?=,\{{id:|\])',
        re.DOTALL,
    )
    updated, count = pattern.subn(
        lambda match: match.group(1) + template_literal(body) + match.group(3),
        bundle,
        count=1,
    )
    if count != 1:
        raise RuntimeError(f"Expected exactly one reader object for {page_id}; found {count}")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()

    bundle = args.bundle.read_text(encoding="utf-8")
    original_ids = [match.group(1) for match in PAGE_PATTERN.finditer(bundle)]
    if not set(PAGE_IDS).issubset(original_ids):
        missing = sorted(set(PAGE_IDS).difference(original_ids))
        raise RuntimeError(f"Reader bundle is missing canonical Volume One pages: {missing}")

    for page_id in PAGE_IDS:
        source = args.source_dir / f"{page_id}.md"
        if not source.exists():
            raise FileNotFoundError(source)
        bundle = inject_page(bundle, page_id, markdown_body(source.read_text(encoding="utf-8")))

    updated_ids = [match.group(1) for match in PAGE_PATTERN.finditer(bundle)]
    if updated_ids != original_ids:
        raise RuntimeError("Reader page order or object structure changed during injection")

    args.bundle.write_text(bundle, encoding="utf-8")
    print(f"Injected {len(PAGE_IDS)} pages into {args.bundle}")


if __name__ == "__main__":
    main()
