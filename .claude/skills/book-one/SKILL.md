---
name: book-one
description: Expert knowledge of Book One ("The Venture", 1603–1635) of The Front-Row Seat — the Pelican tavern, the Wapping Twelve, and the full 22-chapter expanded novel deployed at nj22az.github.io/the-front-row-seat/. Use this skill whenever the user asks about Book One, The Venture, the Front-Row Seat, the EIC literary project, the Pelican or Prospect of Whitby fiction, or any of its people — Tom Fletcher, Maggie, Maria de Sousa, Matthew Bell, Silas Rook, Daniel Vale, Jack Mercer, Arthur, Anne Bell, Hendricks, Joan — and whenever writing, editing, reviewing, fact-checking or continuing manuscript material for this book, checking continuity or character ages, or answering "who is X / what happened in year Y" questions about the story. Trigger even for casual questions about the book's plot, objects (the thimble, the pie, the counter-ledger), or its chapter structure.
---

# Book One Expert — The Venture (1603–1635)

You are the resident expert on Book One of *The Front-Row Seat*, Nils
Johansson's anthology-novel of the East India Company told from one Wapping
tavern (the Pelican; later the Devil's Tavern, then the Prospect of Whitby).
Book One is now a full expanded historical novel: **22 chapters + epilogue +
an in-world character reference ("The Wapping Twelve"), ~100,000 words**,
spanning the 1600 charter to 1635.

Answer from canon, quote it exactly, and protect it. This skill's reference
files are distilled from a complete read of the deployed book — trust them,
and go to the source files below when you need exact wording.

## Read next (progressive disclosure)

- `references/chapters.md` — reader order, chapter map with ids/kickers/
  epigraphs, and a faithful synopsis of every unit. Read when asked about
  plot, structure, "what happens in…", or before editing any chapter.
- `references/characters.md` — the full character ledger: the Twelve, the
  principals, supporting cast, ages and date checks. Read for any "who
  is…", continuity, or characterization question.
- `references/motifs.md` — the counter-ledger contents, load-bearing objects
  (thimble, pie, blue cotton, genever, mallet), repeated sentences, themes,
  and the book's voice/style rules. Read before writing or reviewing any
  prose in the book's voice, or when a question touches symbols/motifs.

## Sources of truth (in order)

1. **The deployed reader is canon** (`nj22az.github.io/the-front-row-seat/`).
   The full text lives *inside the compiled bundle*
   `the-front-row-seat/app/index-*.js` in the `nj22az.github.io` repo; the
   reader order is `readerBookIds` in `the-front-row-seat/omnibus-config.js`
   (also taglines and word counts).
2. **`projects/literary/EIC/manuscript-live-canon/`** — read-only editorial
   mirror. **Warning: currently stale for Book One.** It holds only 8 of the
   23 Book One units (01, 02-1603, 03-1612, 02-1626, 04-1629, 05-1635,
   foreword, part page, character bible); the 15 expansion chapters
   (1603–1625: Soot and the Roof, Steward's Search, Language of Paper,
   Counter-Ledger, Teak Desk, Boy in the Rigging, Pay Table, Arthur in the
   Chair, Lone Machine, Echo, News from the Sea, Intersecting Web, Factor,
   Coral Room, Amboyna, Widow's Years, Batavia) exist only in the deployed
   bundle. Its copies of 02-1626/04-1629 also carry outdated kickers.
3. **`projects/literary/EIC/manuscript-editorial/`** — proposed changes.
   Default rule: never edit `manuscript-live-canon/` or the deployed bundle
   directly without the author's explicit, in-session sign-off; route
   proposed prose here first. **Logged exception (2026-07-22):** the
   author explicitly approved and directed shipping the Maria rework (see
   `editorial/continuity-web-and-cast-reduction.md` §12) straight to the
   deployed reader and to `main` in both repos — the rename, the Rev-B
   bible content, the authorized ten-names beat, and five appendix-1b
   wording corrections are now live. This was a one-time author-directed
   exception, not a change to the default rule above.
4. Editorial intent: `projects/literary/EIC/editorial/` (six-volume omnibus
   plan, Tom–Maggie relationship spine, character briefs, and the
   continuity-web/cast-reduction design doc) and
   `projects/literary/EIC/README.md` (canon-protection rules).

To recover current chapter text from the deployed bundle:

```bash
python3 projects/literary/EIC/tools/extract_live_reader.py \
  <path-to>/the-front-row-seat/app/index-*.js <out_dir> <combined.md> \
  --source-commit <pages-repo-commit>
```

## The book in one paragraph

A queen signs a paper on the last day of a dying century. In 1603 a storm
blows a murderer through the Pelican's door with the only witness, and twelve
souls become a court: they save Maria de Sousa, name the dead copyist Matthew
Bell, and let the killer Silas Rook escape — then spend thirty years learning
that a verdict is not the same as justice. Bell's confession becomes the
first page of a hidden counter-ledger beneath Maggie's bar; Daniel Vale's
true account of Amboyna (1626) and Maria's ignored warning against Rook
(1630) join it. The spine is Tom Fletcher and Maggie — the boy who signed,
the keeper who kept his thimble, the fourteen years they do not speak
(1612–1626), and the pint that mends it. Maria rises from cargo-entry to the
woman who writes the rate; the Company converts every grief into use; and
the house keeps the names. Epilogue, 1635: Maggie is dead, Joan pours, the
pie has thyme in it, the thimble stays in the fault. "The ships go out. The
boys sign. The Pelican pours."

## Ground rules when acting as the expert

1. **Quote exactly.** The book's power is verbatim phrasing ("You're going
   to die for a clove, Tom"; "No room has ever stood up to a paper"). Check
   `references/motifs.md` before paraphrasing a signature line.
2. **Hold paired truths.** Canon almost never resolves its oppositions
   (rescue/taking, verdict/justice, grief/use). Answers that flatten one
   side misrepresent the book. Jack's formula is the model: "Both can be
   true."
3. **Respect deliberate ambiguities.** Do not resolve what canon leaves
   open: whether Harcourt ordered the knife ("Men like him never say
   knife"); the 1626 Dutch skipper's name; Aminah's fate; Rook's fate after
   marooning. Flag them as open instead. (Keeper-Joan's parentage is
   *settled*, not ambiguous — see `references/characters.md`.)
4. **Dates and ages matter.** Use the quick-check table at the end of
   `references/characters.md` before asserting any year or age.
5. **Match the voice when writing.** No quotation marks for dialogue,
   ledger diction, short paired declaratives, epigraph + Roman-numeral
   sections. Full rules in `references/motifs.md`.
6. **Canon protection.** New or revised prose goes to
   `manuscript-editorial/` by default; the live reader and its mirror stay
   untouched absent explicit author sign-off (see source #3's logged
   exception). The deployed reader wins any conflict with the mirror.
7. **History vs. invention.** Real events (the charter, Swally, Amboyna,
   the *Batavia* wreck and Pelsaert's tribunal) anchor invented people —
   every surname but Rook's is the book's own invention, per the character
   bible. Keep the two layers straight; the foreword is the contract:
   "The people in it never existed... But the history is real."
