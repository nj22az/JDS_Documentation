#!/usr/bin/env python3
"""JDS-PRJ-SFW-001 — JDS Image Studio. Entry point."""

import signal
import sys

signal.signal(signal.SIGINT, lambda *_: sys.exit(0))


def check_deps():
    """Verify critical dependencies are installed. Show dialog if not."""
    missing = []
    for mod in ["torch", "diffusers", "transformers", "customtkinter",
                "PIL", "numpy", "huggingface_hub"]:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if missing:
        try:
            import tkinter as tk
            from tkinter import messagebox
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Missing Dependencies",
                f"The following packages are not installed:\n\n"
                f"{', '.join(missing)}\n\n"
                f"Run setup.command first, or:\n"
                f"  pip install -r requirements.txt")
            root.destroy()
        except Exception:
            print(f"ERROR: Missing packages: {', '.join(missing)}")
            print("Run: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    check_deps()
    from gui import App
    App().mainloop()
