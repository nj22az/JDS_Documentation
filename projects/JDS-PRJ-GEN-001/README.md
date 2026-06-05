# Reda i garaget — Book Project

| | |
|---|---|
| **Document No.** | JDS-PRJ-GEN-001 |
| **Revision** | DRAFT |
| **Date** | 2026-06-05 |
| **Status** | DRAFT |
| **Author** | N. Johansson |
| **Client** | Internal (self-published / publisher pitch) |
| **Project Code** | REDA |

---

## What Is This?

A **Swedish-language book** about decluttering, cleaning out, and keeping order in the
**garage, workshop (verkstad) and storage room (förråd)** — the spaces that every
Swedish home-organizing bestseller leaves out.

Working title: **"Reda i garaget — rensa, organisera och håll ordning i verkstad och förråd"**

The book takes the proven Swedish decluttering format (clear, project-by-project,
warm and practical) and applies a real engineer's **5S workshop method** to the one
room the lifestyle authors avoid: the space full of tools, oil, fasteners, seasonal
gear and heavy equipment.

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
├── 02-manuscript/                             ← the book itself
│   ├── JDS-MAN-GEN-001_book-outline.md          ← concept, structure, chapter outline
│   ├── JDS-MAN-GEN-002_style-guide.md           ← voice, method words, chapter shape, self-check
│   └── chapters/                                ← Swedish chapter drafts (kapitel-NN-*.md)
│
│  Authoring: `/write-chapter` drafts a chapter against the style guide, then
│  `scripts/book-check.py` self-corrects it until it reports ✓ clean.
│
├── 03-assets/                                 ← photos, diagrams, illustrations
│   └── images/
│
└── 04-production/                             ← cover, layout, ISBN, publishing notes
```

---

## Objectives

- [ ] Validate the niche with market research *(done — see JDS-RPT-GEN-001)*
- [ ] Lock the book concept, target reader and structure (JDS-MAN-GEN-001)
- [x] Establish the manuscript style guide & self-correcting check (JDS-MAN-GEN-002 + book-check.py)
- [ ] Draft the full manuscript, chapter by chapter *(Del 1 + Del 2 sample chapters done — 5 of 15)*
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
| 2 | Concept & outline | 🟡 In progress |
| 3 | Manuscript draft | ⬜ Not started |
| 4 | Illustration & production | ⬜ Not started |
| 5 | Publishing | ⬜ Not started |

---

## Related Documents

| Document No. | Title |
|---|---|
| JDS-RPT-GEN-001 | Market Research — Swedish Garage & Workshop Decluttering Book |
| JDS-MAN-GEN-001 | Reda i garaget — Book Concept & Chapter Outline |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| DRAFT | 2026-06-05 | N. Johansson | Project created — research complete, concept and outline drafted |
