#!/usr/bin/env python3
"""
JDS-PRJ-SFW-001 — Local Image Generator
A flat, iOS-style local image generation app using Stable Diffusion.
Runs entirely on-device via Hugging Face Diffusers with Apple MPS backend.

Author: N. Johansson
"""

import os
import sys
import json
import threading
import datetime
from pathlib import Path
from PIL import Image, ImageTk

import customtkinter as ctk

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
APP_NAME = "JDS Image Studio"
APP_VERSION = "1.0.0"
CONFIG_DIR = Path.home() / ".jds-image-studio"
CONFIG_FILE = CONFIG_DIR / "config.json"
DEFAULT_OUTPUT_DIR = Path.home() / "Pictures" / "JDS-Image-Studio"
DEFAULT_MODEL = "stabilityai/stable-diffusion-2-1"

# iOS-style colour palette (flat, muted)
COLORS = {
    "bg": "#F2F2F7",           # System grouped background
    "surface": "#FFFFFF",       # Card / surface
    "text": "#1C1C1E",          # Primary label
    "text_secondary": "#8E8E93",# Secondary label
    "accent": "#007AFF",        # System blue
    "accent_hover": "#0056CC",
    "destructive": "#FF3B30",   # System red
    "success": "#34C759",       # System green
    "warning": "#FF9500",       # System orange
    "separator": "#E5E5EA",     # Separator
    "fill": "#E5E5EA",          # Tertiary fill
}

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

def load_config():
    """Load or create default configuration."""
    defaults = {
        "model_id": DEFAULT_MODEL,
        "model_path": "",
        "output_dir": str(DEFAULT_OUTPUT_DIR),
        "default_width": 512,
        "default_height": 512,
        "default_steps": 25,
        "default_guidance": 7.5,
        "safety_checker": False,
    }
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                saved = json.load(f)
            defaults.update(saved)
        except Exception:
            pass
    return defaults


