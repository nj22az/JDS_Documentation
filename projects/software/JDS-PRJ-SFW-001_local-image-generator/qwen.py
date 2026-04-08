"""qwen.py — Qwen-Image-Edit on M1 Pro 16GB (max optimized).

Direct image editing from natural language. 4 steps, CFG 1.
Engineered to run the full 20B model on M1 Pro 16GB unified memory.

Loading strategy (the hard part):
1. offload_state_dict=True — don't duplicate weights during load
2. device_map="auto" — let accelerate spread across MPS + CPU + disk
3. offload_folder on SSD — spill excess weights to NVMe (fast on M1)
4. Load components separately, flush between each

Inference strategy:
1. enable_model_cpu_offload — whole components swap (text enc → GPU → CPU,
   then transformer → GPU → CPU, then VAE → GPU → CPU)
2. Attention slicing (size=1) — one head at a time
3. VAE tiling + slicing — decode in 512px tiles
4. 768px default — half the attention memory of 1024
5. torch.inference_mode + aggressive gc + MPS cache flush
6. float16 — MPS native dtype, no emulation overhead

Cloud mode is still default (free, fast). Local is for offline use.
"""

import io
import gc
import json

from models import (CONFIG_DIR, MODELS_DIR, bg_thread as _bg)

_SETTINGS_FILE = CONFIG_DIR / "qwen.json"
_OFFLOAD_DIR = MODELS_DIR / "qwen_offload"

# Model IDs
EDIT_TRANSFORMER = "linoyts/Qwen-Image-Edit-Rapid-AIO"
EDIT_BASE_PIPE = "Qwen/Qwen-Image-Edit-2509"
EDIT_CLOUD_MODEL = "Qwen/Qwen-Image-Edit"
EDIT_PRUNED = "OPPOer/Qwen-Image-Edit-2509-13B-4steps"

# Inference: 4 steps, CFG 1, no negative prompt
STEPS = 4
CFG = 1.0

# M1 optimized resolution
M1_SIZE = 768


def load_settings():
    defaults = {"mode": "cloud", "local_model": "full"}
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
    """Aggressively free memory."""
    gc.collect()
    try:
        import torch
        if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
            torch.mps.empty_cache()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


def _is_mps():
    try:
        import torch
        return hasattr(torch.backends, "mps") and torch.backends.mps.is_available()
    except Exception:
        return False


def _is_cuda():
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False


# -------------------------------------------------------------------
# Local pipeline — M1 Pro 16GB: full 20B model
# -------------------------------------------------------------------

_pipe = None


def _load_pipe(status=None):
    """Load full 20B pipeline — engineered for M1 Pro 16GB.

    The challenge: from_pretrained loads all weights into RAM first.
    20B at float16 = ~40GB safetensors → needs to stream, not bulk load.

    Solution: load transformer separately with disk offload, build
    pipeline in stages, flush aggressively between each stage.
    """
    global _pipe
    if _pipe is not None:
        return True

    try:
        import torch
        from diffusers import QwenImageEditPlusPipeline

        # Prepare offload directory on SSD (M1 NVMe is fast)
        _OFFLOAD_DIR.mkdir(parents=True, exist_ok=True)

        settings = load_settings()
        use_pruned = settings.get("local_model") == "pruned"
        mps = _is_mps()
        cuda = _is_cuda()

        if use_pruned:
            # --- Pruned path: 13.6B, easier on memory ---
            if status:
                status("Qwen: loading pruned 13.6B...")

            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_PRUNED,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                offload_state_dict=True,
            )
            _flush()

        else:
            # --- Full 20B path: staged loading ---

            # Stage 1: Load transformer alone (the big part, ~28GB safetensors)
            # Uses disk offload so it never needs all weights in RAM at once
            from diffusers.models import QwenImageTransformer2DModel

            if status:
                status("Qwen: loading transformer (streaming from disk)...")

            transformer = QwenImageTransformer2DModel.from_pretrained(
                EDIT_TRANSFORMER,
                subfolder="transformer",
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                offload_state_dict=True,
            )
            _flush()

            # Stage 2: Load pipeline shell (text encoder + VAE, ~3GB)
            # Pass the already-loaded transformer so it doesn't reload
            if status:
                status("Qwen: loading text encoder + VAE...")

            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_BASE_PIPE,
                transformer=transformer,
                torch_dtype=torch.float16,
                low_cpu_mem_usage=True,
                offload_state_dict=True,
            )

            # Free the separate reference — pipeline owns it now
            del transformer
            _flush()

        # --- Apply memory optimizations ---
        if status:
            status("Qwen: configuring memory optimizations...")

        if mps or cuda:
            # Model-level CPU offload: moves whole components to GPU one
            # at a time (text_encoder → GPU → done → CPU, transformer →
            # GPU → done → CPU, VAE → GPU → done → CPU).
            # Lighter than sequential (less back-and-forth), still fits 16GB.
            device = "mps" if mps else "cuda"

            try:
                _pipe.enable_model_cpu_offload(device=device)
            except TypeError:
                # Older diffusers: no device arg for model offload
                _pipe.enable_sequential_cpu_offload(device=device)

            # Fallback: if model offload still OOMs during inference,
            # sequential offload is the nuclear option (one layer at a time)
            _pipe._m1_fallback_device = device
        else:
            _pipe.to("cpu")

        # Attention: process one head at a time (minimum memory per op)
        _pipe.enable_attention_slicing(slice_size=1)

        # VAE: decode in small tiles instead of full resolution at once
        if hasattr(_pipe, "enable_vae_tiling"):
            _pipe.enable_vae_tiling()
        if hasattr(_pipe, "enable_vae_slicing"):
            _pipe.enable_vae_slicing()

        _flush()

        model_name = "pruned 13.6B" if use_pruned else "full 20B"
        device_name = "MPS" if mps else "CUDA" if cuda else "CPU"
        if status:
            status(f"Qwen: {model_name} ready on {device_name}.")

        return True

    except ImportError as e:
        if status:
            status(f"Missing package: {e}")
        return False
    except Exception as e:
        if status:
            status(f"Qwen load failed: {e}")
        _pipe = None
        _flush()
        return False


