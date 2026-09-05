# 188 — v0.1 Engineering Decisions and Integration Contracts

**Status:** proposed, implementation-specific decisions under the operator's request for a native Chromebook v0.1; not a grant of canonical architecture authority.
**Prepared:** 2026-09-04. **Root authority:** Verious Smith III / [185](185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md).
**Release requirements:** [186](186-veragensia-v0.1-native-chromebook-release-spec.md). **Installation:** [187](187-veragensia-chromebook-first-install-runbook.md).

## 1. Decision provenance

The operator explicitly selected an agent-first, deeply integrated Veragensia direction, requested real specifications and repository updates, and identified native Omarchy on the arriving Chromebook as the immediate target. The following engineering defaults translate that direction; they must not be presented as previously approved exact architecture decisions.

```yaml
scope: Veragensia v0.1 native single-owner developer preview
status: proposed
canonical_authority: Verious Smith III
authority_delegation_ref: null
constitution_ref: docs/185-veragensia-architecture-authority-provenance-and-wirebot-identity-policy.md
source: operator request for implementable specs and connected-repository updates
runtime_authority_changes: none
wirebot_delegation_created: false
```

No new owner key, principal hash, signed delegation, or constitutional digest is fabricated by this documentation change. Runtime users are represented by their enrolled principal, not hardcoded personal names. Customer/contributor provenance remains advisory.

## 2. Selected engineering defaults

| ID | Selection for implementation | Consequence / rejected alternative |
|---|---|---|
| D01 | Stock supported Omarchy plus additive native integration | No deep fork, custom ISO, or replacement DE for v0.1 |
| D02 | Existing Focusa daemon and existing project/continuity/Workpoint model | No parallel “OS brain,” task database, or new canonical world-state service |
| D03 | One session bridge; QML plugin inside Omarchy shell | No standalone Veragensia shell beside Omarchy; no service per cognitive primitive |
| D04 | Python 3 stdlib bridge/CLI for the preview; QML rendering | Minimize build/dependency setup; language can change behind the contract |
| D05 | Explicit user-selected project binding; workspace context advisory | Window focus or folder selection does not assert user intent or ownership |
| D06 | One isolated local governed run and a reviewable artifact | No broad computer-control agent or unrestricted same-user shell as the first proof |
| D07 | Pin and verify existing Focusa/Workforce artifacts | No floating latest download, on-device full build, or license bypass |
| D08 | Local continuity and read-only status work without a model | Provider work is explicit, bounded, and optional for ordinary desktop use |
| D09 | Installer from a pinned checkout before package distribution | Avoid making signed repository/ISO infrastructure a critical-path dependency |
| D10 | Fly/Sprites is a later execution adapter | No Fly account, billing, or remote availability required to boot/use v0.1 |
| D11 | Workcell is a bounded execution-context specialization | Reuse Focusa affordance, permission, resource, reliability, and reversibility concepts |
| D12 | Observation is opt-in and minimised; consequences governed | No ambient private-content capture merely because an API can read it |

These selections are concrete implementation inputs, not an alternative-choice menu or a second task tracker. Work items and dependencies remain in `br`.

## 3. Contracts between owners

- **Omarchy/Linux → bridge:** session/compositor/power observations. The producer owns the physical observation; the bridge does not infer an authorized task from it.
- **Bridge → Focusa:** validated operation request with explicit scope, using Focusa's existing authentication and generated schema. The bridge does not issue its own grants.
- **Focusa → bridge:** operational result/projection with revision, evidence, warnings, and canonical/degraded posture preserved.
- **Bridge → shell:** bounded presentation data, never provider secrets or a raw arbitrary-command surface.
- **Focusa runner + OS containment → execution:** one approved run with enforced boundaries and a cancellation handle. Resource control is not a substitute for filesystem/network isolation.
- **Worker → Focusa:** proposed artifacts/outcomes and evidence. A worker cannot self-approve, expand its input scope, or settle its own unsupported claim as fact.

Focusa's current operational authority is not organizational architecture authority. Linux root is not an architectural signature. Omarchy shell plugins run with user-account access; do not use an unsandboxed plugin or peer UID alone as the security boundary against same-user hostile code.

## 4. Proposed public CLI

The product's existing short form is **Veragens**; use `veragens`, not a second competing `veragensctl` name. This interface is **specified, not yet implemented at the planning baseline**.

