"""Reading and updating the JDS master document register.

The register (``jds/registry/document-register.md``) is the controlled list of
every document. Studio only ever *appends* a row under the correct category
section — it never rewrites existing rows, so the file's history stays clean and
diffs stay reviewable.
"""

import re

from . import config

# Matches a full register table row: | [JDS-XXX](path) | Title | Rev | Date | Status | Author |
ROW_RE = re.compile(
    r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|"   # doc_no, path
    r"\s*([^|]*?)\s*\|"                       # title
    r"\s*([A-Z]+)\s*\|"                       # revision
    r"\s*([^|]*?)\s*\|"                       # date
    r"\s*([^|]*?)\s*\|"                       # status
    r"\s*([^|]*?)\s*\|"                       # author
)

def read_text(path=None):
    """Return the raw register markdown."""
    with open(path or config.REGISTRY_PATH, "r", encoding="utf-8") as handle:
        return handle.read()


def parse_entries(registry_text):
    """Return a list of dict rows parsed from the register."""
    entries = []
    for match in ROW_RE.finditer(registry_text):
        doc_no = match.group(1)
        if not config.DOC_NUMBER_RE.fullmatch(doc_no):
            continue
        entries.append({
            "doc_no": doc_no,
            "path": match.group(2),
            "title": match.group(3),
            "rev": match.group(4),
            "date": match.group(5),
            "status": match.group(6),
            "author": match.group(7),
        })
    return entries


def _row(doc_no, rel_path, title, rev, date, status, author):
    return (f"| [{doc_no}]({rel_path}) | {title} | {rev} | {date} | "
            f"{status} | {author} |")


def append_entry(registry_text, category, doc_no, rel_path, title, rev, date,
                 status, author):
    """Return new register text with a row appended under `category`'s section.

    Raises KeyError if the category has no known section, and ValueError if the
    section heading is not present in the register.
    """
    section = config.CATEGORY_SECTIONS[category]
    lines = registry_text.splitlines()
    heading = f"## {section}"

    # Locate the section heading.
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == heading)
    except StopIteration:
        raise ValueError(f"Register has no section heading '{heading}'")

    # Within the section, find the last table row (last line starting with '|').
    # The section ends at the next '## ' heading or end of file.
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break

    insert_at = None
    for i in range(start + 1, end):
        if lines[i].lstrip().startswith("|"):
            insert_at = i  # track the last table row in the section
    new_row = _row(doc_no, rel_path, title, rev, date, status, author)
    if insert_at is None:
        # Empty section (only heading + blank/header): append before section end.
        insert_at = end - 1
        lines.insert(insert_at + 1, new_row)
    else:
        lines.insert(insert_at + 1, new_row)

    return "\n".join(lines) + ("\n" if registry_text.endswith("\n") else "")


def update_entry(registry_text, doc_no, rev=None, date=None, status=None):
    """Return register text with the row for `doc_no` updated in place.

    Only the named fields change; the link, title, and author are preserved.
    Raises ValueError if the document is not registered.
    """
    lines = registry_text.splitlines()
    for i, line in enumerate(lines):
        match = ROW_RE.search(line)
        if not match or match.group(1) != doc_no:
            continue
        f = list(match.groups())  # doc_no, path, title, rev, date, status, author
        if rev:
            f[3] = rev
        if date:
            f[4] = date
        if status:
            f[5] = status
        lines[i] = (f"| [{f[0]}]({f[1]}) | {f[2]} | {f[3]} | {f[4]} | "
                    f"{f[5]} | {f[6]} |")
        return "\n".join(lines) + ("\n" if registry_text.endswith("\n") else "")
    raise ValueError(f"{doc_no} is not in the register")


def write_text(registry_text, path=None):
    """Persist register markdown back to disk."""
    with open(path or config.REGISTRY_PATH, "w", encoding="utf-8") as handle:
        handle.write(registry_text)
