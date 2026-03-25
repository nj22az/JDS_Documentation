# 3D Modeling Projects

Each project has its own folder named with its JEDS drawing number.

## Structure

```
3d-modeling/
├── JEDS-DWG-001_project-name/    # One folder per project
│   ├── README.md                  # Project card
│   ├── source/                    # Working files (.blend, .shapr, .py)
│   ├── exports/                   # Output files (.stl, .step, .obj, .gltf)
│   ├── references/                # Reference images, datasheets
│   └── renders/                   # Screenshots and renders
│
└── _shared-references/            # Shared across projects
```

## Creating a New Project

1. Get the next DWG number from the [Document Registry](../jeds/registry/document-register.md)
2. Create the folder: `JEDS-DWG-[NNN]_short-name/`
3. Add subfolders: `source/`, `exports/`, `references/`, `renders/`
4. Fill in the README.md project card
5. Register in the document registry

Full procedure: [JEDS-PRO-003](../jeds/procedures/JEDS-PRO-003_3d-model-management.md)

## Tools

- **Blender** — modeling, rendering, visualization
- **Shapr3D** — quick concept CAD, iPad workflow
- **build123d** — parametric CAD via Python scripts
