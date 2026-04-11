#!/bin/bash
# ============================================================
# JDS Image Studio — Launch
# Double-click this file in Finder to start the app.
# ============================================================

cd "$(dirname "$0")"

# Check setup was done
if [ ! -d "venv" ]; then
    echo ""
    echo "First-time setup required."
    echo "Double-click setup.command first."
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

# Activate and run
source venv/bin/activate
python3 app.py

# When the window closes, the script exits — nothing left running.
