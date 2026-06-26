# Changelog — JDS Document Studio (JDS-PRJ-SFW-002)

All notable changes to this project are recorded here.

---

## [Rev G] — 2026-06-26

### Changed — Consolidation & hardening (self-enhancement sweep)
- **One definition each:** the JDS-number regex (was duplicated in `registry`,
  `editor`, and `templates`) and the `today()` date helper (duplicated in
  `creator` and `editor`) now live once in `config` (`DOC_NUMBER_RE`,
  `today_iso`) — JDS-PRO-004 §6.
- **PDF route hardened:** `engine.generate_pdf` and `POST /api/pdf` now run their
  paths through the shared `config.resolve_in_repo` guard, like every other
  filesystem entry point.
- No behaviour change; 21/21 tests still pass.

## [Rev F] — 2026-06-26

### Added — Vessel classification & supervision (AFS 2017:3)
- Wires `scripts/jds-classify.py` into Studio so it produces the **real
  regulatory documents**, not just generic ones:
  - **Quick classify** — PS, volume, medium → AFS 2017:3 risk class, PED
    category, inspector, and inspection intervals (`POST /api/classify`).
  - **Supervision pipeline** — CSV → inventory → program → round / review
    (`POST /api/supervision`), each step reading and writing inside the repo.
- New UI panel "Supervision (AFS 2017:3)" with a quick-classify form and a
  pipeline-step runner.
- `engine.classify_quick()` and `engine.supervision()` wrappers; both reuse the
  shared repo-path guard.

### Changed — Internal
- Factored the repo-path-safety check into **`config.resolve_in_repo()`** (now
  used by creator, editor, and the supervision engine — JDS-PRO-004 §6, shared
  helper in one place).

### Tests
- 16/16 core + 5/5 server; the classify route and the full inventory→program
  pipeline were exercised against the real `jds-classify.py` in this environment.

## [Rev E] — 2026-06-26

### Added — Edit & revise (completes the document lifecycle)
- **`studio/revision.py`**: JDS revision sequencing (A→B…, skipping I/O/Q/S/X/Z;
  DRAFT→A) plus metadata-field and revision-history updates.
- **`studio/editor.py`**: read / save / **revise** an existing document — one
  action stamps the new revision and date, adds a history row, and syncs the
  register (`registry.update_entry`). Path access is constrained to the repo.
- UI **Edit & Revise panel**: choose a registered document, edit its body, save,
  or bump the revision with a change description.

### Added — Solidity
- **`studio/doctor.py`** dependency preflight + **`GET /api/health`**; the server
  prints the report on startup and the UI shows a banner when a package is missing.
- **`tests/test_server.py`**: HTTP-route tests via FastAPI TestClient (create +
  revise round-trip, validation rejections, metadata routes). Core tests now 15.
- Verified in-environment: 15/15 core + 3/3 server tests pass; the real app boots
  and serves its routes and static assets.

### Dependencies
- Added `httpx` (tests only — TestClient transport).

## [Rev D] — 2026-06-26

### Added — Iconography (PRO-012 §12.4)
- Panel headers now carry **SF Symbol-equivalent inline-SVG icons** (new document
  → `doc.badge.plus`, validate → `checkmark.seal`, office → clipboard/list),
  each paired with its text label and marked `aria-hidden` (decorative-redundant).
- Icons inherit text colour and weight via `currentColor` (`.icon` class), so they
  adapt to light/dark and match the heading weight — per §12.4.

## [Rev C] — 2026-06-26

### Changed — Apple HIG alignment (PRO-012 §12)
- **Adaptive light & dark appearance** via `prefers-color-scheme`: the JDS palette
  now resolves to light and dark values through CSS custom properties; native
  controls adapt via `color-scheme`.
- **44pt minimum hit targets** on buttons and inputs.
- System typography retained (`-apple-system` stack); surfaces refactored onto
  semantic tokens so appearance is consistent and themeable.

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
