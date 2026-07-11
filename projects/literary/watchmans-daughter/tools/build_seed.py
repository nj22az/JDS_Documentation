#!/usr/bin/env python3
"""Split the canonical 1888 chapter into provenance-marked seed units."""

from __future__ import annotations

import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "source-canon/12-1888-the-watchmans-daughter.md"
OUTPUT = PROJECT / "manuscript-seed"


def filename(index: int, heading: str) -> str:
    title = re.sub(r"^[IVXLCDM]+\.\s*", "", heading)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{index:02d}-{slug}.md"


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    first_section = re.search(r"^##\s+", source, flags=re.MULTILINE)
    if not first_section:
        raise RuntimeError("The canonical chapter contains no section headings")

    opening = source[: first_section.start()].rstrip() + "\n"
    (OUTPUT / "00-title-and-epigraph.md").write_text(
        "<!-- standalone-seed: copied from the protected live canon -->\n"
        "<!-- do not edit; create revised prose in manuscript-draft/ -->\n\n"
        + opening,
        encoding="utf-8",
    )

    sections = re.split(r"(?=^##\s+)", source[first_section.start() :], flags=re.MULTILINE)
    sections = [section for section in sections if section.strip()]
    if len(sections) != 13:
        raise RuntimeError(f"Expected 13 sections; found {len(sections)}")

    for index, section in enumerate(sections, start=1):
        match = re.match(r"^##\s+(.+)$", section, flags=re.MULTILINE)
        if not match:
            raise RuntimeError(f"Section {index} has no heading")
        destination = OUTPUT / filename(index, match.group(1))
        destination.write_text(
            "<!-- standalone-seed: copied verbatim from 1888 live canon -->\n"
            "<!-- do not edit; create revised prose in manuscript-draft/ -->\n\n"
            + section.rstrip()
            + "\n",
            encoding="utf-8",
        )

    print(f"Built {len(sections)} seed sections plus title and epigraph")


if __name__ == "__main__":
    main()
