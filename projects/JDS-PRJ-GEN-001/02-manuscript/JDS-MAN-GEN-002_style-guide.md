# Reda i garaget — Manuscript Style Guide

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

Every chapter of *Reda i garaget* must read as if one person wrote it in one sitting:
same voice, same method words, same chapter shape. This guide is the single source of
truth. The `/write-chapter` skill drafts against it and **self-corrects** against the
checklist in §8 before any chapter is considered done.

## 2. Voice & Tone

- **Language:** Swedish throughout. Plain, modern, spoken-but-tidy. No English loanwords
  where a normal Swedish word exists.
- **Address the reader as "du"** — never "man" as the main voice, never "ni".
- **Warm and on the reader's side.** The garage is not a moral failing; it's an overflow
  valve. Never shame, never nag.
- **Engineer's authority, lightly worn.** Short declarative sentences. Concrete nouns
  (hyllplan, krok, märkning), not abstractions. Show the method works; don't oversell.
- **Encouraging, finishable.** Every chapter leaves the reader able to *do* something this
  weekend, not just think about it.
- **Avoid:** exclamation-mark hype, brand names, jargon, long subordinate-clause chains.

## 3. The Method Words (FIXED — never paraphrase)

The five steps are a fixed vocabulary. Always these words, always this order, always bold
on first use in a chapter:

| Step | Fixed Swedish label | Plain meaning |
|------|---------------------|---------------|
| 1 | **Sortera** | Keep / bin / move elsewhere |
| 2 | **Systematisera** | A place for everything (zones, shelves, boards) |
| 3 | **Städa** | A clean floor and bench as the baseline |
| 4 | **Standardisera** | Make the order the default with simple rules |
| 5 | **Säkra** | Keep it alive with a short routine |

Do not invent synonyms (not "rensa-steget" for Sortera as a *label* — "rensa" is fine as
an ordinary verb). The five S-words are the brand.

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

**Units:** metric only (cm, m, liter, kg). **Brands:** none — describe the *type* of
product (väggskena, perforerad tavla), never a manufacturer.

## 5. Chapter Shape (every chapter follows this)

1. **Kroken** (the hook) — 1–2 short paragraphs. A recognisable scene or a sharp truth.
2. **Problemet** — name what's really going on in this chapter's topic.
3. **Metoden här** — apply the relevant method step(s) to the topic, concretely.
4. **Ett exempel** — one short worked example or a real before/after.
5. **Boxar** (see §6) — at least one **Helgprojektet** box; add **Säkerhet** / **Verkstadsregeln** where relevant.
6. **Att ta med sig** — 3–5 bullet takeaways, each an action or a rule, not a summary of feelings.

Chapter length: ~1,200–2,200 words (see §9 for why this band, not longer). One H1 (chapter
title), H2 for the sections above, no deeper than H3.

## 6. Recurring Boxes (consistent labels & purpose)

| Box label | Purpose | Style |
|-----------|---------|-------|
| **Helgprojektet** | The concrete do-it-now task for the chapter | Numbered steps, finishable in a weekend |
| **Verkstadsregeln** | A one-line durable rule worth remembering | One bold sentence |
| **Säkerhet** | Safety / chemical / fire / lifting warning | Short, calm, specific |
| **Ärvt & svårt** | The emotional/inherited-gear angle | Gentle, respectful |

Render boxes as a blockquote starting with the bold label, so they're visually distinct
and easy to lift into layout later.

## 7. Structural & House Rules

- One H1 per chapter; never skip heading levels; max depth H3.
- Swedish quotation style and dashes; no Oxford-comma habits carried from English.
- No numbered lists longer than 7 items — split instead.
- Tables: max 7 columns (JDS PDF rule), units in the header only.
- Each chapter file starts with a small status line: chapter no., title, draft date.
- Filenames: `kapitel-NN-kort-titel.md`, lowercase, hyphenated, å/ä/ö → a/a/o in filename.

## 8. Self-Correction Checklist (run after every draft)

The `/write-chapter` skill must verify each item and fix failures before finishing:

- [ ] Reader addressed as **du** throughout (no stray "ni"/"man" as main voice)
- [ ] The five method words spelled exactly per §3, bolded on first use, right order
- [ ] Glossary terms (§4) used consistently — no drift, no brand names
- [ ] Metric units only
- [ ] Chapter shape complete: Kroken → Problemet → Metoden här → Exempel → Box → Att ta med sig
- [ ] At least one **Helgprojektet** box, finishable in a weekend
- [ ] **Säkerhet** box present wherever chemicals, fuel, fire, electricity or lifting appear
- [ ] One H1, no skipped levels, max H3
- [ ] Length 1,200–2,200 words
- [ ] No English loanwords where a Swedish word exists
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

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-06-05 | N. Johansson | Initial style guide — voice, method words, chapter shape, self-correction checklist |
