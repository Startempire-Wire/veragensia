# 190 — Veragensia Agent-First Software and Capability Resolution Specification

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 182b (base/overlay), 182c (elastic fleet), 188 (v0.1 contracts), 191–197 (elasticity, telemetry, enforcement, control, identity, trust, voice), Focusa agent/Pi/Voice contracts, UIAI Agent-First Browser contracts.

## 1. Decision

A Veragensia Agent Computer is not a generic Linux desktop with an AI bolted on. It is a workstation intentionally composed to maximize the useful agency of governed agents while remaining a complete, understandable human computer.

Software selection therefore treats **agent operability, enforceability, attestability, and modality parity as primary platform properties**. Human usability remains mandatory, but familiarity or market share alone does not make an application a Veragensia default.

> Prefer software that exposes stable machine-operable state, typed capabilities, deterministic actions, provenance, evidence, recoverable outcomes, enforceable least privilege, and natural non-keyboard interaction. Preserve full graphical computer use as the universal fallback.

This specification establishes the software-selection doctrine and capability-resolution model. It does **not** freeze a permanent application catalog. Individual application choices remain subject to later evidence-based review.

## 2. Canonical default surfaces

Every normal full Agent Computer profile SHOULD compose these existing first-party surfaces unless the trust class, platform, entitlement, or resource budget explicitly excludes one:

1. **Focusa daemon/core** — canonical scoped cognition, continuity, governance, Workpoints, Trajectory, Context Authority, Evidence, receipts, learning, recovery, Expression, and Conversation lineage.
2. **Focusa Desktop** — default governed human work/cognition presentation surface. It is a presenter over Focusa authority, not a second cognitive store or independent product authority.
3. **Pi + Focusa Pi extension** — default/reference agent harness integration for Focusa. Pi remains a disciplined harness-edge consumer/producer; the Focusa daemon/core remains cognitive authority. Other harnesses remain supported through thin parity adapters.
4. **UIAI Engine and its Cockpit/browser/computer surfaces** — first-party browser/computer execution, observation, diagnostics, proof and control-lease surfaces. UIAI remains execution-domain authority for its runtime, not Focusa cognitive truth or constitutional architecture authority.
5. **Veragensia enforcement/control substrate** — ExecutionPrincipal, WorkloadIdentity, EnforcementPlan, secure attention, DesktopObservation, ResourceRef/runtime-incarnation binding, and Human Control Reserve from Docs 193–196.
6. **Voice / Conversation surface** — trusted audio capture/playback bound to Focusa Spec 181 and Veragensia Doc 197, making keyboard and mouse optional peripherals in a voice-complete full profile.
7. **Veragensia native shell/session integration** — host-level work context, lifecycle, containment, application composition, interruption, review and recovery.

These are defaults because they form the integrated Agent Computer substrate. They are not examples in a replaceable productivity-app list.

## 3. Agent interaction hierarchy

Agents SHOULD use the strongest truthful control surface available for an operation:

```text
1. Structured capability
   typed Focusa/UIAI operation, MCP, ACP, API, CLI, D-Bus, application protocol

2. Semantic application automation
   accessibility tree, DOM, application object model, stable semantic refs

3. Computer use
   visual desktop, pointer/keyboard-equivalent actuation, arbitrary application interaction
```

Rules:

- Level 1 is preferred when it preserves the same user-visible outcome and authority/evidence guarantees.
- Level 2 is preferred over pixel-driven control when a stable semantic model exists.
- Level 3 MUST exist so the Agent Computer can operate arbitrary and legacy software, but it is a fallback rather than the desired default path.
- A fallback MUST NOT broaden authority, data disclosure, network access, device access, credential access, or consequence scope.
- The human-visible application state and machine-operated state must converge on the same underlying work rather than becoming parallel realities.
- **Voice is an intent/input modality above this execution hierarchy.** Spoken intent should resolve to the strongest available execution path rather than simulating mouse use unnecessarily.

## 4. Agentability classes

Veragensia classifies candidate applications by the strongest normal machine surface they expose **and whether that surface can be governed in the Agent Computer substrate**.

