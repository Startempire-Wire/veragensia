# 200 — Veragensia Living Agent Computer Implementation Tranche Plan

**Status:** implementation sequencing contract, 2026-09-05; this document defines dependency order and acceptance gates, not mutable task status.  
**Canonical human architecture authority:** Verious Smith III under Doc 185.  
**System specs:** Focusa 181–184; Veragensia 190–199; UIAI Agent-First Browser/control contracts; Wirebot Ambient convergence; portable Ambient Operator profile.  
**Task rule:** materialize each accepted tranche/slice into the owning repository's `br`/Beads graph. Do not track mutable progress in this document.

---

## 0. Outcome

Build one coherent **living Agent Computer** that can:

```text
stay grounded in one or many exact Workstreams
→ maintain persistent Project Foremen across model/session changes
→ notice meaningful developments through Radar
→ converse naturally by voice with keyboard/mouse optional
→ accompany the owner through a paired phone/earbuds
→ preserve attributable meetings/conversations
→ use owner-life context without making it project-global memory
→ execute real computer/browser work through UIAI/Agent Apps
→ enforce semantic authority at the Linux/runtime boundary
→ prove outcomes with Evidence/Receipts
```

The first integrated release is not required to implement custom wearable hardware or perfect iOS parity.

---

## 1. Critical-path principles

### 1.1 One vertical slice before broad surface area

Do not implement every Radar source, every mobile sensor, every application, or every voice provider first.

The first end-to-end slice should prove:

```text
one Workstream
→ one Foreman
→ one voice conversation
→ one Radar Signal
→ one worker/UIAI action
→ one Evidence/Receipt
→ one paired Android Companion
→ one searchable audit trail
```

### 1.2 Primitive owner first

Implement semantic types/operations in the primitive-owning repo before client projections:

```text
Focusa semantic contract
→ Veragensia/UIAI/Wirebot adapter
→ Omarchy/mobile UI
```

No client should invent its own Foreman/Radar/Conversation state just because the core operation is not ready yet.

### 1.3 Read-only before mutation

Every new cross-system surface lands in this order where practical:

```text
identity/health
→ read projection
→ proposal
→ governed mutation
→ autonomous bounded action
```

### 1.4 Structured before visual

Use existing typed Focusa/UIAI events first. Do not begin Radar by screenshotting desktops or begin voice by simulating clicks.

### 1.5 Local/private proving ground first

Ambient voice, phone context and meetings are private-operator features. Do not use `os.focusa.dev` as their proving ground.

---

## 2. Tranche 0 — Contract/codegen closure

**Goal:** make the new primitives callable before building UI.

### Focusa

Materialize Specs 181–184 core object/operation slices:

- Spec 181 core Conversation objects/events/operations required by one voice session;
- `ForemanBinding`, `ForemanRuntimeAttachment`, hydration packet;
- `RadarObservation`, `RadarEpisode`, `RadarSignal`;
- `AmbientSession`, `AmbientPresenceProjection`, `AmbientSyncEnvelope`;
- Operation Registry / generated machine contracts;
- API/CLI/Pi reference projection where required by the standard Focusa tool contract.

Suggested code ownership:

```text
crates/focusa-core/src/
crates/focusa-api/src/routes/
crates/focusa-cli/src/commands/
apps/pi-extension/
docs/contracts/
```

Exact module filenames are selected by the implementation agent to match current crate organization; do not create a parallel crate merely for product naming.

### Acceptance T0

- one daemon can hold two Workstream roots with distinct Foreman refs;
- Foreman hydration reconstructs after daemon/model-session restart;
- one synthetic ConversationSession preserves utterance/correction/principal refs;
- one synthetic Radar observation deduplicates into one Episode/Signal;
- one Ambient envelope survives serialize/validate/replay-idempotency tests;
- generated operation schemas and API/CLI/Pi descriptors agree;
- zero new daemon-global `current_foreman`/`current_radar` singleton.

---

## 3. Tranche 1 — Native Omarchy read-only vertical slice

**Goal:** put real current Focusa state into stock Omarchy without adding trust-bearing QML logic.

### Veragensia

Implement:

