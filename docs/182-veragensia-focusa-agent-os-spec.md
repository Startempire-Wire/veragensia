# 182 — Veragensia · Focusa Agent OS and Agent Cloud Computer

**Status:** DRAFT canonical product direction; native v0.1 implementation proposal added 2026-09-04.
**Canonical human architecture authority:** Verious Smith III, under Doc 185.
**Original naming/product draft:** 2026-08-26. The prior draft is preserved in Git at `948e9080efa1f52662b159193523e9c12a3d05a3`; this revision explicitly updates the native integration and release framing rather than claiming the old GUI plan was implemented.
**Live proving ground:** `https://os.focusa.dev`, governed separately by Doc 183.
**Companions:** 182b (base/overlay), 182c (fleet bridge), 183 (public lifecycle), 185 (authority), 186 (native v0.1), 187 (Chromebook bring-up), 188 (integration contracts), 190 (agent-first software), 191 (Elastic Agent Computing), 192 (telemetry/improvement), 193 (execution enforcement), 194 (trusted control/desktop observation), 195 (resource/runtime identity), 196 (platform/runtime trust), 197 (voice-native Agent Computer), Focusa Spec 181 (Voice/Conversation).

## 1. Product and naming

**Veragensia** is the Focusa Agent OS: a human-owned operating environment with governed agents as native participants. **Veragens** is the short form and CLI/package naming direction. A provisioned, streamable instance is an **Agent Cloud Computer**.

The product lifts existing Focusa primitives from extension/daemon interaction into desktop services and native surfaces. It does not replace Linux, create a deep Omarchy fork, or make the browser extension the only interface.

> Surfaces are interchangeable; primitives are the platform.

The useful experience is continuous work across applications: explicit project context, recoverable progress, bounded assistance, understandable changes, dependable stop/recovery controls, natural conversation, and the ability to expand into cloud compute or additional agent workforce without making the user manually design infrastructure.

Two additional constitutional product laws now apply:

> **Focusa decides what a governed actor may do. Veragensia is the enforcement substrate that makes the machine behave as though that semantic authority is real.**

> **Keyboard and mouse are optional peripherals. A full voice-complete Agent Computer can accomplish ordinary supported work through natural spoken interaction and spoken agent response.**

Agent-first must not make normal desktop interaction depend on a model call. Essential stop, mute, takeover, secure attention and local control paths must remain deterministic/low-latency.

## 2. Authority and ownership

Verious Smith III remains the architecture root. Focusa owns its scoped operational state and conversation semantics, not the product's constitutional authority. Veragensia owns the assigned OS integration/enforcement substrate; UIAI owns its browser/computer execution runtime. Customer identities, issue authors, agents, repository presence, model outputs, or external platforms do not mint architecture authority. Doc 185 controls conflicts and future Wirebot delegation.

Do not introduce competing Veragensia memory, task, grant, conversation-truth, or canonical state stores where an existing Focusa primitive already owns the concern. A presentation cache, transcript view, app descriptor, runtime attestation or control lease is not canonical cognition.

## 3. Platform composition

| Layer | Responsibility |
|---|---|
| Stock Omarchy / Arch / Hyprland | Hardware, session, compositor, system lifecycle, supported desktop integration points |
| Veragensia enforcement/control substrate | ExecutionPrincipal, WorkloadIdentity, EnforcementPlan, ResourceRef/runtime-incarnation binding, secure attention, DesktopObservation, control leases, Human Control Reserve |
| Veragensia shell/session/audio integration | Work context, lifecycle, application composition, voice/audio devices, interruption, review, containment and recovery |
| Focusa Desktop | Default governed human work/cognition/conversation presentation on supported full profiles; presenter only, not a second cognitive authority |
| Pi + Focusa Pi extension | Default/reference Focusa-aware agent harness integration; typed tools, skills/runbooks, scope/authority hooks and recovery |
| Existing Focusa daemon/core | Project/continuity, Workpoints, Worksets, authorization, sessions, Evidence, operational reduction/persistence, learning, recovery, Expression Engine and Conversation Ledger semantics |
| UIAI Engine + Cockpit/Workforce surfaces | First-party governed browser/computer perception, action, diagnostics, oversight, control-lease support and proof |
| Execution adapters | Enforced local/cloud workcells, Agent Apps and other runtimes under Focusa permission/resource semantics and Veragensia machine enforcement |

