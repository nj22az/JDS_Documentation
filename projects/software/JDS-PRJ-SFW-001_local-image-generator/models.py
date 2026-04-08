"""models.py — Config, constants, model registry, colour palette."""

import json
import threading
from pathlib import Path

APP_NAME = "JDS Image Studio"
APP_VERSION = "5.2.0"

CONFIG_DIR = Path.home() / ".jds-image-studio"
CONFIG_FILE = CONFIG_DIR / "config.json"
MODELS_DIR = CONFIG_DIR / "models"
HISTORY_DIR = CONFIG_DIR / "history"
OUTPUT_DIR = Path.home() / "Pictures" / "JDS-Image-Studio"

# Shared defaults — used by engine, cloudgen, gui
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512
DEFAULT_STEPS = 30
DEFAULT_CFG = 7.0
MAX_SEED = 2**32 - 1

# Face detection
FACE_DET_SIZE = (640, 640)
FACE_CROP_PAD = 0.3
IDENTITY_THUMB_SIZE = (512, 512)

# Upscaling / hires fix
HIRES_MAX_DIM = 1536
UPSCALE_TILE = 256
FACE_FIX_MAX_DIM = 768
FACE_FIX_STRENGTH = 0.4

# Diffusion refinement (DiffFace)
REFINE_STEPS = 15
REFINE_CFG = 5.0
REFINE_STRENGTH = 0.25

# Pose quality thresholds
POSE_POOR = 0.3
POSE_WARN = 0.5

# Mask parameters
LANDMARK_BLUR_SIZE = (51, 51)
LANDMARK_BLUR_SIGMA = 20
FACE_ELLIPSE_W = 0.55
FACE_ELLIPSE_H = 0.65
DEFAULT_BRUSH_SIZE = 30
MASK_OVERLAY_ALPHA = 100

# Cloud API
HORDE_ANON_KEY = "0000000000"
HORDE_API_BASE = "https://stablehorde.net/api/v2"
PRODIA_API_URL = "https://api.prodia.com/v1/sd/generate"
REPLICATE_API_BASE = "https://api.replicate.com/v1"
HTTP_TIMEOUT = 30
HTTP_TIMEOUT_SHORT = 15
PRODIA_MAX_POLLS = 120
HORDE_MAX_POLLS = 180
REPLICATE_MAX_POLLS = 180

# Video generation
VIDEO_FRAMES_DEFAULT = 25
VIDEO_FPS_DEFAULT = 7
VIDEO_MOTION_STRENGTH = 127

# GUI
WINDOW_SIZE = "1200x820"
WINDOW_MIN = (1000, 700)
SIDEBAR_WIDTH = 330
SIZE_PRESETS = [(512, 512), (512, 768), (768, 512), (768, 768), (1024, 1024)]

# --- Prompt Enhancement (Playbox-grade realism) ---
# Quality anchors prepended to user prompt when "Enhance" is on
QUALITY_ANCHORS = {
    "Photorealistic": (
        "photorealistic, ultra-detailed skin textures with visible pores "
        "and subsurface scattering, sharp focus, natural skin tones, "
        "realistic anatomy, highly detailed face and body"
    ),
    "Asian Realism": (
        "photorealistic, beautiful asian woman, ultra-detailed skin textures "
        "with visible pores and subsurface scattering, natural asian features, "
        "monolid or double eyelid eyes, warm natural skin tone, "
        "sharp focus, realistic anatomy, highly detailed face and body, "
        "professional photography, 8K UHD"
    ),
    "Gravure": (
        "photorealistic, japanese gravure idol photography, magazine quality, "
        "ultra-detailed skin textures, natural asian skin tones, sharp focus, "
        "professional studio photography, highly detailed face and body, "
        "beautiful japanese woman, natural features"
    ),
    "K-Beauty": (
        "photorealistic, beautiful korean woman, flawless dewy skin, "
        "ultra-detailed skin textures, natural korean features, "
        "glass skin effect, soft luminous complexion, sharp focus, "
        "professional beauty photography, highly detailed face"
    ),
    "Portrait": (
        "photorealistic portrait, ultra-detailed face, catchlight in eyes, "
        "visible skin pores, natural skin tones, sharp focus, "
        "professional headshot, studio photography"
    ),
    "Cinematic": (
        "photorealistic, cinematic still frame, ultra-detailed, "
        "film grain, anamorphic lens, natural skin tones, "
        "highly detailed face and body, movie quality"
    ),
}

