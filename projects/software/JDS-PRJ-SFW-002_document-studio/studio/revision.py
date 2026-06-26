"""Revision sequencing and metadata bumping (JDS-PRO-002).

JDS revisions run A, B, C, … skipping the ambiguous letters I, O, Q, S, X, Z.
A DRAFT becomes A on first issue. This module is pure text-in/text-out so it can
be unit-tested without touching the repository.
"""

import re

from . import config, templates


def next_revision(current):
    """Return the next JDS revision letter after `current`.

    DRAFT / blank → A. Raises ValueError on an unknown letter or if the sequence
    is exhausted.
    """
    letters = config.VALID_REV_LETTERS
    cur = (current or "").strip().upper()
    if cur in ("", "DRAFT", "-"):
        return letters[0]
    if cur not in letters:
        raise ValueError(f"'{current}' is not a JDS revision letter")
    index = letters.index(cur) + 1
    if index >= len(letters):
        raise ValueError("Revision sequence exhausted (reached the last letter)")
    return letters[index]


def current_revision(text):
    """Read the Revision value from a document's metadata block, or None."""
    for line in text.splitlines():
        match = templates.META_ROW_RE.match(line)
        if match and match.group("label") == "Revision":
            return match.group("value").strip()
    return None


def set_metadata_field(text, label, value):
    """Return `text` with the metadata row for `label` set to `value`."""
    out, done = [], False
    for line in text.splitlines():
        match = templates.META_ROW_RE.match(line)
        if not done and match and match.group("label") == label:
            out.append(f"| **{label}** | {value} |")
            done = True
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def append_history_row(text, rev, date, author, description):
    """Append a row to the document's Revision History table.

    The table is the markdown table following the '## Revision History' heading.
    Inserts after the last row of that table.
    """
    lines = text.splitlines()
    try:
        start = next(i for i, l in enumerate(lines)
                     if l.strip().lower().startswith("## revision history"))
    except StopIteration:
        raise ValueError("Document has no '## Revision History' section")

    last_row = None
    for i in range(start + 1, len(lines)):
        if lines[i].lstrip().startswith("|"):
            last_row = i
        elif lines[i].startswith("## "):
            break
    if last_row is None:
        raise ValueError("Revision History section has no table")

    row = f"| {rev} | {date} | {author} | {description} |"
    lines.insert(last_row + 1, row)
    return "\n".join(lines) + ("\n" if text.endswith("\n") else "")
