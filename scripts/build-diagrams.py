#!/usr/bin/env python3
"""Generate the B&W line-art diagrams for JDS-PRJ-GEN-001, per language.

Three print-ready grayscale diagrams used in the interior, the EPUB, and Amazon
A+ content. English (default) writes plain names (zone-map.png …); Swedish writes
-sv names (zone-map-sv.png …) with translated labels, so the primary Swedish
edition gets localized figures.

Usage:
    python3 scripts/build-diagrams.py                # English
    python3 scripts/build-diagrams.py --lang sv       # Swedish
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

OUTPUT_DIR = Path("projects/JDS-PRJ-GEN-001/03-assets/images")

INK = (20, 20, 20)
PAPER = (255, 255, 255)
SHADE = (215, 215, 215)
MID = (120, 120, 120)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TEXT = {
    "en": {
        "suffix": "",
        "zone_title": "THE FIVE-ZONE MAP", "door": "GARAGE DOOR", "bench": "bench",
        "z1": "1 · CAR ZONE", "z1s": "floor stays clear",
        "z2": "2 · TOOL ZONE", "z2s": "near the light",
        "z3a": "3 · GARDEN", "z3b": "ZONE", "z3s": "near the exit",
        "z4": "4 · SEASONAL ZONE", "z4s": "high shelves & ceiling — touched twice a year",
        "z5a": "5 · RECYCLING", "z5b": "ZONE", "z5s": "inside the door — out fast",
        "peg_title": "THE SHADOW BOARD",
        "peg_sub": "an outline behind every tool — you see at a glance what's missing",
        "hammer": "hammer", "wrench": "spanner", "missing1": "the empty outline asks",
        "missing2": "for its tool back",
        "steps_title": "THE 10-STEP PROGRAMME",
        "steps_sub": "one or two steps per weekend — about five weekends in all",
        "steps": ["Set the goal", "Empty it out", "Keep · lose · relocate",
                  "Handle the dangerous", "Draw the zone map", "Get it off the floor",
                  "Label everything", "Shine it", "Set the rules", "Sustain it"],
        "phases": ["PREP", "SORT", "SORT", "SORT", "SET IN ORDER", "SET IN ORDER",
                   "SET IN ORDER", "SHINE", "STANDARDISE", "SUSTAIN"],
        "ba_title": "BEFORE  →  AFTER",
        "ba_before": "BEFORE: the car lives outside",
        "ba_after": "AFTER: the car fits, the wall works",
    },
    "sv": {
        "suffix": "-sv",
        "zone_title": "FEM-ZONERS-KARTAN", "door": "GARAGEPORT", "bench": "bänk",
        "z1": "1 · BILZON", "z1s": "golvet hålls fritt",
        "z2": "2 · VERKTYGSZON", "z2s": "nära ljuset",
        "z3a": "3 · TRÄDGÅRDS-", "z3b": "ZON", "z3s": "nära utgången",
        "z4": "4 · SÄSONGSZON", "z4s": "höga hyllor & tak — två gånger om året",
        "z5a": "5 · ÅTERVINNINGS-", "z5b": "ZON", "z5s": "innanför porten — snabbt ut",
        "peg_title": "SKUGGTAVLAN",
        "peg_sub": "en kontur bakom varje verktyg — du ser direkt vad som saknas",
        "hammer": "hammare", "wrench": "skiftnyckel", "missing1": "den tomma konturen",
        "missing2": "ber om sitt verktyg",
        "steps_title": "10-STEGSPROGRAMMET",
        "steps_sub": "ett eller två steg per helg — ungefär fem helger",
        "steps": ["Sätt målet", "Töm ut", "Behåll · lämna · flytta",
                  "Ta hand om farligt", "Rita zonkartan", "Upp från golvet",
                  "Märk allt", "Städa rent", "Sätt reglerna", "Håll vid liv"],
        "phases": ["FÖRBERED", "SORTERA", "SORTERA", "SORTERA", "SYSTEMATISERA",
                   "SYSTEMATISERA", "SYSTEMATISERA", "STÄDA", "STANDARDISERA", "SÄKRA"],
        "ba_title": "FÖRE  →  EFTER",
        "ba_before": "FÖRE: bilen står ute",
        "ba_after": "EFTER: bilen får plats, väggen jobbar",
    },
}


def font(path, size):
    return ImageFont.truetype(path, size)


def text_centered(draw, text, fnt, cx, y, fill=INK):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def zone_map(t):
    width, height = 1800, 1400
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)
    left, top, right, bottom = 150, 150, 1650, 1150
    d.rectangle([left, top, right, bottom], outline=INK, width=8)
    door_left, door_right = 550, 1250
    d.rectangle([door_left - 4, bottom - 4, door_right + 4, bottom + 4], fill=PAPER)
    d.line([door_left, bottom, door_left + 90, bottom + 70], fill=INK, width=6)
    d.line([door_right, bottom, door_right - 90, bottom + 70], fill=INK, width=6)
    text_centered(d, t["door"], font(FONT_REG, 36), (door_left + door_right) / 2, bottom + 80, MID)
    label, sub = font(FONT_BOLD, 44), font(FONT_REG, 32)
    d.rectangle([560, 420, 1240, 1130], outline=MID, width=4)
    d.rounded_rectangle([700, 560, 1100, 1040], radius=70, outline=INK, width=7)
    for cx in (795, 1005):
        for cy in (610, 990):
            d.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], outline=INK, width=7)
    text_centered(d, t["z1"], label, 900, 440)
    text_centered(d, t["z1s"], sub, 900, 495, MID)
    d.rectangle([left + 8, top + 8, 540, 760], fill=SHADE)
    d.rectangle([left + 30, 300, 380, 420], outline=INK, width=6)
    text_centered(d, t["bench"], sub, 270, 340, MID)
    text_centered(d, t["z2"], label, 345, 190)
    text_centered(d, t["z2s"], sub, 345, 245, MID)
    d.rectangle([1260, 520, right - 8, bottom - 8], fill=SHADE)
    text_centered(d, t["z3a"], label, 1455, 560)
    text_centered(d, t["z3b"], label, 1455, 615)
    text_centered(d, t["z3s"], sub, 1455, 675, MID)
    d.rectangle([560, top + 8, 1240, 400], fill=SHADE)
    text_centered(d, t["z4"], label, 900, 220)
    text_centered(d, t["z4s"], sub, 900, 280, MID)
    d.rectangle([left + 8, 780, 540, bottom - 8], fill=SHADE)
    text_centered(d, t["z5a"], label, 345, 880)
    text_centered(d, t["z5b"], label, 345, 935)
    text_centered(d, t["z5s"], sub, 345, 995, MID)
    text_centered(d, t["zone_title"], font(FONT_BOLD, 56), width / 2, 40)
    img.save(OUTPUT_DIR / f"zone-map{t['suffix']}.png")


def pegboard(t):
    width, height = 1800, 1200
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)
    left, top, right, bottom = 150, 180, 1650, 1000
    d.rectangle([left, top, right, bottom], outline=INK, width=8)
    for y in range(top + 60, bottom - 30, 70):
        for x in range(left + 60, right - 30, 70):
            d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=MID, width=3)

    def hammer(cx, cy, present):
        col, wdt = (INK, 7) if present else (MID, 5)
        d.rectangle([cx - 95, cy, cx + 95, cy + 55], outline=col, width=wdt)
        d.rounded_rectangle([cx - 20, cy + 55, cx + 20, cy + 290], radius=20, outline=col, width=wdt)

    def wrench(cx, cy, present):
        col, wdt = (INK, 7) if present else (MID, 5)
        d.ellipse([cx - 60, cy, cx + 60, cy + 120], outline=col, width=wdt)
        d.rounded_rectangle([cx - 22, cy + 110, cx + 22, cy + 300], radius=22, outline=col, width=wdt)

    def screwdriver(cx, cy, present):
        col, wdt = (INK, 7) if present else (MID, 5)
        d.rounded_rectangle([cx - 30, cy, cx + 30, cy + 130], radius=24, outline=col, width=wdt)
        d.line([cx, cy + 130, cx, cy + 300], fill=col, width=wdt + 4)

    hammer(450, 330, True)
    wrench(900, 320, True)
    screwdriver(1350, 330, False)
    lab = font(FONT_REG, 34)
    text_centered(d, t["hammer"], lab, 450, 660, MID)
    text_centered(d, t["wrench"], lab, 900, 660, MID)
    text_centered(d, "?", font(FONT_BOLD, 64), 1350, 470, MID)
    text_centered(d, t["missing1"], lab, 1350, 660, MID)
    text_centered(d, t["missing2"], lab, 1350, 705, MID)
    text_centered(d, t["peg_title"], font(FONT_BOLD, 56), width / 2, 40)
    text_centered(d, t["peg_sub"], font(FONT_REG, 38), width / 2, 110, MID)
    img.save(OUTPUT_DIR / f"pegboard{t['suffix']}.png")


def ten_steps(t):
    width, height = 1800, 1500
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)
    col_x, row_y = (480, 1320), [260 + i * 240 for i in range(5)]
    num_f, step_f, phase_f = font(FONT_BOLD, 52), font(FONT_BOLD, 40), font(FONT_REG, 30)
    centers = [(col_x[i % 2], row_y[i // 2]) for i in range(10)]
    for a, b in zip(centers, centers[1:]):
        d.line([a, b], fill=SHADE, width=14)
    for i, (cx, cy) in enumerate(centers):
        d.ellipse([cx - 64, cy - 64, cx + 64, cy + 64], fill=PAPER, outline=INK, width=8)
        text_centered(d, str(i + 1), num_f, cx, cy - 34)
        text_centered(d, t["steps"][i], step_f, cx, cy + 84)
        text_centered(d, t["phases"][i], phase_f, cx, cy + 136, MID)
    text_centered(d, t["steps_title"], font(FONT_BOLD, 60), width / 2, 50)
    text_centered(d, t["steps_sub"], font(FONT_REG, 40), width / 2, 130, MID)
    img.save(OUTPUT_DIR / f"ten-steps{t['suffix']}.png")


def before_after(t):
    width, height = 1800, 1240
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)
    title_f, lab_f = font(FONT_BOLD, 56), font(FONT_REG, 30)
    text_centered(d, t["ba_title"], title_f, width / 2, 36, INK)

    def garage(x0):
        left, top, right, bottom = x0 + 40, 150, x0 + 760, 880
        d.rectangle([left, top, right, bottom], outline=INK, width=8)
        return left, top, right, bottom

    # BEFORE: clutter on the floor, car outside.
    left, top, right, bottom = garage(0)
    import random
    random.seed(7)
    for _ in range(48):
        x = random.randint(left + 30, right - 90)
        y = random.randint(bottom - 320, bottom - 30)
        w = random.randint(35, 95)
        d.rectangle([x, y, x + w, y + random.randint(25, 70)], outline=MID, width=4)
    # car shape stranded outside, below the garage
    cy = bottom + 70
    d.rounded_rectangle([left + 180, cy, left + 560, cy + 110], radius=34, outline=INK, width=6)
    d.ellipse([left + 230, cy + 80, left + 290, cy + 140], outline=INK, width=6)
    d.ellipse([left + 450, cy + 80, left + 510, cy + 140], outline=INK, width=6)
    text_centered(d, t["ba_before"], lab_f, (left + right) / 2, 1170, MID)

    # AFTER: pegboard wall, clear floor, car inside.
    left, top, right, bottom = garage(900)
    for yy in range(top + 50, top + 230, 46):
        for xx in range(left + 50, right - 30, 46):
            d.ellipse([xx - 5, yy - 5, xx + 5, yy + 5], outline=MID, width=3)
    d.rounded_rectangle([left + 90, top + 70, left + 130, top + 250], radius=16, outline=INK, width=5)
    d.rectangle([left + 200, top + 70, left + 320, top + 120], outline=INK, width=5)
    d.line([left + 400, top + 70, left + 400, top + 250], fill=INK, width=7)
    cy2 = bottom - 230
    d.rounded_rectangle([left + 170, cy2, left + 560, cy2 + 150], radius=44, outline=INK, width=7)
    d.ellipse([left + 220, cy2 + 110, left + 300, cy2 + 190], outline=INK, width=7)
    d.ellipse([left + 440, cy2 + 110, left + 520, cy2 + 190], outline=INK, width=7)
    text_centered(d, t["ba_after"], lab_f, (left + right) / 2, 1170, MID)

    # arrow between panels
    d.line([840, 520, 920, 520], fill=INK, width=10)
    d.polygon([(920, 500), (960, 520), (920, 540)], fill=INK)
    img.save(OUTPUT_DIR / f"before-after{t['suffix']}.png")


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    t = TEXT[lang]
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    zone_map(t)
    pegboard(t)
    ten_steps(t)
    before_after(t)
    for stem in ("zone-map", "pegboard", "ten-steps", "before-after"):
        path = OUTPUT_DIR / f"{stem}{t['suffix']}.png"
        print(f"Built {path} [{lang}] — {Image.open(path).size}")


if __name__ == "__main__":
    main()