| Command | Meaning | Side-effect rule |
|---|---|---|
| `veragens doctor --json` | Platform, dependency, auth, compatibility, and release-gate report | No install, enrollment, network-exposure, or repair side effects |
| `veragens status --json` | One bounded current projection | Read-only; explicit unavailable/stale states |
| `veragens status --watch` | JSON Lines projection stream | Bounded subscriber; no model calls |
| `veragens open` | Summon the native Work panel | No change of project, grant, or agent state |
| `veragens resume --project-root PATH --continuity-id ID` | Read the scoped Focusa continuation | Does not resume execution automatically |
| `veragens run --request FILE` | Submit a strict, previewable, bounded run request | Requires existing Focusa authority and a compatible runner |
| `veragens pause RUN_ID` | Prevent further dispatch at the supported safe boundary | Does not claim arbitrary processes are frozen |
| `veragens stop RUN_ID` | Request cancellation of this owned run | Confirm worker exit or return stop_pending/unknown |

Do not accept arbitrary shell command strings as a convenient implementation of `run`. `FILE` is data validated against the selected run schema. A CLI consumer must not build commands by concatenating project names, filenames, model output, or agent-supplied arguments.

Exit codes: `0` fulfilled; `2` invalid input/schema; `3` unavailable/degraded dependency; `4` unsupported platform/version; `5` authority or entitlement denied; `6` timeout/uncertain outcome; `7` release evidence incomplete. A watch stream reports changing health in frames; it does not terminate merely because one sample is degraded.

## 5. Local wire contract v1

Transport: newline-delimited UTF-8 JSON over the private Unix socket. Maximum request line 16 KiB, maximum response frame 64 KiB, maximum 4 simultaneous subscribers. Reject malformed UTF-8, unknown top-level properties, invalid enums, traversal in local file parameters, over-limit messages, and unexpected schema majors. No generic proxy-to-any-Focusa-route method.

Requests carry `schema`, `request_id`, `operation`, and a strict operation-specific `params`. Peer context is obtained from the local transport, not trusted from a claimed UID inside JSON. Mutation requests require the existing Focusa authorization and current scope in addition to transport identity.

Example read request:

```json
{
  "schema": "veragensia.request.v1",
  "request_id": "example-read-001",
  "operation": "status.read",
  "params": {}
}
```

Projection response (illustrative values, not test evidence):

```json
{
  "schema": "veragensia.session.v1",
  "bridge_epoch": "example-epoch",
  "sequence": 1,
  "health": "unavailable",
  "freshness": "unknown",
  "source_revision": null,
  "scope": null,
  "workpoint": null,
  "run": null,
  "resource_mode": "unknown",
  "errors": [{"code": "daemon_unavailable", "retryable": true}]
}
```

`health`: `ready | degraded | unavailable | incompatible`.
`freshness`: `fresh | stale | unknown`.
`resource_mode`: map the selected Focusa descriptor's actual enum; `unknown` is a presentation fallback, never an invented Focusa mode.
`scope`, when present: explicit `project_root`, `continuity_id`, and existing principal/workset references as available. Filesystem paths remain private local data and are redacted from shared receipts.
`workpoint`, when present: Workpoint ID, canonical/degraded flags, summary, warnings, and bounded evidence references from Focusa. A summary must not strip negative scope/authority warnings.
`run`, when present: run ID, principal ref, runner ref, execution state, bounded progress summary, output refs, and cancellation state. No credentials, full prompt, or raw transcript.

Sequence numbers are monotonic only within `bridge_epoch`. On bridge restart, change epoch; consumers discard old assumptions and request a fresh snapshot. On event gap/disconnect, mark stale and resnapshot. A fresh cache receipt does not make its underlying old source fresh. Default stale threshold is 10 seconds without a successful health/projection refresh; use monotonic timing locally. On reconnect, never replay a mutation just to reconstruct UI state.

## 6. Binding to existing Focusa operations

The selected published candidate has these documented mappings:

```text
focusa_workpoint_resume
  REST POST /v1/workpoint/resume
  fields: project_root, continuity_id, mode=operator_summary
  optional workpoint_id/session_id/current_ask per descriptor

focusa_resource_mode
  REST GET /v1/resource/mode for read
  REST POST /v1/resource/mode for governed control

focusa_work_loop_control
  REST POST /v1/work-loop/enable|pause|resume|stop
  exact body and writer/preflight semantics from the descriptor
```

The bridge must not assume a Pi-session default in an OS process. Explicit scope is mandatory for project-bound calls. Resolve exact project-binding, Workset, evidence, approvals, and runner operations from the selected release's generated registry and persist their descriptor hashes in the compatibility evidence. A route name in current `main` documentation is not proof of a compatible published binary.

