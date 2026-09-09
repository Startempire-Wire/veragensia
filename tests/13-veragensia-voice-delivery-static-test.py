#!/usr/bin/env python3
"""Verify restart-safe voice asset/route delivery contracts."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PATCH_PATH = ROOT / "docker/omarchy-demo/overlay/webtop/voice-page-patch.py"
spec = importlib.util.spec_from_file_location("voice_page_patch", PATCH_PATH)
patch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(patch)


class VoiceDeliveryStaticTest(unittest.TestCase):
    def test_patch_copies_asset_and_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.js"
            target = root / "web" / "src" / "veragensia-voice.js"
            index = root / "index.html"
            nginx = root / "default.conf"
            source.write_text("voice-v1", encoding="utf-8")
            index.write_text("<body>demo</body>", encoding="utf-8")
            nginx.write_text(
                "server {\n    listen 3000;\n}\n\n"
                "server {\n    listen 8080;\n}\n",
                encoding="utf-8")
            patch.VOICE_SOURCE = source
            patch.VOICE_TARGET = target
            patch.WEB_INDEX = index
            patch.NGINX_CONF = nginx

            self.assertEqual(patch.patch_asset(), 0)
            self.assertEqual(target.read_text(encoding="utf-8"), "voice-v1")
            self.assertEqual(patch.patch_index(), 0)
            self.assertEqual(patch.patch_nginx(), 0)
            first = nginx.read_text(encoding="utf-8")
            self.assertEqual(first.count("location /voice-gateway/"), 2)

            self.assertEqual(patch.patch_asset(), 0)
            self.assertEqual(patch.patch_index(), 0)
            self.assertEqual(patch.patch_nginx(), 0)
            self.assertEqual(nginx.read_text(encoding="utf-8"), first)

    def test_partial_nginx_patch_is_completed(self):
        with tempfile.TemporaryDirectory() as tmp:
            nginx = Path(tmp) / "default.conf"
            nginx.write_text(
                "server {\n    listen 3000;\n"
                "    location /voice-gateway/ { proxy_pass http://127.0.0.1:8900/; }\n}\n"
                "server {\n    listen 8080;\n}\n",
                encoding="utf-8")
            patch.NGINX_CONF = nginx
            self.assertEqual(patch.patch_nginx(), 0)
            self.assertEqual(nginx.read_text(encoding="utf-8").count("location /voice-gateway/"), 2)

    def test_image_and_supervisor_own_restart_contract(self):
        dockerfile = (ROOT / "docker/omarchy-demo/Dockerfile").read_text(encoding="utf-8")
        loop = (ROOT / "docker/omarchy-demo/overlay/webtop/voice-gateway-loop.sh").read_text(encoding="utf-8")
        swap = (ROOT / "docker/omarchy-demo/omarchy-demo-swap.sh").read_text(encoding="utf-8")
        self.assertIn("COPY --chown=abc:abc docker/omarchy-demo/overlay/selkies-web/veragensia-voice.js /usr/share/selkies/selkies-dashboard/src/veragensia-voice.js", dockerfile)
        self.assertIn("VERAGENSIA_VOICE_INDEX=/usr/share/selkies/selkies-dashboard/index.html", dockerfile)
        self.assertIn("VERAGENSIA_VOICE_NGINX=/defaults/default.conf", dockerfile)
        self.assertIn("veragensia-voice-page-patch.py", dockerfile)
        self.assertIn("while :; do", loop)
        self.assertIn("retrying", loop)
        self.assertIn("archive_existing_previous", swap)
        self.assertIn('docker rename "$PREV" "$archive"', swap)


if __name__ == "__main__":
    unittest.main(verbosity=2)
