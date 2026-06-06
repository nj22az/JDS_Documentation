#!/usr/bin/env python3
"""Generate the KDP eBook cover for 'Städa i Garaget' (JDS-PRJ-GEN-001).

Produces a 1600x2560 RGB JPEG (Amazon KDP's recommended eBook cover size and
1.6:1 ratio). The design is a bold, thumbnail-legible typographic cover with a
pegboard-and-tools workshop motif, in the JDS navy + amber palette.

Usage:
    python3 scripts/build-cover.py            # write 04-production/cover.jpg
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Configuration (JDS-PRO-004 §3: no magic values in logic) ------------------

OUTPUT = Path("projects/JDS-PRJ-GEN-001/04-production/cover.jpg")

WIDTH, HEIGHT = 1600, 2560
MARGIN = 120

NAVY = (19, 49, 79)          # background
NAVY_LIGHT = (32, 68, 104)   # pegboard panel
DOT = (45, 86, 126)          # pegboard holes
AMBER = (232, 163, 61)       # accent / tools
CREAM = (244, 241, 235)      # title text
MUTED = (180, 198, 214)      # subtitle text

TITLE_LINE1 = "STÄDA I"
TITLE_LINE2 = "GARAGET"
SUBTITLE = "Rensa, organisera och håll ordning\ni verkstad och förråd"
KICKER = "DEN PROFFSIGA ORDNINGSMETODEN — HEM TILL DITT GARAGE"
AUTHOR = "NILS JOHANSSON"

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, fnt, y, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text(((WIDTH - w) / 2, y), text, font=fnt, fill=fill)


def draw_pegboard(draw, top, bottom):
    """Light panel with an evenly spaced grid of holes."""
    draw.rectangle([0, top, WIDTH, bottom], fill=NAVY_LIGHT)
    step = 70
    radius = 7
    for y in range(top + step, bottom - step + 1, step):
        for x in range(step, WIDTH - step + 1, step):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=DOT)


def draw_hammer(draw, cx, top):
    draw.rectangle([cx - 120, top, cx + 120, top + 70], fill=AMBER)          # head
    draw.rectangle([cx - 95, top, cx - 45, top + 55], fill=NAVY_LIGHT)       # claw gap
    draw.rounded_rectangle([cx - 26, top + 60, cx + 26, top + 360],
                           radius=26, fill=AMBER)                            # handle


def draw_wrench(draw, cx, top):
    draw.rounded_rectangle([cx - 30, top + 70, cx + 30, top + 360],
                           radius=30, fill=AMBER)                            # shaft
    draw.ellipse([cx - 80, top, cx + 80, top + 160], fill=AMBER)            # ring head
    draw.ellipse([cx - 38, top + 42, cx + 38, top + 118], fill=NAVY_LIGHT)  # ring hole
    draw.ellipse([cx - 78, top + 300, cx + 78, top + 420], fill=AMBER)      # box head
    draw.ellipse([cx - 34, top + 330, cx + 34, top + 390], fill=NAVY_LIGHT) # box hole


def draw_screwdriver(draw, cx, top):
    draw.rounded_rectangle([cx - 38, top, cx + 38, top + 180],
                           radius=30, fill=AMBER)                            # handle
    draw.rectangle([cx - 14, top + 175, cx + 14, top + 360], fill=AMBER)     # shaft
    draw.polygon([(cx - 14, top + 360), (cx + 14, top + 360),
                  (cx + 6, top + 400), (cx - 6, top + 400)], fill=AMBER)     # tip


def build():
    img = Image.new("RGB", (WIDTH, HEIGHT), NAVY)
    draw = ImageDraw.Draw(img)

    # Top motif: pegboard with three hung tools.
    panel_top, panel_bottom = 0, 1120
    draw_pegboard(draw, panel_top, panel_bottom)
    draw.rectangle([0, panel_bottom, WIDTH, panel_bottom + 16], fill=AMBER)  # rail
    draw_hammer(draw, 430, 360)
    draw_wrench(draw, 800, 320)
    draw_screwdriver(draw, 1170, 360)

    # Kicker line.
    centered(draw, KICKER, font(FONT_BOLD, 34), 1230, AMBER)

    # Title.
    centered(draw, TITLE_LINE1, font(FONT_BOLD, 200), 1330, CREAM)
    centered(draw, TITLE_LINE2, font(FONT_BOLD, 200), 1560, CREAM)

    # Accent rule.
    draw.rectangle([MARGIN, 1820, WIDTH - MARGIN, 1828], fill=AMBER)

    # Subtitle (two lines).
    sub_font = font(FONT_REG, 52)
    y = 1900
    for line in SUBTITLE.split("\n"):
        centered(draw, line, sub_font, y, MUTED)
        y += 70

    # Author.
    centered(draw, AUTHOR, font(FONT_BOLD, 64), HEIGHT - 260, CREAM)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, "JPEG", quality=92)
    return OUTPUT


if __name__ == "__main__":
    path = build()
    kb = path.stat().st_size / 1024
    print(f"Built {path} — {WIDTH}x{HEIGHT}, {kb:.0f} KB")
