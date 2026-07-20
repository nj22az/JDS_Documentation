#!/usr/bin/env python3
"""Compile the ordered YAML manuscript into the React reading edition.

The manuscript and publishing-manifest.json are the source of truth. The build
emits the reader payload, SEO fallback, omnibus configuration, compiled Markdown,
and public image tree without relying on filename order.

Run from reader/:  python3 tools/build_content.py
"""

import json

from content_config import MANIFEST_PATH, NARRATIVE_ROLES, OUT_DATA
from content_outputs import (
    build_seo,
    copy_public_assets,
    write_compiled_markdown,
    write_omnibus_config,
)
from content_source import (
    asset_public,
    book_pages,
    build_credits,
    build_pages,
    load_assets,
    load_json,
    ordered_specs,
)


def main():
    manifest = load_json(MANIFEST_PATH)
    assets = load_assets()
    pages, source_by_id = build_pages(manifest, assets)
    publication = manifest["publication"]
    cover = assets.get(publication["cover_id"])
    payload = {
        "title": publication["title"],
        "subtitle": publication["subtitle"],
        "cover": asset_public(cover) if cover else None,
        "pages": pages,
        "credits": build_credits(assets),
    }

    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    copy_public_assets()
    write_omnibus_config(manifest, pages)
    write_compiled_markdown(ordered_specs(manifest), source_by_id)
    build_seo(manifest, pages)

    book_one = next(book for book in manifest["books"] if book["numeral"] == "I")
    book_one_words = sum(
        page["words"]
        for page in book_pages(book_one, pages)
        if page["role"] in NARRATIVE_ROLES
    )
    print(f"content.json: {len(pages)} pages, {len(payload['credits'])} credits")
    print(f"Book One: {book_one_words:,} words")


if __name__ == "__main__":
    main()
