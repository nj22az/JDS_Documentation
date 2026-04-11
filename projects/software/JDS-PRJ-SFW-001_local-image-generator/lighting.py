"""lighting.py — Directional light and shadow simulation."""

import numpy as np
from PIL import Image, ImageFilter


def apply(image, direction="right", intensity=0.6, warmth=0.3):
    """
    Simulate directional light on a PIL image.
    direction: left/right/top/bottom/top-left/top-right/bottom-left/bottom-right
    intensity: 0.0–1.0   warmth: 0.0 (cool white) – 1.0 (golden)
    """
    img = image.convert("RGB")
    w, h = img.size
    arr = np.array(img, dtype=np.float32)

    x = np.linspace(0, 1, w)
    y = np.linspace(0, 1, h)
    xv, yv = np.meshgrid(x, y)

    grads = {
        "left": 1 - xv, "right": xv, "top": 1 - yv, "bottom": yv,
        "top-left": (2 - xv - yv) / 2, "top-right": (xv + 1 - yv) / 2,
        "bottom-left": (1 - xv + yv) / 2, "bottom-right": (xv + yv) / 2,
    }
    grad = grads.get(direction, grads["right"])[:, :, np.newaxis]

    # Light colour (white → golden)
    lr, lg, lb = 1 + warmth * .15, 1 + warmth * .05, 1 - warmth * .2
    light = grad * intensity * 80
    shadow = (1 - grad) * intensity * 20

    for i, c in enumerate([lr, lg, lb]):
        arr[:, :, i] = np.clip(arr[:, :, i] + light[:, :, 0] * c
                                - shadow[:, :, 0], 0, 255)

    result = Image.fromarray(arr.astype(np.uint8))
    bloom = result.filter(ImageFilter.GaussianBlur(15))
    return Image.blend(result, bloom, intensity * 0.12)
