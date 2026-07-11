# The Watchman's Daughter

| Field | Value |
|---|---|
| Working title | *The Watchman's Daughter* |
| Form | Standalone historical novel / illustrated novella |
| Status | Source isolation and character development |
| Principal character | Su Zhang |
| Place and time | Wapping, Limehouse and Whitechapel, chiefly 1888 |
| Canon baseline | `nj22az/nj22az.github.io@62d14ae19f8cbb3c86c75e83ff3a376e47977e2a` |

## Purpose

This project separates Su Zhang's story from *The Front-Row Seat* so that it can
grow into an independent book without altering the anthology or competing with
the Maggie/1603 work now under development elsewhere.

The book's central promise is simple: in the Ripper autumn, a nineteen-year-old
Chinese-English laundress trained by her father to end violence—but never begin
it—meets a respectable retired Company surgeon in a Wapping alley and must decide
what she is willing to know about the man she stops.

## Isolation rules

1. `source-canon/` is a provenance-locked packet copied from the protected live
   canon. It is never edited in place.
2. `manuscript-seed/` divides the 1888 chapter into workable units without
   rewriting it. It can always be regenerated with `tools/build_seed.py`.
3. New prose belongs in `manuscript-draft/` only.
4. Nothing in this project is automatically copied back into *The Front-Row
   Seat*. Backports require a separate editorial decision.
5. Maggie, Tom and the 1603 Johansson ancestry mechanism are outside this book.
   Erik enters through his relationship with Su, not as a payoff to Chapter One.

This pattern allows the anthology to remain the master vault while individual
characters become separate books with their own structure, pacing and market.

## Project map

```text
watchmans-daughter/
├── README.md
├── source-canon/          protected copies of all relevant source chapters
├── manuscript-seed/       the thirteen 1888 sections, separated but verbatim
├── manuscript-draft/      future standalone prose only
├── editorial/             architecture, source register and guardrails
└── tools/build_seed.py    reproducible splitter for the core chapter
```

The recommended planning range is 45,000–60,000 words. The existing material is
a strong novella-length foundation, but a standalone novel must add lived time
with Su, Wei, Sau-Ling, Lee, Liz, Kate and Erik rather than padding the Ripper
mystery.

The first new scenes now establish Su before the murder autumn. *Three Streets*
turns her childhood attempt to walk home from school into an affectionate but
dangerous dockside adventure; *Seven Winters* fixes Lee's death in 1881 and shows
her pride, humour, impatience and ambition. See `editorial/su-character-study.md`
for the governing character arc.
