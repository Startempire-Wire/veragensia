# 186 — Veragensia v0.1 Native Chromebook Release Specification

**Status:** proposed implementation contract; NOT an implementation-complete or released product.
**Prepared:** 2026-09-04.
**Architecture authority:** Verious Smith III, subject to Doc 185. The operator requested implementable specifications and repository updates for an Omarchy-based Chromebook v0.1. Engineering selections below are explicit proposals within that request; publication is not automatic canonical promotion.
**Baseline inspected:** Veragensia `948e9080efa1f52662b159193523e9c12a3d05a3`.
**Companions:** [182](182-veragensia-focusa-agent-os-spec.md), [182b](182b-veragensia-base-os-and-overlay-detailed-spec.md), [187](187-veragensia-chromebook-first-install-runbook.md), [188](188-veragensia-v0.1-decisions-and-integration-contracts.md).

## 1. Release meaning and present implementation gap

v0.1 is a **single-owner, native Omarchy developer preview** demonstrating one complete governed work cycle. It is not the public webtop, a wallpaper package, a custom ISO, a hostile multi-user sandbox, or the full long-term cognitive OS.

At the inspected baseline, `overlay/install.sh` is a KDE/webtop branding script using `/config`, `abc`, and Plasma. There is no native Omarchy installer, session bridge, or native Veragensia shell plugin in that baseline. New paths and `veragens` commands specified here are **to be implemented**, not commands already available after cloning this repository.

A release requires three independently reported results: `base_ready`, `integration_ready`, and `agent_cycle_ready`. Installing Omarchy or downloading Focusa binaries does not make the other two true. The candidate manifest in `config/v0.1-release-candidate.json` intentionally records missing evidence and must remain blocked until those gaps are actually closed.

## 2. Exact initial target

The recovered Chromebook planning thread identified **Dell Chromebook 11 CC11260**, with expected board **ULDRENITE**. This is the working bring-up target, not a substitute for reading the arriving machine's HWID. The 2-in-1 uses a separately listed `ULDRENITE360`; never flash a board selected solely by its product label. RAM, storage, debug-cable availability, and the actual unit's Linux behavior were not recovered as confirmed facts.

Native path: owner-controlled ChromeOS device → exact-board firmware preparation → supported UEFI boot → stock Omarchy → Veragensia integration. Doc 187 owns the destructive-operation and hardware gates. ChromeOS Linux-container and remote-preview paths remain separate modes and must never be labeled native Omarchy.

## 3. User-visible acceptance journey

The reference journey uses a small, synthetic project folder; private files are not required for acceptance.

1. Log into stock Omarchy. A native Veragensia status widget reports the actual daemon connection state. Selecting it opens a compact Work panel.
2. Choose an explicit project root and bind the existing Focusa project/continuity, or use Focusa's authorized creation flow when no project exists. A directory selection alone does not fabricate project identity.
3. Resume the canonical Workpoint. The panel shows the goal, verified result references, blockers, and next action; it preserves `canonical=false` and degraded warnings.
4. Request one bounded agent task against an approved copy/working directory. Show principal, input scope, output location, provider/data-transfer scope, time/turn limits, and cancellation control before launch.
5. Continue ordinary editing while the agent works. The agent does not take the human's pointer or switch their workspace.
6. Inspect the output artifact and verification result. Nothing automatically overwrites the original project or publishes externally.
7. Stop the run, restart the shell, and reopen the project. Workpoint continuity survives; a stopped or failed run is not relabeled successful.

A deterministic fixture may prove transport and UI behavior, but **does not satisfy the real-agent acceptance gate**. At least one actual configured agent must complete the journey with outcome evidence. Unknown license or provider entitlement must not be bypassed to pass it.

## 4. Required scope versus explicit exclusions