| Class | Meaning | Typical characteristics |
|---|---|---|
| `A0_PIXEL` | Pixel-only | vision and generic input are the only practical control surface |
| `A1_SEMANTIC_UI` | Semantically accessible | accessibility tree, stable roles/names, structured GUI state |
| `A2_AUTOMATABLE` | Programmatically operable | CLI/API/D-Bus/UNO/WebDAV/scripting or equivalent |
| `A3_AGENT_NATIVE` | Agent-native | machine-readable capability discovery, typed schemas, MCP/ACP or comparable agent protocol, structured outcomes |
| `A4_VERAGENSIA_NATIVE` | Fully integrated | typed affordances, exact authority scope, stable ResourceRefs/observations, receipts/evidence, lifecycle/events, Focusa-aware governance, enforceable plan, attested software/runtime, voice/nonvisual operation where applicable |

Default-selection rule:

> Prefer `A4` → `A3` → `A2` → `A1`. Use `A0` only when no materially better option exists or the user explicitly requires that application.

Agentability is not a permanent vendor score. It is versioned per application/runtime integration and can improve or regress through adapters, software versions, enforcement support, and observed task evidence.

**An application MUST NOT receive `A4_VERAGENSIA_NATIVE` solely because it publishes a typed API or descriptor.** A4 requires Doc-193 enforceability, Doc-196 attestation/provenance, stable identity/revision semantics where consequential, and the required evidence/control contracts.

## 5. Capability-first profiles

Agent Computer Profiles SHOULD request **capabilities**, not only package names.

Instead of:

```yaml
apps:
  - browser-x
  - office-y
  - notes-z
```

prefer:

```yaml
capabilities:
  browser:
    required: true
    minimum_agentability: A3_AGENT_NATIVE
  governed_work_surface:
    preferred: focusa-desktop
  agent_harness:
    preferred: pi
  voice_conversation:
    required: true
    profile: voice_complete
  office.documents:
    minimum_agentability: A2_AUTOMATABLE
  knowledge.notes:
    minimum_agentability: A2_AUTOMATABLE
  development.editor:
    minimum_agentability: A2_AUTOMATABLE
```

The profile states what the Agent Computer must be able to do. A resolver selects a compatible implementation for the platform, trust class, entitlement, resource budget, user preference, installed capability set, enforcement support, runtime attestation, and modality requirements.

Package names MAY remain as explicit pins when exact software is required.

## 6. Agent App Resolver

The **Agent App Resolver** is a Veragensia platform responsibility.

Inputs may include:

- requested capability;
- user preference or explicit application pin;
- platform/architecture;
- Agentability Class;
- Focusa authority requirements;
- trust class and minimum platform-trust class;
- entitlement/license posture;
- software/descriptor/runtime attestation;
- local/cloud execution profile;
- CPU, memory, GPU and storage budget;
- Human Control Reserve impact;
- isolation requirements;
- Doc-193 EnforcementPlan compiler support;
- Doc-195 ResourceRef/revision semantics;
- data locality/privacy requirements;
- network policy;
- credential-broker compatibility;
- voice/nonvisual operation requirements;
- application health/compatibility evidence;
- observed reliability and accepted-outcome evidence.

The resolver returns an implementation choice plus the machine interfaces that agents and voice/UI surfaces should prefer.

A resolver decision is not permission to execute the application. Normal Focusa/UIAI authority and consequence checks still apply.

### 6.1 Hard governed-execution gate

A selected application/runtime is eligible for **governed execution** only when:

```text
software/descriptor identity verified
+ compatible runtime attestation
+ required operation/capability contracts understood
+ Doc-193 EnforcementPlan compiles
+ enforcement posture verifies
+ required ResourceRefs/observations/control lease available
+ entitlement/authority remain valid
```

If the application can run only with ambient access broader than the grant, the resolver must either:

- place it in a stronger isolation context/dedicated Agent Computer;
- downgrade the effective Agentability/trust posture;
- request explicit broader authority where legitimately needed;
- or return `unsupported_enforcement`.

It MUST NOT label an unrestricted same-user process governed merely because the app descriptor says it is.

## 7. Agent App Descriptor extension

The `veragensia.agent_app.v1` concept allows Focusa and Veragensia to understand how an application is operated, what it claims, and how that claim is enforced and verified.

Illustrative shape:

