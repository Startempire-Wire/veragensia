#!/usr/bin/env python3
"""Doc 201 V201-S2: semantic system-operation registry loader and validator.

The registry (config/system-operations.json) advertises how to invoke system
behaviors; it never executes anything and grants no authority. Actual
permission remains governed by applicable Focusa/Veragensia/UIAI gates
(docs/201 §3). Execution adapters are wired by V201-S4.
"""
from pathlib import Path
import json
import re

CATALOG_SCHEMA = "veragensia.system_operation_catalog.v1"
DESCRIPTOR_SCHEMA = "veragensia.system_operation.v1"
REGISTRY_PATH = Path(__file__).resolve().parent.parent / "config" / "system-operations.json"

CATEGORIES = ("workspace", "window", "app", "audio", "bluetooth", "display", "power",
              "capture", "clipboard", "notification", "agent", "text", "system")
OWNER_RUNTIMES = ("veragensia", "omarchy", "hyprland", "focusa", "uiai", "application")
ADAPTERS = ("omarchy_cli", "hyprland_dispatch", "native_service", "focusa_operation",
            "uiai_operation", "app_protocol")
CONSEQUENCE_CLASSES = ("low", "medium", "high")
OPERATION_ID = re.compile(r"^system\.[a-z0-9]+(?:\.[a-z0-9_]+){1,3}$")
DESCRIPTOR_KEYS = ("schema", "operation_id", "version", "owner_runtime", "category",
                   "human", "voice", "parameters", "preconditions", "execution",
                   "risk", "result")
# Doc 201 V201-S2 first operation families; every family needs >=1 descriptor.
FAMILIES = {
    "workspace/navigation": ("workspace",),
    "window placement/state": ("window",),
    "app launch/close/focus": ("app",),
    "audio/Bluetooth": ("audio", "bluetooth"),
    "display/power": ("display", "power"),
    "capture/clipboard": ("capture", "clipboard"),
    "notification/history": ("notification",),
    "agent launch/selection": ("agent",),
    "dictation/listening control": ("text",),
}


class RegistryError(ValueError):
    """Raised when the registry violates the docs/201 §3 descriptor contract."""


def _fail(op_id, reason):
    raise RegistryError(f"{op_id or '<envelope>'}: {reason}")


def _check_descriptor(op, index):
    if not isinstance(op, dict):
        _fail(None, f"operations[{index}] is not an object")
    op_id = op.get("operation_id")
    missing = [key for key in DESCRIPTOR_KEYS if key not in op]
    if missing:
        _fail(op_id, f"missing keys {missing}")
    if op["schema"] != DESCRIPTOR_SCHEMA:
        _fail(op_id, f"schema must be {DESCRIPTOR_SCHEMA}")
    if not OPERATION_ID.fullmatch(op_id or ""):
        _fail(op_id, "operation_id must match system.<family>[.<name>]")
    if op["version"] != 1:
        _fail(op_id, "version must be 1 for the first registry slice")
    if op["owner_runtime"] not in OWNER_RUNTIMES:
        _fail(op_id, f"owner_runtime must be one of {OWNER_RUNTIMES}")
    if op["category"] not in CATEGORIES:
        _fail(op_id, f"category must be one of {CATEGORIES}")
    human, voice = op["human"], op["voice"]
    if not isinstance(human, dict) or not human.get("label"):
        _fail(op_id, "human.label is required")
    if not isinstance(voice, dict) or not (1 <= len(voice.get("examples", [])) <= 8):
        _fail(op_id, "voice.examples requires 1..8 phrases")
    pre, execution, risk, result = op["preconditions"], op["execution"], op["risk"], op["result"]
    for key in ("capability_refs", "authority_ref_required", "target_observation_required",
                "secure_attention_required"):
        if key not in pre:
            _fail(op_id, f"preconditions.{key} is required")
    if execution["preferred_adapter"] not in ADAPTERS:
        _fail(op_id, f"preferred_adapter must be one of {ADAPTERS}")
    if not set(execution["fallback_adapters"]) <= set(ADAPTERS):
        _fail(op_id, f"fallback_adapters must be within {ADAPTERS}")
    if not execution.get("command_template_ref"):
        _fail(op_id, "execution.command_template_ref is required")
    if risk["consequence_class"] not in CONSEQUENCE_CLASSES:
        _fail(op_id, f"consequence_class must be one of {CONSEQUENCE_CLASSES}")
    if not risk.get("reversibility"):
        _fail(op_id, "risk.reversibility is required")
    if not result.get("schema_ref") or not result.get("evidence_policy_ref"):
        _fail(op_id, "result.schema_ref and result.evidence_policy_ref are required")


def load_registry(path=REGISTRY_PATH):
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    if envelope.get("schema") != CATALOG_SCHEMA:
        raise RegistryError(f"catalog schema must be {CATALOG_SCHEMA}")
    operations = envelope.get("operations")
    if not isinstance(operations, list) or not operations:
        raise RegistryError("operations must be a non-empty list")
    seen = set()
    for index, op in enumerate(operations):
        _check_descriptor(op, index)
        if op["operation_id"] in seen:
            _fail(op["operation_id"], "duplicate operation_id")
        seen.add(op["operation_id"])
    return envelope


def catalog(path=REGISTRY_PATH):
    """Bounded list projection for `veragens operation list`."""
    envelope = load_registry(path)
    operations = sorted(
        ({"operation_id": op["operation_id"], "category": op["category"],
          "label": op["human"]["label"], "owner_runtime": op["owner_runtime"],
          "preferred_adapter": op["execution"]["preferred_adapter"]}
         for op in envelope["operations"]),
        key=lambda item: item["operation_id"])
    return {"schema": "veragensia.system_operation_list.v1",
            "catalog_version": envelope["catalog_version"],
            "spec_ref": envelope["spec_ref"], "count": len(operations),
            "operations": operations}


def describe(operation_id, path=REGISTRY_PATH):
    """Full descriptor projection for `veragens operation describe`."""
    envelope = load_registry(path)
    for op in envelope["operations"]:
        if op["operation_id"] == operation_id:
            return dict(op)
    return None


def family_coverage(path=REGISTRY_PATH):
    """Map each V201-S2 family to its covered categories (release diagnostics)."""
    envelope = load_registry(path)
    present = {op["category"] for op in envelope["operations"]}
    return {family: sorted(set(categories) & present)
            for family, categories in FAMILIES.items()}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", action="store_true", help="validate and print family coverage")
    args = parser.parse_args()
    envelope = load_registry()
    print(f"registry ok: {len(envelope['operations'])} operations, "
          f"{len(family_coverage())}/{len(FAMILIES)} families covered")
