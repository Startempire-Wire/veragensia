# 191 — Veragensia Elastic Agent Computing and Cloud Agent Computer Runtime

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 182b (base/overlay), 182c (fleet bridge), 183 (public demo lifecycle), 190 (agent-first software), 192 (telemetry/improvement).

## 1. Decision

Veragensia is one Agent Computer architecture that can inhabit a local physical body, a full streamed cloud body, headless workcells, browser execution contexts, isolated Agent Apps, and bounded Silent Session teams.

Cloud execution is **not** defined as “spawn more headless agents.” A request for more capability is resolved into the topology that best satisfies the work, authority, resource, privacy, latency and user-interaction requirements.

```text
                         USER
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
    image_profile
    desktop_profile
    capability_profile
    app_profile
    focusa_binding
    agent_team
    storage
    lifecycle
    network_policy
    resource_budget
    telemetry_policy
}
```

The object describes the computer; it does not mint authority. Owner identity, Focusa grants, product entitlement, credential custody and application permissions remain independently verified.

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

## 5. Execution topology classes

A request may resolve into one or more of the following:

### 5.1 Full Agent Computer

A streamed or local complete desktop with the normal first-party surfaces for its profile, including Focusa binding and governed human/agent interaction.

Use when work benefits from persistent desktop state, arbitrary applications, human takeover/assist, visually rich software, or multi-application workflows.

### 5.2 Headless Workcell

A bounded execution environment without a full desktop, suitable for structured tasks, automation, builds, research pipelines, data work or other workloads that do not need persistent graphical interaction.

A workcell specializes existing Focusa ExecutionContext/affordance semantics. It MUST NOT create a parallel authority, identity or permission model.

### 5.3 Silent Session team

Daemon-native Focusa Silent Sessions provide durable background agent execution, steering, pause/resume/restart, approvals, idempotency and receipts.

Use multiple exact workloop-bound sessions for agent-team fanout rather than raw shells or independent mutable worlds.

### 5.4 Agent App

A bounded application capability, potentially native, OCI/containerized, web/UIAI-backed, headless service or remote specialist runtime. Doc 190 defines Agentability and descriptors.

### 5.5 Browser execution context

UIAI Engine may satisfy work through structured browser capabilities, semantic browser automation or authorized visual interaction without requiring a whole new Agent Computer.

## 6. Topology is an OS decision

The user should be able to ask:

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

The topology decision MUST remain inspectable and constrained by resource, privacy, authority and spend policy.

## 7. Agent interaction surfaces on a full Agent Computer

Supported full profiles SHOULD deliberately include the canonical defaults from Doc 190:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser surfaces;
- Veragensia session/shell integration.

Constrained, special-purpose and public-demo profiles MAY omit surfaces deliberately. Omission must be declared by profile; it must not silently redefine the canonical full Agent Computer composition.

## 8. Application execution classes

Do not containerize every graphical application blindly. The initial execution classes are:

| Class | Examples | Runtime |
|---|---|---|
| Desktop-native | file manager, terminal, native editor | main Agent Computer |
| Sandboxed Agent App | CRM helper, PDF processor, dev environment | OCI/container or equivalent isolation |
| Web Agent App | SaaS, vendor portal, web CRM | UIAI/browser context |
| Headless service | transforms, indexing, data/service work | workcell/service runtime |
| Remote specialist | high-resource or special platform application | separate Agent Computer/runtime |

The resolver chooses by capability, Agentability, isolation, state, latency, licensing and resources—not by a blanket “everything in Docker” rule.

## 9. Full computer use is required

Agents need three ways to accomplish work:

```text
1. Structured capability
   API / typed operation / CLI / agent protocol

2. Semantic application automation
   browser DOM/AX / accessibility / application model

3. Computer use
   see desktop / pointer / keyboard / arbitrary app
```

Prefer 1 over 2 and 2 over 3 when the resulting outcome and governance are equivalent. Level 3 remains mandatory for legacy, unfamiliar and otherwise non-automatable software.

## 10. Agent Assist Session

A full Agent Computer supports a first-class **Agent Assist Session** for authorized collaborative desktop work.

Conceptual modes:

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

Requirements:

- session binds human, agent principal, task/Workpoint, computer/runtime and authority refs;
- observation and action scope are explicit;
- human interruption/revocation is immediate where the runtime permits;
- actions use structured/semantic interfaces when available and visual control when necessary;
- resulting material changes produce appropriate Evidence/receipts;
- private content outside the authorized session scope is not ambiently captured;
- a remote-control channel is transport capability, never authority by itself.

This should feel like a highly capable human assistant joining the computer while remaining governed by Focusa and Veragensia.

## 11. Focusa work fabric and writer fencing

Elastic execution MUST build on Focusa's existing exact routing and mutation-fencing work.

The relevant routing identity includes:

```text
project_root
+ continuity_id
+ working_subpath_id
```

Multi-node/multi-agent execution requires exact scope assignment, health/capability registration, writer leases where applicable, mutation IDs, payload digests, effect receipts and isolated workspaces/worktrees.

The invariant is:

> Many agents may collaborate on one mission; they MUST NOT become many independent writers that each believe they own the same writable world.

Infrastructure lease, VM ownership, container ownership, root access or browser control never substitutes for Focusa application authority.

## 12. Elastic lifecycle

A cloud Agent Computer or workcell SHOULD support evidence-backed lifecycle transitions such as:

```text
requested
→ provisioned
→ binding
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

Filesystem checkpoint, process resume, Focusa cognitive continuity and reversal of external effects remain separate concepts. Do not describe infrastructure snapshotting as cognitive or real-world rollback.

## 13. Resource and spend governance

Elasticity is bounded.

A profile/request may define:

- default team size and burst maximum;
- CPU/memory/GPU/storage limits;
- browser/session limits;
- model/provider/token budgets;
- wall-clock duration;
- maximum active Agent Computers/workcells;
- network/egress policy;
- idle suspend/retire thresholds.

Scale-up does not imply permission expansion. Scale-down must preserve canonical work/evidence and honest uncertain/pending states.

## 14. Local/cloud continuity

Local and cloud bodies share Focusa project/continuity semantics without becoming one undifferentiated mutable machine.

A handoff SHOULD preserve:

- exact project/continuity/workpoint identity;
- relevant bounded context;
- authority/grant refs;
- input revision/workspace binding;
- evidence and outstanding blockers;
- execution ownership and cancellation state.

Private content stays local by default unless explicitly required and authorized for the remote execution context.

## 15. Commercial abstraction

The product abstraction is not “subscribe to a chatbot.” It is closer to:

> **Attach elastic agent workforce and computing capability to your Agent Computer.**

Possible packaging may later distinguish personal, professional, team and vertical capability profiles, with usage dimensions such as Agent Computer time, workcell/container time, browser-runtime time, model spend and storage.

This specification does not set pricing or licensing terms.

## 16. Acceptance invariants

A future implementation of Elastic Agent Computing is valid only when:

1. a request for capability/workforce can resolve into an inspectable mixed topology;
2. full Agent Computers and headless workcells use the same Focusa authority/identity foundations rather than parallel permission models;
3. full profiles deliberately include the canonical Doc-190 first-party surfaces unless a profile declares an omission;
4. multi-agent writes are fenced by exact scope, leases/idempotency/receipts and isolated workspaces as applicable;
5. Agent Assist binds identity, task, authority, observation/action scope and revocation;
6. suspend/teardown preserves Workpoint/Evidence continuity and does not claim external-effect rollback;
7. resource/spend scaling is bounded and observable;
8. the user can request outcomes/teams without manually selecting infrastructure topology.
