# 197 — Veragensia Voice-Native Agent Computer, Audio UI, and Conversation Continuity

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Core decision:** Keyboard and mouse are optional peripherals, not architectural dependencies.
**Primitive owner relationship:** Focusa Doc 181 owns Voice/Conversation/Expression semantics and Conversation Ledger; Veragensia owns OS audio devices, modality delivery, trusted control, surface integration and end-to-end voice-complete Agent Computer experience.
**Dependencies:** Docs 193–196; Focusa Doc 08 Expression Engine, Doc 181 Voice/Conversation primitive, Spec 151 modality parity; UIAI Engine/Cockpit computer-control surfaces.

## 1. Decision

A Veragensia Agent Computer MUST be designed so a person can accomplish ordinary supported work **without needing a keyboard or mouse**.

Voice is not an accessibility afterthought, dictation box, hotkey, or chatbot overlay. It is a foundational input/output modality of the operating environment.

The target feeling is:

> Speak naturally to the computer and its agents, accomplish real work across the entire computer, hear useful responses, interrupt freely, collaborate with multiple specialists, and later inspect exactly what everyone said and what actions followed.

Keyboard, mouse, touch and visual UI remain excellent optional modalities. None may be the only route to a supported ordinary action in a declared voice-complete full profile.

## 2. Constitutional interaction law

```text
VOICE
TOUCH
KEYBOARD
POINTER
STRUCTURED AGENT API
REMOTE CONTROL

        ↓

same canonical Focusa operations
same authority
same Evidence / Receipts
same ResourceRefs
same Control Leases
same settlement
```

No modality gets a hidden parallel implementation of business/work authority.

## 3. No-keyboard/no-mouse invariant

For a **voice-complete Agent Computer profile**:

1. first useful operation after login/unlock can be performed by voice;
2. application/work navigation is voice-operable;
3. documents/files/browser/code can be manipulated by voice through agents and canonical operations;
4. agents/teams can be created, assigned, steered, paused and stopped by voice;
5. approvals/clarifications can be completed without keyboard/mouse;
6. system health and work status are available audibly;
7. takeover/return-control and emergency stop are voice-operable;
8. conversation/audit history is voice-searchable and voice-readable;
9. recovery/resume after restart is voice-operable;
10. ordinary setup/configuration is voice-operable where the underlying platform permits;
11. an operation that requires a keyboard/mouse must be reported as a voice-parity defect or explicit unsupported platform limitation.

The test is not whether speech can click buttons. The test is whether the person can achieve the outcome naturally without thinking like a mouse user.

## 4. Voice is primarily semantic, not simulated input

Preferred route:

```text
spoken intent
→ Focusa current ask / operation discovery
→ structured capability
→ semantic application automation
→ UIAI/desktop computer-use fallback
```

Do not turn every voice command into synthesized mouse coordinates when a typed operation exists.

Example:

```text
"Open the Q3 forecast and fix the totals."
```

should resolve semantic resources/app capabilities and let an agent operate the spreadsheet, not require the user to say:

```text
"click cell D14, type equals sum..."
```

The human speaks in goals, objects, relationships and corrections. The Agent Computer translates those into exact operations.

## 5. Natural conversation contract

The person should be able to speak conversationally:

```text
"Where were we?"
"Keep going."
"No, I meant the other customer."
"Stop."
"Ask the security agent what it thinks."
"Both of you discuss the tradeoff and give me your recommendation."
"Open what the accounting agent was referring to."
"Take care of it and tell me when it's actually verified."
```

Context resolution uses Focusa ProjectIdentity, Workpoint, Conversation Ledger, current surface and explicit reference resolution. Context does not grant new authority.

## 6. Audio UI architecture

```text
Microphones / remote audio endpoints
        ↓
Trusted Audio Capture Service
        ↓
ASR / speech model adapter
        ↓
Focusa Doc 181 Conversation + Utterance
        ↓
Focusa operation / agent reasoning
        ↓
Expression Engine output
        ↓
Speech Renderer / TTS
        ↓
Trusted Audio Playback Service
        ↓
Speakers / headphones / remote audio endpoints
```

Capture/render services have WorkloadIdentity and RuntimeAttestation under Docs 193/196.

Ordinary Agent Apps do not inherit microphone access simply because the trusted voice service has it.

## 7. Full-duplex by default

The long-term experience is **full-duplex conversational audio**, not push-to-talk as the only architecture.

The system supports:

- voice activity detection;
- natural end-of-turn detection;
- human barge-in;
- agent speech cancellation/ducking;
- overlapping human/agent speech;
- overlapping multi-human speech where hardware permits;
- interrupting an agent without necessarily cancelling its underlying operation;
- immediate steering from the newest operator utterance;
- configurable wake/attention policy;
- push-to-talk as an optional privacy/control mode.

## 8. Listening states and privacy

Voice capability does not mean ambient recording without policy.

Declared modes include:

```text
muted
push_to_talk
wake_word_local
active_conversation
continuous_local_session
remote_audio_session
```

The current state must be unmistakable through available modalities, including an audible status query.

