# 206 — Veragensia push-to-talk voice for the mobile demo (T2 preview slice)

- **Status:** live on the public demo
- **Spec authority:** `docs/201` §14 V201-S4/S5 consumption, §15 T2 invariants (transcript/speaker/action lineage); `docs/197` voice-native direction; `docs/200` §1.5 proving-ground-first
- **Date:** 2026-09-09
- **Why:** mobile operators cannot use the streamed desktop's keyboard, scrolling, or a mouse. Voice is the usable input; the big push-to-talk button is the interface.

## 1. What exists

| Artifact | Role |
|---|---|
| `overlay/webtop/voice-gateway.py` | HTTP gateway: transcript → S2 registry match → S4 invoke (audited) → transcription ledger with lineage → desktop notification |
| `overlay/webtop/voice-gateway-loop.sh` | Supervisor; exec-once keeps it alive with the session (port 8900, loopback) |
| `overlay/selkies-web/veragensia-voice.js` | The push-to-talk button: 132px hold-to-talk circle, browser SpeechRecognition, vibration + color feedback, big status banner |
| `overlay/webtop/voice-page-patch.py` | Idempotent asset, page, and nginx patches (button script tag; `/voice-gateway/` into every server block) |
| `tests/12-veragensia-voice-gateway-test.py` | Matcher + full lineage tests (5) |
| `tests/13-veragensia-voice-delivery-static-test.py` | Restart-safe image/patch/supervisor contract tests |

## 2. Flow (phone → desktop)

```text
hold TALK button → phone mic (browser SpeechRecognition) → text
  → POST os.focusa.dev/voice-gateway/command  (nginx, same origin)
  → gateway: normalize → parameterized match (workspace N, directions)
     → else registry voice.examples → else label → else unmatched
  → S4 invoke (authority gate applies; refusal is audited)
  → transcription ledger entry + action lineage (audit seq)
  → hyprctl notify toast on the desktop + JSON result to the phone
```

## 3. Understanding the demo (say these)

Understanding is now an **LLM intent layer**, not a phrase list. The gateway
sends each transcript with the full operation registry to the operator's
OpenAI subscription (`gpt-5.6-luna`, max reasoning) through a KH-side intent
proxy, and the model returns `{operation_id, args, confidence}` — so natural
phrasings work: "can you put me on the third workspace please",
"hey um switch me over to workspace 5 thanks", "shrink the window a bit".
Useful examples (any natural phrasing is fine):

- workspace travel: "go to workspace 2" … "the third workspace"
- move a window: "move this window to workspace 4", "send it to workspace two"
- focus/move: "move focus left", "put the window on the right side"
- resize: "shrink the window a bit", "make it wider"
- windows: "make this fullscreen", "take it out of fullscreen", "make this window float"
- scratchpad: "show the scratchpad", terminal: "open a terminal"
- deliberately gated: "close this window" refuses without authority (audited)

If the LLM is unreachable the previous deterministic matcher still answers
exact phrasings (`regex_fallback` in the ledger); if both fail the utterance
is ledgered as `unmatched` and the phone shows a hint.

Architecture notes:

- The subscription credential lives only on KH in the Pi harness auth file
  and is refreshed there; the demo host holds **no model secrets**.
- The KH proxy (`ops/veragensia-intent-proxy.py`, systemd
  `veragensia-intent-proxy.service`, 127.0.0.1:8912, tailnet-only via
  `tailscale serve`) reads the token fresh per request, forwards one bounded
  intent call, and logs no transcripts and no secrets.
- The LLM only classifies intent. It never executes anything; consequence
  classes and the authority gate still govern every action (S4 unchanged).
- Transcripts go to the phone browser's speech service and, through the KH
  proxy, to OpenAI under the operator's subscription. Nothing else leaves
  the demo stack.

## 4. Honest limits

- **ASR is the phone browser's** (Chrome/Android and Safari/iOS both support
  the Web Speech API). Text leaves the phone to the browser vendor's speech
  service; nothing about the desktop leaves it. In-container whisper ASR is
  the follow-up slice for a self-contained path.
- Low-risk primitives only, by the registry's authority posture. Medium/high
  operations refuse under voice until an authority mechanism for the demo is
  deliberately designed (that is the gate working, not a bug).
- The unmatched case is ledgered too ("not understood" toasts on the desktop),
  so every attempt — understood or not — is in the record.

## 5. Restart durability and audit metadata

The demo image now carries the voice JavaScript asset in the Selkies
dashboard source, the page injection, and the same-origin nginx route in the
`/defaults` template at build time; the webtop startup copies those into the
runtime paths. `voice-page-patch.py` remains an idempotent runtime compatibility
guard and also copies a newer mounted asset when the source overlay changes.
The gateway supervisor retries after a transient process exit instead of
leaving the button with a dead endpoint.

The browser sends speech confidence and listening duration when available.
The HTTP layer ignores caller-supplied actor names and records the stable
`voice-browser` actor, so request JSON cannot spoof audit attribution. Gateway
exceptions return a bounded JSON failure instead of an empty browser response;
the failed transcription attempt is still recorded. The atomic container swap
archives any pre-existing rollback container under a timestamped name before
reusing `uiai-webtop.prev`, preserving rollback history across repeated swaps.

## 6. Live verification (2026-09-09)

Public path `POST https://os.focusa.dev/voice-gateway/command` executed
workspace travel, focus movement, fullscreen on/off; `close this window` was
**refused** by the authority gate and audited; transcription entries carry
`action_audit_seq` lineage into the operations ledger; chain verify intact.
The restart-safe image was built as
`sha256:0603908824c472f8b77a5eecb9eda97ef86b36b7f9a04aa6dda1c0d0a1071b35`,
atomically swapped, and verified through the public route plus a local CDP
PNG capture showing the visible 132×132 TALK button.

LLM intent verification (same public path, gpt-5.6-luna at max reasoning):
"can you put me on the third workspace please" → `workspace.activate 3` ok;
"hey um switch me over to workspace 1 thanks" → ok; "shrink the window a bit"
and "make the window wider please" → `resize_active` ok (deltas split into
hyprctl tokens); "move the window over to the right side" → ok;
"close this window" → `refused / authority_required` (gate intact, audited);
"what is the meaning of life" → honest `llm_unmatched` with a hint. Ledger
entries record `intent_engine` and `intent_confidence`; audit chain verified
unbroken after every attempt.
