# Veragensia — the Focusa Agent OS

> *ver-* (truth) + *agens* (the actor) + *-ia* (realm) — **the realm of the true agent.**

Veragensia is an **agent/human operating environment**: a real Linux desktop where people and governed agents work side by side. It brings Focusa's existing primitives into the operating environment rather than creating another agent framework or independent authority.

**Live build-in-public demo / agent playground:** <https://os.focusa.dev>

## Native Chromebook v0.1 — start here

The next implementation target is a **native Omarchy developer preview**, with project continuity, a native Work panel, one bounded agent run, artifact review, and reliable cancellation. The recovered hardware planning target is Dell Chromebook 11 CC11260 / expected `ULDRENITE`; the actual board and Linux behavior must be checked on the device.

**Current status: specification and bring-up planning, not a released native v0.1 installer.** The existing `overlay/install.sh` applies KDE/webtop branding. Do not run it on a Chromebook expecting a native Omarchy installation.

- [186 — v0.1 release specification and acceptance gates](docs/186-veragensia-v0.1-native-chromebook-release-spec.md)
- [187 — exact-device installation and bring-up runbook](docs/187-veragensia-chromebook-first-install-runbook.md)
- [188 — engineering decisions, CLI, IPC, and integration contracts](docs/188-veragensia-v0.1-decisions-and-integration-contracts.md)
- [190 — agent-first software and capability resolution](docs/190-veragensia-agent-first-software-and-capability-resolution-spec.md)
- [191 — Elastic Agent Computing and cloud runtime](docs/191-veragensia-elastic-agent-computing-and-cloud-runtime-spec.md)
- [192 — telemetry and improvement plane](docs/192-veragensia-telemetry-and-improvement-plane-spec.md)
- [193 — execution substrate, workload identity, and capability enforcement](docs/193-veragensia-execution-substrate-workload-identity-and-capability-enforcement-spec.md)
- [194 — trusted human control, secure attention, and desktop observation](docs/194-veragensia-trusted-human-control-secure-attention-and-desktop-observation-spec.md)
- [195 — resource identity, runtime incarnation, and state transfer](docs/195-veragensia-resource-identity-runtime-incarnation-and-state-transfer-spec.md)
- [196 — platform trust, genesis, supply chain, and runtime attestation](docs/196-veragensia-platform-trust-genesis-supply-chain-and-runtime-attestation-spec.md)
- [197 — voice-native Agent Computer, Audio UI, and conversation continuity](docs/197-veragensia-voice-native-agent-computer-audio-ui-and-conversation-continuity-spec.md)
- [198 — foundation integration and native-v0.1 scope guard](docs/198-veragensia-foundation-integration-and-native-v0.1-scope-guard-addendum.md)
- [199 — Ambient Operator, Companion sync, and Omarchy integration](docs/199-veragensia-ambient-operator-companion-sync-and-omarchy-integration-spec.md)
- [199A — dated Omarchy/Android/iOS platform qualification evidence](docs/199a-veragensia-current-platform-qualification-evidence-2026-09-05.md)
- [200 — ordered Living Agent Computer implementation tranches](docs/200-veragensia-living-agent-computer-implementation-tranche-plan.md)
- [200A — semantic-operation/dictation critical-path amendment](docs/200a-veragensia-semantic-operation-and-dictation-critical-path-amendment.md)
- [201 — semantic OS operations, keybinding projection, and VoxType integration](docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md)
- [201A — current Omarchy keybinding and VoxType evidence](docs/201a-veragensia-current-omarchy-keybinding-and-voxtype-evidence-2026-09-05.md)
- [201B — Obsidian Agent App/vault and SingleEye retrieval evidence](docs/201b-veragensia-obsidian-agent-app-vault-and-singleeye-retrieval-evidence-2026-09-05.md)
- [Semantic system-operation/keybinding map](docs/contracts/system-operation-keybinding-map.v1.yaml)
- [Ambient Operator convergence map](docs/contracts/ambient-operator-convergence-map.v1.yaml)
- [Machine-readable candidate/dependency inventory](config/v0.1-release-candidate.json)

These documents distinguish existing capabilities, selected engineering proposals, implementation gaps, and device evidence. Downloading Focusa binaries or booting Omarchy does not establish Veragensia release readiness. Doc 198 explicitly prevents the constrained native v0.1 proof from being mistaken for the limits of the full enforcement- and voice-native Agent Computer. Doc 200 is the implementation sequencing contract; Doc 200A inserts the semantic-operation layer between native shell projection and voice-control closure. Mutable execution state belongs in repository-local `br`, not in these specs.