# Lighting presets appended to enhanced prompts
LIGHTING_PRESETS = {
    "Studio soft": "soft volumetric studio lighting, even illumination, "
                   "subtle shadows, professional photography",
    "Golden hour": "golden hour side lighting, warm tones, "
                   "long soft shadows, natural sunlight",
    "Rembrandt": "Rembrandt lighting, dramatic side light, "
                 "triangle highlight on cheek, dark background",
    "High key": "high key lighting, bright even illumination, "
                "minimal shadows, white background",
    "Natural window": "soft natural window light, gentle shadows, "
                      "ambient fill, indoor photography",
    "Ring light": "ring light, even face illumination, "
                  "catchlight rings in eyes, beauty photography",
    "None": "",
}

# Lens simulation terms appended for extra realism
LENS_PRESETS = {
    "85mm portrait": "85mm lens at f/1.8, shallow depth of field, "
                     "creamy bokeh background",
    "50mm standard": "50mm lens at f/2.8, natural perspective, "
                     "moderate depth of field",
    "135mm telephoto": "135mm lens at f/2.0, compressed background, "
                       "strong bokeh, subject isolation",
    "35mm wide": "35mm lens at f/4.0, environmental context, "
                 "wide angle, full scene visible",
    "None": "",
}

# Master enhanced negative — comprehensive artifact prevention
ENHANCED_NEGATIVE = (
    "cartoon, anime, drawing, painting, illustration, sketch, 3d render, "
    "cgi, doll, plastic, deformed, ugly, blurry, bad anatomy, bad hands, "
    "extra fingers, missing fingers, extra limbs, disfigured, out of frame, "
    "mutated anatomy, fused fingers, too many fingers, long neck, "
    "malformed limbs, poorly drawn face, poorly drawn hands, "
    "disproportionate body, oversized breasts, unrealistic body proportions, "
    "bad eyes, asymmetric eyes, deformed iris, deformed pupils, "
    "bad skin, waxy skin, plastic skin, uncanny valley, "
    "overexposed, underexposed, flat lighting, "
    "watermark, text, logo, signature, low quality, lowres, jpeg artifacts"
)

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

# Negative prompt presets (selectable in GUI)
NEG_PRESETS = {
    "Photo (general)": (
        "cartoon, anime, drawing, painting, illustration, sketch, 3d render, "
        "cgi, doll, plastic, deformed, ugly, blurry, bad anatomy, bad hands, "
        "extra fingers, missing fingers, extra limbs, disfigured, out of frame, "
        "watermark, text, logo, signature, low quality, jpeg artifacts"
    ),
    "Realistic body": (
        "cartoon, anime, 3d render, cgi, doll, plastic, deformed, ugly, blurry, "
        "bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
        "disfigured, disproportionate body, oversized breasts, unnaturally large breasts, "
        "unrealistic body proportions, inflated body parts, bad feet, fused fingers, "
        "too many fingers, long neck, mutated hands, poorly drawn hands, "
        "poorly drawn face, mutation, extra legs, extra arms, malformed limbs, "
        "watermark, text, logo, signature, low quality, jpeg artifacts"
    ),
    "Portrait (face)": (
        "bad eyes, asymmetric eyes, deformed iris, deformed pupils, "
        "bad teeth, crooked teeth, extra teeth, deformed face, ugly face, "
        "blurry face, poorly drawn face, asymmetric face, bad skin, "
        "plastic skin, waxy skin, doll face, uncanny valley, "
        "cartoon, anime, 3d render, painting, watermark, text, low quality"
    ),
    "Artistic (minimal)": (
        "blurry, low quality, watermark, text, logo, signature, "
        "jpeg artifacts, deformed, ugly, bad anatomy"
    ),
    "Asian realism": (
        "cartoon, anime, drawing, painting, illustration, sketch, 3d render, "
        "cgi, doll, plastic, deformed, ugly, blurry, bad anatomy, bad hands, "
        "extra fingers, missing fingers, extra limbs, disfigured, "
        "western features, caucasian features, blue eyes, blonde hair, "
        "unrealistic eye size, anime eyes, exaggerated features, "
        "oversized breasts, disproportionate body, bad skin, waxy skin, "
        "flat lighting, overexposed, watermark, text, logo, signature, "
        "low quality, jpeg artifacts, bad eyes, asymmetric face"
    ),
    "Gravure (glamour)": (
        "cartoon, anime, 3d render, cgi, doll, plastic, deformed, ugly, blurry, "
        "bad anatomy, bad hands, extra fingers, missing fingers, extra limbs, "
        "disfigured, disproportionate body, oversized breasts, bad skin, "
        "waxy skin, flat lighting, harsh shadows, underexposed, overexposed, "
        "watermark, text, logo, signature, low quality, jpeg artifacts, "
        "bad eyes, asymmetric face, poorly drawn face, bad teeth"
    ),
}

