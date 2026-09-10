# 205 — Veragensia operation execution, audit, and transcription (V201-S4 slice 1)

- **Status:** implemented and live on the demo proving ground
- **Spec authority:** `docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md` §14 V201-S4, §15 invariants 5/5.5/5.6; `docs/193` execution substrate
- **Date:** 2026-09-09

## 1. What exists

| Artifact | Role |
|---|---|
| `scripts/veragens-operations-exec.py` | hyprland_dispatch execution: read-verified dispatch, authority gate, fenced batches, audit hook |
| `config/operation-execution.json` | Operation→dispatcher bindings with `none`/`literal`/`fixed` arg modes |
| `scripts/veragens-audit.py` | One append-only hash-chained JSONL ledger implementation for both the operations audit and transcriptions |
| `scripts/veragens` | `operation invoke <id> [args] --authority-ref?`, `operation batch --file --fence`, `operation audit [--verify]` |
| `tests/11-veragensia-operation-execution-test.py` | 9 contract tests: gate, args, snapshots, fence, tamper detection, refusal auditing, lineage |

## 2. Agent control semantics

- **Read-verified dispatch (§15.6):** window/workspace operations snapshot the
  relevant compositor state (`hyprctl -j activewindow` / `activeworkspace`)
  before and after the dispatch; the result envelope carries both so the
  caller can verify the claimed effect instead of trusting it.
- **Authority gate:** the registry's declared posture is enforced at
  invocation — `medium`/`high` consequence operations refuse without
  `--authority-ref`. **Refusals are audited like executions.** Low-risk
  reversible primitives (focus, workspace travel, layout toggles) invoke freely.
- **Argument hardening:** caller args are bounded (≤4, ≤64 chars, strict
  charset), `none`-mode bindings reject any args, `fixed`-mode bindings
  ignore caller args and dispatch their declared fixed command.
- **Fenced batches (§15.5):** a batch checks the fence file between steps; an
  existing fence aborts before the next operation. A hard cap bounds runs.

## 3. Audit and transcription (transcript→action lineage)

`veragens-audit.py` is the single ledger implementation (DRY): append-only
JSONL, `O_APPEND` single writes, sha256 hash chain (`prev_hash` +
`entry_hash`), bounded tail reads with chain verification. Tampering with
any historical line breaks the chain at that point and `audit --verify`
reports it.

- **Operations ledger** (`operations-audit.jsonl`): every attempt — ok,
  refused, failed, unknown — with actor, authority presence, dispatcher,
  argument digest, and before/after state.
- **Transcription ledger** (`transcriptions.jsonl`): every recognized
  utterance with engine, text, confidence, matched operation id, match
  method, and the audit seq of the action it caused — the T2 lineage
  requirement, ready before the voice daemon lands.

Ledgers live under `/config/.local/state/veragensia/` (the persisted
`/config` volume) so audit history survives container swaps.

## 4. Live verification (demo proving ground, 2026-09-09)

- Full primitive demo keymap: **36 bindings**, S1 inventory count 36, S3
  classification **36 semantic_operation / 0 unmapped_gap**.
- Live invocations: `focus_direction r` (foot↔chromium focus verified in
  snapshots), `workspace.activate 2` (ws 1→2 verified), `workspace.activate 1`
  (return), and `session.exit` **refused** (high consequence, no authority)
  — refusal audited as entry 2.
- `operation audit --verify`: 4 entries at the S4 slice proof, chain intact; the live ledger has since grown (22 entries verified 2026-09-09, chain still intact — see docs/207).

## 5. Deliberately not in this slice

- ASR/voice daemon: next slice; consumes the transcription ledger contract
  and the same S2/S4 path (voice → registry match → invoke → audited).
- Non-hyprland adapters (`focusa_operation`, `native_service`,
  `application_protocol`): unbound operations return `adapter_unavailable`.
- No credential or secret ever enters a ledger line; authority references
  are stored as truncated hashes with a presence flag.
