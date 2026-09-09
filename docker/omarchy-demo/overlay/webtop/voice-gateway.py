#!/usr/bin/env python3
"""Veragensia demo voice gateway (docs/201 T2 preview slice).

POST /command {"text": "..."} -> utterance -> semantic operation match ->
S4 invoke (audited) -> transcription ledger entry with action lineage ->
desktop notification feedback. Runs inside the demo container with the
Hyprland session env; nginx routes /voice-gateway/ here. Stdlib only.
"""
import json
import os
import re
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import importlib.util as _ilu
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[3]  # /veragensia repo root inside the container mount

def _load(name, rel):
    spec = _ilu.spec_from_file_location(name, _ROOT / "scripts" / rel)
    mod = _ilu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

operations = _load("veragens_operations", "veragens-operations.py")
opexec = _load("veragens_operations_exec", "veragens-operations-exec.py")
audit = _load("veragens_audit", "veragens-audit.py")

BINDINGS = opexec.load_execution()
MAX_TEXT = 256
DIRECTIONS = (("left", "l"), ("right", "r"), ("up", "u"), ("down", "d"))

# LLM intent layer (docs/206): the operator's OpenAI subscription classifies
# the utterance against the semantic registry via the KH-side intent proxy.
# No credential material lives on the demo host; the proxy is tailnet-only.
INTENT_URL = os.environ.get(
    "VERAGENSIA_INTENT_URL", "http://100.94.238.56:8912/intent")
INTENT_HOST = os.environ.get(
    "VERAGENSIA_INTENT_HOST", "host-philoveracity-com:8912")
INTENT_ENGINE = os.environ.get(
    "VERAGENSIA_INTENT_ENGINE", "llm:gpt-5.6-luna(max)")
INTENT_TIMEOUT = float(os.environ.get("VERAGENSIA_INTENT_TIMEOUT", "80"))
ARG_HINTS = {
    "system.workspace.activate": ['"1".."9"'],
    "system.workspace.move_window_to": ['"1".."9"'],
    "system.window.focus_direction": ['"l"|"r"|"u"|"d"'],
    "system.window.move_direction": ['"l"|"r"|"u"|"d"'],
    "system.window.resize_active": ['two args "dx","dy" e.g. "-40","0" (negative shrinks)'],
}
INTENT_INSTRUCTIONS = (
    "You are the intent classifier for a voice-controlled Linux desktop. "
    "Map ONE spoken utterance to at most ONE operation from the provided "
    "list, or to null. Rules: use exact operation_id strings from the list; "
    "follow each operation's args hints exactly (workspace numbers are the "
    "strings \"1\"..\"9\"; directions are \"l\"|\"r\"|\"u\"|\"d\"; resize takes "
    "pixel deltas like \"40 0\"; every arg is a short ASCII string); prefer "
    "the operator's intent over their exact words (rude, casual, indirect, "
    "or polite phrasings all count); questions about the desktop that match "
    "a read-style operation still count; greetings, smalltalk, and anything "
    "outside the list are null. Never invent operation ids. Reply ONLY "
    "minified JSON: {\"operation_id\":string|null,\"args\":[string],"
    "\"confidence\":number}."
)


def normalize(text):
    return re.sub(r"[^a-z0-9 ]", " ", str(text).lower()).strip()


def _ops_list(registry):
    """Registry dicts and test doubles both work; real calls pass the dict."""
    if isinstance(registry, dict):
        return registry["operations"]
    return registry.operations


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
    for op in _ops_list(registry):
        op_id = op["operation_id"]
        if op_id in ("system.workspace.activate", "system.window.focus_direction",
                     "system.window.move_direction"):
            continue  # parameterized above
        for example in op["voice"]["examples"]:
            if normalize(example) in t or normalize(example) == t:
                return op_id, [], "voice_example"
    for op in _ops_list(registry):
        label = normalize(op["human"]["label"])
        if label and label in t:
            return op["operation_id"], [], "label"
    return None


def _registry_digest(registry):
    ops = []
    for op in _ops_list(registry):
        ops.append({
            "id": op["operation_id"],
            "label": op["human"]["label"],
            "examples": op["voice"]["examples"][:2],
            "args": ARG_HINTS.get(op["operation_id"], []),
        })
    return ops


def parse_intent_text(raw):
    """Parse the model's final text into a validated intent dict or None."""
    text = str(raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text).strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        intent = json.loads(text[start:end + 1])
    except ValueError:
        return None
    if not isinstance(intent, dict):
        return None
    op_id = intent.get("operation_id")
    try:
        confidence = max(0.0, min(1.0, float(intent.get("confidence", 0.0))))
    except (TypeError, ValueError):
        confidence = 0.0
    args = intent.get("args") or []
    if not isinstance(args, list):
        args = []
    args = [str(a).strip()[:64] for a in args if str(a).strip()][:4]
    return {"operation_id": (str(op_id) if op_id else None),
            "args": args, "confidence": confidence}


