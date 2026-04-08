"""qwen.py — Qwen-Image-Edit-Rapid-AIO NSFW v23 integration.

Direct image editing from natural language. Type "remove her clothes"
and the model edits the image. 4 steps, 1 CFG, no negative prompt needed.

Two modes:
- Cloud (default): HuggingFace Inference API (free, no install)
- Local: diffusers pipeline on M1 (needs ~14GB, uses MPS/Metal)

Based on Phr00t/Qwen-Image-Edit-Rapid-AIO (v23 NSFW variant).
Pipeline: QwenImageEditPlusPipeline from diffusers.
Transformer: linoyts/Qwen-Image-Edit-Rapid-AIO (distilled 4-step).

Fully unrestricted. No filters. No refusals.
"""

import io
import json
import base64
from pathlib import Path

from models import (CONFIG_DIR, OUTPUT_DIR, HTTP_TIMEOUT, bg_thread as _bg)

_SETTINGS_FILE = CONFIG_DIR / "qwen.json"

# Model IDs
EDIT_TRANSFORMER = "linoyts/Qwen-Image-Edit-Rapid-AIO"
EDIT_BASE_PIPE = "Qwen/Qwen-Image-Edit-2509"
EDIT_CLOUD_MODEL = "Qwen/Qwen-Image-Edit"

# Rapid-AIO v23: 4 steps, CFG 1, no neg prompt
RAPID_STEPS = 4
RAPID_CFG = 1.0


def load_settings():
    defaults = {"mode": "cloud"}
    if _SETTINGS_FILE.exists():
        try:
            with open(_SETTINGS_FILE) as f:
                defaults.update(json.load(f))
        except Exception:
            pass
    return defaults


