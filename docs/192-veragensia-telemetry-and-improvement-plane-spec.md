# 192 — Veragensia Telemetry and Improvement Plane Specification

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 190 (agent-first software), 191 (Elastic Agent Computing), Focusa evidence/reliability/telemetry contracts.

## 1. Decision

Every Veragensia execution body—physical Agent Computer, Cloud Agent Computer, workcell, Agent App, browser context and Silent Session—SHOULD participate in one privacy-tiered **Veragensia Telemetry Plane**.

The plane exists to improve reliability, agentability, cost, responsiveness and product quality. It is **not** permission for ambient surveillance or indiscriminate upload of user activity.

> Cloud coordinates. Node decides. Receipts prove. Private state stays local.

Telemetry MUST preserve that control-plane principle.

## 2. Improvement loop

The desired product loop is:

```text
Telemetry
→ Pattern
→ Evidence
→ Improvement Candidate
→ Spec / br item
→ Implementation
→ Release
→ Telemetry comparison
```

Operational measurements become evidence for improvement; they do not silently become architecture decisions, user memory or canonical facts.

## 3. Telemetry classes

The default privacy hierarchy is:

```text
METRICS
    numerical / bounded / cloud-safe by policy

EVENTS
    structured / redacted / purpose-bound

TRACES
    sampled / task-correlated / bounded

ARTIFACTS
    explicit Evidence references

PRIVATE CONTENT
    local by default
```

A higher-detail class never inherits permission merely because a lower-detail class is allowed.

## 4. Node and computer telemetry

Possible bounded node metrics include:

- CPU, memory and process pressure;
- disk headroom and storage growth;
- battery, thermal and power state where available;
- network quality and transfer volume;
- boot/resume and readiness latency;
- shell/session responsiveness;
- crash/restart counts;
- local vs cloud execution placement.

Do not collect unrelated filenames, document contents, clipboard contents or process arguments merely to measure resource use.

## 5. Desktop telemetry

Possible structured desktop events/metrics include:

- application launch/exit/crash class;
- workspace/surface transition counts;
- UI responsiveness;
- notification volume;
- Agent Assist start/stop/mode changes;
- agent/human control-contention events;
- structured-interface vs visual-computer-use selection.

Desktop telemetry SHOULD identify application/capability class rather than capture private window contents.

## 6. Agent execution telemetry

Possible bounded agent metrics include:

- queue delay;
- run/session duration;
- model/provider class and approved usage accounting;
- token/tool invocation counts;
- retries and recovery paths;
- completion/verification status;
- Evidence coverage;
- operator interventions/takeovers;
- cancellation latency;
- structured/semantic/visual execution mix.

Raw prompts, chain-of-thought, arbitrary page contents and private artifacts are not telemetry by default.

## 7. Cloud/runtime telemetry

Possible infrastructure metrics include:

- provision and warmup latency;
- active, idle and suspended Agent Computer time;
- workcell/container/runtime seconds;
- bandwidth and storage consumption;
- scale-up/scale-down events;
- checkpoint/suspend/resume latency;
- resource-limit and budget events;
- cost attribution by bounded execution context.

Infrastructure usage telemetry MUST NOT imply that the infrastructure provider or orchestrator becomes work or architecture authority.

## 8. Focusa telemetry projection

Veragensia SHOULD reuse Focusa-owned operational signals rather than creating a second cognitive telemetry authority.

Useful projections may include:

- Workpoint recovery success/failure;
- project/scope conflict and routing ambiguity;
- writer-lease contention;
- daemon routing health;
- secondary cognition/reflex activity counts;
- Silent Session state transitions;
- Evidence coverage and verification posture;
- receipt settlement/reconciliation failures;
- constrained/LowMem transitions;
- Context Authority blocked/allowed classes;
- degraded-cognition or stale-client states.

Focusa remains owner of the underlying cognitive/operational semantics.

## 9. Agentability telemetry

Doc 190 introduces Agentability Classes. The telemetry plane SHOULD measure whether software is actually helping agents.

Candidate metrics:

- `structured_interface_success_rate`;
- `semantic_automation_success_rate`;
- `visual_fallback_rate`;
- `fallback_recovery_rate`;
- `operator_takeover_rate`;
- `mean_retries_per_accepted_outcome`;
- `evidence_complete_rate`;
- `mean_cost_per_accepted_outcome`;
- `mean_latency_per_accepted_outcome`.

A popular application that repeatedly forces fragile pixel interaction can therefore score worse than a less familiar application with reliable typed interfaces.

## 10. Content boundary

A cloud service may learn:

```text
agent browser action latency = 840 ms
structured browser action = success
verification = passed
```

without receiving:

```text
full page content
private email/document text
credential material
arbitrary screenshots
```

unless the content is explicitly required by an authorized task, Evidence path, troubleshooting session or opt-in diagnostic collection.

## 11. Data minimization and redaction

Telemetry collectors MUST:

- collect the minimum fields required for a declared purpose;
- avoid secret values, credentials, tokens and authentication material;
- avoid raw query/body capture when bounded status/latency is enough;
- redact or hash identifiers where identity is unnecessary;
- preserve tenant/project/trust-class isolation;
- bound retention;
- support deletion/retention policy consistent with the owning product contract;
- mark sampled, inferred, stale or degraded data honestly.

A hash of private content is still derived from private content and requires a justified purpose; hashing is not a universal privacy bypass.

## 12. Local-first telemetry reduction

Where practical, nodes SHOULD reduce high-volume raw observations locally into bounded metrics/events before cloud coordination.

For example:

```text
local raw action timings
→ local aggregate
→ bounded metric/event
→ optional cloud comparison
```

Raw local traces may remain available for authorized debugging without becoming normal cloud telemetry.

## 13. Evidence and architecture boundary

Telemetry can identify candidate regressions or opportunities. Promotion path:

```text
measurement
→ Evidence
→ proposed improvement
→ operator/delegated architecture decision
→ implementation
```

Telemetry, A/B results, customer behavior, benchmarks or model recommendations do not independently mint canonical architecture authority.

## 14. User and operator controls

Profiles SHOULD expose understandable controls for:

- telemetry level/policy;
- diagnostic trace opt-in;
- local-only vs cloud-coordinated metrics where supported;
- current collection health;
- retained local diagnostic artifacts;
- clearing non-required local diagnostic caches.

Required audit/evidence records and security logs may have separate retention rules; those boundaries must be explicit rather than hidden under a generic telemetry toggle.

## 15. Failure posture

Telemetry failure MUST NOT:

- block ordinary human desktop use unless the missing signal is itself safety-critical;
- grant broader authority;
- cause execution to be reported as complete;
- silently switch to broader content capture;
- delete canonical Focusa state or user work.

A telemetry-dependent optimization can degrade or disable while the core Agent Computer remains usable.

## 16. Acceptance invariants

A future telemetry implementation satisfies this direction only when:

1. metrics/events/traces/artifacts/private-content classes are technically distinguishable;
2. private content is local by default and not collected merely for convenience;
3. local, cloud, workcell, Agent App, UIAI and Silent Session activity can be correlated through bounded execution references without merging authority domains;
4. Agentability and cost-per-accepted-outcome can be compared across software/runtime choices;
5. Focusa cognitive signals are projected from Focusa-owned contracts rather than redefined;
6. telemetry-derived proposals remain evidence until valid architecture/product authority promotes them;
7. telemetry failure degrades honestly without pretending work succeeded or expanding collection.
