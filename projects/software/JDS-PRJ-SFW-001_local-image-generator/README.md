# JDS Image Studio — Local Image Generator

| Field | Value |
|-------|-------|
| **Document No.** | JDS-PRJ-SFW-001 |
| **Revision** | T |
| **Date** | 2026-04-07 |
| **Status** | CURRENT |
| **Author** | N. Johansson |

---

## What Is This?

A fully local image generation and photo editing app, with optional cloud backends for higher quality. Runs on Apple Silicon via Stable Diffusion. No filters, no restrictions.

Double-click to launch. Close to quit. Nothing stays running.

## Modes

| Mode | What It Does |
|------|-------------|
| **txt2img** | Generate images from text prompts (local or cloud) |
| **img2img** | Transform photos with a prompt + strength (local or cloud) |
| **inpaint** | Paint a mask, regenerate just that area (change outfits, remove items) |
| **edit** | Smart masks, inpaint presets, ControlNet, background, lighting, face swap |

## Key Features

- **Smart masking** — auto-detect clothing, skin, body, face regions for targeted editing
- **Inpaint presets** — one-click workflows: remove clothing, change outfit, swimwear, lingerie, artistic nude, enhance body, gravure swimwear/lingerie/portrait
- **ControlNet** — preserve pose/structure while regenerating (openpose, canny edge, depth)
- **Auto Mask + Inpaint** — one-click: detect clothing, apply preset prompt, inpaint
- **Inpainting** — brush over socks, clothes, objects to remove or replace them
- **Background removal** — one click, subject detected automatically (rembg)
- **Background replacement** — describe new background, AI generates it around the subject
- **Lighting effects** — simulate sun, lamp, any direction with warmth control
- **Neural face swap** — ReActor-grade INSwapper model, auto-downloads, Poisson fallback
- **Multi-face swap** — swap all faces in a group photo, similarity-ranked (FaceSwapLab)
- **Diffusion refinement** — optional SD inpaint pass over swapped face to fix artifacts (DiffFace)
- **Face switch** — swap faces between two photos (A's face on B, B's face on A), both results saved
- **Pose quality check** — warns if face is at extreme angle before swapping, proceeds anyway
- **Face checkpoints** — save/reuse faces across sessions (FaceSwapLab concept)
- **Cloud generation** — optional HuggingFace / Prodia / AI Horde backends for SDXL, Flux quality, NSFW-capable models
- **Gravure presets** — optimized prompts for Japanese glamour photography (swimwear, lingerie, portrait)
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
    app.py          Entry point
    models.py       Config, constants, model registry
    engine.py       All ML pipelines (txt2img, img2img, inpaint, bg, upscale)
    painter.py      Mask painting canvas widget
    lighting.py     Directional light effects
    fixer.py        Face/hand auto-detection and fix (Adetailer concept)
    history.py      Auto-save generations with metadata, gallery browser
    prompts.py      Dynamic prompt templating {a|b|c}
    consistency.py  Character identity persistence (IP-Adapter)
    faceswap.py     Neural face swap (ReActor + FaceSwapLab + DiffFace)
    smartmask.py    Smart auto-masking (clothing, skin, body, face)
    cloudgen.py     Cloud backends (HuggingFace, Prodia, AI Horde)
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
| T | 2026-04-07 | N. Johansson | Gravure photography presets: 3 inpaint presets (swimwear, lingerie, portrait) + 1 negative prompt preset with optimized prompts for Japanese glamour photography. Version 4.1.0 |
| R | 2026-04-07 | N. Johansson | Full 7-point code audit per JDS-PRO-004. Fixed: critical Image import bug in engine.py, removed dead code (_gen, NEG_PHOTO, IP_ADAPTER_FACEID, unused import), consolidated 6 duplicate _bg() into shared bg_thread(), extracted 30+ hardcoded values to models.py config, centralized 3 missing UI colours. Version 4.0.0 |
| P | 2026-04-07 | N. Johansson | Smart masking (clothing/skin/body/face auto-detection via rembg + HSV/YCrCb skin detection), ControlNet (openpose/canny/depth for pose preservation), inpaint workflow presets (7 presets), one-click Auto Mask + Inpaint. New smartmask.py (184 lines). 13 files, 3774 total lines |
| N | 2026-04-07 | N. Johansson | Expanded cloud model registry with NSFW-capable models. AI Horde default (free, no key, unrestricted). Added WAI-NSFW SDXL, AlbedoBase XL, ICBINP XL, Pony Diffusion XL, PPP to Horde. WAI-NSFW SDXL on HuggingFace. All backends pass nsfw:true/censor_nsfw:false flags |
| M | 2026-04-07 | N. Johansson | Cloud generation: three free backends (HuggingFace Inference API, Prodia, AI Horde). Toggle "Use Cloud" for SDXL/Flux quality without local GPU load. Backend selector, cloud model picker, API key settings popup. New cloudgen.py module (315 lines) |
| L | 2026-04-07 | N. Johansson | Face pose quality scoring: detects extreme angles using landmark symmetry, warns before swap. Works with any pose/size/angle difference — neural swap handles alignment automatically |
| K | 2026-04-07 | N. Johansson | Bidirectional face switch: upload two photos, faces swap both ways. Primary shown on screen, second auto-saved to history |
| J | 2026-04-07 | N. Johansson | Neural face swap (ReActor INSwapper + FaceSwapLab landmark masks + DiffFace refinement). Auto-downloads swapper model, convex hull masking, Lab colour correction, face similarity ranking, face checkpoints, optional SD inpaint refinement |
| H | 2026-04-07 | N. Johansson | Face swap: warp source face onto target with affine alignment, Poisson seamless blending, colour correction. Single and multi-face swap modes |
| G | 2026-04-07 | N. Johansson | Character identity consistency (IP-Adapter concept): save a face, generate new scenes keeping the same person. insightface for face embedding |
| F | 2026-04-07 | N. Johansson | Face auto-fix (Adetailer), image history gallery, dynamic prompts {a|b|c}, inspired by Forge ecosystem research |
| E | 2026-04-07 | N. Johansson | Upscaling: Real-ESRGAN 2x/4x upscaler + Hires Fix (model-based detail enhancement), capped at 1536px for 16GB safety |
| D | 2026-04-07 | N. Johansson | Error dialogs, dependency checker, body proportion presets (4 negative prompt presets), syntax validated |
| C | 2026-04-07 | N. Johansson | Inpainting, background removal/replacement, lighting effects, subject detection, edit mode, code split into 6 files per JDS |
| B | 2026-04-07 | N. Johansson | Model Manager, double-click launch, realistic human models, DPM++ scheduler, negative presets, clean shutdown |
| A | 2026-04-07 | N. Johansson | Initial release — txt2img, img2img, flat iOS GUI, MPS backend |