def save_settings(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(_SETTINGS_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


# -------------------------------------------------------------------
# Local pipeline (M1 compatible via MPS)
# -------------------------------------------------------------------

_pipe = None


def _load_pipe(status=None):
    """Load QwenImageEditPlusPipeline locally. First run downloads ~14GB."""
    global _pipe
    if _pipe is not None:
        return True

    try:
        import torch
        from diffusers.models import QwenImageTransformer2DModel
        from diffusers import QwenImageEditPlusPipeline

        if status:
            status("Qwen: downloading transformer (~14GB first time)...")

        transformer = QwenImageTransformer2DModel.from_pretrained(
            EDIT_TRANSFORMER, subfolder="transformer",
            torch_dtype=torch.bfloat16)

        if status:
            status("Qwen: loading pipeline...")

        _pipe = QwenImageEditPlusPipeline.from_pretrained(
            EDIT_BASE_PIPE, transformer=transformer,
            torch_dtype=torch.bfloat16)

        # Device selection: CUDA > MPS > CPU
        if torch.cuda.is_available():
            _pipe.to("cuda")
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            _pipe.to("mps")
            _pipe.enable_attention_slicing()
        else:
            _pipe.to("cpu")
            _pipe.enable_attention_slicing()

        if status:
            status("Qwen: pipeline ready.")
        return True

    except ImportError:
        if status:
            status("Qwen: missing diffusers. pip3 install diffusers transformers torch")
        return False
    except Exception as e:
        if status:
            status(f"Qwen: load failed — {e}")
        _pipe = None
        return False


def _local_edit(image, prompt, status=None, done=None, error=None):
    """Edit image locally using QwenImageEditPlusPipeline."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen pipeline.\n\n"
                          "Install: pip3 install diffusers transformers torch\n"
                          "Needs ~14GB RAM. Close other apps on M1 16GB.\n\n"
                          "Or use cloud mode (free, no install needed).")
                return

            import torch
            from PIL import Image

            if status:
                status(f"Qwen: editing ({RAPID_STEPS} steps)...")

            # Resize to 1024x1024 for best results
            original_size = image.size
            img_in = image.copy().resize((1024, 1024), Image.LANCZOS)

            result = _pipe(
                image=[img_in],
                prompt=prompt,
                num_inference_steps=RAPID_STEPS,
                guidance_scale=RAPID_CFG,
                true_cfg_scale=RAPID_CFG,
                negative_prompt=" ",
                num_images_per_prompt=1,
            ).images[0]

            # Resize back to original
            result = result.resize(original_size, Image.LANCZOS)

            if status:
                status("Qwen: edit complete.")
            if done:
                done(result, -1)

        except Exception as e:
            if error:
                error(f"Qwen edit error: {e}")
    _bg(_run)


def _local_generate(prompt, width=1024, height=1024,
                    status=None, done=None, error=None):
    """Text-to-image using Qwen (no input image)."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen pipeline.")
                return

            import torch

            if status:
                status(f"Qwen: generating ({RAPID_STEPS} steps)...")

            result = _pipe(
                image=[],
                prompt=prompt,
                num_inference_steps=RAPID_STEPS,
                guidance_scale=RAPID_CFG,
                true_cfg_scale=RAPID_CFG,
                negative_prompt=" ",
                num_images_per_prompt=1,
                height=height,
                width=width,
            ).images[0]

            if status:
                status("Qwen: generation complete.")
            if done:
                done(result, -1)

        except Exception as e:
            if error:
                error(f"Qwen generate error: {e}")
    _bg(_run)


# -------------------------------------------------------------------
# Cloud edit (HuggingFace Inference API — free)
# -------------------------------------------------------------------

def _cloud_edit(image, prompt, hf_token="",
                status=None, done=None, error=None):
    """Edit image via Qwen-Image-Edit on HuggingFace (free)."""
    def _run():
        try:
            from huggingface_hub import InferenceClient
            from PIL import Image

            if status:
                status("Qwen cloud: connecting...")

            client = InferenceClient(token=hf_token or None)

            img_in = image.copy().resize((1024, 1024), Image.LANCZOS)

            if status:
                status(f"Qwen cloud: '{prompt[:50]}...'")

            result = client.image_to_image(
                img_in, prompt=prompt, model=EDIT_CLOUD_MODEL)

            if isinstance(result, bytes):
                result = Image.open(io.BytesIO(result))

            result = result.resize(image.size, Image.LANCZOS)

            if status:
                status("Qwen cloud: done.")
            if done:
                done(result, -1)

        except Exception as e:
            msg = str(e)
            if "rate limit" in msg.lower() or "429" in msg:
                msg += "\n\nRate limited. Add HF token for higher limits."
            if error:
                error(f"Qwen cloud error: {msg}")
    _bg(_run)


def _cloud_generate(prompt, width=1024, height=1024, hf_token="",
                    status=None, done=None, error=None):
    """Text-to-image via Qwen on HuggingFace (free)."""
    def _run():
        try:
            from huggingface_hub import InferenceClient
            from PIL import Image

            if status:
                status("Qwen cloud: generating...")

            client = InferenceClient(token=hf_token or None)

            result = client.text_to_image(
                prompt, model=EDIT_CLOUD_MODEL,
                width=width, height=height)

            if isinstance(result, bytes):
                result = Image.open(io.BytesIO(result))

            if status:
                status("Qwen cloud: done.")
            if done:
                done(result, -1)

        except Exception as e:
            msg = str(e)
            if error:
                error(f"Qwen cloud error: {msg}")
    _bg(_run)


# -------------------------------------------------------------------
# Unified API — called by GUI
# -------------------------------------------------------------------

def _get_hf_token():
    """Get HF token from cloud settings."""
    try:
        from cloudgen import load_settings as load_cloud
        return load_cloud().get("hf_token", "")
    except Exception:
        return ""


def edit(image, prompt, status=None, done=None, error=None):
    """Edit an image. Routes to cloud or local based on settings."""
    mode = load_settings().get("mode", "cloud")
    if mode == "local":
        _local_edit(image, prompt, status, done, error)
    else:
        _cloud_edit(image, prompt, _get_hf_token(), status, done, error)


def generate(prompt, width=1024, height=1024,
             status=None, done=None, error=None):
    """Text-to-image. Routes to cloud or local based on settings."""
    mode = load_settings().get("mode", "cloud")
    if mode == "local":
        _local_generate(prompt, width, height, status, done, error)
    else:
        _cloud_generate(prompt, width, height, _get_hf_token(),
                        status, done, error)
