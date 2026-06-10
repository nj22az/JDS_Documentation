#!/usr/bin/env python3
"""Generate the B&W line-art diagrams for The Garage Reset (JDS-PRJ-GEN-001).

Produces three print-ready diagrams (grayscale, 300 DPI class) used in the
paperback interior, the EPUB, and the Amazon A+ content:

  zone-map.png        - the five-zone garage map (chapter 6)
  pegboard.png        - shadow-board pegboard with outlines (chapter 8)
  ten-steps.png       - the 10-step program as a road strip (front matter)

Black ink only: KDP's B&W interior is the cheap one, so the diagrams are pure
grayscale line art by design.

Usage:
    python3 scripts/build-diagrams.py
"""

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


def font(path, size):
    return ImageFont.truetype(path, size)


def text_centered(draw, text, fnt, cx, y, fill=INK):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


# --- Diagram 1: the five-zone map ----------------------------------------------

def zone_map():
    width, height = 1800, 1400
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)

    # Garage outline with a door opening at the bottom.
    left, top, right, bottom = 150, 150, 1650, 1150
    d.rectangle([left, top, right, bottom], outline=INK, width=8)
    door_left, door_right = 550, 1250
    d.rectangle([door_left - 4, bottom - 4, door_right + 4, bottom + 4], fill=PAPER)
    d.line([door_left, bottom, door_left + 90, bottom + 70], fill=INK, width=6)
    d.line([door_right, bottom, door_right - 90, bottom + 70], fill=INK, width=6)
    text_centered(d, "GARAGE DOOR", font(FONT_REG, 36), (door_left + door_right) / 2,
                  bottom + 80, MID)

    label = font(FONT_BOLD, 44)
    sub = font(FONT_REG, 32)

    # Car zone: center floor.
    d.rectangle([560, 420, 1240, 1130], outline=MID, width=4)
    d.rounded_rectangle([700, 560, 1100, 1040], radius=70, outline=INK, width=7)
    d.ellipse([745, 960, 845, 1060], outline=INK, width=7)
    d.ellipse([955, 960, 1055, 1060], outline=INK, width=7)
    d.ellipse([745, 580, 845, 680], outline=INK, width=7)
    d.ellipse([955, 580, 1055, 680], outline=INK, width=7)
    text_centered(d, "1 · CAR ZONE", label, 900, 440)
    text_centered(d, "floor stays clear", sub, 900, 495, MID)

    # Tool zone: left wall (with bench).
    d.rectangle([left + 8, top + 8, 540, 760], fill=SHADE)
    d.rectangle([left + 30, 300, 380, 420], outline=INK, width=6)
    text_centered(d, "bench", sub, 270, 340, MID)
    text_centered(d, "2 · TOOL ZONE", label, 345, 190)
    text_centered(d, "near the light", sub, 345, 245, MID)

    # Garden zone: right wall near door.
    d.rectangle([1260, 520, right - 8, bottom - 8], fill=SHADE)
    text_centered(d, "3 · GARDEN", label, 1455, 560)
    text_centered(d, "ZONE", label, 1455, 615)
    text_centered(d, "near the exit", sub, 1455, 675, MID)

    # Seasonal zone: back wall, high/far.
    d.rectangle([560, top + 8, 1240, 400], fill=SHADE)
    text_centered(d, "4 · SEASONAL ZONE", label, 900, 220)
    text_centered(d, "high shelves & ceiling — touched twice a year", sub, 900, 280, MID)

    # Recycling zone: just inside the door, left.
    d.rectangle([left + 8, 780, 540, bottom - 8], fill=SHADE)
    text_centered(d, "5 · RECYCLING", label, 345, 880)
    text_centered(d, "ZONE", label, 345, 935)
    text_centered(d, "inside the door — out fast", sub, 345, 995, MID)

    text_centered(d, "THE FIVE-ZONE MAP", font(FONT_BOLD, 56), width / 2, 40)
    img.save(OUTPUT_DIR / "zone-map.png")


# --- Diagram 2: the shadow-board pegboard --------------------------------------

