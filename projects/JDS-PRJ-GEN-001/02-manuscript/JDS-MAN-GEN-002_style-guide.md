# Städa i Garaget — Manuscript Style Guide

| | |
|---|---|
| **Document No.** | JDS-MAN-GEN-002 |
| **Revision** | A |
| **Date** | 2026-06-05 |
| **Status** | DRAFT |
| **Author** | N. Johansson |

> **Note on language:** This guide is written in English (JDS-QMS-000 §15). It governs how
> the **Swedish** manuscript is written. Swedish examples are quoted as the product.

---

## 1. Why This Guide Exists

Every chapter of *Städa i Garaget* must read as if one person wrote it in one sitting:
same voice, same method words, same chapter shape. This guide is the single source of
truth. The `/write-chapter` skill drafts against it and **self-corrects** against the
checklist in §8 before any chapter is considered done.

## 2. Voice & Tone

- **Language:** English-first (master). The Swedish edition mirrors it. In Swedish: plain,
  modern, spoken-but-tidy, no English loanwords where a normal Swedish word exists.
- **More vivid than plain.** The English master leans into voice: a sharp opening scene per
  chapter, varied rhythm, the occasional first-person engineer aside, and **named** characters
  in examples (Tom, Maria, Erik…) rather than anonymous "a man / a woman". Keep it tasteful —
  warmth and concreteness, not stand-up comedy.
- **Address the reader as "you"** (Swedish: "du") — never an impersonal voice, never "ni".
- **Warm and on the reader's side.** The garage is not a moral failing; it's an overflow
  valve. Never shame, never nag.
- **Engineer's authority, lightly worn.** Short declarative sentences. Concrete nouns
  (hyllplan, krok, märkning), not abstractions. Show the method works; don't oversell.
- **Encouraging, finishable.** Every chapter leaves the reader able to *do* something this
  weekend, not just think about it.
- **Avoid:** exclamation-mark hype, brand names, jargon, long subordinate-clause chains.

## 3. The Method Words (FIXED — never paraphrase)

The book is **English-first** (master: *The Garage Reset*, `en/`) with a **Swedish edition**
(*Städa i Garaget*, `sv/`). The five steps are a fixed vocabulary per edition. Always these
words, always this order, always bold on first use in a chapter:

| Step | English label (master) | Fixed Swedish label | Plain meaning |
|------|------------------------|---------------------|---------------|
| 1 | **Sort** | **Sortera** | Keep / bin / move elsewhere |
| 2 | **Set in Order** | **Systematisera** | A place for everything (zones, shelves, boards) |
| 3 | **Shine** | **Städa** | A clean floor and bench as the baseline |
| 4 | **Standardize** | **Standardisera** | Make the order the default with simple rules |
| 5 | **Sustain** | **Säkra** | Keep it alive with a short routine |

The English labels are the canonical **5S** terms used in real workshops — name 5S explicitly;
it's the author's credibility hook. Use US spelling ("Standardize", not "Standardise"). Do not
invent synonyms for the labels. The five S-words are the brand.

Box labels per edition: **Weekend Project** / Helgprojektet, **Workshop Rule** / Verkstadsregeln,
**Safety** / Säkerhet, **Inherited & Hard** / Ärvt & svårt. Required section headings:
English `## The problem` (Swedish `## Problemet`). The English edition no longer uses a
`## Takeaways` recap — the **Workshop Rule** box is the chapter's takeaway (see §5, §9).

## 4. Fixed Terminology (glossary)

Use these consistently. Pick one term and never drift.

| Use this | Not this |
|----------|----------|
| garaget | garaget/förrådet mixed loosely — name the space you mean |
| verkstad | verkstaden/verkstad — use "verkstad" generically |
| förråd | förrådsutrymme |
| zon | "område" when you mean a defined zon |
| hylla / hyllplan | "hyllor" loosely for shelf *systems* |
| verktygstavla | redskapstavla |
| märkning / märka | "labela", "tagga" |
| helgprojekt | "weekend-projekt", "projekt för helgen" |
| återvinning / miljöstation | "soptippen", "tippen" |
| fritidshus, uthus | "stuga" (use only when quoting people) |

**Units & build conventions:** the product is **EU-first (Sweden primary), USA second.** The
Swedish edition is **metric only**. The English edition is **metric-first with imperial in
parentheses** — e.g., "90 cm (36 in)" — so it reads naturally in both markets. Build specs must
be **EU-aware**: timber studs at **600 mm centres** (note "16 in in North America"), **plasterboard**
not "drywall", concrete/brick/block walls are common, **petrol/gasol** not "gas/propane" as the
primary term. US spelling is kept for the prose (Standardize, organize). **Brands:** none —
describe the *type* of product (wall rail, pegboard, French cleat), never a manufacturer.

## 5. Chapter Shape (every chapter follows this)

1. **Hook** — 1–2 short paragraphs. A recognisable scene or a sharp truth.
2. **The problem** — name what's really going on in this chapter's topic.
3. **The method here** — apply the relevant 5S step(s) to the topic, concretely.
4. **An example** — one short worked example with a *named* person.
5. **Boxes** (see §6) — at least one **Weekend Project**; add **Safety**, **Workshop Rule**,
   and a **Specs** box (hard numbers) where the topic is a build/handling one.

No `## Takeaways` recap — it restated the prose and was cut (§9). End the chapter on a box; the
**Workshop Rule** carries the one-line takeaway. Say less with more: cut filler, never pad to a
word count. One H1, H2 for the sections above, no deeper than H3.

