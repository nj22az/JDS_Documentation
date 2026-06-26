"""Dependency preflight for JDS Document Studio.

Reports which runtime dependencies are present so a first launch fails *loudly
and clearly* (PRO-012 §5 — prevent the error, give the way out) instead of a
stack trace deep in a request. Uses importlib.util.find_spec, so it never has to
import the heavy libraries just to check for them.
"""

import importlib.util

# import name -> (what it is for, pip package name)
DEPENDENCIES = {
    "fastapi": ("HTTP server", "fastapi"),
    "uvicorn": ("server runtime", "uvicorn"),
    "markdown": ("PDF: markdown → HTML", "markdown"),
    "weasyprint": ("PDF: HTML → PDF", "weasyprint"),
    "openpyxl": ("office workbooks", "openpyxl"),
}


def check():
    """Return {name: {present, purpose, package}} for every dependency."""
    report = {}
    for name, (purpose, package) in DEPENDENCIES.items():
        present = importlib.util.find_spec(name) is not None
        report[name] = {"present": present, "purpose": purpose, "package": package}
    return report


def missing(report=None):
    """Return the names of dependencies that are not installed."""
    report = report or check()
    return [name for name, info in report.items() if not info["present"]]


def format_report(report=None):
    """Human-readable preflight report."""
    report = report or check()
    lines = ["JDS Document Studio — dependency check", "-" * 38]
    for name, info in report.items():
        mark = "ok     " if info["present"] else "MISSING"
        lines.append(f"  [{mark}] {name:11} {info['purpose']}")
    gaps = missing(report)
    lines.append("")
    if gaps:
        lines.append("Install the missing packages:")
        lines.append("  pip3 install " + " ".join(report[n]["package"] for n in gaps))
    else:
        lines.append("All dependencies present — you're ready to launch.")
    return "\n".join(lines)


def main():
    print(format_report())
    return 1 if missing() else 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
