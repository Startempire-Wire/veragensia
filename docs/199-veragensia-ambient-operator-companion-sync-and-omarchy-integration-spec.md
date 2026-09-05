# 199 — Veragensia Ambient Operator, Companion Sync, and Omarchy Integration Specification

**Status:** DRAFT canonical product direction, 2026-09-05.  
**Canonical human architecture authority:** Verious Smith III under Doc 185.  
**Focusa dependencies:** Spec 181 Voice/Conversation, Spec 182 Project Foreman, Spec 183 Radar, Spec 184 Ambient Operator, Spec 139 Presence/Placement, Spec 164 Workstream Root, Spec 53 pairing, Spec 136 settlement, Spec 156 credentials.  
**Veragensia dependencies:** Docs 190–198.  
**UIAI dependency:** canonical UIAI Engine Agent-First Browser/computer-control contracts and `UIAI_VERAGENSIA_COMPUTER_CONTROL_AND_VOICE_BINDING_2026-09-04.md`.  
**Reference mobile/context adapters:** Wirebot Core Context Core, Phone Bridge, and current `wbt` voice runtime.  
**Base target:** stock supported Omarchy/Arch/Hyprland/Quickshell; no deep fork.

---

## 0. One-line definition

> **Ambient Operator is the embodied edge of the Veragensia Agent Computer: a paired mobile/wearable surface that carries bounded human presence, auditable conversation, proactive Radar attention, Wirebot/Foreman interaction, and voice-first control into and out of the same Focusa-governed operating environment without creating a second cognition, authority, or execution stack.**

The phone can leave the desk. The Agent Computer remains one governed organism.

---

## 1. Canonical system composition

```text
                            HUMAN
                              |
                  +-----------+-----------+
                  |                       |
              EARBUDS                  MOBILE
              audio I/O          sensors / UI / queue
                  |                       |
                  +-----------+-----------+
                              |
                      FOCUSA AMBIENT OPERATOR
                    Spec 184 / Spec 181 voice
                              |
               +--------------+--------------+
               |                             |
            WIREBOT                       FOREMAN
         Chief of Staff                 Workstream role
               |                             |
               +--------------+--------------+
                              |
                           FOCUSA
        Workstream · Workpoint · authority · Radar · Evidence
                              |
                +-------------+-------------+
                |                           |
          VERAGENSIA                    UIAI ENGINE
       Linux/Omarchy host          browser/computer execution
       enforcement/control             proof/diagnostics
                |                           |
                +-------------+-------------+
                              |
                      Agent Apps / workers
```

No arrow grants authority by transport alone.

---

## 2. Responsibility map

### Focusa owns

- Workstream/project identity and current Workpoint;
- Project Foreman role projection;
- Radar Signals/Episodes;
- Voice/Conversation/Conversation Ledger semantics;
- ExpressionOutput;
- Context Authority and capability decisions;
- Evidence/Receipts/settlement references;
- pairing semantics where Focusa is the pairing owner.

### Veragensia owns

- Linux process/service placement and machine enforcement;
- Omarchy/Hyprland/Quickshell integration;
- trusted desktop audio-device brokering;
- local Companion sync service;
- ResourceRef/runtime-incarnation mapping;
- Secure Attention/human-control reserve;
- local Agent Computer lifecycle;
- profile readiness and capability composition.

### UIAI Engine owns

- browser/computer execution in its domain;
- UIAI observations and semantic refs;
- browser control leases;
- diagnostics, execution capsules and proof;
- FPV/remote browser control surfaces where authorized.

### Wirebot/Context Core owns in the Startempire reference deployment

- broad owner/life/business Chief-of-Staff context outside one Focusa Workstream;
- raw phone sensor/location context when configured there;
- current operator-context derivation such as coarse place/activity/interruptibility;
- cross-project delegation to exact Foremen.

Wirebot Context Core MUST NOT become a second Focusa Workstream store or authorization engine.

---

## 3. Omarchy integration law

Veragensia consumes Omarchy through supported user/plugin/session integration points. It does not fork the desktop to gain ambient capability.

