# Uchiwa Fan — Split Blade with Locking Handle

| | |
|---|---|
| **Document No.** | JDS-DWG-MEC-001 |
| **Revision** | A |
| **Date** | 2026-07-14 |
| **Status** | CURRENT |
| **Author** | Nils Johansson |
| **Project** | Personal — 3D printed flat Japanese hand fan |

---

## 1. Description

A full-width (240 mm) uchiwa — the flat, non-folding Japanese hand fan — printed in three pieces that assemble without tools or glue:

- **Blade halves (left + right)**: a 1.2 mm ribbed panel with a stiffening rim and eight radiating ribs. The halves join edge-to-edge with three flared puzzle-dovetail tabs.
- **Handle**: contains a dovetail channel socket. The bottom 40 mm of the joined blade stem is a thickened dovetail tang that slides down into the channel.

**Locking principle** — three mechanisms stack:
1. The dovetail channel captures the tang against pull-out in the fanning direction (1.28 mm undercut per side vs 0.20 mm clearance).
2. The channel walls clamp the blade seam shut over the full 40 mm engagement, so the halves cannot separate while the handle is on.
3. A spherical detent bump on each blade half clicks into a through-window in the handle front wall at full insertion; the closed channel floor is the depth stop. To release, push a pin through the windows and slide the blade out.

Designed for FDM printing in PETG. Each blade half fits a 220 × 220 mm bed at the full 240 mm fan width.

## 2. Design Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Head (paddle) width | 240.0 | mm |
| Head height | 180.0 (220 for authentic proportions, needs ≥260 bed) | mm |
| Assembled length | 310 | mm |
| Panel thickness | 1.2 | mm |
| Rib height / width | 0.8 / 2.5 | mm |
| Tang width / depth / thickness | 21.0 / 40.0 / 6.0 | mm |
| Dovetail flank angle | 12 | deg |
| Detent bump proud / engagement | 0.6 / 0.35 | mm |
| Seam tab flare (lock) | 3.0 | mm |
| Handle length × width × thickness | 130 × 30 × 16 | mm |
| Socket clearance (width / thickness) | 0.20 / 0.25 | mm |
| Seam tab clearance | 0.20 | mm |
| Material | PETG | — |

## 3. Source Files

| File | Tool | Location |
|------|------|----------|
| `uchiwa-fan.py` | build123d 0.11.1 | `source/` |

### Running the Script

```bash
python3 projects/3d-modeling/JDS-DWG-MEC-001_uchiwa-fan/source/uchiwa-fan.py
```

The script is **self-verifying**: after building, it computes part-to-part interference volumes (must be zero), bed-fit footprints, and lock-geometry margins, and prints PASS/FAIL for each. It is also **self-correcting** — fillets, chamfers, 2D offsets, and engraving fall back to reduced parameters if geometry fails.

## 4. Exports

| Format | File | Purpose |
|--------|------|---------|
| STEP / STL / 3MF | `JDS-DWG-MEC-001_blade-left.*` | Blade left half (has tab sockets) |
| STEP / STL / 3MF | `JDS-DWG-MEC-001_blade-right.*` | Blade right half (has tabs) |
| STEP / STL / 3MF | `JDS-DWG-MEC-001_handle.*` | Handle with locking socket |
| STEP | `JDS-DWG-MEC-001_assembly.step` | All parts in assembled position |

Renders (assembled + parts layout) are in `renders/`.

## 5. Bill of Materials

| Item | Part | Description | Qty | Material |
|------|------|-------------|-----|----------|
| 1 | Blade left half | Ribbed panel, tab sockets, detent bump | 1 | PETG |
| 2 | Blade right half | Ribbed panel, dovetail tabs, detent bump | 1 | PETG |
| 3 | Handle | Dovetail channel socket, detent windows | 1 | PETG |

## 6. Printing

- **Blade halves**: flat on the bed as exported, ribs up. 0.2 mm layers, 3 perimeters, no supports. The halves are mirror twins except the tabs — print both.
- **Handle**: lay on its flat back face (as exported, flat side down). The socket roof bridges ~19 mm — printable without supports in PETG; the detent windows anchor the bridge.
- Clearances are tuned for PETG on a 0.4 mm nozzle. For PLA, reduce `WIDTH_CLEARANCE` and `THICKNESS_CLEARANCE` by 0.05 in the script and re-run.

## 7. Assembly

1. Lay the halves face-down and press the three dovetail tabs into their sockets (they drop in out-of-plane, then lock in-plane).
2. Slide the joined stem into the handle mouth (lead-in chamfer) and push down until both detent bumps click into the windows and the stem seats on the channel floor.
3. To disassemble, push a pin or 3 mm hex key through each window while pulling the blade.

> **Note:** The tabs alone do not resist out-of-plane separation — that is the handle's job. Always fit the handle before fanning.

## 8. Notes

- **Bed-size trade**: at `HEAD_HEIGHT = 180` each half is exactly 220 mm tall. For authentic taller proportions set `HEAD_HEIGHT = 220` (halves become 260 mm — needs a large-format bed).
- **No rib at 90°**: the rib pattern deliberately skips the vertical so no rib lands on the seam.
- **Seam stays prismatic in the socket zone**: the blade outline is trimmed flush to the stem width below the handle mouth so the neck fillet cannot interfere with the socket (caught by the automated fit check).
- **Brand**: "JE 1983" engraved on the handle front, reading upward.

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-07-14 | Nils Johansson | Initial design — split ribbed blade, dovetail + detent locking handle |
