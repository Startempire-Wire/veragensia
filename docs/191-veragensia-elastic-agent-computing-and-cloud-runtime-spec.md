# 191 — Veragensia Elastic Agent Computing and Cloud Agent Computer Runtime

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 182b (base/overlay), 182c (fleet bridge), 183 (public demo lifecycle), 190 (agent-first software), 192 (telemetry/improvement), 193–197 (enforcement, control, identity, trust, voice).

## 1. Decision

Veragensia is one Agent Computer architecture that can inhabit a local physical body, a full streamed cloud body, headless workcells, browser execution contexts, isolated Agent Apps, and bounded Silent Session teams.

Cloud execution is **not** defined as “spawn more headless agents.” A request for more capability is resolved into the topology that best satisfies the work, authority, resource, privacy, latency, trust and user-interaction requirements.

```text
                         USER
                   voice / UI / API
                          |
                     Veragensia
                  the Agent Computer
                          |
              +-----------+-----------+
              |                       |
         LOCAL BODY               CLOUD BODY
      physical Omarchy       full streamed computer
              |                       |
              |                 Focusa Desktop
              |                 Pi / agents
              |                 UIAI Cockpit
              |                 Voice / Audio UI
              |                 Agent Apps
              |                       |
              +---------- FOCUSA WORK FABRIC ---------+
                          |             |
                     workcells     Silent Sessions
```

The diagram is a responsibility model, not a requirement that all elements run in one process or one host.

## 2. Core abstraction: Agent Computer

An **Agent Computer** is a governed Veragensia execution environment with a human/agent interaction surface, Focusa binding, declared application/capability profile, bounded resources, identity/trust class, storage/lifecycle policy and execution topology.

Illustrative object:

```text
AgentComputer {
    owner_principal_ref
    trust_class
    platform_trust_class
    runtime_attestation_ref
    runtime_incarnation_ref
    image_profile
    desktop_profile
    capability_profile
    voice_profile
    enforcement_profile
    app_profile
    focusa_binding
    agent_team
    storage
    lifecycle
    network_policy
    resource_budget
    topology_grant_ref
    telemetry_policy
}
```

The object describes the computer; it does not mint authority. Owner identity, Focusa grants, product entitlement, credential custody and application permissions remain independently verified.

Doc 193 governs actual workload enforcement; Doc 195 governs runtime incarnation/state transfer; Doc 196 governs platform/runtime trust.

## 3. `os.focusa.dev` as the first crude Cloud Agent Computer runtime

The existing public demo has the correct primitive shape even though it is not the production architecture:

- LinuxServer webtop Ubuntu/KDE full desktop;
- persistent `/config` desktop state;
- real Chromium;
- Focusa Workforce extension;
- local Focusa daemon;
- Selkies streaming;
- Cloudflare tunnel;
- keeper/self-healing and public lifecycle controls.

Architecturally, this is the first crude implementation of the **Veragensia Cloud Agent Computer Runtime**.

`os.focusa.dev` remains a special `public_demo` trust profile governed by Doc 183. Its public credential posture, implementation details and lifecycle MUST NOT be copied into private/customer profiles merely because the runtime shape is reused.

## 4. Agent Computer Profiles

Profiles describe capability and experience requirements rather than cloning one giant machine image.

Illustrative profiles:

```yaml
profile: executive_assistant
desktop: true
voice: voice_complete
capabilities:
  - research
  - correspondence
  - scheduling
  - document_editing
  - browser_work
  - remote_desktop_assistance
agents:
  default_team: 4
  burst_max: 20
```

```yaml
profile: software_team
desktop: true
voice: voice_complete
capabilities:
  - browser_work
  - software_development
  - source_control
  - terminal
  - build_and_test
agents:
  default_team: 6
  burst_max: 40
```

```yaml
profile: real_estate_assistant
desktop: true
voice: voice_complete
capabilities:
  - browser_work
  - crm
  - correspondence
  - scheduling
  - pdf
  - spreadsheet
  - mapping
agents:
  default_team: 3
  burst_max: 15
```

Same Veragensia primitives; different **affordance packages**.

Doc 190 governs application/capability resolution. A profile MAY pin an exact app where required, but capability requests are preferred.

