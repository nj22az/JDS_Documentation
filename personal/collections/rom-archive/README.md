# Digital Archive — Personal Collection

**Purpose:** Personal backup archive organised using JDS folder structure principles (QMS-000 §21).

---

## Structure

This collection follows the JDS collection folder pattern (QMS-000 §21.6):

```
archive-name/
├── README.md               ← This file (collection overview)
├── _shared-references/      ← Cross-item resources
└── [category]/              ← One folder per category
    └── [item-name]/         ← One folder per item
        ├── README.md        ← Item card (metadata, status)
        ├── source/          ← Primary files
        ├── documentation/   ← Manuals, guides, references
        ├── screenshots/     ← Screenshots and captures
        └── notes/           ← Personal notes
```

## Naming Conventions

**Category folders:** lowercase, hyphenated (e.g., `retro-computing`, `hardware-manuals`)

**Item folders:** lowercase, hyphenated item name

## Item Card (README) Template

Every item folder has a README.md with at minimum:

```markdown
# [Item Title]

| Field | Value |
|-------|-------|
| **Category** | [Category] |
| **Source** | [Where it came from] |
| **Date Added** | [Date] |

## Status

- [ ] Primary files present
- [ ] Documentation present
- [ ] Personal notes

## Notes

[Personal notes about this item.]
```

## Large Files

Files under 50MB can be stored in Git directly. Larger files should be stored externally, with the README documenting what exists and where to find it.

## Relationship to JDS

This collection is not document-numbered (it's in `personal/`), but it follows JDS structural principles:
- One folder per item, with a README card (QMS-000 §21.4)
- Collection folder pattern with categories and shared references (QMS-000 §21.6)
- Completeness checklist inspired by the complete document set concept (QMS-000 §8)
