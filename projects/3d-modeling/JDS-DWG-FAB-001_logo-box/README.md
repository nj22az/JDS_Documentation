# Circular Logo Box with Screw Lid

| | |
|---|---|
| **Document No.** | JDS-DWG-FAB-001 |
| **Revision** | A |
| **Date** | 2026-03-25 |
| **Status** | CURRENT |
| **Author** | Nils Johansson |
| **Project** | Personal — 3D printed storage container |

---

## 1. Description

A round screw-top container inspired by Milwaukee-style parts boxes. Features two internal compartments separated by a divider wall with a chamfer on one side. The lid screws onto the base and has the Johansson Engineering "JE 1983" logo embossed on top.

Designed for FDM or SLA 3D printing.

## 2. Design Parameters

| Parameter | Value | Unit |
|-----------|-------|------|
| Outer diameter | 80.0 | mm |
| Box body height | 30.0 | mm |
| Thread zone height | 8.0 | mm |
| Total height (body) | 38.0 | mm |
| Wall thickness | 2.5 | mm |
| Floor thickness | 2.5 | mm |
| Divider thickness | 1.8 | mm |
| Divider chamfer | 2.0 (auto-reduced to 1.2) | mm |
| Thread pitch | 3.0 | mm |
| Thread depth | 1.0 | mm |
| Lid clearance | 0.4 | mm |
| Thread engagement | 1.6 | mm |
| Lid top thickness | 3.0 | mm |
| Lid skirt height | 10.0 | mm |
| Logo emboss depth | 0.8 | mm |
| Material | PLA / PETG / ABS | — |
| Tolerance (general) | 0.2 | mm |

## 3. Source Files

| File | Tool | Location |
|------|------|----------|
| `logo-box.py` | build123d 0.10.0 | `source/` |

### Running the Script

```bash
python3 projects/3d-modeling/JDS-DWG-FAB-001_logo-box/source/logo-box.py
```

The script is **self-correcting**: geometry operations that can fail (chamfers, threads, 3MF mesh) are wrapped with fallback logic that automatically reduces parameters or uses alternative export strategies.

## 4. Exports

| Format | File | Purpose |
|--------|------|---------|
| STEP | `JDS-DWG-FAB-001_box.step` | Box body — CAD interchange |
| STEP | `JDS-DWG-FAB-001_lid.step` | Lid — CAD interchange |
| STEP | `JDS-DWG-FAB-001_assembly.step` | Both parts — assembly view |
| STL | `JDS-DWG-FAB-001_box.stl` | Box body — 3D printing |
| STL | `JDS-DWG-FAB-001_lid.stl` | Lid — 3D printing |
| 3MF | `JDS-DWG-FAB-001_box.3mf` | Box body — modern 3D printing |
| 3MF | `JDS-DWG-FAB-001_lid.3mf` | Lid — modern 3D printing |

## 5. Bill of Materials

| Item | Part | Description | Qty | Material |
|------|------|-------------|-----|----------|
| 1 | Box body | Cylinder with thread and divider | 1 | PLA |
| 2 | Lid | Screw lid with logo emboss | 1 | PLA |

## 6. Notes

- **Thread design**: External thread on box, internal thread on lid. Pitch 3.0mm, depth 1.0mm, clearance 0.4mm. Verified 1.6mm engagement — lid grips securely.
- **Self-correction**: The build script automatically reduces chamfer size if geometry fails, falls back to ring-style threads if helix sweep fails, and converts STL to 3MF if direct mesh export fails.
- **Parametric**: All dimensions are defined as constants at the top of the script. Change any parameter and re-run to generate updated exports.
- **Logo**: "JE" (Johansson Engineering) and "1983" embossed on lid top with a decorative bar.
- **Print orientation**: Print box upright, lid upside down (flat top on bed).

---

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-03-25 | Nils Johansson | Initial design — screw-top box with divider and logo |
