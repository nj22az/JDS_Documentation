"""qwen.py — Qwen-Image-Edit with intelligent system-aware loading.

Full quality (1024px) on M1 Pro 16GB without lockup. Auto-detects hardware,
picks offload strategy, preloads in background, thread-safe.
"""

import io
import gc
import os
import json
import threading
from pathlib import Path

from models import (CONFIG_DIR, MODELS_DIR, bg_thread as _bg)

_SETTINGS_FILE = CONFIG_DIR / "qwen.json"
_OFFLOAD_DIR = MODELS_DIR / "qwen_offload"

EDIT_TRANSFORMER = "linoyts/Qwen-Image-Edit-Rapid-AIO"
EDIT_BASE_PIPE = "Qwen/Qwen-Image-Edit-2509"
EDIT_CLOUD_MODEL = "Qwen/Qwen-Image-Edit"
EDIT_PRUNED = "OPPOer/Qwen-Image-Edit-2509-13B-4steps"

STEPS = 4
CFG = 1.0
FULL_SIZE = 1024

_system = None


def _detect_system():
    """Profile hardware once, cache forever. Returns device, RAM, strategy."""
    global _system
    if _system is not None:
        return _system

    info = {"device": "cpu", "ram_gb": 8.0}

    try:
        info["ram_gb"] = (os.sysconf("SC_PHYS_PAGES")
                          * os.sysconf("SC_PAGE_SIZE")) / (1024 ** 3)
    except Exception:
        pass

    try:
        import torch
        if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            info["device"] = "mps"
        elif torch.cuda.is_available():
            info["device"] = "cuda"
    except Exception:
        pass

    ram = info["ram_gb"]
    if ram >= 32:
        info.update(model="full", offload="model")
    elif ram >= 16:
        info.update(model="full", offload="sequential")
    else:
        info.update(model="pruned", offload="sequential")

    _system = info
    return info


def system_info():
    """Human-readable system profile for GUI display."""
    hw = _detect_system()
    return (f"{hw['ram_gb']:.0f}GB RAM, {hw['device'].upper()}, "
            f"{hw['model']} model, {FULL_SIZE}px")


def _is_cached(model_id):
    """Check if model weights exist in HuggingFace cache (fast dir check)."""
    try:
        hf_home = Path(os.environ.get(
            "HF_HOME", Path.home() / ".cache" / "huggingface"))
        slug = "models--" + model_id.replace("/", "--")
        snapshots = hf_home / "hub" / slug / "snapshots"
        return snapshots.exists() and any(snapshots.iterdir())
    except Exception:
        return False


def load_settings():
    defaults = {"mode": "cloud", "local_model": "auto"}
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


_torch = None


def _get_torch():
    """Import torch once, cache the module reference."""
    global _torch
    if _torch is None:
        import torch
        _torch = torch
    return _torch


def _flush():
    """Free memory aggressively — call between every major operation."""
    gc.collect()
    try:
        torch = _get_torch()
        if hasattr(torch, "mps") and hasattr(torch.mps, "empty_cache"):
            torch.mps.empty_cache()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


def _lower_priority():
    """Lower process priority so macOS stays responsive."""
    try:
        os.nice(10)
    except (OSError, AttributeError):
        pass


_pipe = None
_load_lock = threading.Lock()
_compiled = False


def _resolve_model():
    """Decide full vs pruned: explicit setting overrides auto-detect."""
    choice = load_settings().get("local_model", "auto")
    if choice == "pruned":
        return True
    if choice == "full":
        return False
    return _detect_system()["model"] == "pruned"


def preload(status=None):
    """Background preload — non-blocking, thread-safe, no-op if loaded."""
    if _pipe is not None:
        return
    if not _load_lock.acquire(blocking=False):
        return
    _load_lock.release()
    _bg(lambda: _load_pipe(status))