A `voice_complete` profile is subject to Doc 197: ordinary supported workflows cannot depend on keyboard/pointer mechanics.

## 5. Execution topology classes

A request may resolve into one or more of the following:

### 5.1 Full Agent Computer

A streamed or local complete desktop with the normal first-party surfaces for its profile, including Focusa binding and governed human/agent interaction.

Use when work benefits from persistent desktop state, arbitrary applications, human takeover/assist, voice conversation, visually rich software, or multi-application workflows.

### 5.2 Headless Workcell

A bounded execution environment without a full desktop, suitable for structured tasks, automation, builds, research pipelines, data work or other workloads that do not need persistent graphical interaction.

A workcell specializes existing Focusa ExecutionContext/affordance semantics. It MUST NOT create a parallel authority, identity or permission model. It receives a Doc-193 ExecutionPrincipal/EnforcementPlan and Doc-196 workload/runtime attestation.

### 5.3 Silent Session team

Daemon-native Focusa Silent Sessions provide durable background agent execution, steering, pause/resume/restart, approvals, idempotency and receipts.

Use multiple exact workloop-bound sessions for agent-team fanout rather than raw shells or independent mutable worlds.

### 5.4 Agent App

A bounded application capability, potentially native, OCI/containerized, web/UIAI-backed, headless service or remote specialist runtime. Doc 190 defines Agentability and descriptors; Doc 193 defines its enforcement eligibility.

### 5.5 Browser execution context

UIAI Engine may satisfy work through structured browser capabilities, semantic browser automation or authorized visual interaction without requiring a whole new Agent Computer.

### 5.6 Voice conversation surface

A voice request itself is not a separate compute topology. Focusa Doc 181/Veragensia Doc 197 interpret the conversation into canonical operations that may resolve into any of the topologies above.

## 6. Topology is an OS decision

The user should be able to ask—naturally by voice or another modality:

> Give this project another team.

Veragensia may resolve that request as, for example:

```text
+ 20 Silent Sessions
+ 4 browser workcells
+ 1 full Agent Computer
```

or:

```text
1 full Agent Computer
  + browser capability
  + correspondence capability
  + spreadsheet/PDF capability
  + CRM Agent App
  + 8-agent team
```

The user does not need to choose VMs, containers, Durable Objects, browser contexts or process topology merely to request more workforce.

The topology decision MUST remain inspectable and constrained by resource, privacy, authority, trust, data locality and spend policy.

## 7. `TopologyGrant`

Elasticity itself is a capability and MUST be bounded so agents cannot recursively create unbounded agents/computers merely because they can request more help.

```yaml
schema: veragensia.topology_grant.v1
topology_grant_id:
subject_principal_ref:
project_ref:
continuity_id:
allowed_runtime_classes:
  - full_agent_computer
  - workcell
  - silent_session
  - agent_app
  - browser_context
max_active_agent_computers:
max_active_workcells:
max_active_sessions:
max_total_agents:
max_fanout_per_request:
max_spawn_depth:
max_spend:
max_wall_time:
allowed_regions: []
data_locality_refs: []
provider_refs: []
may_delegate: false
expires_at:
revocation_ref:
```

Rules:

- `may_delegate` defaults to `false`;
- a child topology can never exceed the parent grant;
- an agent created under a grant cannot create another fleet unless explicitly allowed;
- fanout multiplication cannot multiply spend/capability bounds implicitly;
- topology capacity is not application authority;
- scale-down/revocation must fence stale workloads rather than merely stop showing them in UI.

Focusa's existing FanoutPlan/session budgets remain the work-orchestration primitive; `TopologyGrant` bounds the **infrastructure/execution bodies** that may be created to realize it.

## 8. Agent interaction surfaces on a full Agent Computer

Supported full profiles SHOULD deliberately include the canonical defaults from Doc 190:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser/computer surfaces;
- Veragensia enforcement/control substrate;
- Voice/Conversation service bound to Focusa Doc 181;
- Veragensia session/shell integration.

Constrained, special-purpose and public-demo profiles MAY omit surfaces deliberately. Omission must be declared by profile; it must not silently redefine the canonical full Agent Computer composition.