def pegboard():
    width, height = 1800, 1200
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)

    # Board with peg holes.
    left, top, right, bottom = 150, 180, 1650, 1000
    d.rectangle([left, top, right, bottom], outline=INK, width=8)
    for y in range(top + 60, bottom - 30, 70):
        for x in range(left + 60, right - 30, 70):
            d.ellipse([x - 6, y - 6, x + 6, y + 6], outline=MID, width=3)

    def outline_hammer(cx, cy, present):
        col = INK if present else MID
        wdt = 7 if present else 5
        d.rectangle([cx - 95, cy, cx + 95, cy + 55], outline=col, width=wdt)
        d.rounded_rectangle([cx - 20, cy + 55, cx + 20, cy + 290], radius=20,
                            outline=col, width=wdt)

    def outline_wrench(cx, cy, present):
        col = INK if present else MID
        wdt = 7 if present else 5
        d.ellipse([cx - 60, cy, cx + 60, cy + 120], outline=col, width=wdt)
        d.rounded_rectangle([cx - 22, cy + 110, cx + 22, cy + 300], radius=22,
                            outline=col, width=wdt)

    def outline_screwdriver(cx, cy, present):
        col = INK if present else MID
        wdt = 7 if present else 5
        d.rounded_rectangle([cx - 30, cy, cx + 30, cy + 130], radius=24,
                            outline=col, width=wdt)
        d.line([cx, cy + 130, cx, cy + 300], fill=col, width=wdt + 4)

    outline_hammer(450, 330, True)
    outline_wrench(900, 320, True)
    outline_screwdriver(1350, 330, False)  # the missing tool — the empty outline

    lab = font(FONT_REG, 34)
    text_centered(d, "hammer", lab, 450, 660, MID)
    text_centered(d, "wrench", lab, 900, 660, MID)
    text_centered(d, "?", font(FONT_BOLD, 64), 1350, 470, MID)
    text_centered(d, "the empty outline asks", lab, 1350, 660, MID)
    text_centered(d, "for its tool back", lab, 1350, 705, MID)

    text_centered(d, "THE SHADOW BOARD", font(FONT_BOLD, 56), width / 2, 40)
    text_centered(d, "an outline behind every tool — you see at a glance what's missing",
                  font(FONT_REG, 38), width / 2, 110, MID)
    img.save(OUTPUT_DIR / "pegboard.png")


# --- Diagram 3: the 10-step road strip ------------------------------------------

def ten_steps():
    width, height = 1800, 1500
    img = Image.new("RGB", (width, height), PAPER)
    d = ImageDraw.Draw(img)

    steps = [
        ("1", "Set the goal"), ("2", "Empty it out"), ("3", "Keep · lose · relocate"),
        ("4", "Handle the dangerous"), ("5", "Draw the zone map"),
        ("6", "Get it off the floor"), ("7", "Label everything"),
        ("8", "Shine it"), ("9", "Set the rules"), ("10", "Sustain it"),
    ]
    phases = [(0, 0, "PREP"), (1, 3, "SORT"), (4, 6, "SET IN ORDER"),
              (7, 7, "SHINE"), (8, 8, "STANDARDIZE"), (9, 9, "SUSTAIN")]

    rows = 5
    col_x = (480, 1320)
    row_y = [260 + i * 240 for i in range(rows)]
    num_f = font(FONT_BOLD, 52)
    step_f = font(FONT_BOLD, 40)
    phase_f = font(FONT_REG, 30)

    phase_of = {}
    for start, end, name in phases:
        for i in range(start, end + 1):
            phase_of[i] = name

    centers = []
    for i, (num, title) in enumerate(steps):
        row, col = divmod(i, 2)
        cx, cy = col_x[col], row_y[row]
        centers.append((cx, cy))

    # Connecting path (serpentine).
    for a, b in zip(centers, centers[1:]):
        d.line([a, b], fill=SHADE, width=14)

    for i, ((num, title), (cx, cy)) in enumerate(zip(steps, centers)):
        d.ellipse([cx - 64, cy - 64, cx + 64, cy + 64], fill=PAPER, outline=INK, width=8)
        text_centered(d, num, num_f, cx, cy - 34)
        text_centered(d, title, step_f, cx, cy + 84)
        text_centered(d, phase_of[i], phase_f, cx, cy + 136, MID)

    text_centered(d, "THE 10-STEP PROGRAM", font(FONT_BOLD, 60), width / 2, 50)
    text_centered(d, "one or two steps per weekend — about five weekends in all",
                  font(FONT_REG, 40), width / 2, 130, MID)
    img.save(OUTPUT_DIR / "ten-steps.png")


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    zone_map()
    pegboard()
    ten_steps()
    for name in ("zone-map.png", "pegboard.png", "ten-steps.png"):
        path = OUTPUT_DIR / name
        print(f"Built {path} — {Image.open(path).size}")


if __name__ == "__main__":
    main()
