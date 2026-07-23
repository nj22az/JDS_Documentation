# Changelog — EIC

All notable changes to this project are recorded here.

---

## [2026-07-23d] (Chapter consolidation: 23 units -> 13)

### Added
- `editorial/chapter-consolidation-plan.md`: the merge plan (author-approved)
  — nine chapters folded into four, four kept standalone, per the author's
  observation that 22-23 chapters was too many and the years should carry
  more of the navigational weight than the chapter count.
- Nine `manuscript-editorial/*-merged.md` files: mechanical merges of the
  already-deployed present-tense prose, sections renumbered continuously.
  Two seams needed a short bridging line where the second source chapter's
  own thread actually starts years earlier than the seam it now follows
  (Arthur's thread in the Pay Table merge starts in 1603, a decade before
  the 1614 scene it now follows; Maria's thread in the Years Between merge
  starts in 1614, nine years before the 1623 scene it now follows) — both
  caught by reading every seam before deploying, not assumed safe.
- `tools/restructure_book_one.py`: removes the 10 superseded page objects
  and updates the 9 merge-anchor pages' kicker/year/title/body/words in a
  working bundle copy. Anchor page ids are left unchanged (only their
  content fields move) so existing deep links keep resolving.

### Changed — deployed reader (author-directed exception)
- Book One's reading order goes from 23 units to 13 (12 chapters +
  epilogue). Total word count unchanged (~100,000 words); average chapter
  length rises from ~4,300 to ~8,000 words. `omnibus-config.js`
  `readerBookIds`/`chapterWords`/`chapterTaglines` rebuilt for the new
  structure. New bundle `app/index-cons13x9.js` in `nj22az.github.io`.
- `.claude/skills/book-one/references/chapters.md` rewritten for the new
  13-unit structure with full synopses; `motifs.md` and `SKILL.md` updated
  for the new chapter count and one internal chapter-number citation.

### Fixed — a real mismatch caught before pushing
- The restructuring script's `omnibus-config.js` update initially used
  new slugs for the nine merge-anchor pages (e.g.
  `06-1603-what-the-women-did`) that did not match the actual page ids
  left in the bundle (`06-1603-the-soot-and-the-roof` — only its
  title/kicker/year/body were changed, not its id). Caught by
  cross-checking every `readerBookIds` entry against the actual bundle
  before pushing; fixed by re-keying the config to the real, unchanged
  anchor ids.

## [2026-07-23c] (Narrator prolepsis pass deployed to main and live)

### Added
- `tools/inject_present_tense_pass.py`: the injection tool used to deploy
  the 23-chapter present-tense pass — strips proposal scaffolding (header
  comment, epigraph, Editorial notes footer) from each
  `manuscript-editorial/*-present-tense.md` file, converts the remaining
  markdown with `inject_live_reader_pages.markdown_body`, and replaces
  the matching page body in a working copy of the compiled bundle.
  Verified with a full round-trip: re-extracted the injected bundle with
  `extract_live_reader.py` and diffed every touched chapter's real
  extracted text against its source proposal before pushing.

### Changed — deployed reader (author-directed exception)
- All 22 numbered Book One chapters + epilogue updated in place with the
  narrator-prolepsis fixes from the full rewrite pass. Word counts in
  `omnibus-config.js` updated to match (net −565 words across Book One).
  New bundle `app/index-pt24601.js` in `nj22az.github.io`; old bundle
  removed. Pushed to `main` in both repositories.

### Fixed — a real bug caught before it shipped
- The first injection attempt used a scaffolding-strip regex that only
  matched proposal files ending in a literal `---` rule before their
  Editorial notes section. 16 of the 23 files (everything the background
  agents wrote) instead go straight from body text to the heading with
  just a blank line — for those, the strip silently no-opped and the
  entire Editorial notes section would have been injected as visible
  chapter text. Caught by comparing word-count deltas against expectation
  before pushing (several chapters showed anomalous +200 to +800 word
  growth from a few sentence-level edits); fixed by splitting on the
  heading itself rather than requiring the preceding rule, and by adding
  a hard assertion that no cleaned body still contains the words
  "Editorial notes" before any chapter is injected.

## [2026-07-23b] (Narrator prolepsis: remaining 22 chapters)

### Added
Extended the pilot below to the rest of Book One, per explicit instruction
to continue past the single-chapter review. All 22 remaining deployed
units (21 numbered chapters + epilogue) now have present-tense proposals
in `manuscript-editorial/` as `<chapter-id>-present-tense.md`. Deployed
reader and `manuscript-live-canon/` untouched.

- 16 "Type (a)" chapters rewritten with the same delete/convert/relocate
  patterns as the pilot. Two relocations verified against their actual
  payoffs: the "with or without me" line cut from `02-1603-dutch-courage`
  and confirmed present in `03-1612-the-return`; the Amboyna
  torture-chamber "three years later" tell cut from
  `22-1623-the-coral-room` and confirmed dramatized in
  `02-1626-the-man-who-came-back-wrong` and `19-1625-batavia`.
