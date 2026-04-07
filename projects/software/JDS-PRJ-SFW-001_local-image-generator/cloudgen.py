"""cloudgen.py — Cloud image + video generation backends (optional).

Four free backends for images:
1. HuggingFace Inference API — zero new deps, uses huggingface_hub
2. Prodia API — free key, many uncensored SD/SDXL models
3. AI Horde — fully free, no key, community-powered GPUs
4. Replicate — free tier, best Flux hosting, video generation

Plus cloud video generation (image-to-video via Replicate or HuggingFace).

All follow the same callback pattern as engine.py (status/done/error).
"""

import io
import json
import base64
from PIL import Image

from models import (CONFIG_DIR, DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_STEPS,
                    DEFAULT_CFG, HORDE_ANON_KEY, HORDE_API_BASE,
                    PRODIA_API_URL, REPLICATE_API_BASE,
                    HTTP_TIMEOUT, HTTP_TIMEOUT_SHORT,
                    PRODIA_MAX_POLLS, HORDE_MAX_POLLS, REPLICATE_MAX_POLLS,
                    VIDEO_FRAMES_DEFAULT, VIDEO_FPS_DEFAULT,
                    VIDEO_MOTION_STRENGTH, OUTPUT_DIR, bg_thread as _bg)

_SETTINGS_FILE = CONFIG_DIR / "cloud.json"


# ---------------------------------------------------------------------------
# Settings persistence
# ---------------------------------------------------------------------------

def load_settings():
    defaults = {"backend": "horde", "hf_token": "",
                "prodia_key": "", "horde_key": HORDE_ANON_KEY,
                "replicate_token": "",
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
    "replicate": [
        {"id": "black-forest-labs/flux-1.1-pro",
         "name": "Flux 1.1 Pro", "desc": "Best quality Flux. Fast."},
        {"id": "black-forest-labs/flux-schnell",
         "name": "Flux Schnell", "desc": "Fastest Flux. 4 steps."},
        {"id": "black-forest-labs/flux-dev",
         "name": "Flux Dev", "desc": "High quality Flux. Slower."},
        {"id": "stability-ai/sdxl",
         "name": "SDXL", "desc": "Stable Diffusion XL via Replicate."},
        {"id": "lucataco/realistic-vision-v5.1",
         "name": "Realistic Vision v5.1", "desc": "Photorealistic. Uncensored."},
    ],
}

# Cloud video models (image-to-video)
VIDEO_MODELS = {
    "replicate": [
        {"id": "stability-ai/stable-video-diffusion",
         "name": "Stable Video Diffusion",
         "desc": "Image to 25-frame video. Best motion quality."},
        {"id": "minimax/video-01-live",
         "name": "MiniMax Video-01",
         "desc": "Image to video. Natural motion."},
        {"id": "wan-video/wan-2.1-i2v-480p",
         "name": "Wan 2.1 I2V",
         "desc": "Image to video. 480p. Fast."},
    ],
    "huggingface": [
        {"id": "stabilityai/stable-video-diffusion-img2vid-xt",
         "name": "SVD-XT",
         "desc": "Stable Video Diffusion. 25 frames. Free API."},
    ],
}


# ---------------------------------------------------------------------------
# Backend 1: HuggingFace Inference API
# ---------------------------------------------------------------------------

def _hf_generate(prompt, neg="", model="", w=DEFAULT_WIDTH, h=DEFAULT_HEIGHT,
                 steps=DEFAULT_STEPS, cfg=DEFAULT_CFG, image=None,
                 strength=0.75, token="", status=None, done=None, error=None):
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

def _prodia_generate(prompt, neg="", model="sdxl", w=DEFAULT_WIDTH,
                     h=DEFAULT_HEIGHT, steps=DEFAULT_STEPS, cfg=DEFAULT_CFG,
                     key="",
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
                PRODIA_API_URL,
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                job = json.loads(resp.read())

            job_id = job["job"]
            if status: status(f"Cloud: generating (job {job_id[:8]})...")

            for _ in range(PRODIA_MAX_POLLS):
                time.sleep(2)
                req = urllib.request.Request(
                    f"https://api.prodia.com/v1/job/{job_id}",
                    headers=headers)
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SHORT) as resp:
                    result = json.loads(resp.read())

                if result["status"] == "succeeded":
                    img_url = result["imageUrl"]
                    req = urllib.request.Request(img_url)
                    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
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

