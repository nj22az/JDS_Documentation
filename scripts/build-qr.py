#!/usr/bin/env python3
"""Generate QR codes that link to the printable templates for JDS-PRJ-GEN-001.

Each QR points at a download URL for one printable (and one "all downloads" hub).
The base URL is a placeholder the author replaces with the real hosting location,
then re-runs this and `build-epub.py`.

Usage:
    python3 scripts/build-qr.py                 # English QR set
    python3 scripts/build-qr.py --lang sv        # Swedish QR set
"""

import sys
from pathlib import Path

import segno

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------
# Replace these with your real download page before publishing, then re-run.

BASE_URL = {
    "en": "https://thegaragereset.com/print",
    "sv": "https://stadaigaraget.se/skriv-ut",
}

OUT = Path("projects/JDS-PRJ-GEN-001/03-assets/images/qr")

SLUGS = ["inventory", "lifetime", "hazmat", "zone", "seasonal", "program",
         "fireround", "safetyround"]


def make(url, path):
    segno.make(url, error="m").save(str(path), scale=8, border=2, dark="#13314f")


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    base = BASE_URL[lang]
    suffix = "" if lang == "en" else "-sv"
    out_dir = OUT
    out_dir.mkdir(parents=True, exist_ok=True)

    make(base, out_dir / f"qr-all{suffix}.png")
    print(f"Built {out_dir / f'qr-all{suffix}.png'} -> {base}")
    for slug in SLUGS:
        url = f"{base}/{slug}.pdf"
        path = out_dir / f"qr-{slug}{suffix}.png"
        make(url, path)
        print(f"Built {path} -> {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
