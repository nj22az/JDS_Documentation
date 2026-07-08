# EIC — The Front-Row Seat

| Field | Value |
|-------|-------|
| **Type** | Literary Project |
| **Working Title** | The Front-Row Seat: Five Centuries of History from the Banks of the Thames |
| **Status** | DRAFT |
| **Started** | 2026-07-01 |
| **Author** | N. Johansson |

---

## What Is This?

A historical fiction anthology-novel: the East India Company, told from one fixed
point of view — the Prospect of Whitby (formerly the Devil's Tavern) in Wapping,
London — across five centuries, from its 1600 charter to its 2019 afterlife as a
tourist stop across the river from Canary Wharf. Real history (the Every manhunt,
Kidd's hanging, the Bengal Famine, the Company's 1772 bailout and the Boston
Tea Party, the Opium Wars, the Cutty Sark killing, Cawnpore) mixed with invented characters and, in one chapter, an invented
resolution to a real unsolved crime (the 1888 Whitechapel murders).

Not a JDS-numbered engineering document — this folder is non-technical creative
writing tracked outside the JDS document numbering system, alongside other work
output under `projects/`.

## Structure

```
EIC/
├── README.md                       ← This project card
├── CHANGELOG.md                    ← Change log
├── manuscript/                     ← Draft chapters, in reading order (source of truth)
│   ├── 00-frontmatter.md / 00a-foreword.md
│   ├── 01-1603 ... 15-2019         ← 15 chapters, numbered chronologically
│   └── appendix-timeline.md / appendix-bibliography.md
├── exports/
│   ├── the-front-row-seat.md       ← Compiled single-file book (regenerate after chapter edits)
│   └── the-front-row-seat.pdf      ← Publishable 6×9 book PDF (`python3 scripts/md2book.py projects/literary/EIC/manuscript projects/literary/EIC/exports/the-front-row-seat.pdf`)
├── notes/
│   └── outline-and-craft-plan.md   ← Working plan: strengths, weaknesses, next moves
└── references/                     ← Source material, inspiration (empty so far)
```

## Status

15 chapters drafted (1603–2019; the 1603 evening spans two), every chapter carrying an invented protagonist
with an active in-scene choice, connected across the centuries by three light
background devices (the Cache under the bar, the Maggie/Hannah keeper line, and
recurring "scar tissue" damage to the room itself). See
`notes/outline-and-craft-plan.md` for the standing craft plan; remaining work is
polish-level (epigraph consistency, refrain rationing, an Author's Note, and a
full continuity read-through), not structural. Next decisions are logged there,
not here.
