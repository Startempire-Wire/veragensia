# 182 — Veragensia · Focusa Agent OS and Agent Cloud Computer

**Status:** DRAFT product direction; native v0.1 implementation proposal added 2026-09-04.
**Canonical human architecture authority:** Verious Smith III, under Doc 185.
**Original naming/product draft:** 2026-08-26. The prior draft is preserved in Git at `948e9080efa1f52662b159193523e9c12a3d05a3`; this revision explicitly updates the native integration and release framing rather than claiming the old GUI plan was implemented.
**Live proving ground:** `https://os.focusa.dev`, governed separately by Doc 183.
**Companions:** 182b (base/overlay), 182c (fleet), 183 (public lifecycle), 185 (authority), 186 (native v0.1), 187 (Chromebook bring-up), 188 (integration contracts).

## 1. Product and naming

**Veragensia** is the Focusa Agent OS: a human-owned operating environment with governed agents as native participants. **Veragens** is the short form and CLI/package naming direction. A provisioned, streamable instance is an **Agent Cloud Computer**.

The product lifts existing Focusa primitives from extension/daemon interaction into desktop services and native surfaces. It does not replace Linux, create a deep Omarchy fork, or make the browser extension the only interface.

> Surfaces are interchangeable; primitives are the platform.

The useful experience is continuous work across applications: explicit project context, recoverable progress, bounded assistance, understandable changes, and dependable stop/recovery controls. Agent-first must not make normal desktop interaction depend on a model call.

## 2. Authority and ownership

Verious Smith III remains the architecture root. Focusa owns its scoped operational state, not the product's constitutional authority. Veragensia owns the assigned OS integration substrate; UIAI owns its browser runtime. Customer identities, issue authors, agents, repository presence, model outputs, or external platforms do not mint architecture authority. Doc 185 controls conflicts and future Wirebot delegation.

Do not introduce competing Veragensia memory, task, grant, or truth stores where an existing Focusa primitive already owns the concern. A presentation cache is not canonical state.

## 3. Platform composition

| Layer | Responsibility |
|---|---|
| Stock Omarchy / Arch / Hyprland | Hardware, session, compositor, system lifecycle, supported desktop integration points |
| Native Veragensia surfaces | Work context, agent activity, artifact review, approvals, interruption and recovery |
| Session adapter | Bounded observation and projection; scoped requests into existing Focusa contracts |
| Existing Focusa daemon | Project/continuity, Workpoints, Worksets, authorization, sessions, evidence, operational reduction/persistence |
| UIAI / Workforce | Governed browser perception/action and a private surface into the same Focusa state |
| Execution adapters | Enforced local or later remote environments under existing permission/resource semantics |

The current public demo remains a separate Ubuntu/KDE webtop implementation. Its existence does not demonstrate native Omarchy compatibility.

### Native shell revision

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

A workspace association is an aid to navigation, not proof of intent. Agents should work in separate bounded environments without stealing pointer/focus from the human. Accessibility, pointer use, keyboard navigation, readable scaling, reduced motion, and honest limitations are acceptance concerns, not later visual polish.

## 7. Chromebook and constrained hardware

Reclaimed/constrained hardware is a design target, not an excuse for degraded foreground interaction. Reuse Focusa's existing constrained/LowMem mechanisms. Keep essential local continuity and normal desktop behavior independent of a mandatory resident model or cloud service.

The initial recovered planning target is Dell Chromebook 11 CC11260 / expected ULDRENITE. Exact board, firmware procedure, resource capacity and Linux hardware qualification are device gates in Doc 187. ChromeOS Linux-container integration and remote access are distinct modes, not native Omarchy substitutes.

Idle, locked, and suspended are different states. Absence never broadens permissions. Do not enable unattended work or lingering automatically.

## 8. UIAI Engine and browser

Chromium plus Focusa Workforce remains a first-class product surface. The native preview must use a private profile and the same enrolled Focusa identity; current public demo browser profiles and credentials must not be copied to the laptop.

