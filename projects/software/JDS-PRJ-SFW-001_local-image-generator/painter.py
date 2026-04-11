"""painter.py — Mask painting canvas widget for inpainting."""

import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
from models import C


class MaskPainter(tk.Canvas):
    """
    Transparent overlay canvas for painting inpaint masks.
    White strokes on black = areas to regenerate.
    """

    def __init__(self, master, width=512, height=512, **kw):
        super().__init__(master, width=width, height=height,
                         bg=C["surface"], highlightthickness=0, **kw)
        self._w = width
        self._h = height
        self.brush_size = 30
        self._photo = None
        self._base_image = None

        # Internal mask (L mode: black=keep, white=edit)
        self._mask = Image.new("L", (width, height), 0)
        self._draw = ImageDraw.Draw(self._mask)

        # Drawing state
        self._drawing = False
        self.bind("<Button-1>", self._start)
        self.bind("<B1-Motion>", self._paint)
        self.bind("<ButtonRelease-1>", self._stop)

    def set_image(self, pil_image):
        """Set the base image to paint over."""
        self._base_image = pil_image.copy().convert("RGBA")
        self._w, self._h = self._base_image.size
        self.config(width=self._w, height=self._h)
        self._mask = Image.new("L", (self._w, self._h), 0)
        self._draw = ImageDraw.Draw(self._mask)
        self._refresh()

    def get_mask(self):
        """Return the mask as a PIL Image (L mode)."""
        return self._mask.copy()

    def get_display_size(self):
        return self._w, self._h

    def clear_mask(self):
        self._mask = Image.new("L", (self._w, self._h), 0)
        self._draw = ImageDraw.Draw(self._mask)
        self._refresh()

    def invert_mask(self):
        from PIL import ImageOps
        self._mask = ImageOps.invert(self._mask)
        self._draw = ImageDraw.Draw(self._mask)
        self._refresh()

    def set_mask(self, mask_image):
        """Load an external mask (e.g. from subject detection)."""
        self._mask = mask_image.convert("L").resize((self._w, self._h))
        self._draw = ImageDraw.Draw(self._mask)
        self._refresh()

    def _start(self, e):
        self._drawing = True
        self._dot(e.x, e.y)

    def _paint(self, e):
        if self._drawing:
            self._dot(e.x, e.y)

    def _stop(self, _):
        self._drawing = False

    def _dot(self, x, y):
        r = self.brush_size // 2
        self._draw.ellipse([x - r, y - r, x + r, y + r], fill=255)
        self._refresh()

    def _refresh(self):
        if self._base_image is None:
            return
        # Composite: base image + semi-transparent red mask overlay
        overlay = Image.new("RGBA", (self._w, self._h), (0, 0, 0, 0))
        mask_rgba = Image.merge("RGBA", (
            self._mask.point(lambda p: 255 if p > 0 else 0),  # R
            Image.new("L", (self._w, self._h), 0),             # G
            Image.new("L", (self._w, self._h), 0),             # B
            self._mask.point(lambda p: 100 if p > 0 else 0),   # A
        ))
        composite = Image.alpha_composite(self._base_image, mask_rgba)

        # Fit to canvas display
        self._photo = ImageTk.PhotoImage(composite)
        self.delete("all")
        self.create_image(0, 0, anchor="nw", image=self._photo)
