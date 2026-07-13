# EIC — The Front-Row Seat

| Field | Value |
|-------|-------|
| **Type** | Literary Project |
| **Working Title** | The Front-Row Seat: Five Centuries of History from the Banks of the Thames |
| **Status** | LIVE CANON PROTECTED; EDITORIAL REVISION IN PROGRESS |
| **Started** | 2026-07-01 |
| **Author** | N. Johansson |

---

## What Is This?

A historical fiction anthology-novel: the East India Company, told from one fixed
place — the historic Wapping tavern site now called the Prospect of Whitby —
across five centuries, from its 1600 charter to its 2019 afterlife as a tourist
stop across the river from Canary Wharf. Real history (the Every manhunt,
Kidd's hanging, the Bengal Famine, the Company's 1772 bailout and the Boston
Tea Party, the Opium Wars, the Cutty Sark killing, Cawnpore) mixed with invented characters and, in one chapter, an invented
resolution to a real unsolved crime (the 1888 Whitechapel murders).

Not a JDS-numbered engineering document — this folder is non-technical creative
writing tracked outside the JDS document numbering system, alongside other work
output under `projects/`.

## Canon and protected editions

The deployed reader at `nj22az.github.io/the-front-row-seat/` is the canon. Its
source revision is protected on `archive/front-row-seat-live-2026-07-11` in the
Pages repository. The earlier JDS manuscript is protected on
`archive/front-row-seat-legacy-2026-07-03` in this repository.

The live reader was recovered from its compiled bundle into 25 Markdown files.
`manuscript-live-canon/` is therefore a read-only editorial mirror, not a new
source competing with the website. Proposed changes belong in
`manuscript-editorial/` until approved.

## Structure

```
EIC/
├── README.md                       ← This project card
├── CHANGELOG.md                    ← Change log
├── manuscript-live-canon/          ← Extracted, read-only mirror of the live reader
├── manuscript-editorial/           ← Approved-scope editorial working copies
├── manuscript/                     ← Protected earlier JDS edition
├── editorial/                      ← Comparison report and edit notes
├── exports/
│   ├── the-front-row-seat.md       ← Compiled earlier JDS edition
│   └── the-front-row-seat-live-canon-2026-07-11.md
├── notes/
│   └── outline-and-craft-plan.md   ← Working plan: strengths, weaknesses, next moves
├── tools/
│   └── extract_live_reader.py      ← Reproducible live-reader extraction
└── references/                     ← Source material, inspiration (empty so far)
```

## Status

The live canon contains 15 narrative chapters/interludes and approximately 62,390
narrative words. It is 26.5 per cent longer than the protected JDS edition, with
most expansion concentrated in the 1603, 1626, 1774, 1888 and 1940 material.

The long-form direction is now six independently readable historical novels,
collected eventually as *The Front-Row Seat* omnibus. The anthology remains the
protected compressed canon while those books are developed. See
`editorial/six-volume-omnibus-plan.md` for the working volume boundaries and
reader contract.

Volumes One–Four are Prospect-of-Whitby and East-India-Company first. Su's Volume
Five is the deliberate permission to drift into her wider East End, and Volume
Six may retain that freedom while returning to the Prospect as the cycle's home.
After the Company's 1858 dissolution it appears only through legacy—people,
institutions, docks, records and habits—not as an active organisation.

The first editorial sample covers both 1603 units. It restores the intended
implicit ancestry, removes unsupported history and demonstrates a 31.7 per cent
compression without changing the deployed book. See
`editorial/comparison-2026-07-11.md` and
`editorial/opening-line-edit-2026-07-11.md` before extending the edit.

The current final-book development sample is
`manuscript-editorial/14-2019-what-jerry-bought.md`. It expands Jerry Vale from a
passing hedge-fund tourist into the cycle's active modern antagonist. His
governing brief is `editorial/jerry-vale-character-brief.md`.
