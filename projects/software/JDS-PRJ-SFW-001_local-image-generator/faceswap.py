"""faceswap.py — Neural face swap (ReActor + FaceSwapLab + DiffFace).

Three swap modes (auto-selected):
1. Neural (INSwapper) — ReActor-grade quality, needs inswapper_128.onnx
2. Poisson (affine warp + seamlessClone) — fallback, no extra model
3. Neural + Refine — swap then SD inpaint to fix artifacts (DiffFace concept)

FaceSwapLab features: landmark convex hull mask, face similarity ranking,
face checkpoints (save/reuse faces across sessions).
"""

import numpy as np
from pathlib import Path
from PIL import Image

from models import (CONFIG_DIR, FACE_DET_SIZE, FACE_CROP_PAD, FACE_ELLIPSE_W,
                    FACE_ELLIPSE_H, LANDMARK_BLUR_SIZE, LANDMARK_BLUR_SIGMA,
                    POSE_POOR, POSE_WARN, REFINE_STEPS, REFINE_CFG,
                    REFINE_STRENGTH, bg_thread as _bg)

SWAPPER_DIR = CONFIG_DIR / "swapper"
SWAPPER_FILE = SWAPPER_DIR / "inswapper_128.onnx"
CHECKPOINTS_DIR = CONFIG_DIR / "face_checkpoints"

_analyser = None
_swapper = None


# ---------------------------------------------------------------------------
# Model management
# ---------------------------------------------------------------------------

def swapper_ready():
    """True if inswapper_128.onnx is downloaded and ready."""
    return SWAPPER_FILE.exists()


def download_swapper(status=None, done=None, error=None):
    """Download inswapper_128.onnx from HuggingFace."""
    def _run():
        try:
            SWAPPER_DIR.mkdir(parents=True, exist_ok=True)
            if status: status("Downloading swapper model (~500 MB)...")
            from huggingface_hub import hf_hub_download
            hf_hub_download("ezioruan/inswapper_128.onnx",
                            "inswapper_128.onnx",
                            local_dir=str(SWAPPER_DIR))
            if status: status("Swapper model ready.")
            if done: done()
        except Exception as e:
            if error: error(f"Download failed: {e}\n\n"
                            "Manual: place inswapper_128.onnx in\n"
                            f"{SWAPPER_DIR}")
    _bg(_run)


def _get_analyser():
    global _analyser
    if _analyser is None:
        from insightface.app import FaceAnalysis
        _analyser = FaceAnalysis(name="buffalo_l",
                                  providers=["CPUExecutionProvider"])
        _analyser.prepare(ctx_id=0, det_size=FACE_DET_SIZE)
    return _analyser


def _get_swapper():
    global _swapper
    if _swapper is not None:
        return _swapper
    if not SWAPPER_FILE.exists():
        return None
    import insightface
    _swapper = insightface.model_zoo.get_model(
        str(SWAPPER_FILE), providers=["CPUExecutionProvider"])
    return _swapper


def _largest_face(faces):
    return max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) *
               (f.bbox[3] - f.bbox[1]))


def _face_similarity(a, b):
    """Cosine similarity between two face embeddings (FaceSwapLab)."""
    e1, e2 = a.embedding, b.embedding
    return float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))


def _face_pose_score(face):
    """Score face pose quality 0-1 based on landmark symmetry.
    1.0 = perfect frontal, <0.3 = extreme profile (likely poor swap).
    Uses the 5 keypoints: left_eye, right_eye, nose, left_mouth, right_mouth."""
    kps = face.kps
    if kps is None or len(kps) < 5:
        return 0.5  # unknown, assume OK

    le, re, nose = kps[0], kps[1], kps[2]

    # Eye-to-nose distance ratio (asymmetric = turned head)
    d_left = np.linalg.norm(le - nose)
    d_right = np.linalg.norm(re - nose)
    ratio = min(d_left, d_right) / max(d_left, d_right, 1e-6)

    # Eye distance relative to bbox (small = far away or extreme angle)
    eye_dist = np.linalg.norm(le - re)
    bbox_w = face.bbox[2] - face.bbox[0]
    eye_ratio = eye_dist / max(bbox_w, 1e-6)

    # Combined score: both should be close to 1.0 for good frontal face
    score = (ratio * 0.6 + min(eye_ratio / 0.4, 1.0) * 0.4)
    return float(np.clip(score, 0.0, 1.0))


