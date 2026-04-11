#!/bin/bash
# ============================================================
# JDS Image Studio — One-Time Setup
# Double-click this file in Finder to install everything.
# ============================================================

# Move to the script's own directory (wherever the user put it)
cd "$(dirname "$0")"

echo ""
echo "=============================================="
echo "  JDS Image Studio — Setup"
echo "=============================================="
echo ""

# Check Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed."
    echo "Install it from https://www.python.org/downloads/ or via Homebrew:"
    echo "  brew install python@3.11"
    echo ""
    read -p "Press Enter to close..."
    exit 1
fi

PY_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Found Python $PY_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
echo ""
echo "Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

echo ""
echo "=============================================="
echo "  Setup complete!"
echo "=============================================="
echo ""
echo "  To launch the app, double-click:"
echo "    JDS Image Studio.command"
echo ""
echo "  On first launch, the app will help you"
echo "  download a model (~4-5 GB)."
echo ""
read -p "Press Enter to close..."
