#!/bin/bash
# JDS Document Studio launcher — double-click on macOS, or run from a terminal.
# Installs dependencies on first run, then starts the local server and opens it.
set -e
cd "$(dirname "$0")"

echo "JDS Document Studio — preparing…"
python3 -m pip install --quiet -r requirements.txt

URL="http://127.0.0.1:8731"
( sleep 2; command -v open >/dev/null && open "$URL" ) &

python3 -m studio.server
