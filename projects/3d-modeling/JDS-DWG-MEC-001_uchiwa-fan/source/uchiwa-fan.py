"""
JDS-DWG-MEC-001 — Uchiwa Fan (flat Japanese hand fan) in locking pieces
Parametric CAD model using build123d

Three printed parts:
- Blade left half  — ribbed panel, puzzle-dovetail tabs sockets, detent bump
- Blade right half — ribbed panel, puzzle-dovetail tabs, detent bump
- Handle           — dovetail channel socket that clamps the blade seam,
                     closed floor as depth stop, snap-detent windows

Locking principle: the two blade halves join edge-to-edge with flared
puzzle-dovetail tabs; the bottom 40 mm of the joined stem forms a
dovetail-profile tang that slides down into the handle channel. The
channel walls clamp the seam shut, the floor stops insertion, and a
spherical detent bump on each half clicks into a through-window in the
handle front wall (push a pin through the window to release).

All dimensions in mm. Designed for FDM printing in PETG.
Each blade half fits a 220 x 220 mm bed at the full 240 mm fan width.

Self-correcting: fillets, chamfers, text and 2D offsets that can fail
are wrapped with fallback logic and parameter reduction (JDS pattern,
see JDS-DWG-FAB-001).
"""

from build123d import *
from math import cos, sin, radians, tan
from pathlib import Path

# ── Design Parameters ──────────────────────────────────────────────
# Printer / material (PETG)
BED_SIZE = 220.0            # mm — each part must fit this square
THICKNESS_CLEARANCE = 0.25  # mm — socket gap on tang top/bottom faces
WIDTH_CLEARANCE = 0.20      # mm — socket gap on tang side faces
SEAM_CLEARANCE = 0.20       # mm — gap on blade-half puzzle tabs

# Blade head (the paddle)
HEAD_WIDTH = 240.0          # mm — full traditional uchiwa width
HEAD_HEIGHT = 180.0         # mm — 180 fits a 220 bed; 220 = authentic
STEM_WIDTH = 21.0           # mm — stem below the head, also tang width
STEM_TOP_Y = 45.0           # mm — stem rectangle reaches into the head
NECK_FILLET_RADIUS = 10.0   # mm — 2D fillet where stem meets head

# Blade panel and ribs
PANEL_THICKNESS = 1.2       # mm — membrane thickness
RIB_HEIGHT = 0.8            # mm — ribs proud of the panel top
RIB_WIDTH = 2.5             # mm
RIM_WIDTH = 3.0             # mm — stiffening rim around the outline
RIB_ANGLES_DEG = [35, 50, 65, 80, 100, 115, 130, 145]  # none at 90 (seam)
RIB_FOCAL_Y = -10.0         # mm — ribs radiate from (0, RIB_FOCAL_Y)
RIB_LENGTH = 260.0          # mm — long enough to reach the head edge

# Dovetail tang (bottom 40 mm of the stem, thickened boss)
TANG_LENGTH = 40.0          # mm — engagement depth in the handle
TANG_THICKNESS = 6.0        # mm — boss thickness incl. panel
DOVETAIL_ANGLE_DEG = 12.0   # deg — flank angle of the dovetail
BOSS_TAPER_END_Y = 70.0     # mm — boss tapers back to panel by here

# Snap detent
BUMP_RADIUS = 3.0           # mm — detent sphere radius
BUMP_PROUD = 0.6            # mm — bump height above the tang top face
BUMP_X = 5.0                # mm — one bump per half at +/- BUMP_X
BUMP_Y = 8.0                # mm — bump centre above blade bottom edge
WINDOW_RADIUS = 3.5         # mm — through-window in the handle wall

# Seam puzzle-dovetail tabs (on the right half, sockets on the left)
TAB_CENTRES_Y = [80.0, 130.0, 180.0]   # mm
TAB_ROOT_HALF = 7.0         # mm — half length of tab at the seam
TAB_TIP_HALF = 10.0         # mm — half length at the tip (flare = lock)
TAB_DEPTH = 8.0             # mm — how far tabs reach into the left half