def save_config(config):
    """Persist configuration to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


# ---------------------------------------------------------------------------
# Pipeline loader (runs in background thread)
# ---------------------------------------------------------------------------

_pipeline = None
_pipeline_lock = threading.Lock()


def get_device():
    """Return best available torch device."""
    import torch
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def load_pipeline(model_id_or_path, on_status=None, on_done=None, on_error=None):
    """Load the Stable Diffusion pipeline in a background thread."""

    def _load():
        global _pipeline
        try:
            if on_status:
                on_status("Loading model — this may take a few minutes on first run...")

            import torch
            from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

            device = get_device()
            dtype = torch.float16 if device == "cuda" else torch.float32

            if on_status:
                on_status(f"Device: {device.upper()} | Loading {model_id_or_path}...")

            # Determine if it is a local path or HuggingFace model ID
            is_local = os.path.isdir(model_id_or_path)

            with _pipeline_lock:
                pipe = StableDiffusionPipeline.from_pretrained(
                    model_id_or_path,
                    torch_dtype=dtype,
                    local_files_only=is_local,
                )

                # Disable safety checker for unrestricted use
                pipe.safety_checker = None
                pipe.feature_extractor = None

                pipe = pipe.to(device)

                # Enable attention slicing for low-VRAM / unified memory
                pipe.enable_attention_slicing()

                _pipeline = pipe

            if on_status:
                on_status(f"Ready — {device.upper()}")
            if on_done:
                on_done()

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_load, daemon=True)
    t.start()


def generate_image(prompt, negative_prompt="", width=512, height=512,
                   steps=25, guidance=7.5, seed=-1,
                   on_status=None, on_done=None, on_error=None):
    """Generate an image from a text prompt."""

    def _generate():
        global _pipeline
        try:
            import torch

            if _pipeline is None:
                if on_error:
                    on_error("Model not loaded. Please load a model first.")
                return

            if on_status:
                on_status("Generating image...")

            device = get_device()
            generator = None
            actual_seed = seed

            if seed < 0:
                actual_seed = torch.randint(0, 2**32 - 1, (1,)).item()

            generator = torch.Generator(device="cpu").manual_seed(actual_seed)

            with _pipeline_lock:
                result = _pipeline(
                    prompt=prompt,
                    negative_prompt=negative_prompt if negative_prompt else None,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    guidance_scale=guidance,
                    generator=generator,
                )

            image = result.images[0]

            if on_done:
                on_done(image, actual_seed)

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_generate, daemon=True)
    t.start()


def generate_img2img(prompt, init_image, strength=0.75, negative_prompt="",
                     steps=25, guidance=7.5, seed=-1,
                     on_status=None, on_done=None, on_error=None):
    """Generate an image from an existing image + prompt (img2img)."""

    def _generate():
        global _pipeline
        try:
            import torch
            from diffusers import StableDiffusionImg2ImgPipeline

            if _pipeline is None:
                if on_error:
                    on_error("Model not loaded. Please load a model first.")
                return

            if on_status:
                on_status("Running img2img...")

            # Build an img2img pipeline from the same model components
            img2img_pipe = StableDiffusionImg2ImgPipeline(
                vae=_pipeline.vae,
                text_encoder=_pipeline.text_encoder,
                tokenizer=_pipeline.tokenizer,
                unet=_pipeline.unet,
                scheduler=_pipeline.scheduler,
                safety_checker=None,
                feature_extractor=None,
            )
            img2img_pipe = img2img_pipe.to(_pipeline.device)
            img2img_pipe.enable_attention_slicing()

            actual_seed = seed
            if seed < 0:
                actual_seed = torch.randint(0, 2**32 - 1, (1,)).item()
            generator = torch.Generator(device="cpu").manual_seed(actual_seed)

            # Prepare input image
            init = init_image.convert("RGB").resize(
                (init_image.width // 8 * 8, init_image.height // 8 * 8)
            )

            result = img2img_pipe(
                prompt=prompt,
                image=init,
                strength=strength,
                negative_prompt=negative_prompt if negative_prompt else None,
                num_inference_steps=steps,
                guidance_scale=guidance,
                generator=generator,
            )

            image = result.images[0]

            if on_done:
                on_done(image, actual_seed)

        except Exception as e:
            if on_error:
                on_error(str(e))

    t = threading.Thread(target=_generate, daemon=True)
    t.start()


# ---------------------------------------------------------------------------
# GUI Application
# ---------------------------------------------------------------------------

class ImageStudioApp(ctk.CTk):
    """Main application window — flat iOS-style design."""

    def __init__(self):
        super().__init__()

        self.config = load_config()
        self.current_image = None
        self.input_image = None
        self.last_seed = None

        # --- Window setup ---
        self.title(APP_NAME)
        self.geometry("1100x780")
        self.minsize(900, 650)
        self.configure(fg_color=COLORS["bg"])

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # --- Layout: sidebar + main area ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main_area()

    # -----------------------------------------------------------------------
    # Sidebar
    # -----------------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=320, corner_radius=0,
                               fg_color=COLORS["surface"])
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        pad = {"padx": 16, "pady": (0, 0)}

        # App title
        title = ctk.CTkLabel(sidebar, text=APP_NAME, font=("SF Pro Display", 22, "bold"),
                             text_color=COLORS["text"])
        title.pack(padx=16, pady=(20, 2), anchor="w")

        version_lbl = ctk.CTkLabel(sidebar, text=f"v{APP_VERSION}",
                                   font=("SF Pro Text", 12),
                                   text_color=COLORS["text_secondary"])
        version_lbl.pack(padx=16, pady=(0, 12), anchor="w")

        # Separator
        sep = ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["separator"])
        sep.pack(fill="x", padx=16, pady=(0, 12))

        # --- Mode tabs ---
        mode_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        mode_frame.pack(fill="x", **pad)

        self.mode_var = ctk.StringVar(value="txt2img")
        self.txt2img_btn = ctk.CTkSegmentedButton(
            mode_frame,
            values=["txt2img", "img2img"],
            variable=self.mode_var,
            command=self._on_mode_change,
            font=("SF Pro Text", 13),
        )
        self.txt2img_btn.pack(fill="x", pady=(0, 12))

        # --- Prompt ---
        prompt_lbl = ctk.CTkLabel(sidebar, text="Prompt", font=("SF Pro Text", 13, "bold"),
                                  text_color=COLORS["text"])
        prompt_lbl.pack(padx=16, pady=(8, 4), anchor="w")

        self.prompt_box = ctk.CTkTextbox(sidebar, height=80, corner_radius=10,
                                         font=("SF Pro Text", 13),
                                         fg_color=COLORS["fill"],
                                         text_color=COLORS["text"],
                                         border_width=0)
        self.prompt_box.pack(fill="x", padx=16, pady=(0, 8))

        # --- Negative prompt ---
        neg_lbl = ctk.CTkLabel(sidebar, text="Negative Prompt", font=("SF Pro Text", 13, "bold"),
                               text_color=COLORS["text"])
        neg_lbl.pack(padx=16, pady=(4, 4), anchor="w")

        self.neg_prompt_box = ctk.CTkTextbox(sidebar, height=50, corner_radius=10,
                                             font=("SF Pro Text", 13),
                                             fg_color=COLORS["fill"],
                                             text_color=COLORS["text"],
                                             border_width=0)
        self.neg_prompt_box.pack(fill="x", padx=16, pady=(0, 8))

        # --- img2img controls (hidden by default) ---
        self.img2img_frame = ctk.CTkFrame(sidebar, fg_color="transparent")

        load_img_btn = ctk.CTkButton(self.img2img_frame, text="Load Input Image",
                                     corner_radius=10, height=36,
                                     font=("SF Pro Text", 13),
                                     fg_color=COLORS["fill"],
                                     text_color=COLORS["text"],
                                     hover_color=COLORS["separator"],
                                     command=self._load_input_image)
        load_img_btn.pack(fill="x", pady=(0, 4))

        self.strength_label = ctk.CTkLabel(self.img2img_frame, text="Strength: 0.75",
                                           font=("SF Pro Text", 12),
                                           text_color=COLORS["text_secondary"])
        self.strength_label.pack(anchor="w")

        self.strength_slider = ctk.CTkSlider(self.img2img_frame, from_=0.1, to=1.0,
                                             number_of_steps=18,
                                             command=self._on_strength_change)
        self.strength_slider.set(0.75)
        self.strength_slider.pack(fill="x", pady=(0, 8))

        # --- Settings ---
        sep2 = ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["separator"])
        sep2.pack(fill="x", padx=16, pady=(4, 8))

        settings_lbl = ctk.CTkLabel(sidebar, text="Settings", font=("SF Pro Text", 13, "bold"),
                                    text_color=COLORS["text"])
        settings_lbl.pack(padx=16, pady=(0, 4), anchor="w")

        settings_grid = ctk.CTkFrame(sidebar, fg_color="transparent")
        settings_grid.pack(fill="x", padx=16, pady=(0, 8))
        settings_grid.grid_columnconfigure((0, 1), weight=1)

        # Width
        ctk.CTkLabel(settings_grid, text="Width", font=("SF Pro Text", 12),
                     text_color=COLORS["text_secondary"]).grid(row=0, column=0, sticky="w")
        self.width_entry = ctk.CTkEntry(settings_grid, width=80, corner_radius=8,
                                        font=("SF Pro Text", 12),
                                        fg_color=COLORS["fill"], border_width=0)
        self.width_entry.insert(0, str(self.config["default_width"]))
        self.width_entry.grid(row=0, column=1, sticky="e", pady=2)

        # Height
        ctk.CTkLabel(settings_grid, text="Height", font=("SF Pro Text", 12),
                     text_color=COLORS["text_secondary"]).grid(row=1, column=0, sticky="w")
        self.height_entry = ctk.CTkEntry(settings_grid, width=80, corner_radius=8,
                                         font=("SF Pro Text", 12),
                                         fg_color=COLORS["fill"], border_width=0)
        self.height_entry.insert(0, str(self.config["default_height"]))
        self.height_entry.grid(row=1, column=1, sticky="e", pady=2)

        # Steps
        ctk.CTkLabel(settings_grid, text="Steps", font=("SF Pro Text", 12),
                     text_color=COLORS["text_secondary"]).grid(row=2, column=0, sticky="w")
        self.steps_entry = ctk.CTkEntry(settings_grid, width=80, corner_radius=8,
                                        font=("SF Pro Text", 12),
                                        fg_color=COLORS["fill"], border_width=0)
        self.steps_entry.insert(0, str(self.config["default_steps"]))
        self.steps_entry.grid(row=2, column=1, sticky="e", pady=2)

        # Guidance
        ctk.CTkLabel(settings_grid, text="CFG Scale", font=("SF Pro Text", 12),
                     text_color=COLORS["text_secondary"]).grid(row=3, column=0, sticky="w")
        self.guidance_entry = ctk.CTkEntry(settings_grid, width=80, corner_radius=8,
                                           font=("SF Pro Text", 12),
                                           fg_color=COLORS["fill"], border_width=0)
        self.guidance_entry.insert(0, str(self.config["default_guidance"]))
        self.guidance_entry.grid(row=3, column=1, sticky="e", pady=2)

        # Seed
        ctk.CTkLabel(settings_grid, text="Seed", font=("SF Pro Text", 12),
                     text_color=COLORS["text_secondary"]).grid(row=4, column=0, sticky="w")
        self.seed_entry = ctk.CTkEntry(settings_grid, width=80, corner_radius=8,
                                       font=("SF Pro Text", 12),
                                       fg_color=COLORS["fill"], border_width=0)
        self.seed_entry.insert(0, "-1")
        self.seed_entry.grid(row=4, column=1, sticky="e", pady=2)

        # --- Model selector ---
        sep3 = ctk.CTkFrame(sidebar, height=1, fg_color=COLORS["separator"])
        sep3.pack(fill="x", padx=16, pady=(4, 8))

        model_lbl = ctk.CTkLabel(sidebar, text="Model", font=("SF Pro Text", 13, "bold"),
                                 text_color=COLORS["text"])
        model_lbl.pack(padx=16, pady=(0, 4), anchor="w")

        self.model_entry = ctk.CTkEntry(sidebar, corner_radius=10,
                                        font=("SF Pro Text", 12),
                                        fg_color=COLORS["fill"],
                                        text_color=COLORS["text"],
                                        border_width=0,
                                        placeholder_text="HuggingFace ID or local path")
        model_val = self.config.get("model_path") or self.config.get("model_id", DEFAULT_MODEL)
        self.model_entry.insert(0, model_val)
        self.model_entry.pack(fill="x", padx=16, pady=(0, 4))

        browse_btn = ctk.CTkButton(sidebar, text="Browse Local Model...",
                                   corner_radius=10, height=32,
                                   font=("SF Pro Text", 12),
                                   fg_color=COLORS["fill"],
                                   text_color=COLORS["text"],
                                   hover_color=COLORS["separator"],
                                   command=self._browse_model)
        browse_btn.pack(padx=16, pady=(0, 4), anchor="w")

        load_model_btn = ctk.CTkButton(sidebar, text="Load Model",
                                       corner_radius=10, height=36,
                                       font=("SF Pro Text", 13, "bold"),
                                       fg_color=COLORS["accent"],
                                       hover_color=COLORS["accent_hover"],
                                       command=self._load_model)
        load_model_btn.pack(fill="x", padx=16, pady=(4, 8))

        # --- Generate button ---
        self.generate_btn = ctk.CTkButton(sidebar, text="Generate",
                                          corner_radius=12, height=44,
                                          font=("SF Pro Display", 16, "bold"),
                                          fg_color=COLORS["accent"],
                                          hover_color=COLORS["accent_hover"],
                                          command=self._on_generate)
        self.generate_btn.pack(fill="x", padx=16, pady=(8, 8), side="bottom")

        # --- Status bar ---
        self.status_label = ctk.CTkLabel(sidebar, text="No model loaded",
                                         font=("SF Pro Text", 11),
                                         text_color=COLORS["text_secondary"])
        self.status_label.pack(padx=16, pady=(0, 12), side="bottom", anchor="w")

    # -----------------------------------------------------------------------
    # Main area (image preview)
    # -----------------------------------------------------------------------
    def _build_main_area(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["bg"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Image display card
        self.image_card = ctk.CTkFrame(main, corner_radius=16,
                                       fg_color=COLORS["surface"])
        self.image_card.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.image_card.grid_rowconfigure(0, weight=1)
        self.image_card.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.image_card, text="",
                                        font=("SF Pro Text", 15),
                                        text_color=COLORS["text_secondary"])
        self.image_label.configure(text="Load a model and enter a prompt to generate an image.")
        self.image_label.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Bottom toolbar
        toolbar = ctk.CTkFrame(main, height=48, corner_radius=0,
                               fg_color=COLORS["bg"])
        toolbar.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 12))

        save_btn = ctk.CTkButton(toolbar, text="Save Image", width=120,
                                 corner_radius=10, height=36,
                                 font=("SF Pro Text", 13),
                                 fg_color=COLORS["accent"],
                                 hover_color=COLORS["accent_hover"],
                                 command=self._save_image)
        save_btn.pack(side="left")

        self.seed_display = ctk.CTkLabel(toolbar, text="",
                                         font=("SF Pro Text", 12),
                                         text_color=COLORS["text_secondary"])
        self.seed_display.pack(side="right")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------
    def _set_status(self, msg):
        self.after(0, lambda: self.status_label.configure(text=msg))

    def _on_mode_change(self, mode):
        if mode == "img2img":
            self.img2img_frame.pack(fill="x", padx=16, pady=(0, 8),
                                    after=self.neg_prompt_box)
        else:
            self.img2img_frame.pack_forget()

    def _on_strength_change(self, val):
        self.strength_label.configure(text=f"Strength: {val:.2f}")

    def _browse_model(self):
        from tkinter import filedialog
        path = filedialog.askdirectory(title="Select model folder")
        if path:
            self.model_entry.delete(0, "end")
            self.model_entry.insert(0, path)

    def _load_input_image(self):
        from tkinter import filedialog
        path = filedialog.askopenfilename(
            title="Select input image",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")]
        )
        if path:
            self.input_image = Image.open(path)
            self._display_image(self.input_image)
            self._set_status(f"Input image loaded: {os.path.basename(path)}")

    def _load_model(self):
        model = self.model_entry.get().strip()
        if not model:
            self._set_status("Enter a model ID or path first.")
            return

        self.generate_btn.configure(state="disabled")
        self._set_status("Loading model...")

        def on_done():
            self.after(0, lambda: self.generate_btn.configure(state="normal"))
            self.config["model_id"] = model
            save_config(self.config)

        def on_error(e):
            self._set_status(f"Error: {e}")
            self.after(0, lambda: self.generate_btn.configure(state="normal"))

        load_pipeline(model, on_status=self._set_status, on_done=on_done, on_error=on_error)

    def _on_generate(self):
        prompt = self.prompt_box.get("1.0", "end").strip()
        if not prompt:
            self._set_status("Enter a prompt first.")
            return

        neg = self.neg_prompt_box.get("1.0", "end").strip()

        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            steps = int(self.steps_entry.get())
            guidance = float(self.guidance_entry.get())
            seed = int(self.seed_entry.get())
        except ValueError:
            self._set_status("Invalid settings — check your numbers.")
            return

        # Ensure dimensions are multiples of 8
        w = (w // 8) * 8
        h = (h // 8) * 8

        self.generate_btn.configure(state="disabled")

        def on_done(image, actual_seed):
            self.current_image = image
            self.last_seed = actual_seed
            self.after(0, lambda: self._display_image(image))
            self.after(0, lambda: self.seed_display.configure(
                text=f"Seed: {actual_seed}"))
            self._set_status("Done.")
            self.after(0, lambda: self.generate_btn.configure(state="normal"))

        def on_error(e):
            self._set_status(f"Error: {e}")
            self.after(0, lambda: self.generate_btn.configure(state="normal"))

        mode = self.mode_var.get()
        if mode == "img2img" and self.input_image is not None:
            strength = self.strength_slider.get()
            generate_img2img(
                prompt=prompt, init_image=self.input_image,
                strength=strength, negative_prompt=neg,
                steps=steps, guidance=guidance, seed=seed,
                on_status=self._set_status, on_done=on_done, on_error=on_error,
            )
        else:
            generate_image(
                prompt=prompt, negative_prompt=neg,
                width=w, height=h, steps=steps, guidance=guidance, seed=seed,
                on_status=self._set_status, on_done=on_done, on_error=on_error,
            )

    def _display_image(self, pil_image):
        """Fit image into the preview area preserving aspect ratio."""
        card_w = self.image_card.winfo_width() - 40
        card_h = self.image_card.winfo_height() - 40
        if card_w < 100:
            card_w = 500
        if card_h < 100:
            card_h = 500

        img = pil_image.copy()
        img.thumbnail((card_w, card_h), Image.LANCZOS)

        self._tk_image = ImageTk.PhotoImage(img)
        self.image_label.configure(image=self._tk_image, text="")

    def _save_image(self):
        if self.current_image is None:
            self._set_status("No image to save.")
            return

        from tkinter import filedialog
        output_dir = self.config.get("output_dir", str(DEFAULT_OUTPUT_DIR))
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        default_name = f"jds_image_{timestamp}.png"

        path = filedialog.asksaveasfilename(
            title="Save Image",
            initialdir=output_dir,
            initialfile=default_name,
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All", "*.*")]
        )
        if path:
            self.current_image.save(path)
            self._set_status(f"Saved: {os.path.basename(path)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    app = ImageStudioApp()
    app.mainloop()


if __name__ == "__main__":
    main()