```yaml
schema: veragensia.agent_app.v1
id: app:example
version: 1

provenance:
  publisher_ref:
  software_digest_ref:
  descriptor_digest:
  signature_ref:
  capability_schema_digest:
  agentability_evidence_refs: []

runtime:
  type: native | oci | web | remote
  image_digest: null
  minimum_platform_trust: T1_DEVELOPER

human:
  desktop: true
  voice_operable: true
  nonvisual_operable: true

agent:
  claimed_agentability: A3_AGENT_NATIVE
  effective_agentability: A3_AGENT_NATIVE
  preferred_interface_order:
    - typed_capability
    - cli
    - accessibility
    - computer_use
  interfaces:
    typed_capability:
      protocol: mcp
    cli:
      command: example
    accessibility:
      protocol: at-spi
    computer_use:
      supported: true
      role: fallback

capabilities:
  - object.read
  - object.create
  - object.edit

focusa:
  exact_scope_required: true
  evidence_supported: true
  mutation_receipts: true

identity:
  resource_ref_support: true
  revision_preconditions: true

enforcement:
  compiler_profile_ref:
  ambient_home_required: false
  network_policy_ref: default-deny
  accessibility_scope_required: true
  device_capability_refs: []

resources:
  cpu: 1
  memory_mb: 512

filesystem:
  mounts: []

network:
  policy_ref: default-deny

credentials:
  broker_refs: []

voice:
  semantic_operation_projection: true
  direct_audio_access_required: false
```

Descriptors advertise affordances; they do not grant them. Claimed Agentability is evidence input. **Effective Agentability is determined by the trusted Veragensia resolver from attested software plus real integration evidence.**

## 8. Default first-party composition

The following relationship is normative:

```text
                          VERAGENSIA
                        Agent Computer
                              |
         +--------------------+--------------------+
         |                    |                    |
 Focusa Desktop        UIAI Cockpit          Voice / Audio UI
 governed work         browser/computer      natural conversation
 presentation          execution/proof       + audit navigation
         |                    |                    |
         +--------------------+--------------------+
                              |
                      Focusa daemon/core
             cognition · authority · conversation
                              |
                         Pi harness
                  reference agent runtime
                              |
                 other thin agent adapters
                              |
              Veragensia enforcement substrate
                              |
                 Linux / apps / workcells
```

The diagram is a responsibility map, not a process topology requirement. Pi, UIAI and voice services may call Focusa through generated interfaces rather than being children of one process.

## 9. Pi position

Pi is fundamental to Focusa's current agent experience and MUST be treated accordingly in Veragensia planning.

- Pi is the **reference/default Focusa-aware harness** for an Agent Computer.
- The Focusa Pi extension supplies typed tools, skills/runbooks, scope/authority hooks, Workpoint/Trajectory/evidence access, metacognition and recovery surfaces.
- Pi does not become Focusa's reducer, canonical memory, ontology owner, conversation owner, or independent cognitive authority.
- Non-Pi agents remain first-class supported consumers through the Focusa Agent Adapter Contract and generated capability surfaces.
- Veragensia must not make the OS architecture dependent on Pi-only hidden state; all canonical state and Conversation Ledger semantics stay in Focusa-owned contracts.

This preserves both truths: Pi is fundamental to the reference Focusa system, and Focusa remains portable across agent harnesses.

## 10. Focusa Desktop position

Focusa Desktop is the default human-facing governed work surface on a full Agent Computer.

It SHOULD expose, through the existing Focusa presenter/operation contracts:

- selected project/continuity;
- Trajectory and current Workpoint;
- Work Surfaces / Mission Canvas / Work Rail as applicable;
- agent activity and Silent Sessions;
- approvals and authority posture;
- Evidence, receipts, review and recovery;
- capability/application availability;
- Voice/Conversation participant and transcript/audit navigation;
- degraded/stale/blocked states honestly.

Focusa Desktop MUST NOT evaluate or invent authority independently of the Focusa execution guard, write reducer/storage state directly, or become a second product/license/conversation authority.

## 11. UIAI position

UIAI Engine remains the first-party browser and browser-adjacent execution system. Veragensia SHOULD consume its existing Agent-First Browser contracts rather than inventing a parallel browser automation layer.

In particular, Veragensia should preserve UIAI's existing model of:

- compact capability discovery;
- versioned browser observations;
- observation-bound actions;
- structured semantic references;
- Focusa-directed verification;
- provenance/influence controls;
- execution capsules and evidence handles;
- human oversight/takeover through Cockpit/FPV where authorized;
- control-lease generation/fencing and mandatory re-observation after takeover.

