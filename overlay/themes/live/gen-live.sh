#!/bin/bash
# Veragensia "living wallpaper" — generate N branded aurora frames via PIL.
# Run from this dir:
#   python3 gen-live.py  frames/  12  1920 1080
set -e
cd "$(dirname "$0")"
OUT="${1:-frames}"
N="${2:-12}"
W="${3:-1920}"
H="${4:-1080}"
python3 gen-live.py "$OUT" "$N" "$W" "$H"
echo "generated $N frames in $OUT/"