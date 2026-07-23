#!/usr/bin/env python3
"""Consolidate Book One's 23 reader units into 13 per the chapter-merge plan.

Removes the 10 retired page objects, updates the 9 merge-anchor pages'
kicker/year/title/body/words, and renumbers the kicker on the 3 pages that
kept their own content but moved position. Run from the-front-row-seat/.
"""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "ilp",
    "/home/user/JDS_Documentation/projects/literary/EIC/tools/inject_live_reader_pages.py",
)
ilp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ilp)

MDIR = Path("/home/user/JDS_Documentation/projects/literary/EIC/manuscript-editorial")

RETIRED_IDS = [
    "02-1603-dutch-courage", "20-1603-the-stewards-search",
    "09-1612-the-teak-desk", "03-1612-the-return",
    "14-1614-the-pay-table", "22-1614-arthur-in-the-chair",
    "17-1622-the-echo", "10-1623-the-intersecting-web",
    "22-1623-the-coral-room", "18-1623-amboyna",
]

# anchor_id -> (source_file_stem, new_title, new_year)
MERGE_ANCHORS = {
    "01-1603-the-boy-who-signed": ("01-1603-the-boy-who-signed-merged", "The Boy Who Signed", "1603"),
    "06-1603-the-soot-and-the-roof": ("06-1603-what-the-women-did-merged", "What the Women Did", "1603"),
    "08-1604-the-language-of-paper": ("08-1604-marias-passage-east-merged", "Maria's Passage East", "1603–1612"),
    "21-1611-the-counter-ledger": ("21-1611-the-return-merged", "The Return", "1603–1612"),
    "11-1613-the-boy-in-the-rigging": ("11-1613-the-pay-table-merged", "The Pay Table", "1603–1614"),
    "15-1620-the-lone-machine": ("15-1620-tom-at-surat-merged", "Tom at Surat", "1614–1622"),
    "23-1622-news-from-the-sea": ("23-1622-the-years-between-merged", "The Years Between", "1614–1623"),
    "20-1621-the-factor": ("20-1621-amboyna-merged", "Amboyna", "1621–1623"),
    "19-1625-batavia": ("19-1625-batavia-merged", "Batavia", "1623–1626"),
}

# page_id -> new kicker text (all remaining Book One pages get renumbered)
NEW_KICKERS = {
    "01-1603-the-boy-who-signed": "Chapter One",
    "06-1603-the-soot-and-the-roof": "Chapter Two",
    "08-1604-the-language-of-paper": "Chapter Three",
    "21-1611-the-counter-ledger": "Chapter Four",
    "11-1613-the-boy-in-the-rigging": "Chapter Five",
    "15-1620-the-lone-machine": "Chapter Six",
    "23-1622-news-from-the-sea": "Chapter Seven",
    "20-1621-the-factor": "Chapter Eight",
    "24-1623-the-widows-years": "Chapter Nine",
    "19-1625-batavia": "Chapter Ten",
    "02-1626-the-man-who-came-back-wrong": "Chapter Eleven",
    "04-1629-the-south-land": "Chapter Twelve",
}


def clean_merged_body(raw: str) -> str:
    text = re.sub(r"^(?:<!--.*?-->\n)+\n?", "", raw, flags=re.DOTALL)
    text = re.sub(r"^#\s+.*?\n", "", text, count=1).lstrip("\n")
    if text.startswith(">"):
        lines = text.splitlines()
        cut = next(i for i, line in enumerate(lines) if not line.startswith(">"))
        text = "\n".join(lines[cut:]).lstrip("\n")
    text = re.split(r"\n##\s+Editorial notes", text, maxsplit=1)[0]
    text = re.sub(r"\n---\s*$", "", text)
    text = re.sub(r"^\* \* \*$", "***", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def words_of_html(markup: str) -> int:
    return len(re.sub(r"<[^>]+>", " ", markup).split())


def object_span(bundle: str, page_id: str) -> tuple[int, int]:
    """Return (start, end) of a page object, end exclusive of the following comma."""
    marker = '{id:"%s"' % page_id
    start = bundle.find(marker)
    if start < 0:
        raise RuntimeError(f"page id not found: {page_id}")
    next_obj = bundle.find(',{id:"', start + 1)
    if next_obj < 0:
        # last object in the array; end at the closing bracket of the array
        next_obj = bundle.find("]", start)
    return start, next_obj


def delete_page(bundle: str, page_id: str) -> str:
    marker = ',{id:"%s"' % page_id
    start = bundle.find(marker)
    if start < 0:
        raise RuntimeError(f"page id not found for deletion (or is first in array): {page_id}")
    end = bundle.find(',{id:"', start + 1)
    if end < 0:
        raise RuntimeError(f"could not find following object after: {page_id}")
    return bundle[:start] + bundle[end:]


def set_string_field(bundle: str, page_id: str, field: str, new_value: str) -> str:
    start, end = object_span(bundle, page_id)
    segment = bundle[start:end]
    pattern = re.compile(re.escape(field) + r':"([^"]*)"')
    new_segment, count = pattern.subn(
        lambda m: f'{field}:"{new_value}"', segment, count=1
    )
    if count != 1:
        raise RuntimeError(f"{page_id}: field {field} not found")
    return bundle[:start] + new_segment + bundle[end:]


def replace_body(bundle: str, page_id: str, new_html: str) -> tuple[str, int]:
    i = bundle.find('{id:"%s"' % page_id)
    b = bundle.find("body:`", i) + 6
    e = bundle.find("`,hidden:", b)
    old_words = words_of_html(bundle[b:e])
    return bundle[:b] + ilp.template_literal(new_html) + bundle[e:], old_words


def set_words(bundle: str, page_id: str, new_count: int) -> str:
    i = bundle.find('{id:"%s"' % page_id)
    j = bundle.find("`,hidden:", i)
    k = bundle.find(",words:", j)
    e = bundle.find(",", k + 7)
    return bundle[:k] + ",words:%d" % new_count + bundle[e:]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()

    bundle = args.bundle.read_text(encoding="utf-8")

    # 1. Remove the 10 retired page objects.
    for page_id in RETIRED_IDS:
        bundle = delete_page(bundle, page_id)
        print(f"deleted: {page_id}")

    # 2. Update the 9 merge-anchor pages: title, year, body, words.
    for anchor_id, (source_stem, new_title, new_year) in MERGE_ANCHORS.items():
        raw = (MDIR / f"{source_stem}.md").read_text(encoding="utf-8")
        body_markdown = clean_merged_body(raw)
        if "Editorial notes" in body_markdown:
            raise RuntimeError(f"{anchor_id}: scaffolding survived cleaning")
        body_html = ilp.markdown_body(body_markdown)
        bundle = set_string_field(bundle, anchor_id, "title", new_title)
        bundle = set_string_field(bundle, anchor_id, "year", new_year)
        bundle, old_words = replace_body(bundle, anchor_id, body_html)
        new_words = words_of_html(body_html)
        bundle = set_words(bundle, anchor_id, new_words)
        print(f"updated: {anchor_id} -> \"{new_title}\" ({new_year}), {old_words} -> {new_words} words")

    # 3. Renumber every remaining Book One kicker.
    for page_id, kicker in NEW_KICKERS.items():
        bundle = set_string_field(bundle, page_id, "kicker", kicker)
        print(f"kicker: {page_id} -> {kicker}")

    args.bundle.write_text(bundle, encoding="utf-8")
    print(f"\nDone. {len(RETIRED_IDS)} pages removed, {len(MERGE_ANCHORS)} anchors updated.")


if __name__ == "__main__":
    main()
