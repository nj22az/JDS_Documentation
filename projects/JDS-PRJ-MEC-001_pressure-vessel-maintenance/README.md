# Pressure Vessel Ongoing Maintenance Program

> **JDS-PRJ-MEC-001** | **Rev A** | **CURRENT** | 2026-03-25 | N. Johansson

---

## What Is This?

A complete, reusable service for managing ongoing maintenance and inspection of pressurised vessels. Built on Swedish regulations (AFS 2017:3) as the foundation, but designed so it can be adapted to any country's requirements.

This is a service you can offer to clients: *"I will set up and manage your pressure vessel maintenance program, ensuring regulatory compliance and full documentation traceability."*

## How This Program Is Organised

```
JDS-PRJ-MEC-001_pressure-vessel-maintenance/
│
├── 01-framework/                ← UNIVERSAL (works in any country)
│   ├── equipment-register.md    ← Master inventory of all vessels
│   ├── inspection-planning.md   ← How to schedule inspections
│   └── documentation-guide.md   ← What records you must keep
│
├── 02-regulations/              ← COUNTRY-SPECIFIC rules
│   ├── SE-sweden/               ← Swedish rules (AFS 2017:3)
│   └── [add countries here]/    ← Norway, Germany, etc.
│
├── 03-active-programs/          ← CLIENT WORK (real inventories)
│   └── [client-name]/           ← One folder per client
│
└── CHANGELOG.md                 ← Master log of ALL changes
```

### What goes where?

| Folder | What's in it | When it changes |
|--------|-------------|-----------------|
| **01-framework/** | The universal building blocks — equipment register template, inspection logic, documentation requirements. Works regardless of country. | Only when you improve the service itself |
| **02-regulations/** | Country-specific rules and requirements. Each country has its own subfolder. | When regulations change or you add a new country |
| **03-active-programs/** | Real client work. Each client has their own subfolder with their actual equipment register, inspection schedules, and reports. | During active client work |

## How to Expand to a New Country

1. Create a new folder under `02-regulations/` (e.g., `NO-norway/`)
2. Document that country's pressure vessel regulations
3. Map their requirements to the framework categories
4. The equipment register and inspection planning from `01-framework/` still apply — just reference the new country's inspection intervals and categories

**You never touch the Swedish files to add another country.**

## Related Documents

| Doc No. | Title | Location |
|---------|-------|----------|
| JDS-LOG-MEC-001 | Equipment Register (Framework Template) | `01-framework/equipment-register.md` |
| JDS-PRO-004 | Inspection Planning Procedure | `01-framework/inspection-planning.md` |
| JDS-MAN-MEC-001 | Documentation Guide | `01-framework/documentation-guide.md` |

## How to Know You Have the Latest Version

Every document in this program has a status block at the very top:

```
> JDS-XXX-MEC-NNN | Rev A | CURRENT | 2026-03-25 | N. Johansson
```

- **CURRENT** = This is the version you should use
- **SUPERSEDED** = A newer version exists — do NOT use this
- **DRAFT** = Not yet approved

The **CHANGELOG.md** in this folder logs every single change across all documents. Open it to see the full history.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | N. Johansson | Initial release — project structure and framework |
