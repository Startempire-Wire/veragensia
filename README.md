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
- [Machine-readable candidate/dependency inventory](config/v0.1-release-candidate.json)

These documents distinguish existing capabilities, selected engineering proposals, implementation gaps, and device evidence. Downloading Focusa binaries or booting Omarchy does not establish Veragensia release readiness.

## Composition and ownership

```text
Native Omarchy shell surfaces: work, agent activity, review, status
                    |
Veragensia session integration: observations, presentation, OS containment
                    |
Existing Focusa daemon: scoped state, continuity, authorization, evidence
                    |
Focusa Desktop + Pi reference harness + UIAI Engine/Cockpit
                    |
Stock Omarchy + Arch + Hyprland, consumed without a deep fork
```

The diagram is a responsibility map, not a second kernel or a claim that every proposed native component already exists.

- **Base:** upstream Omarchy, consumed through supported integration points. The current public proving ground is separately based on Ubuntu/KDE webtop.
- **Focusa primitives:** re-homed, not rebuilt: project/continuity, Worksets/Workpoints, sessions, authorization, approvals, credentials, pairing, work loop, roles, surfaces, events, and audit.
- **Focusa Desktop:** default governed human work/cognition presentation on supported full Agent Computer profiles; it remains a presenter over Focusa authority rather than an independent state or authority layer.
- **Pi:** default/reference Focusa-aware agent harness on supported profiles. The Focusa Pi extension is fundamental to the reference integration, while canonical cognition/state remains in Focusa daemon/core and non-Pi harnesses remain supported through thin adapters.
- **UIAI Engine + Cockpit:** deliberately listed first-party browser/computer execution, observation, diagnostics, oversight, and proof surfaces for the Agent Computer. They are foundational, not one browser candidate among many.
- **Native presentation:** plugin-generation Omarchy is the proposed target; validate exact versions instead of assuming compatibility or installing a second shell.

An **Agent Cloud Computer** is a provisioned, streamable Veragensia instance. Remote execution providers are optional adapters, not dependencies for ordinary local desktop use.

## Agent-first software doctrine

A Veragensia Agent Computer is intentionally stocked for **agent leverage**, not merely human familiarity. Default software should expose structured, semantic, inspectable machine surfaces wherever possible while remaining good human software. Full visual computer use remains the universal fallback.

The preferred interaction hierarchy is:

```text
structured capability
→ semantic application automation
→ visual computer use
```

Applications are ranked by agentability: Veragensia-native typed integration first, then agent-native protocols, programmatic automation, semantic UI, and finally pixel-only control. Profiles should request **capabilities** rather than freezing package names, with an Agent App Resolver choosing the best compatible implementation for platform, trust class, entitlement, resources, privacy, and user preference.

See [Doc 190](docs/190-veragensia-agent-first-software-and-capability-resolution-spec.md). The detailed default application catalog is intentionally deferred for a later evidence-based software evaluation.

## Architecture principles

**Surfaces are interchangeable; primitives are the platform.**

**Cloud coordinates. Node decides. Receipts prove. Private state stays local.**

**Observe within scope; act under authority; preserve useful work.**

**Prefer structured capability, then semantic automation, then visual computer use.**

[Doc 185](docs/185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md) identifies **Verious Smith III as the sole current and final canonical human architecture authority**. Focusa operational authority, repository presence, and external proposals do not confer architecture ownership. Future Wirebot authority requires explicit verified delegation; a name or hash alone does not grant it.

## Repository

- `overlay/` — current webtop branding and the home of future native integrations.
- `scripts/` — lab lifecycle, atomic deployment, browser launcher, narrow remote control, and evidence tooling.
- `ops/sudoers/` — least-privilege deployment templates for the live lab.
- `docs/182*` — product, base/overlay, and fleet specifications.
- `docs/183-*` — live public-computer security and lifecycle contract.
- `docs/185-*` — architecture authority and provenance policy.
- `docs/186-*`, `187-*`, `188-*` — proposed native v0.1 implementation and bring-up contracts.
- `docs/190-*` — Agent Computer software doctrine, agentability, capability profiles, and Agent App resolution.

## Run the existing lab

```bash
scripts/uiai-lab-live up
scripts/uiai-lab-live persist on
scripts/uiai-lab-push
```

These are existing lab operations, not Chromebook-install commands. The public demo is a `public_demo` trust class: operator/provider credentials must never persist in its public profile. Privileged authentication requires a separate authorized private context. See Doc 183 and `AGENTS.md`.

## Planning and releases

Use repository-local beads_rust through **`br` only**. Do not maintain duplicate execution backlogs in GitHub issues or Markdown. Specification acceptance IDs and candidate release metadata are contracts/evidence, not a second task tracker.

The operator and planning agent determine canonical decisions and sequencing. Proposed specifications must not be described as implemented merely because they are committed. Native release tagging requires the evidence gates in Doc 186; this documentation update does not publish a release or alter the live demo.

## License

TBD. Omarchy is MIT; Focusa primitives are source-available. Existing licensing and entitlement boundaries remain in force. See the product specification's open questions.
