"""qwen.py — Qwen-Image-Edit on M1 Pro 16GB (max optimized).

Direct image editing from natural language. 4 steps, CFG 1.
Optimized for M1 Pro 16GB unified memory — it WILL be slow but it WILL work.

Memory tricks used:
1. Pruned model default (13.6B / 40 layers, not 20B / 60)
2. float16 (MPS-native, not bfloat16 which MPS must emulate)
3. Sequential CPU offload (one transformer block on GPU at a time)
4. Attention slicing (slice_size=1, minimum memory per head)
5. VAE tiling (decode in 512x512 tiles, not full image at once)
6. Aggressive gc + MPS cache flush between pipeline stages
7. 768x768 default (half the memory of 1024x1024)
8. torch.inference_mode (no grad graph, no autograd overhead)

Cloud mode is still default (free, fast). Local is for offline use.
"""

import io
import gc
import json
import base64

from models import (CONFIG_DIR, OUTPUT_DIR, HTTP_TIMEOUT, bg_thread as _bg)

_SETTINGS_FILE = CONFIG_DIR / "qwen.json"

# Model IDs
EDIT_TRANSFORMER = "linoyts/Qwen-Image-Edit-Rapid-AIO"
EDIT_BASE_PIPE = "Qwen/Qwen-Image-Edit-2509"
EDIT_CLOUD_MODEL = "Qwen/Qwen-Image-Edit"
EDIT_PRUNED = "OPPOer/Qwen-Image-Edit-2509-13B-4steps"

# Inference: 4 steps, CFG 1, no negative prompt
STEPS = 4
CFG = 1.0

# M1 optimized resolution (1024x1024 needs 4x more memory)
M1_SIZE = 768


def load_settings():
    defaults = {"mode": "cloud", "local_model": "pruned"}
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


def _flush():
    """Aggressively free memory — call between pipeline stages."""
    gc.collect()
    try:
        import torch
        if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
            torch.mps.empty_cache()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


# -------------------------------------------------------------------
# Local pipeline — M1 Pro 16GB optimized
# -------------------------------------------------------------------

_pipe = None


def _load_pipe(status=None):
    """Load pipeline with every memory optimization available."""
    global _pipe
    if _pipe is not None:
        return True

    try:
        import torch
        from diffusers import QwenImageEditPlusPipeline

        settings = load_settings()
        use_pruned = settings.get("local_model") != "rapid"

        # Step 1: Choose model — pruned (9GB) vs full (14GB)
        if use_pruned:
            if status:
                status("Qwen: loading pruned 13.6B (first time ~9GB download)...")
            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_PRUNED,
                torch_dtype=torch.float16,       # float16 = MPS native
                low_cpu_mem_usage=True,           # load weights incrementally
            )
        else:
            from diffusers.models import QwenImageTransformer2DModel
            if status:
                status("Qwen: loading full 20B (first time ~14GB download)...")
            transformer = QwenImageTransformer2DModel.from_pretrained(
                EDIT_TRANSFORMER, subfolder="transformer",
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True)
            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_BASE_PIPE, transformer=transformer,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True)

        # Step 2: Memory optimizations (layered, most aggressive first)
        is_mps = hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
        is_cuda = torch.cuda.is_available()

        if is_mps:
            # M1/M2/M3: sequential offload — one layer on Metal at a time
            _pipe.enable_sequential_cpu_offload(device="mps")
            if status:
                status("Qwen: sequential CPU offload enabled (MPS)...")
        elif is_cuda:
            vram_gb = torch.cuda.get_device_properties(0).total_mem / 1e9
            if vram_gb >= 16:
                _pipe.to("cuda")
            else:
                _pipe.enable_sequential_cpu_offload()
        else:
            _pipe.to("cpu")

        # Attention slicing: process one attention head at a time
        # slice_size=1 = absolute minimum memory per attention op
        _pipe.enable_attention_slicing(slice_size=1)

        # VAE tiling: decode output in 512x512 tiles instead of full image
        if hasattr(_pipe, "enable_vae_tiling"):
            _pipe.enable_vae_tiling()

        # VAE slicing: process one image at a time through VAE
        if hasattr(_pipe, "enable_vae_slicing"):
            _pipe.enable_vae_slicing()

        _flush()

        if status:
            model_name = "pruned 13.6B" if use_pruned else "full 20B"
            device_name = "MPS" if is_mps else "CUDA" if is_cuda else "CPU"
            status(f"Qwen: {model_name} ready on {device_name}.")

        return True

    except ImportError:
        if status:
            status("Missing: pip3 install diffusers transformers torch")
        return False
    except Exception as e:
        if status:
            status(f"Qwen load failed: {e}")
        _pipe = None
        return False