def _pose_warning(face, label=""):
    """Return warning string if face is at a difficult angle, else None."""
    score = _face_pose_score(face)
    if score < POSE_POOR:
        return f"{label}Face is near-profile ({score:.0%} quality) — results may be poor."
    if score < POSE_WARN:
        return f"{label}Face is at a steep angle ({score:.0%} quality) — results may show artifacts."
    return None


# ---------------------------------------------------------------------------
# Masking — FaceSwapLab: landmark convex hull instead of simple oval
# ---------------------------------------------------------------------------

def _landmark_mask(shape, face):
    """Convex hull from 106-point landmarks, fallback to ellipse from bbox."""
    import cv2
    h, w = shape[:2]
    mask = np.zeros((h, w), dtype=np.uint8)

    lm = getattr(face, "landmark_2d_106", None)
    if lm is not None and len(lm) >= 10:
        hull = cv2.convexHull(np.int32(lm))
        cv2.fillConvexPoly(mask, hull, 255)
    else:
        x1, y1, x2, y2 = [int(v) for v in face.bbox]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        rw = int((x2 - x1) * FACE_ELLIPSE_W)
        rh = int((y2 - y1) * FACE_ELLIPSE_H)
        cv2.ellipse(mask, (cx, cy), (rw, rh), 0, 0, 360, 255, -1)

    mask = cv2.GaussianBlur(mask, LANDMARK_BLUR_SIZE, LANDMARK_BLUR_SIGMA)
    return mask


# ---------------------------------------------------------------------------
# Colour correction — Lab space (better perceptual match than RGB)
# ---------------------------------------------------------------------------

