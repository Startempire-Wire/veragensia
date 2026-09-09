#!/usr/bin/env python3
"""Doc 201 V201-S3: keybinding parity compiler (read-only).

Correlates V201-S1 live bindings (arguments stored as sha256 only) with the
V201-S2 semantic operation registry, applies the docs/201 §4.2 classification
gate to every live binding, and detects projection drift against a stored
baseline (docs/201 §15 invariant 8). Never executes bindings and never
mutates the desktop; unmapped_gap records are release defects, not errors.
"""
import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PROJECTION_SCHEMA = "veragensia.keybinding_projection_report.v1"
RULE_SCHEMA = "veragensia.keybinding_projection_rule.v1"
RULES_PATH = Path(__file__).resolve().parent.parent / "config" / "keybinding-projection.json"
CLASSES = ("semantic_operation", "text_input", "application_internal",
           "hardware_firmware", "unsupported_platform", "unmapped_gap")
SOURCES = ("omarchy_default", "user_override", "generated", "application")
# Hyprland modmask bits, ordered for the docs/201 §4 chord style "SUPER + SHIFT + O".
MOD_BITS = ((64, "SUPER"), (1, "SHIFT"), (4, "CTRL"), (8, "ALT"),
            (16, "MOD2"), (32, "MOD3"), (128, "MOD5"))
# Dispatchers that act inside an application or are inherently non-semantic
# without a matching argument digest rule.
NON_SEMANTIC_DISPATCHERS = ("exec", "mouse", "movewindow", "resizewindow")


def key_chord(modmask, key):
    """Render a binding as the docs/201 §4 chord style, e.g. SUPER + SHIFT + O."""
    names = [label for bit, label in MOD_BITS if modmask & bit]
    names.append(str(key).upper())
    return " + ".join(names)


def binding_ref(item):
    """Stable identity of a live binding tuple; raw arguments never appear."""
    material = json.dumps({
        "modmask": item.get("modmask"), "key": item.get("key"),
        "keycode": item.get("keycode"), "dispatcher": item.get("dispatcher"),
        "argument_sha256": item.get("argument_sha256"),
    }, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(material.encode()).hexdigest()


def load_rules(path=RULES_PATH):
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    if envelope.get("schema") != RULE_SCHEMA and envelope.get("schema") != "veragensia.keybinding_projection_rules.v1":
        raise ValueError(f"projection rules schema must be {RULE_SCHEMA} or rules envelope")
    rules = envelope.get("rules", envelope) if isinstance(envelope, dict) else []
    if not isinstance(rules, list):
        raise ValueError("rules must be a list")
    seen = set()
    for rule in rules:
        op = rule.get("operation_id")
        if not op or op in seen:
            raise ValueError(f"rule missing or duplicate operation_id: {op!r}")
        seen.add(op)
        match = rule.get("match") or {}
        if not isinstance(match.get("dispatcher"), str):
            raise ValueError(f"rule {op}: match.dispatcher is required")
        digest = rule.get("argument_sha256")
        if digest is not None and not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError(f"rule {op}: argument_sha256 must be a 64-hex digest or null")
        if rule.get("source") not in SOURCES:
            raise ValueError(f"rule {op}: source must be one of {SOURCES}")
    return rules


def classify(item, rules):
    """Apply the docs/201 §4.2 classification gate to one live binding."""
    dispatcher = item.get("dispatcher")
    argument = item.get("argument_sha256")
    for rule in rules:
        match = rule.get("match") or {}
        if match.get("dispatcher") != dispatcher:
            continue
        required = rule.get("argument_sha256")
        if required is not None and required != argument:
            continue
        return {"classification": "semantic_operation",
                "operation_ref": rule.get("operation_id"),
                "source": rule.get("source")}
    if dispatcher in NON_SEMANTIC_DISPATCHERS:
        return {"classification": "application_internal", "operation_ref": None,
                "source": "application"}
    return {"classification": "unmapped_gap", "operation_ref": None, "source": None}


def compile_projection(inventory, rules, observed_at=None, runtime_incarnation_ref=None):
    """Compile an S1 inventory report into a keybinding projection report."""
    source = inventory.get("sources", {}).get("hyprland_bindings", {})
    if source.get("status") not in ("ok", "incomplete"):
        raise ValueError("inventory hyprland_bindings source must be ok/incomplete")
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    records = []
    for item in source.get("items", []):
        verdict = classify(item, rules)
        records.append({
            "schema": "veragensia.keybinding_projection.v1",
            "binding_ref": binding_ref(item),
            "key_chord": key_chord(item.get("modmask", 0), item.get("key", "")),
            "dispatcher": item.get("dispatcher"),
            "argument_sha256": item.get("argument_sha256"),
            "operation_ref": verdict["operation_ref"],
            "classification": verdict["classification"],
            "source": verdict["source"],
            "active": True,
            "observed_at": observed_at,
            "runtime_incarnation_ref": runtime_incarnation_ref
            or inventory.get("runtime_ref"),
        })
    counts = {cls: sum(1 for r in records if r["classification"] == cls) for cls in CLASSES}
    return {
        "schema": PROJECTION_SCHEMA,
        "observed_at": observed_at,
        "inventory_status": source.get("status"),
        "inventory_total": source.get("total", len(records)),
        "classified_total": len(records),
        "classification_counts": counts,
        "unmapped_gap_count": counts["unmapped_gap"],
        "unmapped_gap_is_release_defect": True,
        "projection_drift": False,
        "drift": {"added": [], "removed": [], "changed": []},
        "records": records,
    }


def diff_projection(current, baseline):
    """Detect drift between the current projection and a stored baseline."""
    def index(report):
        return {r["binding_ref"]: r for r in report.get("records", [])}

    now, base = index(current), index(baseline)
    drift = {"added": sorted(set(now) - set(base)),
             "removed": sorted(set(base) - set(now)),
             "changed": sorted(ref for ref in set(now) & set(base)
                               if now[ref]["operation_ref"] != base[ref].get("operation_ref")
                               or now[ref]["classification"] != base[ref].get("classification"))}
    result = dict(current)
    result["projection_drift"] = bool(drift["added"] or drift["removed"] or drift["changed"])
    result["drift"] = drift
    result["baseline_observed_at"] = baseline.get("observed_at")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True,
                        help="V201-S1 inventory report JSON (hyprland_bindings source)")
    parser.add_argument("--rules", type=Path, default=RULES_PATH,
                        help="projection rule file (default: repo config/keybinding-projection.json)")
    parser.add_argument("--baseline", type=Path, default=None,
                        help="prior projection report JSON; emits drift when the keymap changed")
    parser.add_argument("--json", action="store_true", required=True)
    args = parser.parse_args()
    inventory = json.loads(Path(args.inventory).read_text(encoding="utf-8"))
    rules = load_rules(args.rules)
    report = compile_projection(inventory, rules)
    if args.baseline is not None:
        baseline = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
        report = diff_projection(report, baseline)
    print(json.dumps(report, sort_keys=True))
    # Exit 0 even with unmapped_gap records: the report is the deliverable.
    # Exit 2 only when the compiler could not produce a projection at all.
    return 0


if __name__ == "__main__":
    sys.dont_write_bytecode = True
    raise SystemExit(main())
