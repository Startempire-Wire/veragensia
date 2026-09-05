# 201 — Veragensia Semantic OS Operations, Keybinding Projection, and VoxType Integration

**Status:** DRAFT canonical product direction, 2026-09-05.  
**Canonical human architecture authority:** Verious Smith III under Doc 185.  
**Companions:** Docs 190, 193–200; Focusa Operation Registry / Spec 141 capability contracts / Spec 181 Voice; UIAI Agent-First Browser/control contracts; current Omarchy CLI/hotkey/dictation behavior recorded as external platform evidence.  

---

## 0. Decision

Omarchy is intentionally keyboard-first. Veragensia MUST preserve the speed and elegance of that design while removing the assumption that a human keyboard is the canonical control API.

> **Every meaningful Omarchy/desktop keybinding must resolve to a semantic system operation that can be invoked directly by agents, voice, mobile, hardware controls, CLI, or human hotkeys. The hotkey is a projection of the operation, not the operation itself.**

The target is not an agent that presses keys quickly. The target is an Agent Computer whose agents can operate the shell and applications through direct structured operations at machine speed, falling back to semantic UI or guarded input injection only when no stronger interface exists.

```text
semantic system operation
        |
        +-- human keybinding
        +-- natural voice
        +-- Focusa/Pi agent call
        +-- Ambient Operator
        +-- CLI/API
        +-- hardware/wearable control
        +-- automation
```

## 1. Foundational laws

1. **Keybinding is presentation, not authority.** Possessing or replaying a hotkey never grants Focusa permission.
2. **Keybinding is not canonical operation identity.** `SUPER + SHIFT + O` may launch Obsidian today and something else tomorrow; operation identity remains stable across remapping.
3. **Agent speed comes from direct operations, not synthetic typing.** Use Omarchy CLI, Hyprland dispatch, application protocol/API, Focusa capability, or UIAI semantic action before injecting keys.
4. **Live runtime wins over static documentation for available bindings.** Omarchy keymaps evolve. Discover/verify the active keymap at runtime.
5. **One operation, many modalities.** Voice, Pi, Desktop, mobile, API, hardware controls, and hotkeys call the same operation contract.
6. **Target identity is explicit.** Operations acting on windows/resources use current ResourceRef/DesktopObservation/runtime identity rather than assuming the focused object is intended.
7. **Focused window is context, not authority.** A focused application can help resolve a target but cannot define project/task permission.
8. **Batching is first-class.** Agents can invoke safe ordered operation batches without serially emulating human keystrokes.
9. **Low-latency control remains interruptible.** Owner voice/takeover/stop can fence an agent even while rapid shell operations are running.
10. **User customizations survive.** Veragensia must not overwrite the owner's `bindings.lua` merely to maintain agent control.
11. **Application-internal shortcuts are adapters, not OS primitives.** Where an application exposes a native command/API, use it; key injection remains compatibility fallback.
12. **Text insertion is not semantic control.** Dictation into a text field and commanding the computer are separate interaction modes.
13. **VoxType is an adapter, not conversation or authority owner.** It may supply capture/ASR/meeting/dictation machinery but cannot replace Focusa Spec 181 or Veragensia trusted audio/control.
14. **Keyboard absence is a release test.** A voice-complete profile must perform representative operations with the physical keyboard/pointer unavailable.

## 2. Current Omarchy relationship

Current Omarchy exposes three valuable control surfaces:

```text
1. Omarchy CLI
   `omarchy <group> <command>`
   `omarchy commands --all --json --check`

2. Hyprland / shell runtime
   live compositor/window/workspace state and dispatch operations

3. Keybinding projection
   user overrides in `~/.config/hypr/bindings.lua`
   live keymap discoverable from Omarchy/Hyprland
```

Veragensia should consume all three, in that order of semantic strength where applicable.

Do not scrape the manual and freeze today's default hotkeys into the Agent Computer architecture.

## 3. `SystemOperationDescriptor`

```yaml
schema: veragensia.system_operation.v1
operation_id: system.workspace.activate
version: 1
owner_runtime: veragensia | omarchy | hyprland | focusa | uiai | application
category: workspace | window | app | audio | bluetooth | display | power | capture | clipboard | notification | agent | text | system

human:
  label: "Go to workspace"
  current_hotkeys: []

voice:
  examples:
    - "Go to workspace two"
    - "Take me to the next workspace"

parameters:
  schema_ref:

preconditions:
  capability_refs: []
  authority_ref_required: false
  target_observation_required: false
  secure_attention_required: false

execution:
  preferred_adapter: omarchy_cli | hyprland_dispatch | native_service | focusa_operation | uiai_operation | app_protocol
  fallback_adapters: []
  command_template_ref:

risk:
  consequence_class:
  reversibility:

result:
  schema_ref:
  evidence_policy_ref:
```