Where wake-word detection is enabled, local/on-device detection is preferred when practical so ambient audio need not leave the node merely to decide whether the user addressed the computer.

## 9. Audio device model

```yaml
schema: veragensia.audio_endpoint.v1
audio_endpoint_ref:
kind: microphone | speaker | headset | array | remote_mobile | virtual
node_ref:
hardware_or_service_ref:
trust_class:
capabilities:
  capture:
  playback:
  echo_cancellation:
  spatial_audio:
  beamforming:
  hardware_mute_state:
runtime_incarnation_ref:
privacy_zone_ref:
```

Hot-plug/device replacement advances applicable runtime identity and cannot silently redirect private conversation to a different output device.

## 10. Trusted speech surface

The Agent Computer must distinguish:

```text
trusted Veragensia/Focusa speech
ordinary application audio
agent-generated media audio
remote participant audio
```

Applications can imitate words/voices, so audio resemblance is not secure identity.

For security-sensitive spoken approval, Doc 194 Secure Attention Plane owns the interaction. It may:

- reserve/duck competing audio;
- state exact actor/target/consequence;
- use a trusted hardware/visual/haptic indicator where available;
- require authenticated device/presence factor for high-consequence decisions;
- capture the spoken decision as Focusa Doc 181 provenance.

No keyboard/mouse is required, but voice biometrics alone are not a universal security factor.

## 11. Agent voices and identity

Every agent/expert may have a distinct voice presentation for usability.

```yaml
schema: veragensia.agent_voice_presentation.v1
agent_principal_ref:
display_name:
role_ref:
voice_profile_ref:
tts_provider_ref:
language_refs: []
style_profile_ref:
```

Rules:

- audible voice is presentation, not identity authority;
- stable agent principal is always recorded independently;
- changing TTS provider/voice does not change the agent;
- two agents may never become indistinguishable in the Conversation Ledger simply because voices sound alike;
- user may ask "who is speaking?" at any time;
- group mode SHOULD make speaker changes obvious without requiring visual attention.

## 12. Multi-agent spoken rooms

The user may converse with one agent or a group of specialists.

```text
User
  ↕
Conversation Room
  ├── Chief of Staff
  ├── Security expert
  ├── Accounting expert
  └── Builder
```

Each participant has:

- principal ref;
- role/expertise ref;
- conversation participant ref;
- voice presentation ref;
- authority scope;
- utterance/action lineage.

Agents may discuss with each other when authorized. The system preserves who said what rather than collapsing the discussion into one assistant blob.

## 13. Turn floor and interruption

Focusa Doc 181 owns conversational floor semantics. Veragensia supplies audio rendering/capture.

The experience supports:

```text
"Security, go first."
"Accounting, respond to that."
"Stop both of you."
"Builder, continue."
"Everybody hold on—I'm changing the requirement."
```

The newest explicit human steering takes precedence over agent conversational momentum.

## 14. Conversation Ledger integration

Every voice interaction is represented through Focusa Doc 181.

The user can later inspect:

- their own utterances;
- each agent utterance;
- external human participant utterances;
- ASR confidence/corrections;
- timestamps;
- interruptions/overlap;
- addressed-to/reply-to relationships;
- which statement initiated an operation;
- operations/actions/tools performed;
- Evidence/Receipt/outcome relationships;
- what was spoken back and whether playback was interrupted.

The transcript is extensive and searchable but remains distinct from canonical Focusa memory/state.

## 15. Transcript and audit UX

Focusa Desktop and voice UI must support queries such as:

```text
"Go back to what I said about the interface yesterday."
"Show every time we discussed this customer."
"What exactly did the security agent say before I approved that?"
"Which agent disagreed?"
"Read the five minutes around the deployment decision."
"What did you hear me say?"
"Correct that transcript: I said 50, not 15."
```

Visual transcript surfaces may provide:

- speaker-separated timeline;
- expandable action/evidence branches;
- audio replay when retained;
- ASR correction history;
- semantic search;
- filters by participant/project/Workpoint/time/action;
- jump from utterance → action → Evidence → Receipt.

But all important audit navigation also has a voice path.

## 16. Editing by voice

Voice-complete editing is semantic and agent-assisted.

Examples:

```text
"In the second paragraph, change 'required' to 'recommended'."
"Move the section about billing after security."
"Undo the last change you made to this file."
"Compare this version to what we agreed on Tuesday."
"Read the changed paragraph back to me."
```

The runtime resolves exact ResourceRefs/revisions through Doc 195 and uses structured app capabilities before visual fallback.

## 17. Browser/computer use by voice

UIAI Engine/Cockpit remains the execution surface.

Examples:

```text
"Open GitHub and check whether CI passed."
"Fill out this form from the customer record but don't submit it yet."
"I see the wrong account selected—give me control."
"Submit now."
```

Voice does not alter UIAI observation-bound actions, influence firewall, control leases or settlement requirements.

## 18. Window/workspace control by voice

The shell/compositor integration exposes semantic window/workspace operations:

```text
"Bring Focusa Desktop here."
"Put the browser on the other screen."
"Go back to the spreadsheet."
"Close the app we just opened."
"Show me what the security agent is working on."
```

