# EIC — The Front-Row Seat

| Field | Value |
|-------|-------|
| **Type** | Literary Project |
| **Title** | The Front-Row Seat: A Six-Book Historical Omnibus |
| **Status** | Book One complete at 100,000 words; Books Two–Six in compact edition |
| **Started** | 2026-07-01 |
| **Author** | N. Johansson |

---

## What Is This?

A historical-fiction cycle about the East India Company, observed from one fixed
point on the Thames: the riverside house now called the Prospect of Whitby. The
six books span 1603–2019. Real events and economic systems are carried by invented
characters whose private accounts preserve what official ledgers omit.

Book One, *The Venture*, is a standalone historical novel of exactly 100,000 words
by the project's inclusive manuscript count. It contains twenty-two numbered
chapters and an epilogue. The later books remain the compact omnibus editions while
their standalone expansions are developed.

This is non-technical creative work, so it is not assigned a JDS document number.
Git remains the controlled source under the wider JDS project structure.

## Source and Reading Order

`manuscript/` is the source of truth for publication. Its Markdown pages use YAML
keys (`id`, `kicker`, `year`, `title`, `hero`) that remain stable when chapter
titles or positions change. `manuscript/publishing-manifest.json` is the only
authoritative reading order; Book One must never be sorted by filename or year.

The manifest also records book groupings, hidden pages, reader taglines, and the
publication metadata used by the website build. The Wapping Twelve reference is
published at a stable deep link but deliberately omitted from contents and linear
previous/next navigation.

```text
EIC/
├── README.md
├── CHANGELOG.md
├── manuscript/
│   ├── publishing-manifest.json
│   ├── front-matter/
│   ├── book-1-the-venture/         # 22 chapters + Epilogue + hidden reference
│   ├── book-2-the-gallows-years/
│   ├── book-3-kings-of-bengal/
│   ├── book-4-the-poppy/
│   ├── book-5-the-watchmans-daughter/
│   ├── book-6-the-engine-room/
│   └── appendices/
├── reader/                         # React/Vite illustrated reading edition
├── exports/
│   ├── the-front-row-seat.md      # generated single-file reading export
│   └── html/assets/               # canonical visual archive and credits
└── notes/                           # editorial and research notes
```

Private series mechanics and expansion working notes remain outside the published
JDS manuscript tree. They must not be emitted by the website build.

## Build and Publish

From `reader/`:

```bash
python3 tools/build_content.py
npm run build
```

The content build validates all 48 declared Markdown pages, emits the reader JSON,
copies and credits the canonical images, generates grouped SEO/no-JavaScript
content, writes reading statistics, and refreshes the compiled Markdown export.
The Vite build writes the deployable site to `reader/dist/`.

The live reader is published from `the-front-row-seat/` on the `main` branch of
`nj22az/nj22az.github.io` and is available at:

<https://nj22az.github.io/the-front-row-seat/>
