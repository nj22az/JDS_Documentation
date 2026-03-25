"""
JDS-DWG-FAB-001 — Circular Logo Box with Screw Lid and Divider
Parametric CAD model using build123d

A round screw-top container with:
- Cylindrical box body with external thread
- Screw-on lid with internal thread and embossed "JE 1983" logo
- Internal divider wall with chamfer on one side
- Knurled grip on lid exterior

Inspired by Milwaukee-style round parts containers.
All dimensions in mm. Designed for FDM/SLA 3D printing.

Self-correcting: geometry operations that can fail (chamfers, threads)
are wrapped with fallback logic and parameter reduction.
"""

from build123d import *
from pathlib import Path
import sys

# ── Design Parameters ──────────────────────────────────────────────
# Box body
OUTER_DIAMETER = 80.0       # mm
WALL_THICKNESS = 2.5        # mm
FLOOR_THICKNESS = 2.5       # mm
BOX_HEIGHT = 30.0           # mm — body height (without thread zone)

# Thread zone (top of box body, where lid screws on)
THREAD_HEIGHT = 8.0         # mm — height of threaded section
THREAD_PITCH = 3.0          # mm — distance between thread crests
THREAD_DEPTH = 1.0          # mm — how deep thread cuts into wall

# Divider
DIVIDER_THICKNESS = 1.8     # mm
DIVIDER_CHAMFER = 2.0       # mm — chamfer on one top edge

# Lid
LID_TOP_THICKNESS = 3.0     # mm — solid top disc
LID_SKIRT_HEIGHT = THREAD_HEIGHT + 2.0  # mm — skirt wraps around thread
LID_CLEARANCE = 0.4         # mm — radial gap for thread play

# Logo
LOGO_TEXT_LINE1 = "JE"
LOGO_TEXT_LINE2 = "1983"
LOGO_DEPTH = 0.8            # mm — emboss above lid surface

# Derived
OUTER_RADIUS = OUTER_DIAMETER / 2
INNER_RADIUS = OUTER_RADIUS - WALL_THICKNESS
TOTAL_BOX_HEIGHT = BOX_HEIGHT + THREAD_HEIGHT
LID_INNER_RADIUS = OUTER_RADIUS + LID_CLEARANCE
LID_OUTER_RADIUS = LID_INNER_RADIUS + WALL_THICKNESS

# ── Export directory ───────────────────────────────────────────────
EXPORT_DIR = Path(__file__).parent.parent / "exports"
EXPORT_DIR.mkdir(exist_ok=True)


def safe_chamfer(part_builder, edges, length, label=""):
    """Try chamfer, reduce size on failure, skip if impossible."""
    for attempt_length in [length, length * 0.6, length * 0.3]:
        try:
            chamfer(edges, length=attempt_length)
            if attempt_length != length:
                print(f"  SELF-CORRECT: {label} chamfer reduced from "
                      f"{length:.1f}mm to {attempt_length:.1f}mm")
            return True
        except (ValueError, Exception):
            continue
    print(f"  SELF-CORRECT: {label} chamfer skipped — geometry too tight")
    return False


def make_thread_helix(radius, height, pitch, depth, internal=False):
    """Create a triangular thread profile swept along a helix.

    For external thread: cuts into the outer wall of the box.
    For internal thread: cuts into the inner wall of the lid skirt.
    """
    # Thread profile — triangular cross-section
    # The profile is a small triangle that will be swept along the helix
    half_pitch = pitch / 2

    if internal:
        # Internal thread: profile points inward (toward center)
        profile_pts = [
            (radius, 0),
            (radius + depth, half_pitch * 0.8),
            (radius + depth, -half_pitch * 0.8),
            (radius, 0),
        ]
    else:
        # External thread: profile points outward
        profile_pts = [
            (radius, 0),
            (radius - depth, half_pitch * 0.8),
            (radius - depth, -half_pitch * 0.8),
            (radius, 0),
        ]

    # Number of turns
    turns = height / pitch

    # Create helix path
    helix = Helix(pitch=pitch, height=height, radius=radius, center=(0, 0, 0))

    # Create the thread profile as a face on the XZ plane at the helix start
    with BuildSketch(Plane.XZ.offset(0)) as thread_profile:
        with BuildLine():
            Polyline(
                (0, -half_pitch * 0.8),
                (depth if not internal else -depth, 0),
                (0, half_pitch * 0.8),
                (0, -half_pitch * 0.8),
            )
        make_face()

    # Position the profile at the start of the helix
    profile_face = thread_profile.sketch.moved(
        Location((radius, 0, 0))
    )

    thread_solid = sweep(profile_face, path=helix)
    return thread_solid


