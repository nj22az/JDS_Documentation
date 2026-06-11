# Fonts — rounded display face

The book's headings and the compartment "bento" furniture (chapter cards, box labels,
legend) are set in a **rounded maru-gothic** face — the friendly, Japanese-information-design
look. HG Maru Gothic Pro is proprietary, so we use its free equivalent:

**M PLUS Rounded 1c** — © The M+ FONTS Project Authors, licensed under the
**SIL Open Font License 1.1** (see `OFL.txt`). Source: <https://github.com/coz-m/MPLUS_FONTS>.
The OFL permits embedding in documents, including commercial ones.

## What's here

| File | What it is |
|------|------------|
| `MPLUSRounded1c-{Regular,Medium,Bold}-subset.ttf` | Subset weights actually embedded in the book |
| `OFL.txt` | The licence (must travel with the font) |

The full weights live in `jds/assets/fonts/`. `scripts/build-fonts.py` subsets them to just the
characters the book uses (Latin + accents + punctuation + the five box icons ▲ ▶ ● ◆ ◇),
turning ~3.5 MB per weight into ~60 KB — so the EPUB stays small and incurs **no KDP delivery
fee**. Rebuild the subsets with:

```bash
python3 scripts/build-fonts.py
```

`build-epub.py` embeds these subsets and references them via `@font-face`; `build-print-pdf.py`
loads them through a weasyprint `FontConfiguration`. Body text stays serif for long-form
readability.