The descriptor advertises how to invoke a system behavior; actual permission remains governed by applicable Focusa/Veragensia/UIAI gates.

## 4. Keybinding projection and parity

Veragensia SHALL maintain a runtime **Keybinding Projection** that correlates live bindings to semantic operations.

Illustrative record:

```yaml
schema: veragensia.keybinding_projection.v1
binding_ref:
source: omarchy_default | user_override | generated | application
key_chord: "SUPER + SHIFT + O"
operation_ref: app.launch.obsidian
active: true
observed_at:
runtime_incarnation_ref:
```

### 4.1 Runtime discovery

A qualification/diagnostic path SHOULD compare:

- Omarchy command registry (`omarchy commands --all --json --check` where supported);
- Omarchy keybinding print/introspection;
- live Hyprland bindings/state;
- user `~/.config/hypr/bindings.lua` overrides;
- Veragensia operation catalog.

### 4.2 Classification gate

Every live binding must be classified as one of:

```text
semantic_operation
text_input
application_internal
hardware_firmware
unsupported_platform
unmapped_gap
```

`unmapped_gap` is a release/agentability defect for a full Agent Computer profile.

### 4.3 Generated hotkeys are optional

Veragensia MAY generate or suggest user bindings for its own operations, but direct agent/voice access MUST NOT depend on those bindings existing.

## 5. Agent invocation hierarchy

For any keyboard-accessible action, the agent chooses the strongest truthful route:

```text
A. Focusa/Veragensia typed operation
B. Omarchy CLI command
C. Hyprland/native shell dispatcher
D. application API / CLI / D-Bus / MCP / ACP
E. accessibility/semantic UI
F. UIAI/computer-use observation-bound action
G. guarded keybinding replay / text injection
```

The system records which route was used.

### Example: launch Obsidian

Human projection today may be:

```text
SUPER + SHIFT + O
```

Agent path should be closer to:

```text
app.launch {
  app_ref: "obsidian"
}
```

which resolves to the installed/profile-approved launcher.

### Example: move a window

Do not simulate:

```text
SUPER + SHIFT + ArrowRight
```

when the compositor can target the exact current window/surface directly.

### Example: paste text

If the task is literally dictation/compatibility text entry, clipboard/type injection may be correct. It is not the normal route for system control.

## 6. Rapid conversational control

The Agent Computer should feel faster than a skilled keyboard user during conversation.

Example:

```text
Owner: "Put the browser on workspace two, bring the project terminal beside it, and open Focusa Desktop here."

speech
→ Focusa current ask
→ resolve exact application/window refs
→ operation batch
    workspace.assign(browser, 2)
    workspace.assign(project_terminal, 2)
    focusa_desktop.present(current_monitor)
→ verify final desktop observation
→ concise spoken acknowledgement
```

The user does not have to wait for an agent to perform three visible keyboard dances.

## 7. `SystemOperationBatch`

```yaml
schema: veragensia.system_operation_batch.v1
batch_id:
origin_utterance_ref:
workstream_ref:
operations:
  - operation_ref:
    args:
    expected_target_ref:
    expected_observation_ref:
atomicity: best_effort_ordered | stop_on_failure | transactional_where_supported
interruption_policy_ref:
created_at:
```

Rules:

- batch execution cannot broaden the union of authority granted to individual operations;
- consequential operations retain their own preview/approval/settlement requirements;
- owner interruption fences remaining operations;
- completion reports partial execution honestly.

## 8. Voice grammar is generated from operation semantics

Focusa/Veragensia should not maintain a hand-written library of thousands of magic phrases.

Operation descriptors provide:

- human description;
- parameter names/types;
- synonyms/examples;
- target classes;
- risk/confirmation requirements.

The conversational layer maps natural language to these capabilities dynamically.

Emergency operations MAY retain deterministic phrases such as:

```text
"Stop all agent input."
"Give me control."
"Mute the microphone."
```

but ordinary use remains natural.

## 9. VoxType current role

Current Omarchy already integrates **VoxType** as its AI dictation feature.

That makes VoxType a preferred candidate/reuse source for:

- PipeWire/PulseAudio microphone capture;
- compositor-triggered push-to-talk/toggle handling;
- local ASR engines/model management;
- VAD/eager processing;
- transcript post-processing hooks;
- meeting capture/diarization adapters;
- local-first operation;
- Wayland/Hyprland output compatibility;
- audio OSD/state feedback.

Veragensia MUST NOT create a redundant dictation daemon simply because Focusa adds richer conversation semantics.

## 10. VoxType integration modes

### 10.1 Compatibility dictation

```text
VoxType capture/ASR
→ transcript
→ clipboard/type into focused application
```

Use for arbitrary legacy text fields where no stronger application operation exists.

This is a compatibility capability such as:

```text
text.dictate_into_focused_input
```

not the canonical voice-control path.

