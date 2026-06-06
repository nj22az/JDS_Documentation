# Cover Brief & KDP Specs

> The cover is the single biggest driver of impulse sales on Amazon. `cover.jpg` in this
> folder is a programmatic first draft (built by `scripts/build-cover.py`). This brief
> documents the specs and the design so it can be iterated or handed to a designer.

---

## eBook cover (current deliverable)

| Spec | Value |
|------|-------|
| File | `cover-en.jpg` (English, primary) · `cover.jpg` (Swedish) |
| Size | 1600 × 2560 px (Amazon's recommended 1.6:1 ratio) |
| Colour | RGB |
| Format | JPEG, quality 92 |
| Max file size | 50 MB (KDP limit) — current ~230 KB |

**Design (draft):** JDS navy background; a pegboard panel with three amber tool silhouettes
(hammer, wrench, screwdriver) hung from a rail; bold cream title **STÄDA I GARAGET** set big
for thumbnail legibility; amber kicker line foregrounding the engineer/5S angle; subtitle and
author below. Rebuild any time with `python3 scripts/build-cover.py --lang en` (or `--lang sv`).
The English cover headlines "A 10-STEP PROGRAM…"; the Swedish one "ETT 10-STEGSPROGRAM…".

**Thumbnail test:** the title must be readable at ~160 px wide (the size in Amazon search).
The two-line, high-contrast title passes this; keep it if iterating.

## Paperback cover (later — needs page count first)

A print cover is a single wraparound PDF (back + spine + front) and can only be finalised once
the interior is laid out and the **page count** is known.

| Spec | Value / formula |
|------|-----------------|
| Trim size | 6 × 9 in (15.24 × 22.86 cm) — standard non-fiction |
| Bleed | 0.125 in on all outer edges |
| Spine width | pages × 0.0572 mm (white paper) — compute after layout |
| Back cover | Short hook + 4–5 bullet benefits + author line + barcode area |
| Resolution | 300 DPI, CMYK PDF |

## If handing to a professional designer

Give them: this brief, `cover.jpg` as the concept, the JDS palette (navy #13314F, amber
#E8A33D, cream #F4F1EB), and the title/subtitle/author text. Ask for a photographic option
too — a real, beautifully ordered pegboard wall shot often outsells an illustrated cover in
this category.

## Palette

| Colour | Hex | Use |
|--------|-----|-----|
| Navy | #13314F | Background |
| Navy light | #204468 | Pegboard panel |
| Amber | #E8A33D | Accent, tools, kicker |
| Cream | #F4F1EB | Title text |
| Muted blue | #B4C6D6 | Subtitle text |