| ID | Required v0.1 behavior | Negative boundary |
|---|---|---|
| V01-01 | Native install/uninstall and compatibility doctor | No upstream Omarchy edits or whole-dotfile replacement |
| V01-02 | Reuse one healthy Focusa daemon or install one under an explicit lifecycle contract | No daemon per window, agent, or shell widget |
| V01-03 | Native status widget plus Work panel | No second desktop shell or fake activity animation |
| V01-04 | Explicit project binding and Workpoint continuation | No parallel Veragensia memory/task database |
| V01-05 | One governed local agent run with bounded resources | No unrestricted shell launcher presented as governed execution |
| V01-06 | Artifact preview, verification, and explicit disposition | No automatic publication, spending, package installation, or original-file replacement |
| V01-07 | Stop, pause, failure, stale-state, and reconnect behavior | Stopping a work loop is not proof every child process stopped |
| V01-08 | One private Chromium/Workforce surface connected to the same Focusa instance | No public-demo profile or exposed CDP on the laptop |
| V01-09 | Opt-in workspace observation and resource/lock-state handling | No clipboard, keystroke, microphone, camera, screen-content, or home-directory surveillance |
| V01-10 | Repeat-install, rollback, and exact-device evidence | No release tag merely because static tests pass |

Deferred: Fly/Sprites backend; custom ISO; distributed task migration; local model requirement; automatic model/provider switching; autonomous package repair; agent-generated ontology/reflex installation; global desktop-control agents; replacing authentication/lock/polkit; always-on screenshot analysis; native messaging migration; broad communications connectors. Existing explicit communications priorities remain governed by AGENTS.md and their own contracts, not silently bundled into this native preview.

## 5. Process and ownership topology

Omarchy owns the graphical session, compositor, system controls, and shell host. Focusa owns its existing operational state and authorization. Veragensia owns adapters and presentation.

The always-on application services are the existing Focusa daemon and **one lightweight session bridge**. The QML plugin lives in Omarchy's shell process; cognition and execution workers are started only when needed. CLI/watch clients are bounded subprocesses, not additional authorities. Do not create one daemon per primitive.

Selected implementation default: Python 3 standard-library session adapter/CLI for v0.1, QML for the Omarchy plugin, shell for installation. This avoids a new on-device compiler/toolchain requirement. These choices do not fix the long-term implementation language; the versioned adapter contract must permit replacement.

Proposed repository layout (not present at the baseline):

```text
overlay/omarchy/install.sh
overlay/omarchy/uninstall.sh
overlay/omarchy/bin/veragens
overlay/omarchy/lib/veragens.py
overlay/omarchy/services/veragens-session.service
overlay/omarchy/plugins/veragensia.work/manifest.json
overlay/omarchy/plugins/veragensia.work/Status.qml
overlay/omarchy/plugins/veragensia.work/WorkPanel.qml
overlay/omarchy/fixtures/
tests/native/
```

Focusa binaries, Workforce build output, and UIAI artifacts are consumed at pinned revisions, not copied into this repository as another implementation. Build any unavailable artifacts on the established build infrastructure, not by imposing a full Rust/browser build on the Chromebook.

## 6. Supported integration seams

Use `~/.config/omarchy/plugins/veragensia.work/` and the supported shell configuration interface. Validate the staged plugin using `omarchy plugin validate`; preserve existing bar entries and other plugins. The repository is not itself a plugin-root repository: **do not run `omarchy plugin add` against this repository and assume a root manifest exists**.

Use an additive user menu entry and an optional conflict-checked binding. Do not take over Omarchy's default launcher keys. On plugin-generation Omarchy, use supported user Lua overrides; on an unsupported generation, report `unsupported_platform` rather than rewriting legacy configs opportunistically. Compatibility requires an exact recorded Omarchy/Hyprland/Quickshell version set, not merely the word “latest.”

The bridge may consume Hyprland events after per-session opt-in. Default payload contains workspace identity and allowlisted application class, not full window titles or document contents. Workspace association is user-confirmed metadata; it cannot change Focusa project authority on its own. Reconnect or compositor restart causes resynchronization, not replayed agent launches.

## 7. State, IPC, and API contracts

Doc 188 specifies the wire envelope and CLI. The bridge's socket is `${XDG_RUNTIME_DIR}/veragensia/session.sock`, in a mode-0700 directory with a mode-0600 socket. Refuse unsafe ownership, stale foreign sockets, unsupported schema versions, and unbounded input. Check Unix peer UID; same-UID access is **not** a hostile-code security boundary.

Keep only a bounded projection cache and local installer metadata outside Focusa. Private configuration is `${XDG_CONFIG_HOME:-$HOME/.config}/veragensia/`; installer state is `${XDG_STATE_HOME:-$HOME/.local/state}/veragensia/`. No credentials in command arguments, QML, status frames, or receipts.

