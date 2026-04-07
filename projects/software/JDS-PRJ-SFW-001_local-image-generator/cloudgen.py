"""cloudgen.py — Cloud image generation backends (optional, not 100% local).

Three free backends:
1. HuggingFace Inference API — zero new deps, uses huggingface_hub
2. Prodia API — free key, many uncensored SD/SDXL models
3. AI Horde — fully free, no key, community-powered GPUs

All follow the same callback pattern as engine.py (status/done/error).
"""

import io
import json
import threading
from PIL import Image

from models import CONFIG_DIR

_SETTINGS_FILE = CONFIG_DIR / "cloud.json"


def _bg(fn):
    threading.Thread(target=fn, daemon=True).start()


# ---------------------------------------------------------------------------
# Settings persistence
# ---------------------------------------------------------------------------

def load_settings():
    defaults = {"backend": "horde", "hf_token": "",
                "prodia_key": "", "horde_key": "0000000000",
                "cloud_model": "AlbedoBase XL (SDXL)"}
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


# ---------------------------------------------------------------------------
# Cloud model registry — higher quality than local SD 1.5
# ---------------------------------------------------------------------------

CLOUD_MODELS = {
    "huggingface": [
        {"id": "stabilityai/stable-diffusion-xl-base-1.0",
         "name": "SDXL 1.0", "desc": "Best quality. 1024x1024 native."},
        {"id": "stablediffusionapi/wai-nsfw-illustrious-sdxl",
         "name": "WAI-NSFW SDXL", "desc": "SDXL fine-tune. Unrestricted."},
        {"id": "SG161222/Realistic_Vision_V5.1_noVAE",
         "name": "Realistic Vision v5.1", "desc": "Photorealistic humans. Uncensored."},
        {"id": "stablediffusionapi/deliberate-v2",
         "name": "Deliberate v2", "desc": "Versatile realistic. Uncensored."},
        {"id": "dreamlike-art/dreamlike-photoreal-2.0",
         "name": "Dreamlike Photoreal", "desc": "Photo + artistic flair."},
        {"id": "black-forest-labs/FLUX.1-schnell",
         "name": "Flux Schnell", "desc": "Latest gen. Very fast, high quality."},
        {"id": "black-forest-labs/FLUX.1-dev",
         "name": "Flux Dev", "desc": "Latest gen. Slower, highest quality."},
    ],
    "prodia": [
        {"id": "sdxl", "name": "SDXL", "desc": "High quality 1024px."},
        {"id": "realistic_vision_v5.1", "name": "Realistic Vision v5.1",
         "desc": "Photorealistic. Uncensored."},
        {"id": "deliberate_v2", "name": "Deliberate v2",
         "desc": "Versatile realistic. Uncensored."},
        {"id": "rev_animated", "name": "RevAnimated",
         "desc": "Anime + semi-realistic."},
    ],
    "horde": [
        {"id": "AlbedoBase XL (SDXL)", "name": "AlbedoBase XL",
         "desc": "High-quality SDXL. Unrestricted."},
        {"id": "ICBINP XL", "name": "ICBINP XL",
         "desc": "Photorealistic SDXL. Unrestricted."},
        {"id": "WAI-NSFW-illustrious-SDXL", "name": "WAI-NSFW SDXL",
         "desc": "SDXL NSFW fine-tune. Best for unrestricted."},
        {"id": "Pony Diffusion XL", "name": "Pony Diffusion XL",
         "desc": "SDXL fine-tune. Versatile unrestricted."},
        {"id": "Deliberate", "name": "Deliberate",
         "desc": "Realistic. Uncensored."},
        {"id": "PPP", "name": "PPP",
         "desc": "Realistic humans. NSFW-tuned."},
        {"id": "SDXL 1.0", "name": "SDXL 1.0",
         "desc": "Standard SDXL baseline."},
        {"id": "stable_diffusion", "name": "SD 1.5",
         "desc": "Fastest on Horde."},
    ],
}


# ---------------------------------------------------------------------------
# Backend 1: HuggingFace Inference API
# ---------------------------------------------------------------------------

def _hf_generate(prompt, neg="", model="", w=512, h=512, steps=30,
                 cfg=7.0, image=None, strength=0.75,
                 token="", status=None, done=None, error=None):
    def _run():
        try:
            from huggingface_hub import InferenceClient
            if status: status(f"Cloud: connecting to HuggingFace...")

            client = InferenceClient(token=token or None)
            model_id = model or "stabilityai/stable-diffusion-xl-base-1.0"

            kwargs = {
                "negative_prompt": neg or None,
                "guidance_scale": cfg,
                "num_inference_steps": steps,
                "width": w // 8 * 8,
                "height": h // 8 * 8,
            }

            if image is not None:
                if status: status(f"Cloud img2img: {model_id}...")
                result = client.image_to_image(
                    image, prompt=prompt, model=model_id,
                    strength=strength, **kwargs)
            else:
                if status: status(f"Cloud txt2img: {model_id}...")
                result = client.text_to_image(
                    prompt, model=model_id, **kwargs)

            if isinstance(result, bytes):
                result = Image.open(io.BytesIO(result))

            if status: status("Cloud generation complete.")
            if done: done(result, -1)

        except Exception as e:
            msg = str(e)
            if "rate limit" in msg.lower() or "429" in msg:
                msg += ("\n\nFree tier rate limited. Wait a moment and retry,\n"
                        "or add a HuggingFace token for higher limits.")
            if error: error(msg)
    _bg(_run)


# ---------------------------------------------------------------------------
# Backend 2: Prodia API (free key from prodia.com)
# ---------------------------------------------------------------------------

