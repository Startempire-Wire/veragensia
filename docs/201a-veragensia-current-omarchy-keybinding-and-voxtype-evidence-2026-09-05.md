# 201A — Current Omarchy Keybinding and VoxType Qualification Evidence

**Status:** dated upstream/platform evidence, 2026-09-05.  
**Companion:** [Doc 201](201-veragensia-semantic-os-operation-keybinding-and-voxtype-integration-spec.md).  
**Rule:** re-verify before release qualification; this file records current upstream behavior, not permanent architecture.

## 1. Omarchy is deliberately keyboard-first

Current Omarchy Navigation documentation says essentially all normal desktop operation is designed around the keyboard, with `Super + Space` exposing the Omarchy Menu and direct hotkeys preferred for speed.

Source: <https://omarchy.org/manual/navigation/>

Qualification decision:

- preserve human keyboard speed;
- do not make the key chord the canonical machine API;
- every meaningful system hotkey should map to a semantic operation under Doc 201.

## 2. Current hotkey/config surface

Current Omarchy documentation lists major bindings for navigation, workspaces, window layout, system panels, app launch, clipboard, capture, notifications, style, toggles, reminders, Tmux, and related actions.

User keybinding overrides live in:

```text
~/.config/hypr/bindings.lua
```

Source: <https://omarchy.org/manual/hotkeys/>
Source: <https://omarchy.org/manual/dotfiles/>

Package-owned Omarchy files should not be edited directly; user overrides/configuration should be used instead.

## 3. Omarchy CLI is an agent-friendly primitive

Current Omarchy documents a CLI command center and explicitly notes that the CLI is particularly useful when an AI agent is helping with configuration.

Current discovery includes:

```text
omarchy
omarchy commands --all --json --check
omarchy <group> --help
omarchy <group> <command> --help
```

Source: <https://omarchy.org/manual/omarchy-cli/>

Qualification decision:

- prefer Omarchy CLI commands over key replay when equivalent;
- inspect the live command registry rather than freezing the manual into code;
- map CLI commands into Doc-201 SystemOperationDescriptors.

## 4. Keymap representation is currently moving

Current Omarchy 4/Quattro uses Lua for Hyprland user configuration. Recent upstream issues show migration/representation edge cases:

- old `bindings.conf` customizations may remain on disk but stop being loaded after Lua migration;
- `omarchy menu keybindings --print` and `hl.unbind` / `o.bind` use different textual key-chord formats in current reports.

Sources:

- <https://github.com/basecamp/omarchy/issues/6933>
- <https://github.com/basecamp/omarchy/issues/7627>

Qualification decision:

> Never treat one textual keybinding representation as semantic operation identity.

Veragensia should compare live/runtime binding state, Omarchy command discovery, and user override state and report drift explicitly.

## 5. Current Omarchy dictation is VoxType

Current Omarchy Text Extraction & Dictation documentation states that Omarchy installs **VoxType** through:

```text
Install > AI > Dictation
```

and currently exposes:

```text
F9                 push-to-talk dictation
Super + Ctrl + X   toggle dictation
```

Source: <https://omarchy.org/manual/text-extraction-dictation/>
Source: <https://omarchy.org/manual/hotkeys/>

Qualification decision:

Veragensia should reuse/interoperate with the VoxType installation Omarchy already expects rather than create a redundant desktop dictation stack.

## 6. Current VoxType capabilities

Current VoxType upstream (`peteonrails/voxtype`) documents:

- local-first Linux speech-to-text;
- multiple ASR engines including Whisper and ONNX-family engines;
- CPU/GPU execution options;
- VAD/eager processing;
- configurable model loading/unloading;
- compositor-native push-to-talk/toggle integration;
- Wayland output through `wtype` with other fallbacks;
- post-processing hooks;
- meeting mode;
- speaker attribution/diarization;
- Markdown/JSON/SRT/VTT export;
- OSD/audio-state visualization;
- optional remote transcription backends.

Sources:

- <https://github.com/peteonrails/voxtype>
- <https://github.com/peteonrails/voxtype/blob/dev/docs/USER_MANUAL.md>
- <https://github.com/peteonrails/voxtype/blob/dev/docs/INSTALL.md>

Qualification decision:

VoxType is a strong candidate for **capture/ASR/dictation/meeting adapter reuse** beneath Veragensia/Focusa. Its normal `text -> virtual keyboard/clipboard` output remains compatibility behavior, not canonical semantic voice control.

## 7. Output injection gotcha

Typing text into an application is not equivalent to sending semantic text. Current VoxType supports several injection/fallback paths; current community discussion also notes that translating Unicode text into synthetic keyboard events can depend on keyboard-layout agreement.

Qualification decision:

Use output modes by purpose:

```text
semantic voice/control
    Focusa/Veragensia operations; no auto-paste

legacy dictation field
    clipboard/text injection permitted

meeting capture
    ingest structured transcript/diarization into Focusa Spec 181
```

Do not use synthetic typing for secure approval or trusted control.

## 8. Input-permission gotcha

VoxType compositor bindings are preferable on Hyprland because they do not require broad kernel input-group access merely to detect a hotkey. Some fallback modes use lower-level input mechanisms that can require broader permissions.

Qualification decision:

For a Veragensia governed profile:

- prefer compositor-native trigger integration;
- do not add the owner or agent workloads to broad input groups unless the exact enforcement/security impact is accepted;
- `veragens-audiod` and VoxType-compatible adapter permissions remain independently scoped.

## 9. Hardware/CPU qualification

Current Omarchy/VoxType issue history shows prebuilt binaries can depend on an x86-64-v3/AVX2-class CPU baseline, causing illegal-instruction failures on older CPUs if not preflighted.

Source: <https://github.com/basecamp/omarchy/issues/8312>

The current CC11260 reference profile is an Intel N150 / 4 GB RAM machine, but the physical device and actual runtime capabilities still require qualification under Doc 189.

Qualification decision:

`veragens doctor`/installation preflight should verify:

```text
CPU feature compatibility with selected VoxType binary/engine
model memory/disk requirement
actual microphone/PipeWire availability
ASR latency on the reference workload
idle model unload behavior
```

A large local model must not starve the human-control reserve or ordinary Agent Computer workload.

## 10. Release re-verification gate

Before qualifying the semantic-operation/voice path, re-check:

```text
Omarchy active hotkey/config generation
Omarchy command registry interface
live Hyprland binding introspection
Omarchy dictation integration
installed VoxType version/source
VoxType ASR engine/model requirements
VoxType meeting/diarization behavior
VoxType output/injection behavior
reference hardware CPU/RAM/audio compatibility
```

Record versions/digests/dates in release evidence.
