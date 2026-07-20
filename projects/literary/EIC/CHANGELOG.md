# Changelog — EIC

All notable changes to this project are recorded here.

---

## [2026-07-20] (Book One 100,000-word sync and live-reader publication)

### Manuscript
- Replaced the stale flat 14-chapter JDS source with the current 48-page,
  six-book YAML manuscript tree.
- Book One, *The Venture*, now contains twenty-two numbered chapters plus
  *Last Orders* as its epilogue and verifies at exactly **100,000 words** by
  the inclusive manuscript count.
- Added `manuscript/publishing-manifest.json` as the stable reading-order and
  publication manifest. Filename and date sorting are explicitly rejected for
  Book One. The Wapping Twelve remains a hidden, deep-linked reference page.
- Synced the final Silas image in *The South Land*: wordless in the shallows,
  watching the departing *Sardam* with empty hands opening and closing as if he
  could tear the ship plank from plank.

### Reader and publication tooling
- Reworked `reader/tools/build_content.py` for recursive YAML pages, explicit
  manifest order, semantic embedded figures, generated six-book SEO, automatic
  word statistics, hidden-page metadata, and compiled Markdown output.
- Preserved the existing Safari language fallback and large-screen sizing work.
- Brought the production six-book contents and desktop spread layer back into
  the maintained JDS reader source, with generated configuration instead of
  hard-coded manuscript order and word counts.
- Imported and registered the ten production illustrations used by Chapter One
  and *The Watchman's Daughter*, raising the credited archive to 57 assets.
- Updated the React reader so hidden pages do not appear in contents or linear
  previous/next navigation.

### Verification
- Content build: 48 unique pages, 57 credited assets, Book One 100,000 words.
- Production Vite build completed successfully.

## [2026-07-06] (tightening pass — Chapters 4 onward)

