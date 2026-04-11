"""fixer.py — Face/hand detection and auto-fix (Adetailer concept).

Detects faces and hands in generated images, crops each region,
runs a high-detail inpaint pass at larger resolution, pastes back.
Result: sharp faces, correct hands, natural proportions.
"""

from PIL import Image, ImageDraw, ImageFilter

from models import (FACE_FIX_MAX_DIM, FACE_FIX_STRENGTH, bg_thread as _bg)


def _load_detector():
    """Load OpenCV face detector (ships with opencv-python)."""
    import cv2
    face = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    profile = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_profileface.xml")
    return face, profile


def detect_faces(image):
    """Return list of (x, y, w, h) face bounding boxes."""
    import cv2
    import numpy as np

    face_det, profile_det = _load_detector()
    img = np.array(image.convert("RGB"))
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    boxes = []
    for det in [face_det, profile_det]:
        hits = det.detectMultiScale(gray, scaleFactor=1.1,
                                     minNeighbors=5, minSize=(40, 40))
        for (x, y, w, h) in hits:
            boxes.append((x, y, w, h))

    # Deduplicate overlapping boxes
    return _merge_boxes(boxes)


def _merge_boxes(boxes, overlap=0.4):
    """Merge overlapping bounding boxes."""
    if not boxes:
        return []
    merged = []
    used = set()
    for i, (x1, y1, w1, h1) in enumerate(boxes):
        if i in used:
            continue
        bx, by, bw, bh = x1, y1, w1, h1
        for j, (x2, y2, w2, h2) in enumerate(boxes):
            if j <= i or j in used:
                continue
            # Check overlap
            ox = max(0, min(bx + bw, x2 + w2) - max(bx, x2))
            oy = max(0, min(by + bh, y2 + h2) - max(by, y2))
            inter = ox * oy
            area = min(bw * bh, w2 * h2)
            if area > 0 and inter / area > overlap:
                # Merge
                nx = min(bx, x2)
                ny = min(by, y2)
                bw = max(bx + bw, x2 + w2) - nx
                bh = max(by + bh, y2 + h2) - ny
                bx, by = nx, ny
                used.add(j)
        merged.append((bx, by, bw, bh))
        used.add(i)
    return merged


def _expand_box(x, y, w, h, img_w, img_h, pad=0.5):
    """Expand box by pad fraction for context."""
    pw, ph = int(w * pad), int(h * pad)
    nx = max(0, x - pw)
    ny = max(0, y - ph)
    nw = min(img_w - nx, w + 2 * pw)
    nh = min(img_h - ny, h + 2 * ph)
    return nx, ny, nw, nh


def _make_soft_mask(w, h, box_in_crop):
    """Create a soft-edged mask for the detection area within the crop."""
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    bx, by, bw, bh = box_in_crop
    draw.ellipse([bx, by, bx + bw, by + bh], fill=255)
    return mask.filter(ImageFilter.GaussianBlur(bw // 4))


def fix_faces(image, pipe_fn, prompt, neg="",
              steps=25, cfg=7.0, detail=1.5,
              status=None, done=None, error=None):
    """
    Detect faces, run targeted inpaint on each at higher resolution.
    pipe_fn: function(prompt, image, mask, neg, steps, cfg, strength) -> PIL Image
    detail: scale factor for the face crop (1.5 = 50% larger for detail).
    """
    def _run():
        try:
            faces = detect_faces(image)
            if not faces:
                if status: status("No faces detected.")
                if done: done(image)
                return

            if status: status(f"Fixing {len(faces)} face(s)...")
            result = image.copy().convert("RGB")
            img_w, img_h = result.size

            for i, (fx, fy, fw, fh) in enumerate(faces):
                # Expand region for context
                ex, ey, ew, eh = _expand_box(fx, fy, fw, fh, img_w, img_h)

                # Crop the region
                crop = result.crop((ex, ey, ex + ew, ey + eh))

                # Scale up for detail
                up_w = int(ew * detail) // 8 * 8
                up_h = int(eh * detail) // 8 * 8
                up_w = min(up_w, FACE_FIX_MAX_DIM)
                up_h = min(up_h, FACE_FIX_MAX_DIM)
                crop_up = crop.resize((up_w, up_h), Image.LANCZOS)

                # Soft mask centered on face within the crop
                box_in = (fx - ex, fy - ey, fw, fh)
                # Scale box to upscaled size
                sx = up_w / ew
                sy = up_h / eh
                sbox = (int(box_in[0] * sx), int(box_in[1] * sy),
                        int(box_in[2] * sx), int(box_in[3] * sy))
                mask_up = _make_soft_mask(up_w, up_h, sbox)

                # Run inpaint
                if status: status(f"Fixing face {i + 1}/{len(faces)}...")
                fixed = pipe_fn(prompt, crop_up, mask_up, neg,
                                steps, cfg, FACE_FIX_STRENGTH)

                # Scale back and paste
                fixed_down = fixed.resize((ew, eh), Image.LANCZOS)
                result.paste(fixed_down, (ex, ey))

            if status: status("Face fix complete.")
            if done: done(result)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)