The current public demo remains a separate Ubuntu/KDE webtop implementation. Its existence does not demonstrate native Omarchy compatibility or full voice/enforcement parity.

### 3.1 Canonical full Agent Computer defaults

A supported **full Agent Computer profile** deliberately includes, unless the profile/trust class/resource boundary explicitly omits one:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser/computer surfaces;
- Veragensia enforcement/control substrate;
- Voice/Conversation service bound to Focusa Spec 181;
- Veragensia native shell/session integration.

UIAI Engine is foundational and is deliberately listed so it cannot later be misread as one optional browser candidate among many. Voice is equally deliberate: a full `voice_complete` profile does not require keyboard/pointer mechanics for ordinary supported outcomes.

Constrained v0.1, public-demo, headless and special-purpose profiles MAY omit some surfaces. The omission must be explicit and must not redefine the canonical full-profile composition.

### 3.2 Native shell revision

The earlier Waybar modules plus separate QML-shell plan is **not the selected v0.1 proposal** for plugin-generation Omarchy. The native proposal uses Omarchy's supported shell-plugin/configuration interfaces with a thin session adapter. Omarchy's current manual documents this integration model; exact installed versions and runtime compatibility remain test gates.

Do not rely on historical repository language percentages, assume all Omarchy versions expose the same API, or claim upstream updates merge “for free.” Keep upstream source untouched and test supported versions explicitly.

## 4. Focusa primitive-to-OS mapping

| Focusa concern | OS projection/integration |
|---|---|
| ProjectIdentity + `project_root + continuity_id` | Explicit selected-project binding; no inferred authority from cwd/window focus |
| Workpoint and Trajectory | Continue work with existing evidence/blockers/next action; preserve advisory/canonical distinctions |
| Worksets / Workstreams | Work organization related to, but not identical with, compositor workspaces |
| Sessions / work loop | Bounded governed work with real lifecycle, resource accounting, cancellation and recovery |
| Authorization / approvals | Consequence-specific trusted native/audio prompts using existing authority; no grant stored in QML/audio service |
| Credentials / pairing | Private enrolled surfaces and scoped credential broker grants; no public-profile, shared-session or LAN-token shortcuts |
| Ontology / evidence / verification | Shared meaning and inspectable support; no equation of graph validity with factual truth |
| Reflexes / secondary cognition | Bounded observation, salience and escalation through existing Focusa mechanisms |
| Reliability / trust evidence | Contextual evidence influencing routing/verification, never overriding permission |
| Expression Engine | Semantic content to express; Veragensia/TTS may render it but cannot amend meaning |
| Voice/Conversation Ledger | Spoken-session participants, utterances, ASR/correction lineage, group discussion and audit refs; conversation is not memory/authority |
| Events / audit | Freshness-aware native status and durable outcome/conversation lineage owned by the appropriate runtime |

Implementation must resolve the actual supported operation descriptors and prove both producer and consumer behavior. A generic `can(...)` diagram is not proof of enforced OS containment.

## 5. Machine enforcement foundation

Semantic governance is insufficient if the process can bypass it through ordinary desktop/Linux ambient authority.

Doc 193 defines the required translation:

```text
Focusa CapabilityGrant / AuthorityDecision
→ Veragensia EnforcementPlan
→ ExecutionPrincipal + WorkloadIdentity
→ kernel/compositor/portal/runtime restrictions
→ execution
```

Machine-enforced capability domains are independently controlled:

- filesystem/resources;
- network/listeners;
- D-Bus/session IPC;
- Wayland/Xwayland/compositor observation and actuation;
- accessibility/AT-SPI;
- screen capture/input injection;
- microphone/speaker/camera;
- USB/Bluetooth/other devices;
- credentials/secret brokers;
- CPU/memory/I/O/process budgets.

Same Unix UID, root access, container ownership or socket reachability is transport/capability evidence—not Focusa permission.

A governed run cannot become `ready` until its required EnforcementPlan is installed and verified. Missing enforcement returns `unsupported_enforcement`; it does not fall back to an unrestricted same-user process.

## 6. Trusted human control and secure attention

Doc 194 defines a protected Secure Attention Plane, DesktopObservation and ComputerControlLease.

Security-sensitive approval/stop/takeover cannot rely on application pixels that an Agent App could imitate. The trusted control surface must identify actor, operation, target, consequence and current authority posture through a Veragensia-controlled channel.

