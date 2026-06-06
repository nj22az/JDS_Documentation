#!/usr/bin/env python3
"""Generate the KDP eBook cover for JDS-PRJ-GEN-001.

English-first ('The Garage Reset', cover-en.jpg) with a Swedish edition
('Städa i Garaget', cover.jpg). Produces a 1600x2560 RGB JPEG (KDP's recommended
eBook cover size and 1.6:1 ratio), bold and thumbnail-legible, with a
pegboard-and-tools motif in the JDS navy + amber palette.

Usage:
    python3 scripts/build-cover.py                # English cover (default)
    python3 scripts/build-cover.py --lang sv       # Swedish cover
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

PRODUCTION = Path("projects/JDS-PRJ-GEN-001/04-production")

WIDTH, HEIGHT = 1600, 2560
MARGIN = 120

NAVY = (19, 49, 79)
NAVY_LIGHT = (32, 68, 104)
DOT = (45, 86, 126)
AMBER = (232, 163, 61)
CREAM = (244, 241, 235)
MUTED = (180, 198, 214)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

LANG_CONFIG = {
    "en": {
        "title1": "THE GARAGE",
        "title2": "RESET",
        "subtitle": "Declutter, organize, and keep order\nin your garage and workshop",
        "kicker": "A 10-STEP PROGRAM FOR AN ORDERLY GARAGE",
        "author": "NILS JOHANSSON",
        "output": PRODUCTION / "cover-en.jpg",
    },
    "sv": {
        "title1": "STÄDA I",
        "title2": "GARAGET",
        "subtitle": "Rensa, organisera och håll ordning\ni verkstad och förråd",
        "kicker": "ETT 10-STEGSPROGRAM FÖR ETT GARAGE I ORDNING",
        "author": "NILS JOHANSSON",
        "output": PRODUCTION / "cover.jpg",
    },
}


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, fnt, y, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text(((WIDTH - w) / 2, y), text, font=fnt, fill=fill)


def draw_pegboard(draw, top, bottom):
    draw.rectangle([0, top, WIDTH, bottom], fill=NAVY_LIGHT)
    step, radius = 70, 7
    for y in range(top + step, bottom - step + 1, step):
        for x in range(step, WIDTH - step + 1, step):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=DOT)


def draw_hammer(draw, cx, top):
    draw.rectangle([cx - 120, top, cx + 120, top + 70], fill=AMBER)
    draw.rectangle([cx - 95, top, cx - 45, top + 55], fill=NAVY_LIGHT)
    draw.rounded_rectangle([cx - 26, top + 60, cx + 26, top + 360], radius=26, fill=AMBER)


def draw_wrench(draw, cx, top):
    draw.rounded_rectangle([cx - 30, top + 70, cx + 30, top + 360], radius=30, fill=AMBER)
    draw.ellipse([cx - 80, top, cx + 80, top + 160], fill=AMBER)
    draw.ellipse([cx - 38, top + 42, cx + 38, top + 118], fill=NAVY_LIGHT)
    draw.ellipse([cx - 78, top + 300, cx + 78, top + 420], fill=AMBER)
    draw.ellipse([cx - 34, top + 330, cx + 34, top + 390], fill=NAVY_LIGHT)


def draw_screwdriver(draw, cx, top):
    draw.rounded_rectangle([cx - 38, top, cx + 38, top + 180], radius=30, fill=AMBER)
    draw.rectangle([cx - 14, top + 175, cx + 14, top + 360], fill=AMBER)
    draw.polygon([(cx - 14, top + 360), (cx + 14, top + 360),
                  (cx + 6, top + 400), (cx - 6, top + 400)], fill=AMBER)


def build(cfg):
    img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(img)

    panel_bottom = 1120
    draw_pegboard(draw, 0, panel_bottom)
    draw.rectangle([0, panel_bottom, WIDTH, panel_bottom + 16], fill=AMBER)
    draw_hammer(draw, 430, 360)
    draw_wrench(draw, 800, 320)
    draw_screwdriver(draw, 1170, 360)

    centered(draw, cfg["kicker"], font(FONT_BOLD, 34), 1230, AMBER)
    centered(draw, cfg["title1"], font(FONT_BOLD, 190), 1330, CREAM)
    centered(draw, cfg["title2"], font(FONT_BOLD, 190), 1560, CREAM)
    draw.rectangle([MARGIN, 1820, WIDTH - MARGIN, 1828], fill=AMBER)

    y = 1900
    for line in cfg["subtitle"].split("\n"):
        centered(draw, line, font(FONT_REG, 52), y, MUTED)
        y += 70

    centered(draw, cfg["author"], font(FONT_BOLD, 64), HEIGHT - 260, CREAM)

    cfg["output"].parent.mkdir(parents=True, exist_ok=True)
    img.save(cfg["output"], "JPEG", quality=92)
    return cfg["output"]


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    path = build(LANG_CONFIG[lang])
    kb = path.stat().st_size / 1024
    print(f"Built {path} [{lang}] — {WIDTH}x{HEIGHT}, {kb:.0f} KB")


if __name__ == "__main__":
    main()