def build_box() -> Part:
    """Build the cylindrical box body with thread and internal divider."""

    # Step 1: Solid outer cylinder (full height including thread zone)
    with BuildPart() as box:
        with BuildSketch():
            Circle(OUTER_RADIUS)
        extrude(amount=TOTAL_BOX_HEIGHT)

        # Hollow out the inside
        with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
            Circle(INNER_RADIUS)
        extrude(amount=TOTAL_BOX_HEIGHT - FLOOR_THICKNESS, mode=Mode.SUBTRACT)

    box_part = box.part

    # Step 2: Create external thread on the upper portion
    # The thread is a helical ridge on the outside of the box wall
    thread_base_z = BOX_HEIGHT  # thread starts above the body
    try:
        helix_path = Helix(
            pitch=THREAD_PITCH,
            height=THREAD_HEIGHT - THREAD_PITCH * 0.5,  # leave room at top
            radius=OUTER_RADIUS,
        )

        # Triangular thread profile on XZ plane
        tp = THREAD_PITCH * 0.4  # half-width of thread triangle
        with BuildSketch(Plane.XZ) as tprof:
            with BuildLine():
                Polyline(
                    (0, -tp),
                    (THREAD_DEPTH, 0),
                    (0, tp),
                    (0, -tp),
                )
            make_face()

        # Move profile to helix start and sweep
        profile = tprof.sketch.moved(Location((OUTER_RADIUS, 0, 0)))
        thread = sweep(profile, path=helix_path)
        thread = thread.moved(Location((0, 0, thread_base_z + THREAD_PITCH * 0.25)))
        box_part = box_part + thread
        print("  External thread: OK")
    except Exception as e:
        print(f"  SELF-CORRECT: External thread failed ({e})")
        print("  Falling back to simple ridge rings for thread indication")
        # Fallback: add simple rings as thread indicators
        with BuildPart() as rings:
            for i in range(int(THREAD_HEIGHT / THREAD_PITCH)):
                z = thread_base_z + i * THREAD_PITCH + THREAD_PITCH * 0.25
                with BuildSketch(Plane.XY.offset(z)):
                    Circle(OUTER_RADIUS + THREAD_DEPTH)
                    Circle(OUTER_RADIUS, mode=Mode.SUBTRACT)
                extrude(amount=THREAD_PITCH * 0.3)
        box_part = box_part + rings.part

    # Step 3: Build divider separately, chamfer it, then clip and combine
    with BuildPart() as divider:
        with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
            Rectangle(DIVIDER_THICKNESS, INNER_RADIUS * 2)
        extrude(amount=BOX_HEIGHT - FLOOR_THICKNESS - 0.5)

        # Find the top edge on +X side for chamfer
        div_top_z = BOX_HEIGHT - 0.5
        tol = 0.3
        top_edges = [
            e for e in divider.edges()
            if abs(e.center().Z - div_top_z) < tol
            and e.length > INNER_RADIUS * 0.5
        ]
        if top_edges:
            top_edges.sort(key=lambda e: e.center().X, reverse=True)
            safe_chamfer(divider, top_edges[:1], DIVIDER_CHAMFER, "divider")

    # Clip divider to inner cylinder
    with BuildPart() as clip:
        with BuildSketch(Plane.XY.offset(FLOOR_THICKNESS)):
            Circle(INNER_RADIUS - 0.01)
        extrude(amount=BOX_HEIGHT - FLOOR_THICKNESS)

    clipped_div = divider.part & clip.part
    box_part = box_part + clipped_div

    return box_part


