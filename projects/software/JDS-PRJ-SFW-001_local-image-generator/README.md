# JDS Image Studio — Local Image Generator

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-001 |
| **Revision** | A |
| **Date** | 2026-04-07 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A fully local, unrestricted image generation desktop app that runs on Apple Silicon using Stable Diffusion. No cloud, no internet required after model download, no content filters. Your machine, your rules.

## Key Features

- **Text-to-Image** — Generate images from text prompts
- **Image-to-Image** — Transform existing photos with a prompt and strength control
- **No safety filters** — Full unrestricted generation (safety checker disabled)
- **Flat iOS-style GUI** — Clean, modern interface built with CustomTkinter
- **Apple Silicon optimised** — Runs on MPS (Metal Performance Shaders) backend
- **Any model** — Load HuggingFace models or local .safetensors model folders
- **Seed control** — Reproduce results with explicit seed values

## System Requirements

| Requirement | Minimum |
|-------------|---------|
| macOS | 12.0+ (Monterey) |
| Chip | Apple M1 / M1 Pro / M2+ |
| RAM | 16 GB |
| Python | 3.10+ |
| Disk | ~5 GB per model |

## Quick Start

```bash
# 1. Navigate to the project
cd projects/software/JDS-PRJ-SFW-001_local-image-generator/

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the app
python3 app.py
```

On first run, click **Load Model** to download the default model (~5 GB). Subsequent launches use the cached model.

## How It Works

```
User prompt → Diffusers pipeline (MPS) → Generated image → Preview & save
```

1. The app loads a Stable Diffusion model via HuggingFace Diffusers
2. The model runs on Apple's Metal backend (MPS) — fully on-device
3. Generated images display in the preview panel
4. Save to disk in PNG or JPEG format

## Recommended Models for M1 Pro 16GB

| Model | Size | Notes |
|-------|------|-------|
| `stabilityai/stable-diffusion-2-1` | ~5 GB | Default, good general quality |
| `runwayml/stable-diffusion-v1-5` | ~4 GB | Lighter, faster |
| `prompthero/openjourney-v4` | ~4 GB | Stylised art |
| Any local .safetensors folder | Varies | Browse to folder in app |

## Project Structure

```
JDS-PRJ-SFW-001_local-image-generator/
    app.py              # Main application (GUI + generation engine)
    requirements.txt    # Python dependencies
    README.md           # This file (project card)
    CHANGELOG.md        # All revisions tracked here
```

## Configuration

Settings are saved to `~/.jds-image-studio/config.json` and persist between sessions:
- Last used model
- Default image dimensions
- Default steps and guidance scale
- Output directory

## Revision History

| Rev | Date | Author | Description |
|-----|------|--------|-------------|
| A | 2026-04-07 | N. Johansson | Initial release — txt2img, img2img, flat iOS GUI, MPS backend |