## 6. Recurring Boxes (consistent labels & purpose)

| Box label | Purpose | Style |
|-----------|---------|-------|
| **Weekend Project** / Helgprojektet | The concrete do-it-now task for the chapter | Numbered steps, finishable in a weekend |
| **Workshop Rule** / Verkstadsregeln | The chapter's one-line takeaway, worth remembering | One bold sentence |
| **Specs** | Hard numbers a tradesman expects (heights, anchors, clearances, loads) | Tight bullets, real figures |
| **Safety** / Säkerhet | Safety / chemical / fire / lifting warning | Short, calm, specific |
| **Inherited & Hard** / Ärvt & svårt | The emotional/inherited-gear angle | Gentle, respectful |

Render boxes as a blockquote starting with the bold label, so they're visually distinct
and easy to lift into layout later.

## 7. Structural & House Rules

- One H1 per chapter; never skip heading levels; max depth H3.
- Swedish quotation style and dashes; no Oxford-comma habits carried from English.
- No numbered lists longer than 7 items — split instead.
- Tables: max 7 columns (JDS PDF rule), units in the header only.
- Each chapter file starts with a small status line: chapter no., title, draft date.
- Filenames: `chapter-NN-short-title.md` (EN) / `kapitel-NN-kort-titel.md` (SV), lowercase,
  hyphenated; å/ä/ö → a/a/o in Swedish filenames.

## 8. Self-Correction Checklist (run after every draft)

The `/write-chapter` skill must verify each item and fix failures before finishing:

- [ ] Reader addressed as **you** / **du** throughout (no impersonal main voice, no "ni")
- [ ] The five method words spelled exactly per §3 (EN 5S or SV), bolded on first use, right order
- [ ] Glossary terms (§4) used consistently — no drift, no brand names
- [ ] Metric units only
- [ ] Chapter shape complete: Hook → The problem → method applied → example → boxes (ends on a box, no Takeaways recap)
- [ ] At least one **Weekend Project** / **Helgprojektet** box, finishable in a weekend
- [ ] **Safety** / **Säkerhet** box present wherever chemicals, fuel, fire, electricity or lifting appear
- [ ] One H1, no skipped levels, max H3
- [ ] Length 850–2,200 words — dense, not padded; cut filler rather than pad to a floor
- [ ] Build/handling chapters carry a **Specs** box with real numbers (imperial, EN)
- [ ] No English loanwords where a Swedish word exists
- [ ] No non-Latin homographs (Cyrillic/Greek letters disguised as Latin) — `book-check.py` errors on these
- [ ] Tone: warm, no shame, no hype, finishable
- [ ] CHANGELOG updated for the chapter

## 9. Continuous Improvement

When a recurring style problem is found in a draft (a word that keeps drifting, a missing
box), do the JDS thing:
1. Fix the chapter.
2. Add the rule to this guide (§4 or §8).
3. Update the `/write-chapter` skill if the workflow allowed it.
4. Log it in the project CHANGELOG.

This guide gets stricter and better every chapter — never looser on **voice and quality**.
Calibration figures (like word bands) may be corrected when they prove wrong for the format,
and the correction is logged below so it is transparent, not silent.

### Improvement Log

| Date | Found in | Change | Reason |
|------|----------|--------|--------|
| 2026-06-05 | First 5 sample chapters | Chapter band 1,600–2,600 → **1,200–2,200** words | The book is an illustrated, box-driven project guide (Draganja-style). The five drafted chapters were expanded ~60–75% to ~1,300–1,530 words and read complete; the original band was set before the format was decided and was too high. `book-check.py` thresholds updated to match. Voice/structure rules unchanged. |
| 2026-06-05 | Kapitel 8 | Added **homograph guard** to `book-check.py` (errors on Cyrillic/Greek letters) | A Cyrillic "а" (U+0430), visually identical to Latin "a", had slipped into "lägga-tillbaka-testet" and survived several passes because nothing checked for it. Fixed the chapter, then taught the checker to catch any non-Latin homograph so it can never recur silently. |
| 2026-06-06 | Whole book | **English-first pivot.** English becomes the master edition; Swedish moves to `sv/`. | The author judged the English voice stronger. English also lets the method use the real **5S** terms (Sort, Set in Order, Shine, Standardize, Sustain) — a more authentic credibility hook than the translated Swedish S-words. `book-check.py`, `build-epub.py`, `build-cover.py` made language-aware (`--lang`); voice rules upgraded to vivid + named characters (§2). |
| 2026-06-10 | English edition (critique) | **Tighten & harden pass.** Cut all `## Takeaways` recaps; removed word-count padding; rewrote the build chapters (5,6,7) with hard specs; added **Specs** boxes; imperial units; floor lowered 1,200 → **850**. | A two-lens critique (book critic + master garage builder) found the book over-padded and short on builder credibility — generic where free content already wins. Fix = *less filler, more substance*: the Takeaways restated the prose (the Workshop Rule already carries the nugget), padding was added earlier only to hit a floor, and the build chapters lacked real numbers (anchors by substrate, French cleats, overhead-rack loads, mounting heights, bench height, lighting lumens, fuel/propane storage). The floor was lowered because dense-and-short is now the goal, not a length target. |

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-06-05 | N. Johansson | Initial style guide — voice, method words, chapter shape, self-correction checklist |
