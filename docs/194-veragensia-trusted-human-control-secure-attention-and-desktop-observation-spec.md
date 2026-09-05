# 194 — Veragensia Trusted Human Control, Secure Attention, and Desktop Observation

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Dependencies:** Doc 193 execution enforcement, Doc 195 resource/runtime identity, Focusa authority/settlement, UIAI Agent-First Browser contracts and `uiai.cockpit_operator_control_lease_takeover_reconciliation.v1`.

## 1. Decision

A future Agent Computer needs a trusted control plane that ordinary applications and agents cannot convincingly impersonate, plus versioned desktop observations that make computer-use actions conditional on the exact world the agent observed.

The primitive relationship is:

```text
Trusted Human Control
    secure attention · consent · emergency stop
              |
              v
DesktopObservation
    exact surface/window/object/generation
              |
              v
ComputerControlLease
    one current actuator holder + fencing
              |
              v
Observation-bound Action
              |
              v
OperatorDelta / Re-observation / Evidence
```

## 2. Foundational laws

1. **Human authority needs a trusted path.** A security-sensitive approval rendered inside an arbitrary app is not sufficient.
2. **Ordinary pixels cannot impersonate secure attention.** The trusted control surface has a compositor/OS-owned identity and presentation contract.
3. **Human control survives agent failure.** Emergency freeze/stop/revoke paths remain available even when Focusa, a model, a browser, or an Agent App is degraded.
4. **One active actuator holder per controlled scope.** Human, agent and remote operator cannot concurrently inject uncontrolled input into the same actuator scope.
5. **Control uses generation and fencing.** Stale controllers cannot resume after takeover/restart.
6. **Local safety freeze is not canonical Focusa pause.** Preserve UIAI's existing distinction.
7. **Returning control requires delta capture and re-observation.** An agent may not resume from stale assumptions after the human changes the computer.
8. **Actions bind to observations.** Computer use must say which surface/window/object/generation it believed it was acting on.
9. **Coordinates are never enough.** Position is interpreted only inside an explicit coordinate-space/surface mapping.
10. **Surface identity survives presentation changes where possible; runtime identity does not pretend to survive replacement.**
11. **Window focus is not intent.** Focused window/tab alone never chooses project, task or authority.
12. **Voice can operate trusted control.** Voice-complete profiles must expose secure approval, takeover, stop and review without keyboard/mouse dependence.
13. **Voice identity alone is not trusted attention or authorization.** See Focusa Doc 181 and Veragensia Doc 197.

## 3. Trusted Secure Attention Plane

The **Secure Attention Plane** is a Veragensia-controlled UI/audio surface whose origin and state are distinguishable from application content.

It handles only bounded high-trust interactions such as:

- consequential approval/denial;
- exact target confirmation;
- credential/authentication handoff status;
- control takeover/return;
- global agent pause/stop;
- emergency revocation;
- trust/degraded warnings that affect safe action.

It does not become Focusa authority. It presents and returns the result of Focusa/credential/runtime authority operations through a trusted OS surface.

## 4. Trusted prompt contract

```yaml
schema: veragensia.secure_attention_prompt.v1
prompt_id:
authority_decision_ref:
operation_ref:
actor_principal_ref:
target_resource_refs: []
consequence_class:
summary:
material_effects: []
uncertainty_refs: []
confirmation_modes:
  - spoken
  - touch
  - hardware_presence
  - keyboard
expires_at:
trusted_surface_generation:
```

A normal application cannot mint this schema into a valid trusted prompt merely by drawing the same visual design.

## 5. Voice-secure confirmation

For voice-complete profiles, trusted prompts support a spoken interaction such as:

```text
System: "Security confirmation. Agent Build-7 is requesting to deploy project X to production. This may restart the service. Say approve deployment or deny."
Human: "Approve deployment."
```

The system records:

- authenticated session/presence context;
- secure prompt ID;
- exact spoken transcript/source observation;
- speaker attribution confidence;
- decision;
- operation and target;
- expiry;
- resulting authority receipt.

High-consequence policy may require an additional presence/authentication factor that is still keyboard/mouse independent.

## 6. `DesktopObservation`

```yaml
schema: veragensia.desktop_observation.v1
observation_id:
agent_computer_ref:
runtime_incarnation_ref:
compositor_generation:
control_lease_ref:

surface:
  surface_ref:
  application_ref:
  process_or_workload_ref:
  window_ref:
  workspace_ref:
  title_projection:

coordinate_spaces:
  compositor_space_ref:
  stream_space_ref:
  scale:
  transform_ref:

semantic:
  accessibility_snapshot_ref:
  semantic_object_refs: []

visual:
  screenshot_or_frame_ref:
  visual_hash:

input_state:
  focus_ref:
  pointer_ref:
  modal_dialog_ref:

captured_at:
freshness:
```

Private titles/content follow the observation's scope/redaction policy.

