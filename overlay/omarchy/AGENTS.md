# AGENTS.md — Veragensia Native Omarchy Integration

This subtree implements Veragensia on stock Omarchy. It supplements repository-root and `docs/AGENTS.md` rules and may only tighten them.

## Required reading

Before changing native Omarchy keybindings, shell integration, app launch behavior, voice/dictation, audio, or agent control, read:

- `../../docs/182b-veragensia-base-os-and-overlay-detailed-spec.md`;
- `../../docs/193-veragensia-execution-substrate-workload-identity-and-capability-enforcement-spec.md`;
- `../../docs/194-veragensia-trusted-human-control-secure-attention-and-desktop-observation-spec.md`;
- `../../docs/197-veragensia-voice-native-agent-computer-audio-ui-and-conversation-continuity-spec.md`;
- `../../docs/199-veragensia-ambient-operator-companion-sync-and-omarchy-integration-spec.md`;
- `../../docs/200a-veragensia-semantic-operation-and-dictation-critical-path-amendment.md`;
- `../../docs/201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md`;
- `../../docs/201a-veragensia-current-omarchy-keybinding-and-voxtype-evidence-2026-09-05.md`;
- `../../docs/contracts/system-operation-keybinding-map.v1.yaml`.

## Native-control laws

1. **Hotkey is a projection, not the API.** Do not implement agent control primarily by replaying Omarchy shortcuts.
2. Prefer `SystemOperation` → Omarchy CLI/Hyprland/native adapter before UI or input injection.
3. Discover the live keymap and command registry; do not freeze a copied manual into code.
4. Preserve owner `~/.config/hypr/bindings.lua`; installation must not overwrite unrelated custom bindings.
5. Every active keybinding must map to a semantic operation or explicit classification. Unknown mappings remain visible gaps.
6. Window focus is contextual evidence, never Workstream/task authority.
7. Operation batches must stop/fence on owner interruption and report partial completion honestly.
8. QML/Quickshell plugins remain presenters/forwarders, not credential, microphone, Focusa-state, authorization, or enforcement boundaries.

## VoxType laws

Current Omarchy's VoxType integration is reused where compatible.

- `type`/clipboard/paste is legacy text-entry compatibility.
- Semantic voice requests go through trusted audio → Focusa Conversation → SystemOperation, with no automatic paste.
- Meeting/diarization output is converted into Focusa Spec-181 source/participant/utterance/revision records.
- Do not grant broad input/uinput permissions merely for convenience when compositor-native triggers suffice.
- VoxType cannot approve, authorize, become Secure Attention, or own canonical conversation state.

## Implementation sequence

First native control closure follows Doc 200A:

```text
live Omarchy command/keymap inventory
→ SystemOperation registry
→ keybinding parity map
→ direct `veragens` operation invocation
→ Focusa/voice projection
→ VoxType adapters
→ agent-speed benchmark
```

Representative acceptance must prove an agent can rearrange/focus/launch a multi-window workspace directly, with zero unnecessary synthetic hotkeys, and that the owner can interrupt it immediately.