### 3.1 Omarchy shell plugin is presentation, not trust boundary

The proposed native plugin:

```text
~/.config/omarchy/plugins/veragensia.ambient/
    manifest.json
    Status.qml
    AmbientPanel.qml
```

may project:

- Focusa/Foreman binding;
- Radar attention count/state;
- current voice/listening mode;
- paired Companion health;
- active conversation/meeting indicator;
- microphone/output route state;
- sync state;
- human takeover/stop affordances;
- degraded/stale warnings.

It MUST NOT own:

- Focusa canonical state;
- raw credential material;
- trusted microphone authorization;
- speaker identity authority;
- CapabilityGrant evaluation;
- EnforcementPlan compilation;
- Secure Attention decisions;
- direct reducer/database writes;
- general shell-command execution from arbitrary UI payloads.

### 3.2 Why

Omarchy/Quickshell plugins execute as user-space shell code and are not an isolation boundary. Therefore Veragensia treats the plugin as an **untrusted-capable presenter within the owner session**, even when it is first-party.

A visually identical third-party QML surface must never be sufficient to impersonate a trusted approval/audio authority.

### 3.3 Supported shell interaction

The plugin should use the supported Omarchy shell/plugin lifecycle, manifest validation and shell IPC rather than patching package-owned source.

Veragensia-specific native operations remain behind typed IPC/service APIs so the same actions can be projected through:

```text
Omarchy plugin
Focusa Desktop
voice
mobile
CLI/API
```

without QML-only business logic.

---

## 4. Native service topology

The full desktop profile converges on a small number of bounded services rather than placing trusted behavior in the shell plugin.

```text
focusa-daemon
    canonical cognition / authority / conversation / Radar / Foreman

veragens-sessiond
    owner-session projection + Omarchy/Hyprland integration

veragens-audiod
    trusted desktop audio endpoint broker / capture / playback boundary

veragens-syncd
    paired Companion sync / offline queue reconciliation

uiai-engine
    browser/computer execution + proof

Pi + Focusa extension
    reference agent harness
```

Names are implementation direction and may change behind stable service contracts.

### 4.1 `veragens-sessiond`

Responsibilities:

- bridge Focusa projections to native shell;
- expose semantic shell/window/workspace operations;
- collect bounded session/device facts;
- maintain runtime incarnation/epoch;
- coordinate local Secure Attention presentation with Doc 194;
- never become canonical Workpoint/Foreman/Radar state.

### 4.2 `veragens-audiod`

Responsibilities:

- enumerate trusted audio endpoints;
- resolve microphone/speaker/headset routes;
- expose hardware mute/route changes;
- mediate trusted capture/playback sessions;
- connect audio streams to Focusa Spec-181 conversation adapters;
- reserve/duck playback for Secure Attention where policy allows;
- expose capture/playback health;
- bind every privileged capture to WorkloadIdentity/EnforcementPlan.

It is **not** the ASR/TTS semantic owner. ASR/TTS providers are adapters.

### 4.3 `veragens-syncd`

Responsibilities:

- paired-device authentication;
- encrypted event/delta transport;
- replay protection and idempotency;
- offline queue acknowledgement;
- Conversation/Ambient envelope routing;
- bounded presence projection ingestion;
- LAN/Tailscale/relay transport selection;
- no direct Focusa database synchronization.

---

## 5. Linux enforcement profile

Ambient/voice capability is subject to Doc 193 like every other capability.

### 5.1 Trusted audio capture workload

`veragens-audiod` or an equivalent trusted capture workload receives only the microphone/device capabilities required by the active profile/policy.

Ordinary agents, Agent Apps, browser pages, Pi workers and Omarchy plugins do not inherit that microphone capability.

### 5.2 Companion sync workload

`veragens-syncd` receives:

- paired-device transport access;
- bounded local conversation/presence queue access;
- Focusa operation/API access required for sync reconciliation;
- no arbitrary `$HOME` or credential-store access.

### 5.3 Human-control reserve

The local stop/takeover/audio-status path remains in the protected human-control resource class. Agent load cannot starve:

