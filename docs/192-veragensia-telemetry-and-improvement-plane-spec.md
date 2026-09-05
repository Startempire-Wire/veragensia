# 192 — Veragensia Telemetry and Improvement Plane Specification

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 190 (agent-first software), 191 (Elastic Agent Computing), 193–197 (enforcement, control, identity, trust, voice), Focusa evidence/reliability/telemetry and Voice/Conversation contracts.

## 1. Decision

Every Veragensia execution body—physical Agent Computer, Cloud Agent Computer, workcell, Agent App, browser context and Silent Session—SHOULD participate in one privacy-tiered **Veragensia Telemetry Plane**.

The plane exists to improve reliability, agentability, voice usability, cost, responsiveness and product quality. It is **not** permission for ambient surveillance or indiscriminate upload of user activity.

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
    numerical / bounded / allowlisted dimensions

EVENTS
    structured / redacted / purpose-bound

TRACES
    sampled / task-correlated / bounded

ARTIFACTS
    explicit Evidence references

CONVERSATION CONTENT
    separate Focusa Conversation Ledger domain

PRIVATE CONTENT
    local by default
```

A higher-detail class never inherits permission merely because a lower-detail class is allowed.

**Conversation Ledger content is not telemetry.** Spoken audio, transcripts, agent utterance text and user conversation history remain governed by Focusa Doc 181 / Veragensia Doc 197 privacy/retention policy unless an explicit diagnostic/Evidence flow authorizes otherwise.

## 4. Node and computer telemetry

Possible bounded node metrics include:

- CPU, memory and process pressure;
- disk headroom and storage growth;
- battery, thermal and power state where available;
- network quality and transfer volume;
- boot/resume and readiness latency;
- shell/session responsiveness;
- crash/restart counts;
- local vs cloud execution placement;
- protected Human Control Reserve headroom;
- enforcement/attestation degraded-control counts.

Do not collect unrelated filenames, document contents, clipboard contents, process arguments, conversation text or audio merely to measure resource use.

## 5. Desktop telemetry

Possible structured desktop events/metrics include:

- application launch/exit/crash class;
- workspace/surface transition counts;
- UI responsiveness;
- notification volume;
- Agent Assist start/stop/mode changes;
- agent/human control-contention events;
- control-lease fencing/stale-action counts;
- structured-interface vs semantic vs visual-computer-use selection;
- secure-attention availability/latency;
- DesktopObservation stale/resync rates.

Desktop telemetry SHOULD identify application/capability class rather than capture private window contents, titles, URLs or arbitrary object labels.

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
- structured/semantic/visual execution mix;
- EnforcementPlan compilation/failure class;
- workload attestation mismatch counts;
- stale ResourceRef/runtime-incarnation rejection counts.

Raw prompts, chain-of-thought, arbitrary page contents, full command arguments, private artifacts and conversation text are not telemetry by default.

## 7. Cloud/runtime telemetry

Possible infrastructure metrics include:

- provision and warmup latency;
- active, idle and suspended Agent Computer time;
- workcell/container/runtime seconds;
- bandwidth and storage consumption;
- scale-up/scale-down events;
- TopologyGrant denial/fanout posture;
- checkpoint/suspend/resume latency;
- runtime-incarnation transitions;
- attestation readiness/failure class;
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
- `mean_latency_per_accepted_outcome`;
- `enforcement_plan_success_rate`;
- `stale_target_rejection_rate`.

A popular application that repeatedly forces fragile pixel interaction or broad unenforceable ambient authority can therefore score worse than a less familiar application with reliable typed interfaces and enforceable boundaries.

## 10. Voice quality telemetry

Voice-native quality from Doc 197 MAY be measured through bounded content-free metrics such as:

- `voice_task_success_rate`;
- `keyboard_mouse_fallback_rate` in voice-complete tests;
- ASR hypothesis correction rate;
- high-confidence/low-confidence distribution;
- speaker-attribution uncertainty rate;
- end-of-turn detection latency;
- barge-in detection/stop latency;
- TTS first-audio latency;
- interrupted-spoken-output rate;
- secure-spoken-confirmation latency/failure class;
- Conversation Ledger persistence/recovery availability;
- group-conversation speaker-attribution success rate.

Telemetry MUST NOT include, merely to compute these metrics:

```text
raw microphone audio
transcript text
agent spoken response text
speaker voiceprints
names extracted from conversation
conversation semantic topics
```

Those are private conversation content or identity data and require a separately authorized purpose.

## 11. Content boundary

A cloud service may learn:

```text
agent browser action latency = 840 ms
structured browser action = success
voice barge-in latency = 120 ms
speaker attribution = uncertain
verification = passed
```

without receiving:

```text
full page content
private email/document text
credential material
arbitrary screenshots
raw audio
transcript text
agent utterance text
private filenames or URLs
```

unless the content is explicitly required by an authorized task, Evidence path, troubleshooting session or opt-in diagnostic collection.

## 12. Telemetry Anti-Exfiltration Firewall

A metrics pipeline can leak private data even when it claims to collect "only labels." Veragensia therefore treats telemetry schema itself as an egress boundary.

### 12.1 Field allowlists

Every telemetry schema defines an exact allowlist of fields/dimensions. Unknown keys are dropped or blocked before egress.

### 12.2 Forbidden label classes

Generic telemetry labels MUST NOT contain:

- filesystem paths or filenames;
- arbitrary URLs/query strings/origins unless a specific coarse origin class is authorized;
- document/window titles;
- raw project/customer/user names;
- prompt/transcript/utterance fragments;
- model-generated arbitrary strings;
- credential/token/session values;
- email addresses/phone numbers;
- speaker names or voiceprints;
- arbitrary error payload bodies.

Use stable bounded enums/classes or local opaque aggregation IDs where the metric truly requires grouping.

### 12.3 Cardinality ceilings

Every remote metric family declares:

```yaml
maximum_dimensions:
maximum_distinct_values_per_window:
high_cardinality_policy:
```

Unbounded user-content-derived labels are rejected.

### 12.4 Hashing is not anonymization by fiat

A hash of a filename, URL, transcript, email, voiceprint or private ID is still derived from private data and may remain linkable or guessable. Hashing does not automatically make a field telemetry-safe.

### 12.5 Local aggregation first

Prefer:

```text
raw local observation
→ local classification/aggregation
→ bounded metric
→ optional cloud coordination
```

rather than uploading per-event private identifiers and aggregating centrally.

## 13. Data minimization and redaction

Telemetry collectors MUST:

- collect the minimum fields required for a declared purpose;
- enforce schema field allowlists before egress;
- avoid secret values, credentials, tokens and authentication material;
- avoid raw query/body capture when bounded status/latency is enough;
- avoid high-cardinality arbitrary strings;
- use coarse/bounded classifications when identity is unnecessary;
- preserve tenant/project/trust-class isolation;
- bound retention;
- support deletion/retention policy consistent with the owning product contract;
- mark sampled, inferred, stale or degraded data honestly;
- distinguish telemetry from required security/audit/Evidence records.

## 14. Local-first telemetry reduction

Where practical, nodes SHOULD reduce high-volume raw observations locally into bounded metrics/events before cloud coordination.

For example:

```text
local raw action timings
→ local aggregate
→ bounded metric/event
→ optional cloud comparison
```

and:

```text
local ASR utterance results
→ correction count + confidence bucket
→ bounded voice metric
→ transcript/audio stay in Conversation Ledger domain
```

Raw local traces may remain available for authorized debugging without becoming normal cloud telemetry.

## 15. Evidence and architecture boundary

Telemetry can identify candidate regressions or opportunities. Promotion path:

```text
measurement
→ Evidence
→ proposed improvement
→ operator/delegated architecture decision
→ implementation
```

Telemetry, A/B results, customer behavior, benchmarks or model recommendations do not independently mint canonical architecture authority.

## 16. User and operator controls

Profiles SHOULD expose understandable controls for:

- telemetry level/policy;
- diagnostic trace opt-in;
- local-only vs cloud-coordinated metrics where supported;
- current collection health;
- retained local diagnostic artifacts;
- clearing non-required local diagnostic caches;
- conversation/audio retention separately from telemetry.

Required audit/Evidence/security records and Focusa Conversation Ledger retention may have separate rules; those boundaries must be explicit rather than hidden under a generic telemetry toggle.

## 17. Failure posture

Telemetry failure MUST NOT:

- block ordinary human desktop or voice use unless the missing signal is itself safety-critical;
- grant broader authority;
- cause execution to be reported as complete;
- silently switch to broader content capture;
- delete canonical Focusa state, Conversation Ledger state, or user work;
- disable the Human Control Reserve.

A telemetry-dependent optimization can degrade or disable while the core Agent Computer remains usable.

## 18. Acceptance invariants

A future telemetry implementation satisfies this direction only when:

1. metrics/events/traces/artifacts/conversation/private-content classes are technically distinguishable;
2. private and conversation content is local by default and not collected merely for convenience;
3. remote telemetry schemas enforce field allowlists and cardinality ceilings;
4. filenames, URLs, transcript/audio, prompts and arbitrary model strings cannot leak through generic metric labels;
5. local, cloud, workcell, Agent App, UIAI and Silent Session activity can be correlated through bounded execution references without merging authority domains;
6. Agentability and cost-per-accepted-outcome can be compared across software/runtime choices;
7. voice quality can be measured without exporting conversation content;
8. Focusa cognitive/conversation signals are projected from Focusa-owned contracts rather than redefined;
9. telemetry-derived proposals remain evidence until valid architecture/product authority promotes them;
10. telemetry failure degrades honestly without pretending work succeeded or expanding collection.
