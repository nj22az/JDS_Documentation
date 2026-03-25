# 3D Model & Drawing Management Procedure

| | |
|---|---|
| **Document No.** | JDS-PRO-003 |
| **Revision** | B |
| **Date** | 2026-03-25 |
| **Status** | APPROVED |
| **Author** | Nils Johansson |

---

## 1. Purpose

This procedure defines how 3D models, engineering drawings, and related files are organised, named, stored, and tracked within JDS. Every modeling project — whether it's a single part or a full assembly — follows the same structure so that files are always findable, traceable, and version-controlled.

## 2. Scope

Applies to all 3D modeling and drawing work, including:
- Blender projects (.blend)
- Shapr3D projects (.shapr)
- build123d scripts (.py)
- Exported files (STEP, 3MF, STL — mandatory standard set)
- Reference images and sketches
- Related documentation (DWG documents)

## 3. Folder Structure

### 3.1 Overview

Each modeling project gets its own folder under `projects/3d-modeling/`, named with its JDS drawing number:

```
projects/3d-modeling/
├── JDS-DWG-MEC-001_flange-adapter/    # One folder per project
│   ├── README.md                       # Project card (quick reference)
│   ├── source/                         # Source/working files
│   │   ├── flange-adapter.blend        # Blender file
│   │   ├── flange-adapter.shapr        # Shapr3D file
│   │   └── flange-adapter.py           # build123d script
│   ├── exports/                        # Exported output files (standard set)
│   │   ├── flange-adapter.step         # MANDATORY — CAD interchange
│   │   ├── flange-adapter.3mf          # MANDATORY — 3D printing (preferred)
│   │   ├── flange-adapter.stl          # MANDATORY — 3D printing (universal)
│   │   └── flange-adapter.glb          # Optional — web/presentation
│   ├── references/                     # Reference material
│   │   ├── sketch-001.jpg
│   │   └── datasheet.pdf
│   └── renders/                        # Screenshots and renders
│       └── final-render.png
│
├── JDS-DWG-STR-001_bracket-mount/     # Next project (Structural domain)
│   ├── README.md
│   ├── source/
│   ├── exports/
│   ├── references/
│   └── renders/
│
└── _shared-references/                 # Materials shared across projects
    ├── standard-fasteners.md
    └── material-properties.md
```

### 3.2 Key Rules

1. **One folder per JDS drawing number.** A project folder is created when a DWG number is assigned.
2. **Folder name = JDS number (with domain) + short description.** Example: `JDS-DWG-MEC-001_flange-adapter/`
3. **Source files go in `source/`.** These are the editable working files.
4. **Exports go in `exports/`.** These are the output files for fabrication, sharing, or viewing.
5. **References go in `references/`.** Sketches, datasheets, photos — anything used as input.
6. **Renders go in `renders/`.** Screenshots, final renders, preview images.
7. **Every project has a `README.md`** — the project card (see Section 5).

### 3.3 Shared References

The `_shared-references/` folder (prefixed with underscore to sort to top) holds material that applies across multiple projects — standard fastener libraries, material property tables, common dimensions, etc.

## 4. File Naming

### 4.1 Source Files

Source files use descriptive lowercase names with hyphens:

```
part-name.blend
part-name.shapr
part-name.py
```

For multi-part projects or assemblies, use a prefix:

```
assembly-name_part-01-housing.blend
assembly-name_part-02-cover.blend
assembly-name_full-assembly.blend
```

### 4.2 Export Files

Exports match the source file name with the appropriate extension:

```
flange-adapter.step         # MANDATORY — CAD interchange
flange-adapter.3mf          # MANDATORY — 3D printing (preferred)
flange-adapter.stl          # MANDATORY — 3D printing (universal)
flange-adapter.glb          # Optional — web/presentation
flange-adapter_v2.step      # Variant — append version if needed
```

### 4.3 Mandatory Export Standard

Every 3D model project **must** export these three formats:

| Format | Extension | Why it's mandatory | Use case |
|--------|-----------|-------------------|----------|
| **STEP** | `.step` | Preserves solid geometry. Editable in any CAD tool. Your insurance policy for future modifications. | CAD interchange, CNC machining, sharing with engineers |
| **3MF** | `.3mf` | Modern printing format. Carries units, materials, colour, and tolerances in one file. | 3D printing (preferred by modern slicers) |
| **STL** | `.stl` | Universal mesh format. Every slicer and viewer reads it. | 3D printing (universal fallback), quick sharing |

**Optional exports** (add when relevant):

| Format | Extension | When to include |
|--------|-----------|----------------|
| **glTF/GLB** | `.gltf` / `.glb` | Web viewers, blog posts, presentations, AR/VR |
| **OBJ** | `.obj` | When specifically requested by a collaborator |
| **PDF (2D)** | `.pdf` | Dimensioned drawings for machine shops or documentation |

**Why STEP is critical:** STL and 3MF are mesh formats — you cannot easily edit them later. STEP preserves the actual solid geometry, so you or anyone else can reopen it in Shapr3D, FreeCAD, or any CAD tool and modify the design. Always export STEP first.

### 4.4 Reference Files

References use descriptive names:

