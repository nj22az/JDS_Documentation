Draft or revise a chapter of *Städa i Garaget* (JDS-PRJ-GEN-001) — the Swedish
garage/workshop decluttering book — and self-correct it against the style guide.

## Input

The chapter to write or revise: $ARGUMENTS
(e.g. a chapter number from the outline, a title, or a path to an existing draft.)

## Before You Write — load the rules

1. **Read the style guide:** `projects/JDS-PRJ-GEN-001/02-manuscript/JDS-MAN-GEN-002_style-guide.md`
   — voice, the five fixed method words, glossary, chapter shape, boxes, the checklist.
2. **Read the outline:** `projects/JDS-PRJ-GEN-001/02-manuscript/JDS-MAN-GEN-001_book-outline.md`
   — find the chapter's place, its part (Del), and its working title.
3. **Skim 1–2 existing chapters** in `02-manuscript/chapters/` so voice and rhythm match.

## Write

4. Draft the chapter **in Swedish**, following the chapter shape (style guide §5):
   **Kroken → Problemet → Metoden här → Ett exempel → Boxar → Att ta med sig**.
   - Address the reader as **du**. Warm, concrete, finishable. No shame, no hype.
   - Use the five method words exactly: **Sortera, Systematisera, Städa, Standardisera, Säkra** —
     bold on first use, never paraphrased as labels.
   - Keep brand-neutral; metric units only; glossary terms consistent (style guide §4).
   - Include at least one **Helgprojektet** box. Add **Säkerhet** wherever chemicals, fuel,
     fire, electricity or lifting appear; **Verkstadsregeln** / **Ärvt & svårt** where they fit.
5. Save as `02-manuscript/chapters/kapitel-NN-kort-titel.md` (lowercase, hyphenated,
   å/ä/ö → a/a/o in the filename only). Start the file with the HTML-comment status line
   used by the other chapters.

## Self-Correct (this is mandatory — do not skip)

6. Run the checker:
   ```bash
   python3 scripts/book-check.py projects/JDS-PRJ-GEN-001/02-manuscript/chapters/<file>.md
   ```
7. **Fix every ERROR and every WARNING**, then re-run until the chapter reports `✓ clean`.
   - Short on words? Add real substance (a deeper *Problemet*, a second worked example, an
     extra box) — never padding.
   - Missing a section or box? Add it.
   - The checker is the floor, not the ceiling — also re-read against the style guide §8
     checklist by eye (tone, du-voice, no English loanwords), since those aren't all
     machine-checkable.

## Continuous Improvement (style guide §9)

8. If a style problem recurs that the checker *didn't* catch, improve the system, in order:
   fix the chapter → add the rule to the style guide → teach `book-check.py` to catch it →
   log it in the style-guide Improvement Log. The checker must get smarter over time.
   - If you change a calibration figure (e.g. the word band), log *why* — never loosen
     voice/quality rules silently.

## Finish

9. Update the project CHANGELOG: `projects/JDS-PRJ-GEN-001/CHANGELOG.md`.
10. Run `python3 scripts/jds-validate.py --quick` to confirm nothing broke.
11. Report the chapter path, its word count, and a one-line note on anything you changed
    in the style guide or checker.

## Important

- Swedish is the product; this skill, the style guide and the checker are English (QMS-000 §15).
- Never invent a method-word synonym as a label. The five S-words are the brand.
- A chapter isn't done until `book-check.py` says `✓ clean` **and** the §8 checklist passes by eye.
