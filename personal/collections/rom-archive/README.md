# ROM Archive — Personal Game Preservation Collection

**Owner:** Nils Johansson
**Purpose:** Personal backup archive of classical video game ROM files, organised with JDS principles for structure, traceability, and completeness.

---

## Principles

This archive applies JDS documentation discipline to personal game preservation:

1. **One folder per game** — every game gets its own folder with a README (game card)
2. **Version tracking** — ROM revisions, regions, and patches are tracked explicitly
3. **Completeness** — each game folder aims to preserve: ROM files, documentation, screenshots, saves, and notes
4. **Verification** — ROM checksums are recorded and verified against known-good databases (No-Intro, Redump)
5. **Organisation by system** — games are grouped by hardware platform

## Folder Structure

```
rom-archive/
├── README.md                    ← This file
├── _shared-references/          ← Cross-game resources (emulator guides, system specs)
│
├── [system-name]/               ← One folder per console/system
│   ├── [game-name]/             ← One folder per game
│   │   ├── README.md            ← Game card (metadata, versions, status)
│   │   ├── roms/                ← ROM files (named with region & version)
│   │   ├── saves/               ← Save files, save states, battery saves
│   │   ├── documentation/       ← Manuals, maps, guides, box scans
│   │   ├── screenshots/         ← Title screens, gameplay, notable moments
│   │   ├── patches/             ← Patches, translations, bug fixes
│   │   └── notes/               ← Personal notes, tips, completion log
│   └── ...
└── ...
```

## System Folder Names

Use lowercase, hyphenated names matching common convention:

| System | Folder Name |
|--------|-------------|
| Nintendo Entertainment System | `nes` |
| Super Nintendo | `super-nintendo` |
| Game Boy | `game-boy` |
| Game Boy Color | `game-boy-color` |
| Game Boy Advance | `game-boy-advance` |
| Nintendo 64 | `nintendo-64` |
| Nintendo DS | `nintendo-ds` |
| Sega Master System | `sega-master-system` |
| Sega Mega Drive / Genesis | `sega-mega-drive` |
| Sega Saturn | `sega-saturn` |
| Sega Dreamcast | `sega-dreamcast` |
| PlayStation | `playstation` |
| PlayStation 2 | `playstation-2` |
| Neo Geo | `neo-geo` |
| TurboGrafx-16 / PC Engine | `pc-engine` |

Add new systems as needed following the same convention.

## Game Card (README) Template

Every game folder must have a README.md with at minimum:

```markdown
# [Game Title]

| Field | Value |
|-------|-------|
| **System** | [Console name] |
| **Developer** | [Developer] |
| **Publisher** | [Publisher] |
| **Year** | [Release year] |
| **Genre** | [Genre] |
| **Region** | [JP / US / EU / etc.] |

## ROM Files

| Filename | Region | Version | Checksum (CRC32) | Verified | Source |
|----------|--------|---------|-------------------|----------|--------|
| ... | ... | ... | ... | Yes/No | No-Intro / Redump / Personal dump |

## Archive Status

- [ ] ROM file(s) present
- [ ] Checksum verified
- [ ] Manual / documentation
- [ ] Screenshots (title + gameplay)
- [ ] Box art / cover scan
- [ ] Personal notes / review

## Notes

[Personal notes, memories, completion status, tips]
```

## ROM File Naming Convention

Follow the No-Intro naming convention where possible:

```
Game Title (Region) (Version).ext

Examples:
Legend of Zelda, The - Link's Awakening DX (USA, Europe) (Rev 2).gbc
Super Mario World (Japan, USA) (Rev 1).sfc
```

## Verification

ROM integrity is verified using checksums against established databases:

| Database | What it covers | URL |
|----------|---------------|-----|
| **No-Intro** | Cartridge-based systems (NES, SNES, GB, GBA, N64, etc.) | no-intro.org |
| **Redump** | Disc-based systems (PS1, PS2, Saturn, Dreamcast, etc.) | redump.org |

Record the CRC32, MD5, or SHA-1 checksum in the game README. Mark as "Verified" only if it matches a known-good dump.

## What NOT to Store in Git

- ROM files larger than 50MB should be tracked with Git LFS or stored externally
- Disc images (ISO, BIN/CUE) for CD-based systems are typically too large for Git — consider external storage with a reference in the README
- For large files, the README serves as the documentation even if the actual file is stored elsewhere

## Relationship to JDS

This archive uses JDS principles but does not use JDS document numbers. Games are not engineering documents. However:

- The folder discipline comes from JDS-PRO-003 (3D Model Management)
- The completeness checklist is inspired by JDS-PRO-006 (Komplekt Standard)
- The verification approach uses JDS confidence levels (Verified / Probable / Uncertain)
- The README game cards follow the JDS project card pattern