Full consistency/chronology audit of Ch4–14 in the spirit of the Ch1–3 review.
**Verified clean:** mortality figures (43/500 = nine-in-ten, consistent), dates and
period facts (Clive's £234k, the 1773 £1.4m bailout, 342 chests, Bounty's 3,600 miles,
Lin's 20k chests, the 10.5% dissolution dividend), no modern finance terms in narration,
clean section numbering in all 14, and the running threads (fuchsia, gin/tonic, Su's
grandfather → Su, Cray 1858 → 1888). Ch4–14 held up far better than Ch1–3 did — only
two real fixes:

### Fixed
- **Keeper-line continuity (Ch5, 1757):** the bar's keepers are framed as a line of
  women (Maggie → the Hannahs; Ch14 "every keeper… in *her* head"), but 1757 has a male
  landlord whose maleness is core to his character. Marked him as the exception ("a man
  this time, which this house has not often been run by"), reconciling it without rewriting
  him or the Author's Note.
- **River-refrain de-duplication (Ch6, 1770):** Ch4 and Ch6 both closed on "the river
  doesn't keep score/count." Kept Ch4's (load-bearing for Kidd's "guilty vs merely useful"),
  varied Ch6's to the famine's own image ("carries the tenth million as lightly as the first").

### Offered, not done
- Deeper per-chapter prose line-editing (wordiness/over-explanation) on Ch4–14 — held back
  rather than churn prose that reads well; available on request per chapter.

---

## [2026-07-06] (editorial pass on Ch1–3 + Author's Note line)

From a detailed editorial review — tightening chronology and consistency, not adding.

### Author's Note
- Added the author's line: "World history belongs to all of us; no single room, least
  of all this one, holds more than a corner of it…" (closes the vantage-point paragraph).

### Ch1 (1603) — fixes
- **Casualty odds reconciled:** every "three in ten" → **nine in ten** (matches the
  repeated 43-of-500 figure; the old numbers contradicted).
- **Hendricks's age fixed:** "before your late Queen was a thought in her father's head"
  (would make him ~70+ in 1603) → "before your Company was so much as a thought in a
  merchant's head."
- **VOC timing:** "the year before last" → "last year" (chartered 1602, chapter late 1603).
- **Fight timing:** "spent an hour learning" → "one bad minute"; "one brave hour" → neutral.
- **Mara's origin** given one clean Portuguese-world route (Macau/Lisbon/sugar islands),
  reconciling the concept art without expanding her.
- Light trims of Wager redundancy; Maggie's backstory split for more air.

### Ch2 (1626) — fixes
- **Cotton de-anachronised:** the calico panic (Spitalfields riots, bonfires, Parliament
  bans — a 1690s–1720s event) rewritten to early-stage 1626 ("not enough yet to frighten
  Parliament… a quarrel for our grandsons"), keeping the India/Surat/cotton pivot.
- **Daniel's route clarified:** Batavia → Surat → home, cleaner.
- **"Paperwork" repetition reduced** (varied "charges/questioning" so the word keeps force;
  the Deposition section now carries the theme).
- **Maggie's age acknowledged** (~65 in 1626; "slower on her feet than she was a generation
  back, when a boy named Tom sat at this same bar").

### Ch3 (1696) — fix
- **Gunsway/Ganj-i-Sawai** made explicit (Gunsway = Wapping's worn-down coinage; the true
  name kept for the trial/those who've been east).

### Not done (author's call)
- Ch3 "meet Esther sooner" restructure — left §I intact rather than reshape a strong chapter.

PDF rebuilt (184 pp).

---

## [2026-07-06] (Foreword simplified + Chapter 2 additions)

### Changed
- **Foreword rewritten** in the author's own plain first-person voice (replacing the
  Jack London pastiche, which read "too weird"). Draws on the author's real writing
  (a Marseille bar, a Seoul airport runner, the lake he grew up beside) to frame the
  book as lived experience laid over real history; disclaims fiction/coincidence;
  points to the back-matter timeline of real events.

### Added — Ch2 (02-1626)
- **New §VI "The Deposition":** a Company clerk takes Daniel's testimony and sanitises
  it in real time ("They drowned us by inches" → "examined with some severity"),
  mirroring the Amboyna clerk of §IV — both empires' paperwork. Daniel signs; he has
  been "drowned twice."
- **Daniel named Daniel Vale;** Pryce's polite-menace line ("The dead are not helped
  by accuracy, Mr. Vale. The living are sometimes ruined by it").
- **Sharper Nell entrance:** she has chased the rumours (told he was dead twice, mad
  once, remarried once), comes anyway, and knows him by his hands before the face.
- **Carter's calculation** (grief sliding into "what can I do with it"; Daniel withdraws)
  and the **old Dutch skipper** who quietly leaves after the genever is poured (the
  river does not sort the guilty from the near-enough). Sections renumbered VI–X.
- Ch2 3,270 → 4,285 words; book PDF → 184 pp.

---

## [2026-07-06] (Ch1 "The Wager" fight interlude + reader SEO + character art)

Big Ch1 enhancement per author's detailed spec ("Enhance Tom"), plus reader SEO /
Safari-translation support and four author character illustrations. Ch1 4,380 → 6,037
words; PDF → 178 pp.

### Added — Ch1 (01-1603)
- **New §IV "The Wager":** a violent tavern interlude between Tom's paper (§III) and the
  Dragon's Lads. **Silas Rook** ("Rock"), a Cornish bruiser, brings in **Mara** (Lisbon
  via São Tomé) on a passage-debt and wagers sailors over her. Tom's turn from
  infatuation → shame (the bruised wrist) → resolve ("It isn't a wager"). An ugly,
  barely-won fight: Rook hits first, fights *through* pain (broken jaw does nothing), Tom
  wins by mechanics not strength (breaks Rook's hand on the bar edge, ale-slick-floor
  sweep). **Maggie ends it** (knife through the sleeve, buys the debt, shelters Mara).
  **Mara keeps agency** — asks Maggie not Tom for the back stairs; one look of recognition,
  not gratitude; gone by dawn. Quiet close: "Hold that to your mouth" + the paper/door line.
  The thimble (§VII) remains the true climax.
- Tom's rough millpond-boy fighting planted in §IV; §VII millpond-as-ocean turned into a
  callback so the same childhood carries both facets.
- Maggie contradiction (§II): takes the last farthing off who can pay, presses bread on who can't.
- Hendricks (§VI): a personal wound (brother **Pieter**, dead of Amboyna-fever raving of
  "punishment"); the old-familiarity "Margareta" exchange with Maggie; and a post-fight
  test that shrinks the fight against the Company ("the difference between a fight and a Company").
- Sections renumbered IV–VIII to accommodate the interlude.

### Added — reader (web app)
- **SEO:** Book JSON-LD (14 chapters), Open Graph / Twitter cards, canonical, sitemap.xml,
  and a crawlable in-shell fallback (title + blurb + linked chapter list). **Safari
  translation:** lang=en + real fallback text so Safari detects English and offers Translate.
- **Four author character images** wired into Ch1: Tom+Maggie (hero), Silas Rook (§IV),
  a Red Dragon hand (§V), Hendricks (§VI). Registered + credited in archive-assets.json.
- Portrait-hero treatment (contained-on-blur) already used for 1888 also applies here.
- `build_content.py` made repo-portable (parents[2] + EIC_ROOT fallback) and now emits SEO.

### Note
- Author supplied a full character-art set (Maggie, Tom, Hendricks, Vasco, Silas). "Vasco"
  is used as an unnamed Red Dragon sailor visual (no new named character, per the spec).
  The Maggie montage is held (a dedicated crop can be made on request).

---

## [2026-07-05] (web reader — React reading app + custom illustrations)

Built a static React (Vite + TS) reading edition to replace the plain multi-page
HTML export — Apple-style: serif reading body, adjustable text size, light/dark/auto,
cover + contents, reading-progress bar, keyboard nav. Live at
https://nj22az.github.io/the-front-row-seat/ (source: `reader/`).

### Added
- `reader/` — versioned app source. Manuscript stays the source of truth:
  `reader/tools/build_content.py` compiles `manuscript/*.md` → `content.json` and
  copies the canonical `exports/html/assets/` images into the app. `content.json`,
  `public/assets/`, `node_modules/`, and `dist/` are generated/ignored (see
  `reader/README.md` for the two-step build).
- Two author illustrations wired into the 1888 chapter:
  `liz-su-laundry.png` (Long Liz + Su at the laundry counter) as the chapter hero,
  with a new portrait-hero treatment (contained image over a blurred fill, so tall
  art isn't cropped); `su-cray-alley.png` (the Su/Cray confrontation) as an inline
  figure at §IX "The Alley". Both registered in `archive-assets.json` and credited
  to the author.

### Note
- A first showdown image (`suvscray.png`) supplied earlier was UTF-8-corrupted and
  unrecoverable; the author re-exported a clean PNG, now `su-cray-alley.png`.
- Homepage card on nj22az.github.io updated to "read online" copy.

---

## [2026-07-04] (Swedish geography corrected — Gothenburg removed)

Author correction: **Gothenburg is wrong and out of the book entirely.** Every
Swedish-origin reference now uses one phrase — **"a small fishing village outside
Stockholm"** — shared by Maggie/Johan (Ch01 §II) and Erik's father (Ch12 §XII), which
also gives the ancestry thread a clean rhyme. Specific real place-names (Stora Mellösa,
Lake Hjälmaren — the author's actual family region near Örebro) are deliberately kept
OFF the page as too obscure for a reader. Hard rule recorded in craft plan §(b-iii) and
in agent memory. Manuscript, compiled export, and HTML verified free of all three names;
`_versions/` snapshots and older log entries retain "Gothenburg" as historical record.
Also hardened `scripts/md2web.py` to skip AppleDouble `._*` files (was crashing the build).

---

## [2026-07-04] (ch13 — the author's father, carried by the docker; + age-bug fix)

Relocated the personal material (father's death) from Ch14 to **Ch13 (1940)** after a
full-book read-through judged it the best home (working-class/family/Blitz chapter; the
docker was a sketch). Adapted fully into period — no hospital, no Örebro. Preserved:
`_versions/13-...pre-father-beat-2026-07-04.md`. PDF 174 pp.

### Fixed (pre-existing continuity bug)
- The docker's age was self-contradictory: "sixty-five, seventy… fifty years working" vs
  "a docker since 1918, when he was fifteen" (~37) vs "a scar from the last war" (WWI vet).
  Reconciled to **~50, a WWI veteran** — which also lets his father die as a still-working
  man (the only age at which "clocked out of work and life" fits). Removed "sixty-five,
  seventy", "fifty years", "since 1918"; the four "old docker" refs → "the docker".

### Added (ch13 §V + §VII)
- §V: the docker's father — a lifelong docker who "clocked out of work and life in the
  same week" this September (the father's own truth, adapted), buried "in the Limehouse
  ground where the family has always gone." The son carries it unspoken. Deepens the docker
  from a sketch and rhymes with Gwen waiting on her son Peter.
- §VII: his silence looking east now carries the double loss — his father AND the docks his
  father gave his life to, both gone in one season; "the one mercy of going three weeks
  before he'd have had to watch it burn."

## [2026-07-04] (ch14 father beat — TRIED then REVERTED)

Author-directed, personal. A Ch14 §VII beat drawn from a family record (father's death,
21 Jul 2023) was added, then **reverted at the author's request** — he didn't want Örebro
named and wasn't happy with the present-day-frame placement. Ch14 restored exactly (174 pp);
`_versions/14-...pre-father-beat-2026-07-04.md` retained. The material is being **relocated
to flesh out an earlier chapter** (chapter + treatment TBD with the author). No name/location
to be used; the transferable core is the working-man's dignified death and "clocked out of
work and life at the same time."

## [2026-07-04] (full-book continuity read-through — 3 fixes, 2 flags)

Read-through of all 14 chapters + frontmatter + appendices, focused on the seams the
recent Ch1/Ch12/timeline work touched, plus the keeper line and the ancestry thread.
Verified consistent: the keeper line (Ashby → trained successors → Hannah; Ch04 confirms
it's trade-based, "not necessarily bloodline," so Maggie's Swedish-son-only rewrite does
NOT break it); the Cache items (thimble/Kidd-paper/1940-notebook) pay off in Ch14 §VIII;
Su reappears as the 1940 "laundrywoman from the Causeway, seventy-odd" (Ch13); dates vs the
timeline; chapters 03/05/07/08 untouched by any changed thread.

### Fixed (real inconsistency, introduced in the ch12 atmosphere pass)
- **Ch12 §III geography.** The grounding said the Zhang shop sat "a mile down the river from
  the Causeway and two streets from the Prospect" — contradicting the book's three "Causeway"
  references for the family (§V "off the Causeway", Ch13 "from the Causeway", Ch14 "a Causeway
  chandler"). Rewritten to place the shop **on the Causeway**, on "the same crook of the
  riverside that fed the Prospect its custom" — keeps the Limehouse-Chinese texture and the
  Prospect orbit without the contradictory mile. (Supersedes the ch12 atmosphere-pass log note.)

### Changed (thread-completion, discretionary)
- **Ch1 §II** prolepsis: "come back up these same river-stairs" → "come back to this same reach
  of the river" (Erik arrives at Su's Causeway shop, not the tavern's stairs).
- **Ch14 §VII** loop-close: the Bow descendant is now "a great-great-granddaughter of a Causeway
  chandler **and a Swedish sailor off the timber ships**" — lands the Johan→Johansson→Erik
  thread (planted Ch1, paid Ch12) in the finale, echoing Ch12's Erik. Trivially reverted.

### Flagged, NOT changed (pre-existing; author's call)
- **Chair vs table, short leg.** The wonky-furniture motif is a *chair* losing a leg in 1701
  (Ch04) and "the chair with the too-short back leg" in 1888 (Ch12), but a *table* with a short
  leg in 2019 (Ch14 §III), "the better part of two centuries." Likely two separate scar-tissue
  items (Ch14's action is pint-on-table), but the echo/timespan don't perfectly line up.
- **Two "Causeway chandlers."** Carter (English chandler off the Causeway, Ch02/Ch13 docker's
  ancestor) and Wei Zhang (Chinese chandler off the Causeway, Ch12). Parallel families, same
  trade and locale across ~250 years — reads as intentional resonance, but the shared phrase
  "Causeway chandler" could be conflated by a close reader.

### Build
- Export re-synced (3 chapters spliced); PDF rebuilt, 174 pp; fix verified absent/present in both.

## [2026-07-03] (timeline appendix — six additions incl. the Gin & Tonic)

Author caught that the Gin & Tonic (established in the 1858 chapter + Author's Note)
was missing from `appendix-1-timeline.md`. Added it and five other Wapping/London-
thematic milestones, in the timeline's house style (bold year, 1–3 thematic sentences).

### Added / expanded (appendix-1-timeline.md)
- **1829** — Peel founds the Metropolitan Police; forward-ties to the 1888 watch committees.
- **1848** — the junk *Keying* on the Thames; its crew's "Chinese boxing" displays echo the
  book's term and set up Su. **Date corrected from the author's 1851** — the Keying was in
  London 1848 (broken up by the mid-1850s), so it was NOT present at the 1851 Exhibition.
- **1851** — the Great Exhibition (kept as its own accurate entry; the Koh-i-Noor).
- **1858** (expanded) — India Act + the **Great Stink** (its actual year) + aerated tonic water
  patented → the **Gin & Tonic** born as an anti-malarial ration. NB: Great Stink belongs here
  (1858), which is why it was declined for the 1888 river scene (anachronistic there).
- **1861** — the Tooley Street Fire (Braidwood); thematic setup for the 1940 Blitz chapter.
- **1889** — the Great Dock Strike ("dockers' tanner"); working-class bookend after 1888.

### Verified
- Chronological order preserved; PDF rebuilt (174 pp); entries phrase-checked mss↔export.
- 1858 timeline entry now consistent with ch10 (1858) and the Author's Note.

## [2026-07-03] (ch01 Maggie Ashby enhancement + explicit Erik thread)

From the author's "enhance Maggie" draft, triaged (most of it Ch1 already had). Author
decisions: weathered/formidable portrait (no beauty-inventory); command-not-combat (no
martial beat — keeps Su singular); and the big one — the **Swedish son as the explicit
Erik Johansson ancestral link**, which rewrites Maggie's origin. Full before/after in
`notes/revision-log-ch01-maggie.md`. Preserved: `_versions/01-1603-...rev-A-pre-maggie-
2026-07-03.md` (+ export). PDF still 174 pp.

### Changed (ch01)
- §II portrait: cold-tide eyes, "a face men were careful around," and the command line
  ("the dangerous thing about her was never her hands…").
- §II biography **rewritten**: widowed-mother origin — first husband **Johan** (Swedish
  fisherman, died of illness, not the sea); a son who took the King's coin in the Swedish
  navy; she crossed to London a widow and married/buried **Ashby** (waterman lost at sea
  off Africa) as her **second** husband. Adds her Swedish boat-competence. Fixes the old
  husband-ordering wrinkle.
- §III: Tom is now "the age her own boy is… on whatever cold deck the Swedish crown keeps him."
- §VI: Ashby = second husband lost at sea (year fixed); Hendricks remembers her arriving "a
  widow… starting the back half of a life," not "young."

### Added (ch01)
- §II proleptic ¶ making the **Johan → Johansson → Erik** thread visible (book's forward-glance
  voice; echoes ch12 Erik's "sea-bag of salt-stiff shirts" entrance). Names the returning name,
  not the ch12 marriage.

### Superseded / reversed
- Prior canon "crossed at seventeen; Ashby the first husband" (CHANGELOG 2026-07-03 craft pivot).
- Craft-plan **(b-ii)**: the "silent / hard-guard, never state the Ashby–Erik link" rule is
  formally **reversed** at author direction; the thread is now explicit on the page.

### Declined (author choice)
- Young-beautiful portrait; Su-like "coiled power"/bare-handed beat; the "butcher/lamb" simile
  (collides with ch12 Cray; kept Ch1's "run off and join a circus" mother-look).

## [2026-07-03] (ch12 atmosphere & world-building — Rev C → Rev D)

From the author's 11-point enhancement list, triaged. Author decisions: keep the
disciplined fight (no zigzag); cold-menace river, NO Great Stink (anachronistic for
1888 + wrong register); Limehouse texture with the shop staying near the Prospect.
Already-present items (watch committees §I, class-impunity §VII) untouched. Full
triage + before/after in `notes/revision-log-ch12-supporting-cast.md` (Pass 3).
Preserved: `_versions/...rev-C-pre-atmosphere-2026-07-03.md` (+ export). Ch12 → 174 pp.

### Added
- §III: Limehouse-Causeway grounding — Wei one of a handful of settled Chinese
  shopkeepers around the Causeway (1856 sailors' home); shop "a mile down the river
  from the Causeway and two streets from the Prospect." Reconciles §V "off the
  Causeway" with the shop's Prospect-proximity.
- §IX: market-to-quiet contrast (Shadwell end of the Highway, naphtha flares,
  costermongers) + the **London Particular** — the pea-souper as coal-and-industry
  fog AND moral obscurity ("unmakes a city … hands you doubt in their stead").

### Changed
- §IX river-fall: cold-menace amplification ("black water … the winter ebb hard and
  cold as a drawn blade"; "indifferent to a pristine surgeon as to anything else it
  has ever been fed"). Elegiac close preserved; no sewer imagery.

### Declined (author choice)
- Zigzag fight rollercoaster (breaks Su's "smallest number of moves"); Great Stink
  grotesque river death (anachronistic; breaks the restrained ending).

### Deferred
- Marketing/positioning artifact (high-concept pitch, comps, upmarket framing) —
  offered as a separate `notes/` sheet, pending author go-ahead.

## [2026-07-03] (ch12 showdown reframe — Rev B → Rev C)

Author brief: Su is not a stalker — she was working and stumbled on the crime.
Cray attacks the witness, underestimates a laundress's strength; her indifference
breaks him and provokes a fatal, clumsy charge; his own momentum carries him into
the Thames. Author decisions: ending = full river-fall (no deliberate kill);
keep §V–VII suspicion, cut only §VIII stalking + §IX ambush. Full before/after in
`notes/revision-log-ch12-supporting-cast.md` (Pass 2). Preserved before this pass:
`_versions/12-1888-...rev-B-pre-showdown-2026-07-03.md` and
`_versions/the-front-row-seat.pre-showdown-2026-07-03.md`. Ch12 11,374 → 11,814 (+440).

### Changed
- §VIII retitled "Three Nights" → **"Never First"** and rewritten: she keeps the
  rule by NOT hunting (banks the heat, returns to the laundry). Planted: she now
  carries her grandfather's fan as a talisman (mirrors her father in the doorway),
  which is how the fan is on her in §IX without premeditation.
- §IX opening rewritten: the two-hour ambush, the pre-built plan, and the boning
  knife are gone. She's walking home from a linen delivery, takes the fog shortcut,
  and the dropped basket frees the victim.
- §IX fight rewritten: Cray moves first (seizes her collar, underestimates her);
  kept the fan-fulcrum "green wood" wrist-break and the two-disables spine. Did
  NOT add the ribs/knee escalation — held the "smallest number of moves" rule.
- §IX "afraid" beat expanded: her blankness is the explicit catalyst ("looked at
  like weather … will not even grant him the tribute of fear").
- §IX ending rewritten: deliberate knife-kill → **river-fall** (his charge, her
  sidestep, his momentum over the wharf lip; Woolwich/Princess-Alice callback).
- §X "The Clasp" reworked for no-body: culpability preserved ("something in her
  steered the empty air he flung himself into"); the CASE (not a body) goes to the
  river; Pass-1 Sau-Ling disposal folded in with adjusted evidence.

### Removed
- Su's premeditation arc (stalking / lying in wait) and the boning knife.

### Verified clean
- §XI (now quietly ironic — "a madman drowned in the river"), §XII ("took him in
  without ceremony" now literal), §V–VII suspicion retained, no orphan knife refs,
  no §IX/§X timeline overlap. Export re-synced and phrase-checked against manuscript.

## [2026-07-03] (ch12 supporting-cast deepening — Rev A → Rev B)

Editorial brief: bring Wei, Sau-Ling, Cray, and Liz/Kate up to Su's depth
(the "raise the waterline on the supporting hull" note). Deepen interiority
within the existing spine; no restructure. Full before/after in
`notes/revision-log-ch12-supporting-cast.md`. Original preserved verbatim at
`_versions/12-1888-the-watchmans-daughter.rev-A-pre-charwork-2026-07-03.md`.
Ch12 9,780 → 11,374 words (+1,594). Nothing deleted — all insertions/expansions.

### Added
- Ch12 §III: present-day "his hands now" ¶ for Wei — rope calluses, tar in the
  knuckle-seams, cold finding the old breaks his bonesetter father set with the
  same fan, grip a half-beat slow, wash-copper caulked chandler-fashion (oakum +
  tar, "the way he would have mended a hull").
- Ch12 §X: Sau-Ling's silent second disposal — she boils Su's bloodied clothes
  "past testimony" before the shop opens; laundress-expertise as agency,
  mirroring Su's river; pays off her §IV creed ("open, at a loss, on purpose").
- Ch12 §II: Kate's held promise — the slow song she only knows the *front* of,
  to be finished with the back half fetched from the Kent hop gardens.
- Ch12 §XII: the song's payoff as an echoing void — Su never learns how "the
  girl on the quay makes out"; "there are tunes she will only ever know the
  fronts of."

### Changed (expanded, original text retained inside each)
- Ch12 §IV (shutters): Wei's vulnerability beat — the stiff high bolt won't come
  for him; Su drives it home unasked; she registers wordlessly that he is aging
  and she is now the stronger (cross-stitched to Liz's grief-language idea).
- Ch12 §IV (Kate's bodice): Sau-Ling's spoken creed — the holy book kept at a
  loss "on purpose, forever," explicitly the opposite of Wei's must-balance
  rules (dramatizes the §III "two systems of debt").
- Ch12 §V (docker's shoulder): one line → full witnessed scene of surgical
  detachment — "the same nothing" the alley later confirms; plants the "flinch"
  the §VI Mutiny-dockworker line already pays off; doubles Cray's hands against
  Wei's ("reads a knot").
- Ch12 §II (Liz): grief-language exchange made mutual — Su gives back her own
  untranslatable word; "briefly and exactly, understood." Strengthens the §XII
  Swedish-marriage payoff.

### Verified clean
- §VI flinch payoff, §XII "accounts kept open on purpose," §III two-systems,
  §IX bruise-silence, fan-as-bonesetter, all dates/names/plot facts — no clashes.

### Deferred
- Book/PDF regenerate (`md2book.py`) and `exports/the-front-row-seat.md` refresh
  held pending author sign-off.

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
