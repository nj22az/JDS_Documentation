#!/usr/bin/env python3
"""Deploy the narrator-prolepsis present-tense rewrite to the reader bundle.

Reads every ``<page-id>-present-tense.md`` proposal in ``manuscript-editorial/``,
strips the review scaffolding (leading HTML comment, epigraph, trailing
Editorial notes section) down to pure body markdown, converts it with
``inject_live_reader_pages.markdown_body``, and replaces the matching page's
body in a working copy of the compiled bundle. Word counts are recomputed and
written back next to each body. Run from the-front-row-seat/ directory.
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

PROPOSAL_DIR = Path(
    "/home/user/JDS_Documentation/projects/literary/EIC/manuscript-editorial"
)
SUFFIX = "-present-tense.md"


def clean_proposal_body(raw: str) -> str:
    """Strip header comment, H1 title, epigraph blockquote and trailing notes."""
    text = re.sub(r"^(?:<!--.*?-->\n)+\n?", "", raw, flags=re.DOTALL)
    text = re.sub(r"^#\s+.*?\n", "", text, count=1)
    text = text.lstrip("\n")
    if text.startswith(">"):
        lines = text.splitlines()
        cut = next(i for i, line in enumerate(lines) if not line.startswith(">"))
        text = "\n".join(lines[cut:]).lstrip("\n")
    text = re.split(r"\n##\s+Editorial notes", text, maxsplit=1)[0]
    text = re.sub(r"\n---\s*$", "", text)
    # Scene dividers are written "* * *" for readability; markdown_body()
    # only recognizes the unspaced "***" form.
    text = re.sub(r"^\* \* \*$", "***", text, flags=re.MULTILINE)
    return text.strip() + "\n"


def words_of_html(markup: str) -> int:
    return len(re.sub(r"<[^>]+>", " ", markup).split())


def replace_body(bundle: str, page_id: str, new_html: str) -> tuple[str, int]:
    i = bundle.find('{id:"%s"' % page_id)
    if i < 0:
        raise RuntimeError(f"page id not found in bundle: {page_id}")
    b = bundle.find("body:`", i) + 6
    e = bundle.find("`,hidden:", b)
    if e < 0:
        raise RuntimeError(f"body terminator not found for: {page_id}")
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
    proposals = sorted(PROPOSAL_DIR.glob(f"*{SUFFIX}"))
    if not proposals:
        raise RuntimeError(f"No proposal files found in {PROPOSAL_DIR}")

    deltas: dict[str, int] = {}
    for path in proposals:
        page_id = path.name[: -len(SUFFIX)]
        raw = path.read_text(encoding="utf-8")
        body_markdown = clean_proposal_body(raw)
        if "Editorial notes" in body_markdown:
            raise RuntimeError(f"{page_id}: scaffolding survived cleaning")
        body_html = ilp.markdown_body(body_markdown)
        bundle, old_words = replace_body(bundle, page_id, body_html)
        new_words = words_of_html(body_html)
        bundle = set_words(bundle, page_id, new_words)
        deltas[page_id] = new_words - old_words
        print(f"{page_id}: {old_words} -> {new_words} words ({deltas[page_id]:+d})")

    args.bundle.write_text(bundle, encoding="utf-8")
    print(f"\nInjected {len(proposals)} chapters into {args.bundle}")

    deltas_path = args.bundle.parent.parent / "present_tense_word_deltas.txt"
    with deltas_path.open("w", encoding="utf-8") as fh:
        for page_id, delta in deltas.items():
            fh.write(f"{page_id} {delta}\n")
    print(f"Word deltas written to {deltas_path}")


if __name__ == "__main__":
    main()
