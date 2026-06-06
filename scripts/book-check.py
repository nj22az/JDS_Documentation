#!/usr/bin/env python3
"""Book chapter consistency checker for the 'Städa i Garaget' project (JDS-PRJ-GEN-001).

Mechanically verifies a chapter draft against the manuscript style guide
(JDS-MAN-GEN-002 §8). This is the self-correcting backbone for the /write-chapter
skill: draft a chapter, run this, fix what it flags, repeat.

Usage:
    python3 scripts/book-check.py <chapter.md>            # check one chapter
    python3 scripts/book-check.py --all                   # check every chapter
"""

import re
import sys
from pathlib import Path

# --- Configuration (JDS-PRO-004 §3: no magic numbers in logic) -----------------

CHAPTERS_DIR = Path("projects/JDS-PRJ-GEN-001/02-manuscript/chapters")

# Word band for an illustrated, box-driven project-guide chapter in Swedish.
# Recalibrated from 1600-2600 to match the chosen format (style guide §9, 2026-06-05).
MIN_WORDS = 1200
MAX_WORDS = 2200
MAX_HEADING_DEPTH = 3  # H3

# The five method words are a FIXED brand vocabulary (style guide §3).
METHOD_WORDS = ["Sortera", "Systematisera", "Städa", "Standardisera", "Säkra"]

# Common misspellings that must never appear (style guide §3).
METHOD_MISSPELLINGS = ["Standarisera", "Systemarisera", "Sytematisera", "Sakra"]

# Required section headings and boxes (style guide §5, §6).
REQUIRED_SECTIONS = ["## Problemet", "## Att ta med sig"]
REQUIRED_BOX = "Helgprojektet"

# Box labels that, when present, must be spelled exactly (style guide §6).
KNOWN_BOXES = ["Helgprojektet", "Verkstadsregeln", "Säkerhet", "Ärvt & svårt"]

# Brand-neutral rule (style guide §4): flag obvious manufacturer names.
BRAND_BLOCKLIST = ["IKEA", "Biltema", "Jula", "Clas Ohlson", "Bauhaus", "Elfa", "Hornbach"]

# Safety triggers — if these appear, a Säkerhet box is expected (style guide §8).
SAFETY_TRIGGERS = ["bensin", "lösningsmedel", "kemikal", "brandfarl", "batteri", "ström", "lyft"]

# Homograph guard: Cyrillic/Greek letters that look identical to Latin ones must never
# appear in the Swedish text — they slip in via copy/paste and corrupt search and spelling
# while looking perfectly normal (style guide §9, added 2026-06-05).
HOMOGRAPH_RANGES = [(0x0400, 0x04FF), (0x0370, 0x03FF)]  # Cyrillic, Greek


def count_words(text):
    """Count words in prose, ignoring markdown comment lines and box labels."""
    prose = "\n".join(line for line in text.splitlines() if not line.strip().startswith("<!--"))
    return len(re.findall(r"\b\w+\b", prose))


def check_chapter(path):
    """Return (errors, warnings) for a single chapter file."""
    errors = []
    warnings = []
    text = path.read_text(encoding="utf-8")

    # 1. Exactly one H1.
    h1_count = len(re.findall(r"^# ", text, re.MULTILINE))
    if h1_count != 1:
        errors.append(f"expected exactly one H1, found {h1_count}")

    # 2. No heading deeper than H3.
    for match in re.finditer(r"^(#{4,})\s", text, re.MULTILINE):
        errors.append(f"heading deeper than H{MAX_HEADING_DEPTH}: '{match.group(1)}'")
        break

    # 3. Word count in range.
    words = count_words(text)
    if words < MIN_WORDS:
        warnings.append(f"short: {words} words (min {MIN_WORDS})")
    elif words > MAX_WORDS:
        warnings.append(f"long: {words} words (max {MAX_WORDS})")

    # 4. Required sections present.
    for section in REQUIRED_SECTIONS:
        if section not in text:
            warnings.append(f"missing section '{section}'")

    # 5. At least one weekend-project box.
    if REQUIRED_BOX not in text:
        warnings.append(f"missing '{REQUIRED_BOX}' box")

    # 6. At least one method word used, and no misspellings.
    if not any(word in text for word in METHOD_WORDS):
        warnings.append("no method word (Sortera/Systematisera/...) referenced")
    for bad in METHOD_MISSPELLINGS:
        if bad in text:
            errors.append(f"misspelled method word '{bad}'")

    # 7. Brand-neutral.
    for brand in BRAND_BLOCKLIST:
        if re.search(rf"\b{re.escape(brand)}\b", text):
            warnings.append(f"brand name '{brand}' — keep brand-neutral (style guide §4)")

    # 8. Safety trigger without a Säkerhet box.
    lower = text.lower()
    if any(trigger in lower for trigger in SAFETY_TRIGGERS) and "Säkerhet" not in text:
        warnings.append("safety topic present but no 'Säkerhet' box (style guide §8)")

    # 9. Homograph guard — no Cyrillic/Greek letters disguised as Latin.
    for line_no, line in enumerate(text.splitlines(), 1):
        for ch in line:
            if any(lo <= ord(ch) <= hi for lo, hi in HOMOGRAPH_RANGES):
                errors.append(f"non-Latin homograph '{ch}' (U+{ord(ch):04X}) on line {line_no}")
                break

    return errors, warnings


def gather_targets(args):
    if "--all" in args:
        return sorted(CHAPTERS_DIR.glob("kapitel-*.md"))
    return [Path(a) for a in args if not a.startswith("--")]


def main():
    targets = gather_targets(sys.argv[1:])
    if not targets:
        print("usage: book-check.py <chapter.md> | --all")
        return 1

    total_errors = 0
    print("Book Chapter Check — Städa i Garaget (JDS-MAN-GEN-002 §8)")
    print("=" * 60)
    for path in targets:
        if not path.exists():
            print(f"  ✗ {path} — file not found")
            total_errors += 1
            continue
        errors, warnings = check_chapter(path)
        status = "PASS" if not errors else "FAIL"
        print(f"\n[{status}] {path.name}")
        for error in errors:
            print(f"  ✗ ERROR:   {error}")
        for warning in warnings:
            print(f"  ⚠ WARNING: {warning}")
        if not errors and not warnings:
            print("  ✓ clean")
        total_errors += len(errors)

    print("\n" + "=" * 60)
    print(f"  {len(targets)} chapter(s) checked, {total_errors} error(s)")
    return 1 if total_errors else 0


if __name__ == "__main__":
    sys.exit(main())
