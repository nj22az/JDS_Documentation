# Project Instructions for Claude

## Repository Purpose
Personal workspace for Nils Johansson's project files, including 3D modeling and software projects.

## Structure
- `jds/` - Johansson Documentation System (quality manual, procedures, templates, registry)
- `blog/` - Jekyll engineering blog (GitHub Pages)
- `3d-modeling/` - 3D modeling projects, each in its own JDS-DWG-[DOM]-NNN folder (Blender, Shapr3D, build123d)
- `projects/` - Engineering projects, each in its own JDS-PRJ-[DOM]-NNN folder
- `software-projects/` - Software development projects
- `documents/` - CV, cover letters, notes
- `archive/` - Archived past projects (e.g., previous website)

## JDS Documentation System
- Technical documents: `JDS-[CAT]-[DOM]-[NNN]` (e.g., JDS-DWG-MEC-003)
- System documents: `JDS-[CAT]-[NNN]` (e.g., JDS-PRO-001)
- Categories: QMS, PRO, RPT, MAN, DWG, PRJ, TSH, EXP, TMP, LOG, COR, BLG
- Domain codes: MEC, MAR, AUT, ELE, PIP, STR, TST, FAB, THR, SFW, GEN
- Always use the appropriate template from `jds/templates/`
- Always register new documents in `jds/registry/document-register.md`
- Revisions follow letter sequence: A, B, C, D... (skip I, O, Q, S, X, Z)
- Blog posts are tracked as BLG category with domain code (e.g., JDS-BLG-MEC-001)
- See `jds/README.md` for full documentation system reference

## 3D Modeling Projects
- Each 3D project gets a DWG number with domain: `3d-modeling/JDS-DWG-MEC-001_name/`
- Standard subfolders: `source/`, `exports/`, `references/`, `renders/`
- Mandatory exports: STEP + 3MF + STL (always all three)
- Every project folder has a README.md project card
- See JDS-PRO-003 for full procedure

## Engineering Projects
- Each project gets a PRJ number with domain: `projects/JDS-PRJ-MEC-001_name/`
- Every project has a README.md and CHANGELOG.md (master change log)
- All document changes within a project are logged in CHANGELOG.md
- Every document has a status block at the top: Doc No | Rev | CURRENT/SUPERSEDED | Date | Author

## Guidelines
- Keep files organized in the appropriate directories
- Use descriptive names for project folders
- Each software project should have its own subfolder under `software-projects/`
