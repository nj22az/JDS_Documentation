# JDS-PRO-004 — Software Code Quality Standard

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRO-004 |
| **Revision** | A |
| **Date** | 2026-04-07 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## 1. Purpose

Define the code quality standard for all JDS software projects. These 7 rules apply both **when writing new code** and **when auditing existing code**. Every line written under JDS must follow these rules from the first keystroke.

## 2. Scope

Applies to all repositories under `projects/software/JDS-PRJ-SFW-*`.

## 3. Two Modes of Use

### 3.1 Code Creation Mode (while writing)
Follow all 7 rules as you write. Do not create technical debt to "fix later."

| Rule | When Writing |
|------|-------------|
| No dead code | Don't write code you don't need yet |
| Clean structure | Put each feature in the right module from the start |
| No hardcoded values | Use the config module for every constant |
| Clear names | Name everything descriptively on first write |
| Think about scale | Write thread-safe, memory-safe code by default |
| Keep files clean | Refactor as you go, don't let files rot |
| Document as you build | README and CHANGELOG updated with every revision |

### 3.2 Audit Mode (reviewing existing code)
Run the full 7-point audit at these intervals:

| Trigger | Audit Level |
|---------|-------------|
| Every commit | Quick (points 1, 3, 4) |
| Every 5 revisions | Full (all 7 points) |
| Before any release tag | Full + manual review |
| After major feature add | Full |

## 4. The 7-Point Code Audit

### 4.1 Dead Code Removal

Scan every file. Identify:
- All unused imports
- Unreferenced functions (defined but never called)
- Duplicate components or helper functions
- Orphaned files that are never imported anywhere

**Action:** Delete dead code. Do not comment it out.

### 4.2 Folder Restructure

Evaluate if files are organized by feature, not by type.

- Each feature should be self-contained in its own module
- No file over 500 lines without justification (GUI files exempt up to 1500)
- Flat structure is acceptable for < 20 files

**Action:** Restructure if files exceed thresholds. Document in CHANGELOG.

### 4.3 Hardcoded Value Extraction

Find every:
- Hardcoded string, colour hex, API URL
- Timeout value and magic number
- Font name/size used in more than one place

**Rule:** All shared constants live in a single config module (e.g., `models.py`) with named exports grouped by category.

**Categories:**
- Paths and directories
- Default parameters (width, height, steps, cfg)
- API endpoints and keys
- UI constants (colours, fonts, sizes)
- ML parameters (thresholds, strengths, tile sizes)

### 4.4 Naming Standardization

Audit all variable names, function names, and file names. Flag:
- Single-letter variables outside list comprehensions (`r`, `p`, `m`, `s`, `g`)
- Vague names: `temp`, `data`, `handler`, `stuff`, `thing`, `result2`, `utils`
- Inconsistent conventions (mixing `camelCase` and `snake_case`)

**Rule:** Every name must describe what it holds, not how it's used. Max 2 underscores per filename.

### 4.5 Scalability Risks

List the top 5 things that will break when load increases. For each:
1. Describe the failure mode
2. Provide a specific fix with code reference

**Note:** For desktop apps (single-user), focus on memory safety, thread safety, and large-file handling instead of concurrent users.

### 4.6 Worst File Rewrite

Identify the single messiest file by these metrics:
- Highest cyclomatic complexity
- Most hardcoded values
- Worst naming
- Most lines without clear section separation

**Action:** Rewrite it completely with clean naming and inline comments explaining non-obvious decisions.

### 4.7 Documentation

Every software project must have:
- `README.md` — what the app does, how to run it, project structure, requirements
- `CHANGELOG.md` — every revision with date and description
- Inline comments only where logic is non-obvious (not on every line)
- Type hints on public function signatures (recommended, not required)

## 5. Shared Utility Rule

Any helper function used in 3+ files must be:
1. Defined once in a shared module
2. Imported by all consumers
3. Never copy-pasted

**Examples:** Thread launchers (`bg_thread`), face detection setup, error dialog helpers.

## 6. Config Module Pattern

All constants must follow this structure in the config module:

```
# --- Paths ---
CONFIG_DIR = ...
MODELS_DIR = ...

# --- Defaults ---
DEFAULT_WIDTH = 512
DEFAULT_STEPS = 30

# --- UI ---
C = {"bg": "#F2F2F7", ...}
WINDOW_SIZE = "1200x820"

# --- ML ---
FACE_DET_SIZE = (640, 640)
REFINE_STRENGTH = 0.25

# --- API ---
HORDE_API_BASE = "https://..."
HTTP_TIMEOUT = 30
```

## 7. Integration with JDS

### Pre-commit (mandatory)
```bash
python3 scripts/jds-validate.py --quick
```

### Post-feature (mandatory)
Run the full 7-point audit. Record findings in the project CHANGELOG.

### Corrective actions
Issues found during audit follow JDS-PRO-008 (Corrective Action):
1. Fix the immediate instance
2. Fix the root cause (template, config, or module)
3. Add automated detection if possible
4. Update this procedure if a new pattern emerges

## 8. Audit Report Template

```
## Code Audit — [Project Name] Rev [X]

Date: YYYY-MM-DD

### 1. Dead Code
| File | Issue | Action |
|------|-------|--------|

### 2. Structure
[ ] Acceptable / [ ] Needs restructure

### 3. Hardcoded Values
| File | Value | Moved To |
|------|-------|----------|

### 4. Naming
| File | Old Name | New Name |
|------|----------|----------|

### 5. Scalability Risks
1. ...
2. ...

### 6. Worst File
File: ___  Rewritten: Yes/No

### 7. Documentation
[ ] README complete  [ ] CHANGELOG current  [ ] Comments adequate
```

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-07 | N. Johansson | Initial release — 7-point code audit procedure based on structural audit methodology |