# Handle
HANDLE_LENGTH = 130.0       # mm
HANDLE_WIDTH = 30.0         # mm — ellipse major (side to side)
HANDLE_THICKNESS = 16.0     # mm — ellipse minor (front to back)
HANDLE_FLAT_OFFSET = 6.4    # mm — flat back cut below axis (print face)
MOUTH_CHAMFER = 1.2         # mm — lead-in on the socket mouth
BOTTOM_FILLET = 5.0         # mm — rounded handle end
ENGRAVE_TEXT = "JE 1983"
ENGRAVE_FONT_SIZE = 7.0     # mm
ENGRAVE_CUT_DEPTH = 2.5     # mm — prism depth; net depth ~1.5 on crown

# ── Derived values ─────────────────────────────────────────────────
HEAD_CENTRE_Y = TANG_LENGTH + HEAD_HEIGHT / 2          # ellipse centre
BLADE_TOP_Y = TANG_LENGTH + HEAD_HEIGHT                # top of the fan
STEM_HALF = STEM_WIDTH / 2
DOVETAIL_SLOPE = tan(radians(DOVETAIL_ANGLE_DEG))
TANG_TOP_HALF = STEM_HALF - TANG_THICKNESS * DOVETAIL_SLOPE
RIB_TOP_Z = PANEL_THICKNESS + RIB_HEIGHT
BUMP_CENTRE_Z = TANG_THICKNESS - (BUMP_RADIUS - BUMP_PROUD)
HANDLE_TOP_Y = TANG_LENGTH                             # handle mouth
HANDLE_BOTTOM_Y = HANDLE_TOP_Y - HANDLE_LENGTH
DOC_NO = "JDS-DWG-MEC-001"

EXPORT_DIR = Path(__file__).parent.parent / "exports"
EXPORT_DIR.mkdir(exist_ok=True)


def attempt(operation, label, fallbacks=()):
    """Try an operation, then each fallback; report self-correction."""
    candidates = [operation, *fallbacks]
    for index, candidate in enumerate(candidates):
        try:
            result = candidate()
            if index > 0:
                print(f"  SELF-CORRECT: {label} used fallback {index}")
            return result
        except Exception as error:
            last_error = error
    print(f"  SELF-CORRECT: {label} skipped — {last_error}")
    return None


def blade_outline() -> Sketch:
    """2D outline of the whole fan: elliptical head + straight stem."""
    with BuildSketch() as outline:
        with Locations((0, HEAD_CENTRE_Y)):
            Ellipse(HEAD_WIDTH / 2, HEAD_HEIGHT / 2)
        Polygon(
            (-STEM_HALF, 0), (STEM_HALF, 0),
            (STEM_HALF, STEM_TOP_Y), (-STEM_HALF, STEM_TOP_Y),
            align=None,
        )
        junction_vertices = [
            vertex for vertex in outline.vertices()
            if 8 < abs(vertex.X) < 14 and 38 < vertex.Y < 48
        ]
        if junction_vertices:
            attempt(
                lambda: fillet(junction_vertices, NECK_FILLET_RADIUS),
                "neck fillet",
                fallbacks=(
                    lambda: fillet(junction_vertices, NECK_FILLET_RADIUS * 0.5),
                    lambda: fillet(junction_vertices, NECK_FILLET_RADIUS * 0.2),
                ),
            )
    return outline.sketch


def rib_pattern(outline: Sketch) -> Sketch:
    """Radiating ribs clipped to the outline shrunk by 1 mm."""
    clip = offset(outline, amount=-1.0)
    with BuildSketch() as ribs:
        for angle_deg in RIB_ANGLES_DEG:
            direction_x = cos(radians(angle_deg))
            direction_y = sin(radians(angle_deg))
            centre = (
                direction_x * RIB_LENGTH / 2,
                RIB_FOCAL_Y + direction_y * RIB_LENGTH / 2,
            )
            with Locations(Location(centre, angle_deg)):
                Rectangle(RIB_LENGTH, RIB_WIDTH)
    return ribs.sketch & clip


