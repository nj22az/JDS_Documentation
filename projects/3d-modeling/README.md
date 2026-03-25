# 3D Modeling Projects

Each project has its own folder named with its JDS drawing number and engineering domain code.

## Structure

```
projects/3d-modeling/
├── JDS-DWG-MEC-001_project-name/  # Mechanical project
│   ├── README.md                   # Project card
│   ├── source/                     # Working files (.blend, .shapr, .py)
│   ├── exports/                    # STEP + 3MF + STL (mandatory)
│   ├── references/                 # Reference images, datasheets
│   └── renders/                    # Screenshots and renders
│
├── JDS-DWG-FAB-001_project-name/  # Fabrication project
│   └── ...
│
└── _shared-references/             # Shared across projects
```

## Domain Codes

| Code | Domain | Examples |
|------|--------|---------|
| MEC | Mechanical | Pumps, valves, flanges, brackets |
| MAR | Marine | Ship systems, engine room parts |
| AUT | Automation | Sensor brackets, panel enclosures |
| STR | Structural | Frames, mounts, supports |
| FAB | Fabrication | 3D printed parts, prototypes |
| TST | Testing | Test fixtures, calibration jigs |
| GEN | General | Cross-discipline parts |

## Mandatory Exports

Every project must export: **STEP** + **3MF** + **STL**

| Format | Why |
|--------|-----|
| STEP | Editable in any CAD tool — your future-proof file |
| 3MF | Modern 3D printing with units, materials, colour |
| STL | Universal fallback for any slicer |

## Creating a New Project

1. Pick the domain code (MEC, MAR, FAB, etc.)
2. Get the next DWG number from the [Document Registry](../../jds/registry/document-register.md)
3. Create the folder: `JDS-DWG-[DOM]-[NNN]_short-name/`
4. Add subfolders: `source/`, `exports/`, `references/`, `renders/`
5. Fill in the README.md project card
6. Export STEP + 3MF + STL to `exports/`
7. Register in the document registry

Full procedure: [JDS-PRO-003](../../jds/procedures/JDS-PRO-003_3d-model-management.md)

## Tools

- **Blender** — modeling, rendering, visualization
- **Shapr3D** — quick concept CAD, iPad workflow
- **build123d** — parametric CAD via Python scripts
