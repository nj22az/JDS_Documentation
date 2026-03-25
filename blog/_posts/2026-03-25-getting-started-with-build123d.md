---
layout: post
title: "Why I Chose build123d for Parametric CAD"
date: 2026-03-25
jeds_no: JEDS-BLG-003
revision: A
---

| **JEDS No.** | JEDS-BLG-003 | **Rev** | A | **Date** | 2026-03-25 |
|---|---|---|---|---|---|

I've been exploring 3D modeling tools for a while now. Blender is excellent for visualization and organic modeling. Shapr3D is intuitive and great for quick concept work on the iPad. But when I wanted to create precise, parametric engineering parts — the kind where you change one dimension and everything updates — I found build123d.

## What is build123d?

[build123d](https://github.com/gumyr/build123d) is a Python-based parametric CAD library. Instead of clicking and dragging in a GUI, you write Python code that describes your geometry. It's built on the Open CASCADE kernel, the same engine behind FreeCAD.

For an engineer who's comfortable with code, this is powerful. Your CAD model becomes a script — version-controllable, parameterizable, and reproducible.

## Why code-based CAD makes sense for engineers

Think about how we work with PLCs. We don't drag and drop logic — we write structured programs with defined inputs and outputs. Parametric CAD in code follows the same philosophy.

Here's a simple example — a flange with bolt holes:

```python
from build123d import *

# Parameters — change these and the whole model updates
od = 120        # outer diameter
id = 60         # inner diameter
thickness = 12  # flange thickness
bolt_pcd = 90   # bolt circle diameter
bolt_d = 10     # bolt hole diameter
n_bolts = 6     # number of bolt holes

# Build the flange
with BuildPart() as flange:
    with BuildSketch():
        Circle(od / 2)
        Circle(id / 2, mode=Mode.SUBTRACT)
    Extrude(amount=thickness)

    # Bolt holes
    with BuildSketch(flange.faces().sort_by(Axis.Z)[-1]):
        with PolarLocations(bolt_pcd / 2, n_bolts):
            Circle(bolt_d / 2, mode=Mode.SUBTRACT)
    Extrude(amount=-thickness, mode=Mode.SUBTRACT)
```

Change `n_bolts` from 6 to 8 and re-run. The model updates. No clicking, no sketching constraints, no feature tree to debug.

## How this fits my workflow

My current setup:

1. **Shapr3D** — quick concept sketches and visual exploration
2. **build123d** — precise parametric parts, especially when I need variants or families of parts
3. **Blender** — rendering, visualization, and anything organic

For engineering parts — brackets, flanges, enclosures, adapters — build123d is becoming my go-to. The fact that it's Python means I can integrate it with calculations, pull dimensions from spreadsheets, or generate families of parts programmatically.

## The learning curve

If you know Python, the learning curve is manageable. The main concepts are:

- **BuildPart** / **BuildSketch** / **BuildLine** — context managers that define what you're building
- **2D operations** — sketching profiles with circles, rectangles, lines
- **3D operations** — Extrude, Revolve, Loft, Sweep
- **Selectors** — finding faces, edges, and vertices to build on or modify

The documentation is solid, and there's an active community. Coming from an engineering background rather than a software one, I found the spatial logic very natural — it maps directly to how you'd describe a part to a machinist.

## What's next

I'm planning to document specific parts I model as I learn. Real engineering components with real constraints, not just tutorial cubes. The kind of content I wished existed when I started.

If you're an engineer curious about code-based CAD, build123d is worth a look. It respects your time and your intelligence.