- Focusa intervention;
- Secure Attention;
- audio mute/stop;
- Companion revocation;
- computer-control fencing.

---

## 6. Audio stack integration

On the Omarchy/Arch target, Veragensia treats the desktop audio stack as a runtime dependency to inspect rather than a fixed assumption.

Required preflight records:

```text
audio server/provider
session manager
Bluetooth service/adapter
input endpoints
output endpoints
headset profiles/codecs
microphone availability
hardware mute state when exposed
echo-cancellation capability
sample rates/channel modes
route-change behavior
```

The reference target is expected to use the normal modern Linux PipeWire/WirePlumber/BlueZ stack, but `veragens doctor` MUST report observed reality.

A Bluetooth device being connected does not prove its microphone profile is active or suitable for full-duplex speech.

---

## 7. Audio endpoint lifecycle

Audio endpoint identity follows Doc 197/195.

Events include:

```text
endpoint_discovered
endpoint_connected
route_selected
capture_started
capture_stopped
profile_changed
route_changed
bluetooth_disconnected
hardware_mute_changed
audio_interrupted
endpoint_replaced
```

A headset disconnect during a private spoken response MUST NOT silently reroute sensitive output to laptop speakers unless policy explicitly permits it.

A route change invalidates applicable capture/playback assumptions and may pause the ConversationSession.

---

## 8. Voice bootstrap versus canonical voice runtime

An existing dictation utility or desktop STT tool MAY be used as an early adapter for transcription experiments.

It MUST NOT define the canonical architecture because simple dictation usually lacks:

- ConversationSession identity;
- multi-speaker attribution;
- full-duplex floor/interruption semantics;
- ExpressionOutput lineage;
- Radar/Foreman identity routing;
- Secure Attention integration;
- meeting retention policy;
- utterance → action → Receipt lineage.

The full profile always converges on Focusa Spec 181 + Veragensia Doc 197/199.

---

## 9. Mobile Companion architecture

The mobile Companion is a paired edge runtime, not a miniature remote desktop by default.

Core local responsibilities:

- device identity/pairing;
- microphone/audio route integration;
- wake/PTT/conversation/meeting modes;
- local capture indicators and privacy controls;
- optional local wake/VAD/ASR/TTS adapters;
- encrypted offline queue;
- bounded Context Core sensor adapter;
- Radar/Foreman/Wirebot interaction UI;
- secure sync to the owner Focusa/Veragensia environment.

It MUST NOT persist Focusa authority state as an independent source of truth.

---

## 10. Android reference implementation direction

Android is the first reference mobile implementation because the Startempire deployment already has a working Android/Termux Phone Bridge and sensor model.

### 10.1 Legacy Phone Bridge remains context-only

The current Phone Bridge pattern continues as a useful prototype for:

- battery;
- DND;
- driving;
- meeting/manual mode;
- context note;
- location-derived owner context.

Do **not** add continuous raw microphone/audio upload to `/signals/phone`.

### 10.2 Native Companion required for full audio profile

A production `ambient_voice`/`meeting_capture` Android profile requires a native mobile app/service because mobile OS microphone/background-lifecycle policy cannot be modeled reliably as a shell cron job.

The app must explicitly model:

```text
foreground_active
ambient_ready
wake_listening
active_conversation
meeting_recording
audio_interrupted
background_restricted
suspended_by_platform
offline
recovering
```

The system reports actual platform state rather than promising an immortal “always listening” process.

### 10.3 Foreground/privacy UX

When the platform requires a visible foreground service/recording indicator, that is part of the product's truthful privacy surface, not something to hide.

---

## 11. iOS parity direction

The same Ambient/Conversation contracts apply on iOS, but background audio/location and app-lifecycle behavior are implemented through supported Apple APIs and entitlements.

No private Apple APIs or undocumented bypasses are allowed.

A parity matrix records which modes are:

```text
full
restricted
foreground_only
unsupported
```

on each qualified OS version.

---

## 12. Sync topology

Preferred transport selection:

```text
same trusted LAN / direct local route
        ↓
private overlay network such as Tailscale
        ↓
explicitly enabled relay
        ↓
offline encrypted queue until reachable
```