def build_blade() -> Part:
    """Full one-piece blade: panel, rim, ribs, tang boss, detent bumps."""
    outline = blade_outline()

    panel = extrude(outline, PANEL_THICKNESS)

    rim = extrude(outline - offset(outline, amount=-RIM_WIDTH), RIB_HEIGHT)
    rim = rim.moved(Location((0, 0, PANEL_THICKNESS)))

    ribs = extrude(rib_pattern(outline), RIB_HEIGHT)
    ribs = ribs.moved(Location((0, 0, PANEL_THICKNESS)))

    # Tang boss: dovetail prism over y 0..TANG_LENGTH that tapers back
    # to the panel by BOSS_TAPER_END_Y (ruled loft between rectangles).
    boss_base = Pos(0, BOSS_TAPER_END_Y / 2, 0) * Rectangle(
        STEM_WIDTH, BOSS_TAPER_END_Y
    )
    boss_top = Pos(0, TANG_LENGTH / 2, TANG_THICKNESS) * Rectangle(
        TANG_TOP_HALF * 2, TANG_LENGTH
    )
    boss = loft([boss_base, boss_top], ruled=True)

    bumps = [
        Pos(sign * BUMP_X, BUMP_Y, BUMP_CENTRE_Z) * Sphere(BUMP_RADIUS)
        for sign in (1, -1)
    ]

    blade = panel + rim + ribs + boss + bumps[0] + bumps[1]

    # The neck fillet flares the outline below the socket mouth; the
    # blade must stay prismatic over the full engagement depth, so trim
    # everything wider than the stem inside the socket zone (y < 40).
    for sign in (1, -1):
        trim = Pos(
            sign * (STEM_HALF + 75), TANG_LENGTH / 2 - 2.5, 5
        ) * Box(150, TANG_LENGTH + 5, 25)
        blade -= trim
    return blade


def seam_parting_sketch() -> Sketch:
    """Closed polygon covering the right side of the seam incl. tabs."""
    points = [(0, -5)]
    for centre_y in TAB_CENTRES_Y:
        points += [
            (0, centre_y - TAB_ROOT_HALF),
            (-TAB_DEPTH, centre_y - TAB_TIP_HALF),
            (-TAB_DEPTH, centre_y + TAB_TIP_HALF),
            (0, centre_y + TAB_ROOT_HALF),
        ]
    points += [(0, BLADE_TOP_Y + 10), (135, BLADE_TOP_Y + 10), (135, -5)]
    with BuildSketch() as parting:
        Polygon(*points, align=None)
    return parting.sketch


def split_blade(blade: Part) -> tuple:
    """Split the blade into halves with SEAM_CLEARANCE on the left cut."""
    parting = seam_parting_sketch()
    grown = attempt(
        lambda: offset(parting, amount=SEAM_CLEARANCE, kind=Kind.INTERSECTION),
        "seam clearance offset",
        fallbacks=(
            lambda: offset(parting, amount=SEAM_CLEARANCE, kind=Kind.ARC),
        ),
    )
    base_plane = Plane.XY.offset(-2)
    right_prism = extrude(base_plane * parting, TANG_THICKNESS + 4)
    grown_prism = extrude(base_plane * grown, TANG_THICKNESS + 4)
    return blade - grown_prism, blade & right_prism