## Composition and ownership

```text
Veragensia trusted shell / semantic OS operations / secure attention / audio UI / enforcement
                    |
Focusa Desktop + Pi reference harness + UIAI Engine/Cockpit
                    |
Existing Focusa daemon: scoped cognition, authority, evidence, conversation lineage
                    |
Linux / Omarchy + governed execution principals / workcells / Agent Apps
```

The diagram is a responsibility map, not a second kernel or a claim that every proposed native component already exists.

- **Base:** upstream Omarchy, consumed through supported integration points. The current public proving ground is separately based on Ubuntu/KDE webtop.
- **Focusa primitives:** re-homed, not rebuilt: project/continuity, Worksets/Workpoints, sessions, authorization, approvals, credentials, pairing, work loop, roles, surfaces, events, audit, Expression Engine, and Voice/Conversation lineage.
- **Focusa Desktop:** default governed human work/cognition presentation on supported full Agent Computer profiles; it remains a presenter over Focusa authority rather than an independent state or authority layer.
- **Pi:** default/reference Focusa-aware agent harness on supported profiles. The Focusa Pi extension is fundamental to the reference integration, while canonical cognition/state remains in Focusa daemon/core and non-Pi harnesses remain supported through thin adapters.
- **UIAI Engine + Cockpit:** deliberately listed first-party browser/computer execution, observation, diagnostics, oversight, and proof surfaces for the Agent Computer. They are foundational, not one browser candidate among many.
- **Veragensia semantic OS operations:** Omarchy/Hyprland keybindings become human projections of stable system operations that agents, voice, mobile and CLI can call directly. Agent speed comes from the operation underneath the key, not from replaying human shortcuts.
- **Veragensia enforcement substrate:** converts Focusa semantic authority into real filesystem/network/session/device/credential/resource restrictions. Same Unix UID or root transport does not count as authorization.
- **Voice / Audio UI:** a canonical full-profile surface. Keyboard and mouse are optional peripherals: supported ordinary work must be achievable through natural spoken interaction, with full agent audio response and Focusa's speaker-attributed Conversation Ledger.
- **Ambient Operator:** optional but first-class personal/ambient profile extending the same Focusa/Veragensia environment through a paired phone, earbuds or future wearable. Project Foreman, Radar and Conversation remain Focusa-owned; Veragensia supplies trusted Linux audio, Companion sync and native integration.
- **Native presentation:** plugin-generation Omarchy is the proposed target; validate exact versions instead of assuming compatibility or installing a second shell.

An **Agent Cloud Computer** is a provisioned, streamable Veragensia instance. Remote execution providers are optional adapters, not dependencies for ordinary local desktop use.

## Agent-first software doctrine

A Veragensia Agent Computer is intentionally stocked for **agent leverage**, not merely human familiarity. Default software should expose structured, semantic, inspectable machine surfaces wherever possible while remaining good human software. Full visual computer use remains the universal fallback.

The preferred execution hierarchy is:

```text
structured capability
→ semantic application automation
→ visual computer use
```

Applications are ranked by agentability: Veragensia-native typed integration first, then agent-native protocols, programmatic automation, semantic UI, and finally pixel-only control. Profiles should request **capabilities** rather than freezing package names, with an Agent App Resolver choosing the best compatible implementation for platform, trust class, entitlement, resources, privacy, enforceability, runtime attestation, and user preference.

See [Doc 190](docs/190-veragensia-agent-first-software-and-capability-resolution-spec.md). The detailed default application catalog is intentionally deferred for a later evidence-based software evaluation.

## Semantic OS operation doctrine

**Omarchy's keyboard speed is the floor, not the ceiling. Humans keep the hotkeys; agents get the operations underneath them.**

A meaningful system hotkey is not the canonical machine interface. Veragensia maps the live Omarchy/Hyprland keymap onto stable `SystemOperationDescriptor` objects so the same behavior can be invoked through:

```text
human hotkey
voice
Pi / Foreman / Wirebot
Ambient Operator
CLI / API
automation / hardware control
```

Preferred execution for shell/system work is:

```text
Focusa/Veragensia typed operation
→ Omarchy CLI
→ Hyprland/native dispatcher
→ application API/CLI/protocol
→ semantic/accessibility UI
→ UIAI observation-bound computer use
→ guarded key/text injection only as compatibility fallback
```

