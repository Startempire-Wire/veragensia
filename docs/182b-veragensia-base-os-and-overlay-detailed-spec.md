# 182b — Veragensia Base OS and Overlay Detailed Specification

**Status:** DRAFT; native v0.1 implementation proposal revised 2026-09-04.
**Authority:** Verious Smith III / Doc 185. **Companions:** 182, 183, 186, 187, 188, 190, 191, 192.
**Invariant:** base source remains upstream-owned; Veragensia behavior lives in its additive integration layer.
**History:** the 2026-08-26 draft remains in Git at `948e9080efa1f52662b159193523e9c12a3d05a3`. This revision distinguishes the existing webtop installer from the native installer that still has to be built and distinguishes the constrained native v0.1 proof from the canonical full Agent Computer profile.

## A. Base targets

### A.1 Existing streamable proving ground

The current live target is LinuxServer webtop using Ubuntu/KDE in Docker, with Chromium, the Workforce extension, streaming and the keeper/deployment lifecycle. Doc 183 owns the live operational contract. Do not change its deployment, trust class, mounts, profiles, or availability as a side effect of native Chromebook planning.

Existing container concepts remain: persistent `/config`, stable parent mount for extension output, repository-managed overlay, Chromium extension readiness and loopback CDP checks, and separate production access governance. The public demo's login-free posture never applies to a private laptop.

Architecturally, this proving ground is the first crude implementation of the Cloud Agent Computer Runtime shape described in Doc 191. It is **not** the canonical private/full Agent Computer software profile and does not gain new trust or credentials from that architectural role.

### A.2 Native product target

Stock Omarchy on supported x86_64 hardware supplies the Arch base, compositor, graphical session, and supported shell/configuration interfaces. The immediate native target is a single-owner developer preview, not an Omarchy-in-container experiment or custom distro installer.

Use the stock Omarchy ISO/install procedure after the hardware's valid UEFI path is established. Exact package versions, installed shell generation, and runtime capabilities must be recorded. A current manual is a source for integration design, not proof that the user's installation matches it.

### A.3 Chromebook modes

| Mode | Promise | Boundary |
|---|---|---|
| Native Omarchy | Full selected desktop/session integration on qualified hardware | Firmware/HWID and Linux-function checks required |
| ChromeOS Linux environment | Companion userland/apps where supported | Does not own ChromeOS's compositor, permissions or full desktop |
| Remote computer surface | Access to a provisioned Veragensia machine | Network-dependent; not local native installation |

The recovered first bring-up target is Dell Chromebook 11 CC11260 / expected ULDRENITE. Actual HWID, resources, firmware prerequisites and compatibility are validated by Doc 187. Do not assert native support from a CPU brand alone. Do not silently replace the requested native target with a remote webpage.

### A.4 Rapid upstream change: stable operations, replaceable integration

Operator direction (2026-09-08): adapt necessary docs/code as Omarchy evolves while
keeping Veragensia's essence and operations unchanged. This rule governs older
renderer/path assumptions; it does not replace their authority/security contracts.

- Keep mission/state/next-action semantics, explicit scope, Focusa ownership,
  privacy, stop/approval behavior and full-profile composition stable.
- Verify the installed or selected upstream revision and actual capabilities before
  changing an integration. Rumored or unreleased changes are not implementation facts.
- Adapt the smallest existing presenter/adapter boundary and update its docs and
  producer/consumer tests together. Ordinary in-scope adjustments need no repeated
  design permission. Never invent a plugin host, command, path or capability.
- Support verified requirements, not hypothetical versions. Add compatibility
  branches only for demonstrated supported-version differences with test coverage;
  do not create a general compatibility framework or parallel authority/store.
- Pin and qualify intentional upgrades; preserve user configuration and a rollback
  path. Do not track floating latest, auto-upgrade, auto-install or replace the base.
- Escalate changes to core operations, trust boundaries, new services/dependencies,
  installation or deployment scope. Unknown compatibility stays explicit rather
  than being silently treated as working.

Inspected upstream `f4378f0de5b44d331ee943746a97872b718a6c18` uses Waybar;
its complete source tree has no desktop Quickshell/plugin host. The QML file found
is an SDDM login theme, not an integration host. Use stock Waybar for the current
compact Work surface; a future renderer must earn support through actual evidence.
This is source evidence, not qualification of the still-unverified native hardware.