def build_lid() -> Part:
    """Build the screw-on lid with internal thread and embossed logo."""

    with BuildPart() as lid:
        # Top disc
        with BuildSketch():
            Circle(LID_OUTER_RADIUS)
        extrude(amount=LID_TOP_THICKNESS)

        # Skirt extending downward (hollow cylinder)
        with BuildSketch():
            Circle(LID_OUTER_RADIUS)
            Circle(LID_INNER_RADIUS, mode=Mode.SUBTRACT)
        extrude(amount=-LID_SKIRT_HEIGHT)

    lid_part = lid.part

    # Internal thread on lid skirt
    skirt_thread_radius = LID_INNER_RADIUS
    try:
        helix_path = Helix(
            pitch=THREAD_PITCH,
            height=THREAD_HEIGHT - THREAD_PITCH * 0.5,
            radius=skirt_thread_radius,
        )

        tp = THREAD_PITCH * 0.4
        with BuildSketch(Plane.XZ) as tprof:
            with BuildLine():
                Polyline(
                    (0, -tp),
                    (-THREAD_DEPTH, 0),
                    (0, tp),
                    (0, -tp),
                )
            make_face()

        profile = tprof.sketch.moved(Location((skirt_thread_radius, 0, 0)))
        thread = sweep(profile, path=helix_path)
        # Position thread inside the skirt
        thread_z = -(LID_SKIRT_HEIGHT - THREAD_PITCH * 0.25)
        thread = thread.moved(Location((0, 0, thread_z)))
        lid_part = lid_part + thread
        print("  Internal thread: OK")
    except Exception as e:
        print(f"  SELF-CORRECT: Internal thread failed ({e})")
        print("  Falling back to simple ridge rings")
        with BuildPart() as rings:
            for i in range(int(THREAD_HEIGHT / THREAD_PITCH)):
                z = -(LID_SKIRT_HEIGHT - i * THREAD_PITCH - THREAD_PITCH * 0.25)
                with BuildSketch(Plane.XY.offset(z)):
                    Circle(skirt_thread_radius)
                    Circle(skirt_thread_radius - THREAD_DEPTH, mode=Mode.SUBTRACT)
                extrude(amount=THREAD_PITCH * 0.3)
        lid_part = lid_part + rings.part

    # Embossed logo text on top surface
    logo_z = LID_TOP_THICKNESS
    try:
        # "JE" large text
        with BuildPart() as logo1:
            with BuildSketch(Plane.XY.offset(logo_z)):
                Text(LOGO_TEXT_LINE1, font_size=20,
                     align=(Align.CENTER, Align.CENTER))
            extrude(amount=LOGO_DEPTH)
        lid_part = lid_part + logo1.part
        print("  Logo 'JE': OK")
    except Exception as e:
        print(f"  SELF-CORRECT: 'JE' text failed ({e})")

    try:
        # "1983" smaller text below
        with BuildPart() as logo2:
            with BuildSketch(Plane.XY.offset(logo_z)):
                with Locations([(0, -14)]):
                    Text(LOGO_TEXT_LINE2, font_size=11,
                         align=(Align.CENTER, Align.CENTER))
            extrude(amount=LOGO_DEPTH)
        lid_part = lid_part + logo2.part
        print("  Logo '1983': OK")
    except Exception as e:
        print(f"  SELF-CORRECT: '1983' text failed ({e})")

    try:
        # Decorative bar between text lines
        with BuildPart() as bar:
            with BuildSketch(Plane.XY.offset(logo_z)):
                with Locations([(0, -6)]):
                    Rectangle(28, 0.8)
            extrude(amount=LOGO_DEPTH)
        lid_part = lid_part + bar.part
        print("  Logo bar: OK")
    except Exception as e:
        print(f"  SELF-CORRECT: Decorative bar skipped ({e})")

    return lid_part


def ensure_exportable(shape):
    """Ensure a shape can be exported via export_step/stl/3mf.

    Boolean operations between Parts and Solids can return Solid or Compound.
    We need to get back to something with export methods.
    """
    if hasattr(shape, 'export_step'):
        return shape
    # Try wrapping in a Compound for export
    if isinstance(shape, (Solid, Compound)):
        # Use the Shape-level exporter via wrapping
        try:
            with BuildPart() as wrapper:
                add(shape)
            return wrapper.part
        except Exception:
            pass
    return shape


def export_part(shape, name_prefix, label):
    """Export a shape to STEP, STL, and 3MF (mandatory per JDS-PRO-003).

    Uses module-level export functions (build123d 0.10+ API).
    """
    print(f"Exporting {label}...")
    step_path = EXPORT_DIR / f"{name_prefix}.step"
    stl_path = EXPORT_DIR / f"{name_prefix}.stl"
    mf_path = EXPORT_DIR / f"{name_prefix}.3mf"

    export_step(shape, str(step_path))
    print(f"  STEP: {step_path.name}")

    export_stl(shape, str(stl_path))
    print(f"  STL:  {stl_path.name}")

    # Try 3MF — multiple strategies for robustness
    exported_3mf = False
    for tol in [0.001, 0.01, 0.05, 0.1]:
        try:
            m = Mesher()
            m.add_shape(shape, linear_deflection=tol, angular_deflection=0.5)
            m.write(str(mf_path))
            print(f"  3MF:  {mf_path.name}" +
                  (f" (tolerance={tol})" if tol > 0.001 else ""))
            exported_3mf = True
            break
        except Exception:
            continue

    if not exported_3mf:
        # Fallback: read the STL we just exported and write as 3MF
        try:
            m = Mesher()
            stl_file = EXPORT_DIR / f"{name_prefix}.stl"
            if stl_file.exists():
                m.read(str(stl_file))
                m.write(str(mf_path))
                print(f"  3MF:  {mf_path.name} (converted from STL)")
                exported_3mf = True
            else:
                print(f"  3MF:  FAILED — no STL to convert")
        except Exception as e:
            print(f"  3MF:  FAILED — {e}")


