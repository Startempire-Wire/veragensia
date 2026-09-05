# 182 — Veragensia · Focusa Agent OS and Agent Cloud Computer

**Status:** DRAFT canonical product direction; native v0.1 implementation proposal added 2026-09-04.
**Canonical human architecture authority:** Verious Smith III, under Doc 185.
**Original naming/product draft:** 2026-08-26. The prior draft is preserved in Git at `948e9080efa1f52662b159193523e9c12a3d05a3`; this revision explicitly updates the native integration and release framing rather than claiming the old GUI plan was implemented.
**Live proving ground:** `https://os.focusa.dev`, governed separately by Doc 183.
**Companions:** 182b (base/overlay), 182c (fleet bridge), 183 (public lifecycle), 185 (authority), 186 (native v0.1), 187 (Chromebook bring-up), 188 (integration contracts), 190 (agent-first software), 191 (Elastic Agent Computing), 192 (telemetry/improvement).

## 1. Product and naming

**Veragensia** is the Focusa Agent OS: a human-owned operating environment with governed agents as native participants. **Veragens** is the short form and CLI/package naming direction. A provisioned, streamable instance is an **Agent Cloud Computer**.

The product lifts existing Focusa primitives from extension/daemon interaction into desktop services and native surfaces. It does not replace Linux, create a deep Omarchy fork, or make the browser extension the only interface.

> Surfaces are interchangeable; primitives are the platform.

The useful experience is continuous work across applications: explicit project context, recoverable progress, bounded assistance, understandable changes, dependable stop/recovery controls, and the ability to expand into cloud compute or additional agent workforce without making the user manually design infrastructure.

Agent-first must not make normal desktop interaction depend on a model call.

## 2. Authority and ownership

Verious Smith III remains the architecture root. Focusa owns its scoped operational state, not the product's constitutional authority. Veragensia owns the assigned OS integration substrate; UIAI owns its browser runtime. Customer identities, issue authors, agents, repository presence, model outputs, or external platforms do not mint architecture authority. Doc 185 controls conflicts and future Wirebot delegation.

Do not introduce competing Veragensia memory, task, grant, or truth stores where an existing Focusa primitive already owns the concern. A presentation cache is not canonical state.

## 3. Platform composition

| Layer | Responsibility |
|---|---|
| Stock Omarchy / Arch / Hyprland | Hardware, session, compositor, system lifecycle, supported desktop integration points |
| Veragensia shell/session integration | Work context, lifecycle, application composition, interruption, review, containment and recovery |
| Focusa Desktop | Default governed human work/cognition presentation on supported full profiles; presenter only, not a second cognitive authority |
| Pi + Focusa Pi extension | Default/reference Focusa-aware agent harness integration; typed tools, skills/runbooks, scope/authority hooks and recovery |
| Existing Focusa daemon/core | Project/continuity, Workpoints, Worksets, authorization, sessions, evidence, operational reduction/persistence, learning and recovery |
| UIAI Engine + Cockpit/Workforce browser surfaces | First-party governed browser/computer perception, action, diagnostics, oversight and proof |
| Execution adapters | Enforced local/cloud workcells, Agent Apps and other runtimes under existing permission/resource semantics |

The current public demo remains a separate Ubuntu/KDE webtop implementation. Its existence does not demonstrate native Omarchy compatibility.

### 3.1 Canonical full Agent Computer defaults

A supported **full Agent Computer profile** deliberately includes, unless the profile/trust class/resource boundary explicitly omits one:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser surfaces;
- Veragensia native/session integration.

UIAI Engine is foundational and is deliberately listed so it cannot later be misread as one optional browser candidate among many.

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
| Authorization / approvals | Consequence-specific native prompts using existing authority; no grant stored in QML |
| Credentials / pairing | Private enrolled surfaces and scoped credentials; no public-profile or LAN-token shortcuts |
| Ontology / evidence / verification | Shared meaning and inspectable support; no equation of graph validity with factual truth |
| Reflexes / secondary cognition | Bounded observation, salience and escalation through existing Focusa mechanisms |
| Reliability / trust evidence | Contextual evidence influencing routing/verification, never overriding permission |
| Events / audit | Freshness-aware native status and durable outcome evidence owned by the appropriate runtime |

Implementation must resolve the actual supported operation descriptors and prove both producer and consumer behavior. A generic `can(...)` diagram is not proof of enforced OS containment.

## 5. Privacy and agent execution

Intelligence can participate widely; perception remains purposeful and scoped. No default capture of clipboard, keystrokes, private window contents, microphone, camera, or arbitrary home-directory content. Observations may be tentative and transient; they do not automatically become memories or actions.

The owner retains ordinary control of the computer. Veragensia must distinguish governed runs from unmanaged upstream launchers. Untrusted code needs enforced separation from user files, session sockets and credentials. A prompt, process label, systemd scope, or shell panel is not sufficient isolation.

A run may prepare a draft or patch within its approved output scope. Replacing originals, publishing, spending, changing system packages, or expanding access are separate authorized operations. Lost connections and failed cancellation must appear as uncertain/pending rather than falsely complete.

