# JDS Image Studio — Local Image Generator

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-001 |
| **Revision** | C |
| **Date** | 2026-04-07 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A fully local, unrestricted image generation and photo editing app. Runs on Apple Silicon via Stable Diffusion. No cloud, no filters, no restrictions.

Double-click to launch. Close to quit. Nothing stays running.

## Modes

| Mode | What It Does |
|------|-------------|
| **txt2img** | Generate images from text prompts |
| **img2img** | Transform photos with a prompt + strength |
| **inpaint** | Paint a mask, regenerate just that area (change outfits, remove items) |
| **edit** | Background removal/replacement, directional lighting effects |

## Key Features

- **Inpainting** — brush over socks, clothes, objects to remove or replace them
- **Background removal** — one click, subject detected automatically (rembg)
- **Background replacement** — describe new background, AI generates it around the subject
- **Lighting effects** — simulate sun, lamp, any direction with warmth control
- **Unrestricted** — no safety filters, no content restrictions, your machine your rules
- **5 curated models** — Realistic Vision v5.1 (default), Deliberate v2, Dreamlike, SD 1.5, SD 2.1
- **Model Manager** — download any HuggingFace model from inside the app
- **Photo negative preset** — one click anti-artifact prompt for clean realistic photos
- **DPM++ 2M Karras** — fast, high-quality sampling
- **Clean shutdown** — close window, model unloaded, memory freed

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| macOS | 12.0+ (Monterey) |
| Chip | Apple M1 / M1 Pro / M2+ |
| RAM | 16 GB |
| Python | 3.10+ |
| Disk | ~5 GB per model |

## Quick Start

### First time

1. Double-click **`setup.command`** in Finder
2. Wait for install (~3 min)

### Every time

1. Double-click **`JDS Image Studio.command`**
2. Model Manager opens on first launch — click **Download & Load** on Realistic Vision
3. Pick a mode, enter a prompt, hit **Generate**

## Project Structure

```
JDS-PRJ-SFW-001_local-image-generator/
    app.py          Entry point (10 lines)
    models.py       Config, constants, model registry
    engine.py       All ML pipelines (txt2img, img2img, inpaint, bg)
    painter.py      Mask painting canvas widget
    lighting.py     Directional light effects
    gui.py          Main window, sidebar, all modes
    setup.command               One-time installer
    JDS Image Studio.command    App launcher
    requirements.txt
    README.md
    CHANGELOG.md
```

## Recommended Models

| Model | Best For |
|-------|----------|
| **Realistic Vision v5.1** | Photorealistic humans, faces (default) |
| Deliberate v2 | Versatile realistic, strong anatomy |
| Dreamlike Photoreal 2.0 | Photorealistic with artistic flair |
| Stable Diffusion 1.5 | Fast, huge LoRA ecosystem |
| Stable Diffusion 2.1 | General purpose baseline |

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| C | 2026-04-07 | N. Johansson | Inpainting, background removal/replacement, lighting effects, subject detection, edit mode, code split into 6 files per JDS |
| B | 2026-04-07 | N. Johansson | Model Manager, double-click launch, realistic human models, DPM++ scheduler, negative presets, clean shutdown |
| A | 2026-04-07 | N. Johansson | Initial release — txt2img, img2img, flat iOS GUI, MPS backend |