def build_handle() -> Part:
    """Handle with dovetail channel socket, windows, engraving.

    Modelled in its own frame (axis = +Z, profile in XY, flat back at
    frame y=-HANDLE_FLAT_OFFSET), then transformed into blade coordinates
    so the socket lines up with the tang at y 0..TANG_LENGTH.
    """
    profile = Ellipse(HANDLE_WIDTH / 2, HANDLE_THICKNESS / 2) - Pos(
        0, -HANDLE_FLAT_OFFSET - 25
    ) * Rectangle(HANDLE_WIDTH + 20, 50)
    body = extrude(profile, HANDLE_LENGTH)

    # Socket channel: blade z maps to frame y - TANG_THICKNESS/2; the
    # profile follows panel (straight) then dovetail flank, + clearance.
    half_thickness = TANG_THICKNESS / 2
    floor_frame_z = HANDLE_LENGTH - TANG_LENGTH
    panel_top = PANEL_THICKNESS + THICKNESS_CLEARANCE - half_thickness
    cavity_top = half_thickness + THICKNESS_CLEARANCE
    flank_slope = (STEM_HALF - TANG_TOP_HALF) / (
        TANG_THICKNESS - PANEL_THICKNESS
    )
    top_half_width = (
        STEM_HALF
        - flank_slope * (TANG_THICKNESS + THICKNESS_CLEARANCE - PANEL_THICKNESS)
        + WIDTH_CLEARANCE
    )
    wide_half = STEM_HALF + WIDTH_CLEARANCE
    with BuildSketch(Plane.XY.offset(floor_frame_z)) as channel:
        Polygon(
            (-wide_half, -half_thickness - THICKNESS_CLEARANCE),
            (wide_half, -half_thickness - THICKNESS_CLEARANCE),
            (wide_half, panel_top),
            (top_half_width, cavity_top),
            (-top_half_width, cavity_top),
            (-wide_half, panel_top),
            align=None,
        )
    body -= extrude(channel.sketch, TANG_LENGTH + 1)

    # Detent windows through the front wall (frame +y side)
    window_frame_z = floor_frame_z + BUMP_Y
    for sign in (1, -1):
        window = Pos(sign * BUMP_X, 7, window_frame_z) * Rot(X=-90) * Cylinder(
            WINDOW_RADIUS, 10
        )
        body -= window

    # Rounded bottom end
    bottom_edges = body.edges().group_by(Axis.Z)[0]
    body = attempt(
        lambda: fillet(bottom_edges, BOTTOM_FILLET),
        "handle bottom fillet",
        fallbacks=(lambda: fillet(bottom_edges, BOTTOM_FILLET * 0.5),),
    ) or body

    # Lead-in chamfer on the socket mouth
    mouth_edges = [
        edge for edge in body.edges()
        if abs(edge.center().Z - HANDLE_LENGTH) < 0.1
        and abs(edge.center().X) < STEM_HALF + 2
        and abs(edge.center().Y) < half_thickness + 2
    ]
    if mouth_edges:
        body = attempt(
            lambda: chamfer(mouth_edges, MOUTH_CHAMFER),
            "socket mouth chamfer",
            fallbacks=(lambda: chamfer(mouth_edges, MOUTH_CHAMFER * 0.5),),
        ) or body

    # Into blade coordinates: frame (x,y,z) -> (-x, z-offset, y+centre)
    body = body.rotate(Axis.X, 90).rotate(Axis.Z, 180)
    body = body.moved(
        Location((0, HANDLE_TOP_Y - HANDLE_LENGTH, half_thickness))
    )

    # Engrave brand text on the front (crown) face, reading upward
    def engrave():
        text_sketch = Pos(0, HANDLE_BOTTOM_Y + 45, half_thickness + 9) * Text(
            ENGRAVE_TEXT, font_size=ENGRAVE_FONT_SIZE, rotation=90
        )
        return body - extrude(text_sketch, -ENGRAVE_CUT_DEPTH)

    return attempt(engrave, "handle engraving") or body


