"""Suggested target folder for a new document.

So the user does not have to type a path by hand, Studio suggests where a
document of a given category belongs. It only suggests where it is *confident*
(PRO-012 §5.3 — make the right action obvious, never the wrong one); for
ambiguous categories it returns "" and the user chooses. The suggestion is
always editable, so the user stays in control.
"""

# Categories with a single, unambiguous home.
CONFIDENT_DIRS = {
    "QMS": "jds/quality-manual",
    "PRO": "jds/procedures",
}

# Template sub-type -> the folder under jds/templates/ that holds it.
TEMPLATE_SUBFOLDERS = {
    "RPT": "reports",
    "LOG": "logs",
    "TSH": "timesheets",
    "EXP": "expenses",
    "MAN": "manuals",
    "DWG": "drawings",
    "PRJ": "projects",
    "BLG": "blog-posts",
    "COR": "correspondence",
}


def suggest_target_dir(category, domain=None, template_type=None):
    """Return a repo-relative folder suggestion, or "" when not confident."""
    if category == "TMP":
        sub = TEMPLATE_SUBFOLDERS.get((template_type or "").upper())
        return f"jds/templates/{sub}" if sub else "jds/templates"
    return CONFIDENT_DIRS.get(category, "")