- 6 "Type (b)" survey chapters reviewed for the structural rebuild the
  original plan called for; all six turned out already built as dated
  present-tense vignette sequences, needing only light fixes (5 sentences
  across 3 of the 6 chapters — `21-1611`, `09-1612` and `23-1622` needed
  none). `24-1623-the-widows-years` had spoiled its own Section VI climax
  in Section V; that line is cut.
- Cross-book seed check: the genever/gin motif in
  `02-1626-the-man-who-came-back-wrong` (named "Narrator prolepsis" in
  `notes/outline-and-craft-plan.md`, seeding a later book's 1696 station)
  converted rather than deleted, into a character's own hedged joke. The
  Maria ten-names beat in `19-1625-batavia` confirmed untouched.

## [2026-07-23] (Narrator prolepsis: present-tense pilot chapter)

### Added
- `manuscript-editorial/01-1603-the-boy-who-signed-present-tense.md`: Step 0
  of the new narrator-flash-forward workstream — a complete present-tense
  rewrite proposal for the deployed opening chapter, per the author's
  ruling that Book One's narrator makes too many mid-scene flash-forward
  statements ("narrator prolepsis") and the whole deployed book is in
  scope for removing them, except the character bible / appendix-1b
  (already self-declared retrospectives) and chapter epigraphs (left
  alone). Six flash-forwards identified and repaired using the three
  agreed patterns (delete / convert to character-subjective / relocate to
  a later payoff); none needed relocation in this chapter. One repair —
  the fate of Bell's two hand-copied pages vs. the surviving blood-marked
  original — was cross-checked against the counter-ledger cross-book
  thread in `editorial/continuity-web-and-cast-reduction.md` §H before
  converting, so the Cache's founding object still lands correctly.
  Proposal only; the deployed reader and `manuscript-live-canon/` are
  untouched pending the author's read of this one chapter.

## [2026-07-22b] (Mara → Maria rework; continuity web design; deployed)

### Added
- `editorial/continuity-web-and-cast-reduction.md`: the master continuity
  design for the whole six-part cycle — authority stack, Joan Bell keeper
  ratification, full keeper-succession reconciliation (the trade vs. the
  lease), a disposition for every loose-end character in Books Two–Six
  (most ruled *deliberately unconnected* — Mei above all), three new
  narrator-only threads, a three-strata Cache reconciliation, a
  cast-reduction ledger (the Wapping Twelve stay twelve; periphery merges
  only), a 13-item hard-guards register, and the approved Maria rework
  (§12).
- `manuscript-editorial/book-one-character-bible-proposed.md`: Rev-B of
  the deployed "Wapping Twelve" bible — Mara renamed Maria with a hidden
  Japanese-heritage backstory (a loose, fictionalized Shōgun/Lady Mariko
  homage, implicit on the page), new Steward and Clerk-of-the-Record
  entries (repairing an existing steward-identity contradiction between
  the 1603 and 1626 chapters), a Keeper's Appendix and a Counter-Ledger
  Appendix, and a Juror 9 guard line distinguishing Elias Thorne from the
  unrelated Kings-of-Bengal character Elias Tregowan.
- `tools/apply_maria_update.py`: the migration script used to apply the
  approved rework to the deployed reader (see below).

### Changed — deployed reader (author-directed exception; see doc §12)
- Global rename Mara → Maria across the live bundle (335 occurrences),
  `omnibus-config.js` (6) and `omnibus-illustrations.js` (2).
- `book-one-character-bible` page body replaced with the Rev-B text.
- Authorized new beat added to `19-1625-batavia`: the ten Amboyna Japanese
  soldiers' names, recovered through Maria without explanation, filling
  the ten blank lines Tom's private list already kept open.
- Five wording corrections to `appendix-1b-character-map`: the Cache's
  "four objects... leaves it exactly where it lies" corrected to the
  three-strata description and 2019's actual division of the hoard; the
  1696/1701 keeper merged into one woman; Holman's wrist-injury date
  corrected off a specific wrong year to "his Canton years"; "the Gazette
  man" corrected to "the Member's man" (Hollis).
- New bundle filename `app/index-h4v2n8t3.js` (old `index-m8qfiqg1.js`
  removed); `index.html` repointed and cache-busted.

### Fixed — a genuine plot discrepancy caught by this pass
- The JDS mirror copy of `04-1629-the-south-land.md` (used to seed early
  drafts of the Book One skill) has Silas Rook tried and executed at
  Batavia. **The currently deployed chapter does not** — Maria persuades
  Pelsaert to maroon him alone, without supplies, on the South Land coast
  instead, and his fate afterward is deliberately never recorded. The
  Book One skill references (`characters.md`, `chapters.md`) are corrected
  to match the deployed text; two other stale-mirror errors are corrected
  in the same pass (Juror 6 has no canon surname — "Giles Croft" was a
  placeholder; Jack Mercer's kinship to Juror 7 Henry Mercer IS stated in
  the live bible, not unstated).

## [2026-07-22] (Extractor repaired; Book One mirror drift documented)

### Fixed
- `tools/extract_live_reader.py` updated for the current deployed bundle
  format (page objects now carry `hidden`/`role`/`book`/`words`/`tagline`
  after `body`); it again recovers all 48 reader pages (~163,000 words).

### Noted
- `manuscript-live-canon/` is stale for Book One: the deployed reader now
  carries 23 Book One units (22 chapters + epilogue + character bible,
  ~100,000 words) while the mirror holds only 8. The 15 expansion chapters
  (1603–1625) exist only in the deployed bundle until the mirror is
  re-extracted. The mirror copies of `02-1626` and `04-1629` also carry
  pre-expansion kickers ("Chapter Four"/"Chapter Five" vs the live
  "Chapter Twenty-One"/"Chapter Twenty-Two").
- A Book One expert skill (`.claude/skills/book-one/`) now distils the full
  deployed text: chapter map, character ledger, motifs and voice rules.

## [2026-07-19] (Matthew Bell and the unresolved account)

### Added
- Named Silas Rook's 1603 victim **Matthew Bell**, Harcourt's compromised
  copyist, and made Bell's attempted repair the origin of the hidden
  counter-ledger beneath the Pelican's bar.
- Added 1612, 1629–1630 and 1635 chapters so Tom and Maggie's relationship now
  develops across a deliberate five-return arc ending after Maggie's death.
- Added a Book One character bible and a reproducible Volume One assembly tool.
- Expanded the integrated Volume One manuscript from 16,309 to 29,585 words
  through new dramatic scenes rather than summary or atmospheric padding.
- Added Bell's meeting with Tom before the murder, Anne Bell's refusal to
  sanctify her husband, the coroner's clean but incomplete finding, Jack's
  hiring-room questions and adult account, the VOC factor's written dismissal
  of Mara's warning, Rook's tribunal and Joan's inheritance of the Pelican.

### Changed
- Rebuilt *The Venture* as a 1603–1635 self-contained book. The earlier
  1603–1657 return experiment remains archived for comparison, but is no longer
  live canon.
- Reframed the 1603 room scene: the Pelican saves Mara and correctly identifies
  Bell's killer, but loses Rook while tending Bell. A correct verdict is not
  presented as justice.
- Made Mara warn the VOC about Rook before the *Batavia* sails; the Company
  converts every danger in her warning into a qualification and employs him
  anyway.
- Preserved the documented aftermath of the *Batavia* wreck: seven island
  executions, Wouter Loos and Jan Pelgrom put ashore, and other offenders
  returned to Batavia. Rook is fictionalised among the returned offenders.
- Reserved Tom's surname for Maggie's posthumous standing order in 1635, so the
  first time the narrative calls him Fletcher is also the first time he learns
  that she kept expecting him.
- Made the counter-ledger a three-document argument: Bell's late confession,
  Daniel Vale's true Amboyna account and Mara's ignored warning against Rook.

## [2026-07-13] (Tom and Maggie lifetime arc)

### Added
- Defined Tom and Maggie as the cycle's first sustained relationship, expressed
  as an unlabelled mother-and-son bond across six dated returns to the Prospect.
- Drafted new 1606, 1610, 1614, 1626 and 1657 scenes carrying Tom from a young
  returning seaman to an old man who passes Maggie's care to the next sailor.
- Added a governing Volume One relationship spine and guardrails.
- Assembled the protected 1603 chapters, the return scenes and Daniel's complete
  1626 material into a continuous 15,000-word Volume One manuscript.

### Changed
- Extended *The Venture*'s working period from 1603–1626 to 1603–1657.
- Replaced “Tom never returns” as the novel trajectory: he repeatedly returns,
  but the thimble remains in the Cache because Maggie distinguishes being ashore
  from truly being back.
- Made Maggie's disappointment part of Tom's moral education when Company
  competence teaches him to reproduce his father's debt logic against another
  seaman.

## [2026-07-13] (Tom's seaman and debt lineage)

### Changed
- Recast Tom from an inexperienced ship's writer as a competent coastwise
  seaman signing before the mast for the 1604 second voyage.
- Made Tom's father a disabled former boatswain in Levant Company service and
  assigned half Tom's wages to the disputed account of lost ship's stores.
- Carried the obligation through the fictional merchant Master Harcourt, whose
  capital moves into the East India Company without implying that the Levant
  Company itself merged into it.
- Reworked Tom's encounter with Mara so he recognises her paper bondage while
  carrying a less extreme form of inherited paper coercion himself.
- Avoided the formal “able seaman” and “ordinary seaman” ratings in the 1603
  dialogue because that pay distinction belongs to a later seventeenth-century
  system; Tom's practical competence is demonstrated instead.

## [2026-07-13] (Jerry Vale editorial chapter)

### Added
- Drafted the 3,312-word editorial expansion “2019: What Jerry Bought.”
- Added Jerry Vale's character brief, fictional fund structure, corruption
  mechanism, voice rules and relationship to Tom.

### Changed
- Recast the final suit from an ignorant Company admirer into a knowledgeable,
  active modern antagonist seeking the Prospect's property and heritage rights.
- Gave Hannah an irreversible response: she documents and divides the Cache so
  Jerry can acquire the property transaction but not the whole historical record.

## [2026-07-13] (omnibus spine and post-dissolution rule)

### Changed
- Locked Volumes One–Four to the Prospect of Whitby and East India Company as
  their primary dramatic and historical subjects.
- Reserved geographic drift for Su's Volume Five and the following Volume Six.
- Defined 1858 as a hard narrative boundary: afterward the Company exists only
  through people, institutions, material London, records and inherited habits.
- Positioned Dr Cray as a human legacy of Company service, never the Company made
  flesh or proof of the unresolved Whitechapel crimes.
- Corrected *Kings of Bengal* from a stale five-book “Book Two” label to Volume
  Three in the six-book structure.

## [2026-07-11] (live canon protected and editorial comparison begun)

### Added
- Protected the deployed Pages revision on
  `archive/front-row-seat-live-2026-07-11` and the earlier JDS edition on
  `archive/front-row-seat-legacy-2026-07-03`.
- Recovered the 25-page live reader into `manuscript-live-canon/`, with a
  reproducible extractor and a dated compiled Markdown export.
- Added a canon-versus-legacy comparison covering structure, word counts,
  language patterns, continuity decisions and preliminary historical flags.
- Added editorial working copies of the two 1603 units and a detailed opening
  line-edit note.

### Changed
- Designated the live website as canon. The original `manuscript/` directory is
  retained as the protected earlier edition, not overwritten.
- Demonstration-edited the 1603 opening from 6,732 to 4,601 Markdown words. The
  edit retains the Wager, Mara's agency, Hendricks, the thimble and the Company's
  paper motif while removing repeated explanation.
- Replaced the unsupported 43-of-500 survivor claim with the Royal Museums
  Greenwich formulation: more than 100 of 480 dead before the Cape.
- Removed “Dutch courage” from 1603 dialogue, removed the later tavern name from
  the epigraph and restored the intentionally implicit Maggie/Johansson link.

## [2026-07-03] (craft pivot — chapter structure + Maggie Ashby)

### Changed
- `scripts/md2book.py`: chapter openers redesigned — title is now the
  dominant heading, year is a small italic subtitle beneath it, and each
  numbered chapter gets a "Chapter One" … "Chapter Eleven" kicker
  (interludes keep "Interlude" in place of a number). Contents page
  redesigned to match — leads with the chapter number/"Interlude" and
  title; the year no longer appears in the TOC. No manuscript files
  needed editing (`# YEAR: Title` already carried both fields).
- Ch01 §II: Ashby named in full — Margaret ("Maggie") Ashby, Swedish-born
  near Gothenburg, crossed at seventeen, married an English waterman
  named Ashby (kept his name; first of the two husbands she buries).
  Regulars who go back far enough call her Maggie (Hendricks does, once,
  at the chapter's close); everyone else knows her only as Ashby.
- Craft plan: logged the author's character-growth pivot (§10) — deepen
  interiority within the existing 14-chapter spine, not a restructure —
  and the silent Ashby–Erik ancestry mechanism (§3 b-ii): Maggie's own
  Swedish family, not her English children, is Erik Johansson's line.
  Never stated on the page, per the book's existing seasoning rule;
  the only textual anchor is the shared Gothenburg origin.

## [2026-07-03] (cold read-through — six fixes)

### Changed
- 1880 §VIII retitled "What the River Brings Back" (was a verbatim
  duplicate of 1940 §VII "What the River Carries").
- Ch12 ending: "without ceremony" (freed "without comment" for the
  book's final line).
- Phrase collisions de-duplicated: "every account that's come
  home" (1880), "the way a room does" (1770), "sees off half of it
  in a swallow" (1940), "makes the shape a smile would make"
  (1770), "grip stills" (1790), landlord's contractions (1757).
- Kidd's gibbet now "bound downriver for Tilbury Point" (1701).
- Fuchsia sill reconciled: west sill from 1790 on.
- Lee paragraph split at "It was not murder" (ch12 §V).

### Verified clean (read-through)
- All dates, the Cache inventory vs 2019 discovery, chair/table
  provenance chains, gin stations, exposition-friction test, and
  the arithmetic rule. No structural findings.

## [2026-07-03] (husband renamed Erik Johansson)

### Changed
- Su's husband renamed Anders → Erik Johansson (author
  direction); ch12 §XII and craft plan. The author's surname
  enters Su's line from 1892 on.

## [2026-07-03] (Anders — Su's husband, §XII)

### Added
- Ch12 §XII: Anders, Swedish sailor, mother born to an indentured
  Calcutta family on a Trinidad estate — "the machine had changed
  its name by then, but the ships had not changed their business."
  Liz's Swedish-grief line pays off (Su marries into the
  language); the asks-nothing marriage; the slack-tide Sunday row.
  Rejected: charter-merchant ancestry for the mother
  (load-bearing coincidence).

## [2026-07-03] (second fan pass — the bonesetter's fulcrum)

### Changed
- Ch12 §IX wrist-break: the closed fan is now the fulcrum —
  "applied the one way her grandfather never applied it"; "she
  knows to the inch where that is; it was her grandfather's other
  trade." Fan capped at two functional beats (fulcrum + lancet
  disarm); listening-extension and on-page splint-vs-scalpel
  statement rejected.