Work-loop control is documented as non-idempotent. Do not automatically retry it after an ambiguous network response. Inspect actual state and correlate the original request first. Do not use a global loop-stop route to terminate an unrelated session. Endpoint scope and actual worker cancellation must be integration-tested before exposing `veragens stop` as working.

No existing contract means `unsupported_capability`, not a silently invented endpoint or direct state-file mutation.

## 7. Run request and lifecycle

A run request must bind an existing project/continuity and task/principal/authorization reference; input revision and allowlisted input paths; isolated execution context; output location; approved provider policy; maximum wall time, turns, retries and output size; and a verification policy. The adapter must use Focusa-owned task/session identity, not issue a competing canonical task ID.

Native projection states:

```text
requested → preflight → awaiting_approval → queued → running
running → verifying → review_ready
running → pausing → paused
running/paused → stopping → stopped
any nonterminal → failed | unknown
```

Transitions are observations/projections of the owning runner and Focusa, not a second durable reducer. `review_ready` requires validated artifacts and evidence. `stopped` requires termination confirmation; `failed` and `unknown` never become success based on elapsed time. Reconcile after process/daemon restart using the owning runtime's identity and status.

Verification binds the output to its input revision. Changes to source invalidate direct application; present a conflict. For v0.1, writes stay in the approved output/copy area. Original-file replacement and external effects require separate authorization and tests.

## 8. Three initial reflex rules

Implement deterministic rules through existing Focusa signal/governance paths, not model-generated self-modifying code:

| Trigger | Bounded response | Forbidden escalation |
|---|---|---|
| Daemon or event connection lost | Mark UI stale/unavailable; disable new mutations; reconnect with bounded backoff | Start a duplicate daemon or replay a lost mutation |
| Resource pressure/battery policy reached | Defer new expensive work; request existing bounded pause/resource-mode operation when authorized | Kill canonical persistence or switch providers/data destinations without permission |
| Locked/suspending session | Preserve continuity; follow previously granted run policy; require confirmed checkpoint/stop where needed | Treat user absence as broader authority or imply sleeping hardware still executes |

Each observer result includes cause/correlation identity so a response does not repeatedly trigger itself. Debounce/coalesce observations; retained raw observations are bounded and short-lived. Surface meaningful state changes, not every event.

Secondary cognition uses existing Focusa workers when justified by a bounded task. Ontology extensions, trust/reliability evidence, and RDF/semantic verification remain Focusa-owned mechanisms; this release projects their results rather than reimplementing them in QML or the bridge.

## 9. Install transaction details

Stages: `inspect → validate → stage → backup_owned_entries → activate → verify → commit`.

Record exact source revision, dependency digests, owned files, prior config fragments and hashes, activation result, and rollback reference. Do not overwrite a nonempty destination that is not recorded as Veragensia-owned. Reject unsafe symlinks and concurrent config changes; recheck hashes before commit. If another application edited a shared config during installation, abort and preserve both states for resolution.

Only integrate through supported user/plugin hooks. Keep `/usr/share/omarchy` unchanged. No automatic firmware/disk/system-package changes; list prerequisites when missing. Service activation must not enable linger or start model work. Browser pairing is a separate private action.

On failure, restore only this transaction's owned changes. Do not use a blanket `git reset`, home-directory cleanup, or root snapshot as an overlay rollback. Test interrupted staging, failed plugin validation, failed daemon auth, failed activation, repeated install, and user edits before uninstall.

## 10. Machine-readable release gate

`config/v0.1-release-candidate.json` records inspected source/dependency facts and missing test evidence. It is a **candidate inventory**, not a credential, signed attestation, or executable policy grant. A release evaluator must reject unknown schema majors, mismatched dependency hashes, missing compatibility pins, absent installer/runner/browser artifacts, and any gate without passed evidence.

Status words have exact meaning: `not_run` is not `pass`; `candidate` is not `compatible`; `published_dependency` is not `Veragensia_released`; `base_ready` is not `integration_ready`.

Spec-validation can pass while release readiness remains false. Publishing these specifications does not produce a native binary, installation test, or hardware qualification. Release evidence must name the tested revision, not merely a mutable branch name.

## 11. Source references

- [Omarchy plugin API and unsandboxed-code warning](https://omarchy.org/manual/shell-plugins/).
- [Omarchy supported user configuration and hooks](https://omarchy.org/manual/dotfiles/).
- [Pinned Workpoint contract](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_workpoint_resume.md).
- [Pinned resource-mode contract](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_resource_mode.md).
- [Pinned loop-control contract](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/docs/focusa-tools/tools/focusa_work_loop_control.md).

Fly's environment/lifecycle ideas remain design inspiration for a later adapter, not a new operational dependency or new source of authority for v0.1.
