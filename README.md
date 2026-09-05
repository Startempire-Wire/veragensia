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
UIAI Engine / Workforce browser surface / bounded execution adapters
                    |
Stock Omarchy + Arch + Hyprland, consumed without a deep fork
```

The diagram is a responsibility map, not a second kernel or a claim that every proposed native component already exists.

- **Base:** upstream Omarchy, consumed through supported integration points. The current public proving ground is separately based on Ubuntu/KDE webtop.
- **Focusa primitives:** re-homed, not rebuilt: project/continuity, Worksets/Workpoints, sessions, authorization, approvals, credentials, pairing, work loop, roles, surfaces, events, and audit.
- **Native presentation:** plugin-generation Omarchy is the proposed target; validate exact versions instead of assuming compatibility or installing a second shell.
- **Browser:** Chromium plus Focusa Workforce remains a first-class product surface; UIAI Engine supplies governed browser capabilities.

An **Agent Cloud Computer** is a provisioned, streamable Veragensia instance. Remote execution providers are optional adapters, not dependencies for ordinary local desktop use.

## Architecture principles

**Surfaces are interchangeable; primitives are the platform.**

**Cloud coordinates. Node decides. Receipts prove. Private state stays local.**

**Observe within scope; act under authority; preserve useful work.**

[Doc 185](docs/185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md) identifies **Verious Smith III as the sole current and final canonical human architecture authority**. Focusa operational authority, repository presence, and external proposals do not confer architecture ownership. Future Wirebot authority requires explicit verified delegation; a name or hash alone does not grant it.

## Repository

- `overlay/` — current webtop branding and the home of future native integrations.
- `scripts/` — lab lifecycle, atomic deployment, browser launcher, narrow remote control, and evidence tooling.
- `ops/sudoers/` — least-privilege deployment templates for the live lab.
- `docs/182*` — product, base/overlay, and fleet specifications.
- `docs/183-*` — live public-computer security and lifecycle contract.
- `docs/185-*` — architecture authority and provenance policy.
- `docs/186-*`, `187-*`, `188-*` — proposed native v0.1 implementation and bring-up contracts.

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
