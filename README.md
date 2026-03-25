# The Office of Nils Johansson

Personal workspace for 3D modeling, software projects, and an engineering blog.

## Blog

The `blog/` directory is a Jekyll site served via GitHub Pages — a classical technical engineering blog documenting practical problem-solving, 3D modeling, and lessons from the field.

## JDS — Johansson Documentation System

The `jds/` directory contains a complete in-house documentation and quality management system. It defines how all documents are numbered, created, revised, and tracked. See [jds/README.md](jds/README.md) for the full guide.

## Structure

```
├── jds/                 # Documentation & quality system (JDS)
│   ├── quality-manual/   # Quality manual and standards
│   ├── procedures/       # Work procedures and routines
│   ├── templates/        # Document templates
│   ├── registry/         # Master document register
│   └── examples/         # Worked examples
├── blog/                 # Jekyll blog (GitHub Pages)
├── 3d-modeling/          # 3D modeling projects (JDS-managed)
│   ├── JDS-DWG-NNN_name/ # One folder per project
│   │   ├── README.md      # Project card
│   │   ├── source/        # Working files (.blend, .shapr, .py)
│   │   ├── exports/       # Output files (.stl, .step, .obj, .gltf)
│   │   ├── references/    # Reference images, datasheets
│   │   └── renders/       # Screenshots and renders
│   └── _shared-references/ # Shared across all projects
│
├── projects/             # Engineering projects (JDS-managed)
│   └── JDS-PRJ-MEC-001_pressure-vessel-maintenance/
│
├── software-projects/    # Software development projects
│
├── documents/            # Personal documents
│   ├── cv/               # CV and cover letters
│   └── notes/            # Project notes
│
└── archive/              # Archived projects
    └── website-2025/     # Previous personal website (zipped)
```
