#!/usr/bin/env python3
"""V201-S4 execution + audit contract tests.

Covers the hyprland_dispatch adapter (mock runner), authority gating, argument
validation, read-verified dispatch snapshots, fenced batches, and the
tamper-evident audit/transcription ledgers including refusal auditing.
"""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location(
    "veragens_operations_exec", ROOT / "scripts/veragens-operations-exec.py")
executor = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(executor)

_audit_spec = importlib.util.spec_from_file_location(
    "veragens_audit", ROOT / "scripts/veragens-audit.py")
audit = importlib.util.module_from_spec(_audit_spec)
_audit_spec.loader.exec_module(audit)

_ops_spec = importlib.util.spec_from_file_location(
    "veragens_operations", ROOT / "scripts/veragens-operations.py")
operations = importlib.util.module_from_spec(_ops_spec)
_ops_spec.loader.exec_module(operations)

BINDINGS = executor.load_execution()
DESCRIBE = operations.describe


def fake_runner(responses):
    """Runner returning canned hyprctl -j JSON and ok exits for dispatch."""
    calls = []

    def run(argv):
        calls.append(argv)
        if argv[1] == "-j":
            return {"status": "ok", "exit_code": 0}, json.dumps(responses.get(argv[2], {})).encode()
        return {"status": "ok", "exit_code": 0}, b"ok"
    return run, calls


class OperationExecutionTest(unittest.TestCase):
    def test_low_risk_dispatch_with_state_snapshots(self):
        run, calls = fake_runner({"activewindow": {"class": "foot", "pid": 7}})
        result = executor.invoke("system.window.focus_direction", ["r"],
                                 registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["dispatcher"], "movefocus")
        self.assertEqual(result["before"]["activewindow"]["class"], "foot")
        self.assertIn(["hyprctl", "dispatch", "movefocus", "r"], calls)
        self.assertIn("after", result)

    def test_authority_gate_refuses_medium_high_without_ref(self):
        run, _ = fake_runner({})
        result = executor.invoke("system.window.close", [],
                                 registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(result["status"], "refused")
        self.assertEqual(result["error"], "authority_required")
        self.assertEqual(result["consequence_class"], "medium")

    def test_authority_gate_accepts_with_ref(self):
        run, calls = fake_runner({"activewindow": {"class": "foot"}})
        result = executor.invoke("system.window.close", [], authority_ref="demo-operator",
                                 registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(result["status"], "ok")
        self.assertTrue(result["authority_ref_present"])

    def test_unknown_operation_and_adapter(self):
        run, _ = fake_runner({})
        unknown = executor.invoke("system.does.not_exist", [], registry_describe=DESCRIBE,
                                  bindings=BINDINGS, runner=run)
        self.assertEqual(unknown["error"], "unknown_operation")
        unbound = executor.invoke("system.audio.output.mute_toggle", [],
                                  registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(unbound["error"], "adapter_unavailable")

    def test_argument_validation(self):
        run, _ = fake_runner({})
        bad = executor.invoke("system.window.focus_direction", ["../evil"],
                              registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(bad["error"], "invalid_arguments")
        none_op = executor.invoke("system.window.toggle_floating", ["extra"],
                                  registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(none_op["error"], "invalid_arguments")
        fixed = executor.invoke("system.workspace.toggle_special", ["magic"],
                                registry_describe=DESCRIBE, bindings=BINDINGS, runner=run)
        self.assertEqual(fixed["status"], "ok")
        self.assertEqual(fixed["dispatch_args"], ["magic"])

    def test_fenced_batch_and_cap(self):
        run, calls = fake_runner({"activewindow": {}})
        with tempfile.TemporaryDirectory() as tmp:
            fence = Path(tmp) / "fence"
            steps = [{"operation_id": "system.window.focus_direction", "args": ["r"]},
                     {"operation_id": "system.window.toggle_floating"}]
            fence.write_text("stop")
            fenced = executor.batch(steps, registry_describe=DESCRIBE, bindings=BINDINGS,
                                    runner=run, fence_path=fence)
            self.assertEqual(fenced["outcome"], "fenced")
            self.assertEqual(fenced["executed"], 0)
            fence.unlink()
            ran = executor.batch(steps, registry_describe=DESCRIBE, bindings=BINDINGS,
                                 runner=run, fence_path=fence)
            self.assertEqual(ran["outcome"], "completed")
            self.assertEqual(ran["executed"], 2)
            self.assertEqual(len(calls), 4 + 2)  # snapshots + dispatches


class AuditLedgerTest(unittest.TestCase):
    def _dir(self):
        return tempfile.TemporaryDirectory()

    def test_hash_chain_and_tamper_detection(self):
        with self._dir() as tmp:
            ledger = Path(tmp) / "ops.jsonl"
            first = audit.append(ledger, {"kind": "operation", "operation_id": "a"})
            second = audit.append(ledger, {"kind": "operation", "operation_id": "b"})
            self.assertEqual(first["status"], "ok")
            self.assertEqual(second["prev_hash"], first["entry_hash"])
            report = audit.tail(ledger, verify=True)
            self.assertEqual(report["broken"], [])
            self.assertEqual(report["total"], 2)
            entries = report["entries"]
            tampered = json.loads((ledger).read_text().splitlines()[0])
            tampered["operation_id"] = "tampered"
            lines = (ledger).read_text().splitlines()
            lines[0] = json.dumps(tampered, sort_keys=True, separators=(",", ":"))
            (ledger).write_text("\n".join(lines) + "\n")
            report = audit.tail(ledger, verify=True)
            self.assertEqual(len(report["broken"]), 1)
            self.assertEqual(report["broken"][0]["reason"], "hash_mismatch")

    def test_refusals_are_audited(self):
        with self._dir() as tmp:
            run, _ = fake_runner({})
            result = executor.invoke("system.window.close", [], registry_describe=DESCRIBE,
                                     bindings=BINDINGS, runner=run, audit_dir=tmp)
            self.assertEqual(result["audit_write"], "ok")
            report = audit.tail(Path(tmp) / audit.OPERATIONS_LEDGER)
            self.assertEqual(report["entries"][-1]["status"], "refused")
            self.assertEqual(report["entries"][-1]["operation_id"], "system.window.close")

    def test_transcription_lineage(self):
        with self._dir() as tmp:
            run, _ = fake_runner({})
            action = executor.invoke("system.window.toggle_floating", [],
                                     registry_describe=DESCRIBE, bindings=BINDINGS,
                                     runner=run, audit_dir=tmp)
            transcript = audit.record_transcription(
                tmp, "make this window float", "whisper-tiny.en", "voice-daemon",
                confidence=0.91, matched_operation_id="system.window.toggle_floating",
                match_method="voice_example", audio_duration_ms=1200,
                action_audit_seq=action["audit_seq"])
            self.assertEqual(transcript["status"], "ok")
            report = audit.tail(Path(tmp) / audit.TRANSCRIPTIONS_LEDGER)
            entry = report["entries"][-1]
            self.assertEqual(entry["matched_operation_id"], "system.window.toggle_floating")
            self.assertEqual(entry["action_audit_seq"], action["audit_seq"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
