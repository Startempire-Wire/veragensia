#!/usr/bin/env python3
"""Veragensia append-only audit and transcription ledgers (docs/193, docs/201 T2).

One authoritative implementation for both ledgers:
- operations audit: every S4 execution attempt — including refusals and
  unknown-operation attempts — with a sha256 hash chain (tamper-evident).
- transcription: every recognized utterance, linked to the audit entry of
  the action it caused (transcript → action lineage, docs/201 §15 T2).

JSONL, append-only, bounded reads, no silent failures: a failed append is
reported in the returned envelope, never swallowed.
"""
import hashlib
import json
import os
from pathlib import Path
import time

AUDIT_SCHEMA = "veragensia.audit_entry.v1"
TRANSCRIPTION_SCHEMA = "veragensia.transcription_entry.v1"
DEFAULT_DIR = Path(os.environ.get("VERAGENSIA_AUDIT_DIR",
                                  "/config/.local/state/veragensia"))
OPERATIONS_LEDGER = "operations-audit.jsonl"
TRANSCRIPTIONS_LEDGER = "transcriptions.jsonl"
MAX_LINE_BYTES = 65536
MAX_TAIL = 512


def _line_hash(entry, prev_hash):
    material = json.dumps(entry, sort_keys=True, separators=(",", ":")) + prev_hash
    return hashlib.sha256(material.encode()).hexdigest()


def append(ledger_path, entry):
    """Append one entry with hash-chain integrity; returns the stored record."""
    path = Path(ledger_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    prev_hash = "0" * 64
    if path.exists():
        with path.open("rb") as source:
            for line in source:
                if line.strip():
                    try:
                        prev_hash = json.loads(line).get("entry_hash", prev_hash)
                    except ValueError:
                        pass
    seq = 0
    if path.exists():
        with path.open("rb") as source:
            for line in source:
                if line.strip():
                    seq += 1
    stored = dict(entry)
    stored["seq"] = seq
    stored["prev_hash"] = prev_hash
    stored["entry_hash"] = _line_hash({k: v for k, v in stored.items()}, prev_hash)
    blob = json.dumps(stored, sort_keys=True, separators=(",", ":")) + "\n"
    if len(blob) > MAX_LINE_BYTES:
        return {"status": "failed", "reason": "entry_oversized"}
    # O_APPEND single write: entries never rewrite earlier lines.
    try:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
        try:
            os.write(fd, blob.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)
    except OSError as exc:
        return {"status": "failed", "reason": f"open_or_write_failed: {exc}"}
    return {"status": "ok", "seq": seq, "prev_hash": prev_hash, "entry_hash": stored["entry_hash"]}


def tail(ledger_path, limit=64, verify=False):
    """Bounded newest-last read; optionally verify the hash chain."""
    path = Path(ledger_path)
    entries, broken = [], []
    if not path.exists():
        return {"schema": "veragensia.audit_tail.v1", "entries": [], "broken": [],
                "total": 0, "ledger": str(path)}
    lines = []
    with path.open("rb") as source:
        for line in source:
            if line.strip():
                lines.append(line)
    total = len(lines)
    prev_hash = "0" * 64
    for index, line in enumerate(lines):
        try:
            entry = json.loads(line)
        except ValueError:
            broken.append({"line": index, "reason": "invalid_json"})
            continue
        expected = _line_hash({k: v for k, v in entry.items()
                               if k != "entry_hash"}, entry.get("prev_hash", prev_hash))
        if verify:
            if entry.get("prev_hash") != prev_hash:
                broken.append({"seq": entry.get("seq"), "reason": "chain_break"})
            elif entry.get("entry_hash") != expected:
                broken.append({"seq": entry.get("seq"), "reason": "hash_mismatch"})
        prev_hash = entry.get("entry_hash", prev_hash)
        entries.append(entry)
    return {"schema": "veragensia.audit_tail.v1", "ledger": str(path),
            "total": total, "entries": entries[-limit:], "broken": broken}


def record_operation(audit_dir, result, actor, authority_ref=None):
    """Audit one S4 execution attempt (success, refusal, or failure)."""
    entry = {"schema": AUDIT_SCHEMA, "kind": "operation",
             "observed_at": result.get("observed_at"),
             "actor": actor,
             "operation_id": result.get("operation_id"),
             "status": result.get("status") or result.get("outcome"),
             "error": result.get("error"),
             "dispatcher": result.get("dispatcher"),
             "arg_sha256": result.get("arg_sha256"),
             "authority_ref_sha256": hashlib.sha256(authority_ref.encode()).hexdigest()[:16]
             if authority_ref else None,
             "authority_ref_present": result.get("authority_ref_present", False),
             "before": result.get("before"), "after": result.get("after")}
    outcome = append(Path(audit_dir) / OPERATIONS_LEDGER, entry)
    return {"audit_write": outcome.get("status"), "audit_seq": outcome.get("seq"),
            "audit_entry_hash": outcome.get("entry_hash"),
            "audit_failed_reason": outcome.get("reason")}


def record_transcription(audit_dir, text, engine, actor, confidence=None,
                         matched_operation_id=None, match_method=None,
                         audio_duration_ms=None, action_audit_seq=None):
    """Record one transcribed utterance and its action lineage."""
    entry = {"schema": TRANSCRIPTION_SCHEMA, "kind": "transcription",
             "observed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "actor": actor, "engine": engine,
             "text": str(text)[:512],
             "confidence": confidence,
             "matched_operation_id": matched_operation_id,
             "match_method": match_method,
             "audio_duration_ms": audio_duration_ms,
             "action_audit_seq": action_audit_seq}
    outcome = append(Path(audit_dir) / TRANSCRIPTIONS_LEDGER, entry)
    return outcome
