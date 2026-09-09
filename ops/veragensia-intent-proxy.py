#!/usr/bin/env python3
"""Veragensia intent proxy — KH-side OpenAI subscription bridge (tailnet only).

The OVH demo voice gateway classifies utterances with the operator's OpenAI
subscription (Codex backend, gpt-5.6-luna at max reasoning). The subscription
credential lives ONLY on this host and is refreshed by the local Pi harness;
this proxy reads it fresh per request, forwards one bounded intent request,
and returns the model's final text. No secrets and no transcripts are logged.

Endpoints:
  POST /intent  {"instructions": str, "input": str}  -> {"ok":true,"text":str,...}
  GET  /health                                      -> {"ok":true,...}

Bound to 127.0.0.1 only; exposed to the tailnet via `tailscale serve`.
"""
import base64
import json
import os
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

AUTH_PATH = os.environ.get("VERAGENSIA_AUTH_JSON", "/root/.pi/agent/auth.json")
AUTH_ENTRY = os.environ.get("VERAGENSIA_AUTH_ENTRY", "openai-codex")
CODEX_URL = os.environ.get(
    "VERAGENSIA_CODEX_URL", "https://chatgpt.com/backend-api/codex/responses")
MODEL = os.environ.get("VERAGENSIA_INTENT_MODEL", "gpt-5.6-luna")
EFFORT = os.environ.get("VERAGENSIA_INTENT_EFFORT", "max")
MAX_BODY = 32768
MAX_CONCURRENT = 4
CALL_TIMEOUT = 240

_state = {"active": 0}
_lock = threading.Lock()


def _credentials():
    with open(AUTH_PATH, "r", encoding="utf-8") as fh:
        auth = json.load(fh)
    entry = auth.get(AUTH_ENTRY) or {}
    token = entry.get("access")
    if not token:
        raise RuntimeError("subscription token unavailable")
    return token, entry.get("accountId", "")


def _codex_intent(instructions, user_input):
    token, account = _credentials()
    body = {
        "model": MODEL,
        "instructions": instructions,
        "input": [{"role": "user", "content": [
            {"type": "input_text", "text": user_input}]}],
        "store": False,
        "stream": True,
        "reasoning": {"effort": EFFORT},
    }
    req = urllib.request.Request(
        CODEX_URL, data=json.dumps(body).encode("utf-8"), method="POST",
        headers={
            "Authorization": "Bearer " + token,
            "chatgpt-account-id": account,
            "Content-Type": "application/json",
            "originator": "pi",
        })
    resp = urllib.request.urlopen(req, timeout=CALL_TIMEOUT)
    text, tokens, status, model = [], None, None, None
    for raw in resp:
        line = raw.decode("utf-8", errors="replace").strip()
        if not line.startswith("data:"):
            continue
        payload = line[5:].strip()
        if payload == "[DONE]":
            break
        try:
            event = json.loads(payload)
        except ValueError:
            continue
        kind = event.get("type", "")
        if kind == "response.output_text.delta":
            text.append(event.get("delta", ""))
        elif kind == "response.completed":
            data = event.get("response", {})
            status = data.get("status")
            usage = data.get("usage", {}) or {}
            tokens = usage.get("total_tokens")
            model = data.get("model")
            if not text:  # non-delta completions carry content inline
                text = [c.get("text", "") for item in data.get("output", [])
                        for c in (item.get("content") or [])
                        if isinstance(c, dict) and c.get("text")]
    if status and status != "completed":
        raise RuntimeError(f"codex_status_{status}")
    return {"text": "".join(text), "model": model or MODEL,
            "tokens": tokens, "status": status or "completed"}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _reply(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.startswith("/health"):
            self._reply(200, {"ok": True, "model": MODEL, "effort": EFFORT,
                              "active": _state["active"]})
        else:
            self._reply(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        if not self.path.startswith("/intent"):
            self._reply(404, {"ok": False, "error": "not_found"})
            return
        with _lock:
            if _state["active"] >= MAX_CONCURRENT:
                self._reply(503, {"ok": False, "error": "busy"})
                return
            _state["active"] += 1
        try:
            try:
                length = min(max(int(self.headers.get("Content-Length", 0)), 0), MAX_BODY)
            except (TypeError, ValueError):
                length = 0
            try:
                payload = json.loads(self.rfile.read(length) or b"{}")
            except (TypeError, ValueError):
                self._reply(400, {"ok": False, "error": "bad_json"})
                return
            instructions = str(payload.get("instructions", ""))[:8000]
            user_input = str(payload.get("input", ""))[:8000]
            if not user_input:
                self._reply(400, {"ok": False, "error": "empty_input"})
                return
            result = _codex_intent(instructions, user_input)
            self._reply(200, {"ok": True, **result})
        except Exception as exc:  # never leak secrets; log only the class
            print(f"intent-proxy failure: {type(exc).__name__}", file=sys.stderr, flush=True)
            try:
                self._reply(502, {"ok": False, "error": "upstream_failed"})
            except Exception:
                pass
        finally:
            with _lock:
                _state["active"] -= 1

    def log_message(self, fmt, *args):
        pass  # bounded logging: no transcripts, no secrets, no per-request noise


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8912), Handler)
    server.daemon_threads = True
    server.serve_forever()


if __name__ == "__main__":
    main()
