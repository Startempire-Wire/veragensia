#!/usr/bin/env python3
"""Scope-preserving CLI continuation reads; never execution resumption."""
import copy
import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/veragens"
api = runpy.run_path(str(SCRIPT))


class ResumeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "project with spaces"
        self.root.mkdir()
        self.continuity = "synthetic-continuity"
        self.packet = {"schema_version": "focusa.workpoint_resume_packet.v2", "status": "completed",
                       "canonical": True, "degraded": False,
                       "resume_packet": {"project_root": str(self.root), "continuity_id": self.continuity,
                                         "canonical": True, "mission": "synthetic", "next_slice": "read only"}}

    def runner(self, packet):
        return lambda argv: ({"status": "ok"}, json.dumps(packet).encode())

    def fixture(self, body):
        path = Path(self.temp.name) / "focusa"
        path.write_text(f"#!{sys.executable}\n{body}\n")
        path.chmod(0o700)

    def test_transparent_canonical_reply_and_exact_argv(self):
        calls = []
        def runner(argv):
            calls.append(argv)
            return {"status": "ok"}, json.dumps(self.packet).encode()
        report, code = api["resume"](str(self.root), self.continuity, runner)
        self.assertEqual(code, 0)
        self.assertEqual(report, self.packet)
        self.assertEqual(calls, [["focusa", "workpoint", "resume", f"--project-root={self.root}",
                                 f"--continuity-id={self.continuity}", "--json"]])

    def test_explicit_local_scope_is_required_before_probe(self):
        def forbidden(argv):
            self.fail("probe must not run without explicit local scope")
        for root, continuity in [("relative", self.continuity), (str(self.root), " "),
                                 (str(self.root / "missing"), self.continuity)]:
            with self.subTest(root=root):
                report, code = api["resume"](root, continuity, forbidden)
                self.assertEqual(code, 2)
                self.assertEqual(report["reason"], "explicit_local_scope_required")

    def test_foreign_packet_not_disclosed(self):
        for field, value in [("project_root", "/foreign"), ("continuity_id", "foreign")]:
            packet = copy.deepcopy(self.packet)
            packet["resume_packet"].update({field: value, "mission": "PRIVATE_FOREIGN_MISSION"})
            report, code = api["resume"](str(self.root), self.continuity, self.runner(packet))
            self.assertEqual(code, 2)
            self.assertEqual(report["reason"], "focusa_scope_mismatch")
            self.assertNotIn("PRIVATE_FOREIGN_MISSION", json.dumps(report))

    def test_noncanonical_and_contradictory_replies_are_unavailable(self):
        for field, value in [("canonical", False), ("degraded", True), ("status", "blocked")]:
            packet = copy.deepcopy(self.packet)
            packet[field] = value
            self.assertEqual(api["resume"](str(self.root), self.continuity, self.runner(packet))[1], 2)
        packet = copy.deepcopy(self.packet)
        packet["resume_packet"]["canonical"] = False
        self.assertEqual(api["resume"](str(self.root), self.continuity, self.runner(packet))[1], 2)

    def test_unknown_schema_and_invalid_json(self):
        packet = copy.deepcopy(self.packet)
        packet["schema_version"] = "focusa.workpoint_resume_packet.v99"
        report, code = api["resume"](str(self.root), self.continuity, self.runner(packet))
        self.assertEqual((report["reason"], code), ("unsupported_focusa_reply", 2))
        report, code = api["resume"](str(self.root), self.continuity,
                                    lambda argv: ({"status": "ok"}, b"PRIVATE_NOT_JSON"))
        self.assertEqual((report["reason"], code), ("focusa_invalid_json", 2))
        self.assertNotIn("PRIVATE_NOT_JSON", json.dumps(report))

    def test_missing_focusa_and_process_errors(self):
        with patch.dict(os.environ, {"PATH": ""}):
            report, code = api["resume"](str(self.root), self.continuity)
        self.assertEqual((report["reason"], code), ("focusa_unavailable", 2))
        self.fixture("import sys; print('PRIVATE_STDERR', file=sys.stderr); sys.exit(7)")
        with patch.dict(os.environ, {"PATH": self.temp.name}):
            report, code = api["resume"](str(self.root), self.continuity)
        self.assertEqual((report["reason"], code), ("focusa_error", 2))
        self.assertEqual(report["exit_code"], 7)
        self.assertNotIn("PRIVATE_STDERR", json.dumps(report))

    def test_bounded_timeout_and_oversized_reply(self):
        module = api["inventory_module"]()
        for body, expected in [("import time; time.sleep(10)", "focusa_timeout"),
                               ("print('x'*300000)", "focusa_oversized")]:
            self.fixture(body)
            with patch.dict(os.environ, {"PATH": self.temp.name}):
                report, code = api["resume"](str(self.root), self.continuity,
                                            lambda argv: module.probe(argv, timeout=0.1))
            self.assertEqual((report["reason"], code), (expected, 2))

    def test_cli_arguments_are_data_not_shell_commands(self):
        sentinel = Path(self.temp.name) / "executed"
        continuity = f"stream; touch {sentinel}"
        packet = copy.deepcopy(self.packet)
        packet["resume_packet"]["continuity_id"] = continuity
        expected = ["workpoint", "resume", f"--project-root={self.root}", f"--continuity-id={continuity}", "--json"]
        self.fixture(f"import json,sys\nassert sys.argv[1:]=={expected!r}\nprint(json.dumps({packet!r}))")
        scripts = Path(self.temp.name) / "cli/scripts"
        scripts.mkdir(parents=True)
        shutil.copy2(SCRIPT, scripts / "veragens")
        shutil.copy2(ROOT / "scripts/veragens-omarchy-inventory.py", scripts)
        env = {**os.environ, "PATH": self.temp.name}
        env.pop("PYTHONDONTWRITEBYTECODE", None)
        result = subprocess.run([sys.executable, str(scripts / "veragens"), "resume", "--project-root", str(self.root),
                                 "--continuity-id", continuity], env=env, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), packet)
        self.assertFalse(sentinel.exists())
        self.assertFalse((scripts / "__pycache__").exists())

    def test_cli_does_not_infer_scope(self):
        result = subprocess.run([sys.executable, str(SCRIPT), "resume"], capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--project-root", result.stderr)
        self.assertIn(b"--continuity-id", result.stderr)


if __name__ == "__main__":
    unittest.main()
