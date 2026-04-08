"""gui.py — Main window, sidebar, all modes, model manager."""

import os
import sys
import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

import customtkinter as ctk

import engine
import lighting
import history
import prompts
import fixer
import consistency
import faceswap
import cloudgen
import smartmask
import qwen
from models import (APP_NAME, APP_VERSION, MODELS, NEG_PRESETS, C,
                    LIGHT_DIRS, INPAINT_PRESETS, SIZE_PRESETS,
                    WINDOW_SIZE, WINDOW_MIN, SIDEBAR_WIDTH,
                    OUTPUT_DIR, QUALITY_ANCHORS, LIGHTING_PRESETS,
                    LENS_PRESETS, ENHANCED_NEGATIVE, PROMPT_TEMPLATES,
                    AVATAR_ETHNICITY, AVATAR_AGE, AVATAR_HAIR_STYLE,
                    AVATAR_HAIR_COLOR, AVATAR_EYE_COLOR, AVATAR_EYE_SHAPE,
                    AVATAR_FACE_SHAPE, AVATAR_SKIN_TONE, AVATAR_LIPS,
                    AVATAR_MAKEUP, AVATAR_BREAST_SIZE, AVATAR_BUTT_SIZE,
                    AVATAR_BODY_TYPE, AVATAR_POSE, AVATAR_EXPRESSION,
                    AVATAR_OUTFIT, AVATAR_SETTING,
                    load_config, save_config)
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
# History Gallery
# -----------------------------------------------------------------------
class HistoryWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master_app = master
        self.title("Generation History")
        self.geometry("700x500")
        self.configure(fg_color=C["bg"])

        ctk.CTkLabel(self, text="History",
                     font=("SF Pro Display", 20, "bold"),
                     text_color=C["text"]).pack(padx=20, pady=(16, 4), anchor="w")
        ctk.CTkLabel(self, text="All generated images are saved automatically.",
                     font=("SF Pro Text", 12),
                     text_color=C["muted"]).pack(padx=20, pady=(0, 8), anchor="w")

        self._scroll = ctk.CTkScrollableFrame(self, fg_color=C["bg"])
        self._scroll.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        self._thumbs = []  # keep references alive
        entries = history.list_all(limit=50)
        if not entries:
            ctk.CTkLabel(self._scroll, text="No images yet.",
                         font=("SF Pro Text", 13),
                         text_color=C["muted"]).pack(pady=20)
            return

        for img_path, meta in entries:
            self._entry(img_path, meta)

    def _entry(self, path, meta):
        row = ctk.CTkFrame(self._scroll, corner_radius=10, fg_color=C["surface"])
        row.pack(fill="x", pady=3)
        inner = ctk.CTkFrame(row, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=8)

        # Thumbnail
        thumb = history.load_thumb(path, (80, 80))
        if thumb:
            tk_img = ImageTk.PhotoImage(thumb)
            self._thumbs.append(tk_img)
            ctk.CTkLabel(inner, image=tk_img, text="").pack(side="left", padx=(0, 10))

        # Info
        info = ctk.CTkFrame(inner, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True)
        prompt = meta.get("prompt", "")[:80]
        ctk.CTkLabel(info, text=prompt, font=("SF Pro Text", 11),
                     text_color=C["text"], wraplength=380,
                     justify="left").pack(anchor="w")
        details = (f"Seed: {meta.get('seed', '?')} | "
                   f"{meta.get('mode', '')} | "
                   f"{meta.get('timestamp', '')}")
        ctk.CTkLabel(info, text=details, font=("SF Pro Text", 10),
                     text_color=C["muted"]).pack(anchor="w")

        # Load button
        ctk.CTkButton(inner, text="Load", width=60, corner_radius=8,
                      height=28, font=("SF Pro Text", 11),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=lambda p=path, m=meta: self._load(p, m)
                      ).pack(side="right")

    def _load(self, path, meta):
        try:
            img = Image.open(path)
            self.master_app.current_image = img
            self.master_app._show(img)
            self.master_app._msg(f"Loaded from history: seed {meta.get('seed', '?')}")
            # Restore prompt
            self.master_app.prompt.delete("1.0", "end")
            self.master_app.prompt.insert("1.0", meta.get("prompt", ""))
            # Restore seed
            self.master_app.e_seed.delete(0, "end")
            self.master_app.e_seed.insert(0, str(meta.get("seed", -1)))
            self.destroy()
        except Exception as e:
            show_error("Load Error", str(e))


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
        self.swap_face_src = None
        self._busy = False

        self.title(APP_NAME)
        self.geometry(WINDOW_SIZE)
        self.minsize(*WINDOW_MIN)
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

        # Prompt template dropdown
        tpl_row = ctk.CTkFrame(sc, fg_color="transparent")
        tpl_row.pack(fill="x", padx=px, pady=(0, 2))
        self._label(tpl_row, "Prompt", pack=False).pack(side="left")
        self.tpl_menu = ctk.CTkOptionMenu(
            tpl_row, values=list(PROMPT_TEMPLATES.keys()),
            font=("SF Pro Text", 10), width=180, height=22,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"],
            command=self._apply_template)
        self.tpl_menu.set("Template...")
        self.tpl_menu.pack(side="right")

        self.prompt = ctk.CTkTextbox(sc, height=70, corner_radius=10,
                                      font=("SF Pro Text", 12),
                                      fg_color=C["fill"], text_color=C["text"],
                                      border_width=0)
        self.prompt.pack(fill="x", padx=px, pady=(0, 2))

        # Prompt Enhance row
        enh_row = ctk.CTkFrame(sc, fg_color="transparent")
        enh_row.pack(fill="x", padx=px, pady=(0, 2))
        self.enhance_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(enh_row, text="Enhance",
                        variable=self.enhance_var,
                        font=("SF Pro Text", 11),
                        checkbox_height=18, checkbox_width=18,
                        command=self._toggle_enhance).pack(side="left")
        self.quality_menu = ctk.CTkOptionMenu(
            enh_row, values=list(QUALITY_ANCHORS.keys()),
            font=("SF Pro Text", 10), width=110, height=22,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.quality_menu.set("Asian Realism")
        self.lighting_menu = ctk.CTkOptionMenu(
            enh_row, values=list(LIGHTING_PRESETS.keys()),
            font=("SF Pro Text", 10), width=100, height=22,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.lighting_menu.set("Studio soft")
        self.lens_menu = ctk.CTkOptionMenu(
            enh_row, values=list(LENS_PRESETS.keys()),
            font=("SF Pro Text", 10), width=110, height=22,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.lens_menu.set("85mm portrait")
        # Shown by default since Enhance is on
        self._enh_menus = [self.quality_menu, self.lighting_menu, self.lens_menu]
        for menu in self._enh_menus:
            menu.pack(side="left", padx=(4, 0))

        # --- Avatar Creator (collapsible) ---
        av_toggle = ctk.CTkFrame(sc, fg_color="transparent")
        av_toggle.pack(fill="x", padx=px, pady=(2, 0))
        self.avatar_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(av_toggle, text="Avatar Creator",
                        variable=self.avatar_var,
                        font=("SF Pro Text", 11, "bold"),
                        checkbox_height=18, checkbox_width=18,
                        command=self._toggle_avatar).pack(side="left")
        ctk.CTkLabel(av_toggle, text="(builds prompt from selections)",
                     font=("SF Pro Text", 9), text_color=C["muted"]
                     ).pack(side="left", padx=(6, 0))

        self.avatar_frame = ctk.CTkFrame(sc, fg_color=C["surface"],
                                          corner_radius=8)
        # Not packed yet — shown when checkbox is on

        # Helper to create avatar dropdown rows
        av_dd_font = ("SF Pro Text", 10)
        av_lbl_font = ("SF Pro Text", 9)

        def _av_row(parent, label, values, default_idx=0):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", padx=6, pady=(2, 0))
            ctk.CTkLabel(row, text=label, font=av_lbl_font,
                         text_color=C["muted"], width=70, anchor="w"
                         ).pack(side="left")
            menu = ctk.CTkOptionMenu(
                row, values=values, font=av_dd_font,
                width=180, height=20, corner_radius=4,
                fg_color=C["fill"], text_color=C["text"],
                button_color=C["sep"], button_hover_color=C["muted"])
            menu.set(values[default_idx])
            menu.pack(side="left", fill="x", expand=True)
            return menu

        af = self.avatar_frame
        ctk.CTkLabel(af, text="Character Builder",
                     font=("SF Pro Text", 11, "bold"),
                     text_color=C["text"]).pack(padx=6, pady=(6, 2), anchor="w")

        self.av_ethnicity = _av_row(af, "Ethnicity", AVATAR_ETHNICITY)
        self.av_age = _av_row(af, "Age", AVATAR_AGE, 1)
        self.av_face = _av_row(af, "Face", AVATAR_FACE_SHAPE)
        self.av_skin = _av_row(af, "Skin", AVATAR_SKIN_TONE, 2)
        self.av_eye_shape = _av_row(af, "Eye shape", AVATAR_EYE_SHAPE)
        self.av_eye_color = _av_row(af, "Eye colour", AVATAR_EYE_COLOR)
        self.av_hair_style = _av_row(af, "Hair style", AVATAR_HAIR_STYLE)
        self.av_hair_color = _av_row(af, "Hair colour", AVATAR_HAIR_COLOR)
        self.av_makeup = _av_row(af, "Makeup", AVATAR_MAKEUP, 1)
        self.av_lips = _av_row(af, "Lips", AVATAR_LIPS)
        self.av_expression = _av_row(af, "Expression", AVATAR_EXPRESSION)
        self.av_body = _av_row(af, "Body type", AVATAR_BODY_TYPE, 2)
        self.av_breast = _av_row(af, "Breast", AVATAR_BREAST_SIZE, 2)
        self.av_butt = _av_row(af, "Butt", AVATAR_BUTT_SIZE, 2)
        self.av_pose = _av_row(af, "Pose", AVATAR_POSE)
        self.av_outfit = _av_row(af, "Outfit", AVATAR_OUTFIT)
        self.av_setting = _av_row(af, "Setting", AVATAR_SETTING)

        # Height / Weight in avatar frame
        hw_row = ctk.CTkFrame(af, fg_color="transparent")
        hw_row.pack(fill="x", padx=6, pady=(2, 0))
        ctk.CTkLabel(hw_row, text="Height cm", font=av_lbl_font,
                     text_color=C["muted"]).pack(side="left")
        self.av_height = ctk.CTkEntry(hw_row, width=40, height=20,
                                       corner_radius=4, font=av_dd_font,
                                       fg_color=C["fill"], border_width=0,
                                       placeholder_text="160")
        self.av_height.pack(side="left", padx=(2, 8))
        ctk.CTkLabel(hw_row, text="Weight kg", font=av_lbl_font,
                     text_color=C["muted"]).pack(side="left")
        self.av_weight = ctk.CTkEntry(hw_row, width=40, height=20,
                                       corner_radius=4, font=av_dd_font,
                                       fg_color=C["fill"], border_width=0,
                                       placeholder_text="50")
        self.av_weight.pack(side="left", padx=(2, 0))

        # Build Prompt button
        ctk.CTkButton(af, text="Build Prompt from Avatar",
                      corner_radius=6, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._build_avatar_prompt
                      ).pack(fill="x", padx=6, pady=(6, 6))

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

        # Smart masking (auto-detect clothing, skin, body)
        self._label(self.p_edit, "Smart Mask")
        sm_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        sm_row.pack(fill="x", pady=(0, 4))
        ctk.CTkButton(sm_row, text="Clothing", width=75,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color="#FF2D55", hover_color="#CC1A3D",
                      command=self._mask_clothing).pack(side="left", padx=(0, 4))
        ctk.CTkButton(sm_row, text="Skin", width=55,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._mask_skin).pack(side="left", padx=(0, 4))
        ctk.CTkButton(sm_row, text="Body (no face)", width=100,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._mask_body).pack(side="left", padx=(0, 4))
        ctk.CTkButton(sm_row, text="Face", width=50,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._mask_face).pack(side="left")

        # Inpaint workflow presets
        self._label(self.p_edit, "Inpaint Preset")
        preset_names = list(INPAINT_PRESETS.keys())
        self.inpaint_preset = ctk.CTkOptionMenu(
            self.p_edit, values=preset_names,
            font=("SF Pro Text", 11),
            fg_color=C["fill"], text_color=C["text"],
            button_color=C["sep"], button_hover_color=C["muted"],
            command=self._apply_inpaint_preset)
        self.inpaint_preset.set("Custom (manual)")
        self.inpaint_preset.pack(fill="x", pady=(0, 4))
        ctk.CTkButton(self.p_edit, text="Auto Mask + Inpaint",
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color="#FF2D55", hover_color="#CC1A3D",
                      command=self._auto_inpaint).pack(fill="x", pady=(0, 6))

        # Qwen AI Edit — direct neural image editing
        self._label(self.p_edit, "Qwen AI Edit")
        qwen_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        qwen_row.pack(fill="x", pady=(0, 2))
        self.qwen_instruction = ctk.CTkEntry(
            qwen_row, placeholder_text="e.g. remove her clothes, change to bikini...",
            font=("SF Pro Text", 11), height=28, corner_radius=8,
            fg_color=C["fill"], text_color=C["text"], border_width=0)
        self.qwen_instruction.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.qwen_mode_menu = ctk.CTkOptionMenu(
            qwen_row, values=["cloud", "local", "local-pruned"],
            font=("SF Pro Text", 10), width=90, height=24,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.qwen_mode_menu.set("cloud")
        self.qwen_mode_menu.pack(side="right")
        ctk.CTkButton(self.p_edit, text="AI Edit (Qwen)",
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color=C["indigo"], hover_color=C["indigo_h"],
                      command=self._qwen_edit).pack(fill="x", pady=(2, 2))
        self.qwen_status = ctk.CTkLabel(
            self.p_edit,
            text="Type what to change. 4 steps, no neg prompt needed. Cloud = free.",
            font=("SF Pro Text", 9), text_color=C["muted"])
        self.qwen_status.pack(anchor="w", pady=(0, 6))

        # ControlNet (pose/structure preservation)
        self._label(self.p_edit, "ControlNet")
        cn_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        cn_row.pack(fill="x", pady=(0, 6))
        self.cn_type = ctk.CTkOptionMenu(
            cn_row, values=["openpose", "canny", "depth"],
            width=100, font=("SF Pro Text", 11),
            fg_color=C["fill"], text_color=C["text"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.cn_type.set("openpose")
        self.cn_type.pack(side="left", padx=(0, 4))
        ctk.CTkButton(cn_row, text="Generate with Pose", width=140,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color="#5856D6", hover_color="#4240A8",
                      command=self._controlnet_gen).pack(side="left")

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

        # Identity (character consistency)
        self._label(self.p_edit, "Character Identity")
        id_row1 = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        id_row1.pack(fill="x", pady=(0, 4))
        self.id_name = ctk.CTkEntry(
            id_row1, corner_radius=8, fg_color=C["fill"], border_width=0,
            font=("SF Pro Text", 11), placeholder_text="Name (e.g. Mai)")
        self.id_name.pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(id_row1, text="Save", width=55, corner_radius=8,
                      height=28, font=("SF Pro Text", 11, "bold"),
                      fg_color="#AF52DE", hover_color="#8B3FBF",
                      command=self._save_identity).pack(side="right")

        id_row2 = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        id_row2.pack(fill="x", pady=(0, 2))
        self.id_select = ctk.CTkOptionMenu(
            id_row2, values=["(none)"] + consistency.list_identities(),
            font=("SF Pro Text", 11), width=150,
            fg_color=C["fill"], text_color=C["text"],
            button_color=C["sep"], button_hover_color=C["muted"],
            command=self._on_identity_selected)
        self.id_select.set("(none)")
        self.id_select.pack(side="left", fill="x", expand=True, padx=(0, 4))
        ctk.CTkButton(id_row2, text="Generate", width=75, corner_radius=8,
                      height=28, font=("SF Pro Text", 11, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=self._generate_with_identity).pack(side="right")

        self.id_strength_lbl = ctk.CTkLabel(
            self.p_edit, text="Identity strength: 0.6 (face stays, scene changes)",
            font=("SF Pro Text", 10), text_color=C["muted"])
        self.id_strength_lbl.pack(anchor="w")
        self.id_strength = ctk.CTkSlider(
            self.p_edit, from_=0.3, to=1.0, number_of_steps=14,
            command=lambda v: self.id_strength_lbl.configure(
                text=f"Identity strength: {v:.1f} "
                     f"({'face locked' if v > 0.7 else 'face stays, scene changes'})"))
        self.id_strength.set(0.6)
        self.id_strength.pack(fill="x", pady=(0, 6))

        # Face swap (ReActor + FaceSwapLab + DiffFace)
        self._label(self.p_edit, "Face Swap")

        # Model status + download
        model_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        model_row.pack(fill="x", pady=(0, 4))
        self.swap_model_lbl = ctk.CTkLabel(
            model_row, text="Neural swap: checking...",
            font=("SF Pro Text", 10), text_color=C["muted"])
        self.swap_model_lbl.pack(side="left")
        self.swap_dl_btn = ctk.CTkButton(
            model_row, text="Get Swapper Model", width=130,
            corner_radius=8, height=24, font=("SF Pro Text", 10),
            fg_color=C["orange"], hover_color="#CC7700",
            command=self._download_swapper)
        self._refresh_swapper_status()

        # Source face row
        swap_row1 = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        swap_row1.pack(fill="x", pady=(0, 4))
        ctk.CTkButton(swap_row1, text="Load Face", width=80,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._load_swap_face).pack(side="left", padx=(0, 4))

        # Checkpoint dropdown
        self.ckpt_var = ctk.StringVar(value="")
        self.ckpt_menu = ctk.CTkOptionMenu(
            swap_row1, values=[""] + faceswap.list_checkpoints(),
            variable=self.ckpt_var, width=100, height=28,
            corner_radius=8, font=("SF Pro Text", 10),
            fg_color=C["fill"], text_color=C["text"],
            command=self._load_checkpoint_face)
        self.ckpt_menu.pack(side="left", padx=(0, 4))
        ctk.CTkButton(swap_row1, text="Save", width=50,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 10),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._save_swap_checkpoint).pack(side="left")

        # Action row
        swap_row2 = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        swap_row2.pack(fill="x", pady=(0, 4))
        ctk.CTkButton(swap_row2, text="Swap", width=80,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color="#AF52DE", hover_color="#8B3FBF",
                      command=self._do_swap).pack(side="left", padx=(0, 4))
        ctk.CTkButton(swap_row2, text="Swap All", width=70,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._do_multi_swap).pack(side="left", padx=(0, 4))
        ctk.CTkButton(swap_row2, text="Switch", width=65,
                      corner_radius=8, height=28,
                      font=("SF Pro Text", 11),
                      fg_color="#5856D6", hover_color="#4240A8",
                      command=self._do_bidi_swap).pack(side="left", padx=(0, 4))
        self.refine_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(swap_row2, text="Refine (SD)",
                        variable=self.refine_var,
                        font=("SF Pro Text", 10),
                        width=20, height=20, corner_radius=4,
                        fg_color=C["accent"], hover_color=C["hover"]
                        ).pack(side="left", padx=(4, 0))

        self.swap_status = ctk.CTkLabel(
            self.p_edit, text="Load a face or pick a checkpoint, then swap.",
            font=("SF Pro Text", 10), text_color=C["muted"])
        self.swap_status.pack(anchor="w", pady=(0, 6))

        # --- Cloud Video ---
        self._label(self.p_edit, "Cloud Video")
        vid_row = ctk.CTkFrame(self.p_edit, fg_color="transparent")
        vid_row.pack(fill="x", pady=(0, 2))
        self.video_backend_menu = ctk.CTkOptionMenu(
            vid_row, values=["huggingface", "replicate"],
            font=("SF Pro Text", 10), width=110, height=24,
            fg_color=C["fill"], text_color=C["accent"],
            button_color=C["sep"], button_hover_color=C["muted"])
        self.video_backend_menu.set("huggingface")
        self.video_backend_menu.pack(side="left")
        ctk.CTkButton(vid_row, text="Generate Video",
                      corner_radius=8, height=26,
                      font=("SF Pro Text", 11, "bold"),
                      fg_color=C["purple"], hover_color=C["purple_h"],
                      command=self._generate_video).pack(side="left", padx=(6, 0))
        self.video_status = ctk.CTkLabel(
            self.p_edit, text="Generate a short video from current image (free via HuggingFace).",
            font=("SF Pro Text", 10), text_color=C["muted"])
        self.video_status.pack(anchor="w", pady=(0, 6))

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

        # Cloud generation (optional)
        ctk.CTkFrame(sc, height=1, fg_color=C["sep"]).pack(fill="x", padx=px, pady=(0, 6))
        cr = ctk.CTkFrame(sc, fg_color="transparent")
        cr.pack(fill="x", padx=px)
        self.cloud_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(cr, text="Use Cloud",
                        variable=self.cloud_var, font=("SF Pro Text", 11, "bold"),
                        width=20, height=20, corner_radius=4,
                        fg_color="#5856D6", hover_color="#4240A8",
                        command=self._toggle_cloud
                        ).pack(side="left")
        ctk.CTkButton(cr, text="Cloud Settings", width=100, corner_radius=8,
                      height=24, font=("SF Pro Text", 10),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._cloud_settings).pack(side="right")

        cloud_cfg = cloudgen.load_settings()
        self.cloud_backend = ctk.StringVar(value=cloud_cfg["backend"])
        self.cloud_model = ctk.StringVar(value=cloud_cfg["cloud_model"])

        cb_row = ctk.CTkFrame(sc, fg_color="transparent")
        cb_row.pack(fill="x", padx=px, pady=(2, 0))
        ctk.CTkLabel(cb_row, text="Backend:", font=("SF Pro Text", 10),
                     text_color=C["muted"]).pack(side="left")
        self.backend_menu = ctk.CTkOptionMenu(
            cb_row, values=["huggingface", "prodia", "horde", "replicate"],
            variable=self.cloud_backend, width=110, height=24,
            corner_radius=8, font=("SF Pro Text", 10),
            fg_color=C["fill"], text_color=C["text"],
            command=self._on_backend_change)
        self.backend_menu.pack(side="left", padx=(4, 0))

        models = cloudgen.CLOUD_MODELS.get(cloud_cfg["backend"], [])
        model_names = [m["name"] for m in models]
        self.cloud_model_menu = ctk.CTkOptionMenu(
            sc, values=model_names or ["SDXL 1.0"],
            width=260, height=24, corner_radius=8,
            font=("SF Pro Text", 10),
            fg_color=C["fill"], text_color=C["text"],
            command=self._on_cloud_model_change)
        self.cloud_model_menu.pack(fill="x", padx=px, pady=(2, 6))

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
        ctk.CTkButton(bar, text="Fix Faces", width=80, corner_radius=10,
                      height=32, font=("SF Pro Text", 12),
                      fg_color="#AF52DE", hover_color="#8B3FBF",
                      command=self._fix_faces).pack(side="left", padx=(6, 0))
        ctk.CTkButton(bar, text="History", width=70, corner_radius=10,
                      height=32, font=("SF Pro Text", 12),
                      fg_color=C["fill"], text_color=C["text"],
                      hover_color=C["sep"],
                      command=self._show_history).pack(side="left", padx=(6, 0))

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

    def _toggle_avatar(self):
        """Show/hide avatar creator panel."""
        if self.avatar_var.get():
            self.avatar_frame.pack(fill="x", padx=18, pady=(2, 4),
                                    before=self.neg)
        else:
            self.avatar_frame.pack_forget()

    def _build_avatar_prompt(self):
        """Assemble a complete prompt from all avatar dropdown selections."""
        parts = []

        # Core identity
        ethnicity = self.av_ethnicity.get()
        age = self.av_age.get()
        parts.append(f"beautiful {ethnicity} woman, {age}")

        # Face
        parts.append(self.av_face.get())
        parts.append(self.av_skin.get())
        parts.append(self.av_eye_shape.get())
        parts.append(f"{self.av_eye_color.get()} eyes")

        # Hair
        parts.append(f"{self.av_hair_color.get()} {self.av_hair_style.get()}")

        # Makeup & lips
        parts.append(self.av_makeup.get())
        parts.append(self.av_lips.get())

        # Expression
        parts.append(self.av_expression.get())

        # Body
        parts.append(self.av_body.get())
        parts.append(self.av_breast.get())
        parts.append(self.av_butt.get())

        # Height/weight
        try:
            h_cm = int(self.av_height.get())
            w_kg = int(self.av_weight.get())
            bmi = w_kg / ((h_cm / 100) ** 2)
            if h_cm < 155:
                parts.append("petite short stature")
            elif h_cm < 163:
                parts.append("petite")
            elif h_cm >= 170:
                parts.append("tall")
            parts.append(f"{h_cm}cm {w_kg}kg proportions")
        except (ValueError, TypeError, ZeroDivisionError):
            pass

        # Pose
        parts.append(self.av_pose.get())

        # Outfit (skip if "None")
        outfit = self.av_outfit.get()
        if outfit and not outfit.startswith("None"):
            parts.append(outfit)

        # Setting (skip if "None")
        setting = self.av_setting.get()
        if setting and not setting.startswith("None"):
            parts.append(setting)

        # Quality footer
        parts.append("photorealistic, detailed skin texture, professional photography")

        # Fill prompt box
        prompt = ", ".join(parts)
        self.prompt.delete("1.0", "end")
        self.prompt.insert("1.0", prompt)

        # Auto-set quality anchor and neg preset
        self.quality_menu.set("Asian Realism")
        self.enhance_var.set(True)
        self._toggle_enhance()
        self._apply_neg_preset("Asian realism")
        self.neg_preset.set("Asian realism")

        self._msg("Avatar prompt built. Hit Generate!")

    def _apply_template(self, name):
        """Fill prompt box with selected template."""
        text = PROMPT_TEMPLATES.get(name, "")
        if not text:
            return
        self.prompt.delete("1.0", "end")
        self.prompt.insert("1.0", text)
        # Auto-select matching quality anchor and neg preset
        if "gravure" in name.lower():
            self.quality_menu.set("Gravure")
            self._apply_neg_preset("Gravure (glamour)")
            self.neg_preset.set("Gravure (glamour)")
        elif "k-beauty" in name.lower() or "korean" in name.lower():
            self.quality_menu.set("K-Beauty")
            self._apply_neg_preset("Asian realism")
            self.neg_preset.set("Asian realism")
        elif "asian" in name.lower():
            self.quality_menu.set("Asian Realism")
            self._apply_neg_preset("Asian realism")
            self.neg_preset.set("Asian realism")

    def _toggle_enhance(self):
        """Show/hide quality, lighting, lens dropdowns."""
        if self.enhance_var.get():
            for menu in self._enh_menus:
                menu.pack(side="left", padx=(4, 0))
        else:
            for menu in self._enh_menus:
                menu.pack_forget()

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

    # --- Cloud generation ---

    def _toggle_cloud(self):
        on = self.cloud_var.get()
        lbl = "Cloud: ready" if on else "Local mode"
        self._msg(lbl)

    def _on_backend_change(self, backend):
        models = cloudgen.CLOUD_MODELS.get(backend, [])
        names = [m["name"] for m in models]
        self.cloud_model_menu.configure(values=names or ["—"])
        if names:
            self.cloud_model_menu.set(names[0])
            self._on_cloud_model_change(names[0])
        cfg = cloudgen.load_settings()
        cfg["backend"] = backend
        cloudgen.save_settings(cfg)

    def _on_cloud_model_change(self, name):
        backend = self.cloud_backend.get()
        models = cloudgen.CLOUD_MODELS.get(backend, [])
        for m in models:
            if m["name"] == name:
                cfg = cloudgen.load_settings()
                cfg["cloud_model"] = m["id"]
                cfg["backend"] = backend
                cloudgen.save_settings(cfg)
                return

    def _cloud_settings(self):
        """Popup to set API keys for cloud backends."""
        dlg = ctk.CTkToplevel(self)
        dlg.title("Cloud Settings")
        dlg.geometry("420x360")
        dlg.configure(fg_color=C["bg"])
        dlg.transient(self)
        dlg.grab_set()

        cfg = cloudgen.load_settings()
        pad = {"padx": 16, "pady": (4, 0), "anchor": "w"}

        ctk.CTkLabel(dlg, text="Cloud API Settings",
                     font=("SF Pro Display", 16, "bold"),
                     text_color=C["text"]).pack(padx=16, pady=(16, 8), anchor="w")

        ctk.CTkLabel(dlg, text="HuggingFace Token (optional, higher rate limits):",
                     font=("SF Pro Text", 11), text_color=C["muted"]).pack(**pad)
        hf_entry = ctk.CTkEntry(dlg, width=380, placeholder_text="hf_...")
        hf_entry.pack(padx=16, pady=(2, 6))
        if cfg.get("hf_token"):
            hf_entry.insert(0, cfg["hf_token"])

        ctk.CTkLabel(dlg, text="Prodia API Key (free at prodia.com):",
                     font=("SF Pro Text", 11), text_color=C["muted"]).pack(**pad)
        pr_entry = ctk.CTkEntry(dlg, width=380, placeholder_text="xxxxxxxx-xxxx-xxxx...")
        pr_entry.pack(padx=16, pady=(2, 6))
        if cfg.get("prodia_key"):
            pr_entry.insert(0, cfg["prodia_key"])

        ctk.CTkLabel(dlg, text="AI Horde Key (optional, leave blank for anonymous):",
                     font=("SF Pro Text", 11), text_color=C["muted"]).pack(**pad)
        ho_entry = ctk.CTkEntry(dlg, width=380, placeholder_text="0000000000")
        ho_entry.pack(padx=16, pady=(2, 6))
        if cfg.get("horde_key") and cfg["horde_key"] != "0000000000":
            ho_entry.insert(0, cfg["horde_key"])

        ctk.CTkLabel(dlg, text="Replicate Token (optional, for Flux + video):",
                     font=("SF Pro Text", 11), text_color=C["muted"]).pack(**pad)
        rep_entry = ctk.CTkEntry(dlg, width=380, placeholder_text="r8_...")
        rep_entry.pack(padx=16, pady=(2, 6))
        if cfg.get("replicate_token"):
            rep_entry.insert(0, cfg["replicate_token"])

        def _save():
            cfg["hf_token"] = hf_entry.get().strip()
            cfg["prodia_key"] = pr_entry.get().strip()
            cfg["horde_key"] = ho_entry.get().strip() or "0000000000"
            cfg["replicate_token"] = rep_entry.get().strip()
            cloudgen.save_settings(cfg)
            dlg.destroy()
            self._msg("Cloud settings saved.")

        ctk.CTkButton(dlg, text="Save", corner_radius=10, height=32,
                      font=("SF Pro Text", 12, "bold"),
                      fg_color=C["accent"], hover_color=C["hover"],
                      command=_save).pack(fill="x", padx=16, pady=(10, 16))

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

    # --- Smart masking ---

    def _get_edit_image(self):
        img = self.current_image or self.input_image
        if not img:
            show_error("No Image", "Load or generate a photo first.")
        return img

    def _apply_mask_to_painter(self, mask):
        """Load mask into inpaint painter and switch to inpaint mode."""
        self.input_image = self.current_image or self.input_image
        self.mode.set("inpaint")
        self._mode_changed("inpaint")
        self.painter.set_image(self.input_image)
        self.painter.set_mask(mask)
        self._msg("Mask applied. Edit with brush, then Generate.")

    def _mask_clothing(self):
        img = self._get_edit_image()
        if not img: return
        smartmask.clothing_mask(img, status=self._msg,
            done=lambda m: self.after(0, lambda: self._apply_mask_to_painter(m)),
            error=lambda e: self.after(0, lambda: show_error("Mask Error", str(e))))

    def _mask_skin(self):
        img = self._get_edit_image()
        if not img: return
        smartmask.skin_only_mask(img, status=self._msg,
            done=lambda m: self.after(0, lambda: self._apply_mask_to_painter(m)),
            error=lambda e: self.after(0, lambda: show_error("Mask Error", str(e))))

    def _mask_body(self):
        img = self._get_edit_image()
        if not img: return
        smartmask.body_no_face_mask(img, status=self._msg,
            done=lambda m: self.after(0, lambda: self._apply_mask_to_painter(m)),
            error=lambda e: self.after(0, lambda: show_error("Mask Error", str(e))))

    def _mask_face(self):
        img = self._get_edit_image()
        if not img: return
        smartmask.face_region_mask(img, status=self._msg,
            done=lambda m: self.after(0, lambda: self._apply_mask_to_painter(m)),
            error=lambda e: self.after(0, lambda: show_error("Mask Error", str(e))))

    # --- Inpaint presets ---

    def _apply_inpaint_preset(self, name):
        preset = INPAINT_PRESETS.get(name, {})
        p = preset.get("prompt", "")
        n = preset.get("neg", "")
        if p:
            self.prompt.delete("1.0", "end")
            self.prompt.insert("1.0", p)
        if n:
            self.neg.delete("1.0", "end")
            self.neg.insert("1.0", n)

    def _auto_inpaint(self):
        """One-click: auto-mask clothing + fill with preset prompt."""
        img = self._get_edit_image()
        if not img: return

        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            show_error("No Prompt",
                       "Pick an inpaint preset or write a prompt first.")
            return

        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, seed = self._params()

        def _on_mask(mask):
            self._msg("Auto-inpainting with mask...")
            engine.inpaint(prompt, img, mask, neg, steps, cfg, seed,
                           strength=0.85, status=self._msg,
                           done=lambda r, s: self.after(0, lambda: self._finish(r, s)),
                           error=lambda e: self.after(0, lambda: show_error(
                               "Inpaint Error", str(e))))

        smartmask.clothing_mask(img, status=self._msg,
            done=lambda m: self.after(0, lambda: _on_mask(m)),
            error=lambda e: self.after(0, lambda: show_error("Mask Error", str(e))))

    # --- ControlNet ---

    # --- Qwen AI ---

    def _qwen_edit(self):
        """Direct AI image edit via Qwen-Image-Edit."""
        img = self.current_image or self.input_image
        instruction = self.qwen_instruction.get().strip()

        # Save mode
        cfg = qwen.load_settings()
        selected = self.qwen_mode_menu.get()
        cfg["mode"] = "local" if "local" in selected else "cloud"
        cfg["local_model"] = "pruned" if selected == "local-pruned" else "rapid"
        qwen.save_settings(cfg)

        # No image = text-to-image, no instruction = error
        if not img and not instruction:
            self._msg("Enter an instruction (and optionally load an image).")
            return
        if not instruction:
            self._msg("Enter an edit instruction.")
            return

        self.qwen_status.configure(text=f"Qwen: '{instruction[:50]}...'")

        def _ok(result, seed):
            self.after(0, lambda: self._finish(result, seed))
            self.after(0, lambda: self.qwen_status.configure(text="Done."))

        def _fail(msg):
            self.after(0, lambda: show_error("Qwen Error", str(msg)))
            self.after(0, lambda: self.qwen_status.configure(text="Failed."))

        _status = lambda m: self.after(0, lambda: self.qwen_status.configure(text=m))

        if img:
            qwen.edit(img, instruction, status=_status, done=_ok, error=_fail)
        else:
            qwen.generate(instruction, status=_status, done=_ok, error=_fail)

    # --- ControlNet ---

    def _controlnet_gen(self):
        img = self._get_edit_image()
        if not img: return
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            self._msg("Enter a prompt first."); return
        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, seed = self._params()
        engine.controlnet_generate(
            prompt, img, control_type=self.cn_type.get(),
            neg=neg, steps=steps, cfg=cfg, seed=seed,
            status=self._msg,
            done=lambda r, s: self.after(0, lambda: self._finish(r, s)),
            error=lambda e: self.after(0, lambda: show_error(
                "ControlNet Error", str(e))))
        self._msg("Lighting applied.")

    # --- Cloud Video ---

    def _generate_video(self):
        """Generate a short video from the current image via cloud."""
        img = self.current_image or self.input_image
        if not img:
            show_error("No Image", "Generate or load an image first.")
            return

        backend = self.video_backend_menu.get()

        def _vid_done(path, fps):
            self.after(0, lambda: self.video_status.configure(
                text=f"Saved: {path}"))
            self.after(0, lambda: show_info("Video Ready",
                f"Video saved to:\n{path}\n\nOpen with QuickTime or VLC."))

        def _vid_error(msg):
            self.after(0, lambda: self.video_status.configure(
                text="Video generation failed."))
            self.after(0, lambda: show_error("Video Error", str(msg)))

        self.video_status.configure(text="Generating video... (may take 1-3 min)")
        cloudgen.generate_video(
            img, backend=backend,
            status=lambda m: self.after(0, lambda: self.video_status.configure(text=m)),
            done=_vid_done, error=_vid_error)

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

    def _fix_faces(self):
        if not self.current_image:
            show_error("No Image", "Generate an image first.")
            return
        prompt = self.prompt.get("1.0", "end").strip() or "detailed face, sharp eyes"
        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, _ = self._params()

        def pipe_fn(pr, img, mask, ng, st, cf, strength):
            """Synchronous inpaint for the fixer."""
            import torch
            from diffusers import StableDiffusionInpaintPipeline
            p = StableDiffusionInpaintPipeline(
                vae=engine._pipe.vae, text_encoder=engine._pipe.text_encoder,
                tokenizer=engine._pipe.tokenizer, unet=engine._pipe.unet,
                scheduler=engine._pipe.scheduler,
                safety_checker=None, feature_extractor=None)
            p = p.to(engine._pipe.device); p.enable_attention_slicing()
            g = torch.Generator(device="cpu").manual_seed(
                torch.randint(0, 2**32 - 1, (1,)).item())
            ww, hh = img.width // 8 * 8, img.height // 8 * 8
            r = p(prompt=pr, image=img.convert("RGB").resize((ww, hh)),
                  mask_image=mask.convert("RGB").resize((ww, hh)),
                  negative_prompt=ng or None, num_inference_steps=st,
                  guidance_scale=cf, strength=strength, generator=g)
            return r.images[0]

        fixer.fix_faces(
            self.current_image, pipe_fn, prompt, neg, steps, cfg,
            status=self._msg,
            done=lambda img: self.after(0, lambda: self._finish(img)),
            error=lambda e: self.after(0, lambda: show_error("Face Fix Error",
                f"Face fix failed:\n\n{e}\n\n"
                "Install: pip install opencv-python")))

    # --- Face swap (ReActor + FaceSwapLab + DiffFace) ---

    def _refresh_swapper_status(self):
        if faceswap.swapper_ready():
            self.swap_model_lbl.configure(
                text="Neural swap ready", text_color=C["green"])
            self.swap_dl_btn.pack_forget()
        else:
            self.swap_model_lbl.configure(
                text="Neural swap: model not found", text_color=C["orange"])
            self.swap_dl_btn.pack(side="right")

    def _download_swapper(self):
        faceswap.download_swapper(
            status=self._msg,
            done=lambda: self.after(0, self._refresh_swapper_status),
            error=lambda e: self.after(0, lambda: show_error(
                "Download Error", str(e))))

    def _load_swap_face(self):
        p = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if p:
            try:
                self.swap_face_src = Image.open(p)
                self.swap_status.configure(
                    text=f"Face loaded: {os.path.basename(p)}")
                self._msg(f"Swap face loaded: {os.path.basename(p)}")
            except Exception as e:
                show_error("Image Error", str(e))

    def _load_checkpoint_face(self, name):
        if not name:
            return
        face_img, ref_img = faceswap.load_checkpoint(name)
        if ref_img:
            self.swap_face_src = ref_img
            self.swap_status.configure(text=f"Checkpoint: {name}")
            self._msg(f"Loaded face checkpoint: {name}")
        else:
            show_error("Checkpoint Error", f"Could not load '{name}'.")

    def _save_swap_checkpoint(self):
        img = self.swap_face_src or self.current_image or self.input_image
        if not img:
            show_error("No Image", "Load a face photo or generate an image first.")
            return
        dlg = ctk.CTkInputDialog(text="Checkpoint name:", title="Save Face")
        name = dlg.get_input()
        if not name or not name.strip():
            return
        faceswap.save_checkpoint(
            name.strip(), img, status=self._msg,
            done=lambda n: self.after(0, self._refresh_checkpoints),
            error=lambda e: self.after(0, lambda: show_error(
                "Checkpoint Error", str(e))))

    def _refresh_checkpoints(self):
        names = [""] + faceswap.list_checkpoints()
        self.ckpt_menu.configure(values=names)
        self._msg("Face checkpoint saved.")

    def _do_swap(self):
        if not self.swap_face_src:
            show_error("No Face",
                       "Click 'Load Face' or pick a checkpoint first.")
            return
        tgt = self.current_image or self.input_image
        if not tgt:
            show_error("No Target", "Generate or load a target image first.")
            return
        faceswap.swap(
            self.swap_face_src, tgt, refine=self.refine_var.get(),
            status=self._msg,
            done=lambda img: self.after(0, lambda: self._finish(img)),
            error=lambda e: self.after(0, lambda: show_error("Face Swap Error",
                f"Swap failed:\n\n{e}\n\n"
                "Install: pip install insightface opencv-python onnxruntime")))

    def _do_multi_swap(self):
        if not self.swap_face_src:
            show_error("No Face", "Click 'Load Face' or pick a checkpoint.")
            return
        tgt = self.current_image or self.input_image
        if not tgt:
            show_error("No Target", "Generate or load a target image first.")
            return
        faceswap.multi_swap(
            self.swap_face_src, tgt, refine=self.refine_var.get(),
            status=self._msg,
            done=lambda img: self.after(0, lambda: self._finish(img)),
            error=lambda e: self.after(0, lambda: show_error("Face Swap Error",
                f"Multi-swap failed:\n\n{e}")))

    def _do_bidi_swap(self):
        """Switch faces between two photos. Loads Photo B via dialog."""
        photo_a = self.swap_face_src or self.current_image or self.input_image
        if not photo_a:
            show_error("No Photo A",
                       "Load or generate the first photo, then click Switch.")
            return
        p = filedialog.askopenfilename(
            title="Select Photo B (faces will be switched)",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if not p:
            return
        try:
            photo_b = Image.open(p)
        except Exception as e:
            show_error("Image Error", str(e)); return

        def _on_done(result_a, result_b):
            # Show result_b (A's face on B's body) as primary,
            # auto-save result_a (B's face on A's body) to history
            import history
            history.save(result_a, {"type": "bidi_swap",
                                    "note": "B's face on A's body"})
            self.after(0, lambda: self._finish(result_b))
            self.after(100, lambda: self._msg(
                "Both results saved. Second result in history."))

        faceswap.bidi_swap(
            photo_a, photo_b, refine=self.refine_var.get(),
            status=self._msg,
            done=lambda a, b: self.after(0, lambda: _on_done(a, b)),
            error=lambda e: self.after(0, lambda: show_error(
                "Face Switch Error",
                f"Bidirectional swap failed:\n\n{e}")))

    def _save_identity(self):
        name = self.id_name.get().strip()
        if not name:
            show_error("Name Required", "Enter a name for this identity (e.g. Mai, Anna).")
            return
        img = self.current_image or self.input_image
        if not img:
            show_error("No Image", "Generate or load a photo first.")
            return
        consistency.save_identity(
            name, img, status=self._msg,
            done=lambda n: self.after(0, lambda: self._refresh_identities()),
            error=lambda e: self.after(0, lambda: show_error("Identity Error",
                f"Could not save identity:\n\n{e}\n\n"
                "Install: pip install insightface onnxruntime")))

    def _refresh_identities(self):
        ids = ["(none)"] + consistency.list_identities()
        self.id_select.configure(values=ids)
        self._msg("Identity saved.")

    def _on_identity_selected(self, name):
        if name == "(none)":
            return
        try:
            _, face, ref = consistency.load_identity(name)
            if ref:
                self._show(ref)
                self._msg(f"Identity '{name}' loaded — change prompt and Generate.")
        except Exception as e:
            show_error("Load Error", str(e))

    def _generate_with_identity(self):
        name = self.id_select.get()
        if name == "(none)":
            show_error("No Identity", "Select a saved identity first,\n"
                       "or save one from a generated image.")
            return
        prompt = self.prompt.get("1.0", "end").strip()
        if not prompt:
            self._msg("Enter a prompt (new scene/outfit)."); return
        neg = self.neg.get("1.0", "end").strip()
        steps, cfg, seed = self._params()
        try:
            w = int(self.e_w.get()) // 8 * 8
            h = int(self.e_h.get()) // 8 * 8
        except ValueError:
            w, h = 512, 768
        strength = self.id_strength.get()

        self._busy = True
        self.gen_btn.configure(state="disabled", text="Working...")

        def ok(img, s):
            self._busy = False
            self.after(0, lambda: self._finish(img, s))
            self.after(0, lambda: self.gen_btn.configure(state="normal", text="Generate"))

        def fail(e):
            self._busy = False
            self.after(0, lambda: self.gen_btn.configure(state="normal", text="Generate"))
            self.after(0, lambda: show_error("Identity Generation Error",
                f"Failed:\n\n{e}"))

        consistency.generate_with_identity(
            name, prompt, neg, w, h, steps, cfg, seed, strength,
            status=self._msg, done=ok, error=fail)

    def _show_history(self):
        HistoryWindow(self)

    def _params(self):
        """Read steps, cfg, seed from entries."""
        try:
            return (int(self.e_steps.get()), float(self.e_cfg.get()),
                    int(self.e_seed.get()))
        except ValueError:
            return 30, 7.0, -1

    def _generate(self):
        if self._busy: return
        raw_prompt = self.prompt.get("1.0", "end").strip()
        if not raw_prompt:
            self._msg("Enter a prompt."); return

        # Dynamic prompt expansion
        prompt = prompts.expand(raw_prompt) if prompts.has_dynamic(raw_prompt) else raw_prompt
        if prompt != raw_prompt:
            self._msg(f"Expanded: {prompt[:80]}...")

        # Prompt enhancement (quality anchors + lighting + lens)
        if self.enhance_var.get():
            prompt = prompts.enhance(
                prompt,
                quality=self.quality_menu.get(),
                lighting=self.lighting_menu.get(),
                lens=self.lens_menu.get())
            self._msg(f"Enhanced: {prompt[:100]}...")

        neg = self.neg.get("1.0", "end").strip()
        # Auto-apply enhanced negative when Enhance is on and neg is empty
        if self.enhance_var.get() and not neg:
            neg = ENHANCED_NEGATIVE
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

        # Cloud generation (txt2img / img2img only)
        if self.cloud_var.get():
            img_in = None
            strength = 0.75
            if mode in ("img2img", "edit"):
                img_in = self.input_image if mode == "img2img" else (
                    self.current_image or self.input_image)
                if not img_in:
                    self._msg("Load a photo first."); fail("No photo"); return
                strength = self.str_sl.get() if mode == "img2img" else 0.5
            elif mode == "inpaint":
                fail("Cloud inpainting not supported. Uncheck 'Use Cloud'.")
                return
            cloudgen.generate(prompt, neg, w, h, steps, cfg,
                              image=img_in, strength=strength,
                              status=self._msg, done=ok, error=fail)
            return

        # Local generation
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
        # Auto-save to history
        try:
            prompt = self.prompt.get("1.0", "end").strip()
            neg = self.neg.get("1.0", "end").strip()
            model = self.cfg.get("model_id", "")
            history.save(img, prompt, neg, seed or 0, model,
                         self.mode.get(), *self._params())
        except Exception:
            pass  # History save is best-effort
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