Use Focusa's generated operation descriptors for the selected release. The inspected published dependency candidate is `v0.9.184`; newer development documentation is not proof that its binaries expose an operation. Confirm API schemas and authorization against the running binary before enabling mutation.

Verified descriptor anchors at that tag include:

| Need | Existing Focusa contract | Mapping constraint |
|---|---|---|
| Continue work | `focusa_workpoint_resume`; `POST /v1/workpoint/resume` | Explicit `project_root` and `continuity_id`; use `operator_summary` for the panel |
| Resource posture | `focusa_resource_mode`; `GET/POST /v1/resource/mode` | Reads and mutations remain distinct; no model needed to read posture |
| Loop control | `focusa_work_loop_control`; `/v1/work-loop/enable`, `/pause`, `/resume`, `/stop` | Preserve writer authority and preflight; do not infer child-process cancellation |
| Project, Workset, checkpoint, evidence, approvals, agent launch | Selected release's generated capability/operation registry | Resolve exact operation ID, strict schema, transport, and auth in the compatibility record; absent contract blocks that feature |

Do not create guessed REST routes, relay operator credentials to an agent, or mutate Focusa SQLite/event files directly. Prefer the existing verified event stream; if its resumability is unavailable, explicitly use bounded snapshot refresh. v0.1 may use a documented 5-second health/status fallback rather than pretend polling is entirely eliminated.

## 8. Agent execution boundary

One active governed run per native preview session. Reuse Focusa's existing session/work-loop/runner ownership rather than create a second scheduler. The Veragensia adapter adds OS containment and a projection of that state.

Every run requires: existing principal reference; project and continuity scope; authorized operation; input revision; approved working directory; output directory; finite time/turn/retry budgets; provider policy; cancellation handle; and evidence destination. Treat retrieved text, filenames, document content, and model output as data, never new operating instructions or grants.

Untrusted task code must execute outside the human session's filesystem/credential authority. The implementation must prove an enforced sandbox or separately isolated worker with only the approved inputs and output directory, no human HOME/session sockets, no Focusa database, and denied-by-default network. A systemd scope or environment variable alone is not a sandbox. Provider access, when enabled, goes through the existing approved credential/tool boundary; a missing enforceable broker is a blocker, not permission to inject a broad API key.

The launch surface must truthfully distinguish `governed`, `operator_managed`, and `unavailable`. Direct upstream agent launchers are not magically intercepted. Do not claim whole-machine agent governance in v0.1.

Pause prevents further dispatch at a safe boundary; it is not a freeze of arbitrary side effects. Stop first blocks further dispatch, requests runner cancellation, then terminates only owned local process groups/units when necessary. Report `stopped` only after the owned worker's termination is observed. Unknown or disconnected execution remains `stop_pending`/`unknown` and is never success.

## 9. Output settlement and recovery

Outputs start in the run's staging directory. Validate paths, symlinks, byte limits, and expected artifact type before preview. Bind the result to the input revision and run ID. A source that changed during execution produces a conflict, not an overwrite.

The first preview task may produce a Markdown report or a patch against a copy. Applying a patch, replacing an original, or publishing remains a separate explicitly authorized action. A model claiming success is not outcome evidence; exit code alone is also insufficient when the task requires a file/test result.

Shell/bridge restart must recover the existing Focusa scope and reconcile run state. Never restart a mutating request solely because its response was lost. Use existing idempotency semantics where supported; otherwise report an uncertain outcome and reconcile before retry.

## 10. Low-resource behavior

Use Focusa's existing normal/constrained/LowMem/emergency contract. Do not fork it. No mandatory resident local model, browser fleet, microVM, or continuous deep graph scan.

Initial engineering acceptance budgets, **not measurements or a hardware guarantee**:

- bridge steady-state RSS at most 128 MiB; bounded queue at most 256 observations;
- one rendered status frame at most 64 KiB; a local request at most 16 KiB;
- GUI acknowledgment of a local click/stop request p95 at most 100 ms under the reference workload, independently of task completion;
- detect loss of daemon connectivity within 10 seconds; show stale/unknown state immediately on a detected disconnect;
- at most one active agent; expensive background work deferred under pressure;
- no automatic retry loop beyond the run's finite budget.

Measure total desktop, Focusa, browser, bridge, and worker memory separately on the actual unit. Do not advertise 4-GB support from these component budgets. Do not apply a hard daemon memory cap that kills canonical persistence merely to achieve a number. Protect foreground input with tested process/cgroup controls and degrade nonessential work first.

