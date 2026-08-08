# The Venture — Step 18 Assembly Report

Status: assembly system complete on `agent/venture-natural-opening`; generated contiguous manuscript not yet materialised because connector-authored commits did not trigger the repository workflow during this session.

## What was completed

### 1. Final missing prose written

Created:

`manuscript-editorial/15-1622-unsent-letters-natural-insert.md`

This converts the revised seven-letter chronology from an editorial planning document into finished narrative prose.

The section now preserves the governing rule:

- seven letters written after the 1612 rupture;
- none sent;
- the 1622 `You were right` letter burned;
- six physical letters remain by 1625;
- the final Batavia letter is unsigned;
- Daniel Vale remains the eighth living letter carried through the Pelican door.

### 2. Deterministic Book One assembler created

Created:

`scripts/assemble_venture_natural.py`

The assembler reads the branch's selected manuscript sources and produces:

- `projects/literary/EIC/assembled/the-venture-natural-revision.md`
- `projects/literary/EIC/assembled/the-venture-natural-qc.md`

It never reads from or writes to deployed/live canon.

### 3. Approved structural substitutions encoded

The assembler now performs the following deterministically:

- Chapter One uses the natural Pelican opening and enforces `Maria Mori`;
- Chapter Two uses the new natural-opening continuation;
- Chapter Three uses Maria Mori's developmental passage east;
- Chapter Four substitutes the revised `With or Without Me` rupture;
- Chapter Six uses the historically corrected natural revision of `The Same Ink`;
- Chapter Seven removes the obsolete direct-1614 Surat opening and long duplicated parent-death section, changes the chapter span to 1617–1622, and inserts the finished unsent-letter prose;
- Chapter Ten substitutes the revised Anne/Maggie 1612 conversation;
- Chapters Twelve, Thirteen and the epilogue use their complete natural-revision replacements.

### 4. Deterministic prose reductions encoded

The assembly pass removes or rewrites several already-approved pieces of old scaffolding, including:

- notches explicitly described as verdicts;
- repeated `counter-ledger` explanations in Chapter Four;
- selected repeated `machine` declarations in Chapter Seven;
- the old `Not love. Recognition.` formula in Batavia;
- magical-Pelican language that says a room `reads accounts truly`;
- `a deck has better manners than a court`;
- the old Amboyna claim that Daniel is the only Englishman leaving the island;
- the old Tom-at-Surat date;
- abandoned `Maria de Sousa` / `Mara` naming in assembled prose.

### 5. QC generation encoded

The assembler calculates:

- total word count;
- chapter word counts;
- occurrences and line numbers for old framing terms;
- assertions for Maria Mori, the revised Surat dates, Wapping Twelve removal, old court framing and Amboyna survivor wording.

It deliberately does **not** automate Chapter Five's planned 15–25% compression, because that is a literary judgement rather than a safe mechanical operation.

### 6. Protected workflow added

Created:

`.github/workflows/assemble-venture-natural.yml`

The workflow is restricted to `agent/venture-natural-opening`. When an ordinary Git push changes the assembler or manuscript-editorial sources, it runs the assembler and commits only the two generated files under `projects/literary/EIC/assembled/`.

The generated-output commit does not recursively trigger the workflow.

## Execution result in this session

The workflow file and assembler were committed successfully, but commits made through the connected GitHub app did not start the push-triggered Actions workflow during this session. A temporary source trigger was tested and then removed so no junk file remains in the manuscript tree.

Therefore I am **not** claiming that `the-venture-natural-revision.md` currently exists on the branch.

The assembly definition is complete and reproducible; materialisation of the contiguous file remains the outstanding execution item.

## Branch state at report time

`agent/venture-natural-opening` is 32 commits ahead of `main` and 0 commits behind.

No deployed/live canon file has been overwritten.

## Step 18 editorial judgement

The assembly problem is now solved at the source-of-truth level: there is one explicit selection and transformation path from the approved chapter material to the final Book One text.

The remaining work after materialisation is Step 19:

- read the generated manuscript as one continuous novel;
- compress Chapter Five's routine shipboard middle by approximately 15–25%;
- remove any remaining repeated institutional metaphors caught by the QC scan;
- verify chapter transitions after the new Virginia chronology;
- run the final sentence-level prose pass before Step 20 editorial sign-off.