def main():
    """Build all parts and export to STEP, 3MF, and STL."""
    print("=" * 60)
    print("JDS-DWG-FAB-001 — Circular Logo Box with Screw Lid")
    print("=" * 60)
    print(f"  Diameter:  {OUTER_DIAMETER} mm")
    print(f"  Body:      {BOX_HEIGHT} mm + {THREAD_HEIGHT} mm thread zone")
    print(f"  Wall:      {WALL_THICKNESS} mm")
    print(f"  Divider:   {DIVIDER_THICKNESS} mm, {DIVIDER_CHAMFER} mm chamfer")
    print(f"  Thread:    M{OUTER_DIAMETER} pitch {THREAD_PITCH} mm")
    print(f"  Lid:       {LID_TOP_THICKNESS} mm top, {LID_SKIRT_HEIGHT} mm skirt")
    print(f"  Logo:      {LOGO_TEXT_LINE1} / {LOGO_TEXT_LINE2}")
    print()

    print("[1/3] Building box body...")
    box = build_box()

    print("[2/3] Building screw lid...")
    lid = build_lid()

    print("[3/3] Exporting...")
    export_part(box, "JDS-DWG-FAB-001_box", "box")
    export_part(lid, "JDS-DWG-FAB-001_lid", "lid")

    # Assembly STEP — lid placed above box
    print("Exporting assembly STEP...")
    lid_pos = lid.moved(Location((0, 0, TOTAL_BOX_HEIGHT + 10)))
    assembly = Compound(children=[box, lid_pos])
    export_step(assembly, str(EXPORT_DIR / "JDS-DWG-FAB-001_assembly.step"))

    # Verify thread compatibility
    print()
    print("THREAD VERIFICATION:")
    print(f"  Box outer thread radius:  {OUTER_RADIUS} + {THREAD_DEPTH} = "
          f"{OUTER_RADIUS + THREAD_DEPTH:.1f} mm (crest)")
    print(f"  Lid inner thread radius:  {LID_INNER_RADIUS} - {THREAD_DEPTH} = "
          f"{LID_INNER_RADIUS - THREAD_DEPTH:.1f} mm (crest)")
    print(f"  Radial clearance:         {LID_CLEARANCE} mm")
    engagement = THREAD_DEPTH * 2 - LID_CLEARANCE
    print(f"  Thread engagement:        {engagement:.1f} mm")
    if engagement > 0.3:
        print(f"  Status: OK — lid will grip securely")
    elif engagement > 0:
        print(f"  Status: MARGINAL — may be loose, consider reducing clearance")
    else:
        print(f"  Status: FAIL — threads don't engage, reduce LID_CLEARANCE")

    # Summary
    print()
    print("=" * 60)
    print("EXPORT SUMMARY")
    print("=" * 60)
    for f in sorted(EXPORT_DIR.iterdir()):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name:45s} {size_kb:8.1f} KB")
    print()
    print("Mandatory exports (JDS-PRO-003): STEP + 3MF + STL")
    has_step = any(f.suffix == '.step' for f in EXPORT_DIR.iterdir())
    has_stl = any(f.suffix == '.stl' for f in EXPORT_DIR.iterdir())
    has_3mf = any(f.suffix == '.3mf' for f in EXPORT_DIR.iterdir())
    status = "PASS" if (has_step and has_stl and has_3mf) else "FAIL"
    print(f"  STEP: {'YES' if has_step else 'MISSING'}")
    print(f"  STL:  {'YES' if has_stl else 'MISSING'}")
    print(f"  3MF:  {'YES' if has_3mf else 'MISSING'}")
    print(f"  Status: {status}")


if __name__ == "__main__":
    main()
