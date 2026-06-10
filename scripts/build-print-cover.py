#!/usr/bin/env python3
"""Build the KDP paperback wraparound cover (back + spine + front) for JDS-PRJ-GEN-001.

Reads the page count from the built interior PDF, computes the spine width
(pages x 0.002252 in, white paper), and renders a single full-bleed cover PDF at
300 DPI for a 5.5 x 8.5 in trim. The front reuses the eBook cover design; the back
carries the sales hook, benefit bullets, author bio, and a clear barcode area.

Usage:
    python3 scripts/build-print-cover.py                # English print cover
    python3 scripts/build-print-cover.py --lang sv       # Swedish print cover
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader

# --- Configuration (JDS-PRO-004 §3) --------------------------------------------

PRODUCTION = Path("projects/JDS-PRJ-GEN-001/04-production")

DPI = 300
TRIM_W_IN, TRIM_H_IN = 5.5, 8.5
BLEED_IN = 0.125
PAGE_THICKNESS_IN = 0.002252  # KDP white paper
SPINE_TEXT_MIN_PAGES = 100    # KDP guidance: leave the spine blank below this

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
        "interior": PRODUCTION / "The-Garage-Reset-Interior.pdf",
        "output": PRODUCTION / "The-Garage-Reset-Print-Cover.pdf",
        "title1": "THE GARAGE", "title2": "RESET",
        "subtitle": "Declutter, organize, and keep order\nin your garage and workshop",
        "kicker": "A 10-STEP PROGRAM FOR AN ORDERLY GARAGE",
        "author": "NILS JOHANSSON",
        "spine_title": "THE GARAGE RESET",
        "back_head": "The car in the driveway.\nThe tools nowhere to be found.\nThe pile behind the door.",
        "back_lead": ("It isn't your fault — the garage never had a system. "
                      "This book gives you one: a clear 10-step program, one or two "
                      "steps per weekend, built on the 5S method professionals use "
                      "to keep real workshops running."),
        "bullets": [
            "Empty it out, sort it, and let go — with rules that decide for you",
            "Zone the garage so the car fits and the floor stays clear",
            "Find any tool in three seconds with labels and shadow boards",
            "Handle fuel, paint, and chemicals safely",
            "Keep it all in order with just ten minutes a week",
        ],
        "back_bio": ("Nils Johansson is a marine and field-service engineer who has "
                     "spent his working life in workshops and engine rooms — places "
                     "where order is a matter of safety, not appearance."),
    },
    "sv": {
        "interior": PRODUCTION / "Stada-i-Garaget-Interior.pdf",
        "output": PRODUCTION / "Stada-i-Garaget-Print-Cover.pdf",
        "title1": "STÄDA I", "title2": "GARAGET",
        "subtitle": "Rensa, organisera och håll ordning\ni verkstad och förråd",
        "kicker": "ETT 10-STEGSPROGRAM FÖR ETT GARAGE I ORDNING",
        "author": "NILS JOHANSSON",
        "spine_title": "STÄDA I GARAGET",
        "back_head": "Bilen på uppfarten.\nVerktygen försvunna.\nHögen bakom porten.",
        "back_lead": ("Det är inte ditt fel — garaget har aldrig haft ett system. "
                      "Den här boken ger dig ett: ett tydligt 10-stegsprogram, ett "
                      "eller två steg per helg, byggt på metoden proffsen använder "
                      "för att hålla riktiga verkstäder i ordning."),
        "bullets": [
            "Töm, sortera och släpp taget — med regler som bestämmer åt dig",
            "Dela in garaget i zoner så att bilen får plats",
            "Hitta vilket verktyg som helst på tre sekunder",
            "Hantera bensin, färg och kemikalier säkert",
            "Håll ordningen med tio minuter i veckan",
        ],
        "back_bio": ("Nils Johansson är marin- och fältserviceingenjör och har "
                     "tillbringat sitt yrkesliv i verkstäder och maskinrum — platser "
                     "där ordning är en säkerhetsfråga, inte en utseendefråga."),
    },
}


def px(inches):
    return round(inches * DPI)


def font(path, size):
    return ImageFont.truetype(path, size)


def centered(draw, text, fnt, cx, y, fill):
    w = draw.textbbox((0, 0), text, font=fnt)[2]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)


def wrap_text(draw, text, fnt, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def draw_pegboard(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=NAVY_LIGHT)
    step, radius = px(0.23), px(0.023)
    for y in range(y0 + step, y1 - step // 2, step):
        for x in range(x0 + step, x1 - step // 2, step):
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=DOT)


def draw_front(draw, x0, width, height_offset, cfg):
    """Front cover panel: same composition as the eBook cover, scaled to print."""
    s = width / 1600  # scale factor from the 1600-wide eBook design

    def sx(v):
        return x0 + round(v * s)

    def sy(v):
        return height_offset + round(v * 1.0 * s * (2560 / 2560))

    panel_bottom = sy(1120)
    draw_pegboard(draw, x0, height_offset, x0 + width, panel_bottom)
    draw.rectangle([x0, panel_bottom, x0 + width, panel_bottom + round(16 * s)], fill=AMBER)

    # Tools (hammer, wrench, screwdriver) — scaled from the eBook design.
    cx, top = sx(430), sy(360)
    draw.rectangle([cx - round(120 * s), top, cx + round(120 * s), top + round(70 * s)], fill=AMBER)
    draw.rectangle([cx - round(95 * s), top, cx - round(45 * s), top + round(55 * s)], fill=NAVY_LIGHT)
    draw.rounded_rectangle([cx - round(26 * s), top + round(60 * s),
                            cx + round(26 * s), top + round(360 * s)], radius=round(26 * s), fill=AMBER)
    cx, top = sx(800), sy(320)
    draw.rounded_rectangle([cx - round(30 * s), top + round(70 * s),
                            cx + round(30 * s), top + round(360 * s)], radius=round(30 * s), fill=AMBER)
    draw.ellipse([cx - round(80 * s), top, cx + round(80 * s), top + round(160 * s)], fill=AMBER)
    draw.ellipse([cx - round(38 * s), top + round(42 * s),
                  cx + round(38 * s), top + round(118 * s)], fill=NAVY_LIGHT)
    draw.ellipse([cx - round(78 * s), top + round(300 * s),
                  cx + round(78 * s), top + round(420 * s)], fill=AMBER)
    draw.ellipse([cx - round(34 * s), top + round(330 * s),
                  cx + round(34 * s), top + round(390 * s)], fill=NAVY_LIGHT)
    cx, top = sx(1170), sy(360)
    draw.rounded_rectangle([cx - round(38 * s), top, cx + round(38 * s), top + round(180 * s)],
                           radius=round(30 * s), fill=AMBER)
    draw.rectangle([cx - round(14 * s), top + round(175 * s),
                    cx + round(14 * s), top + round(360 * s)], fill=AMBER)

    mid = x0 + width // 2
    centered(draw, cfg["kicker"], font(FONT_BOLD, round(34 * s)), mid, sy(1230), AMBER)
    centered(draw, cfg["title1"], font(FONT_BOLD, round(190 * s)), mid, sy(1330), CREAM)
    centered(draw, cfg["title2"], font(FONT_BOLD, round(190 * s)), mid, sy(1560), CREAM)
    draw.rectangle([x0 + round(120 * s), sy(1820), x0 + width - round(120 * s), sy(1828)], fill=AMBER)
    y = sy(1900)
    for line in cfg["subtitle"].split("\n"):
        centered(draw, line, font(FONT_REG, round(52 * s)), mid, y, MUTED)
        y += round(70 * s)
    centered(draw, cfg["author"], font(FONT_BOLD, round(64 * s)), mid,
             height_offset + round(2560 * s) - round(260 * s), CREAM)


def draw_back(draw, x0, width, top, height, cfg):
    mid = x0 + width // 2
    margin = px(0.55)
    y = top + px(0.7)

    head_f = font(FONT_BOLD, 64)
    for line in cfg["back_head"].split("\n"):
        centered(draw, line, head_f, mid, y, CREAM)
        y += 88

    y += 40
    lead_f = font(FONT_REG, 44)
    for line in wrap_text(draw, cfg["back_lead"], lead_f, width - 2 * margin):
        centered(draw, line, lead_f, mid, y, MUTED)
        y += 62

    y += 50
    bullet_f = font(FONT_REG, 42)
    for bullet in cfg["bullets"]:
        lines = wrap_text(draw, bullet, bullet_f, width - 2 * margin - 70)
        draw.ellipse([x0 + margin, y + 16, x0 + margin + 22, y + 38], fill=AMBER)
        for line in lines:
            draw.text((x0 + margin + 60, y), line, font=bullet_f, fill=CREAM)
            y += 58
        y += 18

    y += 40
    draw.rectangle([x0 + margin, y, x0 + width - margin, y + 5], fill=AMBER)
    y += 50
    bio_f = font(FONT_REG, 38)
    for line in wrap_text(draw, cfg["back_bio"], bio_f, width - 2 * margin):
        centered(draw, line, bio_f, mid, y, MUTED)
        y += 54

    # Barcode clear zone: 2 x 1.2 in, bottom-right of the back panel, in from bleed.
    bc_w, bc_h = px(2.0), px(1.2)
    bx1 = x0 + width - px(0.25)
    by1 = top + height - px(0.25)
    draw.rectangle([bx1 - bc_w, by1 - bc_h, bx1, by1], fill=(255, 255, 255))


def build(cfg):
    pages = len(PdfReader(str(cfg["interior"])).pages)
    spine_in = pages * PAGE_THICKNESS_IN

    total_w = px(BLEED_IN + TRIM_W_IN + spine_in + TRIM_W_IN + BLEED_IN)
    total_h = px(BLEED_IN + TRIM_H_IN + BLEED_IN)
    spine_w = px(spine_in)
    back_x0 = 0
    back_w = px(BLEED_IN + TRIM_W_IN)
    front_x0 = back_w + spine_w
    front_w = total_w - front_x0

    img = Image.new("RGB", (total_w, total_h), NAVY)
    draw = ImageDraw.Draw(img)

    draw_back(draw, back_x0, back_w, 0, total_h, cfg)

    # Spine: slightly darker band; text only if KDP-safe.
    draw.rectangle([back_w, 0, front_x0, total_h], fill=(15, 39, 63))
    if pages >= SPINE_TEXT_MIN_PAGES:
        spine_font = font(FONT_BOLD, min(round(spine_w * 0.52), 56))
        text = f"{cfg['spine_title']}   ·   {cfg['author']}"
        strip = Image.new("RGB", (total_h, spine_w), (15, 39, 63))
        sd = ImageDraw.Draw(strip)
        bbox = sd.textbbox((0, 0), text, font=spine_font)
        sd.text(((total_h - bbox[2]) / 2, (spine_w - bbox[3]) / 2 - bbox[1] / 2),
                text, font=spine_font, fill=CREAM)
        img.paste(strip.rotate(-90, expand=True), (back_w, 0))

    draw = ImageDraw.Draw(img)
    draw_front(draw, front_x0, front_w, 0, cfg)

    cfg["output"].parent.mkdir(parents=True, exist_ok=True)
    img.save(cfg["output"], "PDF", resolution=DPI)
    return pages, spine_in, (total_w, total_h)


def main():
    args = sys.argv[1:]
    lang = args[args.index("--lang") + 1] if "--lang" in args else "en"
    cfg = LANG_CONFIG[lang]
    pages, spine_in, size = build(cfg)
    print(f"Built {cfg['output']} [{lang}] — {size[0]}x{size[1]} px @ {DPI} DPI")
    print(f"Interior: {pages} pages -> spine {spine_in:.4f} in"
          + ("" if pages >= SPINE_TEXT_MIN_PAGES else "  (below spine-text threshold: spine left blank)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
