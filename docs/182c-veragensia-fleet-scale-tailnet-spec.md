# 182c — Veragensia Fleet-Scale and Elastic Agent Computing Bridge

**Status:** DRAFT product direction, revised 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 / 182b / 190 / 191 / 192; private control-plane companion = spec 115 where applicable.

## 1. Revised fleet thesis

The earlier fleet framing emphasized “a few GUI desktops plus many headless workers.” That remains a useful infrastructure observation, but it is no longer the product abstraction.

The canonical model is **Elastic Agent Computing**:

```text
requested capability / workforce
            |
       Veragensia resolver
            |
   +--------+---------+----------------+
   |                  |                |
Full Agent        Headless         Agent App /
Computer          Workcell         browser context
   |                  |                |
   +---------- Focusa work fabric -----+
                  |
             Silent Sessions
```

A user should request outcomes, capability or another team. Veragensia selects the execution topology.

Doc 191 is the detailed cloud/runtime specification. Doc 190 owns agent-first software/capability resolution. Doc 192 owns telemetry/improvement.

## 2. Fleet node classes

### Full Agent Computer

A local or streamed complete Veragensia environment with a declared Agent Computer Profile and, for supported full profiles, the deliberately listed first-party defaults:

- Focusa daemon/core;
- Focusa Desktop;
- Pi + Focusa Pi extension as the reference/default Focusa-aware harness;
- UIAI Engine + Cockpit/browser surfaces;
- Veragensia native/session integration.

Use when persistent desktop state, arbitrary applications, human collaboration/takeover or multi-application workflows matter.

### Headless Workcell

A bounded non-desktop execution environment for structured work, build/test, data, research or other tasks that do not require a persistent graphical desktop.

### Silent Session lane

A daemon-native Focusa execution lane for durable background agent work. Multi-agent scale uses exact scoped sessions/workloops and Focusa writer/idempotency/evidence rules, not raw shells that each assume independent authority.

### Agent App / browser context

A narrower capability may execute through an isolated Agent App, headless service or UIAI browser context without provisioning a whole computer.

## 3. `os.focusa.dev` relationship

The current LinuxServer Ubuntu/KDE webtop at `os.focusa.dev` is the first crude implementation of the **Cloud Agent Computer Runtime** shape: streamed desktop, persistent `/config`, Chromium/Workforce, local Focusa daemon, tunnel and keeper lifecycle.

It remains a `public_demo` trust profile governed by Doc 183. It is not the canonical software profile for private/customer Agent Computers and must never be used as evidence that public credential handling applies elsewhere.

## 4. Provisioning flow

The old conceptual `veragensia.spawn { kind: gui|headless, agents: N }` is generalized to a capability/workforce request.

Illustrative flow:

1. User/Focusa surface requests a capability, team or explicit profile.
2. Veragensia resolves the request into a topology: full Agent Computer, workcell, Agent App, browser context, Silent Sessions, or a mixture.
3. Infrastructure adapter provisions the required runtime(s).
4. Runtime enrolls/registers with exact identity/trust/resource posture.
5. Focusa binds project/continuity/workspace scope and applicable execution authority.
6. Required first-party/default surfaces and profile capabilities become ready.
7. Work runs under exact budgets, writer fencing, Evidence and receipts.
8. On completion/idle, work settles, state checkpoints where applicable, and runtimes suspend/retire according to policy.

Infrastructure provisioning never grants application authority by itself.

## 5. Mesh/networking

Tailscale/tailnet remains one candidate secure transport/mesh for private nodes, but it is an adapter rather than the Agent Computer identity or permission system.

Fleet networking MUST preserve:

- explicit node identity and trust class;
- authenticated private routing;
- no unauthenticated public Focusa daemon exposure;
- least-privilege network policy;
- revocation and teardown;
- separation of transport capability from Focusa/application authority.

Spec 115/private control-plane contracts remain the place for private node-registry/relay details where applicable.

## 6. Scale constraints

Fleet scheduling must account for:

- RAM/CPU/GPU/storage headroom;
- model/provider quotas and cost;
- browser/session limits;
- network/mesh limits;
- application licensing/entitlement;
- trust-class and data-locality restrictions;
- workload latency and interactivity;
- writer/contention risk;
- suspend/resume economics.

Large agent counts are not themselves a product objective. The objective is the lowest practical cost and fragility per correctly authorized, verified outcome.

## 7. Agent Computer Profile examples

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

These names are illustrative until product/profile catalogs are versioned. They do not create architecture authority or customer-specific canon.

## 8. Agent Assist

Full Agent Computers may support the Doc-191 Agent Assist Session modes:

```text
observe_only
→ guide
→ shared_control
→ delegated_control
```

The session binds exact human/agent/runtime/task/authority scope. Remote desktop access or tailnet reachability never grants the right to act.

## 9. Telemetry

Fleet/runtime telemetry follows Doc 192. Default cloud-safe telemetry is bounded metrics and structured/redacted events, not arbitrary private content capture.

Fleet scheduling may consume health/resource/cost/agentability signals without turning telemetry into architecture authority or user memory.

## 10. Phases

- **P0:** existing public streamed Agent Computer proving ground (`os.focusa.dev`) under Doc 183.
- **P1:** one private/profiled Agent Computer runtime plus one headless workcell, both bound to the same Focusa project/continuity model.
- **P2:** capability-based topology resolver, suspend/resume lifecycle, Agent App/browser-context placement, and exact node registry/mesh integration.
- **P3:** mixed-topology team requests, host scheduling, budget governance, Agent Assist and telemetry-driven optimization.
- **P4:** broader commercial/vertical profiles and multi-host elasticity with evidence-backed placement decisions.

Phases are evidence gates, not calendar promises.

## 11. Acceptance

A fleet implementation is acceptable only when:

1. the user can request capability/workforce without manually choosing infrastructure topology;
2. full Agent Computers and headless nodes preserve one Focusa identity/authority model;
3. full-profile defaults deliberately list Focusa Desktop, Pi, UIAI Engine/Cockpit and Veragensia integration;
4. multi-agent mutation uses exact scope and writer/idempotency/evidence fencing;
5. runtimes suspend/retire without losing canonical Workpoint/Evidence continuity;
6. networking provides transport without becoming permission;
7. scaling is budgeted, observable and revocable;
8. privacy-tiered telemetry follows Doc 192.

## 12. Non-goals

- one graphical desktop per agent;
- unbounded LLM/model spend;
- unauthenticated public daemons;
- requiring the user to understand containers/VMs to request more workforce;
- treating every application as its own container;
- treating infrastructure snapshot restore as cognitive or external-effect rollback.
