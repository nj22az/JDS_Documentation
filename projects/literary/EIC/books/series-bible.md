# The Front-Row Seat — Series Bible

**Status:** Working document. Every book in the series is written against this bible; everything a book invents gets logged here before it ships. The anthology (`../manuscript/`) is the series' master timeline and is always canon — novels expand it, never contradict it.

**The premise, one sentence:** One room in Wapping watches the East India Company from charter to afterlife; each book stands alone in its own era, and the district, the room, and a repertory of recurring personalities carry the reader between them.

**The model:** the Yakuza games. Kamurocho is the protagonist and the people are its weather; the reader learns one map, one hub, and a company of recurring roles, and the pleasure of each new entry is recognition — same streets, same slots, new faces, new century.

---

## 1. Canon and precedence

1. The anthology is canon. Where a novel expands a scene the anthology summarises, the anthology's facts (dates, names, outcomes, objects) bind the novel.
2. A novel may invent freely in the anthology's gaps (the years between chapters, the days around an evening, off-page lives). Every invention that could bind a later book is logged in §7 (New Canon Ledger) when the chapter ships.
3. The hard guards (§6) bind every book in the series, forever.

## 2. The Map (Kamurocho = Wapping)

Fixed, recurring locations. Books may add locations; added locations get logged and become available to every other book.

| Place | What it is | First appears |
|---|---|---|
| **The Prospect** (the tavern by the stairs; not yet named the Prospect of Whitby in early eras) | The hub. Every book's centre of gravity. The bar, the corner table, the west sill (fuchsia from 1788), the gap under the counter | 1603 |
| **Wapping Old Stairs** | Where the river and the street exchange people | 1603 |
| **Execution Dock** | The gallows at low tide; the crowd economy around it | 1701 |
| **Carter's chandlery** | Rope, tar, canvas; the Wapping trade families' anchor; later eras: other trades in the same premises | 1626 |
| **The Legal Quays / the warehouses** | Where the cargo lands; the tallymen's world | 1774 |
| **The Causeway, Limehouse** | The Zhang chandlery and wash-copper; the small Chinese settlement | 1888 |
| **The mission church by the docks** | Where crossings get baptised | 1888 |
| **Leadenhall Street (East India House)** | The enemy tower. Seen from Wapping, entered only when a book earns it | 1626 (Pryce comes *from* it) |
| **The river itself** | Not a witness. A river. Takes what it is given, answers nothing | every book |

## 3. The Repertory (recurring personalities, not bloodlines)

Every book casts **all seven roles** with new people. No role may be cast the same way twice. The narrator may know the pattern ("the room casts the same parts every generation; only the costumes change"); no character ever does.

| Role | The slot | Cast so far (anthology) |
|---|---|---|
| **The Keeper** | Runs the room; buys debts, keeps ledgers at a loss, trains the next | Maggie (1603–1626) → the young keeper (1701) → Bess (1770) → Martha (1839/1858) → Flo (1880/1888) → Vera (1940) → Hannah (2019) |
| **The Warner** | Right too early; disliked for it; usually foreign or otherwise outside | Hendricks (1603) → the Mutiny dockworker (1888) → the docker (1940) |
| **The Company Man** | Politeness as a ledger; the machine wearing a face | Pryce (1626) → Sillitoe (1701) → Cray (1888) → the suit (2019) |
| **The Bruiser** | Force as a first language; capable of respecting stated terms | Rook (1603) |
| **The One Who Refuses to Be Property** | Fights for herself, never for rescue | Mara (1603) → Esther Finch (1696) → Su (1888) → the Bermondsey welder (1940) |
| **The Haunted Returner** | Comes back changed; the truth arrives in his body before his mouth | Daniel (1626) → Coates (1757) → Harding (1858) |
| **The Appetite** | Grief and use in the same room; a merchant even in mourning | Carter (1626) → Aldridge (1770) → Pemberton (1839) |

## 4. The Threads (series-level, narrator-only)

Imported from the anthology's character map (`../manuscript/appendix-1b-character-map.md`), which is the authoritative statement. Summary: the Keepers (a trade, aunt to niece to daughter); the Cache (notches + four objects, found and left in 2019 — **closed set: no book may add or remove an object**); the Practice (the Canton thread); the Johansson line (never stated in any chapter); the room itself (scar tissue: Louie's chair, the lopsided table, the fuchsia, the gin thread — **never explained in-story, by anyone, in any book**).

## 5. Voice and craft standards (every book)

- The anthology's narrator: the room, close-third on the era's people, dry, ledger-minded, capable of flash-forward.
- Humanizing budget (calibrated 2026-07-10): em-dashes ≤ ~11/1000 words; "the way" only where load-bearing; trailing epigrams rationed to ~1/section; dialogue registers differentiated (only Keepers, Warners, and masters get aphorisms).
- Sensory grounding per the 1888 standard: every chapter runs on the body at least once per section.
- Epigraph device: every chapter head quotes one of our own invented characters, verbatim from that chapter's body.
- Build: `python3 scripts/md2book.py <book>/manuscript out.pdf`; parts marked with `<!-- part -->` files.