Idle/locked/asleep are different states. Screen lock never grants authority. Suspend stops local execution; remote continuation is out of scope. Do not enable systemd lingering or unattended work by default.

## 11. Installer and rollback contract

The future native installer is separate from the live webtop installer. It must support `--check` (read-only), `--apply` (explicit operator action), and `--rollback` with documented exit codes. These flags are a specified interface, not existing functionality.

Before writes: validate the release manifest, exact dependency versions and digests, platform support, free space, existing Focusa ownership, and configuration conflicts. Stage on the target filesystem. A nonempty unsupported configuration must cause a bounded error, not destructive “repair.”

Install only Veragensia-owned files and additive supported config entries; use a transaction manifest containing original hashes and owned paths. Preserve local edits. Activate services only after validation. A failed activation restores this transaction's changes, not the entire user configuration. Uninstall removes owned integration, preserves Focusa state/projects/credentials, and leaves stock Omarchy usable. Database migration/rollback is Focusa's contract, not a filesystem-copy shortcut.

v0.1 may be installed from a pinned checkout with an idempotent native installer. Signed Arch package distribution is subsequent packaging work, not a prerequisite that delays proving the native cycle. No floating curl-to-shell installer.

## 12. Required evidence gates

These are specification acceptance IDs, not a second task backlog. Implementation status belongs in repository-local `br`.

| Gate | Evidence required |
|---|---|
| G00 authority | Exact owner-approved scope; no implied new architecture authority |
| G01 hardware | Actual board, RAM/storage class, firmware version, working input/display/network/audio/power; redact serials and identifiers |
| G02 base | Stock Omarchy boot and session, recorded versions, tested suspend/resume and recovery path |
| G03 dependencies | Published pinned binary/build artifacts, digests, descriptor compatibility, legitimate entitlement |
| G04 install | Clean install, repeat apply, config-conflict rejection, upstream files unchanged |
| G05 projection | Widget/panel consume real Focusa state; missing/degraded/invalid schema never appears healthy |
| G06 continuity | Project/continuity survives shell, bridge, and daemon restart without duplicates or scope leakage |
| G07 isolation | Worker cannot read human HOME, session sockets, daemon state, or unrelated credentials; denied network tested |
| G08 agent | One actual authorized agent task, expected artifact, verification evidence, and no out-of-scope writes |
| G09 stop | Local stop, child-process termination, lost response, and failed cancellation are tested distinctly |
| G10 resilience | Event loss, duplicate events, stale result, malformed payload, memory pressure, disk-full, and network loss |
| G11 experience | Pointer/keyboard use, readable layout on the actual display, reduced motion, meaningful status; foreground latency measured |
| G12 rollback | Failed activation and uninstall restore a usable stock session while retaining user/cognitive data |
| G13 browser | Private Chromium/Workforce installation, same daemon identity, scoped pairing, no public/laptop credential crossover |

No unexecuted gate may be marked passed. Accessibility limitations must be listed; passing keyboard tests is not proof of screen-reader compatibility. A release candidate with a missing gate is a preview/build candidate, not v0.1 release-ready.

## 13. Implementation dependency order

Build the compatibility/installer transaction first, then the read-only bridge/plugin, then project continuation, then the isolated single-run path, then artifact settlement and cancellation, then device acceptance/rollback. Browser integration can use the existing private supported Workforce pairing path; native messaging is not required to prove this release.

Capture implementation work in `br` only, keyed to these gate IDs. Do not close implementation work from a documentation commit. Do not create a new release tag or deployment as a side effect of updating this spec.

## 14. Source anchors

- [Current Omarchy shell-plugin contract](https://omarchy.org/manual/shell-plugins/) and [user configuration/hooks](https://omarchy.org/manual/dotfiles/), inspected 2026-09-04. Runtime versions must still be pinned and tested.
- [Focusa v0.9.184 published release](https://github.com/Startempire-Wire/focusa/releases/tag/v0.9.184).
- [Workpoint resume descriptor](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_workpoint_resume.md), [resource-mode descriptor](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_resource_mode.md), [work-loop control descriptor](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_work_loop_control.md).
- Focusa documents 66 (Affordance and Execution-Environment Ontology) and 82 (Memory Optimization) supply reused concepts, not independently reimplemented Veragensia authorities.