UIAI's intent verbs, resource budgets, screenshots/artifact references, and event stream remain browser implementation concerns. Native messaging may become a later transport adapter; it is not required before proving the existing supported private pairing path. Do not expose raw CDP or daemon ports to make integration convenient.

## 9. Focusa Cloud and optional execution providers

The existing private control-plane companion remains spec 115 and its approved addenda:

> Cloud coordinates. Node decides. Receipts prove. Private state stays local.

Public documentation can reference accounts, node registry, licensing, scoped pairing/relay, and redacted proof coordination without copying private implementation specifications. Native nodes retain their assigned execution/state authority.

Fly/Sprites-inspired lifecycle, checkpoints and isolated work environments are candidate adapter concepts, not a required v0.1 dependency. “Workcell” specializes existing Focusa ExecutionContext/affordance concepts rather than adding a parallel permission/identity model. Infrastructure leases are not automatic authorization for application actions. Filesystem restore, process resume, cognitive continuity and reversal of external effects remain distinct.

## 10. Packaging and update policy

Consume Omarchy without patching its package-owned source. Use supported user/plugin/service interfaces. v0.1 can use an idempotent, pinned native installer while later signed package distribution is developed; do not put package-repository or custom-ISO work on the initial proof's critical path.

Native and webtop installers are different target adapters. The existing webtop `overlay/install.sh` is not a native installer. Update/rollback must preserve unrelated configuration, user work and Focusa data. OS snapshots do not automatically define valid cognitive-state rollback.

## 11. Release sequence

| Stage | Deliverable and evidence |
|---|---|
| Existing Phase 0 | Public webtop proving ground under Doc 183; independently maintained |
| Native v0.1 | Stock supported Omarchy, native status/Work surface, existing Focusa continuity, one bounded real-agent task, artifact review, tested stop and rollback |
| Native expansion | Richer work surfaces, additional approved application actions, improved packaging and accessibility |
| Execution expansion | Optional remote work environments, provider adapters, evidence-backed handoff and lifecycle |
| Distribution | Reproducible installation/provisioning and broader qualified hardware/fleet support |

The old calendar estimates are not retained as delivery promises. Each stage is evidence-gated. Doc 186 replaces the old undifferentiated native Phase-1/2 GUI framing for the immediate v0.1 proposal, without declaring future phases complete.

## 12. Licensing and trust classes

Existing Focusa/UIAI licensing and entitlement authority remain in force. Unknown, invalid, stale or unsupported entitlement never grants premium capabilities. Normal base desktop use remains available. No testing flag, internal tier, or fake lease may unlock a real user's capabilities.

The public demo is explicitly `public_demo`; private operator/authentication contexts have separate identity, retention and revocation requirements. Doc 183 and AGENTS.md remain authoritative for live behavior and credential handling.

## 13. Acceptance and open boundaries

Doc 186 defines the required native gate IDs. A native release is not accepted from a theme screenshot or a fixture alone. Required evidence includes exact hardware, compatible dependencies, actual Focusa state projection, a real bounded agent result, isolation, cancellation, recovery and install rollback.

Still requiring implementation evidence: native installer; session bridge and plugin; exact Omarchy version set; compatible private Workforce build; chosen governed runner and containment; owner/device acceptance. These are explicit gaps, not claimed finished components.

## 14. Planning discipline and references

Use repository-local `br` for tasks/dependencies. Specifications and release gate metadata are contracts, not duplicate execution backlogs. Do not edit other repositories or the live lab implicitly when revising this product proposal.

- [182b — base and overlay](182b-veragensia-base-os-and-overlay-detailed-spec.md)
- [185 — architecture authority](185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md)
- [186 — native v0.1 requirements](186-veragensia-v0.1-native-chromebook-release-spec.md)
- [187 — Chromebook installation](187-veragensia-chromebook-first-install-runbook.md)
- [188 — decisions and wire contracts](188-veragensia-v0.1-decisions-and-integration-contracts.md)
- [Omarchy shell plugins](https://omarchy.org/manual/shell-plugins/) and [supported user configuration](https://omarchy.org/manual/dotfiles/), checked 2026-09-04.