User `~/.config/hypr/bindings.lua` customizations remain owner-controlled. Key remapping changes the human projection, not the operation identity. A full profile requires live keymap discovery and zero unexplained `unmapped_gap` entries.

Current Omarchy already uses VoxType for dictation. Veragensia therefore treats VoxType as a preferred capture/ASR/dictation/meeting adapter candidate instead of inventing a redundant desktop dictation stack. VoxType's normal “type/paste at cursor” behavior is compatibility dictation; semantic voice control still flows through Focusa Conversation and Veragensia system operations. See Docs 201/201A.

Obsidian is an early structured Agent App proof: when a compatible Obsidian CLI is installed, agents should use vault/search/read/edit/command/query operations rather than launch it and emulate its hotkeys. The separate Startempire Obsidian knowledge vault remains an owner-knowledge domain, not the same thing as the local Obsidian application profile. See Doc 201B.

## Enforcement doctrine

**Focusa decides what a governed actor may do. Veragensia makes the machine behave as though that decision is real.**

The foundational substrate is:

```text
Focusa AuthorityDecision / CapabilityGrant
        ↓
Veragensia EnforcementPlan
        ↓
ExecutionPrincipal + WorkloadIdentity
        ↓
filesystem · network · D-Bus · Wayland · accessibility
screen/audio/input · devices · credentials · cgroups
        ↓
actual process/effect
```

Doc 193 owns enforcement, Doc 194 trusted human control/desktop observations, Doc 195 stable resources/runtime incarnations, and Doc 196 platform/runtime trust.

## Voice-native doctrine

**Keyboard and mouse are optional peripherals.**

A voice-complete full Agent Computer supports natural full-duplex interaction for navigation, work, editing, browser/computer use, agent/team orchestration, approvals, interruption, recovery, and audit without forcing the human to translate goals into pointer mechanics.

```text
human speech
→ Focusa Conversation / current ask
→ semantic system/application operation
→ governed execution
→ Evidence / Receipt
→ Focusa ExpressionOutput
→ spoken agent response
```

Every participant remains attributable. Every governed conversation remains searchable and auditable. The user can go back through what they said, what each agent/expert said, transcript corrections, interruptions, actions, Evidence and Receipts. Conversation history remains distinct from canonical memory/authority.

See [Doc 197](docs/197-veragensia-voice-native-agent-computer-audio-ui-and-conversation-continuity-spec.md), [Doc 201](docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md), and Focusa Spec 181.

## Ambient Operator doctrine

The Agent Computer can remain continuously reachable when the owner leaves the desk without cloning its cognition onto a phone.

```text
phone / earbuds / wearable
        ↓
Focusa Ambient Operator
        ↓
Wirebot Chief of Staff or exact Project Foreman
        ↓
Focusa authority / Radar / Conversation
        ↓
Veragensia + UIAI execution
```

Key laws:

- **phone and earbuds are paired surfaces, not new brains;**
- **Project Foreman is one Workstream's persistent project-intelligence projection;**
- **Radar notices and scores developing situations; it does not mint authority or become hidden surveillance;**
- **Wirebot may hold broader owner-authorized life/portfolio context and delegate to exact Foremen;**
- **meeting/audio history is auditable provenance, not automatic canonical memory;**
- **raw phone GPS/sensor state remains in its owner domain by default and enters Focusa through bounded projections;**
- **Bluetooth is useful for nearby audio/control/proximity, while authenticated LAN/Tailscale/private-network sync carries bulk conversation/evidence data;**
- **mobile sync never writes Focusa persistence directly.**

See [Doc 199](docs/199-veragensia-ambient-operator-companion-sync-and-omarchy-integration-spec.md), [Doc 200](docs/200-veragensia-living-agent-computer-implementation-tranche-plan.md), and Focusa Specs 182–184.

## Omarchy/Linux integration doctrine

Stock Omarchy remains the native base. Veragensia uses supported user/plugin/session integration and keeps upstream package-owned source untouched.

A Quickshell/Omarchy plugin is intentionally a **thin presenter**. Trusted responsibilities such as microphone capture, Companion sync, enforcement, credentials and canonical Focusa state live in separate bounded services/workloads. A QML panel does not become Secure Attention or authority merely because it looks first-party.

The intended full-profile native topology is:

```text
focusa-daemon       cognition / authority / Foreman / Radar / Conversation
veragens-sessiond   native session + Omarchy/Hyprland + SystemOperation projection
veragens-audiod     trusted audio endpoint/capture/playback broker
veragens-syncd      paired Companion sync / offline queue reconciliation
uiai-engine         browser/computer execution + proof
Pi + extension      reference harness
```