General computer actuation binds:

```text
DesktopObservation
+ exact runtime/surface/object generation
+ ComputerControlLease generation/fencing
+ Focusa authority
```

Coordinates alone are never stable identity. Human takeover advances the control generation; returning control requires OperatorDelta capture, fresh observation and authority/credential refresh.

Voice-complete profiles expose the same trusted approval, pause, stop and takeover capabilities by speech without treating voice similarity/voiceprint alone as authorization.

## 7. Resource identity and runtime incarnation

Doc 195 establishes:

> Paths, PIDs, window titles, browser target IDs and stream coordinates are locators—not durable resource identity.

Consequential work binds stable `ResourceRef` + expected revision/content posture. Restarts/restores/migrations create or re-evaluate `RuntimeIncarnation`; stale process/window/stream/control/credential observations cannot silently bind to the new runtime.

Local/cloud workspace copies are replicas with explicit base/current revisions and writer fencing. Filesystem/process restoration never claims to reverse external effects.

## 8. Platform trust and genesis

Doc 196 defines platform/runtime trust classes, first-boot genesis, node/workload identity and runtime attestation.

Initial trust classes range from useful unmeasured/developer posture to hardware-attested deployments. A reclaimed Chromebook can be useful without pretending to equal a production hardware-attested financial node.

A full trusted profile verifies a compatible set of:

- Veragensia;
- Focusa;
- Focusa Desktop;
- Pi/Focusa extension;
- UIAI Engine/Cockpit;
- policy/operation contract bundles;
- Agent App descriptors/software;
- enforcement compiler.

Signed software does not grant authority. A healthy process does not prove compatible runtime posture.

## 9. Privacy and agent execution

Intelligence can participate widely; perception remains purposeful and scoped.

**Ordinary agent workloads:** no default capture of clipboard, keystrokes, private window contents, microphone, camera, arbitrary home-directory content or unrelated accessibility objects.

**Trusted voice service exception:** a voice-complete profile may grant an attested Veragensia/Focusa Conversation capture service the microphone/audio route required by Focusa Spec 181 / Doc 197. That narrowly scoped trusted audio capability does **not** become ambient microphone permission for Pi agents, Agent Apps, browser workers or arbitrary models.

Listening state is explicit (`muted`, `push_to_talk`, local wake-word, active conversation, etc.). Conversation/audio content follows its own privacy and retention domain and is not generic telemetry.

Observations may be tentative and transient; they do not automatically become memories or actions. ASR text is a hypothesis/evidence observation with confidence/correction lineage, not unquestionable operator text.

The owner retains ordinary control of the computer. Veragensia must distinguish governed runs from unmanaged upstream launchers. Untrusted code needs enforced separation from user files, session sockets and credentials. A prompt, process label, systemd scope, same UID, or shell panel is not sufficient isolation.

A run may prepare a draft or patch within its approved output scope. Replacing originals, publishing, spending, changing system packages, or expanding access are separate authorized operations. Lost connections and failed cancellation must appear as uncertain/pending rather than falsely complete.

## 10. Native and voice-native experience

Native surfaces should provide: selected work context; continuation; bounded agent activity; artifact review; understandable approvals; explicit stop; visible stale/degraded state; and voice-first access to the same outcomes. Avoid a permanent giant AI dashboard or simulated cognition. Useful state changes should be visible/audible without notification floods.

**Focusa Desktop** is the default governed full-desktop work/cognition/conversation presentation surface. Native Veragensia shell surfaces complement it with ambient OS context and controls rather than silently replacing its Focusa-owned presenter contracts.

**Keyboard and mouse are optional peripherals for a voice-complete profile.** A user should be able to:

- resume work;
- navigate/open/close apps/workspaces;
- search/retrieve/edit files and documents;
- conduct browser/computer work;
- create/steer/pause/stop agent teams;
- approve/clarify through trusted speech;
- take/return control;
- inspect Evidence/Receipts;
- recover after failure/restart;
- search/replay Conversation Ledger history;

without translating their goal into button/coordinate mechanics.

The preferred human experience is semantic conversation. Veragensia/agents translate goals into structured capability → semantic automation → computer-use fallback.