Window focus itself never establishes task authority.

## 19. Agent/team orchestration by voice

Elastic Agent Computing is voice-native:

```text
"Give this project another team."
"Have three agents investigate independently."
"Pause the expensive workers."
"Move that work to the cloud computer."
"Tell me what all teams are blocked on."
```

TopologyGrant, spend/resource policy and Focusa fanout/writer rules still govern the result.

## 20. Voice-first recovery

After restart, disconnect or failure:

```text
User: "Where were we?"
System: speaks bounded Workpoint/Conversation recovery summary
User: "Continue, but don't rerun the payment."
```

Recovery binds Focusa Workpoint, Spec 136 unknown-effect reconciliation, Doc 195 resource/runtime incarnation and Conversation Ledger history.

The system never replays a consequential command just to reconstruct conversation state.

## 21. Voice onboarding and setup

A voice-complete profile should support spoken setup of:

- language/locale;
- audio devices;
- agent voice preferences;
- privacy/listening mode;
- conversation retention preference within policy;
- user-facing accessibility preferences;
- default response verbosity;
- wake/attention policy;
- companion device enrollment guidance.

Credentials and identity enrollment use trusted providers/factors; the design must not force keyboard/mouse merely because conventional login forms assume them.

## 22. No weird command language

The user must not have to memorize a rigid voice command grammar for normal work.

Canonical operations expose semantic descriptions and argument models to the agent/voice interpreter.

The system may offer concise deterministic phrases for emergency/control operations, but ordinary voice interaction is natural language grounded to exact capabilities.

## 23. Response design

Agents SHOULD adapt spoken responses separately from visual/text detail.

Audio response modes may include:

```text
minimal_ack
concise
normal_conversation
detailed_readback
verbatim_audit_readback
```

A long structured result can be summarized aloud while remaining fully inspectable in Focusa Desktop/Conversation Ledger.

When the user says "read it exactly," the system uses the exact relevant text/artifact rather than a generated paraphrase.

## 24. Latency targets

Voice interaction must feel immediate enough to sustain conversation.

Architecture therefore separates:

```text
fast local capture/VAD/barge-in path
fast acknowledgment/control path
model reasoning path
long-running execution path
```

Stop/takeover/mute do not wait for an LLM.

The system can acknowledge a request audibly while the actual task continues asynchronously.

## 25. Offline/degraded voice

Essential voice controls SHOULD remain available without cloud speech/model service where practical:

- stop/pause/mute;
- secure-attention response;
- status/health basics;
- local navigation/control commands;
- dictation fallback where an installed local model supports it.

Loss of advanced ASR/TTS/model capability is stated audibly and in structured state.

## 26. Language and accessibility

Voice architecture is multilingual/provider-neutral.

Participant records carry language/locale. ASR/TTS adapters may switch per conversation or speaker without changing Focusa identity.

Support should account for:

- accents/dialects;
- speech differences;
- configurable speaking rate;
- captions/transcripts;
- screen-reader coexistence;
- hearing-impaired modes combining visual/haptic output;
- low-bandwidth remote audio.

Voice-first does not mean voice-only for people who need or prefer other modalities.

## 27. Telemetry boundary

Voice quality can be measured with privacy-safe metrics such as:

- endpointer latency;
- ASR correction rate;
- barge-in latency;
- TTS start latency;
- speaker-attribution uncertainty rate;
- task success through voice;
- keyboard/mouse fallback rate in voice-complete tests.

Do not upload transcript/audio content merely to calculate these metrics.

Doc 192 anti-exfiltration/cardinality rules apply.

## 28. Voice-complete acceptance suite

A full voice-complete profile must prove representative workflows entirely without keyboard/mouse:

1. resume current project and Workpoint;
2. open/navigate applications;
3. search/retrieve a file or record;
4. edit a document;
5. perform governed browser work;
6. delegate work to an agent/team;
7. interrupt an agent mid-speech;
8. pause/stop active computer control;
9. complete a trusted low/medium-risk approval verbally;
10. recover from a deliberate ambiguous ASR target without unsafe action;
11. conduct a conversation with at least two independently attributable agent speakers;
12. search the Conversation Ledger by topic/speaker/time;
13. trace a spoken instruction to the resulting action and Receipt;
14. correct a transcript and preserve revision history;
15. restart the Agent Computer and resume voice interaction/continuity;
16. complete the full workflow with keyboard and pointer physically absent or disabled.

## 29. Canonical full-profile composition update

A full Agent Computer profile now deliberately includes:

```text
Focusa daemon/core
Focusa Desktop
Pi + Focusa Pi extension
UIAI Engine + Cockpit/browser/computer surfaces
Veragensia enforcement/control substrate
Voice/Conversation service bound to Focusa Doc 181
Veragensia native shell/session integration
```

A full profile that omits voice may be a constrained/special-purpose profile but MUST NOT claim full voice-complete parity.

## 30. Final principle

> The future Agent Computer is not a computer that happens to accept speech. It is a computer whose entire operating model can be driven through conversation, while preserving exact authority, attribution, provenance, evidence and human control.
