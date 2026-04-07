"""gui.py — Main window, sidebar, all modes, model manager."""

import os
import sys
import traceback
import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import customtkinter as ctk

import engine
import lighting
from models import (APP_NAME, APP_VERSION, MODELS, NEG_PRESETS, C,
                    LIGHT_DIRS, OUTPUT_DIR, load_config, save_config)
from painter import MaskPainter

MODES = ["txt2img", "img2img", "inpaint", "edit"]


def show_error(title, msg):
    """Show a popup error dialog."""
    messagebox.showerror(title, msg)


def show_info(title, msg):
    """Show a popup info dialog."""
    messagebox.showinfo(title, msg)


# -----------------------------------------------------------------------
# Model Manager (popup)
# -----------------------------------------------------------------------
class ModelManager(ctk.CTkToplevel):
    def __init__(self, master, cfg, on_select):
        super().__init__(master)
        self.cfg, self.on_select = cfg, on_select
        self.title("Model Manager")
        self.geometry("600x520")
        self.resizable(False, False)
        self.configure(fg_color=C["bg"])
        self.grab_set()

        ctk.CTkLabel(self, text="Model Manager",
                     font=("SF Pro Display", 20, "bold"),
                     text_color=C["text"]).pack(padx=20, pady=(16, 2), anchor="w")
        ctk.CTkLabel(self, text="All models run 100% local. No filters.",
                     font=("SF Pro Text", 12),
                     text_color=C["muted"]).pack(padx=20, pady=(0, 8), anchor="w")

        scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg"])
        scroll.pack(fill="both", expand=True, padx=12, pady=(0, 4))
        for m in MODELS:
            self._card(scroll, m)

        # Custom ID
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=(4, 4))
        self._custom = ctk.CTkEntry(row, corner_radius=10, fg_color=C["fill"],
                                     border_width=0, font=("SF Pro Text", 12),
                                     placeholder_text="Custom HuggingFace ID")
        self._custom.pack(side="left", fill="x", expand=True, padx=(0, 8))
        ctk.CTkButton(row, text="Download", width=90, corner_radius=10,
                      height=30, font=("SF Pro Text", 12, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._dl_custom).pack(side="right")

        self._status = ctk.CTkLabel(self, text="", font=("SF Pro Text", 11),
                                     text_color=C["muted"])
        self._status.pack(padx=20, pady=(0, 12), anchor="w")

    def _card(self, parent, m):
        f = ctk.CTkFrame(parent, corner_radius=12, fg_color=C["surface"])
        f.pack(fill="x", pady=3)
        inner = ctk.CTkFrame(f, fg_color="transparent")
        inner.pack(fill="x", padx=14, pady=10)

        top = ctk.CTkFrame(inner, fg_color="transparent")
        top.pack(fill="x")
        name = m["name"] + ("  (Recommended)" if m.get("default") else "")
        ctk.CTkLabel(top, text=name, font=("SF Pro Text", 13, "bold"),
                     text_color=C["text"]).pack(side="left")
        ctk.CTkLabel(top, text=m["size"], font=("SF Pro Text", 11),
                     text_color=C["muted"]).pack(side="right")
        ctk.CTkLabel(inner, text=m["desc"], font=("SF Pro Text", 11),
                     text_color=C["muted"], wraplength=480,
                     justify="left").pack(anchor="w", pady=(2, 6))

        btns = ctk.CTkFrame(inner, fg_color="transparent")
        btns.pack(fill="x")
        ctk.CTkButton(btns, text="Download & Load", width=130,
                      corner_radius=10, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=lambda: self._dl_load(m)).pack(side="left", padx=(0, 6))
        ctk.CTkButton(btns, text="Load", width=70,
                      corner_radius=10, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=lambda: self._select(m["id"])).pack(side="left")

    def _msg(self, t):
        self.after(0, lambda: self._status.configure(text=t))

    def _dl_load(self, m):
        self._msg(f"Downloading {m['name']}...")
        def ok(mid, _):
            dl = self.cfg.get("downloaded", [])
            if mid not in dl: dl.append(mid)
            self.cfg["downloaded"] = dl
            save_config(self.cfg)
            self._msg(f"Loading {m['name']}...")
            self.after(0, lambda: self._select(mid))
        engine.download(m["id"], status=self._msg, done=ok, error=self._msg)

    def _select(self, mid):
        self.cfg["model_id"] = mid
        save_config(self.cfg)
        self.on_select(mid)
        self.destroy()

    def _dl_custom(self):
        mid = self._custom.get().strip()
        if mid:
            self._dl_load({"id": mid, "name": mid})


# -----------------------------------------------------------------------
# Main Application
# -----------------------------------------------------------------------
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.cfg = load_config()
        self.current_image = None
        self.input_image = None
        self.last_seed = None
        self._busy = False

        self.title(APP_NAME)
        self.geometry("1200x820")
        self.minsize(1000, 700)
        self.configure(fg_color=C["bg"])
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.protocol("WM_DELETE_WINDOW", self._quit)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._sidebar()
        self._main()

        if not self.cfg.get("model_id"):
            self.after(400, self._models)

    # -------------------------------------------------------------------
    # Sidebar
    # -------------------------------------------------------------------
    def _sidebar(self):
        sb = ctk.CTkFrame(self, width=330, corner_radius=0, fg_color=C["surface"])
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        px = 18

        # Header
        ctk.CTkLabel(sb, text=APP_NAME, font=("SF Pro Display", 20, "bold"),
                     text_color=C["text"]).pack(padx=px, pady=(16, 0), anchor="w")
        ctk.CTkLabel(sb, text=f"v{APP_VERSION} — Local & Unrestricted",
                     font=("SF Pro Text", 10),
                     text_color=C["muted"]).pack(padx=px, pady=(0, 6), anchor="w")
        ctk.CTkFrame(sb, height=1, fg_color=C["sep"]).pack(fill="x", padx=px, pady=(0, 8))

        # Scrollable controls
        sc = ctk.CTkScrollableFrame(sb, fg_color=C["surface"])
        sc.pack(fill="both", expand=True)

        # Mode
        self.mode = ctk.StringVar(value="txt2img")
        ctk.CTkSegmentedButton(
            sc, values=MODES, variable=self.mode,
            command=self._mode_changed,
            font=("SF Pro Text", 12)).pack(fill="x", padx=px, pady=(2, 8))

        # Prompt
        self._label(sc, "Prompt")
        self.prompt = ctk.CTkTextbox(sc, height=70, corner_radius=10,
                                      font=("SF Pro Text", 12),
                                      fg_color=C["fill"], text_color=C["text"],
                                      border_width=0)
        self.prompt.pack(fill="x", padx=px, pady=(0, 6))

        # Negative prompt
        nr = ctk.CTkFrame(sc, fg_color="transparent")
        nr.pack(fill="x", padx=px)
        self._label(nr, "Negative Prompt", pack=False).pack(side="left")
        self.neg_preset = ctk.CTkOptionMenu(
            nr, values=list(NEG_PRESETS.keys()),
            font=("SF Pro Text", 10), width=120, height=22,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"],
            command=self._apply_neg_preset)
        self.neg_preset.set("Preset...")
        self.neg_preset.pack(side="right")
        self.neg = ctk.CTkTextbox(sc, height=40, corner_radius=10,
                                   font=("SF Pro Text", 12),
                                   fg_color=C["fill"], text_color=C["text"],
                                   border_width=0)
        self.neg.pack(fill="x", padx=px, pady=(4, 6))

        # --- Mode-specific panels (packed/hidden dynamically) ---
        # img2img panel
        self.p_img2img = ctk.CTkFrame(sc, fg_color="transparent")
        ctk.CTkButton(self.p_img2img, text="Load Photo",
                      corner_radius=10, height=32,
                      font=("SF Pro Text", 12),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._open_photo).pack(fill="x", pady=(0, 4))
        self.str_lbl = ctk.CTkLabel(self.p_img2img, text="Strength: 0.75",
                                     font=("SF Pro Text", 11), text_color=C["muted"])
        self.str_lbl.pack(anchor="w")
        self.str_sl = ctk.CTkSlider(self.p_img2img, from_=0.1, to=1.0,
                                     number_of_steps=18,
                                     command=lambda v: self.str_lbl.configure(
                                         text=f"Strength: {v:.2f}"))
        self.str_sl.set(0.75)
        self.str_sl.pack(fill="x", pady=(0, 6))

        # Inpaint panel
        self.p_inpaint = ctk.CTkFrame(sc, fg_color="transparent")
        ctk.CTkButton(self.p_inpaint, text="Load Photo to Edit",
                      corner_radius=10, height=32,
                      font=("SF Pro Text", 12),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._open_for_paint).pack(fill="x", pady=(0, 4))
        brush_row = ctk.CTkFrame(self.p_inpaint, fg_color="transparent")
        brush_row.pack(fill="x")
        self.brush_lbl = ctk.CTkLabel(brush_row, text="Brush: 30px",
                                       font=("SF Pro Text", 11), text_color=C["muted"])
        self.brush_lbl.pack(side="left")
        ctk.CTkButton(brush_row, text="Clear", width=50, corner_radius=8,
                      height=22, font=("SF Pro Text", 10),
                      fg_color=C["fill"], text_color=C["red"],
                      hover_color=C["sep"],
                      command=self._clear_mask).pack(side="right")
        ctk.CTkButton(brush_row, text="Invert", width=50, corner_radius=8,
                      height=22, font=("SF Pro Text", 10),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._invert_mask).pack(side="right", padx=(0, 4))
        self.brush_sl = ctk.CTkSlider(self.p_inpaint, from_=5, to=80,
                                       number_of_steps=15,
                                       command=self._brush_changed)
        self.brush_sl.set(30)
        self.brush_sl.pack(fill="x", pady=(2, 4))
        self.inp_str_lbl = ctk.CTkLabel(self.p_inpaint, text="Strength: 0.85",
                                         font=("SF Pro Text", 11), text_color=C["muted"])
        self.inp_str_lbl.pack(anchor="w")
        self.inp_str = ctk.CTkSlider(self.p_inpaint, from_=0.3, to=1.0,
                                      number_of_steps=14,
                                      command=lambda v: self.inp_str_lbl.configure(
                                          text=f"Strength: {v:.2f}"))
        self.inp_str.set(0.85)
        self.inp_str.pack(fill="x", pady=(0, 6))

        # Edit panel (background + lighting)
        self.p_edit = ctk.CTkFrame(sc, fg_color="transparent")
        ctk.CTkButton(self.p_edit, text="Load Photo",
                      corner_radius=10, height=32,
                      font=("SF Pro Text", 12),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._open_photo).pack(fill="x", pady=(0, 4))

        self._label(self.p_edit, "Background")
        bg_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        bg_row.pack(fill="x", pady=(0, 6))
        ctk.CTkButton(bg_row, text="Remove BG", width=90,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._remove_bg).pack(side="left", padx=(0, 4))
        ctk.CTkButton(bg_row, text="Replace BG", width=90,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._replace_bg).pack(side="left", padx=(0, 4))
        ctk.CTkButton(bg_row, text="Get Mask", width=80,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._get_mask).pack(side="left")

        self._label(self.p_edit, "Lighting")
        self.light_dir = ctk.CTkOptionMenu(
            self.p_edit, values=LIGHT_DIRS, font=("SF Pro Text", 11),
            fg_color=C["fill"], text_color=C["text"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.light_dir.set("right")
        self.light_dir.pack(fill="x", pady=(0, 4))

        li_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        li_row.pack(fill="x")
        self.li_lbl = ctk.CTkLabel(li_row, text="Intensity: 0.5",
                                    font=("SF Pro Text", 11), text_color=C["muted"])
        self.li_lbl.pack(side="left")
        self.warm_lbl = ctk.CTkLabel(li_row, text="Warmth: 0.3",
                                      font=("SF Pro Text", 11), text_color=C["muted"])
        self.warm_lbl.pack(side="right")

        self.li_sl = ctk.CTkSlider(self.p_edit, from_=0, to=1.0,
                                    number_of_steps=20,
                                    command=lambda v: self.li_lbl.configure(
                                        text=f"Intensity: {v:.1f}"))
        self.li_sl.set(0.5)
        self.li_sl.pack(fill="x")
        self.warm_sl = ctk.CTkSlider(self.p_edit, from_=0, to=1.0,
                                      number_of_steps=20,
                                      command=lambda v: self.warm_lbl.configure(
                                          text=f"Warmth: {v:.1f}"))
        self.warm_sl.set(0.3)
        self.warm_sl.pack(fill="x", pady=(0, 2))

        ctk.CTkButton(self.p_edit, text="Apply Lighting",
                      corner_radius=10, height=32,
                      font=("SF Pro Text", 12, "bold"),
                      fg_color=C["orange"], hover_color="#CC7700",
                      command=self._apply_light).pack(fill="x", pady=(4, 6))

        # --- Settings ---
        ctk.CTkFrame(sc, height=1, fg_color=C["sep"]).pack(fill="x", padx=px, pady=(4, 6))
        self._label(sc, "Settings")

        grid = ctk.CTkFrame(sc, fg_color="transparent")
        grid.pack(fill="x", padx=px, pady=(0, 4))
        grid.grid_columnconfigure((0, 1), weight=1)

        self.e_w = self._setting(grid, 0, "Width", str(self.cfg["width"]))
        self.e_h = self._setting(grid, 1, "Height", str(self.cfg["height"]))
        self.e_steps = self._setting(grid, 2, "Steps", str(self.cfg["steps"]))
        self.e_cfg = self._setting(grid, 3, "CFG Scale", str(self.cfg["guidance"]))
        self.e_seed = self._setting(grid, 4, "Seed", "-1")

        # Size presets
        sr = ctk.CTkFrame(sc, fg_color="transparent")
        sr.pack(fill="x", padx=px, pady=(0, 6))
        for lbl, ww, hh in [("512x512", 512, 512), ("512x768", 512, 768),
                             ("768x512", 768, 512), ("768x768", 768, 768)]:
            ctk.CTkButton(sr, text=lbl, width=65, corner_radius=8, height=24,
                          font=("SF Pro Text", 10),
                          fg_color=C["fill"], text_color=C["text"],
                          hover_color=C["sep"],
                          command=lambda w=ww, h=hh: self._set_size(w, h)
                          ).pack(side="left", padx=(0, 3))

        # Model
        ctk.CTkFrame(sc, height=1, fg_color=C["sep"]).pack(fill="x", padx=px, pady=(4, 6))
        mr = ctk.CTkFrame(sc, fg_color="transparent")
        mr.pack(fill="x", padx=px)
        self._label(mr, "Model", pack=False).pack(side="left")
        ctk.CTkButton(mr, text="Model Manager", width=100, corner_radius=8,
                      height=24, font=("SF Pro Text", 10),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._models).pack(side="right")

        self.model_lbl = ctk.CTkLabel(
            sc, text=self.cfg.get("model_id") or "No model",
            font=("SF Pro Text", 10), text_color=C["muted"], wraplength=260)
        self.model_lbl.pack(padx=px, pady=(2, 2), anchor="w")

        ctk.CTkButton(sc, text="Load Model", corner_radius=10, height=32,
                      font=("SF Pro Text", 12, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._load_model).pack(fill="x", padx=px, pady=(2, 8))

        # --- Bottom buttons (outside scroll) ---
        self.gen_btn = ctk.CTkButton(
            sb, text="Generate", corner_radius=12, height=46,
            font=("SF Pro Display", 16, "bold"),
            fg_color=C["accent"], hover_color=C["hover"],
            command=self._generate)
        self.gen_btn.pack(fill="x", padx=px, pady=(0, 6), side="bottom")

        self.status = ctk.CTkLabel(
            sb, text="Open Model Manager to start",
            font=("SF Pro Text", 10), text_color=C["muted"], wraplength=260)
        self.status.pack(padx=px, pady=(0, 6), side="bottom", anchor="w")

    # --- Sidebar helpers ---
    def _label(self, parent, text, pack=True):
        lbl = ctk.CTkLabel(parent, text=text, font=("SF Pro Text", 12, "bold"),
                           text_color=C["text"])
        if pack:
            lbl.pack(padx=18, pady=(0, 2), anchor="w")
        return lbl

    def _setting(self, grid, row, label, default):
        ctk.CTkLabel(grid, text=label, font=("SF Pro Text", 11),
                     text_color=C["muted"]).grid(row=row, column=0, sticky="w", pady=1)
        e = ctk.CTkEntry(grid, width=75, corner_radius=8,
                         font=("SF Pro Text", 11),
                         fg_color=C["fill"], border_width=0)
        e.insert(0, default)
        e.grid(row=row, column=1, sticky="e", pady=1)
        return e

    def _set_size(self, w, h):
        for e, v in [(self.e_w, w), (self.e_h, h)]:
            e.delete(0, "end"); e.insert(0, str(v))

    # -------------------------------------------------------------------
    # Main area
    # -------------------------------------------------------------------
    def _main(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color=C["bg"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Image card
        self.card = ctk.CTkFrame(main, corner_radius=16, fg_color=C["surface"])
        self.card.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        self.card.grid_rowconfigure(0, weight=1)
        self.card.grid_columnconfigure(0, weight=1)

        # Preview label (used for non-paint modes)
        self.preview = ctk.CTkLabel(
            self.card, text="Load a model, then generate.",
            font=("SF Pro Text", 14), text_color=C["muted"])
        self.preview.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        # Mask painter (used for inpaint mode, hidden by default)
        self.painter = MaskPainter(self.card, 512, 512)

        # Toolbar
        bar = ctk.CTkFrame(main, height=44, corner_radius=0, fg_color=C["bg"])
        bar.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 10))

        ctk.CTkButton(bar, text="Save", width=80, corner_radius=10, height=32,
                      font=("SF Pro Text", 12), fg_color=C["accent"],
                      hover_color=C["hover"],
                      command=self._save).pack(side="left")
        ctk.CTkButton(bar, text="Copy Seed", width=90, corner_radius=10,
                      height=32, font=("SF Pro Text", 12),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._copy_seed).pack(side="left", padx=(6, 0))

        # Upscale buttons
        ctk.CTkButton(bar, text="Upscale 2x", width=90, corner_radius=10,
                      height=32, font=("SF Pro Text", 12),
                      fg_color=C["green"], hover_color="#2AA847",
                      command=lambda: self._upscale(2)).pack(side="left", padx=(6, 0))
        ctk.CTkButton(bar, text="Hires Fix", width=80, corner_radius=10,
                      height=32, font=("SF Pro Text", 12),
                      fg_color=C["orange"], hover_color="#CC7700",
                      command=self._hires_fix).pack(side="left", padx=(6, 0))

        self.seed_lbl = ctk.CTkLabel(bar, text="", font=("SF Pro Text", 11),
                                      text_color=C["muted"])
        self.seed_lbl.pack(side="right")

    # -------------------------------------------------------------------
    # Mode switching
    # -------------------------------------------------------------------
    def _mode_changed(self, mode):
        for p in [self.p_img2img, self.p_inpaint, self.p_edit]:
            p.pack_forget()

        # Show/hide painter
        if mode == "inpaint":
            self.p_inpaint.pack(fill="x", padx=18, pady=(0, 6),
                                after=self.neg)
            self.preview.grid_forget()
            self.painter.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
        else:
            self.painter.grid_forget()
            self.preview.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)
            if mode == "img2img":
                self.p_img2img.pack(fill="x", padx=18, pady=(0, 6),
                                    after=self.neg)
            elif mode == "edit":
                self.p_edit.pack(fill="x", padx=18, pady=(0, 6),
                                 after=self.neg)

    # -------------------------------------------------------------------
    # Actions
    # -------------------------------------------------------------------
    def _msg(self, t):
        self.after(0, lambda: self.status.configure(text=t))

    def _apply_neg_preset(self, name):
        text = NEG_PRESETS.get(name, "")
        self.neg.delete("1.0", "end")
        self.neg.insert("1.0", text)

    def _models(self):
        ModelManager(self, self.cfg, self._on_model)

    def _on_model(self, mid):
        self.model_lbl.configure(text=mid)
        self.cfg["model_id"] = mid
        save_config(self.cfg)
        self._load_model()

    def _load_model(self):
        mid = self.cfg.get("model_id", "").strip()
        if not mid:
            show_error("No Model", "No model selected.\n\nOpen Model Manager to download one.")
            return
        self.gen_btn.configure(state="disabled")
        self._msg(f"Loading {mid}...")

        def on_err(e):
            self._msg("Model load failed.")
            self.after(0, lambda: self.gen_btn.configure(state="normal"))
            self.after(0, lambda: show_error("Model Load Error",
                f"Could not load model:\n{mid}\n\n{e}\n\n"
                "Try downloading it first via Model Manager."))

        engine.load(mid, status=self._msg,
                    done=lambda: self.after(0, lambda: self.gen_btn.configure(state="normal")),
                    error=on_err)

    def _open_photo(self):
        p = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if p:
            try:
                self.input_image = Image.open(p)
                self._show(self.input_image)
                self._msg(f"Loaded: {os.path.basename(p)}")
            except Exception as e:
                show_error("Image Error", f"Could not open image:\n{p}\n\n{e}")

    def _open_for_paint(self):
        p = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if p:
            try:
                img = Image.open(p)
                img.thumbnail((768, 768), Image.LANCZOS)
                self.input_image = img
                self.painter.set_image(img)
                self._msg(f"Paint over areas to edit: {os.path.basename(p)}")
            except Exception as e:
                show_error("Image Error", f"Could not open image:\n{p}\n\n{e}")

    def _brush_changed(self, v):
        v = int(v)
        self.brush_lbl.configure(text=f"Brush: {v}px")
        self.painter.brush_size = v

    def _clear_mask(self):
        self.painter.clear_mask()

    def _invert_mask(self):
        self.painter.invert_mask()

    def _get_mask(self):
        if not self.input_image:
            self._msg("Load a photo first."); return
        engine.subject_mask(self.input_image, status=self._msg,
                            done=lambda m: self.after(0, lambda: self._show(m)),
                            error=lambda e: self.after(0, lambda: show_error("Error", str(e))))

    def _remove_bg(self):
        if not self.input_image:
            self._msg("Load a photo first."); return
        engine.remove_bg(self.input_image, status=self._msg,
                         done=lambda img: self.after(0, lambda: self._finish(img)),
                         error=lambda e: self.after(0, lambda: show_error("Error", str(e))))

    def _replace_bg(self):
        if not self.input_image:
            self._msg("Load a photo first."); return
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            self._msg("Enter a background description in the prompt."); return
        neg = self.neg.get("1.0", "end").strip()
        s, g, seed = self._params()
        engine.replace_bg(self.input_image, prompt, neg=neg,
                          steps=s, cfg=g, seed=seed,
                          status=self._msg,
                          done=lambda img, sd: self.after(0, lambda: self._finish(img, sd)),
                          error=lambda e: self.after(0, lambda: show_error("Error", str(e))))

    def _apply_light(self):
        img = self.current_image or self.input_image
        if not img:
            self._msg("No image to light."); return
        result = lighting.apply(img, self.light_dir.get(),
                                self.li_sl.get(), self.warm_sl.get())
        self._finish(result)
        self._msg("Lighting applied.")

    def _upscale(self, scale=2):
        if not self.current_image:
            show_error("No Image", "Generate or load an image first.")
            return
        self._msg(f"Upscaling {scale}x with Real-ESRGAN...")
        engine.upscale(
            self.current_image, scale=scale,
            status=self._msg,
            done=lambda img: self.after(0, lambda: self._finish(img)),
            error=lambda e: self.after(0, lambda: show_error("Upscale Error",
                f"Upscaling failed:\n\n{e}\n\n"
                "Install the upscaler:\n  pip install realesrgan basicsr")))

    def _hires_fix(self):
        if not self.current_image:
            show_error("No Image", "Generate an image first, then upscale it.")
            return
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            self._msg("Enter the original prompt for detail enhancement.")
            return
        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, seed = self._params()
        self._msg("Running hires fix (upscale + detail)...")
        engine.hires_fix(
            self.current_image, prompt, neg=neg, scale=2, strength=0.35,
            steps=steps, cfg=cfg, seed=seed,
            status=self._msg,
            done=lambda img, s: self.after(0, lambda: self._finish(img, s)),
            error=lambda e: self.after(0, lambda: show_error("Hires Fix Error",
                f"Hires fix failed:\n\n{e}")))

    def _params(self):
        """Read steps, cfg, seed from entries."""
        try:
            return (int(self.e_steps.get()), float(self.e_cfg.get()),
                    int(self.e_seed.get()))
        except ValueError:
            return 30, 7.0, -1

    def _generate(self):
        if self._busy: return
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            self._msg("Enter a prompt."); return

        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, seed = self._params()
        try:
            w = int(self.e_w.get()) // 8 * 8
            h = int(self.e_h.get()) // 8 * 8
        except ValueError:
            w, h = 512, 512

        self._busy = True
        self.gen_btn.configure(state="disabled", text="Working...")

        def ok(img, s):
            self._busy = False
            self.after(0, lambda: self._finish(img, s))
            self.after(0, lambda: self.gen_btn.configure(state="normal", text="Generate"))

        def fail(e):
            self._busy = False
            self._msg("Generation failed.")
            self.after(0, lambda: self.gen_btn.configure(state="normal", text="Generate"))
            self.after(0, lambda: show_error("Generation Error",
                f"Image generation failed:\n\n{e}\n\n"
                "Check that a model is loaded and your settings are valid."))

        mode = self.mode.get()
        if mode == "txt2img":
            engine.txt2img(prompt, neg, w, h, steps, cfg, seed,
                           status=self._msg, done=ok, error=fail)
        elif mode == "img2img":
            if not self.input_image:
                self._msg("Load a photo first."); fail("No photo"); return
            engine.img2img(prompt, self.input_image, self.str_sl.get(),
                           neg, steps, cfg, seed,
                           status=self._msg, done=ok, error=fail)
        elif mode == "inpaint":
            if not self.input_image:
                self._msg("Load a photo first."); fail("No photo"); return
            mask = self.painter.get_mask()
            engine.inpaint(prompt, self.input_image, mask, neg,
                           steps, cfg, seed, self.inp_str.get(),
                           status=self._msg, done=ok, error=fail)
        elif mode == "edit":
            # In edit mode, Generate = img2img on the current/input image
            img = self.current_image or self.input_image
            if not img:
                self._msg("Load a photo first."); fail("No photo"); return
            engine.img2img(prompt, img, 0.5, neg, steps, cfg, seed,
                           status=self._msg, done=ok, error=fail)

    def _finish(self, img, seed=None):
        self.current_image = img
        if seed is not None:
            self.last_seed = seed
            self.seed_lbl.configure(text=f"Seed: {seed}")
        self._show(img)
        self._msg("Done.")

    def _show(self, img):
        cw = max(self.card.winfo_width() - 32, 400)
        ch = max(self.card.winfo_height() - 32, 400)
        disp = img.copy()
        disp.thumbnail((cw, ch), Image.LANCZOS)
        self._tk = ImageTk.PhotoImage(disp)
        self.preview.configure(image=self._tk, text="")

    def _save(self):
        if not self.current_image:
            self._msg("Nothing to save."); return
        out = self.cfg.get("output_dir", str(OUTPUT_DIR))
        Path(out).mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        p = filedialog.asksaveasfilename(
            initialdir=out, initialfile=f"jds_{ts}.png",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if p:
            self.current_image.save(p)
            self._msg(f"Saved: {os.path.basename(p)}")

    def _copy_seed(self):
        if self.last_seed is not None:
            self.clipboard_clear()
            self.clipboard_append(str(self.last_seed))
            self._msg(f"Seed {self.last_seed} copied.")

    def _quit(self):
        engine.unload()
        self.destroy()
        sys.exit(0)
