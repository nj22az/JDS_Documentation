"""history.py — Image history with metadata. Auto-saves every generation."""

import json
import datetime
from pathlib import Path
from PIL import Image

from models import HISTORY_DIR


def save(image, prompt, neg="", seed=0, model="",
         mode="txt2img", steps=30, cfg=7.0, width=512, height=512):
    """Auto-save image + metadata. Returns the saved path."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"{ts}_{seed}"

    img_path = HISTORY_DIR / f"{stem}.png"
    meta_path = HISTORY_DIR / f"{stem}.json"

    image.save(str(img_path))

    meta = {
        "prompt": prompt, "negative": neg, "seed": seed,
        "model": model, "mode": mode, "steps": steps,
        "cfg": cfg, "width": width, "height": height,
        "timestamp": ts, "file": img_path.name,
    }
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    return str(img_path)


def list_all(limit=100):
    """Return list of (img_path, metadata) tuples, newest first."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    entries = []
    for meta_file in sorted(HISTORY_DIR.glob("*.json"), reverse=True):
        if len(entries) >= limit:
            break
        try:
            with open(meta_file) as f:
                meta = json.load(f)
            img_path = HISTORY_DIR / meta["file"]
            if img_path.exists():
                entries.append((str(img_path), meta))
        except Exception:
            continue
    return entries


def load_thumb(path, size=(128, 128)):
    """Load a thumbnail for gallery display."""
    try:
        img = Image.open(path)
        img.thumbnail(size, Image.LANCZOS)
        return img
    except Exception:
        return None


def delete(img_path):
    """Delete an image and its metadata."""
    p = Path(img_path)
    p.unlink(missing_ok=True)
    p.with_suffix(".json").unlink(missing_ok=True)