def export_part(shape, name_suffix, label):
    """Export STEP + STL + 3MF (mandatory per JDS-PRO-003)."""
    print(f"Exporting {label}...")
    stem = f"{DOC_NO}_{name_suffix}"
    export_step(shape, str(EXPORT_DIR / f"{stem}.step"))
    export_stl(shape, str(EXPORT_DIR / f"{stem}.stl"))
    for tolerance in (0.01, 0.05, 0.1):
        try:
            mesher = Mesher()
            mesher.add_shape(shape, linear_deflection=tolerance)
            mesher.write(str(EXPORT_DIR / f"{stem}.3mf"))
            print(f"  STEP + STL + 3MF: {stem}")
            return
        except Exception:
            continue
    print(f"  3MF FAILED for {stem} — STEP + STL written")


def verify_fit(blade_left, blade_right, handle):
    """Automated interference and bed-fit checks."""
    print()
    print("FIT VERIFICATION:")
    halves_overlap = (blade_left & blade_right).volume
    print(f"  Blade halves overlap:      {halves_overlap:.3f} mm3 "
          f"({'OK' if halves_overlap < 0.01 else 'FAIL'})")
    for label, half in (("left", blade_left), ("right", blade_right)):
        overlap = (half & handle).volume
        print(f"  Handle vs blade {label}:     {overlap:.3f} mm3 "
              f"({'OK' if overlap < 0.01 else 'FAIL'})")
    print()
    print("BED FIT (max footprint per part):")
    for label, part in (
        ("blade left", blade_left),
        ("blade right", blade_right),
        ("handle", handle),
    ):
        size = part.bounding_box().size
        largest = max(size.X, size.Y)
        status = "OK" if largest <= BED_SIZE + 0.01 else "TOO BIG"
        print(f"  {label:12s} {size.X:6.1f} x {size.Y:6.1f} mm  {status}")
    print()
    print("LOCK GEOMETRY:")
    undercut = TANG_THICKNESS * DOVETAIL_SLOPE
    print(f"  Dovetail undercut/side:    {undercut:.2f} mm "
          f"(vs {WIDTH_CLEARANCE} mm clearance — "
          f"{'captures' if undercut > WIDTH_CLEARANCE else 'FAIL'})")
    detent_grip = BUMP_PROUD - THICKNESS_CLEARANCE
    print(f"  Detent engagement:         {detent_grip:.2f} mm "
          f"({'OK' if detent_grip > 0.2 else 'WEAK'})")
    tab_flare = TAB_TIP_HALF - TAB_ROOT_HALF
    print(f"  Seam tab flare:            {tab_flare:.1f} mm "
          f"(vs {SEAM_CLEARANCE} mm clearance — "
          f"{'captures' if tab_flare > SEAM_CLEARANCE else 'FAIL'})")


