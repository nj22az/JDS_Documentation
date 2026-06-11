# Städa i Garaget / The Garage Reset — Book Project

| | |
|---|---|
| **Document No.** | JDS-PRJ-GEN-001 |
| **Revision** | DRAFT |
| **Date** | 2026-06-10 |
| **Status** | DRAFT |
| **Author** | N. Johansson |
| **Client** | Internal (self-published) |
| **Project Code** | REDA |

---

## What Is This?

A book about decluttering, cleaning out, and keeping order in the **garage, workshop, and
storage room** — the spaces that home-organizing bestsellers leave out.

**Two editions. Primary market: EU / Sweden; secondary: USA / international.**

- **Primary edition — Swedish:** *Städa i Garaget — rensa, organisera och håll ordning i verkstad
  och förråd* (amazon.se / EU). Metric, Swedish build conventions.
- **Secondary edition — English:** *The Garage Reset — A 10-Step Program to Declutter, Organize,
  and Keep Order in Your Garage and Workshop* (amazon.com / international). Metric-first with
  imperial in parentheses.

The English text is the **authoring master** (the author's English is the stronger draft); the
Swedish primary edition is translated and localized from it. The book applies a real engineer's
**5S method** (Sort · Set in Order · Shine · Standardize · Sustain) — the order system used in
professional workshops — to the one room the lifestyle authors avoid.

---

## Why This Niche (Market Summary)

The full analysis lives in [`01-research/JDS-RPT-GEN-001_market-research.md`](01-research/JDS-RPT-GEN-001_market-research.md).
In short:

- **The category sells.** Marie Kondo (*Konsten att städa*), Margareta Magnusson
  (*Döstädning*) and Paulina Draganja (*Förvaringsdrottningen*) are proven Swedish
  bestsellers — decluttering is a durable, repeat-purchase market.
- **The shelf is empty.** Every one of those books is about the *home*. A search of
  Bokus, Adlibris and Amazon.se finds **no dedicated Swedish book** on the garage or
  workshop — only retailer guides and blog posts.
- **The demand is real.** 610,000+ holiday homes plus a deep villa/DIY culture mean
  garages and förråd everywhere; retailers (Clas Ohlson, Bauhaus/Elfa, Byggahus)
  invest heavily in garage-organizing content because the audience exists.
- **The author has an unfair advantage.** A working marine/field-service engineer can
  credibly bring 5S and workshop discipline — tools, safety, fasteners, fluids — that
  no lifestyle blogger can match.

**Verdict:** a genuine, defensible niche in a proven category.

---

## How This Project Is Organised

```
JDS-PRJ-GEN-001/
│
├── README.md                                  ← this file (project charter)
├── CHANGELOG.md                               ← master change log for the whole project
│
├── 01-research/                               ← market & competitive research
│   └── JDS-RPT-GEN-001_market-research.md      ← the demand/gap analysis
│
├── 02-manuscript/                             ← the book itself (bilingual)
│   ├── JDS-MAN-GEN-001_book-outline.md          ← concept, structure, chapter outline
│   ├── JDS-MAN-GEN-002_style-guide.md           ← voice, method words, chapter shape, self-check
│   ├── en/                                      ← ENGLISH master (The Garage Reset)
│   │   ├── frontmatter/  chapters/  backmatter/   (chapter-NN-*.md)
│   └── sv/                                      ← Swedish edition (Städa i Garaget)
│       ├── frontmatter/  chapters/  backmatter/   (kapitel-NN-*.md)
│
│  Authoring: `/write-chapter` drafts against the style guide, then
│  `scripts/book-check.py --lang en|sv` self-corrects until ✓ clean.
│
├── 03-assets/                                 ← photos, diagrams, illustrations
│   └── images/
│
└── 04-production/                             ← KDP package (both editions)
    ├── The-Garage-Reset.epub / cover-en.jpg     ← English (primary)
    ├── Stada-i-Garaget.epub / cover.jpg         ← Swedish
    ├── amazon-listing-en.md / -sv.md            ← description, keywords, categories, pricing
    ├── cover-brief.md                           ← cover specs (eBook + paperback)
    └── readiness-assessment.md                  ← honest "is it sellable yet" review
```

Build the KDP package from the manuscript with `scripts/build-cover.py --lang en` then
`scripts/build-epub.py --lang en` (see `04-production/README.md`).

---

## Objectives

- [ ] Validate the niche with market research *(done — see JDS-RPT-GEN-001)*
- [x] Lock the book concept, target reader and structure (JDS-MAN-GEN-001)
- [x] Establish the manuscript style guide & self-correcting check (JDS-MAN-GEN-002 + book-check.py)
- [x] Draft the full manuscript, chapter by chapter *(all 15 chapters drafted, passing book-check.py)*
- [ ] Author review pass; illustration plan; publishing route
- [ ] Produce illustrations / photo plan
- [ ] Decide publishing route (self-publish vs. publisher pitch)
- [ ] Final manuscript ready for layout

---

## Scope

**Included:** Swedish-language manuscript; structure and method; market positioning;
illustration plan; publishing decision.

**Excluded (for now):** Print production, ISBN registration, distribution contracts,
translation editions — handled once the manuscript is approved.

---

## Status

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Market research & niche validation | ✅ Complete |
| 2 | Concept, outline & style guide | ✅ Complete |
| 3 | Manuscript — English master (all 15 ch.) + Swedish edition | ✅ Complete — draft |
| 4 | KDP eBook package both editions (EPUB + diagrams, cover, listing) | ✅ Built — ready to upload |
| 5 | Paperback: interior PDFs + wraparound print covers + diagrams | ✅ Built — ready to upload |
| 6 | Profitability plan & pricing (JDS-RPT-GEN-002) | ✅ Decided — $6.99 / $14.99, KDP Select |
| 7 | Author review (bio, safety passages) & beta reviews | ⬜ Not started — human step |

---

## Related Documents

| Document No. | Title |
|---|---|
| JDS-RPT-GEN-001 | Market Research — Swedish Garage & Workshop Decluttering Book |
| JDS-MAN-GEN-001 | Städa i Garaget — Book Concept & Chapter Outline |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| DRAFT | 2026-06-05 | N. Johansson | Project created — research complete, concept and outline drafted |