## B. Native v0.1 integration layer

### B.1 Responsibility boundaries

Focusa remains the existing operational daemon/core. Veragensia supplies a lightweight session adapter, native presentation, application composition and OS execution containment. UIAI Engine/Workforce remain first-party consumed browser/computer execution components. Pi + the Focusa Pi extension is the default/reference Focusa-aware harness integration for supported profiles. Focusa Desktop is the default governed full-desktop presenter for supported full profiles.

Do not vendor or reimplement those authorities merely to place them on the OS. Do not create a second canonical memory, approval, task, ontology, evidence or audit authority.

The **canonical full Agent Computer profile** deliberately lists:

```text
Focusa daemon/core
Focusa Desktop
Pi + Focusa Pi extension
UIAI Engine + Cockpit/browser surfaces
Veragensia session/shell integration
```

The native Chromebook v0.1 is a constrained proof profile. It MAY omit full-profile surfaces until their dependency/resource/integration gates are ready, but every omission must be explicit and must not redefine the canonical full profile.

Use one native session bridge, not separate services for ontology, memory, reflexes, notifications and audit by default. An existing daemon is reused only after identity, data-directory ownership and API compatibility are verified. A missing GUI connection must not start a duplicate daemon.

### B.2 Proposed component paths

The following are implementation targets, **not existing paths at the inspected baseline**:

```text
overlay/omarchy/install.sh
overlay/omarchy/uninstall.sh
overlay/omarchy/bin/veragens
overlay/omarchy/lib/veragens.py
overlay/omarchy/services/veragens-session.service
```

The first read-only slice uses existing Python 3 standard-library `scripts/veragens` and stock Waybar presentation. `status --json` reuses the validated scoped continuation envelope; `status --waybar` renders its mission, Workpoint state, next slice and checkpoint timestamp. `config/waybar-work.jsonc` is an inert explicit-scope example, not an installer. No resident bridge, extra shell, model call or new toolchain is required for this slice. Existing Focusa binaries remain external dependencies.

The preview `WorkPanel` is not a replacement Focusa Desktop implementation. It is a bounded native shell projection for the first proof. Full-profile Focusa Desktop integration follows the shared presenter/operation contracts.

### B.3 User-owned installed locations

| Concern | Location / rule |
|---|---|
| Versioned integration payload | `${XDG_DATA_HOME:-$HOME/.local/share}/veragensia/releases/<revision>/` |
| Private adapter configuration | `${XDG_CONFIG_HOME:-$HOME/.config}/veragensia/` |
| Install/rollback metadata | `${XDG_STATE_HOME:-$HOME/.local/state}/veragensia/` |
| Session IPC | `${XDG_RUNTIME_DIR}/veragensia/session.sock`; private ownership/modes required |
| Native presenter | Merge only the owned custom module into the verified user Waybar configuration; preserve existing module lists and user edits |
| CLI entry | User-owned `~/.local/bin/veragens`, only after conflict/ownership checks |
| Focusa canonical data | Existing supported Focusa data directory; never relocated/erased implicitly |

Discover the actual Waybar configuration path and respect supported XDG overrides; do not assume an Omarchy plugin directory or copy a complete replacement configuration. Record actual paths locally and redact them in shared evidence. The current CLI slice creates no socket or service; those rows describe the proposed fuller session bridge.

The native installer must not modify `/usr/share/omarchy`, replace whole user dotfiles, enable passwordless privilege, add public listeners, or change firmware/partitions. Third-party shell plugins are unsandboxed user code, not a place for secrets or authority enforcement.

## C. Installation transaction

### C.1 Separate the installers

`overlay/install.sh` currently runs inside the KDE/webtop environment. Preserve that behavior and do not retrofit untested host detection into the live deployment path.

The new `overlay/omarchy/install.sh` interface is specified as:

- `--check`: inspect dependencies/platform/config conflicts without writing or enrolling anything;
- `--apply`: explicit installation of validated, pinned integration files;
- `--rollback`: restore only the recorded Veragensia transaction, preserving unrelated user edits.

These are future interfaces. README and Doc 187 must continue to say they are unavailable until implemented and tested.

