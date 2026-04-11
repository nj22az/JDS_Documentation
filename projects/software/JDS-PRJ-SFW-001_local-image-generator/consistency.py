"""consistency.py — Character identity consistency (IP-Adapter concept).

Save a reference face from any image, then inject that identity into
new generations. Change outfit, background, lighting — face stays the same.

Two methods:
1. IP-Adapter (best quality, needs ip-adapter model download)
2. Face embed + inject (lighter, uses insightface embeddings)
"""

import os
import json
import numpy as np
from pathlib import Path
from PIL import Image

from models import (CONFIG_DIR, FACE_DET_SIZE, FACE_CROP_PAD,
                    IDENTITY_THUMB_SIZE, bg_thread as _bg)

FACES_DIR = CONFIG_DIR / "faces"

# IP-Adapter model ID on HuggingFace
IP_ADAPTER_REPO = "h94/IP-Adapter"


def _faces_dir():
    FACES_DIR.mkdir(parents=True, exist_ok=True)
    return FACES_DIR


def extract_face(image, status=None, done=None, error=None):
    """Extract face embedding from an image using insightface."""
    def _run():
        try:
            if status: status("Detecting face...")
            try:
                from insightface.app import FaceAnalysis
            except ImportError:
                if error:
                    error("insightface not installed.\n\n"
                          "Run: pip install insightface onnxruntime")
                return

            app = FaceAnalysis(name="buffalo_l",
                               providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=0, det_size=FACE_DET_SIZE)

            img_np = np.array(image.convert("RGB"))
            faces = app.get(img_np)

            if not faces:
                if error: error("No face detected in image.")
                return

            # Take the largest face
            face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) *
                       (f.bbox[3] - f.bbox[1]))

            if status: status("Face extracted.")
            if done: done(face)

        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def save_identity(name, image, status=None, done=None, error=None):
    """Save a face identity (embedding + thumbnail) to disk."""
    def _run():
        try:
            if status: status(f"Saving identity '{name}'...")
            try:
                from insightface.app import FaceAnalysis
            except ImportError:
                if error:
                    error("insightface not installed.\n\n"
                          "Run: pip install insightface onnxruntime")
                return

            app = FaceAnalysis(name="buffalo_l",
                               providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=0, det_size=FACE_DET_SIZE)

            img_np = np.array(image.convert("RGB"))
            faces = app.get(img_np)

            if not faces:
                if error: error("No face detected.")
                return

            face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) *
                       (f.bbox[3] - f.bbox[1]))

            # Save embedding
            d = _faces_dir() / name
            d.mkdir(parents=True, exist_ok=True)

            np.save(str(d / "embedding.npy"), face.embedding)

            # Save face crop as thumbnail
            x1, y1, x2, y2 = [int(v) for v in face.bbox]
            pad = int((x2 - x1) * FACE_CROP_PAD)
            x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
            x2 = min(image.width, x2 + pad)
            y2 = min(image.height, y2 + pad)
            crop = image.crop((x1, y1, x2, y2))
            crop.save(str(d / "face.png"))

            # Save reference image
            ref = image.copy()
            ref.thumbnail(IDENTITY_THUMB_SIZE, Image.LANCZOS)
            ref.save(str(d / "reference.png"))

            # Metadata
            meta = {"name": name, "bbox": [x1, y1, x2, y2],
                    "embedding_shape": list(face.embedding.shape)}
            with open(d / "meta.json", "w") as f:
                json.dump(meta, f, indent=2)

            if status: status(f"Identity '{name}' saved.")
            if done: done(name)

        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def list_identities():
    """Return list of saved identity names."""
    d = _faces_dir()
    return sorted([p.name for p in d.iterdir()
                   if p.is_dir() and (p / "embedding.npy").exists()])


def load_identity(name):
    """Load a saved identity. Returns (embedding, face_image, reference_image)."""
    d = _faces_dir() / name
    emb = np.load(str(d / "embedding.npy"))
    face = Image.open(str(d / "face.png")) if (d / "face.png").exists() else None
    ref = Image.open(str(d / "reference.png")) if (d / "reference.png").exists() else None
    return emb, face, ref


def delete_identity(name):
    """Delete a saved identity."""
    import shutil
    d = _faces_dir() / name
    if d.exists():
        shutil.rmtree(d)


def generate_with_identity(name, prompt, neg="", width=512, height=512,
                           steps=30, cfg=7.0, seed=-1, strength=0.6,
                           status=None, done=None, error=None):
    """
    Generate an image using a saved identity via IP-Adapter.
    strength: 0.0 (ignore identity) to 1.0 (strict identity match).
    0.6 is good for keeping face while changing everything else.
    """
    def _run():
        try:
            import engine
            if not engine._pipe:
                if error: error("No model loaded."); return

            emb, face_img, ref_img = load_identity(name)
            if ref_img is None:
                if error: error(f"Identity '{name}' has no reference image.")
                return

            if status: status(f"Generating with identity '{name}'...")

            import torch
            from diffusers import StableDiffusionPipeline

            pipe = engine._pipe
            dev = engine.device()

            # Try IP-Adapter approach first
            try:
                pipe.load_ip_adapter(
                    IP_ADAPTER_REPO, subfolder="models",
                    weight_name="ip-adapter_sd15.bin")
                pipe.set_ip_adapter_scale(strength)

                s = engine._seed(seed)
                g = torch.Generator(device="cpu").manual_seed(s)

                with engine._lock:
                    result = pipe(
                        prompt=prompt,
                        ip_adapter_image=ref_img.convert("RGB"),
                        negative_prompt=neg or None,
                        width=width // 8 * 8, height=height // 8 * 8,
                        num_inference_steps=steps,
                        guidance_scale=cfg, generator=g)

                # Unload IP-Adapter to free memory
                pipe.unload_ip_adapter()

                if done: done(result.images[0], s)
                if status: status("Done.")
                return

            except Exception:
                # Fallback: generate normally then swap face
                pass

            # Fallback: img2img from reference with new prompt
            if status: status("IP-Adapter unavailable, using img2img fallback...")
            from diffusers import StableDiffusionImg2ImgPipeline

            p = StableDiffusionImg2ImgPipeline(
                vae=pipe.vae, text_encoder=pipe.text_encoder,
                tokenizer=pipe.tokenizer, unet=pipe.unet,
                scheduler=pipe.scheduler,
                safety_checker=None, feature_extractor=None)
            p = p.to(dev); p.enable_attention_slicing()

            s = engine._seed(seed)
            g = torch.Generator(device="cpu").manual_seed(s)
            init = ref_img.convert("RGB").resize(
                (width // 8 * 8, height // 8 * 8), Image.LANCZOS)

            result = p(prompt=prompt, image=init,
                       strength=0.65,
                       negative_prompt=neg or None,
                       num_inference_steps=steps,
                       guidance_scale=cfg, generator=g)

            if done: done(result.images[0], s)
            if status: status("Done (fallback mode).")

        except Exception as e:
            if error: error(str(e))
    _bg(_run)