## 9. Application execution classes

Do not containerize every graphical application blindly. The initial execution classes are:

| Class | Examples | Runtime |
|---|---|---|
| Desktop-native | file manager, terminal, native editor | main Agent Computer under appropriate enforcement |
| Sandboxed Agent App | CRM helper, PDF processor, dev environment | OCI/container or equivalent isolation |
| Web Agent App | SaaS, vendor portal, web CRM | UIAI/browser context |
| Headless service | transforms, indexing, data/service work | workcell/service runtime |
| Remote specialist | high-resource or special platform application | separate Agent Computer/runtime |

The resolver chooses by capability, Agentability, enforceability, state, latency, trust, licensing and resources—not by a blanket “everything in Docker” rule.

## 10. Full computer use is required

Agents need three ways to accomplish work:

```text
1. Structured capability
   API / typed operation / CLI / agent protocol

2. Semantic application automation
   browser DOM/AX / accessibility / application model

3. Computer use
   see desktop / generic input / arbitrary app
```

Prefer 1 over 2 and 2 over 3 when the resulting outcome and governance are equivalent. Level 3 remains mandatory for legacy, unfamiliar and otherwise non-automatable software.

The **human** does not need to mirror this mechanic. Under Doc 197 the person can speak in goals and corrections while the Agent Computer selects the execution path.

## 11. Agent Assist Session

A full Agent Computer supports a first-class **Agent Assist Session** for authorized collaborative desktop work.

Conceptual user modes remain:

```text
observe_only
    agent observes authorized surface

guide
    agent points/highlights/explains; human acts

shared_control
    agent may act; human can interrupt immediately

delegated_control
    agent controls the desktop within explicit scope
```

The underlying primitive is stronger than the mode label:

```text
Focusa Intervention
        +
Veragensia/UIAI ComputerControlLease
        +
DesktopObservation
        +
OperatorDeltaReceipt
        +
mandatory re-observation / authority refresh
```

Requirements:

- session binds human, agent principal, task/Workpoint, computer/runtime incarnation and authority refs;
- observation and action scope are explicit;
- one active actuator holder exists per controlled scope;
- control leases carry generation + fencing token;
- human interruption/revocation is immediate where the runtime permits;
- local safety freeze may precede Focusa acknowledgment but MUST NOT masquerade as canonical Focusa pause;
- actions use structured/semantic interfaces when available and visual control when necessary;
- resulting material changes produce appropriate Evidence/receipts;
- private content outside the authorized session scope is not ambiently captured;
- a remote-control channel is transport capability, never authority by itself;
- returning control requires operator delta capture, fresh DesktopObservation and credential/authority refresh;
- voice commands such as "stop", "give me control", "continue", or "don't continue" route to the same intervention/control primitives.

This should feel like a highly capable human assistant joining the computer while remaining governed by Focusa and Veragensia.

## 12. Focusa work fabric and writer fencing

Elastic execution MUST build on Focusa's existing exact routing and mutation-fencing work.

The relevant routing identity includes:

```text
project_root
+ continuity_id
+ working_subpath_id
```

Multi-node/multi-agent execution requires exact scope assignment, health/capability registration, writer leases where applicable, mutation IDs, payload digests, effect receipts and isolated workspaces/worktrees.

Doc 195 extends this with stable ResourceRefs, replica revisions and runtime incarnations.

The invariant is:

> Many agents may collaborate on one mission; they MUST NOT become many independent writers that each believe they own the same writable world.

Infrastructure lease, VM ownership, container ownership, root access or browser control never substitutes for Focusa application authority.

## 13. Elastic lifecycle

A cloud Agent Computer or workcell SHOULD support evidence-backed lifecycle transitions such as:

```text
requested
→ provisioned
→ binding
→ attesting
→ enforcing
→ ready
→ active
→ quiescing
→ checkpointed
→ suspended
→ resumed
→ retiring
→ destroyed
```

When work completes:

```text
agents settle work
→ receipts/evidence committed
→ state checkpointed where applicable
→ Agent Apps/workcells stop
→ full Agent Computer suspends or retires
→ compute usage approaches zero while idle
```

