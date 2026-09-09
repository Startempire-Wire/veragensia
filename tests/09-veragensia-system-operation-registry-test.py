#!/usr/bin/env python3
"""Docs/201 V201-S2: semantic system-operation registry contract tests.

Static and behavioral coverage: registry validates against the docs/201 §3
descriptor contract, every V201-S2 first family is covered, the CLI list and
describe projections work, and the CLI never exposes execution (S4 wiring).
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config/system-operations.json"
CLI = ROOT / "scripts/veragens"

_spec = importlib.util.spec_from_file_location(
    "veragens_operations", ROOT / "scripts/veragens-operations.py")
operations = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(operations)


class SystemOperationRegistryTest(unittest.TestCase):
    def test_registry_loads_and_validates(self):
        envelope = operations.load_registry(REGISTRY)
        self.assertEqual(envelope["schema"], operations.CATALOG_SCHEMA)
        self.assertGreaterEqual(len(envelope["operations"]), 9)

    def test_operation_ids_unique_and_namespaced(self):
        envelope = operations.load_registry(REGISTRY)
        ids = [op["operation_id"] for op in envelope["operations"]]
        self.assertEqual(len(ids), len(set(ids)))
        for op_id in ids:
            self.assertTrue(op_id.startswith("system."), op_id)

    def test_all_v201_s2_families_covered(self):
        coverage = operations.family_coverage(REGISTRY)
        gaps = {family: categories for family, categories in coverage.items() if not categories}
        self.assertEqual(gaps, {}, f"V201-S2 families without descriptors: {gaps}")

    def test_sensitive_operations_declare_authority(self):
        envelope = operations.load_registry(REGISTRY)
        flagged = {op["operation_id"]: op["preconditions"]
                   for op in envelope["operations"]
                   if op["risk"]["consequence_class"] in ("medium", "high")}
        self.assertTrue(flagged)
        for op_id, pre in flagged.items():
            self.assertTrue(pre["authority_ref_required"],
                            f"{op_id} medium/high risk must require an authority ref")

    def test_cli_list_projection(self):
        result = subprocess.run([sys.executable, str(CLI), "operation", "list", "--json"],
                                capture_output=True, text=True, timeout=30, check=True)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], "veragensia.system_operation_list.v1")
        self.assertEqual(report["count"], len(report["operations"]))
        self.assertTrue(all(set(op) == {"operation_id", "category", "label",
                                        "owner_runtime", "preferred_adapter"}
                            for op in report["operations"]))

    def test_cli_describe_known_and_unknown(self):
        known = subprocess.run(
            [sys.executable, str(CLI), "operation", "describe", "system.workspace.activate", "--json"],
            capture_output=True, text=True, timeout=30, check=True)
        descriptor = json.loads(known.stdout)
        self.assertEqual(descriptor["operation_id"], "system.workspace.activate")
        self.assertEqual(descriptor["schema"], operations.DESCRIPTOR_SCHEMA)
        unknown = subprocess.run(
            [sys.executable, str(CLI), "operation", "describe", "system.does.not_exist", "--json"],
            capture_output=True, text=True, timeout=30)
        self.assertEqual(unknown.returncode, 2)
        self.assertEqual(json.loads(unknown.stdout)["error"], "unknown_operation")

    def test_cli_s4_execution_subcommands_present(self):
        # S4 has landed: invoke/batch/audit are the execution + audit surface.
        result = subprocess.run([sys.executable, str(CLI), "operation", "--help"],
                                capture_output=True, text=True, timeout=30, check=True)
        for subcommand in ("invoke", "batch", "audit"):
            self.assertIn(subcommand, result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
