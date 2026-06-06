#!/usr/bin/env python3
"""Book chapter consistency checker for 'The Garage Reset' / 'Städa i Garaget'
(JDS-PRJ-GEN-001).

Mechanically verifies a chapter draft against the manuscript style guide
(JDS-MAN-GEN-002 §8). Self-correcting backbone for the /write-chapter skill:
draft a chapter, run this, fix what it flags, repeat.

The book is written English-first (master) with a Swedish edition. Pass --lang to
choose which edition to check; English is the default.

Usage:
    python3 scripts/book-check.py --all                 # check English chapters (default)
    python3 scripts/book-check.py --all --lang sv        # check Swedish chapters
    python3 scripts/book-check.py <chapter.md>           # check one chapter
"""

import re
import sys
from pathlib import Path

# --- Configuration (JDS-PRO-004 §3: no magic values in logic) ------------------

MANUSCRIPT = Path("projects/JDS-PRJ-GEN-001/02-manuscript")

MIN_WORDS = 1200
MAX_WORDS = 2200
MAX_HEADING_DEPTH = 3  # H3

# Homograph guard: Cyrillic/Greek letters that look identical to Latin ones must
# never appear (style guide §9). Language-agnostic.
HOMOGRAPH_RANGES = [(0x0400, 0x04FF), (0x0370, 0x03FF)]  # Cyrillic, Greek

# Brand-neutral rule (style guide §4): flag obvious manufacturer names. Shared.
BRAND_BLOCKLIST = ["IKEA", "Biltema", "Jula", "Clas Ohlson", "Bauhaus", "Elfa",
                   "Hornbach", "Home Depot", "Lowe's", "Costco"]

# Per-edition rules. The five method words are a FIXED brand vocabulary (§3).
LANG_CONFIG = {
    "en": {
        "chapters_dir": MANUSCRIPT / "en" / "chapters",
        "glob": "chapter-*.md",
        "method_words": ["Sort", "Set in Order", "Shine", "Standardize", "Sustain"],
        "misspellings": ["Set In order", "Standardise"],  # keep US spelling
        "required_sections": ["## The problem", "## Takeaways"],
        "required_box": "Weekend Project",
        "safety_triggers": ["petrol", "gasoline", "solvent", "chemical",
                            "flammable", "battery", "lift"],
        "safety_box": "Safety",
    },
    "sv": {
        "chapters_dir": MANUSCRIPT / "sv" / "chapters",
        "glob": "kapitel-*.md",
        "method_words": ["Sortera", "Systematisera", "Städa", "Standardisera", "Säkra"],
        "misspellings": ["Standarisera", "Systemarisera", "Sytematisera", "Sakra"],
        "required_sections": ["## Problemet", "## Att ta med sig"],
        "required_box": "Helgprojektet",
        "safety_triggers": ["bensin", "lösningsmedel", "kemikal", "brandfarl",
                            "batteri", "ström", "lyft"],
        "safety_box": "Säkerhet",
    },
}


def count_words(text):
    """Count words in prose, ignoring HTML comment lines."""
    prose = "\n".join(line for line in text.splitlines()
                      if not line.strip().startswith("<!--"))
    return len(re.findall(r"\b\w+\b", prose))


def check_chapter(path, cfg):
    """Return (errors, warnings) for a single chapter file under config cfg."""
    errors = []
    warnings = []
    text = path.read_text(encoding="utf-8")

    # 1. Exactly one H1.
    h1_count = len(re.findall(r"^# ", text, re.MULTILINE))
    if h1_count != 1:
        errors.append(f"expected exactly one H1, found {h1_count}")

    # 2. No heading deeper than H3.
    if re.search(r"^#{4,}\s", text, re.MULTILINE):
        errors.append(f"heading deeper than H{MAX_HEADING_DEPTH}")

    # 3. Word count in range.
    words = count_words(text)
    if words < MIN_WORDS:
        warnings.append(f"short: {words} words (min {MIN_WORDS})")
    elif words > MAX_WORDS:
        warnings.append(f"long: {words} words (max {MAX_WORDS})")

    # 4. Required sections present.
    for section in cfg["required_sections"]:
        if section not in text:
            warnings.append(f"missing section '{section}'")

    # 5. At least one weekend-project box.
    if cfg["required_box"] not in text:
        warnings.append(f"missing '{cfg['required_box']}' box")

    # 6. At least one method word used, and no misspellings.
    if not any(word in text for word in cfg["method_words"]):
        warnings.append("no method word referenced")
    for bad in cfg["misspellings"]:
        if bad in text:
            errors.append(f"misspelled/forbidden method spelling '{bad}'")

    # 7. Brand-neutral.
    for brand in BRAND_BLOCKLIST:
        if re.search(rf"\b{re.escape(brand)}\b", text):
            warnings.append(f"brand name '{brand}' — keep brand-neutral (§4)")

    # 8. Safety trigger without a Safety box.
    lower = text.lower()
    if any(t in lower for t in cfg["safety_triggers"]) and cfg["safety_box"] not in text:
        warnings.append(f"safety topic present but no '{cfg['safety_box']}' box (§8)")

    # 9. Homograph guard.
    for line_no, line in enumerate(text.splitlines(), 1):
        if any(any(lo <= ord(ch) <= hi for lo, hi in HOMOGRAPH_RANGES) for ch in line):
            errors.append(f"non-Latin homograph on line {line_no}")
            break

    return errors, warnings


def main():
    args = sys.argv[1:]
    lang = "en"
    if "--lang" in args:
        lang = args[args.index("--lang") + 1]
    cfg = LANG_CONFIG[lang]

    if "--all" in args:
        targets = sorted(cfg["chapters_dir"].glob(cfg["glob"]))
    else:
        targets = [Path(a) for a in args if not a.startswith("--")
                   and a not in LANG_CONFIG]
    if not targets:
        print("usage: book-check.py [--all] [--lang en|sv] [<chapter.md>]")
        return 1

    total_errors = 0
    print(f"Book Chapter Check [{lang}] — JDS-MAN-GEN-002 §8")
    print("=" * 60)
    for path in targets:
        if not path.exists():
            print(f"  ✗ {path} — file not found")
            total_errors += 1
            continue
        errors, warnings = check_chapter(path, cfg)
        print(f"\n[{'PASS' if not errors else 'FAIL'}] {path.name}")
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