def _prodia_generate(prompt, neg="", model="sdxl", w=512, h=512,
                     steps=30, cfg=7.0, key="",
                     status=None, done=None, error=None):
    def _run():
        try:
            import urllib.request
            import time

            if not key:
                if error:
                    error("Prodia API key required.\n\n"
                          "Get a free key at prodia.com\n"
                          "then enter it in Cloud Settings.")
                return

            if status: status(f"Cloud: sending to Prodia ({model})...")

            headers = {"X-Prodia-Key": key,
                       "Content-Type": "application/json"}
            body = json.dumps({
                "model": model, "prompt": prompt,
                "negative_prompt": neg,
                "width": w, "height": h,
                "steps": steps, "cfg_scale": cfg,
            }).encode()

            req = urllib.request.Request(
                "https://api.prodia.com/v1/sd/generate",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                job = json.loads(resp.read())

            job_id = job["job"]
            if status: status(f"Cloud: generating (job {job_id[:8]})...")

            for _ in range(120):
                time.sleep(2)
                req = urllib.request.Request(
                    f"https://api.prodia.com/v1/job/{job_id}",
                    headers=headers)
                with urllib.request.urlopen(req, timeout=15) as resp:
                    result = json.loads(resp.read())

                if result["status"] == "succeeded":
                    img_url = result["imageUrl"]
                    req = urllib.request.Request(img_url)
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        img = Image.open(io.BytesIO(resp.read()))
                    if status: status("Cloud generation complete.")
                    if done: done(img, -1)
                    return
                elif result["status"] == "failed":
                    if error: error("Prodia job failed.")
                    return

            if error: error("Prodia job timed out (4 min).")

        except Exception as e:
            if error: error(f"Prodia error: {e}")
    _bg(_run)


# ---------------------------------------------------------------------------
# Backend 3: AI Horde (free, no key needed, community GPUs)
# ---------------------------------------------------------------------------

_HORDE_API = "https://stablehorde.net/api/v2"


def _horde_generate(prompt, neg="", model="SDXL 1.0", w=512, h=512,
                    steps=30, cfg=7.0, key="0000000000",
                    status=None, done=None, error=None):
    def _run():
        try:
            import urllib.request
            import time

            if status: status(f"Cloud: submitting to AI Horde ({model})...")

            headers = {"apikey": key or "0000000000",
                       "Content-Type": "application/json"}
            body = json.dumps({
                "prompt": prompt,
                "params": {
                    "sampler_name": "k_dpmpp_2m",
                    "cfg_scale": cfg, "steps": steps,
                    "width": w // 64 * 64, "height": h // 64 * 64,
                    "karras": True,
                },
                "nsfw": True, "censor_nsfw": False,
                "models": [model],
                "r2": True,
            }).encode()

            if neg:
                body_dict = json.loads(body)
                body_dict["prompt"] = f"{prompt} ### {neg}"
                body = json.dumps(body_dict).encode()

            req = urllib.request.Request(
                f"{_HORDE_API}/generate/async",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=30) as resp:
                job = json.loads(resp.read())

            job_id = job["id"]
            if status: status(f"Cloud: queued on Horde (ID {job_id[:8]})...")

            for _ in range(180):
                time.sleep(3)
                req = urllib.request.Request(
                    f"{_HORDE_API}/generate/check/{job_id}",
                    headers={"apikey": key or "0000000000"})
                with urllib.request.urlopen(req, timeout=15) as resp:
                    check = json.loads(resp.read())

                if check.get("done"):
                    req = urllib.request.Request(
                        f"{_HORDE_API}/generate/status/{job_id}",
                        headers={"apikey": key or "0000000000"})
                    with urllib.request.urlopen(req, timeout=15) as resp:
                        result = json.loads(resp.read())

                    gens = result.get("generations", [])
                    if not gens:
                        if error: error("Horde returned no image.")
                        return

                    img_url = gens[0].get("img")
                    if img_url:
                        req = urllib.request.Request(img_url)
                        with urllib.request.urlopen(req, timeout=30) as resp:
                            img = Image.open(io.BytesIO(resp.read()))
                        if status: status("Cloud generation complete.")
                        if done: done(img, -1)
                        return

                wp = check.get("wait_time", 0)
                qp = check.get("queue_position", "?")
                if status:
                    status(f"Cloud: queue #{qp}, ~{wp}s remaining...")

            if error: error("AI Horde timed out (9 min). Try again later.")

        except Exception as e:
            if error: error(f"AI Horde error: {e}")
    _bg(_run)


# ---------------------------------------------------------------------------
# Unified API — called by GUI
# ---------------------------------------------------------------------------

def generate(prompt, neg="", w=512, h=512, steps=30, cfg=7.0,
             image=None, strength=0.75,
             backend=None, model=None,
             status=None, done=None, error=None):
    """Generate via cloud. Backend auto-selected from settings if not given."""
    settings = load_settings()
    backend = backend or settings["backend"]
    model = model or settings["cloud_model"]

    if backend == "huggingface":
        _hf_generate(prompt, neg, model, w, h, steps, cfg,
                     image, strength, settings["hf_token"],
                     status, done, error)

    elif backend == "prodia":
        _prodia_generate(prompt, neg, model, w, h, steps, cfg,
                         settings["prodia_key"], status, done, error)

    elif backend == "horde":
        _horde_generate(prompt, neg, model, w, h, steps, cfg,
                        settings["horde_key"], status, done, error)

    else:
        if error: error(f"Unknown backend: {backend}")
