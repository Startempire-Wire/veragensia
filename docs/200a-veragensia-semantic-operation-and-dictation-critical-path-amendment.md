# 200A — Semantic Operation and Dictation Critical-Path Amendment

**Status:** implementation-sequencing amendment, 2026-09-05.  
**Amends:** Doc 200.  
**Depends on:** Doc 201 and 201A; Focusa Operation Registry; Docs 193–197; current Omarchy/Hyprland/VoxType qualification.

## 1. Why this amendment is required

Doc 200 correctly moves from native Omarchy projection into trusted audio. A missing implementation layer is now explicit:

> The Agent Computer must expose the semantic operations underneath Omarchy's keyboard-first UX **before** voice is considered an operating-system control surface.

Otherwise the project risks implementing:

```text
speech
→ recognized phrase
→ synthetic hotkey
```

when the intended architecture is:

```text
speech / agent / hotkey
→ one semantic SystemOperation
→ direct runtime adapter
→ verified result
```

## 2. Critical-path insertion

Doc 200 is amended conceptually as:

```text
T0 Focusa contracts
  ↓
T1 Omarchy read projection
  ↓
T1A Semantic OS Operation / keybinding parity
  ↓
T2 Trusted local audio loop
  ↓
T3+ existing Doc-200 sequence
```

Existing tranche numbers remain stable; `T1A` is the required bridge.

## 3. T1A implementation

Implement Doc-201 slices sufficient for the first living-Agent-Computer vertical:

```text
V201-S1 live Omarchy command/keymap inventory
V201-S2 semantic SystemOperation registry
V201-S3 keybinding parity mapping
V201-S4 direct `veragens operation` invocation
V201-S5 Focusa/voice projection
```

VoxType compatibility/meeting adapter work may begin in parallel but cannot substitute for the operation registry.

## 4. Minimum semantic families before T2 closes

The first audio/voice loop must be able to invoke structured operations for at least:

```text
workspace.select
workspace.next
workspace.previous
window.focus
window.move_to_workspace
window.close
window.fullscreen
window.float_toggle
app.launch
app.focus_or_launch
focusa_desktop.present
agent.foreman.address
agent.pause
agent.stop
system.audio.status
system.audio.output.select
system.bluetooth.status
system.notification.dismiss
system.notification.history
voice.mute
voice.listening_mode.set
```

Exact final IDs are normalized during implementation; these names define semantic intent, not frozen CLI syntax.

## 5. Agent-speed acceptance

Before calling native shell control “agent-friendly,” prove one conversational batch such as:

```text
"Put the browser and project terminal on workspace two, then bring Focusa Desktop here."
```

without replaying the equivalent human key sequences.

Required evidence:

- exact target window/application refs;
- operation batch;
- direct Omarchy/Hyprland/native adapters used;
- final DesktopObservation;
- latency;
- zero unnecessary synthesized keypresses.

## 6. Hotkey-completeness acceptance

Before a full-profile release:

1. collect the live Omarchy/Hyprland keymap;
2. classify every binding under Doc 201;
3. require zero unexplained `unmapped_gap` entries;
4. prove user custom bindings remain untouched;
5. prove remapping a key does not break direct agent invocation.

This is the implementation meaning of “translate all Omarchy keybindings to agent friendliness.”

## 7. VoxType amendment

Current Omarchy already uses VoxType for dictation. T2/T6 should therefore evaluate reuse before building duplicate capture/ASR/meeting code.

Three separate paths must be tested:

```text
compat_dictation
    VoxType -> text injection into legacy focused field

semantic_conversation
    VoxType/capture adapter -> Focusa Spec 181 -> semantic SystemOperation

meeting_capture
    VoxType meeting/diarization adapter -> Focusa Conversation Ledger
```

Only the first path is allowed to make “paste/type at cursor” the expected result.

## 8. Obsidian vertical proof

Obsidian is a useful first application to demonstrate why this distinction matters.

Human Omarchy projection:

```text
Super + Shift + O
```

Agent path:

```text
app.launch.obsidian
→ Obsidian CLI capability discovery
→ search/read/create/edit/query operations
```

A useful early proof is:

```text
Owner: "Open my project notes and find the last discussion about pairing."

→ launch/focus Obsidian
→ structured vault search/read
→ result returned with exact note refs
```

No mouse and no command-palette hotkey choreography should be required when the installed Obsidian CLI can satisfy the request.

The private Startempire vault itself remains a separate owner-knowledge source and is not required for this generic app-control proof.

## 9. SingleEye dependency

The historical SingleEye vault note remains an unresolved source artifact under Doc 201B.

Do not block T1A/T2 implementation on recovering it.

When recovered, its pairing ideas are reconciled into Focusa Spec 53 / Ambient Operator / Veragensia Companion pairing as a separate owner-authorized architecture update.

## 10. Done condition

T1A closes only when:

- agents can directly invoke representative Omarchy shell operations;
- voice can use those same operations;
- keybindings are mapped as projections rather than canonical APIs;
- live keymap drift is detectable;
- one multi-operation conversational instruction completes faster/cleaner than hotkey replay;
- VoxType is classified into compatibility versus semantic-conversation paths;
- Obsidian demonstrates one structured application path beyond launch-only control.