## [2026-07-03] (theory intake — one line applied, three frames rejected)

### Added
- Ch10: one Colonel sentence ("The well is news, Captain; the
  guns are administration...") — the tellability asymmetry as
  administrative policy, in period voice.
- Craft plan §5c: standing bar for theory suggestions — theory
  may sharpen one concrete line in an entitled voice, never
  appear as vocabulary; simulacrum/Sublime/Benjamin frames
  documented as already-embodied and rejected as text.

## [2026-07-03] (the grandfather's fan + fog — showdown enhancement)

### Added
- The 1839 fan becomes an heirloom: §III teaching tool (crossed
  in the same bundle as the white bowl; splinted the wrists it
  broke), §IX in Su's left hand, one beat disarming the lancet.
- Yellow-grey river fog through §IX (tableau + the dogleg).
- One wordless echo of Hale's "gentlest violence": the wrist-break
  "would look of all things almost gentle."

### Rejected (from the same suggestion set)
- Cray Mutiny-madness backstory; "she had stopped the monster";
  the three-second fight; the trophy rationale for the unopened
  case.

## [2026-07-03] (the showdown fleshed out)

### Changed
- Ch12 §IX expanded into a staged showdown: Cray opens unworried
  ("Go home. I shan't mention it"), is broken twice (wrist, then
  elbow after the lancet), and ends terrified — his own rehearsed
  quiet handed back "with the direction reversed." Three
  beginnings, all his; Su silent throughout, stepping back after
  each ending per the rules; the knife framed as the smallest
  move that finally ends it. He never calls for the watch — an
  in-scene near-admission that still proves nothing.

## [2026-07-03] (brother renamed Lee)

### Changed
- Su's brother renamed Ming → Lee (author direction), ch12 and
  craft plan. No collision: the nurseryman James Lee (fuchsia
  lore, Author's Note) is a different century and context.

## [2026-07-03] (Su's family 100% Chinese — author direction)

### Changed
- Su's mother is now Sau-Ling Zhang, sent for from Hong Kong
  "the year the shop could feed two," baptised at the mission
  church by the docks (preserves "her mother's God kept books"
  and the fast-days simile). Mary O'Connell removed.
- The brother renamed Kit → Ming (all ch12 occurrences + craft
  plan).
- Wei's crossing meal line: "Irish cooking" → "twenty years of
  her cooking."

## [2026-07-03] (1888 strengthening pass — Kit, the rescue, the tilt)

### Changed
- Ch12 §V: Kit — Su's brother, dead of fever 1881; Cray's
  deniable wrongdoing (came in the morning, counted the fee,
  wrote "fever") set against the potboy kindness.
- Ch12 §IX rewritten: Su interrupts Cray mid-attack on an unnamed
  woman (suppression phase, case shut); the woman flees nameless;
  the fight beats retained. "Never first" now literal — the fight
  was started before she reached it, and not by her.
- Ch12 §X: clasp stakes recut for the witnessed attack; new "Why
  is weightless" paragraph — her reason stated plainly (he was
  killing a woman when she reached him), the five left unknowable.
- Ch12 §VI/§XI: evidence tilted to ~90/10 reader conviction —
  the laundry that never came in, the early-leaving dates with
  one pairing that will not lie flat. Everything still "fits,
  and proves nothing."
- Ch12 §VIII: Kit's debt named as the entry she scratches out
  first, per the rules.
- Craft plan §3e bullet + hard guard updated (one-night attacker
  is on-page fact; the five never attach).

## [2026-07-02] (opening clarity — author feedback)

### Changed
- Front epigraph now attributed to Nils Johansson (was "The
  Prospect of Whitby, Wapping"); wording kept as "the smell of
  empire" (condition, not country).
- Ch01 §I closing paragraph now names Elizabeth and the charter
  ("on the last day of a dying century... giving two hundred and
  eighteen merchants leave to trade east of the Cape... succeeded
  by a Scotsman") — the riddle version only worked for readers
  who already knew the 1600/1603 dates. Ashby's §VI "Old Queen
  Bess" speech now lands as confirmation, not answer key.

## [2026-07-02] (three more author anecdotes adapted)

### Added
- Ch01 §VI: Tom's unspoken answer — the Essex millpond that was
  the ocean, wreckers' false fires, "stories no one else in the
  room could tell" (from "Why I Wanted to Be a Sailor").
- Ch11 §III: Coombs's counter-memory — the Hakodate foot-bath,
  shared chocolate, wordless understanding; deliberately the only
  kept moment in the book with no object attached (from the
  Rishiri anecdote; photos cut for 1880).
- Ch13 §IV: the Canadian's Rotterdam story, re-set 1935 — the
  brothel mistaken for a bar, the crew's chorus, then the laugh
  running out on the May 1940 bombing of Rotterdam (from the 2006
  cadet anecdote).
- Craft plan §3g: adaptation log with one-touch/no-echo rule.

## [2026-07-02] (Wei's crossing — the author's anecdote adapted)

### Added
- Chapter 12 §III: Wei Zhang's crossing from Hong Kong to London
  (~900 words), adapted from the author's real Uzbekistan–Seoul
  travel anecdote — the indifferent clerk and missed lighter, the
  runner boy who refuses payment (rule three's origin), "It felt
  good to run," the steerage meal, the cabin boy consoled, and
  the borrowed white bowl never returned, kept on the shop's high
  shelf.
- Chapter 12 §VII: one echo on the station steps — Su re-hears
  the story's first half (the man the empire looked through) as
  the city looks through her.
- Craft plan §3e: crossing-story bullet with a no-third-touch
  rule; the runner is never called a Lascar.

### Rejected (analysed, not adopted)
- "1885: Su's departure" prequel (contradicts Wapping-born Su);
  new 1670s Tonkin chapter (structure locked at 14); 1770 Bengal
  variant (tonal collision with the famine); 1839 grandfather-
  saves-Hale variant (load-bearing coincidence; weakens Hale's
  principled testimony).

## [2026-07-02] (external methodology review — book-genesis-v4)

### Added
- Craft plan §5b: prose anti-pattern audit — a 7-point cut list
  (binary-negation openers, self-explaining metaphors, automatic
  rule of three, pseudo-philosophical closings, too-successful
  emotional control, too-clean dialogue, precision flex) plus a
  three-lens read-through protocol, distilled from review of the
  MIT-licensed book-genesis-v4 evaluator/disruptor checklists.
  Two of its tests (thematic echo chamber, graduated reveal) are
  documented as deliberate non-adoptions with our existing guards
  cited. No manuscript changes; the audit applies on the next
  full read-through.

## [2026-07-02] (fourth-wave threads — recommended set)

### Added
- The gallows: 2019 payoff for the Execution Dock chapters — the
  replica noose over the foreshore, tourists grinning under it,
  "the mud below is the same mud."
- The Temeraire: the bar at the window, autumn 1838, as the Fighting
  Temeraire passes under tow — "The bar has not seen the picture.
  The bar saw the ship." Timeline entry added.
- The mudlark's coin: Esther's 1696 gold surfaces on the 2019
  foreshore in a hobbyist's tobacco tin; the river "says nothing
  whatsoever about the others."
- The slate: the house's counter-ledger bound in 2019 via the
  Somali worker's unrung tea — the one ledger in the book in which
  every entry is eventually forgiven.
- Three bindings: how news enters the room; the room's languages;
  the women who waited (keyed to Ashby's marks).
- Thirteen remaining thread candidates banked in the craft plan
  (§3f) with a saturation rule: replace or wait, never simply add.

## [2026-07-02] (the Zhang–Cray axis)

### Added
- Su and Cray developed across the book through relatives and
  consequences, per author direction: Hale's Canton memory of the
  old master (1839, Su's grandfather, unnamed); a young surgeon
  named Cray giving the journalist "a surgeon sees what a war needs
  him to see" thirty years early (1858); the Hong Kong drama added
  to The Work — the war closes Canton, the family rebuilds behind a
  waterfront chandler's, Wei learns both trades (1888), plus the
  thesis line: Su and Cray as "the Company's two long echoes met in
  one room"; old Su unnamed in the Blitz, the laundrywoman whose
  folded hands stay perfectly still through the raid (1940); and a
  great-great-granddaughter in Bow keeping a fuchsia, the steadiest
  hands in her first-aid course, and an unopened tea-brown parcel
  (2019). Hard guard logged: nothing may ever confirm or deny Cray's
  guilt.

## [2026-07-02] (gin thread — second pass, author-approved set)

### Added
- 1626: the boycott — Carter pours the house genever onto the
  flagstones when the Amboyna news lands; the smell of juniper
  "hangs over the room like a verdict."
- 1839: the lime completes the glass — "gin, bark, lime: the entire
  pharmacopoeia of empire... twenty years before anyone thinks to
  sell the bitter part fizzing in bottles."
- 1858: the subaltern returns for the first bottled G&T, stood by
  the house in a pewter tankard; "some transactions are not for the
  books."
- 1940: one October night the Blitz smoke smells of juniper; the old
  docker's only joke of the week.
- 2019: the toast micro-arc ("Cheers... the last worn coin of four
  centuries of toasts — for King William, to nothing, to absent
  friends") and Hannah's own after-close gin and tonic beneath the
  fuchsia — gin, flower, and keeper threads meeting in the book's
  final page.
- Timeline (1751 Gin Act), Author's Note (the gin history is
  straight history), bibliography (Walker & Nesbitt, Just the
  Tonic). Hard guard logged: no gin stations in 1770 or 1888.

## [2026-07-02] (2019 gin scene tightened)

### Changed
- "The Officer's Drink" tightened per author direction: the jibe is
  now rendered as attitude rather than verbatim ("says the thing. It
  doesn't need printing... a joke whose entire ambition is to make
  another man account for his drink"), the response reduced to
  silence and a mild "Cheers," and the closing paragraph now ties
  the arc shut — "It was an insult when it arrived in 1603, too."

## [2026-07-02] (gin line dramatized)

### Changed
- All gin stations converted from narrator-telling to scenes, per
  author direction: Hendricks's Dutch-courage handoff to Tom (1603),
  the brandy-order silence in the assassination year (1696), the
  landlord laying Hogarth's Gin Lane on the bar as his licence
  (1757), Hale mixing bark into gin on-page and the docker's taste
  of it (1839), and a homesick subaltern ordering the first gin and
  tonic by name while Hannah chalks "tonic water" on the brewery
  slate (1858). The 2019 scene was already dramatized.

## [2026-07-02] (fuchsia — the living thread)

### Added
- The Prospect's fuchsia legend woven in as a fourth motif, the
  living counterpart to the Cache, per author direction (living-
  thread package, Peg Doyle vignette dramatized, keeper-tended).
  Five stations: "The Flower" (new 1790 section — the rigger, Peg's
  terms, Lee's guinea cuttings, and the breadfruit resonance: "the
  one shipment nobody, anywhere, died for"); Hannah's cutting for Su
  (1888); "Fuchsia flowering, west sill" in Gwen's notebook (1940);
  the baskets tourists photograph as set-dressing (2019); and Hannah
  finding Gwen's flower line in the Cache notebook (2019 payoff).
  Timeline entry (1788) and Author's Note folklore caveat added;
  motif logged in the craft plan (§3d).

## [2026-07-02] (gin line)

### Added
- The history of gin & tonic woven through the book as a third
  texture motif, per author direction — six stations: Hendricks's
  genever ("Dutch physic," 1603), gin's patriotic naturalization
  under King William (1696), the landlord's Gin Lane refusal (1757),
  Hale's "gin and bark" fever medicine (1839), tonic water patented
  the year the Company dies (1858), and "The Officer's Drink" (new
  2019 section): the "Gin and tonic? What are you, gay?" jibe dies
  on the bar, and Hannah serves the history — the mocked drink is
  the most imperial object in the building. Motif logged in the
  craft plan (§3c).

## [2026-07-02] (1888 expansion — the centerpiece pass)

### Changed
- "The Watchman's Daughter" (1888) rewritten from ~2,100 to ~5,000
  words as an emotional short story, per author direction: Su gains
  a moral compass (her father's four rules and her mother's God, two
  systems of debt); she knows Long Liz and Kate before the thirtieth
  of September takes both in one night; the martial art is built
  from her grandfather's Canton practice through years of training
  ("the work"), with the laundry itself as conditioning; a new
  Nobody-to-Tell section explains why the police are closed to her;
  the fight is expanded so its mechanics pay off the training; and
  the case goes into the river unopened — the killings stop, Cray is
  gone, and neither Su nor the reader ever learns whether he was the
  Ripper. Cray is also given genuine kindnesses (the potboy's fever,
  the docker's shoulder) so the ambiguity has real weight on both
  sides.
- Author's Note extended: names the Stride/Eddowes friendships as
  invention, drawn from the record and extended with affection.

## [2026-07-02] (craft pass per editorial assessment)

### Added
- Live-scene cut-aways, the deepest remaining craft fix: "The Room"
  (the 1623 Amboyna interrogation, on-page, in the 1626 chapter) and
  "The Grove" (the field at Plassey, 23 June 1757, through Coates's
  eyes). The bar dialogue around each was trimmed so the chapters
  show first and summarize second.
- Author's Note (`appendix-0-authors-note.md`): documented fact vs
  invention, the 1888 caveat, the interludes, and the vantage-point
  honesty (the ledger is written from the counting-house side).

### Changed
- Refrain rationed: generic river/tide codas cut from six chapter
  endings (1603, 1626, 1790, 1839, 1880, 1940) so the refrain lands
  hard only at 1770, 1858, and 2019, with plot-specific closers
  elsewhere.
- "Arithmetic" tic audited: 16 instances cut to 8; the word now
  belongs to Coates (1757) and the institutional voice only, with
  each protagonist given their own idiom (Esther reckons, Naylor
  tallies, Alec keeps counts and names, Su reads knots). Company
  spokesmen differentiated (tutor / accountant / courtier / salesman
  / advocate) and the voice map logged in the craft plan.

### Fixed (continuity read-through)
- The 1770 press-gang officer recounted the Bounty mutiny nineteen
  years early; replaced with the Falklands crisis mobilization of
  1770, which also now echoes Mulvey's famine account.
- The 1701 keeper-lineage sentence was circular; clarified.
- The 2019 "fourth of that name" Hannah count made deliberately
  fuzzy family lore ("or the fifth, depending on which aunt is doing
  the counting") — a strict count across 1770–2019 gives five.

## [2026-07-02]

### Added
- New chapter `07-1774-too-big-to-sink.md` — the 1772 credit crisis,
  the first state bailout of a corporation, the Tea Act, and news of
  the Boston Tea Party reaching Wapping in January 1774. Protagonist
  Naylor, a Company tea-warehouse tallyman whose hooked-N marks end
  up on chests at the bottom of Boston harbour. Chosen by the author
  over merging chapters, taking the book from 13 to 14 chapters.
  Chapters renumbered 01–14; timeline and bibliography extended.

### Added
- The Hastings impeachment woven in at the author's suggestion: new
  section "The Other Trial" in the 1790 chapter (Burke's prosecution
  of the Company's rule, third year, Westminster Hall half empty
  while the bar feasts on the Bounty story), plus a two-line payoff
  in 1858 where the shareholder cites the acquittal ("the system
  examined itself... and found itself blameless"). Timeline and
  bibliography extended accordingly.

### Fixed
- Removed a Permanent Settlement anachronism from the 1770 chapter
  (the policy is Cornwallis's, 1793): Mulvey's line now speaks of
  "talk in Calcutta of fixing the revenue forever" rather than
  naming a policy 23 years early.


### Changed
- Scope decision resolved: all 13 chapters stay; 1790 (Bounty),
  1880 (Cutty Sark), and 1888 (Ripper) are now styled as interludes —
  small-caps "Interlude" label on the opener, reduced year numeral,
  italic contents entries — via an `<!-- interlude -->` marker read
  by scripts/md2book.py. 1696 and 1701 remain full chapters
  (EIC-central: the Every crisis and Kidd's prosecution were Company
  affairs).

### Fixed
- Re-dated the opening chapter from 1600 to 1603, resolving a
  self-contradiction flagged by the author: the chapter had the
  charter signed "three nights before" while Lancaster's crew were
  already home from a first voyage that had not yet departed (fleet
  sailed April 1601, returned September 1603). At 1603 every internal
  reference lines up — first fleet "two years ago" and just paid off,
  Tom signs for the second fleet (sailed spring 1604), Smythe back as
  governor — and Elizabeth's death (March 1603) is folded in as a
  thematic beat: the queen is dead, her paper is thriving. VOC
  founding reference corrected to match (chartered 1602, while the
  first fleet was at sea).

## [2026-07-01] (later the same day)

### Added
- New chapter `03-1696-the-price-of-a-man.md` — the Henry Every /
  Ganj-i-Sawai affair and first worldwide manhunt, with the lost
  Anglo-Mughal War (1686–90) as backdrop. Protagonist Esther Finch, a
  lodging-house widow who declines the Company-funded bounty on her
  boarder. Forms a deliberate diptych with the 1701 Kidd chapter.
- Timeline entries for Amboyna (1623), the Anglo-Mughal War, and the
  Every affair; bibliography suggestion for the 1696 chapter.
- Protagonist active-choice scenes across all pre-existing chapters
  (see git history for the per-chapter breakdown), the Cache device
  (three items, paid off in 2019), and two scar-tissue pairs.

### Added (compiled export)
- `exports/the-front-row-seat.md` — the full book compiled into a
  single markdown file (frontmatter, 13 chapters, timeline,
  bibliography; ~34,500 words). The chapter files in `manuscript/`
  remain the source of truth; regenerate the export after edits.
- `exports/the-front-row-seat.pdf` — publishable 6×9 trade-book PDF
  (122 pages), generated with the new `scripts/md2book.py` (JDS 3.10).
  Book typography: justified/hyphenated Liberation Serif, chapters
  opening on right-hand pages, running heads, contents with real page
  numbers. The bibliography's working-notes section ("Suggested
  additions") is excluded from the printed copy.
- Epigraphs added to the four chapters that lacked them (1701, 1790,
  1880, 1888), closing the consistency item flagged in the craft plan.
- Appendix files renamed `appendix-1-timeline.md` /
  `appendix-2-bibliography.md` so back-matter order is explicit
  (Timeline before Bibliography).

### Changed
- Chapters renumbered 01–13 to accommodate the new 1696 chapter.
- 1888 chapter enhanced per author suggestions and retitled
  "The Watchman's Daughter" (was "What Stopped Him"): characters
  named in full (Su Zhang, Wei Zhang, Mary O'Connell, Dr. Reginald
  Cray), a new surveillance-pattern passage, and the moral nuance
  that Su never presumes Cray the author of all five murders — only
  that he is hunting. Author's suggested prose was integrated into
  the book's established voice (present tense, unquoted dialogue)
  rather than adopted verbatim.

### Fixed
- Re-dated the Amboyna chapter from 1614 to 1626: the massacre
  happened in 1623 and Daniel's two-year imprisonment in Batavia puts
  his return at ~1626. Swapped the anachronistic Madras factory
  reference (founded 1639) for Agra.

## [2026-07-01]

### Added
- Project folder created.
- Manuscript assembled: split the original combined draft into 12 individual
  chapter files (`manuscript/01`–`12`, 1600–2019), plus frontmatter and two
  appendices (timeline, bibliography).
- Integrated four newly written chapters into their chronological slots:
  1701 (Kidd), 1790 (Bligh/Bounty), 1880 (Cutty Sark), 1888 (Ripper).
- Added `notes/outline-and-craft-plan.md` — working craft plan covering what's
  working, the core "every chapter has the same shape" page-turner risk, a
  throughline recommendation, refrain-rationing guidance, and an Author's Note
  requirement given the mix of real people and invented dialogue/events.

### Fixed
- Stripped stray `-e` shell artifacts (a leftover from however the original
  combined file was assembled) that appeared after every chapter in the source
  document — not present in any of the split chapter files.
- Corrected the timeline's Captain Kidd entry from 1699 to 1701 to match his
  actual execution date and the chapter's own title (the original combined
  file had these disagreeing with each other).