BLE/Bluetooth may support:

- nearby discovery;
- proximity;
- pairing assistance;
- small state/control messages;
- emergency/local status where implemented.

Bluetooth is not the required bulk transport for meeting audio, transcript history, Evidence or workspaces.

---

## 13. Sync state machine

```text
unpaired
→ pairing
→ paired
→ connected
→ syncing
→ current

connected/current
→ offline_queued
→ reconnecting
→ reconciling
→ current

any
→ revoked
```

Every queued envelope carries source device identity, sequence/idempotency, privacy class, scope and content handles.

Sync success is established by acknowledgement/reconciliation, not by successful local write to an outbound queue.

---

## 14. Desktop/mobile conversation continuity

A ConversationSession may move between:

```text
phone speaker
Bluetooth earbuds
laptop microphone/speaker
remote Agent Computer audio
```

without changing the underlying Focusa conversation identity.

Every capture/render segment still records:

- endpoint/device;
- node/runtime incarnation;
- participant principal;
- ASR/TTS adapter;
- timing/provenance;
- retention/privacy policy.

Changing endpoint does not transfer stale control/credential authority.

---

## 15. Meeting mode

Meeting mode uses Focusa Spec 184/181.

Veragensia/mobile runtime supplies:

- capture lifecycle;
- audio-device routing;
- local encrypted storage;
- chunking/upload/sync;
- battery/storage/thermal policy;
- platform interruption handling.

Focusa supplies:

- ConversationSession;
- speaker/utterance/transcript lineage;
- meeting candidate extraction;
- explicit promotion path;
- Evidence/action/Receipt links.

Radar may observe structured meeting-derived candidates; it does not ingest raw meeting audio by default.

---

## 16. Wirebot / Foreman identity routing

Ambient speech can address either portfolio/life intelligence or exact project intelligence.

```text
"Wirebot, what needs my attention?"
        → Chief-of-Staff route

"Foreman, where are we on Veragensia?"
        → exact Workstream Foreman route
```

The mobile/desktop client sends an address/intention proposal. Focusa/Wirebot scope resolution determines the exact principal and Workstream before action.

An unqualified `Foreman` with more than one plausible Workstream returns clarification.

---

## 17. Radar ambient attention

Radar interruption packets sent to Ambient Operator SHOULD contain only what is required to decide whether to engage:

```yaml
schema: veragensia.ambient_attention_packet.v1
signal_ref:
workstream_ref:
foreman_ref:
summary:
why_now:
urgency:
confidence:
prepared_action_ref:
authority_required:
privacy_class:
expires_at:
```

A typical interaction:

```text
Radar detects deployment instability
→ Foreman investigates
→ prepared low-risk repair exists
→ owner interruptibility becomes high
→ earbuds: "Veragensia Foreman needs one decision..."
→ owner asks details/approves/denies
→ normal Focusa authority/execution path
```

No notification payload may become authority merely because it was spoken aloud.

---

## 18. UIAI Engine path

Ambient/mobile requests that require browser/computer action use the normal UIAI path:

```text
speech/mobile intent
→ Focusa utterance/current ask
→ Foreman/Wirebot resolution
→ Focusa authority
→ Veragensia execution-surface resolver
→ UIAI observation/action/control lease
→ UIAI Evidence/diagnostics
→ Focusa settlement/Receipt
→ ExpressionOutput
→ mobile/earbud spoken response
```

Mobile does not directly remote-control UIAI by issuing ungoverned pointer commands.

An authorized mobile UI MAY receive a bounded FPV/observation stream and request takeover through the same fenced UIAI/Veragensia control-lease model.

---

## 19. Omarchy native Ambient panel

The native panel is intentionally small.

Suggested information architecture:

```text
Ambient
  Foreman: Veragensia
  Voice: wake-word / muted / conversation
  Companion: Pixel 9 · current 4s
  Earbuds: connected · mic ready
  Radar: 2 signals · 1 needs you
  Sync: current
  Trust: T1 developer

  [Talk]
  [Mute]
  [Attention]
  [Open Focusa Desktop]
  [Stop agents]
```