## 6. Native experience

Native surfaces should provide: selected work context; continuation; bounded agent activity; artifact review; understandable approvals; explicit stop; and visible stale/degraded state. Avoid a permanent giant AI dashboard or simulated cognition. Useful state changes should be visible without notification floods.

**Focusa Desktop** is the default governed full-desktop work/cognition presentation surface. Native Veragensia shell surfaces complement it with ambient OS context and controls rather than silently replacing its Focusa-owned presenter contracts.

A workspace association is an aid to navigation, not proof of intent. Agents should work in separate bounded environments without stealing pointer/focus from the human. Accessibility, pointer use, keyboard navigation, readable scaling, reduced motion, and honest limitations are acceptance concerns, not later visual polish.

## 7. Chromebook and constrained hardware

Reclaimed/constrained hardware is a design target, not an excuse for degraded foreground interaction. Reuse Focusa's existing constrained/LowMem mechanisms. Keep essential local continuity and normal desktop behavior independent of a mandatory resident model or cloud service.

The initial recovered planning target is Dell Chromebook 11 CC11260 / expected ULDRENITE. Exact board, firmware procedure, resource capacity and Linux hardware qualification are device gates in Doc 187. ChromeOS Linux-container integration and remote access are distinct modes, not native Omarchy substitutes.

A constrained preview profile does not need to install every canonical full-profile surface on day one. It must state what is omitted and why, and must not claim parity with a full Agent Computer until the relevant capability/profile gates pass.

Idle, locked, and suspended are different states. Absence never broadens permissions. Do not enable unattended work or lingering automatically.

## 8. Agent-first software and applications

A Veragensia Agent Computer should be intentionally stocked with software selected for **agent leverage**, not merely human familiarity.

The preferred control hierarchy is:

```text
1. Structured capability
   typed operation / API / CLI / MCP / ACP / application protocol

2. Semantic application automation
   accessibility / DOM / application object model / stable semantic refs

3. Computer use
   visual desktop / pointer / keyboard / arbitrary application
```

Level 3 remains mandatory as the universal fallback, but default applications should minimize how often agents need fragile pixel-only interaction.

Doc 190 defines:

- Agentability Classes;
- capability-first Agent Computer Profiles;
- the Agent App Resolver;
- versioned Agent App descriptors;
- first-party default composition;
- the deferred evidence-based Agent-First Software Catalog.

Pi is fundamental to Focusa's reference agent experience. It is the default/reference harness integration, not a second cognitive authority. Non-Pi harnesses remain first-class through thin Focusa adapters and generated capability contracts.

## 9. UIAI Engine and browser/computer execution

UIAI Engine is the first-party browser and browser-adjacent execution/proof system for Veragensia. It is deliberately part of the canonical Agent Computer composition.

Chromium plus Focusa Workforce remains a first-class private surface. The native preview must use a private profile and the same enrolled Focusa identity; current public demo browser profiles and credentials must not be copied to the laptop.

Veragensia should consume UIAI's existing Agent-First Browser contracts rather than inventing a parallel browser automation layer: compact capability discovery, versioned observations, observation-bound actions, semantic refs, Focusa-directed verification, provenance/influence controls, execution capsules, Cockpit oversight and visual fallback.

UIAI's intent verbs, resource budgets, screenshots/artifact references, and event stream remain browser implementation concerns. Native messaging may become a later transport adapter; it is not required before proving the existing supported private pairing path. Do not expose raw CDP or daemon ports to make integration convenient.

## 10. Elastic Agent Computing and cloud runtime

The existing private control-plane companion remains spec 115 and its approved addenda:

> Cloud coordinates. Node decides. Receipts prove. Private state stays local.

Cloud execution is no longer modeled only as optional headless workers. Doc 191 defines **Elastic Agent Computing** across:

- full streamed Agent Computers;
- headless workcells;
- Focusa Silent Session teams;
- Agent Apps;
- UIAI browser contexts;
- remote specialist runtimes.

The user requests capability, workforce, or a profile. Veragensia resolves the topology.

`os.focusa.dev` is the first crude implementation of the correct **Cloud Agent Computer Runtime shape**: streamed Linux desktop, persistent `/config`, Chromium/Workforce, local Focusa daemon, Selkies streaming, tunnel and keeper lifecycle. It remains a `public_demo` trust profile governed by Doc 183.

Fly/Sprites and other infrastructure are provider/adaptor concepts, not architecture authority or required local dependencies. Workcell specializes existing Focusa ExecutionContext/affordance concepts rather than adding a parallel permission/identity model. Infrastructure leases are not automatic authorization for application actions. Filesystem restore, process resume, cognitive continuity and reversal of external effects remain distinct.

Multi-agent execution must build on Focusa exact routing, writer leases/idempotency, mutation/effect receipts and isolated workspaces/worktrees. Many agents must not become many independent writers that each believe they own the same writable world.

## 11. Agent Assist

A full Agent Computer may support first-class **Agent Assist Sessions** with modes such as:

```text
observe_only
→ guide
→ shared_control
→ delegated_control
```

