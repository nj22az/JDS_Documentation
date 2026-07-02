# Changelog — EIC

All notable changes to this project are recorded here.

---

## [2026-07-02]

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