# iOS flat colour palette (all UI colours centralized here)
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
    "pink":     "#FF2D55",
    "pink_h":   "#CC1A3D",
    "purple":   "#AF52DE",
    "purple_h": "#8B3FBF",
    "indigo":   "#5856D6",
    "indigo_h": "#4240A8",
}


# Shared background thread launcher (used by all modules)
def bg_thread(fn):
    """Run fn in a daemon thread."""
    threading.Thread(target=fn, daemon=True).start()

# --- Avatar Creator (realistic character builder) ---
AVATAR_ETHNICITY = [
    "Japanese", "Korean", "Chinese", "Vietnamese", "Thai",
    "Filipino", "Indonesian", "Malaysian", "Taiwanese",
    "Mixed Asian",
]

AVATAR_AGE = [
    "18-20 (young)", "21-25 (early twenties)", "26-30 (late twenties)",
    "31-35 (early thirties)", "36-40 (late thirties)", "41-50 (mature)",
]

AVATAR_HAIR_STYLE = [
    "straight long hair", "straight medium hair", "straight short bob",
    "wavy long hair", "wavy shoulder-length hair",
    "curly long hair", "curly medium hair",
    "bangs with long hair", "bangs with bob cut",
    "side-swept bangs", "curtain bangs",
    "ponytail", "high ponytail", "low ponytail",
    "twin tails", "braided hair", "messy bun", "elegant updo",
    "pixie cut", "layered medium hair",
    "wet hair look", "beach waves",
]

AVATAR_HAIR_COLOR = [
    "natural black", "dark brown", "light brown", "auburn",
    "honey brown", "chestnut", "ash brown",
    "blonde highlights", "ombre brown to blonde",
    "red tinted", "burgundy", "dark red",
    "pink", "purple", "blue-black",
]

AVATAR_EYE_COLOR = [
    "dark brown", "brown", "light brown", "hazel",
    "amber", "dark eyes", "black",
]

AVATAR_EYE_SHAPE = [
    "natural asian eyes", "monolid", "double eyelid",
    "almond-shaped eyes", "round eyes", "hooded eyes",
    "cat eyes", "upturned eyes",
]

AVATAR_FACE_SHAPE = [
    "oval face", "round face", "heart-shaped face",
    "v-line jaw face", "diamond face", "square jaw face",
]

AVATAR_SKIN_TONE = [
    "fair porcelain skin", "light ivory skin", "natural beige skin",
    "warm golden skin", "light tan skin", "medium tan skin",
    "honey skin tone", "olive skin tone",
]

AVATAR_LIPS = [
    "natural lips", "full lips", "thin lips",
    "gradient lip tint (korean style)", "red lipstick",
    "pink lipstick", "nude lipstick", "berry lipstick",
    "coral lipstick", "no makeup lips", "glossy lips",
]

