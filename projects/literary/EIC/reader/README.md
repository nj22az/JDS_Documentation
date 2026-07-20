# The Front-Row Seat — web reader

A static React/Vite reading edition of the six-book historical omnibus. It offers
grouped book and chapter contents, light/dark/automatic appearance, adjustable
type, progress and keyboard navigation, a desktop book-spread layout, credited
illustrations, and a crawlable no-JavaScript edition.

**Live:** <https://nj22az.github.io/the-front-row-seat/>

## Source of truth

The reader does not own prose. It compiles the ordered YAML manuscript under
`../manuscript/` according to `../manuscript/publishing-manifest.json`.

`tools/build_content.py` produces:

- `src/data/content.json` — all 48 ordered pages and credits;
- `public/assets/` — images copied from `../exports/html/assets/`;
- `public/omnibus-config.js` — generated book order, word counts, and taglines;
- `public/sitemap.xml` and the SEO regions in `index.html`;
- `../exports/the-front-row-seat.md` — compiled Markdown in reading order.

These generated reader files are ignored. Do not edit them by hand. The tracked
overlay source in `public/omnibus*.{js,css}` preserves the production reader's
six-book contents and desktop spread treatment.

## Build

```bash
python3 tools/build_content.py
npm install                 # first setup only
npm run build               # writes dist/
```

The content step fails if a manuscript page is missing, unlisted, duplicated, or
lacks the required YAML metadata. Book One should report exactly 100,000 words.

## Develop

```bash
python3 tools/build_content.py
npm run dev
```

The Vite application uses a relative base and `HashRouter`, so deep reading links
work beneath the GitHub Pages subdirectory without server rewrites.

## Publish

Copy the verified contents of `dist/` into `the-front-row-seat/` in a current clone
of `nj22az/nj22az.github.io`. Preserve the separate
`1888-motion-graphic-novel/` page, commit the reader payload, and push `main`.
GitHub Pages deploys the live site automatically.

## Editing flow

1. Edit the relevant page under `../manuscript/`.
2. Change `publishing-manifest.json` only when order or publication metadata changes.
3. Run the content build and confirm its page count and Book One word count.
4. Run the Vite build and publication checks before deployment.
