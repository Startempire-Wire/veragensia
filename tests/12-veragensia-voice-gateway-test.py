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
            outcome = gateway.handle_command(
                "tell me a joke", REGISTRY, audit_dir=tmp, runner=fake_runner,
                intent_fn=lambda t, r: None)
            self.assertFalse(outcome["matched"])
            self.assertEqual(outcome["reason"], "llm_unmatched")
            self.assertIn("hint", outcome)
            report = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = report["entries"][-1]
            self.assertEqual(entry["match_method"], "unmatched")
            self.assertIsNotNone(entry["intent_engine"])

    def test_llm_intent_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}
            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"

            def natural(transcript, expected_args):
                def fn(_t, _r):
                    return {"operation_id": "system.workspace.activate",
                            "args": expected_args, "confidence": 0.97}
                return gateway.handle_command(
                    transcript, REGISTRY, audit_dir=tmp, runner=fake_runner,
                    intent_fn=fn)

            outcome = natural("can you put me on the third workspace please", ["3"])
            self.assertTrue(outcome["matched"])
            self.assertEqual(outcome["match_method"], "llm")
            self.assertEqual(outcome["status"], "ok")
            self.assertEqual(outcome["intent_confidence"], 0.97)

            outcome = natural("hey so um switch me over to workspace 5 thanks", ["5"])
            self.assertEqual(outcome["operation_id"], "system.workspace.activate")

            transcriptions = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = transcriptions["entries"][-1]
            self.assertEqual(entry["match_method"], "llm")
            self.assertEqual(entry["intent_engine"], gateway.INTENT_ENGINE)
            self.assertEqual(entry["intent_confidence"], 0.97)
            self.assertIsNotNone(entry["action_audit_seq"])
            ledger = audit.tail(Path(tmp) / audit.OPERATIONS_LEDGER, verify=True)
            self.assertEqual(ledger["broken"], [])

    def test_llm_down_falls_back_to_regex(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}
            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"
            def broken_fn(_t, _r):
                raise OSError("proxy unreachable")
            outcome = gateway.handle_command(
                "go to workspace 2", REGISTRY, audit_dir=tmp, runner=fake_runner,
                intent_fn=broken_fn)
            self.assertTrue(outcome["matched"])
            self.assertEqual(outcome["match_method"], "regex_fallback")

    def test_parse_intent_text(self):
        parsed = gateway.parse_intent_text(
            '```json\n{"operation_id":"system.workspace.activate",'
            '"args":[3],"confidence":0.9}\n```')
        self.assertEqual(parsed["operation_id"], "system.workspace.activate")
        self.assertEqual(parsed["args"], ["3"])
        self.assertEqual(parsed["confidence"], 0.9)
        self.assertIsNone(gateway.parse_intent_text("no json here"))
        self.assertIsNone(gateway.parse_intent_text('{"operation_id":123}').get("x")) if False else None
        junk = gateway.parse_intent_text('{"operation_id":null,"args":"x","confidence":"high"}')
        self.assertIsNone(junk["operation_id"])
        self.assertEqual(junk["args"], [])
        self.assertEqual(junk["confidence"], 0.0)

    def test_handle_command_batch_lineage_and_origin_ref(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}

            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"

            intents = [
                {"operation_id": "system.workspace.activate", "args": ["3"],
                 "confidence": 0.91},
                {"operation_id": "system.window.resize_active", "args": ["40", "0"],
                 "confidence": 0.87},
            ]
            outcome = gateway.handle_command(
                "put me on workspace 3 and make the window wider", REGISTRY,
                audit_dir=tmp, actor="voice-test", runner=fake_runner,
                intent_fn=lambda t, r: intents)
            self.assertTrue(outcome["matched"])
            self.assertEqual(outcome["batch_size"], 2)
            self.assertEqual(outcome["batch_outcome"], "completed")
            self.assertEqual(outcome["batch"][0]["status"], "ok")
            transcriptions = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = transcriptions["entries"][-1]
            self.assertEqual(entry["matched_operation_id"], "system.workspace.activate")
            self.assertEqual(entry["batch_size"], 2)
            self.assertIsNotNone(entry["action_audit_seq"])
            utterance_ref = "veragensia:transcriptions:{}".format(entry["seq"])
            operations_ledger = audit.tail(
                Path(tmp) / audit.OPERATIONS_LEDGER, verify=True)
            self.assertEqual(operations_ledger["broken"], [])
            extra = [e for e in operations_ledger["entries"]
                     if e.get("origin_utterance_ref")]
            self.assertEqual(len(extra), 1)
            self.assertEqual(extra[0]["operation_id"], "system.window.resize_active")
            self.assertEqual(extra[0]["origin_utterance_ref"], utterance_ref)
            # the first op keeps the transcription->audit link
            self.assertEqual(entry["action_audit_seq"],
                             operations_ledger["entries"][-2]["seq"])

    def test_handle_command_batch_refusal_is_independent_and_audited(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}

            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"

            intents = [
                {"operation_id": "system.workspace.activate", "args": ["2"],
                 "confidence": 0.9},
                {"operation_id": "system.session.exit", "args": [],
                 "confidence": 0.9},
            ]
            outcome = gateway.handle_command(
                "switch to workspace 2 then log out", REGISTRY,
                audit_dir=tmp, actor="voice-test", runner=fake_runner,
                intent_fn=lambda t, r: intents)
            self.assertEqual(outcome["status"], "ok")
            self.assertEqual(outcome["batch_outcome"], "failed")
            refused = outcome["batch"][0]
            self.assertTrue(refused["authority_required"])
            self.assertEqual(refused["error"], "authority_required")
            operations_ledger = audit.tail(
                Path(tmp) / audit.OPERATIONS_LEDGER, verify=True)
            self.assertEqual(operations_ledger["broken"], [])
            refused_entries = [e for e in operations_ledger["entries"]
                               if e.get("operation_id") == "system.session.exit"]
            self.assertEqual(len(refused_entries), 1)
            self.assertEqual(refused_entries[0]["status"], "refused")
            self.assertTrue(refused_entries[0].get("origin_utterance_ref", "")
                            .startswith("veragensia:transcriptions:"))

    def test_handle_command_full_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = {"activeworkspace": {"id": 1}, "activewindow": {"class": "foot"}}
            def fake_runner(argv):
                if argv[1] == "-j":
                    return {"status": "ok", "exit_code": 0}, json.dumps(state).encode()
                return {"status": "ok", "exit_code": 0}, b"ok"
            outcome = gateway.handle_command(
                "go to workspace 2", REGISTRY, audit_dir=tmp,
                actor="voice-test", confidence=0.83, audio_duration_ms=1200,
                runner=fake_runner)
            self.assertTrue(outcome["matched"])
            self.assertEqual(outcome["status"], "ok")
            self.assertEqual(outcome["confidence"], 0.83)
            self.assertEqual(outcome["audio_duration_ms"], 1200)
            transcriptions = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = transcriptions["entries"][-1]
            self.assertEqual(entry["matched_operation_id"], "system.workspace.activate")
            self.assertEqual(entry["engine"], "web-speech-api")
            self.assertEqual(entry["confidence"], 0.83)
            self.assertEqual(entry["audio_duration_ms"], 1200)
            self.assertIsNotNone(entry["action_audit_seq"])
            operations_ledger = audit.tail(Path(tmp) / audit.OPERATIONS_LEDGER, verify=True)
            self.assertEqual(operations_ledger["broken"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