def unload():
    """Free pipeline memory. Call when switching to cloud mode."""
    global _pipe, _compiled
    with _load_lock:
        _pipe = None
        _compiled = False
    _flush()


def _load_pipe(status=None):
    """Load pipeline — hardware-aware, cache-aware, thread-safe."""
    global _pipe
    if _pipe is not None:
        return True

    if not _load_lock.acquire(timeout=600):
        return False

    try:
        if _pipe is not None:
            return True

        _lower_priority()
        torch = _get_torch()
        from diffusers import QwenImageEditPlusPipeline

        _OFFLOAD_DIR.mkdir(parents=True, exist_ok=True)

        hw = _detect_system()
        use_pruned = _resolve_model()
        device = hw["device"]

        # Shared loading options: mmap via safetensors, stream weights
        load_opts = dict(torch_dtype=torch.float16, low_cpu_mem_usage=True,
                         offload_state_dict=True,
                         offload_folder=str(_OFFLOAD_DIR),
                         use_safetensors=True)

        if use_pruned:
            cached = _is_cached(EDIT_PRUNED)
            label = "pruned 13.6B"
            if status:
                status(f"Qwen: {'loading' if cached else 'downloading'} "
                       f"{label}{'...' if cached else ' (~9GB, one time)...'}")

            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_PRUNED, **load_opts)
            _flush()
        else:
            label = "full 20B"
            cached_xfmr = _is_cached(EDIT_TRANSFORMER)
            cached_pipe = _is_cached(EDIT_BASE_PIPE)

            # Stage 1: Transformer (~14GB fp16, the big part)
            from diffusers.models import QwenImageTransformer2DModel

            if status:
                status("Qwen: " + ("loading" if cached_xfmr else "downloading")
                       + " transformer"
                       + ("..." if cached_xfmr else " (~14GB, one time)..."))

            transformer = QwenImageTransformer2DModel.from_pretrained(
                EDIT_TRANSFORMER, subfolder="transformer", **load_opts)
            _flush()

            # Stage 2: Pipeline shell (text encoder + VAE, ~3GB)
            if status:
                status("Qwen: " + ("loading" if cached_pipe else "downloading")
                       + " text encoder + VAE"
                       + ("..." if cached_pipe else " (~3GB)..."))

            _pipe = QwenImageEditPlusPipeline.from_pretrained(
                EDIT_BASE_PIPE, transformer=transformer, **load_opts)
            del transformer
            _flush()

        # Offload strategy: sequential on ≤16GB, model-level on ≥32GB
        if status:
            status(f"Qwen: configuring for {hw['ram_gb']:.0f}GB RAM...")

        if device in ("mps", "cuda"):
            if hw["offload"] == "model":
                try:
                    _pipe.enable_model_cpu_offload(device=device)
                except TypeError:
                    _pipe.enable_sequential_cpu_offload(device=device)
            else:
                _pipe.enable_sequential_cpu_offload(device=device)
            _pipe._fallback_device = device
        else:
            _pipe.to("cpu")

        _pipe.enable_attention_slicing(slice_size=1)
        if hasattr(_pipe, "enable_vae_tiling"):
            _pipe.enable_vae_tiling()
        if hasattr(_pipe, "enable_vae_slicing"):
            _pipe.enable_vae_slicing()

        _flush()

        if status:
            status(f"Qwen: {label} ready — {device.upper()}, "
                   f"{hw['ram_gb']:.0f}GB, {FULL_SIZE}px")
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
    finally:
        _load_lock.release()


def _try_compile(pipe):
    """torch.compile for repeated inference speed (CUDA only, no MPS)."""
    global _compiled
    if _compiled or _detect_system()["device"] != "cuda":
        return
    try:
        torch = _get_torch()
        if hasattr(torch, "compile") and hasattr(pipe, "transformer"):
            pipe.transformer = torch.compile(
                pipe.transformer, mode="reduce-overhead")
            _compiled = True
    except Exception:
        pass


