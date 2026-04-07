#!/usr/bin/env python3
"""JDS-PRJ-SFW-001 — JDS Image Studio. Entry point."""

import signal
import sys

signal.signal(signal.SIGINT, lambda *_: sys.exit(0))

from gui import App

if __name__ == "__main__":
    App().mainloop()
