# 201 — Veragensia Agent Body Profiles, Embodiment, and Transfer Addendum

**Status:** DRAFT canonical product direction — additive companion to Docs 182, 190–200.  
**Canonical human architecture authority:** Verious Smith III under Doc 185.  
**Created:** 2026-09-14.  
**Focusa companion:** Spec 153B — Agent Embodiment, Body Profiles, and Cross-Body Continuity Addendum.  
**Primary dependencies:** Docs 191 (Elastic Agent Computing), 193 (enforcement), 194 (trusted human control), 195 (resource/runtime identity and transfer), 196 (trust), 197 (voice-native Agent Computer), 199 (Ambient Operator); Focusa Specs 72, 139, 151, 153/153A/153B, 156, 164, 181–184.

---

## 0. Decision

> **Veragensia treats computers, cloud runtimes, mobile/wearable endpoints, and future robotic/humanoid platforms as replaceable or concurrent Agent Bodies beneath persistent Focusa-governed identity and relationship continuity.**

The body is where a governed actor currently perceives, computes, communicates, and acts. It is not the actor's canonical identity.

A customer may move from:

```text
Chromebook
→ premium laptop / desktop
→ full Veragensia Agent Computer
→ cloud Agent Computer
→ mobile / wearable surfaces
→ future robotic or humanoid body
```

without creating a new canonical partner merely because the hardware changes.

---

## 1. Relationship to the Agent Computer

Doc 191 already defines one Agent Computer architecture capable of inhabiting local physical and cloud bodies plus workcells, browser contexts, Agent Apps, and Silent Session teams.

This addendum generalizes the body vocabulary without weakening the Agent Computer distinction.

```text
                    PERSISTENT PARTNER / AGENT
                 Focusa identity + relationship
                           |
                      BodyBinding
                           |
        +------------------+-------------------+
        |                  |                   |
 interactive computer   cloud body        robotic body
 Chromebook/laptop      Agent Computer     humanoid/etc.
        |                  |                   |
        +------------------+-------------------+
                           |
                same governed work fabric
```

A **Full Veragensia Agent Computer** remains the strongest general-purpose computing body because it includes native enforcement, trusted human control, workload identity, resource governance, voice-complete integration, and full execution topology.

A Chromebook or conventional Linux machine may expose a rich Veragensia integration experience without claiming full Agent Computer enforcement parity.

---

## 2. Foundational laws

1. **Body is runtime, not identity.** Device/chassis/VM/process identifiers are runtime locators or node identities, not the persistent partner identity.
2. **Transfer advances runtime posture.** Moving to another body requires a fresh `RuntimeIncarnation` and re-evaluation of capabilities, trust, EnforcementPlan, credentials, resources, locality, and control leases.
3. **Body capability is discovered, not assumed.** Veragensia records what the body can actually perceive, actuate, compute, communicate, and safely expose.
4. **No stale authority crosses bodies.** Old process IDs, browser targets, compositor objects, device handles, credential leases, control leases, and actuator bindings cannot silently bind to the destination body.
5. **Human control remains available.** Every interactive or physical body profile defines a body-appropriate emergency stop/takeover path that survives agent/model degradation.
6. **Physical bodies add consequence, not sovereignty.** A humanoid or robot chassis does not gain authority merely because it can act in the physical world.
7. **Cloud bodies and physical bodies can coexist.** Heavy computation may remain in cloud Agent Computers while a local physical body supplies presence, sensors, and actuators.
8. **Concurrent bodies require explicit control ownership.** Multiple attached bodies may project the same persistent partner, but actuator/write/control rights are fenced by exact scope and generation.
9. **Body replacement should be routine.** Commodity hardware may improve rapidly; the architecture must allow the persistent system to adopt better bodies without product re-architecture or relationship reset.
10. **The strongest applicable execution body wins under policy.** Placement may select local, cloud, browser, specialist, or physical execution based on work, authority, latency, trust, privacy, resource and embodiment requirements.

