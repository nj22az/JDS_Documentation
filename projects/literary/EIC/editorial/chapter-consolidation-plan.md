<!-- PROPOSED — design note for author review. Nothing here touches the -->
<!-- deployed reader, manuscript-live-canon/, or any chapter prose yet. -->
<!-- This is a structural plan only, per the author's request: "make a -->
<!-- plan... it needs to be able to give an overview by looking at the -->
<!-- chapters, now it's just so much." -->

# Book One chapter consolidation: 23 units → 13

## The problem

Book One currently reads as 22 numbered chapters + epilogue (23 units,
~100,000 words). Six of those are not scenes at all but multi-year
surveys stitched from roman-numeral vignettes (`21-1611`, `09-1612`,
`22-1614`, `23-1622`, `10-1623`, `24-1623`). A reader scanning the table
of contents sees 23 sequential "Chapter One" through "Chapter
Twenty-Two" labels spanning 1603–1635 with no sense, at a glance, of
which chapters are big scenic set-pieces and which are short connective
tissue — the chapter *count* obscures the actual shape of the book. The
years should be doing more of that work than the numbering is.

Average chapter length right now is ~4,300 words. Several adjacent
chapters already share a POV character, a location, or a converging
climax and are only separate because they were drafted in separate
sessions — not because the story needs the seam.

## The plan: merge by direct narrative continuity, not just proximity

Every proposed merge below satisfies at least one of: same POV
character across a direct time continuation, two threads converging on
one shared event, or a survey chapter whose span is fully swallowed by
an adjacent scenic chapter it's building toward. **No content is cut** —
this is re-homing existing (already present-tense) prose under fewer,
larger headings with continuous roman-numeral sections, not a rewrite.

| New # | New title (working) | Years | Folds in | Why |
|---|---|---|---|---|
| 1 | The Boy Who Signed | 1603 | `01-1603` + `02-1603` | Direct continuation — Ch2 picks up minutes after Ch1's climax, same room, same night. |
| 2 | What the Women Did | 1603 | `06-1603` + `20-1603` | Maria's escape and Anne's steward-search are the same night's aftermath, different addresses. |
| 3 | Maria's Passage East | 1603–1612 | `08-1604` + `09-1612` | One character's own continuous arc, Amsterdam to her own Bantam desk. |
| 4 | The Return | 1603–1612 | `21-1611` + `03-1612` | The counter-ledger survey is entirely the nine years building to Tom's homecoming; it has no independent climax of its own. |
| 5 | The Pay Table | 1613–1614 | `11-1613` + `14-1614` + `22-1614` | Jack's voyage out, the pay-table confrontation, and Arthur's parallel bureaucratic build-up all converge on one 1614 event. *Flagged below — this one runs long.* |
| 6 | Tom at Surat | 1614–1622 | `15-1620` + `17-1622` | Same character, direct time continuation, same underlying theme (competence vs. buried trauma). |
| 7 | The Years Between | 1614–1623 | `23-1622` + `10-1623` | Identical year range already; Maggie's waiting and Maria's spy network are the two halves of the same silence. |
| 8 | Amboyna | 1621–1623 | `20-1621` + `22-1623` | Daniel's own arc, direct continuation from build-up into the torture climax. |
| 9 | Batavia | 1623–1626 | `18-1623` + `19-1625` | Tom's Amboyna-aftermath paperwork chapter ends "travelling toward the word" — Batavia. Direct causal handoff, same character. |
| 10 | The Widow's Years | 1603–1623 | *(unchanged)* | Anne Bell's own chapter; kept standalone — she carries enough weight to earn it and doesn't share a climax with any neighbour. |
| 11 | The Man Who Came Back Wrong | 1626 | *(unchanged)* | Standalone. |
| 12 | The South Land | 1629–1630 | *(unchanged)* | Standalone — different cast (Rook, the wreck), no adjacent chapter to fold into. |
| — | Last Orders | 1635 | *(unchanged)* | Epilogue, unchanged. |

**Result: 12 chapters + epilogue = 13 units, down from 23.** Nothing
deleted; total word count unchanged (~99,500 words); average chapter
length rises from ~4,300 to ~8,000 words, which is a normal scene-length
for this genre and finally makes "which chapters are the big rooms and
which are hallways" visible from the years alone.

## The one judgment call: is #5 too big?

Folding `11-1613` + `14-1614` + `22-1614` together gives one ~17,000-word
chapter — the longest in the book by a wide margin, because it's a
genuine three-thread convergence (Jack's voyage, Tom's confrontation,
Arthur's parallel account, one shared 1614 climax). Two ways to go:

- **Keep it merged (recommended).** Three threads paying off on the same
  page is a real dramatic gain, not just consolidation for its own sake —
  and it still reads as one continuous "1613–1614" year-range rather than
  three.
- **Split Arthur back out.** Keeps `11-1613`+`14-1614` merged (still a
  clean two-thread convergence, ~14,000 words) and leaves
  `22-1614-arthur-in-the-chair` as its own short chapter. Result: 13
  chapters + epilogue = 14 units instead of 13.

## What execution actually involves (separate pass, not started)

This is mostly structural surgery on already-finished prose, not fresh
writing:

1. For each merge, concatenate the source chapters' body sections,
   renumber the roman numerals continuously, pick one title, one
   epigraph, and a spanning year range, and write a one- or
   two-sentence bridging line only where two formerly separate chapters
   now sit back to back without one (most already flow directly).
2. Update `readerBookIds`, `chapterWords`, `chapterTaglines` in
   `omnibus-config.js` to the new 13-entry list; retire the merged-away
   page ids.
3. Audit every other book's bible/appendix and this project's own
   `.claude/skills/book-one/references/` for anything that names a
   chapter by its old number or id (e.g. "Ch 11", "Ch 16") — several
   already do, including this very reference file — and update them.
4. Re-run the same round-trip verification used for the present-tense
   deploy (real extraction tool, word-count sanity check, JS syntax
   check) before anything touches `main` or the live reader.

This is a bigger, riskier change than the present-tense pass — it
restructures IDs and the reading order, not just prose inside existing
pages. Recommend the same discipline as before: proposal in
`manuscript-editorial/` first, your read of the new structure, then
deploy as a separate, explicit step.

## Open questions for you

1. Keep the 13-way merge as proposed, or split #5 (→ 14 units)?
2. Any of the titles above you'd rather change now, before the
   mechanical work starts?
3. Any merge here that instinctively feels wrong once you see it laid
   out — a pairing that reads fine as a table row but you know doesn't
   actually want to share a chapter?
