# Active Supervision Programs

This folder contains all active supervision programs managed under the Vessel Supervision System (JDS-PRJ-MEC-002).

---

## How to Create a New Program

1. **Read the manual** — JDS-MAN-MEC-002 (in `01-system/`)
2. **Create a client folder** — name it `[client-name]/` (lowercase, hyphens)
3. **Build the program** — copy JDS-TMP-LOG-005 from `03-program-templates/` and fill it in
4. **Register it** — add a row to JDS-LOG-MEC-005 (in `01-system/`)
5. **Assign a document number** — register in `jds/registry/document-register.md`

## Folder Structure Per Client

```
[client-name]/
├── JDS-LOG-MEC-NNN_supervision-program.md   ← The program document
├── rounds/                                   ← Completed round records (TMP-LOG-006)
│   ├── YYYY-MM-DD_round-record.md
│   └── ...
├── reviews/                                  ← Annual reviews (TMP-LOG-007)
│   ├── YYYY_annual-review.md
│   └── ...
└── findings/                                 ← Corrective actions per JDS-PRO-008
    ├── F-001_description.md
    └── ...
```

## Currently No Active Programs

This section will list active programs as they are created.