---

## 3. Veragensia `AgentBody`

```yaml
schema: veragensia.agent_body.v1
agent_body_ref:
body_class:
body_profile_ref:
node_identity_ref:
runtime_incarnation_ref:
owner_principal_ref:
platform_trust_class:
runtime_attestation_ref:
focusa_binding_ref:

capability_sets:
  perception: []
  actuation: []
  communication: []
  compute: []
  storage: []
  mobility: []
  human_interface: []

execution:
  enforcement_profile_ref:
  resource_budget_ref:
  topology_grant_ref:
  control_lease_refs: []

physical:
  physical_system_ref:
  digital_twin_ref:
  safety_envelope_ref:
  emergency_stop_ref:

lifecycle_state:
freshness_ref:
```

`AgentBody` is a Veragensia runtime projection. It does not replace Focusa `AgentIdentity`, Workstream, Foreman, or conversation/state ownership.

---

## 4. Body classes

### 4.1 `integrated_computer`

Conventional computer with Veragensia integration but not necessarily full Agent Computer enforcement.

Examples:

```text
ChromeOS + Crostini Chromebook
existing Linux laptop
existing Linux desktop
```

Possible experience:

- Workforce browser surface;
- Wirebot App;
- Focusa Desktop/PWA where supported;
- Pi/reference harness;
- voice adapters;
- local telemetry/resource posture;
- remote/cloud workload placement;
- UIAI browser/computer integration;
- launcher/status/notification/workspace integration.

This can feel highly agent-centric while remaining honest about missing machine-enforcement guarantees.

### 4.2 `full_agent_computer`

Full supported Veragensia profile with the native guarantees owned by Docs 182/190–199.

Expected differentiators include:

- `ExecutionPrincipal` / `WorkloadIdentity`;
- machine-installed `EnforcementPlan`;
- Secure Attention Plane;
- Human Control Reserve;
- versioned desktop observations;
- fenced `ComputerControlLease`;
- native resource/pressure governance;
- voice-complete operating path;
- exact trust/attestation profile;
- local/cloud topology resolution.

### 4.3 `cloud_agent_computer`

A full or profile-bounded Agent Computer hosted remotely and accessed through streamed, API, voice, or agent surfaces.

It may supply heavy compute to another body without becoming the human's primary physical interface.

### 4.4 `mobile_wearable`

Paired phone, earbuds, watch, glasses, or similar embodied edge surface governed by Docs 197/199 and Focusa Ambient Operator.

### 4.5 `robotic_body`

A physical execution body with sensors, controllers, and actuators governed by Focusa physical/robotics semantics plus Veragensia identity, trust, enforcement, control and lifecycle rules.

### 4.6 `humanoid_robotic_body`

A specialization of robotic body optimized for human environments and potentially exposing:

```text
vision / depth perception
hearing / speech
head / torso orientation
bipedal or equivalent locomotion
arms / hands / grasping
force / torque / tactile sensing
human-scale tool and environment interaction
local compute / connectivity
physical emergency stop
```

Humanoid form is a body capability package, not a new cognition or identity system.

---

## 5. Integrated computer versus Full Agent Computer

This distinction is commercially and architecturally important.

| Concern | Integrated existing computer | Full Veragensia Agent Computer |
|---|---|---|
| Existing OS retained | Yes | Stock supported base + Veragensia full profile |
| Wirebot / Workforce / Focusa surfaces | Yes | Yes |
| Pi / agents | Yes | Yes |
| UIAI | Yes | Yes |
| Voice | Supported according to adapters | Voice-complete profile possible |
| Remote/cloud workforce | Yes | Yes |
| Custom launcher/status/notifications | Yes where platform permits | Native governed integration |
| Resource-aware placement | Service/advisory where supported | Native topology/resource governance |
| Workload identity | Partial/runtime dependent | First-class |
| Machine enforcement | Best available OS/container/runtime facilities | Required verified `EnforcementPlan` |
| Secure attention | Normal application/platform constraints | Trusted Veragensia surface |
| Human Control Reserve | Best effort | Architectural invariant |
| Computer control fencing | UIAI/platform dependent | Generalized native control lease |
| Physical/robotic extension | Remote/adapter possible | First-class body/runtime profile |