```text
overlay/omarchy/plugins/veragensia.ambient/
    manifest.json
    Status.qml
    AmbientPanel.qml

veragens-sessiond prototype / typed local IPC
```

Panel initially shows only:

- selected Workstream/Foreman;
- current Workpoint summary;
- Radar state/count;
- voice/listening state = unavailable or inactive;
- Companion = unpaired;
- UIAI health;
- trust/profile state;
- stale/degraded markers.

### Omarchy integration proof

- plugin validates using current Omarchy manifest contract;
- install lives in the supported user plugin path;
- no edits under package-owned Omarchy source;
- plugin reload/rescan works;
- session bridge recovers from Focusa restart;
- QML contains no token/credential/direct reducer-write path.

### Acceptance T1

The owner can boot qualified Omarchy and see the exact Focusa Workstream/Foreman/Workpoint state natively while all canonical state still lives in Focusa.

---

## 4. Tranche 2 — Trusted local audio loop

**Goal:** speak naturally to one Foreman on the Agent Computer and hear an attributable response.

### Veragensia

Implement `veragens-audiod` prototype with:

- microphone/output endpoint inventory;
- Bluetooth/headset route events;
- trusted capture/playback session;
- hardware/software mute posture where exposed;
- endpoint/resource identity;
- capture bound to WorkloadIdentity/EnforcementPlan;
- safe route-change behavior.

### Focusa

Wire one ConversationSession flow:

```text
AudioSegment
→ SpeechHypothesis
→ accepted/corrected Utterance
→ Foreman current ask
→ ExpressionOutput
→ SpokenOutput
```

### Provider strategy

Use one practical ASR/TTS or realtime provider adapter for the slice. Provider choice is not architecture. A local dictation tool may bootstrap testing but cannot replace Spec-181 conversation semantics.

### Acceptance T2

- owner can address one exact Foreman by voice;
- human barge-in stops stale spoken output;
- audio route change is visible/recoverable;
- unrelated Pi/worker/browser process cannot open the trusted microphone under the test enforcement profile;
- transcript/agent speaker/principal/action lineage persists;
- no keyboard is used for the representative conversation after session start.

---

## 5. Tranche 3 — Project Foreman operational closure

**Goal:** make Foreman the persistent project-responsible intelligence rather than a name over one chat.

### Focusa

Implement remaining Spec-182 slices:

- bounded hydration from C.R.I.S.T./Runtime Constitution/Trajectory/Workpoint/Evidence/current sessions;
- worker list/delegate/steer/pause/stop adapters over Spec 133/79;
- model/provider/runtime attachment switch;
- restart recovery;
- Evidence-backed `status`/`explain`.

### Acceptance T3

Prove:

```text
Foreman on Pi/Claude
→ switch runtime/model
→ same foreman_ref/workstream_ref
→ same current Workpoint
→ no transcript replay required
```

Then terminate a worker and prove the Foreman can rehydrate/reassign from Focusa state.

---

## 6. Tranche 4 — Radar minimum useful loop

**Goal:** demonstrate proactive attention without notification spam or surveillance.

### First Radar sources only

Start with structured Focusa/UIAI signals:

- Workpoint blocked/stalled;
- repeated worker failure;
- test/build failure;
- UIAI browser diagnostic/verification failure;
- waiting approval/settlement uncertainty.

Do **not** start with ambient microphone or generic screenshots.

### Radar engine

Implement:

- fingerprint/dedupe;
- Episode grouping;
- bounded attention-value inputs;
- Radar Signal;
- Foreman inbox;
- investigate/prepare/escalate loop.

### Acceptance T4

A repeated identical failure creates one developing Episode, not N alerts. The Foreman investigates it, gathers Evidence, and produces one useful prepared response or escalation. Radar itself never mints a grant/Workpoint.

---

## 7. Tranche 5 — Companion sync and Android context edge

**Goal:** connect the existing real phone-context proving ground to the same Focusa/Veragensia system.

### Wirebot Core

Implement:

- Context Core → `AmbientPresenceProjection` adapter;
- coarse place/activity/interruptibility first;
- precise-location task handle path;
- exact source/freshness/privacy metadata.

Keep the existing Termux Phone Bridge context-only.

### Veragensia

Implement `veragens-syncd`:

- paired device identity;
- encrypted sync;
- sequence/replay defense;
- idempotency;
- offline queue ack/reconcile;
- LAN/Tailscale transport path;
- revocation.

### Android Companion alpha

First UI can be intentionally narrow:

```text
Talk
Attention
Meeting
History
Privacy / listening state
Sync/device health
```

### Acceptance T5

- phone publishes coarse bounded context;
- Focusa sees it only through the Ambient projection;
- exact GPS is absent from Workstream state by default;
- offline queue survives app/network restart;
- replay/duplicate envelope cannot duplicate canonical mutation;
- revoked phone cannot sync;
- Radar/Foreman may use interruptibility without gaining raw location authority.

---

## 8. Tranche 6 — Android voice/wake/meeting flight recorder

**Goal:** move from Termux/context prototype to native mobile Ambient Operator.

Implement through supported Android lifecycle:

- PTT;
- active live conversation;
- local wake/VAD path where practical;
- meeting capture;
- foreground/background restriction states;
- Bluetooth route changes;
- encrypted local audio/transcript queue;
- visible recording/listening state;
- diarization/speaker-confidence adapter;
- transcript correction UI;
- raw audio vs transcript retention policy.

### Acceptance T6

- wake mode does not durably retain pre-trigger room audio by default;
- platform suspension/restriction appears truthfully;
- meeting records at least two synthetic speakers and preserves diarization uncertainty/corrections;
- a spoken commitment becomes a candidate only, not a Workpoint/deadline automatically;
- the owner can search/replay the attributable conversation after sync/restart.

---

## 9. Tranche 7 — Wirebot Chief-of-Staff + Radar attention

**Goal:** realize the correct intelligence hierarchy.

### Wirebot Core

Implement:

- Wirebot vs Foreman voice/mobile identity router;
- exact Foreman delegation envelope;
- Radar portfolio projection inbox;
- Context Core interruptibility timing;
- legacy `wbt` → Focusa Spec-181 adapter/migration.

### Acceptance T7

Prove:

```text
Radar A needs owner decision
Radar B has informational success
owner is driving
→ Wirebot holds both
owner becomes interruptible
→ surfaces only A
→ owner says yes
→ exact Foreman A receives governed operation
```

No raw Radar event or meeting transcript is injected into global Wirebot memory merely for convenience.

---

## 10. Tranche 8 — UIAI mobile/voice computer action

**Goal:** make Ambient Operator actually operate the computer, not just discuss it.

One representative scenario:

```text
owner via earbuds/mobile:
"Foreman, open the staging site, verify the broken signup flow, and fix what you can safely fix."

→ Focusa Foreman/current ask
→ authority/capability check
→ UIAI structured/semantic browser observation
→ UIAI action
→ verification/diagnostics
→ Focusa Evidence/Receipt
→ spoken verified result
```

Add one human takeover:

```text
"Give me control."
→ UIAI/Veragensia fenced takeover
→ operator change
→ OperatorDelta
→ fresh observation
→ return control
```

### Acceptance T8

No mobile/voice-specific UIAI bypass exists; ordinary UIAI entitlement/observation/control/verification all still pass.

---

## 11. Tranche 9 — Enforcement and trust closure

**Goal:** prove the architecture is not merely polite software.

Implement/close Doc-193/196 controls needed by the integrated path:

- workload identities for session/audio/sync/UIAI workers;
- per-workload filesystem/network/device/mic access;
- Human Control Reserve;
- service/package/image digest binding;
- runtime incarnation/ref invalidation;
- T1 developer trust explicitly reported on normal current Omarchy baseline;
- compatibility bundle covering Focusa/UIAI/Veragensia/Companion versions.

### Acceptance T9

Adversarial tests prove:

- random same-UID worker cannot read microphone/audio queue/paired-device key;
- stale Companion/control/session ref fails after runtime incarnation change;
- QML plugin cannot directly mutate Focusa state;
- control/stop remains responsive under agent resource pressure;
- no T2+ trust claim exists without separate boot/attestation proof.

---

## 12. Tranche 10 — Voice-complete living Agent Computer dogfood

**Goal:** prove the user experience, not just APIs.

With keyboard and pointer unavailable for the representative path:

1. owner wakes/addresses Wirebot or one Foreman;
2. asks what needs attention;
3. Radar/Foreman explains one real issue;
4. owner delegates additional worker/team if authorized;
5. worker/UIAI acts;
6. owner interrupts/asks questions/takes control if needed;
7. owner reviews Evidence by voice;
8. owner gives bounded approval where required;
9. result settles and is spoken back;
10. owner later searches conversation/meeting history and can identify every human/agent speaker and linked action.

### Acceptance T10

This is the first point at which the integrated profile may claim **living, voice-complete Ambient Agent Computer** behavior for the tested workflow.

---

## 13. Tranche 11 — iOS, broader apps, and hardware expansion

After the Android/private reference path closes:

- iOS Companion parity through supported APIs;
- broader application Agentability catalog;
- more Radar sources/domain packs;
- car audio/smart glasses/other wearables;
- optional purpose-built Focusa earbuds/hardware;
- stronger T2/T3/T4 platform trust variants;
- Cloud Agent Computer audio/Companion handoff;
- commercial/vertical profiles.

Do not place these on the critical path for the first integrated proof.

---

## 14. Dependency graph

```text
T0 contracts
  ↓
T1 Omarchy read projection
  ↓
T2 local audio
  ↓
T3 Foreman operational closure
  ↓
T4 Radar useful loop
  ↓
T5 Companion context/sync
  ↓
T6 Android voice/meeting
  ↓
T7 Wirebot Chief-of-Staff routing
  ↓
T8 UIAI ambient execution
  ↓
T9 enforcement/trust closure
  ↓
T10 voice-complete dogfood
  ↓
T11 expansion
```

Some implementation may proceed in parallel after T0, especially T3/T4 and Android shell work, but no tranche may claim integrated closure without its predecessors' required contracts/evidence.

---

## 15. Repository allocation

| Repository | Immediate implementation train |
|---|---|
| `Startempire-Wire/focusa` | T0, T3, T4 plus Conversation/meeting semantics |
| `Startempire-Wire/veragensia` | T1, T2, T5 sync broker, T8 composition, T9, T10 |
| `Startempire-Wire/wirebot-core` | T5 context adapter, T7, legacy `wbt` convergence |
| `WPUIAI/uiai-engine` | T4 observation bridge, T8 actuator/FPV/takeover proof |
| `Startempire-Wire/agent-driven-life-business-os` | portable conformance/adoption updates only; no duplicate runtime |

---

## 16. First Beads materialization

When implementation begins, create **one parent initiative per owning repository**, then child tasks matching the accepted tranche slices rather than one giant cross-repo task.

Recommended parent intent names:

```text
Focusa: Foreman + Radar + Ambient core primitives
Veragensia: Ambient Agent Computer native integration
Wirebot Core: Ambient Chief-of-Staff convergence
UIAI Engine: Ambient/Foreman/Radar execution bridge
```

Dependencies across repositories should use durable external refs/commit/spec identifiers while canonical local task state remains in each repo's `br` graph.

Do not manually edit Beads storage or use GitHub issues as a replacement for `br`.

---

## 17. What is implemented versus specified today

At publication of this plan:

### Existing/prototyped building blocks include

- Focusa Workstreams, Workpoints, Evidence, Work Loop/Silent Session architecture and broad generated capability surface;
- Pi reference integration;
- UIAI Engine browser/computer stack and existing control/Agent-First contracts in their stated implementation status;
- Wirebot Context Core/Phone Bridge context path;
- Wirebot `wbt` voice runtime;
- Veragensia public streamed webtop proving ground.

### Newly specified/converged but not yet claimed implemented

- Focusa Project Foreman Spec 182;
- Focusa Radar Spec 183;
- Focusa Ambient Operator Spec 184;
- Veragensia trusted Ambient Omarchy/audio/sync integration Doc 199;
- native Android Companion under these contracts;
- end-to-end workload-enforced voice-complete Ambient Agent Computer.

Commit existence is not runtime proof.

---

## 18. Final principle

> **Implement the organism from its spine outward: exact Workstream intelligence, bounded observation, governed conversation, machine enforcement, then the phone/earbuds that make it feel alive everywhere.**
