#!/usr/bin/env python3
"""Doc 201 V201-S1: bounded diagnostics, never desktop control."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import stat
import subprocess
import time
from datetime import datetime, timezone

SCHEMA = "veragensia.omarchy_inventory.v1"
# Upstream f4378f0 produces 283 command records / 137295 JSON bytes.
MAX_BYTES = 262144
MAX_ITEMS = 512
TIMEOUT = 2.0
MIME_TYPES = ("text/plain", "text/html", "x-scheme-handler/http")


def digest(value):
    return hashlib.sha256(value).hexdigest()


def probe(argv, timeout=TIMEOUT, max_bytes=MAX_BYTES):
    """Fixed argv only; cap combined output and kill the process group on failure."""
    executable = shutil.which(argv[0])
    if executable is None:
        return {"status": "unavailable"}, b""
    deadline = time.monotonic() + timeout
    try:
        child = subprocess.Popen(
            [executable, *argv[1:]], stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True,
        )
    except OSError:
        return {"status": "error", "reason": "spawn_failed"}, b""
    output = bytearray()
    total = 0
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
                    chunk = os.read(key.fd, min(4096, max_bytes - total + 1))
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    total += len(chunk)
                    if total > max_bytes:
                        failure = "oversized"
                        break
                    if key.data:
                        output.extend(chunk)
                if failure:
                    break
        if not failure:
            try:
                child.wait(timeout=max(0.001, deadline - time.monotonic()))
            except subprocess.TimeoutExpired:
                failure = "timeout"
    finally:
        if failure or child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass  # Already reaped; no live process group remains.
        child.wait()
        child.stdout.close()
        child.stderr.close()
    if failure:
        return {"status": failure}, b""
    if child.returncode:
        return {"status": "error", "exit_code": child.returncode}, b""
    return {"status": "ok"}, bytes(output)


def json_probe(argv, runner):
    state, raw = runner(argv)
    if state["status"] != "ok":
        return state, None
    try:
        return state, json.loads(raw)
    except (ValueError, UnicodeError, RecursionError):
        return {"status": "invalid_json"}, None


def identifier(value):
    return isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9_ .:/+-]{1,128}", value)


def commands(runner):
    state, data = json_probe(["omarchy", "commands", "--all", "--json"], runner)
    if state["status"] != "ok":
        return state
    rows = data.get("commands") if isinstance(data, dict) else data
    if not isinstance(rows, list):
        return {"status": "unsupported_schema"}
    items = []
    rejected = 0
    for row in rows[:MAX_ITEMS]:
        name = (row if isinstance(row, str) else
                row.get("route", row.get("name")) if isinstance(row, dict) else None)
        if not identifier(name):
            rejected += 1
            continue
        items.append({"name": name})
    return {"status": "ok" if items and not rejected else "incomplete",
            "items": items, "total": len(rows), "rejected": rejected,
            "truncated": len(rows) > MAX_ITEMS}


def bindings(runner):
    state, rows = json_probe(["hyprctl", "-j", "binds"], runner)
    if state["status"] != "ok":
        return state
    if not isinstance(rows, list):
        return {"status": "unsupported_schema"}
    items = []
    rejected = 0
    for row in rows[:MAX_ITEMS]:
        if not isinstance(row, dict) or not identifier(row.get("dispatcher")):
            rejected += 1
            continue
        key = row.get("key", "")
        if not isinstance(key, str) or len(key) > 64 or any(ord(c) < 32 for c in key):
            rejected += 1
            continue
        item = {"key": key, "dispatcher": row["dispatcher"]}
        for field in ("modmask", "keycode"):
            value = row.get(field)
            if type(value) is int and 0 <= value <= 65535:
                item[field] = value
        # Arguments can contain passwords, shell programs or private paths.
        # Retain change identity, not their values; never execute a binding.
        if isinstance(row.get("arg"), str):
            item["argument_sha256"] = digest(row["arg"].encode())
        items.append(item)
    return {"status": "ok" if items and not rejected else "incomplete",
            "items": items, "total": len(rows), "rejected": rejected,
            "truncated": len(rows) > MAX_ITEMS}


def override_metadata(home):
    path = Path(home) / ".config/hypr/bindings.lua"
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
    except FileNotFoundError:
        return {"status": "absent"}
    except OSError:
        return {"status": "unreadable"}
    with os.fdopen(fd, "rb") as source:
        info = os.fstat(source.fileno())
        if not stat.S_ISREG(info.st_mode):
            return {"status": "unsupported_file_type"}
        raw = source.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        return {"status": "oversized"}
    return {"status": "ok", "bytes": len(raw), "sha256": digest(raw),
            "content_included": False}


def defaults(runner):
    items = []
    for mime in MIME_TYPES:
        state, raw = runner(["xdg-mime", "query", "default", mime])
        item = {"mime": mime, **state}
        if state["status"] == "ok":
            try:
                desktop = raw.decode("utf-8").strip()
            except UnicodeError:
                desktop = ""
            if re.fullmatch(r"[A-Za-z0-9_.+-]{1,128}\.desktop", desktop):
                item["desktop_id"] = desktop
            else:
                item["status"] = "unresolved"
        items.append(item)
    return {"status": "ok" if all(i["status"] == "ok" for i in items) else "incomplete",
            "items": items}


def inventory(home, runner=probe):
    sources = {"omarchy_commands": commands(runner), "hyprland_bindings": bindings(runner),
               "user_overrides": override_metadata(home), "app_defaults": defaults(runner)}
    signature = os.environ.get("HYPRLAND_INSTANCE_SIGNATURE", "")
    complete = bool(signature) and all(
        value["status"] == "ok" and not value.get("truncated", False)
        for key, value in sources.items() if key != "user_overrides"
    ) and sources["user_overrides"]["status"] in ("ok", "absent")
    return {"schema": SCHEMA, "observed_at": datetime.now(timezone.utc).isoformat(),
            "status": "observed" if complete else "degraded", "qualification": "not_performed",
            "runtime_ref": digest(signature.encode()) if signature else None,
            "limits": {"bytes_per_probe": MAX_BYTES, "items_per_source": MAX_ITEMS,
                       "seconds_per_probe": TIMEOUT},
            "sources": sources}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-complete", action="store_true",
                        help="exit 2 when any required diagnostic source is incomplete")
    args = parser.parse_args()
    report = inventory(Path.home())
    print(json.dumps(report, sort_keys=True))
    return 2 if args.require_complete and report["status"] != "observed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
