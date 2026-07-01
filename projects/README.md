# Engineering Projects

Each project has its own folder named with its JDS project number and domain code.

## Structure

```
projects/
├── JDS-PRJ-MEC-001/
│   ├── README.md           ← Project overview
│   ├── CHANGELOG.md        ← Master log of all changes
│   ├── 01-framework/       ← Universal building blocks
│   ├── 02-regulations/     ← Country-specific rules
│   ├── 03-supervision/     ← Ongoing supervision system
│   └── 04-active-programs/ ← Real client work & examples
│
├── 3d-modeling/            ← 3D CAD projects (JDS-DWG-*)
├── blog/                   ← Jekyll blog (JDS-BLG-*)
├── literary/               ← Non-JDS creative writing projects
└── index.md                ← Project index
```

## Creating a New Project

1. Pick the domain code (MEC, MAR, AUT, etc.)
2. Get the next PRJ number from the [Document Registry](../jds/registry/document-register.md)
3. Create the folder: `JDS-PRJ-[DOM]-[NNN]/`
4. Add a README.md (project overview) and CHANGELOG.md (master change log)
5. Register in the document registry