def _local_edit(image, prompt, status=None, done=None, error=None):
    """Edit image locally — M1 optimized."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen pipeline.\n\n"
                          "Install: pip3 install diffusers transformers torch\n\n"
                          "Or use cloud mode (free, no install).")
                return

            import torch
            from PIL import Image

            if status:
                status(f"Qwen: editing ({STEPS} steps, {M1_SIZE}px)...")

            original_size = image.size

            # 768x768 uses half the memory of 1024x1024
            img_in = image.copy().resize((M1_SIZE, M1_SIZE), Image.LANCZOS)

            _flush()

            with torch.inference_mode():
                result = _pipe(
                    image=[img_in],
                    prompt=prompt,
                    num_inference_steps=STEPS,
                    guidance_scale=CFG,
                    true_cfg_scale=CFG,
                    negative_prompt=" ",
                    num_images_per_prompt=1,
                ).images[0]

            _flush()

            result = result.resize(original_size, Image.LANCZOS)

            if status:
                status("Qwen: edit complete.")
            if done:
                done(result, -1)

        except Exception as e:
            _flush()
            if error:
                error(f"Qwen edit error: {e}")
    _bg(_run)


def _local_generate(prompt, width=M1_SIZE, height=M1_SIZE,
                    status=None, done=None, error=None):
    """Text-to-image locally — M1 optimized."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen pipeline.")
                return

            import torch

            if status:
                status(f"Qwen: generating ({STEPS} steps, {width}x{height})...")

            _flush()

            with torch.inference_mode():
                result = _pipe(
                    image=[],
                    prompt=prompt,
                    num_inference_steps=STEPS,
                    guidance_scale=CFG,
                    true_cfg_scale=CFG,
                    negative_prompt=" ",
                    num_images_per_prompt=1,
                    height=height,
                    width=width,
                ).images[0]

            _flush()

            if status:
                status("Qwen: generation complete.")
            if done:
                done(result, -1)

        except Exception as e:
            _flush()
            if error:
                error(f"Qwen generate error: {e}")
    _bg(_run)


# -------------------------------------------------------------------
# Cloud (HuggingFace Inference API — free)
# -------------------------------------------------------------------

def _cloud_edit(image, prompt, hf_token="",
                status=None, done=None, error=None):
    """Edit image via HuggingFace (free)."""
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
    """Text-to-image via HuggingFace (free)."""
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
            if error:
                error(f"Qwen cloud error: {e}")
    _bg(_run)


# -------------------------------------------------------------------
# Unified API
# -------------------------------------------------------------------

def _get_hf_token():
    try:
        from cloudgen import load_settings as load_cloud
        return load_cloud().get("hf_token", "")
    except Exception:
        return ""


def edit(image, prompt, status=None, done=None, error=None):
    """Edit an image. Routes to cloud or local."""
    if load_settings().get("mode") == "local":
        _local_edit(image, prompt, status, done, error)
    else:
        _cloud_edit(image, prompt, _get_hf_token(), status, done, error)


def generate(prompt, width=M1_SIZE, height=M1_SIZE,
             status=None, done=None, error=None):
    """Text-to-image. Routes to cloud or local."""
    if load_settings().get("mode") == "local":
        _local_generate(prompt, width, height, status, done, error)
    else:
        _cloud_generate(prompt, width, height, _get_hf_token(),
                        status, done, error)
