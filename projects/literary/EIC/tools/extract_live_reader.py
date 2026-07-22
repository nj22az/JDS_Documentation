#!/usr/bin/env python3
"""Extract the deployed Front-Row Seat reader into editable Markdown.

The GitHub Pages repository currently stores the canonical edition inside the
compiled JavaScript bundle.  This tool recovers the ordered page objects without
modifying the deployed site, converts their controlled HTML subset to Markdown,
and writes both individual source files and a compiled comparison copy.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


# Page objects end either at the closing brace (original bundle) or at the
# metadata fields (hidden/role/book/words/tagline) added in later deployments.
PAGE_PATTERN = re.compile(
    r'\{id:"([^"]+)",kicker:"([^"]+)",year:"([^"]*)",'
    r'title:"([^"]+)",epigraph:(?:""|`(.*?)`),'
    r'hero:(?:null|\{.*?\}),body:`(.*?)`(?:\}|,hidden:)',
    re.DOTALL,
)


def _inline(markup: str) -> str:
    markup = re.sub(
        r'<a\s+[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
        lambda match: f"[{_inline(match.group(2))}]({match.group(1)})",
        markup,
        flags=re.DOTALL,
    )
    markup = re.sub(
        r'<strong>(.*?)</strong>',
        lambda match: f"**{_inline(match.group(1))}**",
        markup,
        flags=re.DOTALL,
    )
    markup = re.sub(
        r'<em>(.*?)</em>',
        lambda match: f"*{_inline(match.group(1))}*",
        markup,
        flags=re.DOTALL,
    )
    markup = re.sub(r'<br\s*/?>', "\n", markup, flags=re.IGNORECASE)
    markup = re.sub(r'<[^>]+>', "", markup)
    return html.unescape(re.sub(r"[ \t]+", " ", markup)).strip()


def _figure(match: re.Match[str]) -> str:
    attrs, inner = match.group(1), match.group(2)
    figure_id = re.search(r'id="([^"]+)"', attrs)
    image = re.search(
        r'<img\s+[^>]*src="([^"]+)"[^>]*alt="([^"]*)"[^>]*>',
        inner,
        flags=re.DOTALL,
    )
    caption = re.search(r'<figcaption>(.*?)</figcaption>', inner, flags=re.DOTALL)
    lines = []
    if figure_id:
        lines.append(f"<!-- figure: {figure_id.group(1)} -->")
    if image:
        lines.append(f"![{html.unescape(image.group(2))}]({image.group(1)})")
    if caption:
        caption_text = _inline(caption.group(1))
        caption_text = re.sub(r"\s*Credit\s*$", "", caption_text).strip()
        if caption_text:
            lines.append(f"*{caption_text}*")
    return "\n\n" + "\n\n".join(lines) + "\n\n"


def html_to_markdown(markup: str) -> str:
    markup = re.sub(
        r'<figure([^>]*)>(.*?)</figure>',
        _figure,
        markup,
        flags=re.DOTALL,
    )

    def blockquote(match: re.Match[str]) -> str:
        content = html_to_markdown(match.group(1)).strip()
        return "\n\n" + "\n".join(
            f"> {line}" if line else ">" for line in content.splitlines()
        ) + "\n\n"

    markup = re.sub(
        r'<blockquote>(.*?)</blockquote>',
        blockquote,
        markup,
        flags=re.DOTALL,
    )
    for level in (2, 3, 4):
        markup = re.sub(
            rf'<h{level}[^>]*>(.*?)</h{level}>',
            lambda match, level=level: (
                f"\n\n{'#' * level} {_inline(match.group(1))}\n\n"
            ),
            markup,
            flags=re.DOTALL,
        )
    markup = re.sub(
        r'<p[^>]*>(.*?)</p>',
        lambda match: f"\n\n{_inline(match.group(1))}\n\n",
        markup,
        flags=re.DOTALL,
    )
    markup = re.sub(r'<hr[^>]*>', "\n\n* * *\n\n", markup)
    markup = _inline(markup)
    markup = re.sub(r"\n[ \t]+", "\n", markup)
    markup = re.sub(r"[ \t]+\n", "\n", markup)
    markup = re.sub(r"\n{3,}", "\n\n", markup)
    return markup.strip() + "\n"


def page_heading(kicker: str, year: str, title: str) -> str:
    if kicker.startswith("Part"):
        return f"# {kicker}: {title}"
    if year:
        return f"# {year}: {title}"
    return f"# {title}"


def extract_pages(bundle: Path) -> list[dict[str, str]]:
    source = bundle.read_text(encoding="utf-8")
    pages = []
    for match in PAGE_PATTERN.finditer(source):
        page_id, kicker, year, title, epigraph, body = match.groups()
        pages.append(
            {
                "id": page_id,
                "kicker": kicker,
                "year": year,
                "title": title,
                "epigraph": epigraph or "",
                "body": body,
            }
        )
    page_ids = [page["id"] for page in pages]
    if len(pages) < 25:
        raise RuntimeError(f"Expected at least 25 reader pages; extracted {len(pages)}")
    if len(page_ids) != len(set(page_ids)):
        raise RuntimeError("Reader bundle contains duplicate page identifiers")
    return pages


def render_page(page: dict[str, str], source_commit: str) -> str:
    pieces = [
        f"<!-- live-canon-source: nj22az/nj22az.github.io@{source_commit} -->",
        "<!-- imported for editorial comparison; deployed reader remains unchanged -->",
        "",
        page_heading(page["kicker"], page["year"], page["title"]),
        "",
    ]
    if page["epigraph"]:
        pieces.extend([html_to_markdown(page["epigraph"]).strip(), ""])
    pieces.append(html_to_markdown(page["body"]).strip())
    return "\n".join(pieces).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("combined", type=Path)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()

    pages = extract_pages(args.bundle)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    args.combined.parent.mkdir(parents=True, exist_ok=True)

    compiled = []
    for page in pages:
        rendered = render_page(page, args.source_commit)
        destination = args.output_dir / f'{page["id"]}.md'
        destination.write_text(rendered, encoding="utf-8")
        compiled.append(rendered)

    args.combined.write_text("\n---\n\n".join(compiled), encoding="utf-8")
    words = sum(
        len(re.findall(r"\b[\w’'-]+\b", html_to_markdown(page["body"])))
        for page in pages
    )
    print(f"Extracted {len(pages)} pages and approximately {words:,} body words")


if __name__ == "__main__":
    main()