A workspace association is an aid to navigation, not proof of intent. Agents should work in separate bounded environments without stealing focus/control from the human. Accessibility, speech differences, pointer/keyboard alternatives, readable scaling, captions, reduced motion, hearing-impaired modes and honest limitations are acceptance concerns, not later visual polish.

## 11. Chromebook and constrained hardware

Reclaimed/constrained hardware is a design target, not an excuse for degraded foreground interaction. Reuse Focusa's existing constrained/LowMem mechanisms. Keep essential local continuity and normal desktop/control behavior independent of a mandatory resident model or cloud service.

The initial recovered planning target is Dell Chromebook 11 CC11260 / expected ULDRENITE. Exact board, firmware procedure, resource capacity and Linux hardware qualification are device gates in Doc 187. ChromeOS Linux-container integration and remote access are distinct modes, not native Omarchy substitutes.

A constrained preview profile does not need to implement every canonical full-profile surface on day one. It must state what is omitted and why, and must not claim parity with a full/voice-complete Agent Computer until the relevant capability/profile gates pass.

Essential local voice controls such as stop/mute/secure attention should not require a remote LLM. Advanced ASR/TTS/model capability may degrade explicitly when constrained/offline.

Idle, locked, and suspended are different states. Absence never broadens permissions. Do not enable unattended work or lingering automatically.

## 12. Agent-first software and applications

A Veragensia Agent Computer should be intentionally stocked with software selected for **agent leverage**, enforceability and human modality parity—not merely human familiarity.

The preferred execution hierarchy is:

```text
1. Structured capability
   typed operation / API / CLI / MCP / ACP / application protocol

2. Semantic application automation
   accessibility / DOM / application object model / stable semantic refs

3. Computer use
   visual desktop / generic input / arbitrary application
```

Level 3 remains mandatory as the universal fallback, but default applications should minimize how often agents need fragile pixel-only interaction.

Voice is an intent modality above that hierarchy: the user says what they want; the Agent Computer selects the best route.

Doc 190 defines Agentability, capability-first profiles, attested Agent App descriptors, enforceability gates, voice/nonvisual operability, and the deferred evidence-based Agent-First Software Catalog.

Pi is fundamental to Focusa's reference agent experience. It is the default/reference harness integration, not a second cognitive/conversation authority. Non-Pi harnesses remain first-class through thin Focusa adapters and generated capability contracts.

## 13. UIAI Engine and browser/computer execution

UIAI Engine is the first-party browser and browser-adjacent execution/proof system for Veragensia. It is deliberately part of the canonical Agent Computer composition.

Chromium plus Focusa Workforce remains a first-class private surface. The native preview must use a private profile and the same enrolled Focusa identity; current public demo browser profiles and credentials must not be copied to the laptop.

Veragensia consumes UIAI's existing Agent-First Browser contracts rather than inventing a parallel browser automation layer: compact capability discovery, versioned observations, observation-bound actions, semantic refs, Focusa-directed verification, provenance/influence controls, execution capsules, Cockpit oversight and visual fallback.

Doc 194 generalizes the same freshness/control philosophy to full-desktop actions. UIAI's existing proposed control-lease generation/fencing and operator-delta/re-observation concepts are reused for Agent Assist rather than duplicated.

Voice requests that need browser/computer action route to normal UIAI capabilities. They never create a separate voice-actuation permission system.

Do not expose raw CDP or daemon ports to make integration convenient.

## 14. Elastic Agent Computing and cloud runtime

The existing private control-plane companion remains spec 115 and its approved addenda:

> Cloud coordinates. Node decides. Receipts prove. Private state stays local.

Doc 191 defines Elastic Agent Computing across full streamed Agent Computers, workcells, Focusa Silent Session teams, Agent Apps, UIAI browser contexts and remote specialist runtimes.

The user requests capability/workforce/profile—naturally by voice or any other modality. Veragensia resolves topology under a bounded `TopologyGrant` so recursive agent/fleet spawning cannot expand without explicit authority/budget/depth constraints.

`os.focusa.dev` is the first crude Cloud Agent Computer Runtime shape. It remains a `public_demo` trust profile governed by Doc 183.

Workcell specializes existing Focusa ExecutionContext/affordance concepts rather than adding a parallel permission/identity model. Infrastructure leases are not automatic application authorization.

Multi-agent execution builds on Focusa exact routing, FanoutPlan/session budgets, writer leases/idempotency, effect receipts and isolated ResourceRef-backed workspaces. Many agents must not become many independent writers.

