# 207 — Veragensia Voice Gateway → Spec 181 Conversation Ledger Mapping

**Status:** current mapping, 2026-09-09 · **Authority:** Sir V3 direction (voice planning docs/197, docs/200 §T0/T2, docs/201 §6–10; Focusa `docs/181-focusa-voice-conversation-expression-and-auditable-interaction-spec.md`, landed collision-free on focusa main)
**Scope:** maps the live, publicly verified Veragensia voice path (push-to-talk webtop demo, LLM intent, S4 semantic execution) onto Spec 181's object model, and names the next conformant slices. This is an implementation-truth document, not a new authority.

## 1. What is live today (verified 2026-09-09)

- Public page `https://os.focusa.dev` carries the 132×132 push-to-talk button baked into the webtop image; speech recognition runs in the phone browser (browser speech vendor), transcript goes only to the KH voice gateway and the KH-side OpenAI intent proxy.
- `voice-gateway.py` classifies natural language against the 22-operation semantic registry (`config/system-operations.json`) via the operator's OpenAI subscription (`llm:gpt-5.6-luna(max)`, KH proxy on the tailnet); regex matching remains as offline fallback.
- Execution is S4-only: `veragens-operations-exec.py` under `hyprland_dispatch`, with `authority_required` refusals for gated operations (e.g. closing windows), all hash-chained in `operations-audit.jsonl` (`veragensia.audit_entry.v1`).
- Every utterance lands in `transcriptions.jsonl` (`veragensia.transcription_entry.v1`) with `action_audit_seq` lineage back to the execution it caused, plus `intent_engine` / `intent_confidence`.

## 2. Spec 181 object → live implementation mapping

| Spec 181 object (§5, §6) | Live surface today | Conformance | Gap to close |
|---|---|---|---|
| `ConversationSession` | one bounded HTTP command per utterance; no durable session object | **partial** — sessions exist implicitly per request | durable session rows with lifecycle (`opened_at`/`ended_at`, surface, participant set) — T2 private lane |
| `ConversationParticipant` | stable `actor: voice-browser` (request JSON cannot spoof it) | **partial** — one pinned participant, no identity/authentication (§10) | voice identity/auth is out of demo scope; private lane |
| `AudioSegment` | not persisted; browser STT only returns text; `audio_duration_ms` is recorded | **partial** — duration yes, audio no | audio retention is privacy-gated (§15); intentionally deferred |
| `SpeechHypothesis` | browser STT transcript + `confidence` recorded when the vendor supplies it | **partial** | multiple hypotheses/rankings if a private STT lane ever lands |
| `UtteranceRecord` | transcription entry: `text`, `engine`, `confidence`, `matched_operation_id`, `match_method`, `intent_engine`, `intent_confidence`, `audio_duration_ms` | **strong** | add `session_ref` + stable `utterance_id` (see §4 below) |
| `TranscriptRevision` | append-only ledger keeps first-record truth; corrections are new entries, never edits | **strong** (append-only satisfies lineage) | explicit `revises` pointer when an operator-corrected transcript needs recording |
| `ExpressionOutput` | HTTP JSON response (`status`, `operation`, `args`, `authority_required`, `hint`) | **partial** — structured result only | `hint` is the seed of the spoken/visual expression path (§13 spoken result policy) |
| `SpokenOutput` | none (silent demo) | **absent** | Kokoro TTS (live `wirebot-wbt.service`, port 8119) is the designated renderer; not wired to the demo by design |
| **Conversation Ledger** | the pair of hash-chained ledgers: `transcriptions.jsonl` (utterances) + `operations-audit.jsonl` (consequences), joined by `action_audit_seq` | **architecture-equivalent** — same law: append-only, hash-chained, tamper-evident, value-bounded | rename/align field names toward Spec 181 vocabulary in a later schema version; do not break the live chain |
| Operation projection (§11) | natural language → registry match → S4 authority gate → execution → structured result | **strong** — this is exactly the Spec 181 §11 chain, minus the spoken reply | multi-operation batch (below) |

## 3. The chain, expressed in Spec 181 terms

```text
phone TALK button (hold)
→ AudioSegment (in-browser, ephemeral) → SpeechHypothesis (transcript + confidence)
→ ConversationParticipant(voice-browser) utters → UtteranceRecord appended (transcriptions.jsonl)
→ intent engine (llm:gpt-5.6-luna(max) via KH proxy; regex fallback) → matched operation
→ authority/consequence gate (S4; refusals recorded as first-class outcomes)
→ execution receipt (operations-audit.jsonl, hash-chained; action_audit_seq joins)
→ ExpressionOutput (HTTP JSON: status/args/hint)
```

Both ledgers already satisfy Spec 181 §6 Conversation Ledger invariants: append-only, hash-linked (`prev_hash`/`entry_hash`), bounded reads, no silent append failures, lineage from transcript to consequence.

## 4. `origin_utterance_ref` — canonical format for the batch slice

Spec 201 §6–10 requires every executed batch to reference the utterance that caused it. The live ledgers already contain the join key; the stable reference format is:

```text
origin_utterance_ref = "veragensia:transcriptions:<seq>"
```

where `<seq>` is the transcription ledger sequence number of the causing utterance (the same sequence that carries `action_audit_seq` pointing at the execution receipt). Properties: stable (append-only), resolvable by both veragens tooling and the audit reader, and leak-free (contains no content, only the handle). When the multi-operation batch slice (`SystemOperationBatch`) lands, each dispatched operation records `origin_utterance_ref` in its audit entry; the demo answers "which words caused this action?" for any operation from either ledger.

## 5. Conformance verdicts for today's demo

- **S4 authority gates:** conformant with Spec 181 §11 + Spec 201 — the LLM classifies; it never executes. Refusals (`authority_required`) are recorded, not swallowed.
- **Provider independence (§16):** conformant in architecture — the browser STT vendor and the OpenAI intent subscription are both replaceable adapters; the registry is the authority. The transcript destinations disclosed to the operator remain: phone browser speech vendor + OpenAI via the KH proxy. Nothing else receives transcripts.
- **Transcript truth (§7):** conformant — first-record truth, no destructive edits, revisions as new entries (none needed yet).
- **Privacy/retention (§15):** conformant by minimization — no audio persisted, transcripts value-bounded (512 chars) and retained only in the local hash-chained ledger; the ambient-voice proving ground stays private (docs/200), not `os.focusa.dev`.
- **Full-duplex/interruption (§8), floor control (§9), voice identity (§10):** not started — correctly out of the push-to-talk demo's scope; these belong to the T2 private trusted-audio lane.

## 6. Next conformant slices, in order

1. **SystemOperationBatch (multi-op):** one utterance may carry several registry operations ("put me on workspace 3 and make the window wider"); each dispatch records `origin_utterance_ref` per §4; per-operation refusal stays independent.
2. **ConversationSession schema v2:** durable per-surface session rows so utterances group into sessions without changing the hash chain (schema bump `veragensia.transcription_entry.v2` adds `session_ref`/`utterance_id`).
3. **ExpressionOutput alignment:** response envelope gains a `conversation` block echoing `utterance_id`, `session_ref`, and the human-readable result sentence Spec 181 §13 expects — the spoken path can then attach Kokoro without rework.
4. **T2 private lane (later):** trusted local audio (VoxType/whisper.cpp), voice identity (§10), full-duplex (§8) — private, never the public proving ground.
