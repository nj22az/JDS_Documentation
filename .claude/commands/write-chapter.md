Draft or revise a chapter of the garage/workshop decluttering book (JDS-PRJ-GEN-001) and
self-correct it against the style guide. The book is **English-first** (master:
*The Garage Reset*, `en/`) with a **Swedish edition** (*Städa i Garaget*, `sv/`).

## Input

The chapter to write or revise, and the edition: $ARGUMENTS
(e.g. "chapter 6 en", a title, or a path to an existing draft. Default edition: English.)

## Before You Write — load the rules

1. **Read the style guide:** `projects/JDS-PRJ-GEN-001/02-manuscript/JDS-MAN-GEN-002_style-guide.md`
   — voice, the five fixed method words per edition (§3), glossary, chapter shape, boxes, checklist.
2. **Read the outline:** `projects/JDS-PRJ-GEN-001/02-manuscript/JDS-MAN-GEN-001_book-outline.md`
   — find the chapter's place, its part, and its title.
3. **Skim 1–2 existing chapters** in `02-manuscript/<en|sv>/chapters/` so voice and rhythm match.

## Write

4. Draft the chapter in the chosen edition's language, following the chapter shape (§5):
   **Hook → The problem → method applied → an example → boxes → Takeaways**.
   - Address the reader as **you** (SV: **du**). Vivid but tasteful: a sharp opening, varied
     rhythm, the occasional first-person engineer aside, and **named** characters in examples
     (not anonymous "a man / a woman"). Warm, concrete, finishable. No shame, no hype.
   - Use the five method words exactly per §3 — EN: **Sort, Set in Order, Shine, Standardize,
     Sustain** (the real 5S; US spelling); SV: **Sortera, Systematisera, Städa, Standardisera,
     Säkra**. Bold on first use, never paraphrased as labels.
   - Keep brand-neutral; metric units only; glossary terms consistent (§4).
   - Include at least one **Weekend Project** / **Helgprojektet** box. Add **Safety** /
     **Säkerhet** wherever chemicals, fuel, fire, electricity or lifting appear;
     **Workshop Rule** / **Verkstadsregeln** and **Inherited & Hard** / **Ärvt & svårt** where they fit.
   - Keep cross-references accurate (chapter numbers, "the next chapter") and avoid repeating
     the front-matter hook beats verbatim.
5. Save as `02-manuscript/en/chapters/chapter-NN-short-title.md` (or `sv/chapters/kapitel-NN-...`,
   with å/ä/ö → a/a/o in the Swedish filename). Start with the HTML-comment status line.

## Self-Correct (mandatory — do not skip)

6. Run the checker for the right edition:
   ```bash
   python3 scripts/book-check.py --lang en <path>     # or --lang sv
   ```
7. **Fix every ERROR and WARNING**, then re-run until it reports `✓ clean`.
   - Short on words? Add real substance (deeper problem, a second example, an extra box) — never padding.
   - The checker is the floor, not the ceiling — also re-read against the §8 checklist by eye
     (tone, you/du voice, no homographs, no English loanwords in SV).

## Continuous Improvement (style guide §9)

8. If a style problem recurs that the checker *didn't* catch, improve the system, in order:
   fix the chapter → add the rule to the style guide → teach `book-check.py` to catch it →
   log it in the style-guide Improvement Log. Never loosen voice/quality rules silently.

## Finish

9. If the chapter is part of the production set, rebuild: `python3 scripts/build-epub.py --lang <en|sv>`.
10. Update the project CHANGELOG, then run `python3 scripts/jds-validate.py --quick`.
11. Report the chapter path, its word count, and any change you made to the style guide or checker.

## Important

- English is the master; the Swedish edition mirrors it. The skill, style guide and checker
  are English (QMS-000 §15); the manuscript editions are the product.
- Never invent a method-word synonym as a label. The five S-words are the brand.
- A chapter isn't done until `book-check.py` says `✓ clean` **and** the §8 checklist passes by eye.
