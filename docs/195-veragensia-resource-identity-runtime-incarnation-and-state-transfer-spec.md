# 195 — Veragensia Resource Identity, Runtime Incarnation, and State Transfer

**Status:** DRAFT canonical product direction, 2026-09-04.
**Canonical human architecture authority:** Verious Smith III under Doc 185.
**Dependencies:** Docs 193–194; Focusa ProjectIdentity, Workpoint, remote-workspace, settlement and temporal authority contracts; UIAI observation/runtime identity.

## 1. Decision

Paths, PIDs, window titles, container names, browser target IDs and streaming coordinates are **locators**, not durable identity.

Elastic Agent Computing requires stable resource identity plus explicit runtime incarnations so a grant or observation cannot accidentally attach to a different object after rename, replacement, restart, restore, migration or ID reuse.

```text
stable logical identity
        +
exact revision/incarnation
        +
current locator/projection
        =
safe action target
```

## 2. Foundational laws

1. **Path is not identity.** A filesystem path may locate a resource but does not prove that the same underlying resource is still there.
2. **PID is not identity.** Process IDs may be reused.
3. **Window title is not identity.** Presentation strings are advisory.
4. **Container/VM name is not workload identity.** Names may be reused or pointed elsewhere.
5. **Runtime IDs are incarnation-scoped.** Browser targets, PipeWire nodes, accessibility nodes and compositor surfaces never pretend to survive replacement.
6. **Every consequential action binds expected revision.** Stale revisions fail closed or reconcile.
7. **Every restart/restore/migration advances an incarnation boundary when old volatile references can no longer be trusted.**
8. **Replica is not original.** Local and cloud copies of one logical project/resource are distinct physical replicas with separate revisions and settlement state.
9. **State transfer is typed.** Files, conversation state, credentials, process checkpoints, Workpoints and external effects have separate transfer semantics.
10. **Snapshot is not rollback of reality.** Restoring files/processes does not reverse email, payment, deployment or other external effects.
11. **Stale cached authority cannot bind a new incarnation.** Control leases, credentials, observations and EnforcementPlans must be revalidated.
12. **Identity mappings are provenance-bearing and inspectable.**

## 3. `ResourceRef`

```yaml
schema: veragensia.resource_ref.v1
resource_ref:
resource_kind:
logical_owner_ref:
project_ref:
continuity_id:
canonical_identity_ref:
revision_ref:
content_digest_ref:
locator_refs: []
replica_refs: []
created_at:
```

Examples include:

```text
file
directory
repository
working_tree
document
spreadsheet
browser_profile
browser_context
application_state
conversation_ledger
artifact
external_record
```

The owning domain remains authoritative for the resource itself.

## 4. `ResourceLocator`

```yaml
schema: veragensia.resource_locator.v1
locator_ref:
resource_ref:
kind: filesystem_path | uri | object_key | provider_id | browser_target | app_object
value:
node_ref:
runtime_incarnation_ref:
verified_at:
fresh_until:
```

A locator may change without changing logical resource identity.

## 5. Revision and compare-and-set

Mutations SHOULD state:

```yaml
expected_resource_ref:
expected_revision_ref:
expected_content_digest_ref:
```

When the current state differs, the runtime returns conflict/reconciliation instead of silently writing to the changed object.

This applies especially to:

- source files;
- documents/spreadsheets;
- configuration;
- application objects;
- browser forms before consequential submit;
- remotely synchronized workspace state.

## 6. Filesystem resolution

For path-backed resources, Veragensia must safely resolve the target beneath its authorized roots and defend against time-of-check/time-of-use replacement.

Required posture includes, where applicable:

- pre-opened directory handles;
- no traversal outside authorized root;
- controlled symlink/magic-link handling;
- inode/file identity checks;
- content/revision validation;
- separate source and output roots;
- atomic promotion where possible;
- explicit conflict instead of blind overwrite.

## 7. `RuntimeIncarnation`

```yaml
schema: veragensia.runtime_incarnation.v1
runtime_incarnation_id:
agent_computer_ref:
node_identity_ref:
parent_incarnation_ref:
reason: boot | service_restart | container_replace | restore | migration | desktop_session_replace | browser_context_replace
boot_or_epoch_ref:
software_attestation_ref:
started_at:
ended_at:
```

Every volatile runtime object references an incarnation.

## 8. Incarnation-scoped objects

