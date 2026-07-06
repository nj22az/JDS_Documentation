# The Front-Row Seat — web reader

A static React (Vite + TypeScript) reading edition of the novel, built for
readability with an Apple-inspired design: serif reading body, comfortable
measure, light/dark/auto appearance, adjustable text size, a cover + contents
view, a reading-progress bar, and keyboard chapter navigation.

**Live:** https://nj22az.github.io/the-front-row-seat/

## Source of truth

The **manuscript is the source of truth** (`../manuscript/*.md`). This app never
holds its own copy of the prose. `tools/build_content.py` compiles the manuscript
into `src/data/content.json` and copies the referenced images from the canonical
`../exports/html/assets/` into `public/assets/`. Both of those are generated and
git-ignored — regenerate them, don't edit them by hand.

Illustrations (heroes, inline figures, credits) are declared in
`../exports/html/assets/data/archive-assets.json` and mapped to chapters/sections
in `tools/build_content.py` (`HERO` and `INLINE`).

## Build

```bash
# 1. compile content + copy images from the manuscript & canonical assets
python3 tools/build_content.py          # needs: pip install markdown

# 2. install and build the app
npm install
npm run build                           # -> dist/
```

`dist/` is what gets deployed to `nj22az.github.io/the-front-row-seat/`.
`base: "./"` + `HashRouter` mean it runs from any sub-path with no server config.

## Develop

```bash
python3 tools/build_content.py
npm run dev            # http://localhost:5173
```

## Deploy

Copy the built `dist/` into the site repo at `the-front-row-seat/` and push
(GitHub Pages, served from `main`).

## Editing flow

1. Edit the chapter in `../manuscript/NN-*.md`.
2. `python3 tools/build_content.py` (recompiles content + assets).
3. `npm run build`, then deploy `dist/`.