### C.2 Preflight

Check actual architecture, base generation, dependency presence, manifest completeness, artifact hashes, free space, private runtime ownership, existing daemon identity, and supported Focusa operations. A preflight failure explains the exact unmet condition. It never runs a firmware utility, package update, browser login, or duplicate daemon as a surprise repair.

Pin Omarchy/Hyprland and the selected presenter (currently Waybar), plus the Focusa/Workforce/agent artifacts, in the compatibility record. `platform.waybar_version` is required for this profile; legacy `quickshell_version` metadata is retained for compatibility, not required or proof of an installed host. Do not silently adopt a newer release because a mutable latest URL changed. Draft artifacts require a separately explicit experimental choice; the published inspected Focusa candidate is v0.9.191 (latest stable, verified 2026-09-09; standing direction: Veragensia always targets the most recent published stable Focusa release, pinned by digest in `config/v0.1-release-candidate.json` and gated by the doctor version-match check), not proof of hardware compatibility.

A full-profile installer/resolver will later need profile-specific checks for Focusa Desktop, Pi/plugin, UIAI Engine/Cockpit, Agent Apps and application capability descriptors. Those later checks must not be falsely reported as native v0.1 requirements before their implementation contracts exist.

### C.3 Apply and activation

Stage on the target filesystem; validate the selected presenter's configuration/entry points and each planned shared-config edit. Capture only the config fragments owned by the integration, with preimage hashes. Abort on conflicting edits or non-owned destinations.

Use verified configuration/menu interfaces and optional conflict-checked user bindings. Do not overwrite stock launcher bindings or invent `omarchy plugin` commands. The first slice has no click/launch binding; full-view opening must use a verified installed Focusa Desktop entry point.

If a later approved profile needs the proposed session service, install/enable it only after its inputs validate. Follow the actual graphical-session lifecycle; no default linger. Authenticate private Focusa access, verify the bridge/projection, then record committed install state. A successful copy is not successful activation.

### C.4 Idempotency and uninstall

Repeat apply must converge without duplicate plugins, services, daemons or menu entries. Existing user changes require a merge/conflict result, not blind overwrite. Uninstall removes only owned files/entries and leaves stock Omarchy functional. Preserve projects, Focusa canonical data, credential state and unrelated applications.

On failed activation restore the transaction's modified entries. Never restore an old Focusa database just because a shell plugin was rolled back. Test interrupted staging, invalid manifest, auth failure, daemon absence, activation failure, repeat install, and user-edited config before uninstall.

## D. Runtime and interaction

### D.1 Native surfaces

The v0.1 plugin provides an ambient status widget and compact Work panel. It projects real connection freshness, selected scope, Workpoint summary, one run, artifact review and stop/pause state. It does not hold credentials, call models on the render path, infer intent from focus, or maintain a separate authoritative ledger.

Use plain language, keyboard/pointer access, readable scaling, and reduced motion. Do not hide degraded or noncanonical evidence behind a green status indicator. Accessibility limitations must be explicit.

For the eventual full profile, Focusa Desktop is the default governed work/cognition presenter. The Omarchy plugin remains complementary ambient OS integration, not a duplicate Mission Canvas/Work Rail state authority.

### D.2 State and requests

Doc 188 defines the `veragens` CLI, private JSON Lines socket, bounded messages, restart epochs, stale-state handling, and operation mapping. Consume the selected release's Focusa descriptors with explicit project/continuity; preserve writer, authorization and entitlement requirements.

The current selected dependency's default daemon bind is loopback `127.0.0.1:8787`. Native installation still requires tested authentication/private access; loopback is not a proof of trust. Do not place tokens in CLI arguments, QML, logs or public receipts. OS containment must keep untrusted task code away from the human session and daemon data.

### D.3 Resource and lifecycle behavior

Use existing Focusa constrained/LowMem contracts. Permit one governed run in v0.1, bounded work queues and summaries, and no mandatory local model. Preserve foreground responsiveness under the measured reference workload.

Lock/idle/suspend changes become scoped observations. They do not broaden authority, silently enable unattended execution, or imply that suspended hardware continues working. Stop confirmation must come from the owning worker/runtime; a closed GUI or stopped loop is not sufficient evidence.

