# Changelog — EIC

All notable changes to this project are recorded here.

---

## [2026-07-08] (Holman elaborated — the whaleman's ledger)

### Changed
- **Ch 8 §VI "The Boston Man" deepened** (author-directed): Holman is
  now a harpooner-turned-mate — try-pot burn up the forearm, a
  scrimshawed whale's tooth of his wife worked in his pocket ("She
  says the nose is wrong. The nose was wrong four voyages ago; the
  rest of her has caught up since."), and a lapsed Nantucket Quaker's
  plain speech that surfaces once, at the port-closing peak ("Close
  that port and thee will starve my wife's mother before thee
  inconveniences one man in paint"). New exchange with the Company
  table's senior man carrying the section's quotable lines: "You can
  kill a whale, because a whale keeps its heart where a harpoon can
  reach it. I've seen no chart yet that marks the heart of a
  company."; the whale-line/knowing-when-to-cut speech ("Two crews,
  one line, and not a knife out on either end of it"); "We light
  London so London can read the Acts it writes against us"; and the
  grandchildren line before Friday's ebb. All prior beats intact
  (naming, cheapness-as-insult, point-of-paint, fair scales, the
  untaken word to the Long Wharf).
- Craft plan §3a 1774 row extended; compiled export regenerated.

## [2026-07-08] (the Wager reworked + the Boston man named)

### Changed
- **Ch 1 §IV "The Wager" rewritten** (author-directed; the dramatic DNA
  of The Sand Pebbles' confrontation borrowed, not copied): Rook now
  auctions Mara against a card debt and makes her serve the room;
  Tom's "She has heard enough" is answered with "Then buy her," his
  emptied pockets swept to the floor — "Not enough." Mara fights for
  herself (the jug of ale into Rook's eyes, the stool into his knee,
  the mug across his wrist), declining to be property rather than
  being rescued. Tom is losing when Maggie's single sentence — "Any
  man who still calls himself a sailor had best decide what sort of
  river he drinks beside" — raises the room: the old docker, the man
  with the killing cough, the tar-arguers, then more. Rook reads the
  arithmetic of a room on its feet and folds; Maggie buys the debt
  with one of Tom's coins, bought and witnessed. Nobody feels
  victorious; the closing papers/doors/locks beat is unchanged.
- **Ch 2 (Dutch Courage) §II**: Hendricks' post-mortem of the fight
  updated to the new version — he arrives after it, hears it from the
  room, and lands the chapter's thesis: "no room has ever once stood
  up to a paper."
- **Ch 8 §VI**: the American mate is now named — James Holman, out of
  Boston (author-chosen name; no collision elsewhere in the book).
- Craft plan §3a rows updated; compiled export regenerated.

## [2026-07-08] (five-part structure + foreword fixes)

### Added
- **Five named parts** grouping the existing chapters (nothing merged,
  nothing removed — author-directed organisation for readability):
  Part One "The Venture" (1603–1626), Part Two "The Gallows Years"
  (1696–1701), Part Three "Kings of Bengal" (1757–1790), Part Four
  "The Poppy" (1839–1888), Part Five "Afterlives" (1940–2019).
  Interludes trail the part whose era they belong to. Each part is a
  `NNz-part-*.md` divider file (`<!-- part -->` marker) with a title,
  year range, and a 2–3 sentence orienting note.
- `scripts/md2book.py`: part-divider support — right-hand part-title
  pages, small-caps part rows in the contents, parts never counted in
  chapter numbering.

### Fixed
- `scripts/md2book.py` silently dropped `00a-foreword.md` (it matched
  none of the three file categories) — the printed book had no
  Foreword. Now rendered after the contents page with its own TOC row.
- Foreword/Author's Note overlap trimmed (author-directed "keep both"):
  the Foreword loses its timeline pointer sentence — the Author's Note
  owns the accounting; the Foreword keeps the promise.

### Changed
- Compiled export regenerated (now includes the five part pages).
- README structure/status and craft-plan status updated; the
  considered-and-rejected chapter-merging option is logged in the
  craft plan (it would recreate the over-length problem the 1603
  split fixed).

## [2026-07-08] (Boston Tea Party — the American sailor + the war-era timeline)

### Changed
- **Ch 8 "1774: Too Big to Sink" — new §VI "The Boston Man"** (~900
  words; old §VI "The Marks" becomes §VII): an American mate off the
  Nantucket oil trade is in the room the night the news arrives. He
  corrects the room's picture (the tea ships — Dartmouth, Eleanour,
  Beaver — were American-owned and American-crewed; the tea was loaded
  in the Thames with Wapping hands under it; the raiders used the
  ships' own tackle, which is why they swept the decks), answers
  Naylor's "stale leaf" with the cheapness-as-insult argument, hears
  the port-closing prophecy as a man whose family eats off that port,
  and chooses Friday's ebb for home. Closing beat: Naylor asks after a
  Long Wharf chandlery without naming Ben; the offer of a word carried
  goes untaken — §VII's "he never learns" stands.
- **Timeline**: 1773 entry expanded (American ships, Thames loading);
  new 1775 (Lexington/press gangs), 1776 (Declaration), 1783 (Treaty
  of Paris — "the threepence collected in full, at the price of a
  continent"), closing the war-era gap between 1774 and 1788.
- Craft plan §3a: 1774 row's connective note extended.
- Compiled export regenerated.

## [2026-07-07] (1603 split into two chapters — readability)

### Changed
- **Chapter 1 (6,000 words, double the book's chapter rhythm) split in
  two at its natural seam**, per author direction, for readability:
  - **Ch 1 "1603: The Boy Who Signed"** (§I–IV, ~3,000 words): the rain,
    Maggie, the interrogation over the paper, and the Rook fight —
    ending on Tom bleeding at the bar, looking at the Company's paper,
    having learned what men do with a door when the lock is theirs.
  - **Ch 2 "1603: Dutch Courage"** (~3,000 words, sections renumbered
    I–IV): the Dragon's lads, Hendricks and the VOC warning, the
    thimble, and the morning after. New epigraph in the invented-
    broadsheet style ("The Hollanders have chartered a company of
    their own…" — Waterman's talk, Wapping, 1603).
  - Same continuous evening; the second chapter's "an hour later"
    opening deliberately carries across the break. No prose changed
    beyond the split, the section renumbering, and the new epigraph.
- Chapters 02–14 renumbered 03–15 (filenames only; titles unchanged).
  The book now has 12 numbered chapters + 3 interludes.
- README and craft plan updated (chapter counts, §3a table now has a
  row per 1603 chapter); compiled export regenerated; `md2book.py`
  needed no changes (kicker words run to "Sixteen") — test build OK.
- **Note:** the web reader (nj22az.github.io/the-front-row-seat) is
  built from a separate app source and must be rebuilt/republished to
  pick up the split.

## [2026-07-07] (manuscript re-synced with published revision — Maggie, Stockholm, Foreword)

### Changed
- **Ashby dropped from the book entirely** (author-directed): the keeper
  is Maggie on every page — ch01 (§II retitled "Maggie"), ch02, 1701's
  "the Maggie who first ran this place," 2019's "the marks Maggie cut,"
  and the Author's Note. No married surname remains in her biography.
- **Gothenburg scrapped** (author-directed): Maggie is now from a small
  fishing village on the coast **outside Stockholm**; Erik Johansson's
  father (ch12 §XII) comes from the same unnamed village. Per author
  direction, Gothenburg is not to appear anywhere unless the book one
  day engages the Swedish East India Company (headquartered there).
- Ch01 §II rewritten and expanded: Maggie's first husband is now Johan,
  a Swedish fisherman lost to illness, their son gone to the Swedish
  navy — the Johansson line stated once, narrator-only, as returning to
  this reach of the river generations later. Second husband remains the
  English waterman lost off Africa. Crossing re-dated: she came over as
  a grown woman, not at seventeen.
- Manuscript synced from the published reader (nj22az.github.io/the-front-row-seat),
  which had run ahead of this folder: revisions ported to ch01, ch02,
  ch03 (Gunsway coinage), ch04, ch05 (male landlord noted), ch06 (new
  river close), ch12 (expanded), ch13, ch14 (Bow descendant gains the
  Swedish sailor), Author's Note (new closing sentence on world
  history), and the timeline (new 1829, 1848, 1851, 1861, 1889 entries;
  expanded 1858).
- Craft plan §3(b-i)/(b-ii) rewritten to record the pivot and the
  updated Maggie–Erik mechanism (narrator-stated once, still invisible
  to every character); all remaining Ashby/Gothenburg references in
  notes and README corrected.
- `exports/the-front-row-seat.md` regenerated from the synced manuscript.

### Added
- `manuscript/00a-foreword.md` — the Foreword ("I am an engineer, not a
  historian"), previously live on the site but missing from the
  manuscript source of truth.

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
