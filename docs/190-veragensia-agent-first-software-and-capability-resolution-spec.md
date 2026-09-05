# 190 — Veragensia Agent-First Software and Capability Resolution Specification

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Companions:** 182 (product), 182b (base/overlay), 182c (elastic fleet), 188 (v0.1 contracts), Focusa agent/Pi contracts, UIAI Agent-First Browser contracts.

## 1. Decision

A Veragensia Agent Computer is not a generic Linux desktop with an AI bolted on. It is a workstation intentionally composed to maximize the useful agency of governed agents while remaining a complete, understandable human computer.

Software selection therefore treats **agent operability as a primary platform property**. Human usability remains mandatory, but familiarity or market share alone does not make an application a Veragensia default.

> Prefer software that exposes stable machine-operable state, typed capabilities, deterministic actions, provenance, evidence, and recoverable outcomes. Preserve full graphical computer use as the universal fallback.

This specification establishes the software-selection doctrine and capability-resolution model. It does **not** freeze a permanent application catalog. Individual application choices remain subject to later evidence-based review.

## 2. Canonical default surfaces

Every normal full Agent Computer profile SHOULD compose these existing first-party surfaces unless the trust class, platform, entitlement, or resource budget explicitly excludes one:

1. **Focusa daemon/core** — canonical scoped cognition, continuity, governance, Workpoints, Trajectory, Context Authority, Evidence, receipts, learning and recovery.
2. **Focusa Desktop** — default governed human work/cognition presentation surface. It is a presenter over Focusa authority, not a second cognitive store or independent product authority.
3. **Pi + Focusa Pi extension** — default/reference agent harness integration for Focusa. Pi remains a disciplined harness-edge consumer/producer; the Focusa daemon/core remains cognitive authority. Other harnesses remain supported through thin parity adapters.
4. **UIAI Engine and its Cockpit/browser surfaces** — first-party browser/computer execution, observation, diagnostics and proof surfaces. UIAI remains execution-domain authority for its runtime, not Focusa cognitive truth or constitutional architecture authority.
5. **Veragensia native shell/session integration** — host-level work context, lifecycle, containment, application composition, interruption, review and recovery.

These are defaults because they form the integrated Agent Computer substrate. They are not examples in a replaceable productivity-app list.

## 3. Agent interaction hierarchy

Agents SHOULD use the strongest truthful control surface available for an operation:

```text
1. Structured capability
   typed Focusa/UIAI operation, MCP, ACP, API, CLI, D-Bus, application protocol

2. Semantic application automation
   accessibility tree, DOM, application object model, stable semantic refs

3. Computer use
   visual desktop, pointer, keyboard, arbitrary application interaction
```

Rules:

- Level 1 is preferred when it preserves the same user-visible outcome and authority/evidence guarantees.
- Level 2 is preferred over pixel-driven control when a stable semantic model exists.
- Level 3 MUST exist so the Agent Computer can operate arbitrary and legacy software, but it is a fallback rather than the desired default path.
- A fallback MUST NOT broaden authority, data disclosure, network access, or consequence scope.
- The human-visible application state and machine-operated state must converge on the same underlying work rather than becoming parallel realities.

## 4. Agentability classes

Veragensia classifies candidate applications by the strongest normal machine surface they expose.

| Class | Meaning | Typical characteristics |
|---|---|---|
| `A0_PIXEL` | Pixel-only | vision, pointer and keyboard are the only practical control surface |
| `A1_SEMANTIC_UI` | Semantically accessible | accessibility tree, stable roles/names, structured GUI state |
| `A2_AUTOMATABLE` | Programmatically operable | CLI/API/D-Bus/UNO/WebDAV/scripting or equivalent |
| `A3_AGENT_NATIVE` | Agent-native | machine-readable capability discovery, typed schemas, MCP/ACP or comparable agent protocol, structured outcomes |
| `A4_VERAGENSIA_NATIVE` | Fully integrated | typed affordances, exact authority scope, stable object identity, receipts/evidence, lifecycle/events, Focusa-aware governance |

Default-selection rule:

> Prefer `A4` → `A3` → `A2` → `A1`. Use `A0` only when no materially better option exists or the user explicitly requires that application.

Agentability is not a permanent vendor score. It is versioned per application/runtime integration and can improve through adapters.

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
  office.documents:
    minimum_agentability: A2_AUTOMATABLE
  knowledge.notes:
    minimum_agentability: A2_AUTOMATABLE
  development.editor:
    minimum_agentability: A2_AUTOMATABLE