def llm_intent(text, registry):
    """Classify one utterance via the KH subscription proxy; None on any failure."""
    payload = json.dumps({
        "instructions": INTENT_INSTRUCTIONS,
        "input": json.dumps({"transcript": text,
                             "operations": _registry_digest(registry)}),
    }).encode("utf-8")
    req = urllib.request.Request(
        INTENT_URL, data=payload, method="POST",
        headers={"Content-Type": "application/json", "Host": INTENT_HOST})
    data = json.load(urllib.request.urlopen(req, timeout=INTENT_TIMEOUT))
    if not data.get("ok"):
        return None
    return parse_intent_text(data.get("text", ""))


def desktop_notify(runner, message):
    runner(["hyprctl", "notify", "4000", "rgb(c4b5fd)", str(message)[:120]])


def _confidence(value):
    try:
        value = float(value)
    except (TypeError, ValueError):
        return None
    return max(0.0, min(1.0, value))


def _duration(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return None
    return max(0, min(120000, value))


def handle_command(text, registry, actor="voice-daemon", audit_dir=None,
                   confidence=None, audio_duration_ms=None, runner=None,
                   intent_fn=None):
    text = str(text)[:MAX_TEXT]
    confidence = _confidence(confidence)
    audio_duration_ms = _duration(audio_duration_ms)
    outcome = {"transcript": text, "confidence": confidence,
               "audio_duration_ms": audio_duration_ms,
               "intent_engine": INTENT_ENGINE if intent_fn is None else "test"}
    runner = runner or opexec.probe
    intent_fn = intent_fn or llm_intent
    intent = None
    intent_unavailable = False
    try:
        intent = intent_fn(text, registry)
    except Exception:
        intent = None  # regex matcher stays as the offline fallback
        intent_unavailable = True
    matched = None
    if intent and intent.get("operation_id"):
        matched = (intent["operation_id"], intent.get("args") or [], "llm")
    else:
        fallback = match_operation(text, registry)
        if fallback:
            matched = (fallback[0], fallback[1], "regex_fallback")
    if matched is None:
        outcome.update(matched=False, reason=("intent_unavailable" if intent_unavailable
                                              else "llm_unmatched"),
                       intent_confidence=(intent or {}).get("confidence"),
                       hint="try: go to workspace 2 / move focus left / make this fullscreen")
        audit.record_transcription(
            audit_dir, text, "web-speech-api", actor, confidence=confidence,
            audio_duration_ms=audio_duration_ms, matched_operation_id=None,
            match_method="unmatched",
            intent_engine=(None if intent_unavailable else INTENT_ENGINE),
            intent_confidence=(intent or {}).get("confidence"))
        desktop_notify(runner, "voice: not understood")
        return outcome
    op_id, args, method = matched
    if op_id == "system.window.resize_active":
        # hyprctl needs dx and dy as separate tokens; models often emit one
        # string like "-40 -40" — expand space-separated values, bounded.
        args = [part for arg in args for part in arg.split()][:4]
    ops = _ops_list(registry)
    result = opexec.invoke(op_id, args, registry_describe=lambda oid: next(
        (o for o in ops if o["operation_id"] == oid), None),
        bindings=BINDINGS, runner=runner, actor=actor, audit_dir=audit_dir)
    intent_engine = INTENT_ENGINE if intent is not None else None
    audit.record_transcription(
        audit_dir, text, "web-speech-api", actor, confidence=confidence,
        audio_duration_ms=audio_duration_ms, matched_operation_id=op_id,
        match_method=method, action_audit_seq=result.get("audit_seq"),
        intent_engine=intent_engine, intent_confidence=(intent or {}).get("confidence"))
    desktop_notify(runner, f"voice: {op_id.split('.', 2)[-1]} {result.get('status')}")
    outcome.update(matched=True, operation_id=op_id, match_method=method,
                   status=result.get("status"), error=result.get("error"),
                   consequence_class=result.get("consequence_class"),
                   authority_required=result.get("error") == "authority_required",
                   intent_confidence=(intent or {}).get("confidence"),
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
        try:
            length = min(max(int(self.headers.get("Content-Length", 0)), 0), 4096)
        except (TypeError, ValueError):
            length = 0
        try:
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (TypeError, ValueError):
            payload = {}
        if not isinstance(payload, dict):
            payload = {}
        text = payload.get("text", "")
        # The request body cannot mint an actor identity. The public route is a
        # fixed browser surface; the transcript and action remain linked in the
        # append-only ledgers under this stable actor label.
        actor = "voice-browser"
        confidence = payload.get("confidence")
        duration = payload.get("audio_duration_ms")
        try:
            outcome = handle_command(
                text, self.registry, actor=actor, audit_dir=audit.DEFAULT_DIR,
                confidence=confidence, audio_duration_ms=duration)
        except Exception:
            # Never leave a browser with an empty HTTP reply. Avoid exposing
            # internal paths/details; the attempt is still recorded as a failed
            # transcription when the ledger is writable.
            safe_text = str(text)[:MAX_TEXT]
            audit.record_transcription(
                audit.DEFAULT_DIR, safe_text, "web-speech-api", actor,
                confidence=_confidence(confidence),
                audio_duration_ms=_duration(duration),
                matched_operation_id=None, match_method="gateway_error")
            outcome = {"transcript": safe_text, "matched": False,
                       "status": "failed", "error": "gateway_error"}
        body = json.dumps(outcome).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
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
