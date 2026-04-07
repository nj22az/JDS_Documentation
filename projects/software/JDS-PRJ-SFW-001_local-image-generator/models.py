"""models.py — Config, constants, model registry, colour palette."""

import json
from pathlib import Path

APP_NAME = "JDS Image Studio"
APP_VERSION = "3.0.0"

CONFIG_DIR = Path.home() / ".jds-image-studio"
CONFIG_FILE = CONFIG_DIR / "config.json"
MODELS_DIR = CONFIG_DIR / "models"
OUTPUT_DIR = Path.home() / "Pictures" / "JDS-Image-Studio"

# Curated models — realistic humans, faces, unrestricted
MODELS = [
    {"id": "SG161222/Realistic_Vision_V5.1_noVAE",
     "name": "Realistic Vision v5.1",
     "desc": "Top pick for photorealistic humans and faces. Uncensored.",
     "size": "~5 GB", "default": True},
    {"id": "dreamlike-art/dreamlike-photoreal-2.0",
     "name": "Dreamlike Photoreal 2.0",
     "desc": "Photorealistic with artistic flair. Great skin tones.",
     "size": "~4 GB"},
    {"id": "stablediffusionapi/deliberate-v2",
     "name": "Deliberate v2",
     "desc": "Versatile realistic model. Strong anatomy, uncensored.",
     "size": "~4 GB"},
    {"id": "runwayml/stable-diffusion-v1-5",
     "name": "Stable Diffusion 1.5",
     "desc": "Fastest. Huge LoRA ecosystem. Good base for any style.",
     "size": "~4 GB"},
    {"id": "stabilityai/stable-diffusion-2-1",
     "name": "Stable Diffusion 2.1",
     "desc": "Official baseline. General purpose.",
     "size": "~5 GB"},
]

# Photo-optimised negative prompt
NEG_PHOTO = (
    "cartoon, anime, drawing, painting, illustration, sketch, 3d render, "
    "cgi, doll, plastic, deformed, ugly, blurry, bad anatomy, bad hands, "
    "extra fingers, missing fingers, extra limbs, disfigured, out of frame, "
    "watermark, text, logo, signature, low quality, jpeg artifacts"
)

# iOS flat colour palette
C = {
    "bg":       "#F2F2F7",
    "surface":  "#FFFFFF",
    "text":     "#1C1C1E",
    "muted":    "#8E8E93",
    "accent":   "#007AFF",
    "hover":    "#0056CC",
    "red":      "#FF3B30",
    "green":    "#34C759",
    "orange":   "#FF9500",
    "sep":      "#E5E5EA",
    "fill":     "#E5E5EA",
    "mask_red": "#FF3B30",
}

LIGHT_DIRS = ["left", "right", "top", "bottom",
              "top-left", "top-right", "bottom-left", "bottom-right"]


def load_config():
    defaults = {
        "model_id": "", "output_dir": str(OUTPUT_DIR),
        "width": 512, "height": 512, "steps": 30,
        "guidance": 7.0, "downloaded": [],
    }
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE) as f:
                defaults.update(json.load(f))
        except Exception:
            pass
    return defaults


def save_config(cfg):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)