def _horde_generate(prompt, neg="", model="SDXL 1.0", w=DEFAULT_WIDTH,
                    h=DEFAULT_HEIGHT, steps=DEFAULT_STEPS, cfg=DEFAULT_CFG,
                    key=HORDE_ANON_KEY,
                    status=None, done=None, error=None):
    def _run():
        try:
            import urllib.request
            import time

            if status: status(f"Cloud: submitting to AI Horde ({model})...")

            headers = {"apikey": key or HORDE_ANON_KEY,
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
                f"{HORDE_API_BASE}/generate/async",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                job = json.loads(resp.read())

            job_id = job["id"]
            if status: status(f"Cloud: queued on Horde (ID {job_id[:8]})...")

            for _ in range(HORDE_MAX_POLLS):
                time.sleep(3)
                req = urllib.request.Request(
                    f"{HORDE_API_BASE}/generate/check/{job_id}",
                    headers={"apikey": key or HORDE_ANON_KEY})
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SHORT) as resp:
                    check = json.loads(resp.read())

                if check.get("done"):
                    req = urllib.request.Request(
                        f"{HORDE_API_BASE}/generate/status/{job_id}",
                        headers={"apikey": key or HORDE_ANON_KEY})
                    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SHORT) as resp:
                        result = json.loads(resp.read())

                    gens = result.get("generations", [])
                    if not gens:
                        if error: error("Horde returned no image.")
                        return

                    img_url = gens[0].get("img")
                    if img_url:
                        req = urllib.request.Request(img_url)
                        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
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

    elif backend == "replicate":
        _replicate_generate(prompt, neg, model, w, h, steps, cfg,
                            image, strength, settings["replicate_token"],
                            status, done, error)

    else:
        if error: error(f"Unknown backend: {backend}")


# ---------------------------------------------------------------------------
# Backend 4: Replicate (free tier available, best Flux host)
# ---------------------------------------------------------------------------

def _replicate_generate(prompt, neg="", model="", w=DEFAULT_WIDTH,
                        h=DEFAULT_HEIGHT, steps=DEFAULT_STEPS, cfg=DEFAULT_CFG,
                        image=None, strength=0.75, token="",
                        status=None, done=None, error=None):
    def _run():
        try:
            import urllib.request
            import time

            if not token:
                if error:
                    error("Replicate API token required.\n\n"
                          "Get a free token at replicate.com\n"
                          "then enter it in Cloud Settings.\n\n"
                          "Tip: HuggingFace and AI Horde are fully free — "
                          "switch backend if you prefer no-signup.")
                return

            model_id = model or "black-forest-labs/flux-schnell"
            if status: status(f"Cloud: sending to Replicate ({model_id})...")

            headers = {"Authorization": f"Bearer {token}",
                       "Content-Type": "application/json",
                       "Prefer": "wait"}

            input_data = {
                "prompt": prompt,
                "width": w // 8 * 8,
                "height": h // 8 * 8,
            }

            if neg:
                input_data["negative_prompt"] = neg
            if "flux" not in model_id.lower():
                input_data["num_inference_steps"] = steps
                input_data["guidance_scale"] = cfg

            if image is not None:
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                img_b64 = base64.b64encode(buf.getvalue()).decode()
                input_data["image"] = f"data:image/png;base64,{img_b64}"
                input_data["prompt_strength"] = strength

            body = json.dumps({
                "version": None,
                "input": input_data,
            }).encode()

            # Create prediction
            req = urllib.request.Request(
                f"{REPLICATE_API_BASE}/models/{model_id}/predictions",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                prediction = json.loads(resp.read())

            pred_url = prediction.get("urls", {}).get("get", "")
            pred_status = prediction.get("status", "")

            # If "Prefer: wait" returned completed result
            if pred_status == "succeeded":
                output = prediction.get("output")
                img_url = output[0] if isinstance(output, list) else output
                req = urllib.request.Request(img_url)
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                    img = Image.open(io.BytesIO(resp.read()))
                if status: status("Cloud generation complete.")
                if done: done(img, -1)
                return

            # Poll for completion
            if status: status("Cloud: generating...")
            for _ in range(REPLICATE_MAX_POLLS):
                time.sleep(2)
                req = urllib.request.Request(
                    pred_url, headers={"Authorization": f"Bearer {token}"})
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SHORT) as resp:
                    result = json.loads(resp.read())

                if result["status"] == "succeeded":
                    output = result.get("output")
                    img_url = output[0] if isinstance(output, list) else output
                    req = urllib.request.Request(img_url)
                    with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                        img = Image.open(io.BytesIO(resp.read()))
                    if status: status("Cloud generation complete.")
                    if done: done(img, -1)
                    return
                elif result["status"] == "failed":
                    if error: error(f"Replicate failed: {result.get('error', 'Unknown')}")
                    return

            if error: error("Replicate timed out (6 min).")

        except Exception as e:
            if error: error(f"Replicate error: {e}")
    _bg(_run)


# ---------------------------------------------------------------------------
# Cloud video generation (image-to-video)
# ---------------------------------------------------------------------------

def _image_to_base64(image):
    """Convert PIL Image to base64 data URI."""
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"


