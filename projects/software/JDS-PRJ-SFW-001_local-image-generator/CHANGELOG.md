# Changelog — JDS Image Studio

> JDS-PRJ-SFW-001 — Local Image Generator

## How to Read This Log

Each entry records what changed, when, and why. Latest changes appear first.

---

| Date | Document | Rev | Author | What Changed |
|------|----------|-----|--------|-------------|
| 2026-04-07 | JDS-PRJ-SFW-001 | K | N. Johansson | Bidirectional face switch: upload two photos, faces swap both ways (A→B and B→A). Primary result shown on screen, second auto-saved to history. New bidi_swap() function with chained diffusion refinement for both results. "Switch" button in GUI |
| 2026-04-07 | JDS-PRJ-SFW-001 | J | N. Johansson | Neural face swap rewrite implementing ReActor (INSwapper ONNX neural swap with auto-download), FaceSwapLab (landmark convex hull masks, face similarity ranking, face checkpoints for reuse), and DiffFace (optional SD inpaint refinement over swapped area). Lab-space colour correction, Poisson fallback when no swapper model. GUI: model download button, checkpoint dropdown, refine toggle |
| 2026-04-07 | JDS-PRJ-SFW-001 | H | N. Johansson | Face swap: warp source face onto target photo with insightface alignment, Poisson seamless blending, per-channel colour correction. Single swap + multi-swap (all faces in target). New faceswap.py module, integrated into edit mode GUI panel |
| 2026-04-07 | JDS-PRJ-SFW-001 | G | N. Johansson | Character identity consistency: save face identity from any image (insightface embedding), generate new scenes/outfits with the same person (IP-Adapter + fallback img2img), identity strength slider (0.3-1.0), identity manager in edit mode, saved identities persist at ~/.jds-image-studio/faces/. Inspired by Forge RefDrop/IP-Adapter/ReActor ecosystem |
| 2026-04-07 | JDS-PRJ-SFW-001 | F | N. Johansson | Face auto-fix (Adetailer concept): OpenCV face detection + targeted high-res inpaint per face. Image history: auto-saves every generation with metadata JSON, gallery browser with thumbnails, load-from-history restores prompt and seed. Dynamic prompts: {a|b|c} random selection syntax with nesting. Inspired by Forge ecosystem (Adetailer, Infinite Image Browsing, Dynamic Prompts). opencv-python added to requirements |
| 2026-04-07 | JDS-PRJ-SFW-001 | E | N. Johansson | Upscaling: Real-ESRGAN 2x/4x neural upscaler, Hires Fix (Lanczos + img2img detail pass), toolbar buttons, 1536px memory cap for 16GB, realesrgan and basicsr added to requirements |
| 2026-04-07 | JDS-PRJ-SFW-001 | D | N. Johansson | Error dialog popups on all failure points, startup dependency checker with dialog, 4 negative prompt presets (general photo, realistic body proportions, portrait face, artistic minimal), body proportion negative prompt fixes oversized/disproportionate anatomy, numpy added to requirements |
| 2026-04-07 | JDS-PRJ-SFW-001 | C | N. Johansson | Inpainting (paint mask, regenerate area), background removal (rembg), background replacement (AI), directional lighting effects, subject detection, edit mode, code split into 6 files per JDS, 5 curated models including Deliberate v2, numpy dependency for lighting |
| 2026-04-07 | JDS-PRJ-SFW-001 | B | N. Johansson | Model Manager with download/load, double-click launch (.command files), curated realistic-human models (Realistic Vision v5.1 default), DPM++ 2M Karras scheduler, photo negative preset, size presets, copy seed, clean shutdown with memory cleanup |
| 2026-04-07 | JDS-PRJ-SFW-001 | A | N. Johansson | Initial release — text-to-image, image-to-image, flat iOS-style GUI, Apple MPS backend, unrestricted generation, model selector, seed control |
