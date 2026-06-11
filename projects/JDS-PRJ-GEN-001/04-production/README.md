# Production — KDP Package

Everything needed to publish the book on Amazon KDP. The book is **English-first** (master:
*The Garage Reset*) with a **Swedish edition** (*Städa i Garaget*) to be kept in step.

## Contents

| File | Edition | What it is |
|------|---------|------------|
| `The-Garage-Reset.epub` | EN | Uploadable eBook with embedded diagrams |
| `cover-en.jpg` | EN | KDP eBook cover, 1600×2560 |
| `The-Garage-Reset-Interior.pdf` | EN | **Paperback interior** — 5.5×8.5 in, 123 pp, B&W, mirrored margins, part dividers |
| `The-Garage-Reset-Print-Cover.pdf` | EN | **Wraparound print cover** — back + 0.277 in spine + front, 300 DPI, bleed |
| `amazon-listing-en.md` | EN | Title fields, HTML description, keywords, categories, pricing |
| `Stada-i-Garaget.epub` | SV | Uploadable Swedish eBook |
| `cover.jpg` | SV | Swedish KDP cover, 1600×2560 |
| `Stada-i-Garaget-Interior.pdf` | SV | Swedish paperback interior — 131 pp, localized diagrams + QR toolkit |
| `Stada-i-Garaget-Print-Cover.pdf` | SV | Swedish wraparound print cover (0.295 in spine) |
| `amazon-listing-sv.md` | SV | Swedish listing copy |
| `advertising-kit.md` | EN+SV | Ad-ready taglines, hooks, blurbs, social copy, pull-quotes, targeting |
| `cover-brief.md` | — | Cover specs + **designer brief & 3 concept directions** (the #1 launch investment) |
| `launch-kit.md` | — | Beta-reader & review request templates + launch checklist + timing |
| `readiness-assessment.md` | — | Honest "is it sellable yet" review + priority next steps |
| `printables/{en,sv}/*.pdf` | EN+SV | The fill-in templates readers download & print (inventory, lifetime journal, hazmat log, zone worksheet, seasonal pass, maintenance program, fire round, safety round) |

Illustrations (original, licence-free) live in `03-assets/images/`: `before-after`, `zone-map`,
`pegboard`, `ten-steps` (each with a `-sv` variant). The **before → after** image is the hero for
ads and the book's Introduction. QR codes for the printables live in `03-assets/images/qr/`.

> **Before publishing — set the real download URL.** The QR codes and the Toolkit appendix point
> at placeholder addresses (`thegaragereset.com/print`, `stadaigaraget.se/skriv-ut`). Host the
> `printables/` PDFs somewhere public, set the real base URL in `scripts/build-qr.py` (and the
> address text in the two Toolkit appendix files), then re-run `build-qr.py` and `build-epub.py`.

Pricing & launch configuration (KDP Select, $6.99 eBook / $14.99 paperback) is decided in
[JDS-RPT-GEN-002 Profitability Plan](../01-research/JDS-RPT-GEN-002_profitability-plan.md).

> **Note:** the print cover regenerates from the interior's page count. If any chapter
> changes, rebuild in order: `build-print-pdf.py` → `build-print-cover.py`.

## Rebuild

The EPUBs and covers are generated from the manuscript — never hand-edit them. Rebuild after any
change to a chapter or front/back-matter file:

```bash
# English (primary)
python3 scripts/build-cover.py --lang en
python3 scripts/build-epub.py  --lang en
python3 scripts/build-diagrams.py            # only if a diagram changed
python3 scripts/build-print-pdf.py --lang en   # paperback interior (reports page count)
python3 scripts/build-print-cover.py --lang en # wraparound cover (reads page count)
python3 scripts/book-check.py --all --lang en

# printables + QR (run once, or after changing the download URL)
python3 scripts/build-printables.py --lang en && python3 scripts/build-printables.py --lang sv
python3 scripts/build-qr.py --lang en && python3 scripts/build-qr.py --lang sv

# Swedish (primary)
python3 scripts/build-diagrams.py --lang sv     # localized figures
python3 scripts/build-cover.py --lang sv
python3 scripts/build-epub.py  --lang sv
python3 scripts/build-print-pdf.py --lang sv
python3 scripts/build-print-cover.py --lang sv
python3 scripts/book-check.py --all --lang sv
```

## Upload checklist (KDP)

1. Create a new Kindle eBook title on KDP (one per edition/marketplace).
2. Paste title, subtitle, author, description (HTML) and keywords from the matching
   `amazon-listing-*.md`.
3. Choose categories (see the listing file).
4. Upload the matching `.epub` as the manuscript and the matching cover as the cover image.
5. Preview in KDP's previewer, set price, publish.

> The paperback is a later step — it needs a laid-out interior PDF and a wraparound cover
> (see `cover-brief.md`).
