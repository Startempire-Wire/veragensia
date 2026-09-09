#!/usr/bin/env python3
"""Idempotent page/nginx patches for the Veragensia push-to-talk voice button.

- Injects the voice-button script tag into the selkies client index.html.
- Adds the /voice-gateway/ nginx location proxying to 127.0.0.1:8900.
Both patches detect existing state and never duplicate. Runs inside the
container; the Dockerfile/startwm can re-run it after image updates.
"""
from pathlib import Path
import os
import sys

WEB_INDEX = Path(os.environ.get(
    "VERAGENSIA_VOICE_INDEX", "/usr/share/selkies/web/index.html"))
VOICE_TAG = '<script src="/src/veragensia-voice.js"></script>'
VOICE_SOURCE = Path(os.environ.get(
    "VERAGENSIA_VOICE_SOURCE",
    "/veragensia/docker/omarchy-demo/overlay/selkies-web/veragensia-voice.js"))
VOICE_TARGET = Path(os.environ.get(
    "VERAGENSIA_VOICE_TARGET", "/usr/share/selkies/web/src/veragensia-voice.js"))
NGINX_CONF = Path(os.environ.get(
    "VERAGENSIA_VOICE_NGINX", "/etc/nginx/conf.d/default.conf"))
NGINX_BLOCK = """    location /voice-gateway/ {
        proxy_pass http://127.0.0.1:8900/;
        proxy_read_timeout 90s;
        proxy_set_header Host $host;
    }
"""


def patch_asset():
    # At image build time the asset is already copied into the target, while a
    # running overlay has the source under /veragensia. Support both paths so
    # the patch remains useful during upgrades and on the live mounted repo.
    if VOICE_SOURCE.exists():
        data = VOICE_SOURCE.read_bytes()
    elif VOICE_TARGET.exists():
        print("voice asset: image copy already present")
        return 0
    else:
        print(f"voice asset: source missing: {VOICE_SOURCE}", file=sys.stderr)
        return 1
    if VOICE_TARGET.exists() and VOICE_TARGET.read_bytes() == data:
        print("voice asset: already current")
        return 0
    VOICE_TARGET.parent.mkdir(parents=True, exist_ok=True)
    VOICE_TARGET.write_bytes(data)
    print("voice asset: installed")
    return 0


def patch_index():
    html = WEB_INDEX.read_text(encoding="utf-8")
    if "veragensia-voice.js" in html:
        print("index.html: voice button already present")
        return 0
    patched = html.replace("</body>", VOICE_TAG + "</body>", 1)
    if patched == html:
        print("index.html: no </body> anchor found", file=sys.stderr)
        return 1
    WEB_INDEX.write_text(patched, encoding="utf-8")
    print("index.html: voice button injected")
    return 0


def _server_ranges(lines):
    """Return (start, end) indexes for the simple nginx server blocks."""
    ranges = []
    index = 0
    while index < len(lines):
        if lines[index].strip() != "server {":
            index += 1
            continue
        depth = lines[index].count("{") - lines[index].count("}")
        end = index
        while depth > 0 and end + 1 < len(lines):
            end += 1
            depth += lines[end].count("{") - lines[end].count("}")
        if depth != 0:
            return []
        ranges.append((index, end))
        index = end + 1
    return ranges


def patch_nginx():
    lines = NGINX_CONF.read_text(encoding="utf-8").split("\n")
    ranges = _server_ranges(lines)
    if not ranges:
        print("nginx: no complete server block anchor found", file=sys.stderr)
        return 1
    insert_at = []
    for start, end in ranges:
        block = "\n".join(lines[start:end + 1])
        if "/voice-gateway/" not in block:
            insert_at.append(end)
    for index in reversed(insert_at):
        lines.insert(index, NGINX_BLOCK.rstrip("\n"))
    if insert_at:
        NGINX_CONF.write_text("\n".join(lines), encoding="utf-8")
        print(f"nginx: voice-gateway location added to {len(insert_at)} server block(s)")
    else:
        print("nginx: voice-gateway location already present in every server block")
    return 0


if __name__ == "__main__":
    raise SystemExit(patch_asset() | patch_index() | patch_nginx())