def _run_inference(pipe, kwargs, status=None):
    """Run inference with automatic OOM fallback to sequential offload."""
    torch = _get_torch()
    _flush()

    try:
        with torch.inference_mode():
            result = pipe(**kwargs).images[0]
        _try_compile(pipe)
        return result
    except RuntimeError as e:
        if "out of memory" not in str(e).lower():
            raise

        if status:
            status("Qwen: OOM — switching to sequential offload...")
        _flush()

        device = getattr(pipe, "_fallback_device", "mps")
        pipe.enable_sequential_cpu_offload(device=device)
        pipe.enable_attention_slicing(slice_size=1)
        _flush()

        with torch.inference_mode():
            return pipe(**kwargs).images[0]


def _local_edit(image, prompt, status=None, done=None, error=None):
    """Edit image locally at full quality."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen.\n\n"
                          "pip3 install diffusers transformers "
                          "torch accelerate safetensors\n"
                          "Or use cloud mode (free).")
                return

            from PIL import Image
            if status:
                status(f"Qwen: editing ({STEPS} steps, {FULL_SIZE}px)...")

            original_size = image.size
            img_in = image.copy().resize(
                (FULL_SIZE, FULL_SIZE), Image.LANCZOS)

            result = _run_inference(_pipe, {
                "image": [img_in], "prompt": prompt,
                "num_inference_steps": STEPS, "guidance_scale": CFG,
                "true_cfg_scale": CFG, "negative_prompt": " ",
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


def _local_generate(prompt, width=FULL_SIZE, height=FULL_SIZE,
                    status=None, done=None, error=None):
    """Text-to-image locally at full quality."""
    def _run():
        try:
            if not _load_pipe(status):
                if error:
                    error("Failed to load Qwen.")
                return

            if status:
                status(f"Qwen: generating ({STEPS} steps, {width}x{height})...")

            result = _run_inference(_pipe, {
                "image": [], "prompt": prompt,
                "num_inference_steps": STEPS, "guidance_scale": CFG,
                "true_cfg_scale": CFG, "negative_prompt": " ",
                "num_images_per_prompt": 1,
                "height": height, "width": width,
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


def _cloud_edit(image, prompt, hf_token="",
                status=None, done=None, error=None):
    """Edit image via HuggingFace cloud (free)."""
    def _run():
        try:
            from huggingface_hub import InferenceClient
            from PIL import Image

            if status:
                status("Qwen cloud: connecting...")
            client = InferenceClient(token=hf_token or None)
            img_in = image.copy().resize((FULL_SIZE, FULL_SIZE), Image.LANCZOS)

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


def _cloud_generate(prompt, width=FULL_SIZE, height=FULL_SIZE,
                    hf_token="", status=None, done=None, error=None):
    """Text-to-image via HuggingFace cloud (free)."""
    def _run():
        try:
            from huggingface_hub import InferenceClient
            from PIL import Image

            if status:
                status("Qwen cloud: generating...")
            client = InferenceClient(token=hf_token or None)
            result = client.text_to_image(
                prompt, model=EDIT_CLOUD_MODEL, width=width, height=height)
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


def _get_hf_token():
    try:
        from cloudgen import load_settings as load_cloud
        return load_cloud().get("hf_token", "")
    except Exception:
        return ""


def edit(image, prompt, status=None, done=None, error=None):
    """Edit an image — routes to local or cloud based on settings."""
    if load_settings().get("mode") == "local":
        _local_edit(image, prompt, status, done, error)
    else:
        _cloud_edit(image, prompt, _get_hf_token(), status, done, error)


def generate(prompt, width=FULL_SIZE, height=FULL_SIZE,
             status=None, done=None, error=None):
    """Generate an image — routes to local or cloud based on settings."""
    if load_settings().get("mode") == "local":
        _local_generate(prompt, width, height, status, done, error)
    else:
        _cloud_generate(prompt, width, height, _get_hf_token(),
                        status, done, error)
