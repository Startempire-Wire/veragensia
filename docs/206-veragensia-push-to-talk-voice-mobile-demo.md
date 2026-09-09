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
| `overlay/webtop/voice-page-patch.py` | Idempotent page + nginx patches (button script tag; `/voice-gateway/` into every server block) |
| `tests/12-veragensia-voice-gateway-test.py` | Matcher + full lineage tests (5) |

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

- "go to workspace 2" … 1–9 (also "switch to workspace N")
- "move focus left/right/up/down", "move this window left/…"
- "close this window" → **refused** (medium risk; the gate proves itself and the refusal is audited)
- "make this fullscreen" / "take it out of fullscreen"
- "make this window float", "show the scratchpad", "open a terminal"

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

## 5. Live verification (2026-09-09)

Public path `POST https://os.focusa.dev/voice-gateway/command` executed
workspace travel, focus movement, fullscreen on/off; `close this window` was
**refused** by the authority gate and audited; transcription entries carry
`action_audit_seq` lineage into the operations ledger; chain verify intact.
