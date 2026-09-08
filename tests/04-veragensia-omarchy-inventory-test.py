#!/usr/bin/env python3
"""Synthetic V201-S1 consumer, privacy, and process-boundary checks."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/veragens-omarchy-inventory.py"
spec = importlib.util.spec_from_file_location("inventory", SCRIPT)
inv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(inv)


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)

    def fixture(self, name, body):
        path = self.home / name
        path.write_text(f"#!{sys.executable}\n{body}\n")
        path.chmod(0o700)
        return str(path)

    @staticmethod
    def good(argv):
        if argv[0] == "omarchy":
            return {"status": "ok"}, b'{"commands":[{"name":"launch browser","token":"SECRET"}]}'
        if argv[0] == "hyprctl":
            return {"status": "ok"}, b'[{"key":"B","modmask":64,"dispatcher":"exec","arg":"SECRET","description":"SECRET"}]'
        return {"status": "ok"}, b"browser.desktop\n"

    def test_inventory_redacts_private_content_and_never_qualifies(self):
        p = self.home / ".config/hypr/bindings.lua"
        p.parent.mkdir(parents=True)
        p.write_text("SECRET")
        with patch.dict(os.environ, {"HYPRLAND_INSTANCE_SIGNATURE": "PRIVATE_SESSION"}):
            result = inv.inventory(self.home, self.good)
        self.assertEqual(result["status"], "observed")
        self.assertEqual(result["qualification"], "not_performed")
        self.assertNotIn("SECRET", json.dumps(result))
        self.assertNotIn("PRIVATE_SESSION", json.dumps(result))
        self.assertEqual(p.read_text(), "SECRET")
        self.assertFalse(result["sources"]["user_overrides"]["content_included"])

    def test_missing_runtime_cannot_report_observed(self):
        with patch.dict(os.environ, {}, clear=True):
            result = inv.inventory(self.home, self.good)
        self.assertEqual(result["status"], "degraded")
        self.assertIsNone(result["runtime_ref"])

    def test_missing_tools(self):
        with patch.dict(os.environ, {"PATH": ""}):
            self.assertEqual(inv.probe(["omarchy"]), ({"status": "unavailable"}, b""))

    def test_bad_json_and_schema(self):
        for raw, expected in [(b"not json", "invalid_json"), (b"{}", "unsupported_schema"),
                              (b'[{"token":"SECRET"}]', "incomplete")]:
            with self.subTest(raw=raw):
                self.assertEqual(inv.commands(lambda _: ({"status": "ok"}, raw))["status"], expected)

    def test_upstream_registry_preserves_full_route(self):
        raw = b'{"ok":true,"commands":[{"route":"launch browser","name":"browser","group":"launch","binary":"omarchy-launch-browser","args":"SECRET"}]}'
        result = inv.commands(lambda _: ({"status": "ok"}, raw))
        self.assertEqual(result["items"], [{"name": "launch browser"}])
        self.assertNotIn("SECRET", json.dumps(result))

    def test_binding_schema_and_field_types(self):
        data = [{"dispatcher": "exec", "key": "X", "modmask": True, "keycode": -1}]
        result = inv.bindings(lambda _: ({"status": "ok"}, json.dumps(data).encode()))
        self.assertNotIn("modmask", result["items"][0])
        self.assertNotIn("keycode", result["items"][0])
        invalid = inv.bindings(lambda _: ({"status": "ok"}, b'{"unexpected":[]}'))
        self.assertEqual(invalid["status"], "unsupported_schema")

    def test_item_cap_is_explicit(self):
        raw = json.dumps(["launch browser"] * (inv.MAX_ITEMS + 1)).encode()
        result = inv.commands(lambda _: ({"status": "ok"}, raw))
        self.assertEqual(len(result["items"]), inv.MAX_ITEMS)
        self.assertTrue(result["truncated"])
        with patch.dict(os.environ, {"HYPRLAND_INSTANCE_SIGNATURE": "synthetic"}):
            result = inv.inventory(self.home, lambda argv: ({"status": "ok"}, raw) if argv[0] == "omarchy" else self.good(argv))
        self.assertEqual(result["status"], "degraded")

    def test_nonzero_exit_has_no_stderr_payload(self):
        executable = self.fixture("error", "import sys; print('SECRET', file=sys.stderr); sys.exit(7)")
        state, raw = inv.probe([executable])
        self.assertEqual(state, {"status": "error", "exit_code": 7})
        self.assertEqual(raw, b"")

    def test_oversized_stdout_and_stderr(self):
        for target in ("stdout", "stderr"):
            with self.subTest(target=target):
                executable = self.fixture("large", f"import sys; print('x'*10000, file=sys.{target})")
                state, raw = inv.probe([executable], max_bytes=100)
                self.assertEqual(state["status"], "oversized")
                self.assertEqual(raw, b"")

    def test_timeout_with_open_and_closed_pipes(self):
        for close in (False, True):
            with self.subTest(close=close):
                body = "import os,time\n"
                if close:
                    body += "os.close(1); os.close(2)\n"
                executable = self.fixture("slow", body + "time.sleep(10)")
                state, raw = inv.probe([executable], timeout=0.1)
                self.assertEqual(state["status"], "timeout")
                self.assertEqual(raw, b"")

    def test_override_file_boundaries(self):
        p = self.home / ".config/hypr/bindings.lua"
        p.parent.mkdir(parents=True)
        p.write_bytes(b"x" * (inv.MAX_BYTES + 1))
        self.assertEqual(inv.override_metadata(self.home)["status"], "oversized")
        p.unlink()
        p.symlink_to(self.home / "missing")
        self.assertEqual(inv.override_metadata(self.home)["status"], "unreadable")
        p.unlink()
        os.mkfifo(p)
        self.assertEqual(inv.override_metadata(self.home)["status"], "unsupported_file_type")

    def test_invalid_desktop_default_is_not_disclosed(self):
        result = inv.defaults(lambda _: ({"status": "ok"}, b"SECRET=/private/path"))
        self.assertEqual(result["status"], "incomplete")
        self.assertNotIn("SECRET", json.dumps(result))

    def test_cli_consumer_success(self):
        # Upstream parse_commands_args gives --check precedence over --json.
        self.fixture("omarchy", "import json,sys\nassert sys.argv[1:3]==['commands','--all']\nif '--check' in sys.argv: print('Command registry valid')\nelse: print(json.dumps({'ok':True,'commands':[{'route':'launch browser','name':'browser','group':'launch'}]}))")
        self.fixture("hyprctl", "import json,sys\nassert sys.argv[1:]==['-j','binds']\nprint(json.dumps([{'key':'B','dispatcher':'exec','arg':'SECRET'}]))")
        self.fixture("xdg-mime", "import sys\nassert sys.argv[1:3]==['query','default']\nprint('browser.desktop')")
        env = {**os.environ, "HOME": str(self.home), "PATH": str(self.home),
               "HYPRLAND_INSTANCE_SIGNATURE": "synthetic"}
        result = subprocess.run([sys.executable, str(SCRIPT), "--require-complete"], env=env,
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], inv.SCHEMA)
        self.assertEqual(report["status"], "observed")
        self.assertEqual(report["sources"]["omarchy_commands"]["items"], [{"name": "launch browser"}])
        self.assertNotIn(b"SECRET", result.stdout)

    def test_cli_consumer_missing_runtime(self):
        env = {**os.environ, "HOME": str(self.home), "PATH": "", "HYPRLAND_INSTANCE_SIGNATURE": ""}
        result = subprocess.run([sys.executable, str(SCRIPT), "--require-complete"], env=env,
                                capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(json.loads(result.stdout)["status"], "degraded")


if __name__ == "__main__":
    unittest.main()