Cloud/full-profile lifecycle, workcells, Agent Apps, Agent Assist and mixed-topology elasticity are governed by Doc 191 rather than being approximated in the native v0.1 bridge.

### D.4 Browser integration

**UIAI Engine + Cockpit/browser surfaces are deliberately canonical first-party Agent Computer defaults.** Chromium and Workforce remain private browser surfaces bound to the same Focusa instance. Use the existing supported pairing path for the initial release; native messaging may follow.

No exposed CDP/LAN daemon, copied public profile, or copied live-server secrets. Exact browser/extension identity and restart durability are release gates.

Veragensia must reuse UIAI's existing Agent-First Browser exchange/verification/evidence contracts where applicable rather than introducing a competing browser-control model. Visual computer use remains the fallback when structured/semantic browser capabilities cannot perform the task.

### D.5 Agent harness integration

Pi + the Focusa Pi extension is the default/reference Focusa-aware harness integration for supported profiles. The harness remains a disciplined consumer/producer at the edge; Focusa daemon/core owns canonical scoped cognition and state.

Native Veragensia components MUST NOT store Pi-private copies of Workpoints, Trajectory, ontology, Evidence, grants, metacognition or recovery state. Compatible non-Pi harnesses use thin adapters over the same Focusa contracts.

### D.6 Application capability resolution

Doc 190 defines Agentability Classes, capability-first profiles, the Agent App Resolver and versioned Agent App descriptors.

The base/overlay layer is responsible for presenting installed/runtime capabilities to that resolver and launching the chosen application/runtime through appropriate OS containment. It does not itself decide canonical work authority.

## E. Acceptance and release state

Doc 186 gate IDs G00–G13 are the release criteria. `config/v0.1-release-candidate.json` records the published dependency candidate and unknown/missing hardware, compatibility, native artifacts and evidence. Null fields and `not_run` are blocking, not pass values.

The current update supplies specifications and an install runbook; it does not implement the native runtime or publish v0.1. A theme-only desktop, a remote webtop, or a fixture-backed panel must not be mislabeled a native agent-first release.

Likewise, native v0.1 success does not automatically prove the canonical full Agent Computer profile, Elastic Agent Computing, Agent Assist, Agent App resolution or telemetry plane. Those have separate later evidence gates.

Tasks/dependencies belong in repository-local `br`. This spec's interfaces and acceptance criteria are not another task tracker.

## F. Later work kept off the critical path

Signed Arch packages, custom images, wider hardware support, full Focusa Desktop profile integration, Pi/reference-harness packaging, UIAI/Cockpit full-profile packaging, capability-based Agent App resolution, Elastic Agent Computing, multi-agent concurrency, broader application affordances, Agent Assist, richer ontology/reflex surfacing, telemetry/improvement, and full native messaging can build on the tested native contract.

They do not justify skipping the first complete governed cycle or changing the live webtop contract.

The exact default productivity/development/knowledge/communications software catalog is intentionally deferred to the evidence-based Doc-190 software-selection work rather than being frozen into this base/overlay spec.

## Sources

- [Complete Omarchy source tree](https://api.github.com/repos/basecamp/omarchy/git/trees/f4378f0de5b44d331ee943746a97872b718a6c18?recursive=1), [base packages](https://github.com/basecamp/omarchy/blob/f4378f0de5b44d331ee943746a97872b718a6c18/install/omarchy-base.packages), and [session autostart](https://github.com/basecamp/omarchy/blob/f4378f0de5b44d331ee943746a97872b718a6c18/default/hypr/autostart.conf), inspected 2026-09-08. These replace the earlier unsupported shell-plugin baseline assumptions.
- [186 — release requirements](186-veragensia-v0.1-native-chromebook-release-spec.md).
- [187 — hardware and first installation](187-veragensia-chromebook-first-install-runbook.md).
- [188 — decisions and integration contracts](188-veragensia-v0.1-decisions-and-integration-contracts.md).
- [190 — agent-first software and capability resolution](190-veragensia-agent-first-software-and-capability-resolution-spec.md).
- [191 — Elastic Agent Computing and cloud runtime](191-veragensia-elastic-agent-computing-and-cloud-runtime-spec.md).
- [192 — telemetry and improvement plane](192-veragensia-telemetry-and-improvement-plane-spec.md).