AVATAR_MAKEUP = [
    "natural no-makeup look", "light natural makeup",
    "korean glass skin makeup", "soft glam makeup",
    "smoky eye makeup", "cat eye eyeliner",
    "dewy luminous makeup", "matte elegant makeup",
    "heavy glamour makeup", "editorial bold makeup",
]

AVATAR_BREAST_SIZE = [
    "flat chest", "small breasts (A cup)", "small-medium breasts (B cup)",
    "medium breasts (C cup)", "medium-large breasts (D cup)",
    "large breasts (DD cup)", "very large breasts",
]

AVATAR_BUTT_SIZE = [
    "small flat butt", "small round butt", "medium round butt",
    "athletic toned butt", "large round butt", "very curvy butt",
]

AVATAR_BODY_TYPE = [
    "very slim, thin frame", "slim, slender figure",
    "slim fit, toned body", "athletic, muscular tone",
    "average build, natural curves", "curvy hourglass figure",
    "full figured, voluptuous", "petite and slim",
]

AVATAR_POSE = [
    "standing naturally", "sitting elegantly", "leaning forward",
    "looking over shoulder", "hands on hips", "arms crossed",
    "lying on side", "kneeling", "walking towards camera",
    "candid laughing", "playful pose", "confident pose",
    "shy pose, looking down", "stretching", "dynamic action pose",
]

AVATAR_EXPRESSION = [
    "soft smile", "confident smile", "serious look",
    "playful wink", "sultry gaze", "innocent look",
    "laughing", "shy expression", "pouting lips",
    "surprised look", "dreamy expression", "fierce look",
]

AVATAR_OUTFIT = [
    "None (use prompt)", "casual t-shirt and jeans", "summer dress",
    "elegant evening dress", "school uniform", "office blouse and skirt",
    "crop top and shorts", "bikini swimsuit", "one-piece swimsuit",
    "lingerie set", "silk robe", "kimono", "hanbok",
    "athletic wear", "oversized sweater", "leather jacket",
    "cocktail dress", "wedding dress",
    "topless", "nude",
]

AVATAR_SETTING = [
    "None (use prompt)", "professional studio, white background",
    "studio, dark background", "bedroom, soft lighting",
    "beach, golden hour", "Tokyo street, neon lights",
    "cherry blossom garden", "rooftop cityscape",
    "cafe interior, window light", "bathroom, steam",
    "pool, summer sun", "hotel room, luxury",
    "forest, dappled sunlight", "rain, wet streets",
    "gym, dramatic lighting", "onsen hot spring",
]

# Ready-to-use prompt templates (fill prompt box with one click)
PROMPT_TEMPLATES = {
    "Template...": "",
    "Asian — studio portrait": (
        "beautiful {japanese|korean|chinese|vietnamese} woman, "
        "close-up portrait, natural makeup, black hair, brown eyes, "
        "soft smile, detailed skin texture, professional studio lighting"
    ),
    "Asian — full body": (
        "beautiful {japanese|korean|chinese} woman, full body shot, "
        "slim natural figure, elegant pose, {casual outfit|summer dress|business attire}, "
        "natural lighting, professional photography"
    ),
    "Asian — outdoor": (
        "beautiful {japanese|korean|vietnamese} woman, outdoor photoshoot, "
        "{cherry blossom garden|urban tokyo street|tropical beach|bamboo forest}, "
        "natural sunlight, candid pose, magazine quality"
    ),
    "Gravure — beach": (
        "japanese gravure idol, beach photoshoot, {white bikini|red bikini|black swimsuit}, "
        "ocean background, golden hour sunlight, wet skin, "
        "natural body, playful pose, magazine cover"
    ),
    "Gravure — studio": (
        "japanese gravure idol, studio photoshoot, {white lingerie|black lingerie|silk robe}, "
        "soft studio lighting, natural body proportions, "
        "elegant pose, warm skin tones, magazine editorial"
    ),
    "Gravure — casual": (
        "japanese gravure idol, {school uniform|oversized sweater|crop top and shorts}, "
        "indoor setting, natural window light, relaxed pose, "
        "cute expression, magazine quality photography"
    ),
    "K-Beauty — closeup": (
        "beautiful korean woman, beauty closeup, glass skin, dewy complexion, "
        "{natural makeup|gradient lip tint|smoky eye}, flawless skin, "
        "ring light, beauty campaign photography"
    ),
    "K-Beauty — fashion": (
        "beautiful korean woman, {elegant hanbok|modern streetwear|luxury fashion}, "
        "{Seoul cityscape|traditional palace|minimalist studio} background, "
        "editorial photography, sharp focus"
    ),
    "Asian — artistic": (
        "beautiful {japanese|korean|chinese} woman, fine art photography, "
        "{flowing silk fabric|flower petals|water reflections}, "
        "dramatic {Rembrandt|butterfly|split} lighting, museum quality"
    ),
    "Asian — fitness": (
        "beautiful {japanese|korean} woman, fitness photoshoot, "
        "{yoga pose|athletic wear|gym setting}, toned body, "
        "natural proportions, professional sports photography"
    ),
}

