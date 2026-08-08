#!/usr/bin/env python3
"""Assemble the protected natural-revision edition of Book One: The Venture.

This script is intentionally deterministic. It reads only repository sources selected by
`editorial/venture-natural-revision-manifest.md`, applies the approved section replacements
and continuity edits, strips editorial scaffolding, and writes one contiguous manuscript plus
a QC report. It does not touch live canon.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EIC = ROOT / "projects/literary/EIC"
ME = EIC / "manuscript-editorial"
OUT_DIR = EIC / "assembled"
OUT = OUT_DIR / "the-venture-natural-revision.md"
QC = OUT_DIR / "the-venture-natural-qc.md"

CHAPTERS = [
    ("Chapter One", ME / "01-1603-the-boy-who-signed-natural-opening.md"),
    ("Chapter Two", ME / "06-1603-what-the-women-did-natural-opening.md"),
    ("Chapter Three", ME / "08-1604-marias-passage-east-natural-revision.md"),
    ("Chapter Four", ME / "21-1611-the-return-merged.md"),
    ("Chapter Five", ME / "11-1613-the-pay-table-merged.md"),
    ("Chapter Six", ME / "book-one-ch06-the-same-ink-natural-revision.md"),
    ("Chapter Seven", ME / "15-1620-tom-at-surat-merged.md"),
    ("Chapter Eight", ME / "23-1622-the-years-between-merged.md"),
    ("Chapter Nine", ME / "20-1621-amboyna-merged.md"),
    ("Chapter Ten", ME / "24-1623-the-widows-years-present-tense.md"),
    ("Chapter Eleven", ME / "19-1625-batavia-merged.md"),
    ("Chapter Twelve", ME / "02-1626-the-man-who-came-back-wrong-natural-revision.md"),
    ("Chapter Thirteen", ME / "04-1629-the-south-land-natural-revision.md"),
    ("Epilogue", ME / "05-1635-last-orders-natural-revision.md"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n")


def strip_scaffolding(text: str) -> str:
    # Remove proposal/editor comments wherever they occur.
    text = re.sub(r"<!--.*?-->\s*", "", text, flags=re.S)
    # Remove trailing editorial-note appendices without disturbing scene separators.
    text = re.split(r"\n---\n\n## Editorial notes?\b", text, maxsplit=1)[0]
    return text.strip() + "\n"


def section_pattern(heading: str) -> re.Pattern[str]:
    return re.compile(
        rf"(?ms)^{re.escape(heading)}\s*\n.*?(?=^## [IVXLCDM]+\. |^---\s*$|\Z)"
    )


def replace_section(doc: str, old_heading: str, replacement: str) -> str:
    pat = section_pattern(old_heading)
    if not pat.search(doc):
        raise RuntimeError(f"Could not find section: {old_heading}")
    return pat.sub(replacement.strip() + "\n\n", doc, count=1)


def remove_section(doc: str, heading: str) -> str:
    pat = section_pattern(heading)
    if not pat.search(doc):
        raise RuntimeError(f"Could not find section to remove: {heading}")
    return pat.sub("", doc, count=1)


def roman(n: int) -> str:
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    out = []
    for value, symbol in vals:
        while n >= value:
            out.append(symbol)
            n -= value
    return "".join(out)


def renumber_sections(doc: str) -> str:
    count = 0
    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"## {roman(count)}. {m.group(1)}"
    return re.sub(r"(?m)^## [IVXLCDM]+\. (.+)$", repl, doc)


def drop_paragraph(doc: str, paragraph: str) -> str:
    p = paragraph.strip()
    if p not in doc:
        return doc
    return doc.replace(p + "\n\n", "", 1).replace(p + "\n", "", 1)


def clean_ch4(doc: str) -> str:
    replacement = strip_scaffolding(read(ME / "21-1612-falling-out-natural-revision.md"))
    doc = replace_section(doc, "## XV. With or Without Me", replacement)
    doc = doc.replace("A cut would have been the verdict.", "A cut would have meant Maggie had stopped honestly expecting him back.")
    for p in [
        "The counter-ledger does not pretend to the Company's exactness. The Company's book can give the month, wage and deduction while losing the person entire. Maggie's wood keeps the opposite truth: somebody sat here, ate, feared and did not come back. When memory can supply the name, the room says it. When memory fails, the cut does not acquire a convenient one.",
        "An honest blank is still an entry.",
        "The room begins keeping things that are not inside the fault. A stool can be an entry. So can a name said properly. So can the dark shape in the grain of the centre table, scrubbed so often that only the person doing the scrubbing knows where to look.",
        "Paper is not the only material that can hold an account.",
        "That is fortunate. Paper belongs too easily to the man with the locked room.",
        "The Company would call this enlargement. More room, more custom, better return from the same house.",
    ]:
        doc = drop_paragraph(doc, p)
    doc = doc.replace(
        "Maggie calls it six more men she can feed before somebody asks them to sign.",
        "The new length gives Maggie room to feed six more men when the house is full.",
    )
    return doc


def clean_ch7(doc: str) -> str:
    doc = remove_section(doc, "## I. The Letter Waiting")
    doc = remove_section(doc, "## V. Orphan's Work")
    letters = strip_scaffolding(read(ME / "15-1622-unsent-letters-natural-insert.md"))
    doc = replace_section(doc, "## X. The Letter Not Sent", letters)
    doc = doc.replace("# 1614–1622: Tom at Surat", "# 1617–1622: Tom at Surat")
    doc = re.sub(
        r"> \*\*1614–1620\*\*\n>\n> \*“A machine does not need to hate a man\. It only needs him to fit\.”\*\n>\n> — Tom Fletcher, Surat, 1620",
        "> **1617–1622**\n>\n> *“Read it again. The error is usually where everybody agreed too quickly.”*\n>\n> — Tom Fletcher, Surat",
        doc,
    )
    doc = drop_paragraph(doc, "Every correction strengthens the machine that required correcting.")
    doc = drop_paragraph(doc, "A man is nearly destroyed. A system learns. The system keeps the lesson longer than the man.")
    doc = doc.replace("## VI. The Lone Machine", "## VI. The Large Order")
    doc = drop_paragraph(doc, "The machine has learned from his refusal.")
    doc = drop_paragraph(doc, "Sometimes Maria stands behind the bar in dark silk, though Tom has never seen her in dark silk and has not seen her at all since the night she vanished. She puts the thimble beside Bell's page and bolts the door from within.")
    doc = drop_paragraph(doc, "Tom hears his own voice and his father's inside it. Beneath both, Maggie: do not call the taking a rescue. Beneath Maggie, Bell asking one quiet question across an unsigned page. Beneath Bell, a woman behind a door who has no English word available and a room deciding what her silence means.")
    doc = doc.replace(
        "Tom takes the doorway and watches the ship settle around the repair. He is forty-one. The scar aches before weather. His name stands beneath more Company orders than he can remember. Somewhere west, a woman he loves may still hate what he became. Somewhere east, other ledgers are closing around names he has not yet heard.",
        "Tom takes the doorway and watches the ship settle around the repair. He is forty-one. The scar aches before weather. His name stands beneath more Company orders than he can remember.",
    )
    return doc


def clean_ch8(doc: str) -> str:
    doc = doc.replace(
        "Maggie is not collecting evidence for Tom's acquittal. That is what paid-off men think at first.",
        "Paid-off men sometimes mistake her questions for a request to defend him.",
    )
    doc = drop_paragraph(doc, "The Company sends fair copies. The sea sends contradictions.")
    doc = drop_paragraph(doc, "Maggie trusts the contradictions more.")
    doc = drop_paragraph(doc, "Trust, Maria understands, is not one rope drawn tight across the sea. One cut would finish it. Trust is an intersecting web: each strand proves where another has held, and no single hand owns the whole.")
    return doc


def clean_ch9(doc: str) -> str:
    doc = doc.replace(
        "He is the only Englishman leaving Amboyna by water that week.",
        "He sees no other English prisoner put aboard with him that evening.",
    )
    doc = drop_paragraph(doc, "Truth is not being sought here. Truth is being transcribed backward.")
    return doc


def clean_ch10(doc: str) -> str:
    replacement = strip_scaffolding(read(ME / "24-1623-widows-years-1612-insert-natural.md"))
    doc = replace_section(doc, "## IV. The Name Maggie Spends", replacement)
    doc = drop_paragraph(doc, "She has learned the room's account. It is hers to bring back when another woman asks.")
    doc = drop_paragraph(doc, "Beneath Maggie's hand, behind the oak, Matthew's other account remains folded in the dark. It does not absolve him. Anne's household book does not condemn him. The two pages perform different work and neither is asked to finish the dead.")
    return doc


def clean_ch11(doc: str) -> str:
    doc = doc.replace("Both facts stand.", "")
    doc = drop_paragraph(doc, "Paper order is not justice. It is the only correction available in the room.")
    doc = drop_paragraph(doc, "He has corrected the machine for twenty years, one line at a time. He has never before heard his own side price a living man below a dead one and call the price patriotism.")
    doc = drop_paragraph(doc, "One long look. Not love. Recognition.")
    doc = doc.replace(
        "There is a room in London that reads accounts truly, she says. I have carried that fact twenty-two years. It is the most valuable thing I own, and I am spending it once. A tavern on Wapping Wall. The Pelican. When England lets him ashore, take him through that door and give him to the keeper.",
        "There is a keeper in Wapping who kept Bell's page when carrying it would have killed me, she says. A tavern on Wapping Wall. The Pelican. If she is still there, take him to her.",
    )
    doc = doc.replace(
        "Tom drinks. Juniper, fire, pine resin — his eyes water, and the woman in dark silk does not laugh, and for a moment the room is full of everyone who has ever handed this particular fire across this particular distance.",
        "Tom drinks. Juniper, fire, pine resin — his eyes water. The woman in dark silk does not laugh.",
    )
    doc = drop_paragraph(doc, "A deck, it turns out, has better manners than a court.")
    doc = drop_paragraph(doc, "It is not freedom. It is the next thing to it: being carried by people who keep true books.")
    doc = drop_paragraph(doc, "The man is the message. She has sent the room back one of its debts.")
    return doc


def clean_global(doc: str) -> str:
    doc = doc.replace("Maria de Sousa", "Maria Mori")
    # `Mara` was an abandoned early name. Replace only as a standalone character name.
    doc = re.sub(r"\bMara\b", "Maria", doc)
    doc = re.sub(r"\n{3,}", "\n\n", doc)
    return doc


def prepare(label: str, path: Path) -> str:
    doc = strip_scaffolding(read(path))
    if label == "Chapter Four":
        doc = clean_ch4(doc)
    elif label == "Chapter Seven":
        doc = clean_ch7(doc)
    elif label == "Chapter Eight":
        doc = clean_ch8(doc)
    elif label == "Chapter Nine":
        doc = clean_ch9(doc)
    elif label == "Chapter Ten":
        doc = clean_ch10(doc)
    elif label == "Chapter Eleven":
        doc = clean_ch11(doc)
    doc = clean_global(doc)
    doc = renumber_sections(doc)
    return doc


def demote_for_volume(doc: str, label: str) -> str:
    lines = doc.strip().splitlines()
    first_heading = None
    for i, line in enumerate(lines):
        if line.startswith("# "):
            first_heading = i
            break
    if first_heading is None:
        raise RuntimeError(f"No chapter heading in {label}")
    out = [f"## {label}", ""]
    for i, line in enumerate(lines):
        if i == first_heading and line.startswith("# "):
            out.append("### " + line[2:])
        elif line.startswith("## "):
            out.append("#### " + line[3:])
        else:
            out.append(line)
    return "\n".join(out).strip() + "\n"


def word_count(text: str) -> int:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    return len(re.findall(r"\b[\w’'-]+\b", text, flags=re.UNICODE))


def scan_hits(text: str, needle: str) -> list[int]:
    return [i for i, line in enumerate(text.splitlines(), 1) if needle.lower() in line.lower()]


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    prepared: list[tuple[str, str]] = []
    for label, path in CHAPTERS:
        prepared.append((label, prepare(label, path)))

    body = [
        "# The Venture",
        "",
        "*Book One of The Front-Row Seat*",
        "",
        "**1603–1635**",
        "",
        "---",
        "",
    ]
    for idx, (label, doc) in enumerate(prepared):
        body.append(demote_for_volume(doc, label))
        if idx != len(prepared) - 1:
            body.extend(["", "---", ""])

    manuscript = clean_global("\n".join(body).strip() + "\n")
    OUT.write_text(manuscript, encoding="utf-8")

    flags = [
        "Wapping Twelve",
        "sat as a court",
        "became a court",
        "Maria de Sousa",
        "Mara",
        "A cut would have been the verdict",
        "Both facts stand",
        "Not love. Recognition",
        "only Englishman leaving Amboyna",
        "1614–1622: Tom at Surat",
        "writes and sends",
        "sent to Maggie",
        "machine",
        "verdict",
    ]

    qc = [
        "# The Venture — Natural Revision QC",
        "",
        "Generated by `scripts/assemble_venture_natural.py`.",
        "",
        f"**Total words:** {word_count(manuscript):,}",
        "",
        "## Chapter word counts",
        "",
    ]
    for label, doc in prepared:
        heading = next((line[2:] for line in doc.splitlines() if line.startswith("# ")), label)
        qc.append(f"- **{label} — {heading}:** {word_count(doc):,}")
    qc.extend(["", "## Flagged phrase scan", ""])
    any_hits = False
    for needle in flags:
        hits = scan_hits(manuscript, needle)
        if hits:
            any_hits = True
            shown = ", ".join(str(n) for n in hits[:20])
            more = " …" if len(hits) > 20 else ""
            qc.append(f"- `{needle}` — {len(hits)} hit(s), line(s): {shown}{more}")
    if not any_hits:
        qc.append("No flagged phrases found.")

    qc.extend([
        "",
        "## Assembly assertions",
        "",
        f"- Maria Mori enforced globally: {'PASS' if 'Maria de Sousa' not in manuscript and re.search(r'\\bMara\\b', manuscript) is None else 'FAIL'}",
        f"- Chapter Seven date 1617–1622: {'PASS' if '1617–1622: Tom at Surat' in manuscript else 'FAIL'}",
        f"- Wapping Twelve removed: {'PASS' if 'Wapping Twelve' not in manuscript else 'FAIL'}",
        f"- Old court framing removed: {'PASS' if 'sat as a court' not in manuscript.lower() and 'became a court' not in manuscript.lower() else 'FAIL'}",
        f"- Old Amboyna sole-survivor claim removed: {'PASS' if 'only Englishman leaving Amboyna' not in manuscript else 'FAIL'}",
        "",
        "## Remaining editorial instruction",
        "",
        "Chapter Five still requires the planned 15–25% compression of routine shipboard material. The assembler deliberately does not automate that literary judgement. Remaining `machine` or `verdict` hits are candidates for the final prose pass, not automatic failures.",
        "",
    ])
    QC.write_text("\n".join(qc), encoding="utf-8")

    print(f"assembled: {OUT}")
    print(f"words: {word_count(manuscript)}")
    print(f"qc: {QC}")


if __name__ == "__main__":
    main()