The session binds the human, agent principal, Agent Computer, task/Workpoint, observation/action scope and authority. The agent should prefer structured/semantic operations but may use the full desktop when needed. Human interruption/revocation and Evidence/receipt capture are required where applicable.

Remote-control connectivity never grants authority by itself. See Doc 191.

## 12. Telemetry and improvement

Doc 192 defines a unified privacy-tiered Veragensia Telemetry Plane across physical/cloud Agent Computers, workcells, Agent Apps, browser contexts and Silent Sessions.

Default hierarchy:

```text
metrics → structured/redacted events → sampled task traces → explicit artifacts
private content stays local by default
```

The purpose is a product improvement flywheel:

```text
Telemetry → Pattern → Evidence → Improvement Candidate → Spec/br → Implementation → Release → comparison
```

Telemetry can inform software Agentability, reliability and cost decisions; it does not become user memory or architecture authority.

## 13. Packaging and update policy

Consume Omarchy without patching its package-owned source. Use supported user/plugin/service interfaces. v0.1 can use an idempotent, pinned native installer while later signed package distribution is developed; do not put package-repository or custom-ISO work on the initial proof's critical path.

Native and webtop installers are different target adapters. The existing webtop `overlay/install.sh` is not a native installer. Update/rollback must preserve unrelated configuration, user work and Focusa data. OS snapshots do not automatically define valid cognitive-state rollback.

Agent Computer Profiles and application capability resolution should evolve independently of the base OS installer where practical. Adding or changing a default application must not require redefining Focusa authority or the core profile ontology.

## 14. Release sequence

| Stage | Deliverable and evidence |
|---|---|
| Existing Phase 0 | Public webtop proving ground under Doc 183; independently maintained |
| Native v0.1 | Stock supported Omarchy, native status/Work surface, existing Focusa continuity, one bounded real-agent task, artifact review, tested stop and rollback |
| Native expansion | Focusa Desktop/full-profile presentation, broader governed application actions, improved packaging/accessibility, capability resolver foundations |
| Elastic execution expansion | Full Cloud Agent Computer runtime, headless workcells, Agent Apps/browser contexts, evidence-backed handoff/lifecycle |
| Fleet/optimization | Mixed-topology team requests, Agent Assist, bounded fleet scheduling and telemetry-driven optimization |
| Distribution | Reproducible installation/provisioning and broader qualified hardware/profile support |

The old calendar estimates are not retained as delivery promises. Each stage is evidence-gated. Doc 186 replaces the old undifferentiated native Phase-1/2 GUI framing for the immediate v0.1 proposal without declaring future phases complete.

## 15. Licensing and trust classes

Existing Focusa/UIAI licensing and entitlement authority remain in force. Unknown, invalid, stale or unsupported entitlement never grants premium capabilities. Normal base desktop use remains available. No testing flag, internal tier, or fake lease may unlock a real user's capabilities.

The public demo is explicitly `public_demo`; private operator/authentication contexts have separate identity, retention and revocation requirements. Doc 183 and AGENTS.md remain authoritative for live behavior and credential handling.

Profile selection and infrastructure availability never create application entitlement. The resolver must treat licensing/entitlement as an input, not something it can synthesize.

## 16. Acceptance and open boundaries

Doc 186 defines the required native gate IDs. A native release is not accepted from a theme screenshot or a fixture alone. Required evidence includes exact hardware, compatible dependencies, actual Focusa state projection, a real bounded agent result, isolation, cancellation, recovery and install rollback.

Still requiring implementation evidence: native installer; session bridge and plugin; exact Omarchy version set; compatible private Workforce build; chosen governed runner and containment; owner/device acceptance; full-profile app resolution; Cloud Agent Computer runtime beyond the public demo; Agent Assist; telemetry plane.

These are explicit gaps, not claimed finished components.

## 17. Planning discipline and references

Use repository-local `br` for tasks/dependencies. Specifications and release gate metadata are contracts, not duplicate execution backlogs. Do not edit other repositories or the live lab implicitly when revising this product proposal.

- [182b — base and overlay](182b-veragensia-base-os-and-overlay-detailed-spec.md)
- [182c — fleet/elastic bridge](182c-veragensia-fleet-scale-tailnet-spec.md)
- [185 — architecture authority](185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md)
- [186 — native v0.1 requirements](186-veragensia-v0.1-native-chromebook-release-spec.md)
- [187 — Chromebook installation](187-veragensia-chromebook-first-install-runbook.md)
- [188 — decisions and wire contracts](188-veragensia-v0.1-decisions-and-integration-contracts.md)
- [190 — agent-first software and capability resolution](190-veragensia-agent-first-software-and-capability-resolution-spec.md)
- [191 — Elastic Agent Computing and cloud runtime](191-veragensia-elastic-agent-computing-and-cloud-runtime-spec.md)
- [192 — telemetry and improvement plane](192-veragensia-telemetry-and-improvement-plane-spec.md)
- [Omarchy shell plugins](https://omarchy.org/manual/shell-plugins/) and [supported user configuration](https://omarchy.org/manual/dotfiles/), checked 2026-09-04.