Migration/restart/resume uses fresh RuntimeIncarnation/workload attestation/EnforcementPlan; stale actuation/credential/writer leases are fenced.

## 15. Agent Assist

A full Agent Computer supports first-class Agent Assist modes (`observe_only`, `guide`, `shared_control`, `delegated_control`), but the underlying architecture is:

```text
Focusa Intervention
+
Veragensia/UIAI ComputerControlLease
+
DesktopObservation
+
OperatorDeltaReceipt
+
mandatory re-observation and authority/credential refresh
```

Human interruption/revocation is protected by the Human Control Reserve. Local freeze is truthfully distinct from canonical Focusa pause. Pending unknown side effects block unsafe resume.

Voice is a first-class control surface for Agent Assist: “stop,” “give me control,” “continue,” “don’t continue,” “take me to the exact window,” and equivalent intents route to these same primitives.

Remote-control connectivity never grants authority by itself.

## 16. Voice, Conversation Ledger and group agents

Focusa Spec 181 is the primitive owner for spoken interaction semantics.

Veragensia Doc 197 supplies the OS experience:

```text
trusted microphone/audio endpoint
→ ASR hypothesis
→ Focusa Conversation/Utterance
→ canonical operation/agent reasoning
→ Focusa ExpressionOutput
→ TTS/spoken output
```

A governed Conversation Ledger preserves:

- every human/agent utterance;
- speaker/agent principal attribution or explicit uncertainty;
- timestamps/word timings where available;
- overlap and interruption;
- transcript revisions/corrections;
- addressed-to/reply-to relationships;
- exact agent ExpressionOutput and spoken-delivery state;
- actions triggered by utterances;
- Evidence/Receipt/outcome links.

Multi-agent spoken rooms keep every expert independently attributable. Synthetic voice is presentation, never principal identity or authority.

Conversation remains distinct from canonical memory/state. Promotion into Workpoints, Evidence, knowledge, policies or ontology follows the existing governed path.

## 17. Telemetry and improvement

Doc 192 defines a privacy-tiered Veragensia Telemetry Plane across physical/cloud Agent Computers, workcells, Agent Apps, browser contexts and Silent Sessions.

Default hierarchy:

```text
bounded allowlisted metrics
→ structured/redacted events
→ sampled task traces
→ explicit artifacts

Conversation Ledger / private content = separate local-first domains
```

Telemetry schemas enforce field allowlists and cardinality ceilings. Generic telemetry labels cannot smuggle filenames, URLs, transcript/audio, prompts, speaker names or arbitrary model strings.

Voice quality can be measured through content-free latency/correction/uncertainty/task-success metrics without uploading conversation content.

Telemetry can inform software Agentability, reliability and cost decisions; it does not become user memory or architecture authority.

## 18. Packaging and update policy

Consume Omarchy without patching its package-owned source. Use supported user/plugin/service interfaces. v0.1 can use an idempotent, pinned native installer while later signed package distribution is developed; do not put package-repository or custom-ISO work on the initial proof's critical path.

Native and webtop installers are different target adapters. The existing webtop `overlay/install.sh` is not a native installer. Update/rollback must preserve unrelated configuration, user work and Focusa data. OS snapshots do not automatically define valid cognitive, conversation or external-effect rollback.

Doc 196 requires first-party compatibility/runtime re-attestation after material updates. A process starting successfully is not enough to retain trusted/enforceable capability status.

Agent Computer Profiles and application capability resolution should evolve independently of the base OS installer where practical. Adding or changing a default application must not require redefining Focusa authority or the core profile ontology.

## 19. Release sequence

| Stage | Deliverable and evidence |
|---|---|
| Existing Phase 0 | Public webtop proving ground under Doc 183; independently maintained |
| Native v0.1 | Stock supported Omarchy, native status/Work surface, existing Focusa continuity, one bounded real-agent task, artifact review, tested stop and rollback |
| Foundation expansion | Enforced ExecutionPrincipal/EnforcementPlan, ResourceRef/runtime-incarnation, secure attention/control lease, runtime attestation, Human Control Reserve |
| Full-profile expansion | Focusa Desktop, Pi/reference harness, UIAI/Cockpit, Voice/Conversation service, capability resolver and voice-complete outcome parity |
| Elastic execution expansion | Full Cloud Agent Computer runtime, headless workcells, Agent Apps/browser contexts, evidence-backed handoff/lifecycle and bounded TopologyGrant |
| Fleet/optimization | Mixed-topology team requests, voice-native orchestration, Agent Assist and telemetry-driven optimization |
| Distribution | Reproducible installation/provisioning and broader qualified hardware/profile/trust support |