Examples:

```text
process identity
Unix socket
Wayland surface
Xwayland server/client
accessibility node
PipeWire stream
browser target/context
control lease
credential lease
EnforcementPlan
DesktopObservation
Agent App process
workcell process tree
```

If an incarnation changes, stale references are invalid until explicitly reconciled/rebound.

## 9. State-transfer domains

Veragensia distinguishes:

### 9.1 Cognitive/work continuity

Owned by Focusa:

- ProjectIdentity;
- continuity_id;
- Workpoint;
- Trajectory;
- Evidence refs;
- outstanding obligations/blockers;
- settlement state.

### 9.2 Resource state

- files;
- documents;
- repository/worktree revisions;
- Agent App data;
- browser state where explicitly transferable.

### 9.3 Runtime/process state

- process memory/checkpoint;
- sockets;
- open handles;
- compositor/browser runtime identity.

Process resume is not cognitive continuity.

### 9.4 Credential state

Credential grants/custody are reissued/revalidated through the credential authority. Secrets are not casually bundled into workspace transfer.

### 9.5 Conversation state

Focusa Doc 181 Conversation Ledger may transfer through exact scoped handles/segments according to privacy/retention policy; a conversation's history does not become a grant on the destination node.

### 9.6 External-effect state

Emails, financial transactions, deployments, provider records and real-world effects are reconciled through Focusa Spec 136. They are never reversed by restoring a local snapshot.

## 10. Replica model

```yaml
schema: veragensia.resource_replica.v1
replica_ref:
resource_ref:
node_ref:
runtime_class: local | cloud_agent_computer | workcell | remote_specialist
base_revision_ref:
current_revision_ref:
sync_state: current | ahead | behind | diverged | unknown
writer_lease_ref:
created_at:
```

One logical resource can have multiple replicas without pretending they are one writable filesystem.

## 11. Writer fencing

Focusa writer/workspace leases bind to ResourceRefs/replicas and exact generations.

A stale worker must not be able to mutate after:

- lease transfer;
- worktree replacement;
- cloud migration;
- operator takeover;
- restart/recovery;
- settlement/conflict.

## 12. Browser/desktop state relationship

Doc 194 DesktopObservation and UIAI BrowserObservation use exact runtime incarnations.

A browser navigation/document replacement or desktop surface replacement can advance local object generations without necessarily replacing the whole Agent Computer incarnation.

Actions are always checked at the narrowest relevant current generation.

## 13. Suspend, hibernate and checkpoint

Suspend does not necessarily create a new Agent Computer incarnation when the same trusted session resumes, but every volatile subsystem defines whether its references survive.

Checkpoint/restore MUST record which identities are:

```text
preserved
rebound
invalidated
unknown
```

Unknown references require re-observation/reconciliation.

## 14. Cloud migration

A migrated Agent Computer/workcell preserves logical work identity while receiving a destination node/workload/runtime incarnation.

The handoff binds:

- exact ProjectIdentity/continuity/Workpoint;
- resource replica/revision set;
- execution intent/attempt identity;
- unresolved external effects;
- workload identity/attestation;
- new EnforcementPlan;
- authority/credential freshness;
- old incarnation termination/fencing evidence.

The destination never adopts the source's stale kernel/compositor/process identifiers.

## 15. Conversation-history continuity

Voice-native interaction should feel continuous across local/cloud bodies.

The conversation ledger can span devices/nodes through scoped segment refs while each utterance preserves:

- capture node/device;
- participant principal;
- audio/transcript source;
- timing authority;
- privacy policy;
- current project/Workpoint binding;
- which Agent Computer incarnation rendered or heard it.

## 16. Acceptance invariants

Tests must prove:

1. replacing a file at the same path triggers revision/identity conflict when material;
2. symlink/path races cannot escape authorized roots;
3. stale PID/window/browser/stream IDs do not bind after incarnation change;
4. a restored runtime revalidates leases/credentials/observations;
5. local/cloud workspace divergence cannot silently overwrite either side;
6. stale writers are fenced after handoff;
7. filesystem restore does not mark external effects rolled back;
8. conversation continuity preserves source incarnation and speaker lineage;
9. state-transfer reports preserved/rebound/invalidated/unknown refs explicitly.

## 17. Final principle

> Veragensia acts on identities and revisions. Paths, pixels, process numbers and names are merely temporary ways to find them.
