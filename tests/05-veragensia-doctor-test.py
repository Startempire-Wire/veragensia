#!/usr/bin/env python3
"""Candidate data never substitutes for native release proof."""
import copy
import hashlib
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/veragens"
api = runpy.run_path(str(SCRIPT))


class DoctorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / "candidate.json"
        self.candidate = json.loads((ROOT / "config/v0.1-release-candidate.json").read_text())
        version_stub = patch.dict(api["doctor"].__globals__, {
            "focusa_cli_version": lambda: {"status": "unavailable", "version": None}})
        version_stub.start()
        self.addCleanup(version_stub.stop)

    def write(self, value):
        self.path.write_text(json.dumps(value))

    def test_current_candidate_reports_existing_gaps(self):
        self.write(self.candidate)
        result = api["manifest_gaps"](self.path)
        self.assertEqual(result["status"], "gaps_found")
        fields = {g["field"] for g in result["gaps"]}
        self.assertIn("platform.omarchy_version", fields)
        self.assertIn("native_artifacts.installer_revision", fields)
        self.assertIn("required_gates.G13", fields)

    def test_missing_invalid_oversized_and_unknown_schema(self):
        self.assertEqual(api["manifest_gaps"](self.path)["status"], "missing")
        self.path.write_text("not-json")
        self.assertEqual(api["manifest_gaps"](self.path)["status"], "invalid_json")
        self.path.write_bytes(b"x" * (api["MAX_MANIFEST_BYTES"] + 1))
        self.assertEqual(api["manifest_gaps"](self.path)["status"], "oversized")
        for value in ([], {"schema": "veragensia.release_candidate.v2"}):
            self.write(value)
            self.assertEqual(api["manifest_gaps"](self.path)["status"], "unsupported_schema")

    def test_manifest_never_approves_itself(self):
        value = copy.deepcopy(self.candidate)
        value["release_ready"] = True
        value["status"] = "released"
        value["hardware"]["actual_board_verified"] = True
        for section, fields in api["REQUIRED_FIELDS"].items():
            for field in fields:
                value[section][field] = "claimed-proof"
        for gate in value["required_gates"]:
            gate.update(status="pass", evidence_ref="claimed-proof")
        value["platform"]["architecture"] = "x86_64"
        self.write(value)
        info = os.uname_result(("Linux", "unused", "6.test", "unused", "x86_64"))
        with patch.object(api["os"], "uname", return_value=info):
            result = api["doctor"](self.path, collector=lambda: {"status": "observed"})
        self.assertFalse(result["release_ready"])
        self.assertEqual(result["status"], "incomplete")
        self.assertEqual(result["manifest"]["status"], "metadata_present_unverified")
        self.assertEqual(result["manifest"]["evidence_verification"], "not_performed")

    def test_wrong_sections_duplicate_gates_and_bad_digests(self):
        self.candidate["platform"] = "SECRET"
        self.candidate["focusa_candidate"]["artifacts"][0]["sha256"] = "SECRET"
        self.candidate["required_gates"].append(self.candidate["required_gates"][0])
        self.write(self.candidate)
        result = api["manifest_gaps"](self.path)
        reasons = {g["reason"] for g in result["gaps"]}
        self.assertIn("missing_or_invalid_section", reasons)
        self.assertIn("missing_or_duplicate_gate", reasons)
        self.assertIn("missing_or_invalid_digest", reasons)
        self.assertNotIn("SECRET", json.dumps(result))

    def test_empty_gates_are_not_success(self):
        self.candidate["required_gates"] = []
        self.write(self.candidate)
        result = api["manifest_gaps"](self.path)
        self.assertEqual(sum(g["reason"] == "missing_or_duplicate_gate" for g in result["gaps"]), 14)

    def test_no_follow_or_block_on_special_file(self):
        self.path.symlink_to(Path(self.temp.name) / "missing")
        self.assertEqual(api["manifest_gaps"](self.path)["status"], "unreadable")
        self.path.unlink()
        os.mkfifo(self.path)
        self.assertEqual(api["manifest_gaps"](self.path)["status"], "unsupported_file_type")

    def artifact_fixture(self):
        directory = Path(self.temp.name) / "artifacts"
        directory.mkdir()
        for artifact in self.candidate["focusa_candidate"]["artifacts"]:
            content = b"#!/bin/sh\nexit 99\n"
            path = directory / artifact["name"]
            path.write_bytes(content)
            path.chmod(0o700)
            artifact["sha256"] = hashlib.sha256(content).hexdigest()
        self.write(self.candidate)
        return directory

    def test_local_hash_match_does_not_certify_readiness(self):
        directory = self.artifact_fixture()
        result = api["doctor"](self.path, lambda: {"status": "degraded"}, directory)
        self.assertEqual(result["manifest"]["artifact_hash_verification"], "matched")
        self.assertFalse(result["release_ready"])
        self.assertNotIn("dependency_artifact_hash_verification", result["remaining_checks"])
        self.assertIn("release_evidence_verification", result["remaining_checks"])
        self.assertEqual(result["manifest"]["evidence_verification"], "not_performed")

    def test_local_hash_mismatch_missing_and_invalid_metadata(self):
        directory = self.artifact_fixture()
        (directory / "focusa").write_bytes(b"changed")
        (directory / "focusa-daemon").unlink()
        result = api["manifest_gaps"](self.path, directory)
        self.assertEqual(result["artifact_hash_verification"], "failed")
        self.assertEqual([c["status"] for c in result["artifact_checks"]], ["mismatch", "missing"])
        self.candidate["focusa_candidate"]["artifacts"][0]["sha256"] = "invalid"
        self.write(self.candidate)
        result = api["manifest_gaps"](self.path, directory)
        self.assertEqual(result["artifact_checks"][0]["status"], "invalid_metadata")

    def test_hashing_has_no_execution_and_respects_file_bounds(self):
        path = Path(self.temp.name) / "artifact"
        sentinel = Path(self.temp.name) / "executed"
        content = f"#!/bin/sh\ntouch {sentinel}\n".encode()
        path.write_bytes(content)
        path.chmod(0o700)
        self.assertEqual(api["artifact_hash"](path, hashlib.sha256(content).hexdigest()), "match")
        self.assertFalse(sentinel.exists())
        with patch.dict(api["artifact_hash"].__globals__, {"MAX_ARTIFACT_BYTES": 4}):
            self.assertEqual(api["artifact_hash"](path, "0" * 64), "oversized")
        path.unlink()
        os.mkfifo(path)
        self.assertEqual(api["artifact_hash"](path, "0" * 64), "unsupported_file_type")
        path.unlink()
        path.symlink_to(self.path)
        self.assertEqual(api["artifact_hash"](path, "0" * 64), "unreadable")

    def test_cli_opt_in_hashing(self):
        directory = self.artifact_fixture()
        env = {**os.environ, "PATH": "", "HOME": self.temp.name,
               "HYPRLAND_INSTANCE_SIGNATURE": "", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, str(SCRIPT), "doctor", "--json", "--manifest", str(self.path),
                                 "--artifact-dir", str(directory)], env=env, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["manifest"]["artifact_hash_verification"], "matched")
        self.assertFalse(report["release_ready"])

    def test_host_observation_omits_identity_and_never_qualifies_native(self):
        self.write(self.candidate)
        info = os.uname_result(("Linux", "PRIVATE_HOSTNAME", "6.test", "PRIVATE_BUILD", "x86_64"))
        with patch.object(api["os"], "uname", return_value=info):
            result = api["doctor"](self.path, lambda: {"status": "degraded"})
        self.assertEqual(result["platform"]["status"], "observed")
        self.assertEqual(result["platform"]["system"], "Linux")
        self.assertEqual(result["platform"]["kernel_release"], "6.test")
        self.assertEqual(result["platform"]["architecture"], "x86_64")
        self.assertTrue(result["manifest"]["architecture_match"])
        self.assertEqual(result["platform"]["native_qualification"], "not_verified")
        self.assertIn("native_target_qualification", result["remaining_checks"])
        self.assertFalse(result["release_ready"])
        self.assertNotIn("PRIVATE_HOSTNAME", json.dumps(result))
        self.assertNotIn("PRIVATE_BUILD", json.dumps(result))

    def test_architecture_mismatch_and_missing_candidate_value(self):
        self.write(self.candidate)
        result = api["manifest_gaps"](self.path, observed_architecture="aarch64")
        self.assertIs(result["architecture_match"], False)
        self.assertIn({"field": "platform.architecture", "reason": "host_architecture_mismatch"}, result["gaps"])
        for value in (None, "", [], "unknown"):
            self.candidate["platform"]["architecture"] = value
            self.write(self.candidate)
            result = api["manifest_gaps"](self.path, observed_architecture="x86_64")
            self.assertIsNone(result["architecture_match"])
        self.candidate["platform"]["architecture"] = None
        self.write(self.candidate)
        self.assertIn({"field": "platform.architecture", "reason": "missing_or_invalid_value"},
                      api["manifest_gaps"](self.path)["gaps"])

    def test_unavailable_or_partial_host_observation_is_explicit(self):
        self.write(self.candidate)
        with patch.object(api["os"], "uname", side_effect=OSError("unavailable")):
            result = api["doctor"](self.path, lambda: {"status": "degraded"})
        self.assertEqual(result["platform"]["status"], "unknown")
        self.assertEqual(result["platform"]["error_class"], "OSError")
        self.assertIsNone(result["manifest"]["architecture_match"])
        self.assertFalse(result["release_ready"])
        for machine in ("", "unknown"):
            info = os.uname_result(("Linux", "unused", "6.test", "unused", machine))
            with patch.object(api["os"], "uname", return_value=info):
                result = api["doctor"](self.path, lambda: {"status": "degraded"})
            self.assertEqual(result["platform"]["status"], "partial")
            self.assertIsNone(result["platform"]["architecture"])
            self.assertIsNone(result["manifest"]["architecture_match"])

    def test_cli_version_parser_uses_fixed_command(self):
        calls = []
        def runner(argv):
            calls.append(argv)
            return {"status": "ok"}, b"focusa 0.9.184\n"
        result = api["focusa_cli_version"](runner)
        self.assertEqual(result, {"status": "observed", "version": "0.9.184"})
        self.assertEqual(calls, [["focusa", "--version"]])
        result = api["focusa_cli_version"](lambda argv: ({"status": "ok"}, b"focusa 0.10.0-rc.1+abc\n"))
        self.assertEqual(result["version"], "0.10.0-rc.1+abc")

    def test_cli_version_unknown_and_failed_outputs_are_not_exposed(self):
        for raw in (b"0.9.184", b"focusa latest", b"\xff", b"focusa 0.9.184\nPRIVATE_FOOTER"):
            result = api["focusa_cli_version"](lambda argv: ({"status": "ok"}, raw))
            self.assertEqual(result, {"status": "invalid_output", "version": None})
        for state in ({"status": "unavailable"}, {"status": "timeout"}, {"status": "oversized"},
                      {"status": "error", "exit_code": 7}):
            result = api["focusa_cli_version"](lambda argv: (state, b"PRIVATE_OUTPUT"))
            self.assertEqual(result, {**state, "version": None})
            self.assertNotIn("PRIVATE_OUTPUT", json.dumps(result))

    def test_doctor_cli_pin_match_mismatch_and_unknown(self):
        self.candidate["focusa_candidate"]["version"] = "0.9.184"
        self.write(self.candidate)
        for observed, expected in (("0.9.184", True), ("0.9.183", False), (None, None)):
            with patch.dict(api["doctor"].__globals__, {
                    "focusa_cli_version": lambda: {"status": "observed" if observed else "unavailable", "version": observed}}):
                result = api["doctor"](self.path, lambda: {"status": "degraded"})
            self.assertIs(result["manifest"]["focusa_cli_version_match"], expected)
            self.assertEqual(result["dependencies"]["focusa_cli"]["version"], observed)
            self.assertFalse(result["release_ready"])
            mismatch = {"field": "focusa_candidate.version", "reason": "focusa_cli_version_mismatch"}
            self.assertEqual(mismatch in result["manifest"]["gaps"], expected is False)
        self.candidate["focusa_candidate"]["version"] = None
        self.write(self.candidate)
        self.assertIsNone(api["manifest_gaps"](self.path, observed_focusa_version="0.9.184")["focusa_cli_version_match"])

    def test_cli_json_and_no_manifest_changes(self):
        self.write(self.candidate)
        before = self.path.read_bytes()
        env = {**os.environ, "PATH": "", "HOME": self.temp.name,
               "HYPRLAND_INSTANCE_SIGNATURE": "", "PYTHONDONTWRITEBYTECODE": "1"}
        result = subprocess.run([sys.executable, str(SCRIPT), "doctor", "--json", "--manifest", str(self.path)],
                                env=env, capture_output=True, timeout=10)
        self.assertEqual(result.returncode, 2, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["schema"], "veragensia.doctor.v1")
        self.assertFalse(report["release_ready"])
        self.assertEqual(report["runtime"]["status"], "degraded")
        self.assertEqual(before, self.path.read_bytes())


if __name__ == "__main__":
    unittest.main()