LIGHT_DIRS = ["left", "right", "top", "bottom",
              "top-left", "top-right", "bottom-left", "bottom-right"]

# Inpaint workflow presets — prompt + negative for common edit tasks
INPAINT_PRESETS = {
    "Custom (manual)": {"prompt": "", "neg": ""},
    "Remove clothing": {
        "prompt": "bare skin, natural body, realistic anatomy, "
                  "detailed skin texture, photorealistic",
        "neg": "clothing, fabric, cloth, shirt, dress, pants, underwear, "
               "deformed, bad anatomy, blurry, doll, plastic, cartoon",
    },
    "Change outfit": {
        "prompt": "wearing elegant dress, high fashion, photorealistic, "
                  "detailed fabric texture",
        "neg": "deformed, bad anatomy, blurry, low quality, cartoon",
    },
    "Swimwear": {
        "prompt": "wearing bikini swimsuit, beach, realistic skin, "
                  "photorealistic, natural body",
        "neg": "deformed, bad anatomy, blurry, cartoon, plastic",
    },
    "Lingerie": {
        "prompt": "wearing delicate lace lingerie, photorealistic, "
                  "detailed fabric, natural body proportions",
        "neg": "deformed, bad anatomy, blurry, plastic, cartoon",
    },
    "Artistic nude": {
        "prompt": "fine art nude photograph, studio lighting, "
                  "museum quality, elegant pose, realistic anatomy",
        "neg": "vulgar, deformed, bad anatomy, blurry, low quality, "
               "cartoon, plastic, oversized breasts",
    },
    "Enhance body": {
        "prompt": "fit athletic body, natural proportions, "
                  "realistic anatomy, detailed skin texture",
        "neg": "deformed, bad anatomy, disproportionate, oversized, "
               "blurry, plastic, cartoon",
    },
    "Gravure — swimwear": {
        "prompt": "gravure idol swimsuit photoshoot, japanese model, bikini, "
                  "natural body, soft studio lighting, professional photography, "
                  "magazine quality, warm skin tones, detailed skin texture",
        "neg": "cartoon, anime, 3d render, deformed, bad anatomy, blurry, "
               "plastic, doll, oversized breasts, harsh shadows, low quality",
    },
    "Gravure — lingerie": {
        "prompt": "gravure idol lingerie photoshoot, japanese model, delicate lace, "
                  "soft diffused lighting, warm tones, natural body proportions, "
                  "professional studio, magazine editorial, photorealistic",
        "neg": "cartoon, anime, 3d render, deformed, bad anatomy, blurry, "
               "plastic, doll, oversized breasts, harsh shadows, low quality",
    },
    "Gravure — portrait": {
        "prompt": "gravure idol close-up portrait, japanese model, beautiful face, "
                  "soft bokeh background, natural makeup, warm studio lighting, "
                  "magazine cover quality, catchlight in eyes, photorealistic",
        "neg": "cartoon, anime, 3d render, deformed, bad eyes, asymmetric face, "
               "blurry face, plastic skin, waxy, bad teeth, low quality",
    },
}


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