### 10.2 Focusa semantic conversation

```text
VoxType-compatible capture/ASR engine
→ trusted veragens-audiod session
→ Focusa AudioSegment / SpeechHypothesis / Utterance
→ Foreman/Wirebot/canonical operations
```

No automatic paste occurs.

### 10.3 Meeting capture

VoxType's meeting/transcription/diarization functionality MAY serve as one capture/ASR adapter for Focusa Ambient Operator meeting mode.

Output must be converted into Spec-181 objects preserving:

- source audio handle;
- engine/model/version;
- timestamps;
- speaker candidate/confidence;
- transcript correction lineage;
- retention policy.

A VoxType Markdown/JSON export is not automatically the canonical Conversation Ledger.

## 11. VoxType must not own secrets or authority

Even when installed by Omarchy:

- API/model credentials follow Veragensia/Focusa credential policy;
- microphone access belongs only to the trusted audio workload/profile that needs it;
- a transcription result never authorizes an operation;
- VoxType post-processing scripts cannot silently mutate Focusa meaning;
- auto-paste cannot be used for trusted Secure Attention confirmations;
- VoxType's own conversation/meeting files remain source artifacts until ingested through Focusa contracts.

## 12. Low-resource profile

The CC11260 reference system has 4 GB RAM. Voice integration must preserve the constrained-device posture.

Recommended initial strategy:

```text
local capture + mute + VAD + stop path
+
one small/on-demand local ASR model OR remote/private ASR adapter
+
models unload when idle where supported
+
no mandatory large resident speech model
```

A speech model consuming a large portion of system RAM must not starve Focusa, UIAI, the human-control reserve, or the browser.

## 13. Obsidian relationship

Current Omarchy exposes Obsidian as a first-class launch target, but Veragensia should represent Obsidian through semantic application capabilities rather than only the launch hotkey.

Future Agent App/catalog work should discover and prefer, where available:

```text
app.launch
note.search
note.open
note.create
note.edit
link.create
vault.query
```

through Obsidian CLI/plugin/filesystem/other structured surfaces before keyboard simulation.

The existing Startempire Obsidian vault/Wiki integration remains a separate owner-knowledge domain and must not be conflated with installing the Obsidian desktop app on an Agent Computer.

## 14. Implementation slices

### V201-S1 — live Omarchy operation/keymap inventory

Implement diagnostics that capture:

```text
Omarchy command registry
live Omarchy/Hyprland keybindings
user binding overrides
current app launch/default mappings
```

and emit a bounded JSON inventory.

### V201-S2 — semantic system-operation registry

Implement descriptors for the first operation families:

- workspace/navigation;
- window placement/state;
- app launch/close/focus;
- audio/Bluetooth;
- display/power;
- capture/clipboard;
- notification/history;
- agent launch/selection;
- dictation/listening control.

### V201-S3 — keybinding parity compiler

Map every live Omarchy binding to a semantic operation or explicit classification.

### V201-S4 — direct agent/CLI execution

Expose:

```text
veragens operation list --json
veragens operation describe <id> --json
veragens operation invoke <id> --args ... --json
veragens operation batch --file ... --json
veragens keymap inspect --json
```

Exact final CLI spelling remains subordinate to existing `veragens` command conventions.

### V201-S5 — Focusa/voice projection

Generate agent/voice capability projection from the same operation descriptors.

### V201-S6 — VoxType compatibility adapter

Reuse installed VoxType where compatible for dictation and ASR/capture experiments without giving it Focusa authority.

### V201-S7 — VoxType semantic/meeting adapter

Bind selected VoxType capture/ASR/meeting output into Focusa Spec-181 Conversation objects.

### V201-S8 — rapid conversation benchmark

Benchmark representative voice instructions against skilled-hotkey/manual execution and require the structured agent path to avoid unnecessary visible input choreography.

## 15. Acceptance invariants

1. every active default Omarchy system hotkey is mapped or explicitly classified;
2. remapping a hotkey does not change the semantic operation identity;
3. an agent can invoke common workspace/window/app/audio operations without keyboard injection;
4. voice uses the same operation registry;
5. owner interruption fences a running operation batch;
6. exact window/resource target is verified instead of relying solely on focus;
7. user `bindings.lua` customizations survive installation/update;
8. a changed Omarchy keymap is detected as projection drift rather than silently breaking agent control;
9. VoxType dictation can type into a legacy field without becoming trusted system control;
10. VoxType-derived conversation/meeting data enters Focusa with engine/speaker/transcript lineage;
11. random Agent Apps do not inherit trusted microphone access because VoxType/`audiod` is installed;
12. representative system navigation succeeds without physical keyboard/pointer in a voice-complete profile.

## 16. Final principle

> **Omarchy's keyboard speed becomes the floor, not the ceiling. Humans keep the hotkeys; agents get the operations underneath them.**