The integrated profile is not “Veragensia Lite.” It is a legitimate deployment mode for bringing the human-agent system to an existing computer while preserving an honest boundary around guarantees only a Full Agent Computer can provide.

---

## 6. Body attachment

A body is attached only after:

```text
identify node/body
→ verify owner/pairing
→ establish runtime incarnation
→ verify platform/runtime trust
→ discover capabilities
→ evaluate resource/energy/network posture
→ bind Focusa actor/Workstream/Foreman scope
→ compile/install applicable enforcement
→ issue only necessary current leases/grants
→ activate body projection
```

Attaching a body does not transfer canonical databases by default.

---

## 7. Body transfer

A transfer moves primary embodied interaction/execution from one body to another.

```yaml
schema: veragensia.body_transfer.v1
body_transfer_id:
actor_principal_ref:
focusa_binding_ref:
source_body_ref:
source_runtime_incarnation_ref:
destination_body_ref:
destination_runtime_incarnation_ref:
resource_replica_refs: []
unsettled_effect_refs: []
conversation_continuity_refs: []
control_lease_transition_refs: []
credential_reissue_refs: []
enforcement_plan_refs: []
source_fencing_ref:
started_at:
completed_at:
result:
```

Transfer requirements:

1. preserve logical work/relationship identity through Focusa;
2. create or verify the destination incarnation;
3. re-establish exact ResourceRefs/replicas/revisions;
4. reissue applicable credentials rather than copying stale leases;
5. compile destination-appropriate enforcement;
6. invalidate stale observation/control/actuator handles;
7. reconcile unsettled external effects;
8. fence the source where exclusive control is required;
9. produce evidence/receipts for the transition.

---

## 8. Body concurrency

The preferred system may use several bodies simultaneously.

Example:

```text
Wirebot / persistent partner
            |
    +-------+---------+----------------+
    |                 |                |
Chromebook        Cloud Agent      Humanoid
interaction       Computer          presence
voice/display     heavy compute     manipulation
browser           software fleet    physical world
```

This is not identity cloning.

Each body has:

- its own `NodeIdentity`;
- its own `RuntimeIncarnation`;
- its own capability snapshot;
- its own trust/resource posture;
- body-specific control/credential/enforcement state.

The persistent actor/role/Workstream above them remains shared according to Focusa authority.

---

## 9. Placement with embodiment requirements

Doc 191 placement/topology resolution gains one additional class of requirement: **embodiment**.

A work request may declare:

```yaml
embodiment_requirements:
  physical_presence: optional | required
  mobility: []
  manipulation: []
  perception: []
  human_interaction: []
  locality_constraints: []
  latency_class:
```

Examples:

```text
compile repository
→ cloud workcell

research website
→ UIAI browser context

speak privately with owner
→ local trusted audio / paired wearable

carry package to another room
→ robotic body with locomotion + grasping
```

No topology resolver may satisfy a physical-actuation requirement with a nonphysical body and falsely report completion.

---

## 10. Robotic body enforcement boundary

Physical actuation is governed through layered control:

```text
Focusa intent / authority
        ↓
Veragensia workload/body identity
        ↓
body capability + current state
        ↓
physical safety preflight
        ↓
controller command envelope
        ↓
deterministic robot controller
        ↓
actuator
```

Veragensia is not required to replace vendor motor-control firmware or robotics middleware. It binds high-level governed operations to verified body capabilities and enforces the boundary around who may request what.

For consequential actuation, the body profile MUST expose where applicable:

- deterministic emergency stop;
- watchdog health;
- current actuator/controller identity;
- current sensor freshness/calibration;
- energy/thermal posture;
- physical safety envelope;
- control holder/fencing generation;
- post-action observation route.

---

## 11. Human control on a physical body

Doc 194 Secure Attention/Human Control semantics extend to physical bodies.

Body-appropriate controls MAY include:

```text
spoken stop
dedicated hardware emergency stop
paired trusted-device stop
local physical takeover
remote operator takeover
motion freeze
actuator disable
```

A network request to stop is insufficient as the only safety path for a consequential physical body.

A local deterministic safety stop may occur before higher-level Focusa reconciliation. That local stop MUST NOT be misreported as canonical mission completion.

---

## 12. Relationship continuity UX

The product must present body replacement as continuity, not re-onboarding.

Expected customer experience:

```text
Old Chromebook
   ↓
"Move my Partner to the new computer."
   ↓
new body qualified and attached
   ↓
same Wirebot relationship
same Workstreams / Foremen
same current work
same evidence/history
new capabilities available
```

Future robotic experience:

```text
"Attach the humanoid body."
   ↓
qualify body / trust / sensors / actuators
   ↓
attach to same governed system
   ↓
physical capabilities become available
without replacing the persistent partner
```

The product SHOULD make newly available and unavailable capabilities explicit after transfer.

---

## 13. Cloud augmentation of a physical body

A physical body need not contain all intelligence or compute locally.

A premium embodied Partner may use:

```text
physical body
  sensors + actuators + local deterministic control
              |
              v
local Veragensia safety / body runtime
              |
              v
Focusa / Wirebot relationship layer
              |
              v
elastic cloud Agent Computers / workcells / specialists
```

Latency-sensitive or safety-critical loops remain local/deterministic where required. High-level reasoning, software work, research, large-context operations, simulation, and additional workforce may scale elastically in the cloud under `TopologyGrant` and placement policy.

This separation allows physical hardware to remain replaceable while the available workforce/compute can scale independently.

---

## 14. Product direction

Veragensia's long-term body model explicitly supports a progression from inexpensive integrated computers to premium Full Agent Computers and future robotic/humanoid embodiments without changing the persistent human-agent relationship architecture.

The commercial product is therefore not defined by one chassis.

It is the governed software/relationship/execution system that can inhabit successively richer bodies and attach elastic cloud workforce as needed.

This statement does not claim that a Veragensia humanoid product is presently implemented, safe, certified, or commercially available.

---

## 15. Acceptance invariants

Tests for body portability must prove:

1. body replacement preserves higher-level actor/Foreman/Workstream identity;
2. destination runtime receives a fresh incarnation;
3. source runtime handles fail after fencing;
4. capability differences are exposed rather than silently emulated;
5. body-specific credentials/control leases are reissued under current authority;
6. Workpoint/Evidence/conversation continuity remains available;
7. concurrent bodies have explicit actuator/write ownership;
8. cloud augmentation does not bypass physical safety/locality requirements;
9. physical actuation cannot proceed under stale/unknown body state;
10. hardware replacement does not require rebuilding the partner relationship from scratch.

---

## 16. Ownership and non-goals

Focusa owns persistent cognition/work/relationship state and physical semantic authority. Veragensia owns body/runtime integration, enforcement, trust, lifecycle, resource placement, and trusted control. UIAI owns browser/computer execution inside its domain. Vendor robotics stacks may own servo control, motion planning, hardware drivers, and real-time safety mechanisms beneath registered governed operations.

This addendum does not:

- select a robot vendor;
- define a custom humanoid chassis;
- replace ROS/vendor robotics middleware;
- claim current robotic-product readiness;
- let cloud reasoning directly drive motors;
- turn a device serial or chassis identity into the persistent partner identity;
- collapse Wirebot, Focusa, Workforce, UIAI, and Veragensia into one implementation owner.
