"""engine.py — All ML pipelines: generate, img2img, inpaint, background, download."""

import os
import gc
import threading
from models import MODELS_DIR

_pipe = None
_lock = threading.Lock()
_model_id = None


def _bg(fn):
    """Run fn in a daemon thread."""
    threading.Thread(target=fn, daemon=True).start()


def device():
    import torch
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cuda" if torch.cuda.is_available() else "cpu"


def unload():
    global _pipe, _model_id
    with _lock:
        if _pipe:
            del _pipe
            _pipe = _model_id = None
            gc.collect()
            try:
                import torch
                if hasattr(torch.mps, "empty_cache"): torch.mps.empty_cache()
                elif torch.cuda.is_available(): torch.cuda.empty_cache()
            except Exception:
                pass


def download(model_id, status=None, done=None, error=None):
    def _run():
        try:
            if status: status(f"Downloading {model_id}...")
            from huggingface_hub import snapshot_download
            path = snapshot_download(model_id, cache_dir=str(MODELS_DIR),
                                     resume_download=True)
            if status: status(f"Downloaded: {model_id}")
            if done: done(model_id, path)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def load(model_id, status=None, done=None, error=None):
    def _run():
        global _pipe, _model_id
        try:
            unload()
            if status: status("Loading model...")
            import torch
            from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler

            dev = device()
            dt = torch.float16 if dev == "cuda" else torch.float32
            local = os.path.isdir(model_id)

            with _lock:
                p = StableDiffusionPipeline.from_pretrained(
                    model_id, torch_dtype=dt,
                    cache_dir=str(MODELS_DIR) if not local else None,
                    local_files_only=local)
                p.safety_checker = p.feature_extractor = None
                p.scheduler = DPMSolverMultistepScheduler.from_config(
                    p.scheduler.config, use_karras_sigmas=True,
                    algorithm_type="dpmsolver++")
                p = p.to(dev)
                p.enable_attention_slicing()
                _pipe, _model_id = p, model_id

            if status: status(f"Ready — {dev.upper()}")
            if done: done()
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def _seed(s):
    import torch
    return s if s >= 0 else torch.randint(0, 2**32 - 1, (1,)).item()


def _gen(fn):
    import torch
    return torch.Generator(device="cpu")


def txt2img(prompt, neg="", w=512, h=512, steps=30, cfg=7.0, seed=-1,
            status=None, done=None, error=None):
    def _run():
        try:
            if not _pipe:
                if error: error("No model loaded."); return
            if status: status("Generating...")
            import torch
            s = _seed(seed)
            g = torch.Generator(device="cpu").manual_seed(s)
            with _lock:
                r = _pipe(prompt=prompt, negative_prompt=neg or None,
                          width=w, height=h, num_inference_steps=steps,
                          guidance_scale=cfg, generator=g)
            if done: done(r.images[0], s)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def img2img(prompt, image, strength=0.75, neg="", steps=30, cfg=7.0,
            seed=-1, status=None, done=None, error=None):
    def _run():
        try:
            if not _pipe:
                if error: error("No model loaded."); return
            if status: status("img2img...")
            import torch
            from diffusers import StableDiffusionImg2ImgPipeline
            p = StableDiffusionImg2ImgPipeline(
                vae=_pipe.vae, text_encoder=_pipe.text_encoder,
                tokenizer=_pipe.tokenizer, unet=_pipe.unet,
                scheduler=_pipe.scheduler,
                safety_checker=None, feature_extractor=None)
            p = p.to(_pipe.device); p.enable_attention_slicing()
            s = _seed(seed)
            g = torch.Generator(device="cpu").manual_seed(s)
            init = image.convert("RGB")
            init = init.resize((init.width // 8 * 8, init.height // 8 * 8))
            r = p(prompt=prompt, image=init, strength=strength,
                  negative_prompt=neg or None, num_inference_steps=steps,
                  guidance_scale=cfg, generator=g)
            if done: done(r.images[0], s)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def inpaint(prompt, image, mask, neg="", steps=30, cfg=7.0, seed=-1,
            strength=0.85, status=None, done=None, error=None):
    """mask: white=regenerate, black=keep."""
    def _run():
        try:
            if not _pipe:
                if error: error("No model loaded."); return
            if status: status("Inpainting...")
            import torch
            from diffusers import StableDiffusionInpaintPipeline
            p = StableDiffusionInpaintPipeline(
                vae=_pipe.vae, text_encoder=_pipe.text_encoder,
                tokenizer=_pipe.tokenizer, unet=_pipe.unet,
                scheduler=_pipe.scheduler,
                safety_checker=None, feature_extractor=None)
            p = p.to(_pipe.device); p.enable_attention_slicing()
            s = _seed(seed)
            g = torch.Generator(device="cpu").manual_seed(s)
            ww, hh = image.width // 8 * 8, image.height // 8 * 8
            r = p(prompt=prompt,
                  image=image.convert("RGB").resize((ww, hh)),
                  mask_image=mask.convert("RGB").resize((ww, hh)),
                  negative_prompt=neg or None, num_inference_steps=steps,
                  guidance_scale=cfg, strength=strength, generator=g)
            if done: done(r.images[0], s)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def remove_bg(image, status=None, done=None, error=None):
    def _run():
        try:
            if status: status("Removing background...")
            from rembg import remove
            if done: done(remove(image))
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def subject_mask(image, status=None, done=None, error=None):
    """Returns L-mode mask: white=subject, black=background."""
    def _run():
        try:
            if status: status("Detecting subject...")
            from rembg import remove
            rgba = remove(image)
            mask = rgba.split()[-1].point(lambda p: 255 if p > 128 else 0)
            if done: done(mask)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def replace_bg(image, prompt, neg="", steps=30, cfg=7.0, seed=-1,
               status=None, done=None, error=None):
    """Detect subject, inpaint only the background."""
    def _run():
        try:
            if not _pipe:
                if error: error("No model loaded."); return
            if status: status("Detecting subject...")
            from rembg import remove
            from PIL import ImageOps
            import torch
            from diffusers import StableDiffusionInpaintPipeline

            rgba = remove(image)
            bg_mask = ImageOps.invert(
                rgba.split()[-1].point(lambda p: 255 if p > 128 else 0))

            if status: status("Generating new background...")
            p = StableDiffusionInpaintPipeline(
                vae=_pipe.vae, text_encoder=_pipe.text_encoder,
                tokenizer=_pipe.tokenizer, unet=_pipe.unet,
                scheduler=_pipe.scheduler,
                safety_checker=None, feature_extractor=None)
            p = p.to(_pipe.device); p.enable_attention_slicing()
            s = _seed(seed)
            g = torch.Generator(device="cpu").manual_seed(s)
            ww, hh = image.width // 8 * 8, image.height // 8 * 8
            r = p(prompt=prompt,
                  image=image.convert("RGB").resize((ww, hh)),
                  mask_image=bg_mask.convert("RGB").resize((ww, hh)),
                  negative_prompt=neg or None, num_inference_steps=steps,
                  guidance_scale=cfg, strength=0.95, generator=g)
            if done: done(r.images[0], s)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)