The old calendar estimates are not retained as delivery promises. Each stage is evidence-gated. Native v0.1 remains a constrained proof and must not be presented as full voice/enforcement parity.

## 20. Licensing and trust classes

Existing Focusa/UIAI licensing and entitlement authority remain in force. Unknown, invalid, stale or unsupported entitlement never grants premium capabilities. Normal base desktop use remains available. No testing flag, internal tier, fake lease, platform root or runtime attestation may mint a real user's product authority.

The public demo is explicitly `public_demo`; private operator/authentication contexts have separate identity, retention and revocation requirements. Doc 183 and AGENTS.md remain authoritative for live behavior and credential handling.

Profile selection and infrastructure availability never create application entitlement. Platform trust, software attestation and product entitlement are independent inputs.

## 21. Acceptance and open boundaries

Doc 186 defines the required immediate native gate IDs. A native release is not accepted from a theme screenshot or a fixture alone.

A future **full Agent Computer** claim additionally requires evidence for:

- machine-enforced capability isolation (Doc 193);
- trusted secure attention and human control (Doc 194);
- stable ResourceRef/runtime-incarnation semantics (Doc 195);
- compatible platform/runtime attestation (Doc 196);
- full voice-complete workflows and Conversation Ledger continuity (Doc 197 / Focusa 181);
- Focusa Desktop/Pi/UIAI canonical surface composition;
- capability-based app resolution;
- Agent Assist control fencing/re-observation;
- privacy-safe telemetry.

Still requiring implementation evidence: native installer; session bridge and plugin; exact Omarchy version set; compatible private Workforce/UIAI builds; chosen governed runner and containment; owner/device acceptance; enforcement compiler; workload identity; secure attention; full-profile app resolution; Cloud Agent Computer runtime beyond public demo; voice service/ledger projection; Agent Assist; telemetry plane.

These are explicit gaps, not claimed finished components.

## 22. Planning discipline and references

Use repository-local `br` for tasks/dependencies. Specifications and release gate metadata are contracts, not duplicate execution backlogs.

- [182b — base and overlay](182b-veragensia-base-os-and-overlay-detailed-spec.md)
- [182c — fleet/elastic bridge](182c-veragensia-fleet-scale-tailnet-spec.md)
- [185 — architecture authority](185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md)
- [186 — native v0.1 requirements](186-veragensia-v0.1-native-chromebook-release-spec.md)
- [187 — Chromebook installation](187-veragensia-chromebook-first-install-runbook.md)
- [188 — decisions and wire contracts](188-veragensia-v0.1-decisions-and-integration-contracts.md)
- [190 — agent-first software and capability resolution](190-veragensia-agent-first-software-and-capability-resolution-spec.md)
- [191 — Elastic Agent Computing and cloud runtime](191-veragensia-elastic-agent-computing-and-cloud-runtime-spec.md)
- [192 — telemetry and improvement plane](192-veragensia-telemetry-and-improvement-plane-spec.md)
- [193 — execution substrate and enforcement](193-veragensia-execution-substrate-workload-identity-and-capability-enforcement-spec.md)
- [194 — trusted control and desktop observation](194-veragensia-trusted-human-control-secure-attention-and-desktop-observation-spec.md)
- [195 — resource identity and runtime incarnation](195-veragensia-resource-identity-runtime-incarnation-and-state-transfer-spec.md)
- [196 — platform trust and attestation](196-veragensia-platform-trust-genesis-supply-chain-and-runtime-attestation-spec.md)
- [197 — voice-native Agent Computer](197-veragensia-voice-native-agent-computer-audio-ui-and-conversation-continuity-spec.md)
- Focusa `docs/181-focusa-voice-conversation-expression-and-auditable-interaction-spec.md` — conversation primitive.
- [Omarchy shell plugins](https://omarchy.org/manual/shell-plugins/) and [supported user configuration](https://omarchy.org/manual/dotfiles/), checked 2026-09-04.
