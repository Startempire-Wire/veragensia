#!/usr/bin/env python3
"""Voice gateway matcher + lineage tests (docs/201 T2 preview slice)."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "voice_gateway", ROOT / "docker/omarchy-demo/overlay/webtop/voice-gateway.py")
gateway = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gateway)

_audit_spec = importlib.util.spec_from_file_location(
    "veragens_audit", ROOT / "scripts/veragens-audit.py")
audit = importlib.util.module_from_spec(_audit_spec)
_audit_spec.loader.exec_module(audit)

REGISTRY = gateway.operations.load_registry()


class VoiceMatcherTest(unittest.TestCase):
    def test_parameterized_workspace_and_directions(self):
        for text, op, args in (
            ("go to workspace 3", "system.workspace.activate", ["3"]),
            ("switch to workspace number 2", "system.workspace.activate", ["2"]),
            ("move focus left", "system.window.focus_direction", ["l"]),
            ("focus right", "system.window.focus_direction", ["r"]),
            ("move this window up", "system.window.move_direction", ["u"]),
        ):
            matched = gateway.match_operation(text, REGISTRY)
            self.assertEqual(matched[0], op, text)
            self.assertEqual(matched[1], args, text)
            self.assertEqual(matched[2], "parameterized")

    def test_voice_examples_match_without_parameters(self):
        for text, op in (
            ("close this window", "system.window.close"),
            ("make this fullscreen", "system.window.fullscreen"),
            ("take it out of fullscreen", "system.window.fullscreen"),
            ("make this window float", "system.window.toggle_floating"),
            ("show the scratchpad", "system.workspace.toggle_special"),
        ):
            matched = gateway.match_operation(text, REGISTRY)
            self.assertEqual(matched[0], op, text)
            self.assertEqual(matched[2], "voice_example", text)

    def test_unmatched_transcript(self):
        self.assertIsNone(gateway.match_operation("tell me a joke", REGISTRY))

    def test_handle_command_unmatched_is_ledgered(self):
        with tempfile.TemporaryDirectory() as tmp:
            def fake_runner(argv):
                return {"status": "ok", "exit_code": 0}, b""
            outcome = gateway.handle_command("tell me a joke", REGISTRY, audit_dir=tmp,
                                             runner=fake_runner)
            self.assertFalse(outcome["matched"])
            report = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            self.assertEqual(report["entries"][-1]["match_method"], "unmatched")

    def test_handle_command_full_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}
            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"
            outcome = gateway.handle_command(
                "go to workspace 2", REGISTRY, audit_dir=tmp,
                actor="voice-test", runner=fake_runner)
            self.assertTrue(outcome["matched"])
            self.assertEqual(outcome["status"], "ok")
            transcriptions = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = transcriptions["entries"][-1]
            self.assertEqual(entry["matched_operation_id"], "system.workspace.activate")
            self.assertEqual(entry["engine"], "web-speech-api")
            self.assertIsNotNone(entry["action_audit_seq"])
            operations_ledger = audit.tail(Path(tmp) / audit.OPERATIONS_LEDGER, verify=True)
            self.assertEqual(operations_ledger["broken"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
