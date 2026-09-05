# 182b — Veragensia Base OS and Overlay Detailed Specification

**Status:** DRAFT; native v0.1 implementation proposal revised 2026-09-04.
**Authority:** Verious Smith III / Doc 185. **Companions:** 182, 183, 186, 187, 188.
**Invariant:** base source remains upstream-owned; Veragensia behavior lives in its additive integration layer.
**History:** the 2026-08-26 draft remains in Git at `948e9080efa1f52662b159193523e9c12a3d05a3`. This revision distinguishes the existing webtop installer from the native installer that still has to be built.

## A. Base targets

### A.1 Existing streamable proving ground

The current live target is LinuxServer webtop using Ubuntu/KDE in Docker, with Chromium, the Workforce extension, streaming and the keeper/deployment lifecycle. Doc 183 owns the live operational contract. Do not change its deployment, trust class, mounts, profiles, or availability as a side effect of native Chromebook planning.

Existing container concepts remain: persistent `/config`, stable parent mount for extension output, repository-managed overlay, Chromium extension readiness and loopback CDP checks, and separate production access governance. The public demo's login-free posture never applies to a private laptop.

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

## B. Native v0.1 integration layer

### B.1 Responsibility boundaries

Focusa remains the existing operational daemon. Veragensia supplies a lightweight session adapter, native presentation, and OS execution containment. UIAI/Workforce remain consumed components. Do not vendor those implementations or create a second canonical memory, approval, task or audit authority.

Use one native session bridge, not separate services for ontology, memory, reflexes, notifications and audit by default. An existing daemon is reused only after identity, data-directory ownership and API compatibility are verified. A missing GUI connection must not start a duplicate daemon.

### B.2 Proposed component paths

The following are implementation targets, **not existing paths at the inspected baseline**:

```text
overlay/omarchy/install.sh
overlay/omarchy/uninstall.sh
overlay/omarchy/bin/veragens
overlay/omarchy/lib/veragens.py
overlay/omarchy/services/veragens-session.service
overlay/omarchy/plugins/veragensia.work/manifest.json
overlay/omarchy/plugins/veragensia.work/Status.qml
overlay/omarchy/plugins/veragensia.work/WorkPanel.qml
```

The native preview uses Python 3 standard-library adapter code and QML presentation as the selected engineering default. Existing Focusa binaries are pinned external artifacts. No resident model, new on-device Rust toolchain, or browser compilation is an installation prerequisite.

### B.3 User-owned installed locations

| Concern | Location / rule |
|---|---|
| Versioned integration payload | `${XDG_DATA_HOME:-$HOME/.local/share}/veragensia/releases/<revision>/` |
| Private adapter configuration | `${XDG_CONFIG_HOME:-$HOME/.config}/veragensia/` |
| Install/rollback metadata | `${XDG_STATE_HOME:-$HOME/.local/state}/veragensia/` |
| Session IPC | `${XDG_RUNTIME_DIR}/veragensia/session.sock`; private ownership/modes required |
| Native plugin | `~/.config/omarchy/plugins/veragensia.work/`; validated real files, not unsafe internal symlinks |
| CLI entry | User-owned `~/.local/bin/veragens`, only after conflict/ownership checks |
| Focusa canonical data | Existing supported Focusa data directory; never relocated/erased implicitly |

Respect existing custom XDG configuration where the actual upstream consumer supports it; do not assume a relocated plugin path works when Omarchy's selected version expects `~/.config/omarchy`. Record actual paths locally and redact them in shared evidence.

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

Pin Omarchy/Hyprland/Quickshell and the Focusa/Workforce/agent artifacts in the compatibility record. Do not silently adopt a newer release because a mutable latest URL changed. Draft artifacts require a separately explicit experimental choice; the published inspected Focusa candidate is v0.9.184, not proof of hardware compatibility.

### C.3 Apply and activation

Stage on the target filesystem; validate plugin schema/entry points and each planned shared-config edit. Capture only the config fragments owned by the integration, with preimage hashes. Abort on conflicting edits or non-owned destinations.