Every mutation goes through typed service/Focusa operations.

No secrets/raw transcript are required in the bar widget.

---

## 20. Secure Attention limitation on stock Omarchy plugin

A normal Quickshell plugin cannot by itself constitute a hardened Secure Attention Plane because it shares the user's shell/runtime trust boundary.

Therefore profiles distinguish:

```text
secure_attention_ux_presenter
    developer/preview indication and operation forwarding

secure_attention_hardened
    separately proven OS/compositor/device trust path
```

Native v0.1 and early Omarchy builds MUST NOT claim hardened Secure Attention merely because a QML panel visually looks trusted.

---

## 21. Platform trust on current Omarchy target

The normal reclaimed/owner-controlled Omarchy development target begins at:

```text
T1_DEVELOPER
```

unless stronger signed/measured/hardware-attested boot is separately implemented and evidenced under Doc 196.

Installing Omarchy or using full-disk encryption does not automatically raise the trust class.

The Agent Computer remains useful at T1 while higher-consequence profiles may require stronger trust.

---

## 22. Profile capability declarations

Example full profile extension:

```yaml
profile: personal_agent_computer

interaction:
  voice_complete: true
  ambient_operator: true
  meeting_capture: opt_in

companion:
  mobile_required: false
  nearby_sync: true
  private_network_sync: true

focusa:
  foreman: true
  radar: true
  conversation_ledger: true

privacy:
  wake_pretrigger_retention: none
  raw_audio_default: session_policy
  precise_location_default: owner_context_only
```

Capability availability is reported truthfully from installed/runtime evidence.

---

## 23. `veragens doctor` Ambient checks

Future native doctor output SHOULD include:

```text
omarchy_shell_supported
ambient_plugin_valid
focusa_daemon_ready
foreman_operations_ready
radar_operations_ready
conversation_operations_ready
sessiond_ready
audiod_ready
syncd_ready
audio_input_ready
audio_output_ready
bluetooth_ready
headset_mic_ready
companion_pairing_ready
private_sync_route_ready
uiai_ready
voice_complete_status
secure_attention_class
platform_trust_class
```

No single green health endpoint substitutes for the whole profile.

---

## 24. Implementation slices

These are **implementation/acceptance slices**, not a parallel task database. Materialize them into repository-local `br` with exact dependencies before code work begins.

### V199-S1 — Omarchy plugin skeleton

Target:

```text
overlay/omarchy/plugins/veragensia.ambient/
```

Deliver:

- manifest;
- compact bar/status component;
- Ambient panel;
- validation fixture/test;
- no direct Focusa DB/API secrets;
- typed IPC client only.

Done when the plugin loads/unloads/rescans on the qualified Omarchy shell without modifying upstream package-owned files.

### V199-S2 — Native session bridge

Target:

```text
overlay/omarchy/services/veragens-session.service
native/session bridge implementation
```

Deliver:

- Focusa projection stream;
- shell summon/toggle/open operations;
- runtime epoch/incarnation;
- stale/degraded posture;
- semantic window/workspace operation facade;
- restart recovery.

### V199-S3 — Audio endpoint broker and preflight

Deliver:

- audio endpoint inventory;
- PipeWire/session-manager/Bluetooth observed posture;
- headset mic/profile diagnostics;
- route-change events;
- trusted capture/playback session contract;
- microphone denied to unrelated test workload;
- privacy indicator tests.

### V199-S4 — Focusa conversation binding

Deliver:

- trusted audio stream → Spec-181 AudioSegment/SpeechHypothesis/Utterance path;
- ExpressionOutput → TTS/playback path;
- interruption/barge-in;
- endpoint/provenance refs;
- no second conversation store in Veragensia.

### V199-S5 — Companion sync service

Deliver:

- paired-device authentication;
- AmbientSyncEnvelope transport;
- sequence/replay/idempotency;
- encrypted offline queue;
- LAN/Tailscale route selection;
- reconciliation/ack receipts;
- revocation.

### V199-S6 — Android Companion alpha

Reference implementation:

- native Android application;
- context-only, PTT, wake, conversation, meeting modes;
- background/foreground state machine;
- Bluetooth audio route handling;
- local indicators;
- encrypted queue;
- private-network sync;
- Context Core adapter;
- no raw-audio use of legacy Phone Bridge endpoint.

### V199-S7 — Foreman/Radar Ambient route

Deliver:

- Workstream Foreman selector;
- Wirebot vs Foreman routing;
- Radar Attention packet;
- interruptibility-aware delivery;
- voice/text parity;
- Evidence-backed status answers.

### V199-S8 — Meeting flight-recorder path

Deliver:

- meeting capture/session start-stop;
- diarization/speaker confidence;
- transcript correction lineage;
- raw-audio retention modes;
- candidate extraction;
- no automatic Workpoint/policy promotion;
- local restart/offline recovery.

### V199-S9 — UIAI voice/mobile execution

Deliver one end-to-end mobile request that:

```text
spoken request
→ Focusa Foreman
→ UIAI action
→ UIAI verification
→ Receipt
→ spoken result
```

and one takeover test with fencing/re-observation.

### V199-S10 — Enforcement/trust closure

Deliver:

- WorkloadIdentity/EnforcementPlan for audio/sync services;
- no ambient same-UID microphone authority for worker processes;
- explicit T1 baseline;
- first-party compatibility bundle entries;
- service digest/attestation evidence.

### V199-S11 — Voice-complete Ambient Agent Computer dogfood

Without keyboard/pointer for the representative path:

```text
wake/talk
→ choose Workstream Foreman
→ ask status
→ Radar surfaces useful issue
→ delegate worker
→ UIAI/browser action
→ review Evidence
→ approve bounded action
→ receive verified spoken result
→ search Conversation Ledger
```

### V199-S12 — iOS + wearable hardware parity

After Android/reference closure:

- supported iOS implementation;
- platform capability matrix;
- commodity-earbud parity;
- optional purpose-built wearable contract;
- physical secure-control research/proof.

---

## 25. Cross-repository implementation allocation

| Concern | Canonical repo/owner |
|---|---|
| Foreman/Radar/Ambient/Conversation semantics | `Startempire-Wire/focusa` |
| Linux/Omarchy/audio/sync/enforcement integration | `Startempire-Wire/veragensia` |
| browser/computer actuator + proof | `WPUIAI/uiai-engine` |
| Startempire Chief-of-Staff/context/legacy phone + voice adapters | `Startempire-Wire/wirebot-core` |
| portable client/deployment contract | `Startempire-Wire/agent-driven-life-business-os` |

Implementation must move behavior to the primitive owner rather than reproduce it in every repository.

---

## 26. Acceptance invariants

The integrated Ambient Agent Computer is valid only when:

1. Omarchy plugin is a presenter and cannot become a hidden authority/secret/microphone owner;
2. Focusa remains canonical owner of Foreman/Radar/Conversation semantics;
3. UIAI remains browser/computer execution/proof owner;
4. raw phone context remains in its owner domain and reaches Focusa through bounded projections;
5. mobile sync cannot write Focusa persistence directly;
6. microphone capability is limited to trusted capture workload/profile;
7. wake-word mode can operate without durable pre-trigger room recording by default;
8. headset route changes cannot silently disclose private audio;
9. offline mobile work is marked stale/queued and reconciles idempotently;
10. Wirebot/Foreman identity routing preserves exact scope;
11. Radar optimizes attention rather than forwarding every event;
12. meeting history preserves speaker/ASR correction lineage without making transcript canonical cognition;
13. spoken/mobile browser action follows normal UIAI observation/control/verification contracts;
14. stock Omarchy developer profile is not misrepresented as hardened Secure Attention or hardware-attested trust;
15. full `voice_complete` claim requires a no-keyboard/no-pointer dogfood proof.

---

## 27. Final principle

> **Omarchy gives Veragensia a native Linux body. Focusa gives it governed cognition. UIAI gives it hands and eyes. Ambient Operator lets that same living system accompany the human beyond the desk without splitting into another brain.**
