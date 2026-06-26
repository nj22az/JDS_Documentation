# Changelog — JDS Document Studio (JDS-PRJ-SFW-002)

All notable changes to this project are recorded here.

---

## [Rev B] — 2026-06-26

### Added
- **Smart folder placement** (`studio/placement.py`): the target folder is now
  pre-filled where Studio is confident (QMS → `jds/quality-manual`, PRO →
  `jds/procedures`, TMP → `jds/templates/<type>`). It never guesses for ambiguous
  categories, and the field stays editable so the user keeps control (PRO-012 §5).
- **Office document generation**: timesheet / expense / mileage / all buttons,
  wired through `engine.generate_office()` to `scripts/generate-office-docs.py`.
- `GET /api/next-number` now also returns the suggested folder; new
  `POST /api/office?kind=` endpoint.

### Tests
- 10/10 passing (added `test_suggest_target_dir`).

## [Rev A] — 2026-06-26

### Added — Initial MVP
- **Pure core** (`studio/`): `config`, `numbering`, `registry`, `templates`,
  `creator` — the JDS-critical logic, with no third-party dependencies.
  - Next-free-number resolution scans the register **and** the filesystem and is
    prefix-anchored, so `JDS-RPT` never swallows `JDS-RPT-MEC` numbers.
  - Registry append inserts exactly one row under the correct category section and
    never rewrites existing rows.
  - Template instantiation fills the H1 title and metadata block, leaving the body.
- **Engine** (`studio/engine.py`): subprocess wrappers around the existing JDS
  scripts (`md2pdf.py`, `jds-validate.py`, `generate-office-docs.py`) — reused,
  never reimplemented (JDS-PRO-004 §6).
- **Server** (`studio/server.py`): thin FastAPI HTTP layer.
- **Web UI** (`web/`): single-page, vanilla JS, styled to PRO-007 (Navy/Steel,
  sans-serif, softened-corner Guide Note from Doc).
- **Tests** (`tests/test_core.py`): 9 unit + integration tests, all passing,
  including end-to-end document creation against a temporary sandbox repo and
  input-validation guards.
- **Conforms to JDS-PRO-012** (Interface Design Standard) as its reference
  implementation: visible focus indicators, control labels, reduced-motion
  support, and invalid actions prevented before any write (empty title, bad
  revision letter, out-of-repo target path).

### Design Decision — Web over Swift
Chosen because the entire document engine already exists in Python. A web app
reuses `md2pdf.py` / `jds-validate.py` / `generate-office-docs.py` directly and
runs cross-platform; a native Swift app would either shell out to Python anyway
or duplicate the whole pipeline — two engines to maintain, against the JDS
"reuse, keep it simple" principles. Swift remains the right call only if a
polished, distributable native macOS app becomes the explicit goal.

### Notes
- Built and unit-tested where possible. The HTTP server and PDF rendering require
  `fastapi`/`uvicorn`/`weasyprint` (see `requirements.txt`); install and run with
  `run.command` or `python3 -m studio.server`.