## 7. Stable desktop object references

Where available, an agent acts on a stable semantic object:

```yaml
schema: veragensia.desktop_object_ref.v1
object_ref:
observation_ref:
surface_ref:
runtime_object_id:
role:
name_fingerprint:
state_fingerprint:
bounds_in_surface_space:
accessibility_ref:
visual_anchor_ref:
```

Runtime identifiers are valid only for the matching runtime/surface generation.

## 8. Coordinate spaces

Every visual action declares its coordinate-space mapping.

Never treat:

- streamed video pixels;
- physical display pixels;
- compositor logical coordinates;
- accessibility object bounds;
- browser viewport coordinates

as interchangeable.

Resize, DPI/scale change, monitor rearrangement, stream rescaling, window movement or document replacement may invalidate the mapping and require re-observation.

## 9. Observation-bound action

```yaml
schema: veragensia.desktop_action_request.v1
action_id:
focusa_action_proposal_ref:
capability_grant_ref:
control_lease_ref:
expected:
  observation_id:
  runtime_incarnation_ref:
  compositor_generation:
  surface_ref:
  object_ref:
  state_fingerprint:
action:
  kind:
  parameters:
response_policy_ref:
```

Before input injection Veragensia/UIAI revalidates the binding.

Material mismatch returns:

```text
stale
resync_required
fencing_conflict
object_changed
surface_replaced
control_not_held
```

rather than clicking anyway.

## 10. Generalized `ComputerControlLease`

Veragensia adopts the semantics already designed in UIAI's operator-control lease contract.

```yaml
schema: veragensia.computer_control_lease.v1
control_lease_id:
lease_generation:
fencing_token:
agent_computer_ref:
runtime_incarnation_ref:
scope_ref:
holder_principal_ref:
actuator_refs: []
state: agent_controlled | operator_controlled | local_freeze | return_pending | terminated | orphaned | fencing_conflict
issued_at:
expires_at:
focusa_intervention_ref:
```

One lease may cover a browser context, application surface or full desktop according to scope.

## 11. Takeover sequence

Canonical sequence:

```text
human requests takeover
→ immediate local input freeze where necessary
→ Focusa intervention request
→ lease generation advances
→ human becomes actuator holder
→ human acts
→ OperatorDelta captured
→ return requested
→ Focusa reconciliation
→ fresh DesktopObservation
→ authority/credential refresh
→ agent resumes / redirects / blocks / stops
```

The agent never resumes merely because the human stopped touching the pointer.

## 12. `OperatorDeltaReceipt`

```yaml
schema: veragensia.operator_delta_receipt.v1
delta_receipt_id:
control_lease_ref:
conversation_ref:
started_at:
ended_at:
changed_resource_refs: []
changed_surface_refs: []
not_performed: []
pending_side_effect_refs: []
current_observation_refs: []
reobservation_required: true
redaction_ref:
```

Secrets are represented as value-free state changes.

## 13. Voice takeover and control

Voice-complete profiles support commands such as:

```text
"Stop moving the mouse."
"Give me control."
"Pause the deployment."
"Take me to the exact window you're using."
"I changed the account selection. You can continue."
"Don't continue; stop this task."
```

These are mapped to the same trusted control/intervention operations. Speech does not bypass fencing, target binding or reconciliation.

## 14. Human control reserve

Doc 193 protects the resource budget required for:

- secure attention;
- input arbitration;
- emergency freeze/stop;
- Focusa intervention;
- voice interaction where enabled.

A resource-starved agent fleet must not be able to starve the stop path.

## 15. Remote/streamed desktops

Remote viewing/control must preserve:

- exact Agent Computer identity;
- surface/runtime generation;
- coordinate-space transform;
- control-lease holder;
- latency/degraded posture;
- trusted-control indication;
- session privacy/trust class.

A stream URL or remote-desktop connection is transport capability, not authorization.

## 16. Accessibility and computer use

Semantic accessibility actions and visual computer use both produce DesktopObservation lineage.

Preferred path:

```text
structured application capability
→ accessibility/semantic object
→ visual object/coordinates
```

Each fallback preserves the same control lease and authority scope.

## 17. Acceptance invariants

Production acceptance requires proof that:

1. an app cannot create a valid trusted Secure Attention prompt;
2. human stop/takeover works while an agent is actively controlling the desktop;
3. stale control generations cannot inject input;
4. return from human control requires a fresh observation;
5. a moved/replaced target fails an observation-bound action;
6. stream/display coordinate changes trigger remapping rather than mis-clicks;
7. accessibility and visual actions share the same authority/control scope;
8. pending unknown side effects block unsafe resume;
9. trusted approval is fully operable by voice in a voice-complete profile;
10. agent resource pressure cannot starve secure attention or stop control.

## 18. Final principle

> Human control is not a courtesy layered over agent automation. It is a protected operating-system primitive with stronger freshness and fencing guarantees than the automation it governs.
