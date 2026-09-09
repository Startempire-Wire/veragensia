#!/usr/bin/env python3
"""Docs/201 V201-S3: keybinding parity compiler contract tests.

Covers the §4.2 classification gate, chord rendering, invariant 2 (operation
identity is chord-independent), invariant 8 (drift detection), the CLI path,
and the defect posture of unmapped_gap.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts/veragens"
PARITY = ROOT / "scripts/veragens-keymap-parity.py"

_spec = importlib.util.spec_from_file_location("veragens_keymap_parity", PARITY)
parity = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(parity)

RULES = parity.load_rules()

FOOT_DEMO_DIGEST = "7442729aadb77c95048605246869656ce799ba65d8ed5150100676d5f273b7ad"


def inventory(items, runtime="demo-runtime"):
    return {"schema": "veragensia.omarchy_inventory.v1", "runtime_ref": runtime,
            "sources": {"hyprland_bindings": {"status": "ok", "total": len(items), "items": items}}}


class KeybindingParityTest(unittest.TestCase):
    def test_demo_bindings_classify_to_semantic_operations(self):
        items = [
            {"modmask": 64, "key": "Return", "keycode": 0, "dispatcher": "exec",
             "argument_sha256": FOOT_DEMO_DIGEST},
            {"modmask": 64, "key": "q", "keycode": 0, "dispatcher": "killactive",
             "argument_sha256": None},
            {"modmask": 64, "key": "f", "keycode": 0, "dispatcher": "fullscreen",
             "argument_sha256": None},
            {"modmask": 65, "key": "q", "keycode": 0, "dispatcher": "exit",
             "argument_sha256": None},
        ]
        report = parity.compile_projection(inventory(items), RULES)
        by_op = {r["operation_ref"]: r for r in report["records"] if r["operation_ref"]}
        self.assertEqual(by_op["system.app.launch.terminal"]["classification"], "semantic_operation")
        self.assertEqual(by_op["system.window.close"]["key_chord"], "SUPER + Q")
        self.assertEqual(by_op["system.session.exit"]["key_chord"], "SUPER + SHIFT + Q")
        self.assertEqual(report["unmapped_gap_count"], 0)
        self.assertEqual(report["classified_total"], 4)

    def test_classification_gate_unmapped_and_non_semantic(self):
        items = [
            {"modmask": 64, "key": "x", "keycode": 0, "dispatcher": "unknown_dispatcher",
             "argument_sha256": None},
            {"modmask": 64, "key": "y", "keycode": 0, "dispatcher": "exec",
             "argument_sha256": "b" * 64},
        ]
        report = parity.compile_projection(inventory(items), RULES)
        classes = [r["classification"] for r in report["records"]]
        self.assertEqual(classes, ["unmapped_gap", "application_internal"])
        self.assertEqual(report["unmapped_gap_count"], 1)
        self.assertTrue(report["unmapped_gap_is_release_defect"])

    def test_invariant_2_operation_identity_is_chord_independent(self):
        base = {"keycode": 0, "dispatcher": "killactive", "argument_sha256": None}
        items = [dict(base, modmask=64, key="q"), dict(base, modmask=8, key="w")]
        report = parity.compile_projection(inventory(items), RULES)
        refs = {r["operation_ref"] for r in report["records"]}
        self.assertEqual(refs, {"system.window.close"})
        self.assertEqual(len({r["key_chord"] for r in report["records"]}), 2)

    def test_invariant_8_drift_detection(self):
        items = [
            {"modmask": 64, "key": "q", "keycode": 0, "dispatcher": "killactive",
             "argument_sha256": None},
        ]
        first = parity.compile_projection(inventory(items), RULES, observed_at="t1")
        changed = parity.compile_projection(inventory([
            {"modmask": 64, "key": "w", "keycode": 0, "dispatcher": "killactive",
             "argument_sha256": None},
        ]), RULES, observed_at="t2")
        drifted = parity.diff_projection(changed, first)
        self.assertTrue(drifted["projection_drift"])
        self.assertEqual(len(drifted["drift"]["removed"]), 1)
        self.assertEqual(len(drifted["drift"]["added"]), 1)
        unchanged = parity.diff_projection(
            parity.compile_projection(inventory(items), RULES, observed_at="t2"), first)
        self.assertFalse(unchanged["projection_drift"])

    def test_chord_rendering_order_matches_docs_style(self):
        self.assertEqual(parity.key_chord(64, "Return"), "SUPER + RETURN")
        self.assertEqual(parity.key_chord(65, "q"), "SUPER + SHIFT + Q")
        self.assertEqual(parity.key_chord(0, "F5"), "F5")

    def test_rules_validation_rejects_bad_input(self):
        bad = Path(self.enterContext(_tempdir())) / "rules.json"
        bad.write_text(json.dumps({"schema": "veragensia.keybinding_projection_rules.v1",
                                   "rules": [{"operation_id": "x", "match": {}}]}))
        with self.assertRaises(ValueError):
            parity.load_rules(bad)

    def test_cli_inspect_end_to_end(self):
        fixture = self.enterContext(_tempdir()) / "inv.json"
        items = [{"modmask": 64, "key": "q", "keycode": 0, "dispatcher": "killactive",
                  "argument_sha256": None}]
        fixture.write_text(json.dumps(inventory(items)))
        result = subprocess.run([sys.executable, str(CLI), "keymap", "inspect", "--json",
                                 "--inventory", str(fixture)],
                                capture_output=True, text=True, timeout=30, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], parity.PROJECTION_SCHEMA)
        self.assertEqual(report["records"][0]["operation_ref"], "system.window.close")


from contextlib import contextmanager
import tempfile


@contextmanager
def _tempdir():
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


if __name__ == "__main__":
    unittest.main(verbosity=2)
