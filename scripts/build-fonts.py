#!/usr/bin/env python3
"""Subset the rounded maru-gothic display font for JDS-PRJ-GEN-001.

M PLUS Rounded 1c (jds/assets/fonts/, SIL Open Font License) is a ~3.5 MB CJK
font per weight. The book only needs Latin letters, accents, punctuation and the
five box icons, so we subset each weight down to ~30 KB. That keeps the EPUB
small (no Amazon KDP delivery fee) while embedding the exact rounded look the
author wants — the free equivalent of HG Maru Gothic Pro.

Run once (or after changing the character set):
    python3 scripts/build-fonts.py
"""

from pathlib import Path

from fontTools.subset import Subsetter, Options
from fontTools.ttLib import TTFont

SOURCE_FONTS = Path("jds/assets/fonts")
OUTPUT_FONTS = Path("projects/JDS-PRJ-GEN-001/03-assets/fonts")

WEIGHTS = ["Regular", "Medium", "Bold"]

# The character ranges the book actually sets, plus the five box icons.
UNICODE_RANGES = [
    (0x0020, 0x007E),   # Basic Latin
    (0x00A0, 0x00FF),   # Latin-1 Supplement (å ä ö é ü …)
    (0x0100, 0x017F),   # Latin Extended-A (any stray accents)
    (0x2010, 0x2027),   # dashes, curly quotes, ellipsis, bullet
    (0x00D7, 0x00D7),   # × (e.g. "20 × 20 ft")
]
ICON_CODEPOINTS = [0x25B2, 0x25B6, 0x25CF, 0x25C6, 0x25C7]   # ▲ ▶ ● ◆ ◇


def wanted_codepoints():
    points = set(ICON_CODEPOINTS)
    for start, end in UNICODE_RANGES:
        points.update(range(start, end + 1))
    return points


def subset_weight(weight, points):
    src = SOURCE_FONTS / f"MPLUSRounded1c-{weight}.ttf"
    dst = OUTPUT_FONTS / f"MPLUSRounded1c-{weight}-subset.ttf"
    options = Options()
    options.set(layout_features="*", name_IDs="*", notdef_outline=True)
    font = TTFont(src)
    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=points)
    subsetter.subset(font)
    font.save(dst)
    return dst, dst.stat().st_size / 1024


def main():
    OUTPUT_FONTS.mkdir(parents=True, exist_ok=True)
    points = wanted_codepoints()
    print(f"Subsetting {len(WEIGHTS)} weights to {len(points)} code points:")
    for weight in WEIGHTS:
        dst, size_kb = subset_weight(weight, points)
        print(f"  {dst.name} — {size_kb:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