def _colour_correct(result, target, mask):
    import cv2
    mask_bool = mask > 128
    if not np.any(mask_bool):
        return result

    try:
        res_lab = cv2.cvtColor(result, cv2.COLOR_RGB2LAB).astype(np.float32)
        tgt_lab = cv2.cvtColor(target, cv2.COLOR_RGB2LAB).astype(np.float32)

        for ch in range(3):
            sv = res_lab[:, :, ch][mask_bool]
            tv = tgt_lab[:, :, ch][mask_bool]
            if len(sv) == 0:
                continue
            sm, ss = sv.mean(), max(sv.std(), 1)
            tm, ts = tv.mean(), max(tv.std(), 1)
            res_lab[:, :, ch] = (res_lab[:, :, ch] - sm) * (ts / ss) + tm

        corrected = cv2.cvtColor(
            np.clip(res_lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2RGB)
    except Exception:
        corrected = _rgb_correct(result, target, mask_bool)

    mask_f = (mask / 255.0)[:, :, np.newaxis]
    return (corrected * mask_f + target * (1 - mask_f)).astype(np.uint8)


def _rgb_correct(result, target, mask_bool):
    """Fallback per-channel RGB correction."""
    out = result.copy()
    for ch in range(3):
        sv = out[:, :, ch][mask_bool].astype(np.float32)
        tv = target[:, :, ch][mask_bool].astype(np.float32)
        if len(sv) == 0:
            continue
        sm, ss = sv.mean(), max(sv.std(), 1)
        tm, ts = tv.mean(), max(tv.std(), 1)
        out[:, :, ch] = np.clip(
            (out[:, :, ch].astype(np.float32) - sm) * (ts / ss) + tm,
            0, 255).astype(np.uint8)
    return out


# ---------------------------------------------------------------------------
# Affine + Poisson swap (fallback when no INSwapper model)
# ---------------------------------------------------------------------------

def _affine_swap(src_np, tgt_np, src_face, tgt_face):
    import cv2
    M = cv2.getAffineTransform(np.float32(src_face.kps[:3]),
                                np.float32(tgt_face.kps[:3]))
    h, w = tgt_np.shape[:2]
    warped = cv2.warpAffine(src_np, M, (w, h),
                             borderMode=cv2.BORDER_REFLECT_101)
    mask = _landmark_mask(tgt_np.shape, tgt_face)

    try:
        x1, y1, x2, y2 = [int(v) for v in tgt_face.bbox]
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        mask_bin = (mask > 128).astype(np.uint8) * 255
        result = cv2.seamlessClone(warped, tgt_np, mask_bin,
                                    center, cv2.NORMAL_CLONE)
    except Exception:
        mask_3 = np.stack([mask / 255.0] * 3, axis=-1)
        result = (warped * mask_3 + tgt_np * (1 - mask_3)).astype(np.uint8)

    return _colour_correct(result, tgt_np, mask)


# ---------------------------------------------------------------------------
# Diffusion refinement — DiffFace concept (SD inpaint over swapped area)
# ---------------------------------------------------------------------------

def _diffusion_refine(result_img, mask_np, status=None, done=None, error=None):
    """Low-strength inpaint over swapped face to fix artifacts."""
    try:
        import engine
        if not engine._pipe:
            if done:
                done(result_img)
            return

        mask_img = Image.fromarray(mask_np).convert("L")
        engine.inpaint(
            prompt="highly detailed realistic face, sharp features, natural skin",
            image=result_img, mask=mask_img,
            neg="blurry, deformed, artifact, seam, boundary",
            steps=REFINE_STEPS, cfg=REFINE_CFG, strength=REFINE_STRENGTH,
            seed=-1,
            status=status,
            done=lambda img, s: (done(img) if done else None),
            error=error)
    except Exception:
        if done:
            done(result_img)


# ---------------------------------------------------------------------------
# Public API — swap / multi_swap / bidi_swap
# ---------------------------------------------------------------------------

def swap(source, target, refine=False, status=None, done=None, error=None):
    """Swap face from source onto target. Auto-selects best method."""
    def _run():
        try:
            import cv2

            if status: status("Detecting faces...")
            src_np = np.array(source.convert("RGB"))
            tgt_np = np.array(target.convert("RGB"))

            app = _get_analyser()
            src_faces = app.get(src_np)
            tgt_faces = app.get(tgt_np)

            if not src_faces:
                if error: error("No face found in source image.")
                return
            if not tgt_faces:
                if error: error("No face found in target image.")
                return

            src_face = _largest_face(src_faces)
            tgt_face = _largest_face(tgt_faces)

            # Pose quality check — warn but proceed
            for w in [_pose_warning(src_face, "Source: "),
                      _pose_warning(tgt_face, "Target: ")]:
                if w and status:
                    status(w)

            swapper = _get_swapper()
            if swapper is not None:
                if status: status("Neural swap (ReActor)...")
                result = swapper.get(tgt_np.copy(), tgt_face, src_face,
                                     paste_back=True)
                mask = _landmark_mask(result.shape, tgt_face)
                result = _colour_correct(result, tgt_np, mask)
            else:
                if status: status("Poisson swap (no swapper model)...")
                result = _affine_swap(src_np, tgt_np, src_face, tgt_face)

            if refine:
                if status: status("Refining with diffusion...")
                mask = _landmark_mask(result.shape, tgt_face)
                _diffusion_refine(Image.fromarray(result), mask,
                                  status, done, error)
                return

            if status: status("Face swap complete.")
            if done: done(Image.fromarray(result))

        except ImportError:
            if error:
                error("Missing packages.\n\n"
                      "Run: pip install insightface opencv-python onnxruntime")
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def multi_swap(source, target, refine=False,
               status=None, done=None, error=None):
    """Swap ALL faces in target with source. Similarity-ranked (FaceSwapLab)."""
    def _run():
        try:
            import cv2

            if status: status("Detecting all faces...")
            src_np = np.array(source.convert("RGB"))
            tgt_np = np.array(target.convert("RGB"))

            app = _get_analyser()
            src_faces = app.get(src_np)
            tgt_faces = app.get(tgt_np)

            if not src_faces:
                if error: error("No face in source."); return
            if not tgt_faces:
                if error: error("No faces in target."); return

            src_face = _largest_face(src_faces)
            result = tgt_np.copy()

            # Sort by similarity — best matches first (FaceSwapLab)
            tgt_faces.sort(
                key=lambda f: _face_similarity(src_face, f), reverse=True)

            swapper = _get_swapper()
            all_masks = []

            for i, tgt_face in enumerate(tgt_faces):
                if status: status(f"Swapping face {i+1}/{len(tgt_faces)}...")

                if swapper is not None:
                    result = swapper.get(result, tgt_face, src_face,
                                         paste_back=True)
                    mask = _landmark_mask(result.shape, tgt_face)
                    result = _colour_correct(result, tgt_np, mask)
                else:
                    result = _affine_swap(src_np, result, src_face, tgt_face)
                    mask = _landmark_mask(result.shape, tgt_face)

                all_masks.append(mask)

            if refine and all_masks:
                if status: status("Refining with diffusion...")
                combined = np.zeros_like(all_masks[0])
                for m in all_masks:
                    combined = np.maximum(combined, m)
                _diffusion_refine(Image.fromarray(result), combined,
                                  status, done, error)
                return

            if status: status(f"Swapped {len(tgt_faces)} face(s).")
            if done: done(Image.fromarray(result))

        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def bidi_swap(photo_a, photo_b, refine=False,
              status=None, done=None, error=None):
    """Bidirectional swap: A's face on B's body AND B's face on A's body.
    Returns both results via done(result_a, result_b)."""
    def _run():
        try:
            import cv2

            if status: status("Detecting faces in both photos...")
            np_a = np.array(photo_a.convert("RGB"))
            np_b = np.array(photo_b.convert("RGB"))

            app = _get_analyser()
            faces_a = app.get(np_a)
            faces_b = app.get(np_b)

            if not faces_a:
                if error: error("No face found in Photo A."); return
            if not faces_b:
                if error: error("No face found in Photo B."); return

            face_a = _largest_face(faces_a)
            face_b = _largest_face(faces_b)

            for w in [_pose_warning(face_a, "Photo A: "),
                      _pose_warning(face_b, "Photo B: ")]:
                if w and status:
                    status(w)

            swapper = _get_swapper()

            # Result 1: A's face on B's body
            if status: status("Putting face A on body B...")
            if swapper is not None:
                res_b = swapper.get(np_b.copy(), face_b, face_a, paste_back=True)
                mask_b = _landmark_mask(res_b.shape, face_b)
                res_b = _colour_correct(res_b, np_b, mask_b)
            else:
                res_b = _affine_swap(np_a, np_b, face_a, face_b)

            # Result 2: B's face on A's body
            if status: status("Putting face B on body A...")
            if swapper is not None:
                res_a = swapper.get(np_a.copy(), face_a, face_b, paste_back=True)
                mask_a = _landmark_mask(res_a.shape, face_a)
                res_a = _colour_correct(res_a, np_a, mask_a)
            else:
                res_a = _affine_swap(np_b, np_a, face_b, face_a)

            img_a = Image.fromarray(res_a)
            img_b = Image.fromarray(res_b)

            if refine:
                if status: status("Refining result 1...")
                # Refine both — chain the callbacks
                mask_b_ref = _landmark_mask(res_b.shape, face_b)
                mask_a_ref = _landmark_mask(res_a.shape, face_a)

                def _refine_second(refined_b):
                    _diffusion_refine(
                        img_a, mask_a_ref, status,
                        done=lambda refined_a: (
                            done(refined_a, refined_b) if done else None),
                        error=error)

                _diffusion_refine(img_b, mask_b_ref, status,
                                  done=_refine_second, error=error)
                return

            if status: status("Bidirectional swap complete.")
            if done: done(img_a, img_b)

        except ImportError:
            if error:
                error("Missing packages.\n\n"
                      "Run: pip install insightface opencv-python onnxruntime")
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


# ---------------------------------------------------------------------------
# Face checkpoints — FaceSwapLab: save/reuse faces across sessions
# ---------------------------------------------------------------------------

def save_checkpoint(name, image, status=None, done=None, error=None):
    """Save face as reusable checkpoint (embedding + crop + reference)."""
    def _run():
        try:
            if status: status(f"Saving checkpoint '{name}'...")
            img_np = np.array(image.convert("RGB"))
            faces = _get_analyser().get(img_np)

            if not faces:
                if error: error("No face detected."); return

            face = _largest_face(faces)
            d = CHECKPOINTS_DIR / name
            d.mkdir(parents=True, exist_ok=True)

            np.save(str(d / "embedding.npy"), face.embedding)

            x1, y1, x2, y2 = [int(v) for v in face.bbox]
            pad = int((x2 - x1) * FACE_CROP_PAD)
            crop = image.crop((max(0, x1 - pad), max(0, y1 - pad),
                               min(image.width, x2 + pad),
                               min(image.height, y2 + pad)))
            crop.save(str(d / "face.png"))

            ref = image.copy()
            ref.thumbnail((512, 512), Image.LANCZOS)
            ref.save(str(d / "reference.png"))

            if status: status(f"Checkpoint '{name}' saved.")
            if done: done(name)
        except Exception as e:
            if error: error(str(e))
    _bg(_run)


def list_checkpoints():
    if not CHECKPOINTS_DIR.exists():
        return []
    return sorted([p.name for p in CHECKPOINTS_DIR.iterdir()
                   if p.is_dir() and (p / "face.png").exists()])


def load_checkpoint(name):
    """Returns (face_image, reference_image)."""
    d = CHECKPOINTS_DIR / name
    face = Image.open(str(d / "face.png")) if (d / "face.png").exists() else None
    ref = Image.open(str(d / "reference.png")) if (d / "reference.png").exists() else None
    return face, ref


def delete_checkpoint(name):
    import shutil
    d = CHECKPOINTS_DIR / name
    if d.exists():
        shutil.rmtree(d)
