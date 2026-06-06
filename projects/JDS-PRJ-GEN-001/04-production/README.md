# Production — KDP Package

Everything needed to publish *Städa i Garaget* on Amazon KDP.

## Contents

| File | What it is |
|------|------------|
| `Stada-i-Garaget.epub` | The uploadable eBook (front matter + 15 chapters + back matter, with cover) |
| `cover.jpg` | KDP eBook cover, 1600×2560 |
| `amazon-listing.md` | Title fields, HTML book description, 7 keywords, categories, pricing |
| `cover-brief.md` | Cover specs (eBook + paperback) and design rationale |
| `readiness-assessment.md` | Honest "is it sellable yet" review + priority next steps |

## Rebuild

The EPUB and cover are generated from the manuscript — never hand-edit the EPUB. To rebuild
after changing any chapter or front/back-matter file:

```bash
python3 scripts/build-cover.py      # regenerates cover.jpg
python3 scripts/build-epub.py       # regenerates Stada-i-Garaget.epub (embeds the cover)
python3 scripts/book-check.py --all # confirm chapters still pass
```

## Upload checklist (KDP)

1. Create a new Kindle eBook title on KDP.
2. Paste title, subtitle, author, description (HTML) and keywords from `amazon-listing.md`.
3. Choose categories (see `amazon-listing.md`).
4. Upload `Stada-i-Garaget.epub` as the manuscript and `cover.jpg` as the cover.
5. Preview in KDP's previewer, set price, publish.

> The paperback is a later step — it needs a laid-out interior PDF and a wraparound cover
> (see `cover-brief.md`).