```
sketch-initial-concept.jpg
datasheet-dn50-flange.pdf
photo-site-measurement.jpg
```

## 5. Project Card (README.md)

Every project folder contains a `README.md` that acts as a quick-reference card. Use the template below:

```markdown
# [Part/Assembly Name]

| | |
|---|---|
| **JDS No.** | JDS-DWG-[DOM]-[NNN] |
| **Rev** | A |
| **Date** | YYYY-MM-DD |
| **Status** | DRAFT / APPROVED |
| **Author** | Nils Johansson |

## Description
[What is this? What is it for? 2-3 sentences.]

## Key Dimensions
| Parameter | Value | Unit |
|-----------|-------|------|
| [Dimension] | [Value] | mm |

## Tools Used
- [ ] Blender
- [ ] Shapr3D
- [ ] build123d

## Source Files
| File | Tool | Description |
|------|------|-------------|
| source/[filename] | [Tool] | [What it contains] |

## Exports (mandatory standard set)
| File | Format | Purpose |
|------|--------|---------|
| exports/[filename].step | STEP | CAD interchange (editable) |
| exports/[filename].3mf | 3MF | 3D printing (preferred) |
| exports/[filename].stl | STL | 3D printing (universal) |

## Notes
[Design decisions, constraints, tolerances, material choices, etc.]
```

## 6. Workflow: Creating a New 3D Project

### Step 1: Assign a DWG number

Check the [Document Registry](../registry/document-register.md) for the next available DWG number in your domain. Pick the engineering domain code (MEC, MAR, AUT, etc.) from the [Numbering Standard](../quality-manual/JDS-QMS-001_document-numbering.md).

### Step 2: Create the project folder

```bash
mkdir -p projects/3d-modeling/JDS-DWG-MEC-001_short-name/{source,exports,references,renders}
```

### Step 3: Create the project card

Copy the README template from Section 5 into the project folder and fill in the header.

### Step 4: Do the work

Create your models in the `source/` folder. Collect references in `references/`.

### Step 5: Export the standard set

Export all three mandatory formats to `exports/`:
- `.step` — CAD interchange (always first)
- `.3mf` — 3D printing (preferred)
- `.stl` — 3D printing (universal fallback)

### Step 6: Register the document

Add the DWG entry to the [Document Registry](../registry/document-register.md).

### Step 7: Commit

Commit the project folder to the repository. Use a descriptive commit message:

```
Add JDS-DWG-MEC-001: Flange adapter DN50 — initial model
```

## 7. Revision Control for 3D Models

3D models follow the same revision control as other JDS documents (see JDS-PRO-002), with these additions:

### 7.1 What Counts as a Revision

| Change | Action |
|--------|--------|
| Dimensions changed | New revision (update DWG document + re-export) |
| Material changed | New revision |
| New variant added | New revision OR new DWG number (see 7.2) |
| Cosmetic/render update only | Minor update (same revision, note in commit) |
| Bug fix in build123d script | New revision if output changes; minor if not |

### 7.2 Variants vs. Revisions

- **Revision:** The same part, improved or corrected. Same DWG number, next revision letter.
- **Variant:** A different version of a part (e.g., different size, different mounting). Gets its **own DWG number** with a note referencing the original.

Example:
```
JDS-DWG-MEC-001  Flange Adapter DN50
JDS-DWG-MEC-002  Flange Adapter DN80 (variant of DWG-MEC-001)
```

### 7.3 Export on Every Revision

Whenever a source file is revised, **re-export all output files**. Old exports that don't match the current source are misleading. The Git history preserves previous versions if needed.

## 8. Large Binary Files

### 8.1 Git Considerations

Binary files (`.blend`, `.shapr`, images, STL) don't diff well in Git. Best practices:

- **Commit meaningful snapshots**, not every auto-save
- **Write descriptive commit messages** for binary changes since the diff won't show what changed
- For very large files (>50MB), consider using **Git LFS** (Large File Storage). This can be configured later if needed.

### 8.2 What to Commit

| File type | Commit to Git? | Notes |
|-----------|---------------|-------|
| .blend | Yes | Main working file |
| .blend1 / .blend2 | No | Auto-backups (in .gitignore) |
| .shapr | Yes | Main working file |
| .py (build123d) | Yes | Source code — diffs perfectly |
| .step / .3mf / .stl | Yes | Mandatory export set |
| .glb / .obj | Yes | Optional exports when relevant |
| Reference images | Yes | Keep reasonable sizes (<5MB each) |
| Renders | Yes | Final renders only, not drafts |

## 9. Quick Checklist: New 3D Project

- [ ] DWG number with domain code assigned from registry
- [ ] Project folder created: `projects/3d-modeling/JDS-DWG-[DOM]-[NNN]_name/`
- [ ] Subfolders created: `source/`, `exports/`, `references/`, `renders/`
- [ ] README.md project card filled in
- [ ] Source files saved in `source/`
- [ ] Mandatory exports generated: STEP + 3MF + STL in `exports/`
- [ ] Document registry updated
- [ ] Committed to repository with descriptive message

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial release |
| B | 2026-03-25 | Nils Johansson | Renamed JEDS to JDS. Added domain codes to folder naming. Added mandatory export standard (STEP + 3MF + STL). |