```

The profile states what the Agent Computer must be able to do. A resolver selects a compatible implementation for the platform, trust class, entitlement, resource budget, user preference and installed capability set.

Package names MAY remain as explicit pins when exact software is required.

## 6. Agent App Resolver

The **Agent App Resolver** is a Veragensia platform responsibility.

Inputs may include:

- requested capability;
- user preference or explicit application pin;
- platform/architecture;
- Agentability Class;
- Focusa authority requirements;
- trust class;
- entitlement/license posture;
- local/cloud execution profile;
- CPU, memory, GPU and storage budget;
- isolation requirements;
- data locality/privacy requirements;
- network policy;
- application health/compatibility evidence.

The resolver returns an implementation choice plus the machine interfaces that agents should prefer.

A resolver decision is not permission to execute the application. Normal Focusa/UIAI authority and consequence checks still apply.

## 7. Agent App Descriptor extension

The earlier `veragensia.agent_app.v1` concept is extended so Focusa and Veragensia can understand how an application is operated, not merely that it exists.

Illustrative shape:

```yaml
schema: veragensia.agent_app.v1
id: app:example
version: 1

runtime:
  type: native | oci | web | remote
  image_digest: null

human:
  desktop: true

agent:
  agentability: A3_AGENT_NATIVE
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

resources:
  cpu: 1
  memory_mb: 512

filesystem:
  mounts: []

network:
  policy_ref: default-deny

credentials:
  broker_refs: []
```

Descriptors advertise affordances; they do not grant them.

## 8. Default first-party composition

The following relationship is normative:

```text
                         VERAGENSIA
                       Agent Computer
                             |
              +--------------+--------------+
              |                             |
       Focusa Desktop                 UIAI Cockpit
       governed work                  browser/computer
       presentation                   execution/proof
              |                             |
              +-------------+---------------+
                            |
                    Focusa daemon/core
                    scoped cognition,
                    authority, evidence
                            |
                         Pi harness
                  reference agent runtime
                            |
                 other thin agent adapters
```

The diagram is a responsibility map, not a process topology requirement. Pi and UIAI may call Focusa through generated interfaces rather than being children of one process.

## 9. Pi position

Pi is fundamental to Focusa's current agent experience and MUST be treated accordingly in Veragensia planning.

- Pi is the **reference/default Focusa-aware harness** for an Agent Computer.
- The Focusa Pi extension supplies typed tools, skills/runbooks, scope/authority hooks, Workpoint/Trajectory/evidence access, metacognition and recovery surfaces.
- Pi does not become Focusa's reducer, canonical memory, ontology owner, or independent cognitive authority.
- Non-Pi agents remain first-class supported consumers through the Focusa Agent Adapter Contract and generated capability surfaces.
- Veragensia must not make the OS architecture dependent on Pi-only hidden state; all canonical state stays in Focusa-owned contracts.

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
- degraded/stale/blocked states honestly.

Focusa Desktop MUST NOT evaluate or invent authority independently of the Focusa execution guard, write reducer/storage state directly, or become a second product/license authority.

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
- human oversight/takeover through Cockpit/FPV where authorized.

Browser visual computer use remains available when structured and semantic actuators cannot complete the task.

## 12. Software catalog policy

Veragensia WILL maintain an **Agent-First Software Catalog**, but the catalog is intentionally not frozen by this specification.

Each candidate record SHOULD capture:

- capability families;
- Agentability Class;
- machine interfaces;
- human desktop quality;
- file/data portability;
- Linux/Agent Computer compatibility;
- local/cloud suitability;
- isolation model;
- credential model;
- evidence/provenance support;
- resource requirements;
- licensing/distribution constraints;
- known failure/degraded modes.

Software evaluation must distinguish:

```text
popular software
!=
best software for an Agent Computer
```

and:

```text
"has AI features"
!=
"is agent-operable"
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

The user asks for capability or workforce. Veragensia chooses the topology.

## 14. Telemetry and improvement

Agentability itself is measurable. Privacy-safe telemetry MAY compare:

- structured-interface success rate;
- semantic-automation success rate;
- visual fallback rate;
- retries and recovery rate;
- average model/tool cost per accepted outcome;
- operator takeover/intervention rate;
- evidence completeness;
- latency and resource cost.

The objective is not to maximize automation for its own sake. It is to reduce the total cost and fragility of correctly authorized, verified work while preserving human control.

## 15. Acceptance invariants

A future implementation satisfies this direction only when:

1. Agent Computer Profiles can request capabilities independently of exact packages.
2. Installed applications can advertise versioned agent-operability metadata.
3. Agents can prefer structured/semantic surfaces and fall back to computer use without authority expansion.
4. Focusa Desktop is available as the default governed work presentation on supported full profiles.
5. Pi is available as the default/reference Focusa-aware harness on supported profiles, without making canonical state Pi-private.
6. UIAI remains the first-party browser execution/proof surface and existing Agent-First Browser contracts are reused.
7. The software catalog can evolve without redefining Focusa authority, Veragensia profiles, or the application ontology.
8. The human can still install/use ordinary software even when it is low-agentability; Veragensia reports the limitation rather than pretending structured control exists.

## 16. Deferred software-selection work

A later dedicated evaluation will select and benchmark the best default software for areas including development, shell, office/document work, knowledge, communications, meetings, CRM/business operations, media, data analysis and vertical applications.

That evaluation should use this spec's criteria and real agent task evidence. No candidate named during architecture discussion is canonically selected merely by mention.