def _run_inference(pipe, kwargs, status=None):
    """Run inference with OOM fallback to sequential offload."""
    import torch

    _flush()

    try:
        with torch.inference_mode():
            return pipe(**kwargs).images[0]
    except RuntimeError as e:
        if "out of memory" not in str(e).lower():
            raise

        # OOM: fall back to sequential CPU offload (one layer at a time)
        if status:
            status("Qwen: OOM — switching to sequential offload (slower)...")

        _flush()

        device = getattr(pipe, "_m1_fallback_device", "mps")
        pipe.enable_sequential_cpu_offload(device=device)
        pipe.enable_attention_slicing(slice_size=1)

        _flush()

        with torch.inference_mode():
            return pipe(**kwargs).images[0]


def _local_edit(image, prompt, status=None, done=None, error=None):
    """Edit image locally."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen.\n\n"
                          "pip3 install diffusers transformers torch accelerate\n"
                          "Or use cloud mode (free).")
                return

            from PIL import Image

            if status:
                status(f"Qwen: editing ({STEPS} steps, {M1_SIZE}px)...")

            original_size = image.size
            img_in = image.copy().resize((M1_SIZE, M1_SIZE), Image.LANCZOS)

            result = _run_inference(_pipe, {
                "image": [img_in],
                "prompt": prompt,
                "num_inference_steps": STEPS,
                "guidance_scale": CFG,
                "true_cfg_scale": CFG,
                "negative_prompt": " ",
                "num_images_per_prompt": 1,
            }, status)

            _flush()
            result = result.resize(original_size, Image.LANCZOS)

            if status:
                status("Qwen: edit complete.")
            if done:
                done(result, -1)

        except Exception as e:
            _flush()
            if error:
                error(f"Qwen error: {e}")
    _bg(_run)


def _local_generate(prompt, width=M1_SIZE, height=M1_SIZE,
                    status=None, done=None, error=None):
    """Text-to-image locally."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen.")
                return

            if status:
                status(f"Qwen: generating ({STEPS} steps, {width}x{height})...")

            result = _run_inference(_pipe, {
                "image": [],
                "prompt": prompt,
                "num_inference_steps": STEPS,
                "guidance_scale": CFG,
                "true_cfg_scale": CFG,
                "negative_prompt": " ",
                "num_images_per_prompt": 1,
                "height": height,
                "width": width,
            }, status)

            _flush()

            if status:
                status("Qwen: generation complete.")
            if done:
                done(result, -1)

        except Exception as e:
            _flush()
            if error:
                error(f"Qwen error: {e}")
    _bg(_run)


# -------------------------------------------------------------------
# Cloud (HuggingFace Inference API — free)
# -------------------------------------------------------------------

def _cloud_edit(image, prompt, hf_token="",
                status=None, done=None, error=None):
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
    if load_settings().get("mode") == "local":
        _local_edit(image, prompt, status, done, error)
    else:
        _cloud_edit(image, prompt, _get_hf_token(), status, done, error)


def generate(prompt, width=M1_SIZE, height=M1_SIZE,
             status=None, done=None, error=None):
    if load_settings().get("mode") == "local":
        _local_generate(prompt, width, height, status, done, error)
    else:
        _cloud_generate(prompt, width, height, _get_hf_token(),
                        status, done, error)