Early developer builds may use smaller adapters, but must report the difference honestly. Current upstream/platform assumptions are recorded as dated evidence in Docs 199A and 201A and must be re-verified before release qualification.

## Architecture principles

**Surfaces are interchangeable; primitives are the platform.**

**Cloud coordinates. Node decides. Receipts prove. Private state stays local.**

**Observe within scope; act under authority; preserve useful work.**

**Prefer structured capability, then semantic automation, then visual computer use.**

**Hotkeys are projections, not APIs.**

**Semantic authority is not enough until the machine enforces it.**

**Keyboard and mouse are optional; conversation is a first-class operating surface.**

**Ambient does not mean omniscient, always-recording, or globally authoritative.**

[Doc 185](docs/185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md) identifies **Verious Smith III as the sole current and final canonical human architecture authority**. Focusa operational authority, repository presence, external proposals, external software, and historical vault notes do not confer architecture ownership. Future Wirebot authority requires explicit verified delegation; a name or hash alone does not grant it.

## Repository

- `overlay/` — current webtop branding and the home of future native integrations.
- `scripts/` — lab lifecycle, atomic deployment, browser launcher, narrow remote control, and evidence tooling.
- `ops/sudoers/` — least-privilege deployment templates for the live lab.
- `docs/182*` — product, base/overlay, and fleet specifications.
- `docs/183-*` — live public-computer security and lifecycle contract.
- `docs/185-*` — architecture authority and provenance policy.
- `docs/186-*`, `187-*`, `188-*` — proposed native v0.1 implementation and bring-up contracts.
- `docs/190-*` — Agent Computer software doctrine, agentability, capability profiles, and Agent App resolution.
- `docs/191-*` — Elastic Agent Computing, Cloud Agent Computer runtime, workcells, Agent Apps, Agent Assist, and mixed topology.
- `docs/192-*` — privacy-tiered telemetry, Agentability measurement, and the evidence-to-improvement loop.
- `docs/193-*` — machine enforcement, ExecutionPrincipal, WorkloadIdentity and EnforcementPlan.
- `docs/194-*` — trusted secure attention, desktop observations and computer-control leases.
- `docs/195-*` — stable ResourceRefs, runtime incarnations, replicas and typed state transfer.
- `docs/196-*` — boot/platform trust, genesis, supply-chain binding and runtime attestation.
- `docs/197-*` — voice-native Audio UI, keyboard/mouse independence, group conversation and transcript/audit continuity.
- `docs/198-*` — explicit amendment keeping the constrained Chromebook v0.1 proof subordinate to the full enforcement/voice-native architecture.
- `docs/199-*` — Focusa Ambient Operator, Companion sync, Android/iOS/wearable edge, Omarchy plugin/service topology and UIAI execution convergence.
- `docs/199a-*` — dated upstream-platform qualification evidence for Omarchy/Android/iOS.
- `docs/200-*` / `200a-*` — Living Agent Computer tranches plus required semantic-operation bridge before voice-control closure.
- `docs/201-*` — semantic OS operation/keybinding/VoxType architecture plus Obsidian/SingleEye retrieval evidence.
- `docs/contracts/ambient-operator-convergence-map.v1.yaml` — machine-readable ownership/dependency/acceptance map; mutable execution work remains in `br`.
- `docs/contracts/system-operation-keybinding-map.v1.yaml` — machine-readable semantic operation/keybinding families and acceptance map.

## Run the existing lab

```bash
scripts/uiai-lab-live up
scripts/uiai-lab-live persist on
scripts/uiai-lab-push
```

These are existing lab operations, not Chromebook-install commands. The public demo is a `public_demo` trust class: operator/provider credentials must never persist in its public profile. Privileged authentication requires a separate authorized private context. See Doc 183 and `AGENTS.md`.

## Planning and releases

Use repository-local beads_rust through **`br` only**. Do not maintain duplicate execution backlogs in GitHub issues or Markdown. Specification acceptance IDs, convergence maps and tranche plans are contracts/decomposition inputs, not a second task tracker.

The operator and planning agent determine canonical decisions and sequencing. Proposed specifications must not be described as implemented merely because they are committed. Native release tagging requires the evidence gates in Doc 186; this documentation update does not publish a release or alter the live demo.

## License

TBD. Omarchy is MIT; Focusa primitives are source-available. Existing licensing and entitlement boundaries remain in force. See the product specification's open questions.