## 6. Hard guards (series-wide, permanent)

1. No character ever learns whether Cray was the Ripper; every clue fits and proves nothing.
2. The Cray/Heron question is never resolved in either direction; no character can even ask it.
3. The Johansson line is never stated by or to any character.
4. The Cache is a closed set (notches, thimble, true copy, testimony, notebook); no character who leaves an item knows of another's; found once, in 2019, and left.
5. Scar tissue is never explained in-story.
6. Su tells no one, ever.
7. No Gothenburg unless the Swedish East India Company enters the story. Maggie is from outside Stockholm.
8. Real victims (Stride, Eddowes) are drawn from the record and extended only with affection; no invented solution is ever presented as an answer.

## 7. New Canon Ledger

Everything the novels add that could bind later books. (Append entries as chapters ship.)

- **[Book One ch5, drafted]** Rook returns at noon the day after the wager, sober, wrist in a seaman's sling; pays four counted coins for the night's damage (refuses to pay for the mug: "a man doesn't pay for the shot that hits him"; Mara: "the mug was mine"); disclaims all claim on Mara without being asked. Maggie's daylight terms: Mara works for wages; the house serves him at a penny like anyone; the far table never serves him again. He accepts, drinks standing, and will drink there off and on for twenty years without once sitting at that table. The Bruiser role gains its rule: force respects stated terms — not virtue, bookkeeping. Chapter epigraph line: "Night debts are paid in daylight, or they are not debts. They are weather."
- **[Book One ch5, drafted]** The broken mug's glazed handle passes from Maggie to Mara over the counter ("Yours"); Mara keeps it in her apron pocket. Book-level object, not a Cache item.
- **[Book One ch2, drafted]** Mara's history: passage from São Tomé taken honestly and honestly meant to be paid; the debt paper (her name spelled wrong, the sum grown at every change of hands) sold twice before Rook won it at cards; she can read, and no holder of the paper ever asked. She counts doors before anything else. The room's certainty that she will be "gone before light" is her own rule too — and the night the house locks its doors with her inside and never tries her bolt is the night the rule meets its exception.
- **[Book One ch6, drafted]** Mara joins the bar on wages by December 1603 (slate pencil behind her ear, corrects the brewer's man's arithmetic); her packed bag is quietly unpacked in January. Maggie's first trained keeper-hand — the origin of the trade's teaching pattern (she is NOT the woman who trains the 1701 keeper; that trainer is a later trainee, born ~1610s).
- **[Book One ch4, drafted]** Mr. Cade, Company muster clerk at Philpot Lane (the Company Man role's junior echo): "Make your mark plain. The Company pays no blurred names." The articles hold the Company blameless for "whatsoever else God in His providence may send"; imprest money paid at a second table.
- **[Book One ch6, drafted]** Tom's farewell: "Mind the thimble" / "Mind your figures, writer"; the heel of bread from Mara — the same-weather transaction, no words. The fleet (four ships, spring 1604) passes Wapping on the ebb; Mara raises the jug a hand's width at the second ship; Hendricks bareheaded on his barge; Maggie stays behind the counter. Maggie's line: "Ships are loud going and quiet coming. It is the quiet you learn to listen for."
- **[Book One ch3, drafted]** Pieter Hendricks died in a lodging house off the Ratcliff road raving about the Company's islands and a thing he had watched but could not put into words; Hendricks sat with him four nights and never had the whole of it (the missing piece stays missing — series ambiguity, keep). Hendricks was on the stairs the day Margareta came off the timber ship and is the only man in Wapping who ever heard her whole name said properly.

## 8. The book slate

Each book stands alone; the anthology remains the connective spine. Working slate:

| # | Working title | Era | Keeper | Spine |
|---|---|---|---|---|
| 1 | **The Venture** | 1603–1626 | Maggie | A widow buys a debt, starts a ledger of notches, and decides what a room owes the people who drink in it |
| 2 | **The Gallows Years** | 1696–1701 | the young keeper | Two hangings, two liars with good reasons, and the first objects the building keeps |
| 3 | **Kings of Bengal** | 1757–1790 | Bess | The Company becomes a state; the bar hears it happen in wages and missing men |
| 4 | **The Poppy** | 1839–1858 | Martha | The drug ledger and the Mutiny; the machine dies and changes nothing |
| 5 | **The Watchman's Daughter** | 1880–1892 | Flo | The Su novel: the practice, the autumn, the alley, the marriage — the anthology's centerpiece at full length |
| 6 | **Afterlives** | 1940 / 2019 | Vera, Hannah | The Blitz vigil and the finding; the series' close of accounts |

Sequence of writing ≠ sequence of eras; Book One first, then whichever era the author wants most (Book Five is the natural second — the material is deepest and the author's favourite).