def generate_video(image, motion_strength=VIDEO_MOTION_STRENGTH,
                   frames=VIDEO_FRAMES_DEFAULT, fps=VIDEO_FPS_DEFAULT,
                   backend=None, model=None,
                   status=None, done=None, error=None):
    """Generate a short video from a still image via cloud.

    done callback receives (video_path, fps) — path to saved .mp4 file.
    """
    settings = load_settings()
    backend = backend or settings.get("video_backend", "huggingface")

    if backend == "huggingface":
        _hf_video(image, frames, fps, settings["hf_token"],
                  model, status, done, error)
    elif backend == "replicate":
        _replicate_video(image, motion_strength, frames, fps,
                         settings["replicate_token"], model,
                         status, done, error)
    else:
        if error: error(f"Unknown video backend: {backend}")


def _hf_video(image, frames=VIDEO_FRAMES_DEFAULT, fps=VIDEO_FPS_DEFAULT,
              token="", model=None, status=None, done=None, error=None):
    """Image-to-video via HuggingFace Inference API (free)."""
    def _run():
        try:
            from huggingface_hub import InferenceClient

            model_id = model or "stabilityai/stable-video-diffusion-img2vid-xt"
            if status: status(f"Cloud video: connecting to HuggingFace...")

            client = InferenceClient(token=token or None)

            # Resize to 1024x576 (SVD native resolution)
            img_resized = image.copy()
            img_resized = img_resized.resize((1024, 576), Image.LANCZOS)

            if status: status(f"Cloud video: generating {frames} frames...")

            # HF image-to-video endpoint
            buf = io.BytesIO()
            img_resized.save(buf, format="PNG")
            buf.seek(0)
            result = client.post(
                model=model_id,
                data=buf.getvalue(),
                task="image-to-video")

            # Save result as mp4
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            video_path = OUTPUT_DIR / f"video_{ts}.mp4"

            with open(video_path, "wb") as f:
                if isinstance(result, bytes):
                    f.write(result)
                else:
                    f.write(result.read())

            if status: status(f"Video saved: {video_path.name}")
            if done: done(str(video_path), fps)

        except Exception as e:
            msg = str(e)
            if "not supported" in msg.lower() or "404" in msg:
                msg = ("HuggingFace video model unavailable.\n\n"
                       "SVD may be down or rate-limited on free tier.\n"
                       "Try Replicate backend with a free token.")
            if error: error(f"HF video error: {msg}")
    _bg(_run)


def _replicate_video(image, motion_strength=VIDEO_MOTION_STRENGTH,
                     frames=VIDEO_FRAMES_DEFAULT, fps=VIDEO_FPS_DEFAULT,
                     token="", model=None,
                     status=None, done=None, error=None):
    """Image-to-video via Replicate API."""
    def _run():
        try:
            import urllib.request
            import time

            if not token:
                if error:
                    error("Replicate API token required for video.\n\n"
                          "Get a free token at replicate.com\n"
                          "then enter it in Cloud Settings.\n\n"
                          "Tip: Try HuggingFace backend for free video "
                          "(SVD-XT, no signup needed).")
                return

            model_id = model or "stability-ai/stable-video-diffusion"
            if status: status(f"Cloud video: sending to Replicate...")

            headers = {"Authorization": f"Bearer {token}",
                       "Content-Type": "application/json"}

            input_data = {
                "input_image": _image_to_base64(image),
                "frames_per_second": fps,
                "motion_bucket_id": motion_strength,
            }

            body = json.dumps({
                "version": None,
                "input": input_data,
            }).encode()

            req = urllib.request.Request(
                f"{REPLICATE_API_BASE}/models/{model_id}/predictions",
                data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as resp:
                prediction = json.loads(resp.read())

            pred_url = prediction.get("urls", {}).get("get", "")
            if status: status("Cloud video: generating frames...")

            for _ in range(REPLICATE_MAX_POLLS):
                time.sleep(3)
                req = urllib.request.Request(
                    pred_url, headers={"Authorization": f"Bearer {token}"})
                with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SHORT) as resp:
                    result = json.loads(resp.read())

                if result["status"] == "succeeded":
                    output = result.get("output")
                    video_url = output[0] if isinstance(output, list) else output

                    # Download video
                    req = urllib.request.Request(video_url)
                    with urllib.request.urlopen(req, timeout=60) as resp:
                        video_data = resp.read()

                    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
                    import datetime
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    video_path = OUTPUT_DIR / f"video_{ts}.mp4"

                    with open(video_path, "wb") as f:
                        f.write(video_data)

                    if status: status(f"Video saved: {video_path.name}")
                    if done: done(str(video_path), fps)
                    return
                elif result["status"] == "failed":
                    if error:
                        error(f"Replicate video failed: "
                              f"{result.get('error', 'Unknown')}")
                    return

                if status: status("Cloud video: still rendering...")

            if error: error("Replicate video timed out (9 min).")

        except Exception as e:
            if error: error(f"Replicate video error: {e}")
    _bg(_run)
