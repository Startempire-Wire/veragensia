# 193 — Veragensia Execution Substrate, Workload Identity, and Capability Enforcement

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Primitive role:** Veragensia enforcement substrate translating Focusa semantic authority into actual machine restrictions.
**Dependencies:** Focusa Spec 66 affordance/execution ontology, Spec 136 proposal-to-settlement, Spec 137 temporal authority, Spec 139 environment/placement, Spec 156 credential authority; UIAI execution/control contracts; Docs 190–192.

## 1. Decision

Veragensia is the **machine enforcement substrate** for Focusa-governed action.

Focusa may correctly decide:

```text
agent A may edit resource X
agent A may not read resource Y
agent A may call origin Z
agent A may use one credential for operation Q
```

but those statements are not sufficient until the operating environment makes violations technically unavailable or detectably fail closed.

The core translation is:

```text
Focusa semantic authority
        ↓
CapabilityGrant / AuthorityDecision
        ↓
Veragensia EnforcementPlan
        ↓
ExecutionPrincipal + WorkloadIdentity
        ↓
Linux / compositor / portal / runtime enforcement
        ↓
actual process and effects
```

A process running under the human's ordinary Unix UID with ambient access is not a governed agent merely because its prompt contains restrictions.

## 2. Foundational laws

1. **Capability is not permission; permission is not enforcement.** Preserve Focusa Spec 66 distinctions all the way to the machine.
2. **No ambient authority by shared UID.** Same-UID access to files, D-Bus, keyrings, compositor sockets, accessibility, devices or processes does not count as scoped permission.
3. **Every governed workload has an ExecutionPrincipal.** Human session identity, agent principal, workload identity and Unix/container identity remain distinguishable.
4. **Every privileged workload has a verifiable WorkloadIdentity.** Process/container membership alone is not enough.
5. **Every consequential run has an immutable EnforcementPlan.** It is derived from the approved semantic scope and bound to exact runtime incarnation.
6. **Ready means enforced.** A run cannot report `ready`/`running_governed` until its required isolation and grants are installed and verified.
7. **Default deny across authority channels.** Filesystem, network, session buses, accessibility, screen/audio capture, input injection, credentials and devices are separate capability domains.
8. **Fallback cannot expand authority.** Moving from API → accessibility → computer use never grants broader data or device access.
9. **Credential custody remains brokered.** A workload receives a narrow action/lease/injection capability rather than broad secret material wherever possible.
10. **Human control infrastructure is protected.** Agent resource use may not prevent the owner from observing, interrupting, revoking or recovering the system.
11. **X11/Xwayland is not assumed isolated.** Shared Xwayland access is treated as a broad desktop capability unless application-specific isolation is proven.
12. **Accessibility is privileged.** AT-SPI or equivalent semantic UI access is explicitly granted by target/scope; it is not an ambient agent right.
13. **Portals are capability brokers, not authority sources.** User/session portals may mediate capture, files, devices and remote desktop but cannot create Focusa permission.
14. **Host root does not equal product authority.** Infrastructure privilege is an enforcement mechanism, not permission to act on the user's behalf.
15. **Isolation posture is evidence.** The runtime records which enforcement mechanisms were actually active, their versions and degradation.

## 3. Identity layers

Veragensia must keep these separate:

```text
OwnerPrincipal
    constitutional owner

AgentPrincipal
    conceptual human/AI actor

NodeIdentity
    physical or cloud Agent Computer

WorkloadIdentity
    exact executable/runtime instance making a call

ExecutionPrincipal
    OS/runtime security identity and sandbox boundary

RuntimeAttestation
    exact software/image/policy posture

CapabilityGrant
    what this actor/workload may do
```

No identifier in one layer silently substitutes for another.

## 4. `ExecutionPrincipal`

```yaml
schema: veragensia.execution_principal.v1
execution_principal_id:
node_identity_ref:
workload_identity_ref:
agent_principal_ref:
uid_gid_posture:
namespace_refs: []
cgroup_ref:
security_profile_refs: []
runtime_incarnation_ref:
created_at:
expires_at:
```

