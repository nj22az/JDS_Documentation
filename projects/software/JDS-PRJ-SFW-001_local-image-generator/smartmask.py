"""smartmask.py — Intelligent auto-masking for targeted inpainting.

Detects clothing, skin, and body regions to create precise masks.
Core workflow: subject detection (rembg) + skin detection (HSV) = clothing mask.

Used for: clothing removal/replacement, body editing, targeted regeneration.
"""

import numpy as np
from PIL import Image

from models import (FACE_DET_SIZE, FACE_ELLIPSE_W, FACE_ELLIPSE_H,
                    bg_thread as _bg)


def _skin_mask(img_np):
    """Detect skin pixels using HSV + YCrCb dual-space analysis.
    More robust than single colour space — handles diverse skin tones."""
    import cv2

    # HSV detection (good for light-medium skin)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    hsv_mask = cv2.inRange(hsv, np.array([0, 20, 70]),
                                 np.array([25, 255, 255]))

    # YCrCb detection (good for darker skin tones)
    ycrcb = cv2.cvtColor(img_np, cv2.COLOR_RGB2YCrCb)
    ycrcb_mask = cv2.inRange(ycrcb, np.array([0, 133, 77]),
                                     np.array([255, 173, 127]))

    # Union of both detections
    combined = cv2.bitwise_or(hsv_mask, ycrcb_mask)

    # Clean up noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel, iterations=2)
    combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel, iterations=1)

    return combined


def _subject_mask_sync(image):
    """Get subject mask via rembg (synchronous)."""
    from rembg import remove
    rgba = remove(image)
    alpha = np.array(rgba.split()[-1])
    return (alpha > 128).astype(np.uint8) * 255


def clothing_mask(image, status=None, done=None, error=None):
    """Auto-detect clothing regions: subject minus skin = clothing.
    Returns L-mode mask where white = clothing (area to inpaint)."""
    def _run():
        try:
            import cv2

            if status: status("Detecting subject...")
            img_np = np.array(image.convert("RGB"))
            subj = _subject_mask_sync(image)

            if status: status("Detecting skin regions...")
            skin = _skin_mask(img_np)

            # Clothing = subject AND NOT skin
            clothing = cv2.bitwise_and(subj, cv2.bitwise_not(skin))

            # Expand slightly for clean edges
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            clothing = cv2.dilate(clothing, kernel, iterations=1)

            # Feather edges
            clothing = cv2.GaussianBlur(clothing, (11, 11), 4)

            if status: status("Clothing mask ready.")
            if done: done(Image.fromarray(clothing).convert("L"))

        except ImportError:
            if error: error("Missing packages.\nRun: pip install rembg opencv-python")
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def skin_only_mask(image, status=None, done=None, error=None):
    """Mask of exposed skin regions (white = skin)."""
    def _run():
        try:
            import cv2
            if status: status("Detecting skin...")
            img_np = np.array(image.convert("RGB"))
            subj = _subject_mask_sync(image)
            skin = _skin_mask(img_np)
            # Only skin within subject
            result = cv2.bitwise_and(skin, subj)
            result = cv2.GaussianBlur(result, (11, 11), 4)
            if status: status("Skin mask ready.")
            if done: done(Image.fromarray(result).convert("L"))
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def face_region_mask(image, status=None, done=None, error=None):
    """Mask of face region only (for face-specific inpainting)."""
    def _run():
        try:
            if status: status("Detecting face region...")
            from insightface.app import FaceAnalysis
            import cv2

            app = FaceAnalysis(name="buffalo_l",
                               providers=["CPUExecutionProvider"])
            app.prepare(ctx_id=0, det_size=FACE_DET_SIZE)

            img_np = np.array(image.convert("RGB"))
            faces = app.get(img_np)

            if not faces:
                if error: error("No face detected."); return

            h, w = img_np.shape[:2]
            mask = np.zeros((h, w), dtype=np.uint8)

            for face in faces:
                lm = getattr(face, "landmark_2d_106", None)
                if lm is not None and len(lm) >= 10:
                    hull = cv2.convexHull(np.int32(lm))
                    cv2.fillConvexPoly(mask, hull, 255)
                else:
                    x1, y1, x2, y2 = [int(v) for v in face.bbox]
                    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                    rw = int((x2 - x1) * 0.55)
                    rh = int((y2 - y1) * 0.65)
                    cv2.ellipse(mask, (cx, cy), (rw, rh), 0, 0, 360, 255, -1)

            mask = cv2.GaussianBlur(mask, (21, 21), 8)
            if status: status("Face mask ready.")
            if done: done(Image.fromarray(mask).convert("L"))

        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def body_no_face_mask(image, status=None, done=None, error=None):
    """Subject body minus face (for body editing while preserving face)."""
    def _run():
        try:
            import cv2
            if status: status("Creating body mask (excluding face)...")

            img_np = np.array(image.convert("RGB"))
            subj = _subject_mask_sync(image)

            # Detect face
            face_mask = np.zeros_like(subj)
            try:
                from insightface.app import FaceAnalysis
                app = FaceAnalysis(name="buffalo_l",
                                   providers=["CPUExecutionProvider"])
                app.prepare(ctx_id=0, det_size=(640, 640))
                faces = app.get(img_np)
                for face in faces:
                    x1, y1, x2, y2 = [int(v) for v in face.bbox]
                    pad = int((x2 - x1) * 0.3)
                    x1, y1 = max(0, x1 - pad), max(0, y1 - pad)
                    x2 = min(img_np.shape[1], x2 + pad)
                    y2 = min(img_np.shape[0], y2 + pad)
                    face_mask[y1:y2, x1:x2] = 255
            except Exception:
                pass  # No face detection available, mask full body

            # Body = subject minus face
            result = cv2.bitwise_and(subj, cv2.bitwise_not(face_mask))
            result = cv2.GaussianBlur(result, (11, 11), 4)

            if status: status("Body mask ready (face excluded).")
            if done: done(Image.fromarray(result).convert("L"))

        except Exception as e:
            if error: error(str(e))
    _bg(_run)
