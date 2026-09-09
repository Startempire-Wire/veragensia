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
    if "/voice-gateway" in conf:
        print("nginx: voice-gateway location already present")
        return 0
    # Insert before the final closing brace of the outer server block.
    match = None
    for match in re.finditer(r"\n}", conf):
        pass
    if match is None:
        print("nginx: no closing brace anchor found", file=sys.stderr)
        return 1
    patched = conf[:match.start()] + "\n" + NGINX_BLOCK + conf[match.start():]
    NGINX_CONF.write_text(patched, encoding="utf-8")
    print("nginx: voice-gateway location added")
    return 0


if __name__ == "__main__":
    raise SystemExit(patch_index() | patch_nginx())