An ExecutionPrincipal may use:

- a dedicated Unix UID;
- user namespace;
- container/microVM identity;
- systemd transient service/scope with additional isolation;
- Landlock/seccomp/LSM policy;
- application-specific sandbox;
- a combination.

The schema does not require one technology across every profile, but the declared protection must be testable.

## 5. `WorkloadIdentity`

```yaml
schema: veragensia.workload_identity.v1
workload_identity_id:
node_identity_ref:
agent_principal_ref:
workload_kind: agent | agent_app | workcell | browser_worker | verifier | system_service
software_digest_ref:
image_digest_ref:
entrypoint_digest_ref:
runtime_constitution_ref:
policy_bundle_digest_ref:
attestation_ref:
issued_at:
expires_at:
```

A remote/local privileged service verifies workload identity and matching grant before execution.

Workload identity is designed to remain meaningful across container scheduling while still changing when the executable/runtime posture materially changes.

## 6. `EnforcementPlan`

```yaml
schema: veragensia.enforcement_plan.v1
enforcement_plan_id:
authority_decision_ref:
capability_grant_refs: []
runtime_incarnation_ref:
execution_principal_ref:

filesystem:
  read_resource_refs: []
  write_resource_refs: []
  temp_refs: []
  home_access: none

network:
  allowed_destinations: []
  allowed_protocols: []
  listen: []

dbus:
  session_names: []
  system_names: []

compositor:
  observe_surface_refs: []
  actuate_surface_refs: []

accessibility:
  target_surface_refs: []

audio_video:
  microphone_refs: []
  playback_refs: []
  screen_capture_refs: []
  camera_refs: []

devices:
  refs: []

credentials:
  broker_grant_refs: []

resources:
  cpu_weight:
  io_weight:
  memory_high:
  memory_max:
  pids_max:

syscalls:
  profile_ref:

created_at:
fresh_until:
```

The plan is machine policy, not merely documentation.

## 7. Enforcement compilation

Veragensia compiles an EnforcementPlan from:

- Focusa exact project/continuity/Workpoint;
- operation identity;
- Capability Grant;
- authority/confirmation decision;
- affected ResourceRefs;
- Agent App descriptor;
- placement/trust class;
- credential requirements;
- data-locality/network policy;
- risk/reversibility classification;
- human-control reserve policy.

Compilation is deterministic for fixed inputs and records the source digests.

A capability unknown to the compiler produces `unsupported_enforcement`, not an unrestricted process.

## 8. Filesystem isolation

Path strings are not sufficient authority.

Required principles:

- resolve user-authorized resources through stable ResourceRefs from Doc 195;
- bind read/write policy to pre-opened or safely resolved roots;
- reject traversal, magic-link and symlink escape where applicable;
- prevent access to unrelated `$HOME`, Focusa databases, SSH state, browser profiles and credential stores by default;
- mount or project only required inputs and outputs into workcells/Agent Apps;
- distinguish read source, writable working copy and settlement/apply target;
- verify resource revision before applying a mutation.

## 9. Network isolation

Network is a separate capability.

A workload MAY have:

```text
no network
loopback to named broker only
allowlisted domains/origins/endpoints
project service mesh only
general internet egress
listener capability
```

General internet must not be implicitly inherited because the desktop user has network access.

DNS resolution, redirects, proxies and tunnels must not bypass destination policy.

## 10. D-Bus, secret service and desktop IPC

Session buses are powerful ambient channels.

Agent workloads MUST NOT automatically inherit unrestricted access to:

- Secret Service/keyring;
- notification services with sensitive content;
- clipboard managers;
- password managers;
- desktop portals outside granted operations;
- application private D-Bus APIs;
- system management buses.

Explicitly mediated D-Bus calls may be exposed as Agent App capabilities.

## 11. Wayland, Xwayland and input

Wayland/compositor access is capability-scoped.

Policies distinguish:

