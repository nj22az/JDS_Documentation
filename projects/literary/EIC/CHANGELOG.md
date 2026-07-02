# Changelog — EIC

All notable changes to this project are recorded here.

---

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
