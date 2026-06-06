# Production — KDP Package

Everything needed to publish the book on Amazon KDP. The book is **English-first** (master:
*The Garage Reset*) with a **Swedish edition** (*Städa i Garaget*) to be kept in step.

## Contents

| File | Edition | What it is |
|------|---------|------------|
| `The-Garage-Reset.epub` | EN | Uploadable eBook (front matter + 15 chapters + back matter, with cover) |
| `cover-en.jpg` | EN | KDP eBook cover, 1600×2560 |
| `amazon-listing-en.md` | EN | Title fields, HTML description, keywords, categories, pricing |
| `Stada-i-Garaget.epub` | SV | Uploadable Swedish eBook |
| `cover.jpg` | SV | Swedish KDP cover, 1600×2560 |
| `amazon-listing-sv.md` | SV | Swedish listing copy |
| `cover-brief.md` | — | Cover specs (eBook + paperback) and design rationale |
| `readiness-assessment.md` | — | Honest "is it sellable yet" review + priority next steps |

## Rebuild

The EPUBs and covers are generated from the manuscript — never hand-edit them. Rebuild after any
change to a chapter or front/back-matter file:

```bash
# English (primary)
python3 scripts/build-cover.py --lang en
python3 scripts/build-epub.py  --lang en
python3 scripts/book-check.py --all --lang en

# Swedish
python3 scripts/build-cover.py --lang sv
python3 scripts/build-epub.py  --lang sv
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