Doc 194 generalizes the observation/control principles to the desktop. Browser visual computer use remains available when structured and semantic actuators cannot complete the task.

Voice commands initiating browser/computer work route into these same UIAI operations and controls; voice never creates a second actuator authority.

## 12. Software catalog policy

Veragensia WILL maintain an **Agent-First Software Catalog**, but the catalog is intentionally not frozen by this specification.

Each candidate record SHOULD capture:

- capability families;
- claimed and effective Agentability Class;
- machine interfaces;
- human desktop quality;
- voice/nonvisual operability;
- file/data portability;
- Linux/Agent Computer compatibility;
- local/cloud suitability;
- enforceability profile and negative-isolation evidence;
- platform-trust/runtime-attestation requirements;
- stable object/ResourceRef/revision semantics;
- control-lease/observation compatibility for GUI control;
- isolation model;
- credential model;
- evidence/provenance support;
- resource requirements and Human Control Reserve impact;
- licensing/distribution constraints;
- known failure/degraded modes.

Software evaluation must distinguish:

```text
popular software
!=
best software for an Agent Computer
```

```text
"has AI features"
!=
"is agent-operable"
```

```text
"has a typed API"
!=
"can be governed safely on this Agent Computer"
```

The later software-selection pass may change individual defaults without changing this architecture.

## 13. Cloud Agent Computers

Full Cloud Agent Computers SHOULD use the same capability/profile model as local machines. Cloud-specific differences belong in resolver inputs and runtime policy, not in a separate application ontology.

A cloud profile may select:

- desktop-native application in the main streamed environment;
- isolated OCI Agent App;
- browser/web application through UIAI;
- headless structured service;
- remote specialist computer.

The user asks for capability or workforce—by voice or any other modality. Veragensia chooses the topology under Doc 191's TopologyGrant and placement policy.

## 14. Voice-complete software requirement

A full `voice_complete` profile must be able to achieve supported outcomes without requiring the user to operate application-specific keyboard/mouse mechanics.

This does **not** mean every third-party application needs native speech support.

Veragensia may satisfy voice parity through:

```text
canonical typed operation
→ semantic application adapter
→ UIAI/accessibility automation
→ governed visual computer use
```

The requirement is **outcome parity**, not vendor-provided speech UI.

Catalog evaluation SHOULD record `voice_task_success_rate` and `keyboard_mouse_fallback_rate` for representative tasks.

## 15. Telemetry and improvement

Agentability itself is measurable. Privacy-safe telemetry MAY compare:

- structured-interface success rate;
- semantic-automation success rate;
- visual fallback rate;
- voice-task success rate;
- keyboard/mouse fallback rate in voice-complete testing;
- retries and recovery rate;
- average model/tool cost per accepted outcome;
- operator takeover/intervention rate;
- evidence completeness;
- latency and resource cost.

The objective is not to maximize automation for its own sake. It is to reduce the total cost and fragility of correctly authorized, verified work while preserving human control.

## 16. Acceptance invariants

A future implementation satisfies this direction only when:

1. Agent Computer Profiles can request capabilities independently of exact packages.
2. Installed applications can advertise versioned agent-operability metadata without self-authorizing their trust score.
3. Agents can prefer structured/semantic surfaces and fall back to computer use without authority expansion.
4. Governed execution requires a verified Doc-193 EnforcementPlan and compatible WorkloadIdentity/runtime attestation.
5. A4 Agentability cannot be achieved by descriptor/API claim alone.
6. Focusa Desktop is available as the default governed work presentation on supported full profiles.
7. Pi is available as the default/reference Focusa-aware harness on supported profiles, without making canonical state Pi-private.
8. UIAI remains the first-party browser/computer execution/proof surface and existing Agent-First Browser/control contracts are reused.
9. A `voice_complete` full profile can complete representative application workflows without keyboard/mouse dependence.
10. The software catalog can evolve without redefining Focusa authority, Veragensia profiles, or the application ontology.
11. The human can still install/use ordinary software even when it is low-agentability; Veragensia reports the limitation rather than pretending structured or voice-native control exists.

## 17. Deferred software-selection work

A later dedicated evaluation will select and benchmark the best default software for areas including development, shell, office/document work, knowledge, communications, meetings, CRM/business operations, media, data analysis and vertical applications.

That evaluation should use this spec's criteria and real agent/voice task evidence. No candidate named during architecture discussion is canonically selected merely by mention.
