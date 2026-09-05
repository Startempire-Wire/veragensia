# 182c — Veragensia Fleet-Scale and Elastic Agent Computing Bridge

**Status:** DRAFT product direction, revised 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 / 182b / 190–198; private control-plane companion = spec 115 where applicable.

## 1. Revised fleet thesis

The earlier fleet framing emphasized “a few GUI desktops plus many headless workers.” That remains a useful infrastructure observation, but it is no longer the product abstraction.

The canonical model is **Elastic Agent Computing**:

```text
requested capability / workforce
        voice / UI / API
              |
       Veragensia resolver
              |
      bounded TopologyGrant
              |
   +----------+----------+----------------+
   |                     |                |
Full Agent           Headless         Agent App /
Computer             Workcell         browser context
   |                     |                |
   +------------- Focusa work fabric -----+
                         |
                    Silent Sessions
```

A user should request outcomes, capability or another team. Veragensia selects the execution topology under explicit identity, enforcement, trust, resource, data-locality and spend bounds.

Doc 191 is the detailed cloud/runtime specification. Doc 190 owns agent-first software/capability resolution. Doc 192 owns telemetry/improvement. Docs 193–196 own enforcement/control/resource/runtime trust. Doc 197 owns voice-native Agent Computer behavior.

## 2. Fleet node classes

### Full Agent Computer

A local or streamed complete Veragensia environment with a declared Agent Computer Profile and, for supported full profiles, the deliberately listed first-party defaults:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser/computer surfaces;
- Veragensia enforcement/control substrate;
- Voice/Conversation service bound to Focusa Spec 181;
- Veragensia native/session integration.

Use when persistent desktop state, arbitrary applications, natural human conversation, human collaboration/takeover or multi-application workflows matter.

### Headless Workcell

A bounded non-desktop execution environment for structured work, build/test, data, research or other tasks that do not require a persistent graphical desktop.

Every governed workcell gets a Doc-193 ExecutionPrincipal/WorkloadIdentity/EnforcementPlan and a Doc-196 compatible runtime attestation posture; headless never means unrestricted.

### Silent Session lane

A daemon-native Focusa execution lane for durable background agent work. Multi-agent scale uses exact scoped sessions/workloops and Focusa writer/idempotency/evidence rules, not raw shells that each assume independent authority.

### Agent App / browser context

A narrower capability may execute through an isolated Agent App, headless service or UIAI browser context without provisioning a whole computer. The resolver must prove enforceability and trust rather than rely on the app's self-description.

## 3. `os.focusa.dev` relationship

The current LinuxServer Ubuntu/KDE webtop at `os.focusa.dev` is the first crude implementation of the **Cloud Agent Computer Runtime** shape: streamed desktop, persistent `/config`, Chromium/Workforce, local Focusa daemon, tunnel and keeper lifecycle.

It remains a `public_demo` trust profile governed by Doc 183. It is not the canonical software/enforcement/voice profile for private/customer Agent Computers and must never be used as evidence that public credential handling applies elsewhere.

## 4. Provisioning flow

The old conceptual `veragensia.spawn { kind: gui|headless, agents: N }` is generalized to a capability/workforce request.

Illustrative flow:

1. User/Focusa surface requests a capability, team or explicit profile—through voice, Desktop, API or another canonical modality.
2. Focusa/Veragensia verifies the applicable `TopologyGrant` and work authority.
3. Veragensia resolves the request into a topology: full Agent Computer, workcell, Agent App, browser context, Silent Sessions, or a mixture.
4. Infrastructure adapter provisions the required runtime(s).
5. Runtime enrolls/registers with exact node/workload identity, runtime incarnation, platform/runtime attestation and resource posture.
6. Focusa binds project/continuity/workspace scope and applicable execution authority.
7. Veragensia compiles/verifies the required EnforcementPlan(s).
8. Required first-party/default surfaces and profile capabilities become ready.
9. Work runs under exact budgets, writer fencing, ResourceRefs, Evidence and Receipts.
10. On completion/idle, work settles, state checkpoints where applicable, and runtimes suspend/retire according to policy.

Infrastructure provisioning never grants application authority by itself.

## 5. TopologyGrant and recursive-spawn safety

Fleet creation is itself a capability.

Every elastic request is bounded by Doc 191 `veragensia.topology_grant.v1`, including:

- permitted runtime classes;
- maximum Agent Computers/workcells/sessions/agents;
- maximum fanout per request;
- maximum spawn depth;
- spend and wall-time limits;
- allowed regions/providers;
- data-locality policy;
- expiry/revocation;
- whether delegation is allowed.

`may_delegate` defaults to `false`.

A spawned agent/team cannot recursively create another fleet merely because its parent could. A Focusa FanoutPlan never silently multiplies infrastructure/spend permission beyond the TopologyGrant.

## 6. Mesh/networking

Tailscale/tailnet remains one candidate secure transport/mesh for private nodes, but it is an adapter rather than the Agent Computer identity or permission system.

Fleet networking MUST preserve:

- explicit node identity, workload identity and trust class;
- authenticated private routing;
- no unauthenticated public Focusa daemon exposure;
- Doc-193 least-privilege network EnforcementPlans;
- revocation and teardown;
- separation of transport capability from Focusa/application authority.

Spec 115/private control-plane contracts remain the place for private node-registry/relay details where applicable.

