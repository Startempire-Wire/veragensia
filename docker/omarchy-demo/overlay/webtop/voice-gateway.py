#!/usr/bin/env python3
"""Veragensia demo voice gateway (docs/201 T2 preview slice).

POST /command {"text": "..."} -> utterance -> semantic operation match ->
S4 invoke (audited) -> transcription ledger entry with action lineage ->
desktop notification feedback. Runs inside the demo container with the
Hyprland session env; nginx routes /voice-gateway/ here. Stdlib only.
"""
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import importlib.util as _ilu
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO = _HERE.parent.parent.parent

def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, _HERE / rel)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

operations = _load("veragens_operations", "veragens-operations.py")
opexec = _load("veragens_operations_exec", "veragens-operations-exec.py")
audit = _load("veragens_audit", "veragens-audit.py")

BINDINGS = opexec.load_execution()
MAX_TEXT = 256
DIRECTIONS = (("left", "l"), ("right", "r"), ("up", "u"), ("down", "d"))


def normalize(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).strip()


def match_operation(text, registry):
    """Match a transcript to (operation_id, args, method). Parameterized first."""
    t = normalize(text)
    ws = re.search(r"(?:go to |switch to |show |open )?workspace (?:number )?([1-9])", t)
    if ws:
        return "system.workspace.activate", [ws.group(1)], "parameterized"
    for word, code in DIRECTIONS:
        if re.search(rf"move (?:the )?focus {word}\b", t) or re.search(rf"focus {word}\b", t):
            return "system.window.focus_direction", [code], "parameterized"
        if re.search(rf"move (?:this |the )?window {word}\b", t):
            return "system.window.move_direction", [code], "parameterized"
    for op in registry["operations"]:
        op_id = op["operation_id"]
        if op_id in ("system.workspace.activate", "system.window.focus_direction",
                     "system.window.move_direction"):
            continue  # parameterized above
        for example in op["voice"]["examples"]:
            if normalize(example) in t or normalize(example) == t:
                return op_id, [], "voice_example"
    for op in registry["operations"]:
        label = normalize(op["human"]["label"])
        if label and label in t:
            return op["operation_id"], [], "label"
    return None


def desktop_notify(runner, message):
    runner(["hyprctl", "notify", "4000", "rgb(c4b5fd)", str(message)[:120]])


def handle_command(text, registry, actor="voice-daemon", audit_dir=None):
    text = str(text)[:MAX_TEXT]
    outcome = {"transcript": text}
    matched = match_operation(text, registry)
    if matched is None:
        outcome.update(matched=False, reason="no_operation_match")
        audit.record_transcription(audit_dir, text, "web-speech-api", actor,
                                   matched_operation_id=None, match_method="unmatched")
        desktop_notify(opexec.probe, "voice: not understood")
        return outcome
    op_id, args, method = matched
    result = opexec.invoke(op_id, args, registry_describe=lambda oid: next(
        (o for o in registry["operations"] if o["operation_id"] == oid), None),
        bindings=BINDINGS, runner=opexec.probe, actor=actor, audit_dir=audit_dir)
    audit.record_transcription(audit_dir, text, "web-speech-api", actor,
                               matched_operation_id=op_id, match_method=method,
                               action_audit_seq=result.get("audit_seq"))
    desktop_notify(opexec.probe, f"voice: {op_id.split('.', 2)[-1]} {result.get('status')}")
    outcome.update(matched=True, operation_id=op_id, match_method=method,
                   status=result.get("status"), error=result.get("error"),
                   consequence_class=(result.get("before") is not None and None) or None,
                   authority_required=result.get("error") == "authority_required",
                   before=result.get("before"), after=result.get("after"))
    return outcome


class Handler(BaseHTTPRequestHandler):
    registry = operations.load_registry()

    def do_GET(self):
        if self.path.startswith("/health"):
            body = json.dumps({"status": "ok", "operations": len(self.registry["operations"])}).encode()
            self.send_response(200)
        else:
            body = b"{}"
            self.send_response(404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if not self.path.startswith("/command"):
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        length = min(int(self.headers.get("Content-Length", 0)), 4096)
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except ValueError:
            payload = {}
        actor = str(payload.get("actor") or "voice-daemon")[:64]
        outcome = handle_command(payload.get("text", ""), self.registry, actor=actor,
                                 audit_dir=audit.DEFAULT_DIR)
        body = json.dumps(outcome).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # bounded logging: the ledgers are the record, stdout stays quiet


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8900), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
