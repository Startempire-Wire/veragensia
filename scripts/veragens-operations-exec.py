#!/usr/bin/env python3
"""Doc 201 V201-S4: operation execution via the hyprland_dispatch adapter.

Implements the first execution slice of the semantic operation registry:
read-verified dispatch (state snapshots before and after, docs/201 §15.6),
an authority gate matching the registry's declared posture (medium/high
consequence operations require an explicit authority reference), and a
fenced batch runner (docs/201 §15.5: owner interruption aborts between
operations). The runner only ever executes fixed-argv probes and
`hyprctl dispatch` — never shell interpolation of caller input.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import time

import importlib.util as _ilu
_audit_spec = _ilu.spec_from_file_location(
    "veragens_audit", Path(__file__).resolve().parent / "veragens-audit.py")
audit_mod = _ilu.module_from_spec(_audit_spec)
_audit_spec.loader.exec_module(audit_mod)

EXECUTION_SCHEMA = "veragensia.operation_execution.v1"
RESULT_SCHEMA = "veragensia.operation_result.v1"
EXECUTION_PATH = Path(__file__).resolve().parent.parent / "config" / "operation-execution.json"
MAX_ARG_CHARS = 64
MAX_ARGS = 4
MAX_BATCH_OPS = 32
TIMEOUT = 5.0
ARG_PATTERN = re.compile(r"^[A-Za-z0-9_ -]{1,64}$")
HYPRCTL_ENV_KEYS = ("HYPRLAND_INSTANCE_SIGNATURE", "XDG_RUNTIME_DIR", "WAYLAND_DISPLAY")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def probe(argv, timeout=TIMEOUT):
    """Fixed argv only; bounded output; kill the process group on overrun."""
    executable = shutil.which(argv[0])
    if executable is None:
        return {"status": "unavailable"}, b""
    deadline = time.monotonic() + timeout
    try:
        child = subprocess.Popen([executable, *argv[1:]], stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                 start_new_session=True, env=dict(os.environ))
    except OSError:
        return {"status": "error", "reason": "spawn_failed"}, b""
    output = bytearray()
    failure = None
    try:
        with selectors.DefaultSelector() as selector:
            selector.register(child.stdout, selectors.EVENT_READ, True)
            selector.register(child.stderr, selectors.EVENT_READ, False)
            while selector.get_map():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    failure = "timeout"
                    break
                for key, _ in selector.select(remaining):
                    chunk = os.read(key.fd, 4096)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    output.extend(chunk[:max(0, 262144 - len(output))])
            if failure is None:
                code = child.wait(timeout=max(0.0, deadline - time.monotonic()))
    except subprocess.TimeoutExpired:
        failure = "timeout"
    finally:
        if failure is not None or child.poll() is None:
            try:
                os.killpg(child.pid, 15)
            except OSError:
                pass
            try:
                child.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, 9)
                child.wait()
    if failure is not None:
        return {"status": failure}, bytes(output[:262144])
    return {"status": "ok", "exit_code": code}, bytes(output[:262144])


def load_execution(path=EXECUTION_PATH):
    envelope = json.loads(Path(path).read_text(encoding="utf-8"))
    if envelope.get("schema") != EXECUTION_SCHEMA:
        raise ValueError(f"execution map schema must be {EXECUTION_SCHEMA}")
    bindings = {}
    for binding in envelope.get("bindings", []):
        op = binding.get("operation_id")
        if op in bindings:
            raise ValueError(f"duplicate execution binding: {op}")
        bindings[op] = binding
    return bindings


def _snapshot(runner, queries=("activewindow",)):
    """Read-only compositor state around a dispatch; delivery truth, not claims."""
    states = {}
    for query in queries:
        state, raw = runner(["hyprctl", "-j", query])
        if state.get("status") == "ok":
            try:
                states[query] = json.loads(raw.decode("utf-8", "replace"))
            except ValueError:
                states[query] = {"unparsed": raw.decode("utf-8", "replace")[:256]}
        else:
            states[query] = {"status": state.get("status")}
    return states


def _check_args(args, binding):
    mode = binding.get("arg_mode")
    if mode == "none":
        return "operation takes no arguments" if args else None
    if mode == "fixed":
        return None
    if mode != "literal":
        return f"unknown arg_mode {mode!r}"
    if len(args) > MAX_ARGS:
        return f"at most {MAX_ARGS} arguments allowed"
    for arg in args:
        if not isinstance(arg, str) or not ARG_PATTERN.fullmatch(arg):
            return f"argument rejected: {arg!r}"
    return None


def invoke(operation_id, args=None, registry_describe=None, bindings=None,
           runner=probe, authority_ref=None, observed_at=None, actor="operator-cli",
           audit_dir=None, origin_utterance_ref=None):
    """Execute one semantic operation through its adapter with verification.

    Every attempt — success, refusal, or failure — is audited when audit_dir
    is provided; refusals are audit-worthy, not silent.
    """
    from datetime import datetime, timezone
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    args = list(args or [])
    result = {"schema": RESULT_SCHEMA, "operation_id": operation_id,
              "observed_at": observed_at, "authority_ref_present": bool(authority_ref)}

    def finish():
        if origin_utterance_ref:
            result["origin_utterance_ref"] = str(origin_utterance_ref)[:120]
        if audit_dir is not None:
            result.update(audit_mod.record_operation(
                audit_dir, result, actor, authority_ref,
                origin_utterance_ref=origin_utterance_ref))
        return result

    descriptor = registry_describe(operation_id)
    if descriptor is None:
        result.update(status="failed", error="unknown_operation")
        return finish()
    binding = (bindings or {}).get(operation_id)
    if binding is None or binding.get("adapter") != "hyprland_dispatch":
        result.update(status="failed", error="adapter_unavailable",
                      adapter=descriptor["execution"]["preferred_adapter"])
        return finish()

    consequence = descriptor["risk"]["consequence_class"]
    if consequence in ("medium", "high") and not authority_ref:
        result.update(status="refused", error="authority_required",
                      consequence_class=consequence,
                      reason="registry posture requires an authority reference for medium/high operations")
        return finish()

    arg_error = _check_args(args, binding)
    if arg_error:
        result.update(status="failed", error="invalid_arguments", reason=arg_error)
        return finish()

    category = descriptor["category"]
    query = "activewindow" if category == "window" else "activeworkspace" if category == "workspace" else None
    before = _snapshot(runner, (query,)) if query else {}

    if binding.get("arg_mode") == "fixed":
        dispatch_args = list(binding.get("fixed_args", []))
    elif binding.get("arg_mode") == "none":
        dispatch_args = []
    else:
        dispatch_args = args
    state, raw = runner(["hyprctl", "dispatch", binding["dispatcher"], *dispatch_args])
    ok = state.get("status") == "ok" and state.get("exit_code") == 0
    after = _snapshot(runner, (query,)) if query else {}
    result.update(status="ok" if ok else "failed",
                  dispatcher=binding["dispatcher"],
                  dispatch_args=dispatch_args,
                  arg_sha256=digest(json.dumps(dispatch_args).encode()),
                  exit_code=state.get("exit_code"),
                  stderr_tail=raw.decode("utf-8", "replace")[-256:] if not ok else "",
                  before=before, after=after)
    if not ok:
        result["error"] = "dispatch_failed"
    return finish()


def batch(steps, registry_describe=None, bindings=None, runner=probe,
          authority_ref=None, fence_path=None, max_ops=MAX_BATCH_OPS, observed_at=None,
          actor="operator-cli", audit_dir=None, origin_utterance_ref=None):
    """Run operations sequentially; a fence file existing aborts between steps."""
    from datetime import datetime, timezone
    observed_at = observed_at or datetime.now(timezone.utc).isoformat()
    results = []
    outcome = "completed"
    for index, step in enumerate(steps[:max_ops]):
        if fence_path and Path(fence_path).exists():
            outcome = "fenced"
            break
        entry = invoke(step.get("operation_id"), step.get("args") or [],
                       registry_describe=registry_describe, bindings=bindings,
                       runner=runner, authority_ref=authority_ref, observed_at=observed_at,
                       actor=actor, audit_dir=audit_dir,
                       origin_utterance_ref=origin_utterance_ref)
        entry["step"] = index
        results.append(entry)
        if entry.get("status") != "ok":
            outcome = "failed"
            break
    else:
        if len(steps) > max_ops:
            outcome = "capped"
    if fence_path and outcome == "completed" and len(steps) > max_ops:
        outcome = "capped"
    return {"schema": "veragensia.operation_batch_result.v1", "observed_at": observed_at,
            "outcome": outcome, "requested": len(steps), "executed": len(results),
            "fence_path": str(fence_path) if fence_path else None,
            "results": results}


def main():
    import argparse
    from datetime import datetime, timezone
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    one = sub.add_parser("invoke", help="execute one semantic operation")
    one.add_argument("operation_id")
    one.add_argument("args", nargs="*", help="bounded operation arguments")
    one.add_argument("--authority-ref", default=None,
                     help="authority reference required for medium/high consequence operations")
    one.add_argument("--actor", default="operator-cli",
                     help="audit actor label (e.g. voice-daemon, agent-session)")
    one.add_argument("--no-audit", action="store_true",
                     help="skip the audit ledger append (audited runs are the default)")
    batch_parser = sub.add_parser("batch", help="execute a fenced operation batch")
    batch_parser.add_argument("--file", type=Path, required=True,
                              help="JSON file: [{operation_id, args}]")
    batch_parser.add_argument("--fence", type=Path, required=True,
                              help="interruption fence: existing file aborts between steps")
    batch_parser.add_argument("--authority-ref", default=None)
    batch_parser.add_argument("--actor", default="operator-cli")
    batch_parser.add_argument("--no-audit", action="store_true")
    audit_cmd = sub.add_parser("audit", help="read the operations audit ledger")
    audit_cmd.add_argument("--tail", type=int, default=32)
    audit_cmd.add_argument("--verify", action="store_true",
                           help="verify the hash chain and report any breakage")
    parser.add_argument("--registry", type=Path, default=None)
    parser.add_argument("--execution", type=Path, default=None)
    parser.add_argument("--json", action="store_true", required=True)
    args = parser.parse_args()

    operations_path = args.registry or (Path(__file__).resolve().parent.parent / "config/system-operations.json")
    sys_path = args.execution or EXECUTION_PATH
    registry_describe = None
    spec = __import__("importlib.util", fromlist=["util"]).util
    mod_spec = spec.spec_from_file_location("veragens_operations",
                                            Path(__file__).resolve().parent / "veragens-operations.py")
    operations = spec.module_from_spec(mod_spec)
    mod_spec.loader.exec_module(operations)
    registry_describe = operations.describe

    bindings = load_execution(sys_path)
    audit_dir = None if args.no_audit else audit_mod.DEFAULT_DIR
    if args.command == "invoke":
        report = invoke(args.operation_id, args.args, registry_describe=registry_describe,
                        bindings=bindings, authority_ref=args.authority_ref,
                        actor=args.actor, audit_dir=audit_dir)
    elif args.command == "batch":
        steps = json.loads(args.file.read_text(encoding="utf-8"))
        report = batch(steps, registry_describe=registry_describe, bindings=bindings,
                       authority_ref=args.authority_ref, fence_path=args.fence,
                       actor=args.actor, audit_dir=audit_dir)
    else:
        report = audit_mod.tail(audit_mod.DEFAULT_DIR / audit_mod.OPERATIONS_LEDGER,
                                limit=max(1, min(args.tail, audit_mod.MAX_TAIL)),
                                verify=args.verify)
    print(json.dumps(report, sort_keys=True))
    if args.command == "audit":
        return 0
    return 0 if report.get("status") == "ok" or report.get("outcome") == "completed" else 1


if __name__ == "__main__":
    import sys
    sys.dont_write_bytecode = True
    raise SystemExit(main())