Use supported plugin/config/Omarchy menu interfaces and an optional conflict-checked user keybinding. Do not overwrite stock launcher bindings. Adding the whole repository through `omarchy plugin add` is not valid unless a plugin-root manifest actually exists; install the validated plugin subtree instead.

Install/enable the session service only after its inputs validate. Follow the actual graphical-session lifecycle; no default linger. Authenticate private Focusa access, verify the bridge/projection, then record committed install state. A successful copy is not successful activation.

### C.4 Idempotency and uninstall

Repeat apply must converge without duplicate plugins, services, daemons or menu entries. Existing user changes require a merge/conflict result, not blind overwrite. Uninstall removes only owned files/entries and leaves stock Omarchy functional. Preserve projects, Focusa canonical data, credential state and unrelated applications.

On failed activation restore the transaction's modified entries. Never restore an old Focusa database just because a shell plugin was rolled back. Test interrupted staging, invalid manifest, auth failure, daemon absence, activation failure, repeat install, and user-edited config before uninstall.

## D. Runtime and interaction

### D.1 Native surfaces

The v0.1 plugin provides an ambient status widget and compact Work panel. It projects real connection freshness, selected scope, Workpoint summary, one run, artifact review and stop/pause state. It does not hold credentials, call models on the render path, infer intent from focus, or maintain a separate authoritative ledger.

Use plain language, keyboard/pointer access, readable scaling, and reduced motion. Do not hide degraded or noncanonical evidence behind a green status indicator. Accessibility limitations must be explicit.

### D.2 State and requests

Doc 188 defines the `veragens` CLI, private JSON Lines socket, bounded messages, restart epochs, stale-state handling, and operation mapping. Consume the selected release's Focusa descriptors with explicit project/continuity; preserve writer, authorization and entitlement requirements.

The current selected dependency's default daemon bind is loopback `127.0.0.1:8787`. Native installation still requires tested authentication/private access; loopback is not a proof of trust. Do not place tokens in CLI arguments, QML, logs or public receipts. OS containment must keep untrusted task code away from the human session and daemon data.

### D.3 Resource and lifecycle behavior

Use existing Focusa constrained/LowMem contracts. Permit one governed run in v0.1, bounded work queues and summaries, and no mandatory local model. Preserve foreground responsiveness under the measured reference workload.

Lock/idle/suspend changes become scoped observations. They do not broaden authority, silently enable unattended execution, or imply that suspended hardware continues working. Stop confirmation must come from the owning worker/runtime; a closed GUI or stopped loop is not sufficient evidence.

### D.4 Browser integration

Chromium and Workforce remain first-class private surfaces bound to the same Focusa instance. Use the existing supported pairing path for the initial release; native messaging may follow. No exposed CDP/LAN daemon, copied public profile, or copied live-server secrets. Exact browser/extension identity and restart durability are release gates.

## E. Acceptance and release state

Doc 186 gate IDs G00–G13 are the release criteria. `config/v0.1-release-candidate.json` records the published dependency candidate and unknown/missing hardware, compatibility, native artifacts and evidence. Null fields and `not_run` are blocking, not pass values.

The current update supplies specifications and an install runbook; it does not implement the native runtime or publish v0.1. A theme-only desktop, a remote webtop, or a fixture-backed panel must not be mislabeled a native agent-first release.

Tasks/dependencies belong in repository-local `br`. This spec's interfaces and acceptance criteria are not another task tracker.

## F. Later work kept off the critical path

Signed Arch packages, custom images, wider hardware support, optional Fly/Sprites execution, multi-agent concurrency, broader application affordances, richer ontology/reflex surfacing, and full native messaging can build on the tested native contract. They do not justify skipping the first complete governed cycle or changing the live webtop contract.

## Sources

- [Omarchy plugin interfaces](https://omarchy.org/manual/shell-plugins/) and [supported configuration/hooks](https://omarchy.org/manual/dotfiles/), inspected 2026-09-04.
- [186 — release requirements](186-veragensia-v0.1-native-chromebook-release-spec.md).
- [187 — hardware and first installation](187-veragensia-chromebook-first-install-runbook.md).
- [188 — decisions and integration contracts](188-veragensia-v0.1-decisions-and-integration-contracts.md).