Filesystem checkpoint, process resume, Focusa cognitive continuity, Conversation Ledger continuity and reversal of external effects remain separate concepts.

Doc 195 defines what survives/rebinds/invalidates across restart, restore and migration. A recreated/resumed runtime cannot adopt stale control leases, process IDs, observations or credential leases by convenience.

## 14. Resource and spend governance

Elasticity is bounded by both profile policy and `TopologyGrant`.

A profile/request may define:

- default team size and burst maximum;
- CPU/memory/GPU/storage limits;
- browser/session limits;
- model/provider/token budgets;
- wall-clock duration;
- maximum active Agent Computers/workcells;
- network/egress policy;
- allowed regions/data locality;
- idle suspend/retire thresholds;
- minimum platform trust;
- Human Control Reserve.

Scale-up does not imply permission expansion. Scale-down must preserve canonical work/evidence and honest uncertain/pending states.

Protected human-control/audio/secure-attention resources from Docs 193–194 cannot be consumed by fleet expansion.

## 15. Local/cloud continuity

Local and cloud bodies share Focusa project/continuity semantics without becoming one undifferentiated mutable machine.

A handoff SHOULD preserve:

- exact project/continuity/workpoint identity;
- relevant bounded context;
- authority/grant refs;
- ResourceRefs/replica revisions;
- input revision/workspace binding;
- evidence and outstanding blockers;
- execution ownership and cancellation state;
- unresolved external effects;
- Conversation Ledger segment refs where authorized;
- source and destination runtime-incarnation refs.

The destination receives fresh workload identity, runtime attestation, EnforcementPlan, credential posture and observations.

Private content stays local by default unless explicitly required and authorized for the remote execution context.

## 16. Voice-native elasticity

The entire elasticity model is available through Focusa Doc 181 / Veragensia Doc 197 voice projection.

Examples:

```text
"Give this project another team."
"Use only two cloud workers and keep it under twenty dollars."
"Move the build work to the cloud computer."
"Pause everything expensive."
"Which team is stuck?"
"Bring the verifier into this conversation."
```

Speech does not bypass TopologyGrant, spend policy, Focusa fanout/writer rules, or human confirmation requirements.

Agent speakers in a group voice conversation remain independently attributable to their stable principals and resulting work/Receipt lineage.

## 17. Platform/runtime trust

Doc 196 trust posture is an input to placement.

A workload requiring a higher trust class cannot silently land on a lower-trust node merely because it has spare compute.

Cloud recreation, image replacement or migration creates a fresh RuntimeIncarnation and requires compatible RuntimeAttestation before governed work resumes.

## 18. Commercial abstraction

The product abstraction is not “subscribe to a chatbot.” It is closer to:

> **Attach elastic agent workforce and computing capability to your Agent Computer.**

The human may request that workforce through natural conversation rather than infrastructure controls.

Possible packaging may later distinguish personal, professional, team and vertical capability profiles, with usage dimensions such as Agent Computer time, workcell/container time, browser-runtime time, model spend and storage.

This specification does not set pricing or licensing terms.

## 19. Acceptance invariants

A future implementation of Elastic Agent Computing is valid only when:

1. a request for capability/workforce can resolve into an inspectable mixed topology;
2. full Agent Computers and headless workcells use the same Focusa authority/identity foundations rather than parallel permission models;
3. full profiles deliberately include the canonical Doc-190 first-party surfaces unless a profile declares an omission;
4. every governed workload has verified execution/enforcement posture under Docs 193/196;
5. topology expansion is bounded by a non-recursively escalating `TopologyGrant`;
6. multi-agent writes are fenced by exact scope, ResourceRefs/replicas, leases/idempotency/receipts and isolated workspaces as applicable;
7. Agent Assist uses control-lease generation/fencing, OperatorDelta and mandatory re-observation;
8. suspend/teardown preserves Workpoint/Evidence/authorized Conversation continuity and does not claim external-effect rollback;
9. resource/spend/trust scaling is bounded and observable while protecting Human Control Reserve;
10. the user can request outcomes/teams—including through voice—without manually selecting infrastructure topology;
11. stale runtime incarnations cannot retain actuation, credential or writer authority after handoff/restart.
