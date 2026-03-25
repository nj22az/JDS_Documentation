# Project Instructions for Claude

## Repository Purpose
Personal workspace for Nils Johansson's project files, including 3D modeling and software projects.

## Structure
- `jeds/` - Johansson Engineering Documentation System (quality manual, procedures, templates, registry)
- `blog/` - Jekyll engineering blog (GitHub Pages)
- `3d-modeling/` - 3D modeling projects, each in its own JEDS-DWG-NNN folder (Blender, Shapr3D, build123d)
- `software-projects/` - Software development projects
- `documents/` - CV, cover letters, notes
- `archive/` - Archived past projects (e.g., previous website)

## JEDS Documentation System
- All documents follow the JEDS numbering standard: `JEDS-[CAT]-[NNN]` (e.g., JEDS-RPT-003)
- Categories: QMS, PRO, RPT, MAN, DWG, PRJ, TSH, EXP, TMP, LOG, COR, BLG
- Always use the appropriate template from `jeds/templates/`
- Always register new documents in `jeds/registry/document-register.md`
- Revisions follow letter sequence: A, B, C, D... (skip I, O, Q, S, X, Z)
- Blog posts are tracked as BLG category (e.g., JEDS-BLG-001) with JEDS number in front matter
- See `jeds/README.md` for full documentation system reference

## 3D Modeling Projects
- Each 3D project gets a DWG number and its own folder: `3d-modeling/JEDS-DWG-NNN_name/`
- Standard subfolders: `source/`, `exports/`, `references/`, `renders/`
- Every project folder has a README.md project card
- See JEDS-PRO-003 for full procedure

## Guidelines
- Keep files organized in the appropriate directories
- Use descriptive names for project folders
- Each software project should have its own subfolder under `software-projects/`