def render_previews(blade_left, blade_right, handle):
    """Shaded PNG previews via matplotlib (lazy import; optional)."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plot
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        import numpy
        from stl import mesh as stl_mesh
    except ImportError as error:
        print(f"Render skipped — {error}")
        return

    render_dir = EXPORT_DIR.parent / "renders"
    render_dir.mkdir(exist_ok=True)
    part_files = {
        "blade-left": "#4A90A4",
        "blade-right": "#4A90A4",
        "handle": "#1B3A5C",
    }
    layouts = {
        "assembly": {"blade-left": (0, 0), "blade-right": (0, 0),
                     "handle": (0, 0)},
        "parts": {"blade-left": (-20, 0), "blade-right": (20, 0),
                  "handle": (185, 60)},
    }
    view_elev, view_azim = 60, -90
    view_vector = numpy.array([
        cos(radians(view_elev)) * cos(radians(view_azim)),
        cos(radians(view_elev)) * sin(radians(view_azim)),
        sin(radians(view_elev)),
    ])
    for view_name, offsets in layouts.items():
        figure = plot.figure(figsize=(10, 10))
        axes = figure.add_subplot(projection="3d")
        all_points = []
        for suffix, colour in part_files.items():
            loaded = stl_mesh.Mesh.from_file(
                str(EXPORT_DIR / f"{DOC_NO}_{suffix}.stl")
            )
            triangles = loaded.vectors + numpy.array(
                [*offsets[suffix], 0], dtype=numpy.float32
            )
            normals = numpy.cross(
                triangles[:, 1] - triangles[:, 0],
                triangles[:, 2] - triangles[:, 0],
            )
            lengths = numpy.linalg.norm(normals, axis=1, keepdims=True)
            normals = normals / numpy.clip(lengths, 1e-9, None)
            # Cull triangles facing away from the camera — matplotlib
            # has no z-buffer, so hidden faces would paint over visible
            facing = normals @ view_vector > 0
            triangles, normals = triangles[facing], normals[facing]
            light = numpy.clip(normals @ numpy.array([0.3, -0.4, 0.87]),
                               0.35, 1.0)
            base = numpy.array(matplotlib.colors.to_rgb(colour))
            face_colours = numpy.clip(base * light[:, None], 0, 1)
            collection = Poly3DCollection(
                triangles, facecolors=face_colours, edgecolor="none",
                zsort="average",
            )
            axes.add_collection3d(collection)
            all_points.append(triangles.reshape(-1, 3))
        points = numpy.concatenate(all_points)
        centre = (points.max(axis=0) + points.min(axis=0)) / 2
        radius = (points.max(axis=0) - points.min(axis=0)).max() / 2
        axes.set_xlim(centre[0] - radius, centre[0] + radius)
        axes.set_ylim(centre[1] - radius, centre[1] + radius)
        axes.set_zlim(centre[2] - radius, centre[2] + radius)
        axes.view_init(elev=view_elev, azim=view_azim)
        axes.set_axis_off()
        output = render_dir / f"{DOC_NO}_{view_name}.png"
        figure.savefig(output, dpi=110, bbox_inches="tight",
                       facecolor="white")
        plot.close(figure)
        print(f"  Render: {output.name}")


def main():
    print("=" * 60)
    print(f"{DOC_NO} — Uchiwa Fan (blade halves + locking handle)")
    print("=" * 60)
    print(f"  Head:    {HEAD_WIDTH} x {HEAD_HEIGHT} mm, "
          f"panel {PANEL_THICKNESS} mm + {RIB_HEIGHT} mm ribs")
    print(f"  Tang:    {STEM_WIDTH} mm dovetail, {TANG_LENGTH} mm deep, "
          f"{DOVETAIL_ANGLE_DEG} deg flanks")
    print(f"  Handle:  {HANDLE_LENGTH} x {HANDLE_WIDTH} x "
          f"{HANDLE_THICKNESS} mm, flat print back")
    print(f"  Overall: {BLADE_TOP_Y - HANDLE_BOTTOM_Y:.0f} mm assembled")
    print()

    print("[1/4] Building one-piece blade...")
    blade = build_blade()

    print("[2/4] Splitting blade at the seam...")
    blade_left, blade_right = split_blade(blade)

    print("[3/4] Building handle...")
    handle = build_handle()

    print("[4/4] Exporting (STEP + STL + 3MF per JDS-PRO-003)...")
    export_part(blade_left, "blade-left", "blade left half")
    export_part(blade_right, "blade-right", "blade right half")
    export_part(handle, "handle", "handle")
    assembly = Compound(children=[blade_left, blade_right, handle])
    export_step(assembly, str(EXPORT_DIR / f"{DOC_NO}_assembly.step"))
    print(f"  Assembly STEP: {DOC_NO}_assembly.step")

    verify_fit(blade_left, blade_right, handle)

    print()
    print("Rendering previews...")
    render_previews(blade_left, blade_right, handle)

    print()
    print("EXPORT SUMMARY")
    for file in sorted(EXPORT_DIR.iterdir()):
        if file.name.startswith(DOC_NO):
            print(f"  {file.name:42s} {file.stat().st_size / 1024:8.1f} KB")


if __name__ == "__main__":
    main()
