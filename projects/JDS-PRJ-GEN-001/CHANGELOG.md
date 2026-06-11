# Changelog — Städa i Garaget (Book Project)

> **JDS-PRJ-GEN-001** | Master Change Log

This file logs **every change** to every document in this project.

---

## Change Log

| Date | Document | Rev | Author | What Changed |
|------|----------|-----|--------|-------------|
| 2026-06-05 | JDS-PRJ-GEN-001 (README) | DRAFT | N. Johansson | Project created — charter, structure and status |
| 2026-06-05 | JDS-RPT-GEN-001 (Market Research) | A | N. Johansson | Initial niche-validation research — proven category, empty niche, real demand |
| 2026-06-05 | JDS-MAN-GEN-001 (Book Outline) | A | N. Johansson | Initial concept, 5-step method and 15-chapter outline |
| 2026-06-05 | JDS-MAN-GEN-002 (Style Guide) | A | N. Johansson | Initial style guide — voice, fixed method words, chapter shape, self-correction checklist |
| 2026-06-05 | scripts/book-check.py | — | N. Johansson | New chapter consistency checker (self-correcting backbone for /write-chapter) |
| 2026-06-05 | .claude/commands/write-chapter.md | — | N. Johansson | New /write-chapter skill — drafts a chapter and self-corrects it against the style guide |
| 2026-06-05 | chapters/kapitel-01..05 | draft | N. Johansson | Del 1 + Del 2 sample chapters drafted in Swedish (5 of 15); all pass book-check.py |
| 2026-06-05 | JDS-MAN-GEN-002 (Style Guide) | A | N. Johansson | Improvement log: chapter word band recalibrated 1600–2600 → 1200–2200 to match the illustrated project-guide format (voice/quality rules unchanged) |
| 2026-06-05 | chapters/kapitel-06..15 | draft | N. Johansson | Del 3, Del 4, Del 5 + Avslutning drafted — full 15-chapter manuscript complete, all pass book-check.py clean |
| 2026-06-05 | scripts/book-check.py | — | N. Johansson | Added homograph guard (errors on Cyrillic/Greek lookalike letters) after a Cyrillic "а" slipped into kapitel 8 |
| 2026-06-05 | JDS-MAN-GEN-002 (Style Guide) | A | N. Johansson | Improvement log: homograph guard added to checker and §8 checklist |
| 2026-06-06 | Whole project | — | N. Johansson | Book title changed from "Reda i garaget" to "Städa i Garaget" across all docs, chapters, registry, tooling and series titles |
| 2026-06-06 | frontmatter/, backmatter/ | draft | N. Johansson | Added title page, copyright, Inledning (hook), Om författaren, Ett sista ord |
| 2026-06-06 | scripts/build-epub.py, build-cover.py | — | N. Johansson | New build tools — assemble KDP EPUB and generate 1600×2560 cover from the manuscript |
| 2026-06-06 | 04-production/ | — | N. Johansson | Built KDP package: Stada-i-Garaget.epub + cover.jpg + amazon-listing.md + cover-brief.md + readiness-assessment.md |
| 2026-06-06 | frontmatter/03-programmet.md | draft | N. Johansson | Added explicit problem definition + 10-step program (the reader roadmap) as front-of-book section |
| 2026-06-06 | backmatter/00-checklista.md | draft | N. Johansson | Added tear-out 10-step checklist |
| 2026-06-06 | Listing, cover, Inledning, outline | — | N. Johansson | Foregrounded the 10-step program: cover kicker, Amazon description (numbered program), Inledning framing, outline §3a roadmap; rebuilt EPUB + cover |
| 2026-06-06 | Whole manuscript | draft | N. Johansson | **English-first pivot.** Swedish moved to `02-manuscript/sv/`; wrote full English master *The Garage Reset* in `en/` (15 chapters + front/back matter) with a more vivid voice, named characters, and the real 5S terms (Sort/Set in Order/Shine/Standardize/Sustain). All pass book-check --lang en |
| 2026-06-06 | scripts/*.py | — | N. Johansson | Made book-check, build-epub, build-cover language-aware (`--lang en|sv`); English is the default |
| 2026-06-06 | 04-production/ | — | N. Johansson | Built English KDP package: The-Garage-Reset.epub + cover-en.jpg + amazon-listing-en.md; renamed Swedish listing to amazon-listing-sv.md |
| 2026-06-06 | JDS-MAN-GEN-002, JDS-MAN-GEN-001 | A | N. Johansson | Style guide + outline updated for bilingual/English-first: EN 5S method words, vivid voice, EN section/box labels, improvement-log entry |
| 2026-06-06 | EN manuscript + write-chapter | draft | N. Johansson | End-to-end editing pass: fixed ch4 cross-reference (placing happens in Set in Order, not the literal next chapter), de-duplicated the Introduction/Program/ch1 hook beats, verified all cross-references and box coverage, confirmed no Swedish artifacts or doubled words; updated /write-chapter skill to bilingual/English-first |
| 2026-06-10 | JDS-RPT-GEN-002 | A | N. Johansson | Profitability plan — verified KDP rates, pricing decision ($6.99 eBook / $14.99 paperback, KDP Select), revenue scenarios, ship checklist |
| 2026-06-10 | 03-assets/images + scripts/build-diagrams.py | — | N. Johansson | Three B&W line-art diagrams (five-zone map, shadow board, 10-step strip); embedded in EPUB and print interior (program front matter, ch6, ch8) |
| 2026-06-10 | scripts/build-print-pdf.py, build-print-cover.py | — | N. Johansson | New paperback toolchain: 5.5×8.5 interior with mirrored margins, running heads, part dividers, recto chapter openings (EN 115 pp / SV 121 pp); wraparound 300-DPI print covers sized from real page count |
| 2026-06-10 | 04-production/ | — | N. Johansson | Full shippable KDP package rebuilt, both editions: EPUBs with diagrams + eBook covers + paperback interiors + print covers + listings |
| 2026-06-10 | EN manuscript (all chapters) | draft | N. Johansson | **Tighten & harden pass** from a critic + garage-builder critique: cut all Takeaways recaps and word-count padding; rewrote build chapters 5/6/7 with hard specs; added Specs boxes (anchors, French cleats, overhead loads, heights, bench, lighting, fuel/propane); imperial units; book-check floor 1200→850; style guide §3/§4/§5/§6/§8 + improvement log updated. Interior 115→109 pp despite added specs |
| 2026-06-10 | 04-production (EN) | — | N. Johansson | Rebuilt EN EPUB + interior (109 pp) + print cover (0.246 in spine) after the tighten/harden pass |
| 2026-06-10 | Positioning + EN units | draft | N. Johansson | **Corrected market priority to EU/Sweden primary, USA second.** English edition converted imperial → **metric-first (imperial in parentheses)**; build specs made **EU-aware** (600 mm stud centres, plasterboard, concrete/block, petrol/gasol, Swedish ~25 L petrol limit, powder extinguisher). Profitability plan reframed EU-first (SEK primary / USD secondary); README + style guide §4 updated. EN rebuilt |
| 2026-06-10 | Swedish primary edition | draft | N. Johansson | **Brought the Swedish (primary) edition to parity:** cut all Takeaways; added localized **Mått & fakta** spec boxes to ch 5/6/7/8/11/12 (metric, c/c 600 mm, gips, betong/Leca, gasol, MSB 25 L, pulversläckare); hardened ch7 with anchoring + French-cleat content; made `build-diagrams.py` language-aware and generated **Swedish diagrams** wired into the program, ch6, ch8; book-check sv drops the Takeaways requirement. Rebuilt SV EPUB (119 pp interior + 0.268 in print cover) |