```text
surface_metadata_read
surface_capture
accessibility_read
input_injection
window_management
full_desktop_control
```

A shared Xwayland server can weaken isolation between X11 clients. Agent-controlled X11 applications therefore require one of:

- application-specific Xwayland isolation;
- dedicated Agent Computer/session;
- sandbox proven to prevent cross-client access;
- explicit classification as broad desktop authority.

Do not claim per-app isolation when the runtime actually exposes a shared X11 security domain.

## 12. Accessibility bus

Semantic desktop automation is preferable to pixel automation but is privileged.

An accessibility grant binds:

- exact target application/surface;
- allowed reads/actions;
- runtime generation;
- project/work binding;
- expiry;
- evidence requirements.

A process able to inspect every accessible object in the human session has broad observation authority and must be treated accordingly.

## 13. Audio/video/device capabilities

Microphone, speaker routing, screen capture, camera, USB, Bluetooth, serial, removable storage and other devices are individually mediated.

Doc 181 in Focusa and Veragensia Doc 197 govern voice conversation. A voice-complete profile may keep an approved microphone/audio output route available to the trusted conversation service while ordinary agent workloads still lack ambient microphone access.

## 14. Credential capability

Credential access is an operation capability, not a file/socket convenience.

Preferred sequence:

```text
workload requests registered operation
→ Focusa verifies authority
→ credential broker verifies matching grant
→ broker performs or injects only the required credential action
→ workload receives result/status, not broad secret custody
```

A browser/computer-control lease does not automatically carry credential grants.

## 15. Human Control Reserve

The owner must remain able to stop the system under pressure.

Protected components include at minimum:

- compositor/input path;
- trusted consent/secure-attention surface;
- Focusa daemon authority path;
- Veragensia enforcement/control broker;
- Focusa Desktop/control surface;
- emergency stop/revoke path;
- essential audio interaction path for voice-complete profiles.

Agent workloads are subordinate cgroup/resource classes.

Admission control rejects or throttles new work before protected control components become nonresponsive.

## 16. Enforcement evidence

Before a run becomes governed-ready, the runtime produces:

```yaml
schema: veragensia.enforcement_attestation.v1
plan_ref:
runtime_incarnation_ref:
mechanisms:
  - kind:
    status:
    version:
    evidence_ref:
degraded_controls: []
verified_at:
```

Claims such as `filesystem_isolated=true` require a real negative test/evidence path for release acceptance.

## 17. Integration with Focusa Spec 136

A consequential operation follows:

```text
Focusa proposal / intent
→ authority decision
→ durable execution intent
→ Veragensia enforcement compilation + verification
→ dispatch
→ effect
→ reconciliation
→ outcome verification
→ settlement / Receipt
```

Veragensia does not settle Focusa work. It supplies enforced execution and evidence.

## 18. Integration with Agent App Resolver

Doc 190 resolver selection now has a hard additional gate:

> A selected application/runtime is not eligible for governed execution unless Veragensia can compile and verify an EnforcementPlan appropriate to its declared capabilities and risk.

An A3/A4 descriptor without enforceable isolation cannot receive a higher trust classification merely because its API is structured.

## 19. Acceptance invariants

A governed execution substrate is not accepted until tests prove:

1. an agent denied `$HOME` cannot read unrelated user files;
2. a denied network workload cannot egress through DNS/redirect/proxy shortcuts;
3. same-UID assumptions do not bypass the sandbox;
4. a workload cannot access the keyring/Secret Service without a matching grant;
5. accessibility access is target/scoped;
6. screen/microphone/input capabilities are separately enforced;
7. shared Xwayland exposure is either isolated or reported as broad authority;
8. stale/expired EnforcementPlans fail closed;
9. workload identity mismatch denies the operation;
10. human control remains responsive under CPU/memory/I/O pressure;
11. a fallback actuator cannot expand granted scope;
12. enforcement posture is represented in Evidence/Receipt lineage.

## 20. Final principle

> Focusa decides what an agent may do. Veragensia makes the machine behave as though that decision is real.
