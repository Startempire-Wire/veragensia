#!/usr/bin/env python3
"""Idempotent page/nginx patches for the Veragensia push-to-talk voice button.

- Injects the voice-button script tag into the selkies client index.html.
- Adds the /voice-gateway/ nginx location proxying to 127.0.0.1:8900.
Both patches detect existing state and never duplicate. Runs inside the
container; the Dockerfile/startwm can re-run it after image updates.
"""
from pathlib import Path
import re
import sys

WEB_INDEX = Path("/usr/share/selkies/web/index.html")
VOICE_TAG = '<script src="/src/veragensia-voice.js"></script>'
NGINX_CONF = Path("/etc/nginx/conf.d/default.conf")
NGINX_BLOCK = """    location /voice-gateway/ {
        proxy_pass http://127.0.0.1:8900/;
        proxy_read_timeout 30s;
        proxy_set_header Host $host;
    }
"""


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


def patch_nginx():
    conf = NGINX_CONF.read_text(encoding="utf-8")
    lines = conf.split("\n")
    if "/voice-gateway" in conf:
        print("nginx: voice-gateway location already present")
        return 0
    # Insert the location into EVERY server block (the container ships two:
    # the default :3000 server and a secondary), before each block's final "}".
    # Track brace depth from a simple scan; a block ends when depth returns to 0.
    out, depth, inserted = [], 0, 0
    in_server = False
    for line in lines:
        stripped = line.strip()
        if stripped == "server {":
            in_server = True
        if in_server:
            depth += line.count("{") - line.count("}")
            if depth == 0 and in_server:
                out.append(NGINX_BLOCK.rstrip("\n"))
                inserted += 1
                in_server = False
        out.append(line)
    if not inserted:
        print("nginx: no server block anchor found", file=sys.stderr)
        return 1
    NGINX_CONF.write_text("\n".join(out), encoding="utf-8")
    print(f"nginx: voice-gateway location added to {inserted} server block(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(patch_index() | patch_nginx())
