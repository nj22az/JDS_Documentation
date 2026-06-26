"""Edit and revise existing documents.

Completes the document lifecycle: create (creator.py) → edit → revise. Revising
is the error-prone part done by hand today — bump the revision letter, stamp the
date, add a history row, and keep the register in sync — so Studio does all four
as one atomic action.
"""

import re

from . import config, registry, revision


def _doc_number(text, fallback_name):
    """Find the document's JDS number from its metadata, else its filename."""
    match = re.search(r"\*\*Document No\.\*\*\s*\|\s*(" + config.DOC_NUMBER_RE.pattern + r")",
                      text)
    if match:
        return match.group(1)
    name_match = config.DOC_NUMBER_RE.search(fallback_name)
    return name_match.group(0) if name_match else None


def read_document(rel_path):
    """Return the document's content plus its number and current revision."""
    path = config.resolve_in_repo(rel_path)
    if not path.exists():
        raise FileNotFoundError(rel_path)
    text = path.read_text(encoding="utf-8")
    return {
        "path": rel_path,
        "content": text,
        "doc_no": _doc_number(text, path.name),
        "rev": revision.current_revision(text),
    }


def save_document(rel_path, content):
    """Overwrite a document's body. Path is constrained to the repository."""
    path = config.resolve_in_repo(rel_path)
    if not path.exists():
        raise FileNotFoundError(rel_path)
    path.write_text(content, encoding="utf-8")
    return {"path": rel_path, "bytes": len(content.encode("utf-8"))}


def revise_document(rel_path, author, description, new_status=None, date=None):
    """Bump the revision: stamp metadata, add a history row, sync the register."""
    if not (description or "").strip():
        raise ValueError("A change description is required for a revision")
    date = date or config.today_iso()
    path = config.resolve_in_repo(rel_path)
    if not path.exists():
        raise FileNotFoundError(rel_path)

    text = path.read_text(encoding="utf-8")
    new_rev = revision.next_revision(revision.current_revision(text))

    text = revision.set_metadata_field(text, "Revision", new_rev)
    text = revision.set_metadata_field(text, "Date", date)
    if new_status:
        if new_status not in config.VALID_STATUSES:
            raise ValueError(f"Invalid status '{new_status}'")
        text = revision.set_metadata_field(text, "Status", new_status)
    text = revision.append_history_row(text, new_rev, date, author, description)
    path.write_text(text, encoding="utf-8")

    doc_no = _doc_number(text, path.name)
    if doc_no:
        reg = registry.read_text()
        try:
            reg = registry.update_entry(reg, doc_no, rev=new_rev, date=date,
                                        status=new_status)
            registry.write_text(reg)
        except ValueError:
            pass  # not every document is in the register (e.g. templates)

    return {"path": rel_path, "doc_no": doc_no, "new_rev": new_rev, "date": date}