## 7. Scale constraints

Fleet scheduling must account for:

- RAM/CPU/GPU/storage headroom;
- protected Human Control Reserve;
- model/provider quotas and cost;
- browser/session limits;
- network/mesh limits;
- application licensing/entitlement;
- platform/workload trust requirements;
- enforcement compatibility;
- trust-class and data-locality restrictions;
- workload latency and interactivity;
- voice/audio latency requirements on full interactive profiles;
- writer/contention risk;
- suspend/resume economics.

Large agent counts are not themselves a product objective. The objective is the lowest practical cost and fragility per correctly authorized, enforced, verified outcome while preserving human control.

## 8. Agent Computer Profile examples

Profiles may express capability packages such as:

```text
executive_assistant
software_team
real_estate_assistant
accounting_team
software_factory
public_demo
private_assistant
```

A normal interactive full profile may declare `voice_complete`; headless/special-purpose profiles may not.

These names are illustrative until product/profile catalogs are versioned. They do not create architecture authority or customer-specific canon.

## 9. Agent Assist

Full Agent Computers use Doc-191/194 Agent Assist semantics:

```text
observe_only
→ guide
→ shared_control
→ delegated_control
```

but the actual primitive is:

```text
Focusa Intervention
+ ComputerControlLease generation/fencing
+ DesktopObservation
+ OperatorDeltaReceipt
+ mandatory re-observation / authority refresh
```

The session binds exact human/agent/runtime-incarnation/task/authority scope. Remote desktop access or tailnet reachability never grants the right to act.

Voice-complete profiles expose takeover, pause, stop, redirect and return-control through the same trusted control path.

## 10. Runtime identity, migration and state transfer

Fleet placement uses Doc 195.

A recreated/migrated runtime receives a new RuntimeIncarnation and fresh workload/runtime attestation. Stale process/window/browser/control/credential/writer references do not survive automatically.

Local/cloud workspace copies are explicit ResourceRef replicas with revision and writer-fencing state.

Conversation continuity may span Agent Computers through Focusa Conversation Ledger refs, but the destination does not inherit source-node microphone, credential, input or actuator permissions merely because the conversation continues.

## 11. Voice-native fleet operation

The fleet must be fully steerable through natural conversation in a `voice_complete` profile:

```text
"Give this project another team."
"Use only two cloud workers and keep it under twenty dollars."
"Move the build to the cloud computer."
"Pause the expensive workers."
"Which teams are blocked?"
"Bring the verification expert into this conversation."
```

Speech maps to the same Focusa/TopologyGrant/execution operations; it does not bypass spend, fanout, placement, writer, enforcement or approval gates.

Every speaking agent/expert in group conversation remains attributable to its stable principal and corresponding work/Evidence/Receipt lineage.

## 12. Telemetry

Fleet/runtime telemetry follows Doc 192. Default cloud-safe telemetry is bounded allowlisted metrics and structured/redacted events, not arbitrary private content capture.

Fleet scheduling may consume health/resource/cost/agentability/trust/enforcement signals without turning telemetry into architecture authority or user memory.

Conversation audio/transcript content is not fleet telemetry. Voice quality metrics must remain content-free by default.

## 13. Phases

- **P0:** existing public streamed Agent Computer proving ground (`os.focusa.dev`) under Doc 183.
- **P1:** one private/profiled Agent Computer runtime plus one headless workcell, both bound to the same Focusa project/continuity model.
- **P2:** general enforcement/workload identity/runtime-attestation foundation; capability-based topology resolver; suspend/resume lifecycle; Agent App/browser-context placement; exact node registry/mesh integration.
- **P3:** mixed-topology team requests with TopologyGrant, host scheduling, budget governance, Agent Assist and telemetry-driven optimization.
- **P4:** full voice-native orchestration, broader commercial/vertical profiles and multi-host elasticity with evidence-backed placement decisions.

Phases are evidence gates, not calendar promises.

## 14. Acceptance

A fleet implementation is acceptable only when:

1. the user can request capability/workforce—through voice or another canonical modality—without manually choosing infrastructure topology;
2. full Agent Computers and headless nodes preserve one Focusa identity/authority model;
3. full-profile defaults deliberately list Focusa Desktop, Pi, UIAI Engine/Cockpit, Veragensia enforcement/control, Voice/Conversation and session integration;
4. every governed workload has verified workload/enforcement posture;
5. recursive topology expansion cannot exceed TopologyGrant fanout/depth/spend/delegation limits;
6. multi-agent mutation uses exact scope, ResourceRefs/replicas and writer/idempotency/evidence fencing;
7. runtimes suspend/retire/migrate without losing canonical Workpoint/Evidence continuity or reviving stale runtime authority;
8. networking provides transport without becoming permission;
9. scaling is budgeted, observable and revocable while protecting Human Control Reserve;
10. privacy-tiered telemetry follows Doc 192;
11. a claimed voice-complete fleet can orchestrate/inspect/stop elastic work without keyboard/pointer dependence.

## 15. Non-goals

- one graphical desktop per agent;
- unbounded LLM/model spend;
- unauthenticated public daemons;
- requiring the user to understand containers/VMs to request more workforce;
- treating every application as its own container;
- recursive self-spawning agent fleets without explicit grant;
- treating infrastructure snapshot restore as cognitive, conversation, credential, control-lease, or external-effect rollback.
