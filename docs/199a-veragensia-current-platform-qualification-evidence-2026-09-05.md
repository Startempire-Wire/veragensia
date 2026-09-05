# 199A — Current Platform Qualification Evidence for Ambient Operator

**Status:** dated external-platform evidence companion, 2026-09-05.  
**Companion:** [Doc 199](199-veragensia-ambient-operator-companion-sync-and-omarchy-integration-spec.md).  
**Rule:** this document records current upstream behavior and implementation implications. Upstream behavior may change; re-verify before release qualification.

## 1. Omarchy base reality

Current Omarchy describes itself as Arch Linux + Hyprland + Quickshell.

Source: <https://omarchy.org/manual/>

Implementation implication:

- Veragensia native integration targets normal Arch/Hyprland/Quickshell contracts;
- do not assume KDE/webtop integration behavior applies to native Omarchy;
- exact installed Omarchy/shell version remains a release-gate fact.

## 2. Omarchy shell/plugin model

Current Omarchy documentation states:

- the desktop is one long-lived Quickshell process named `omarchy-shell`;
- first-party plugins live beneath `$OMARCHY_PATH/shell/plugins/`;
- user/third-party plugins live beneath `~/.config/omarchy/plugins/`;
- supported plugin kinds include `bar-widget`, `panel`, `overlay`, `menu`, `service`, and `bar`;
- user plugins run as arbitrary **unsandboxed** code inside the long-lived shell process with the user's permissions;
- `omarchy plugin validate` validates plugin manifests;
- package-owned Omarchy plugin source should be cloned/overridden rather than edited directly.

Source: <https://omarchy.org/manual/shell-plugins/>

### Qualification decision

The proposed `veragensia.ambient` plugin is a **presenter only**.

It MUST NOT be the trusted boundary for:

- credentials/secrets;
- microphone authority;
- Focusa canonical writes;
- capability/authority evaluation;
- EnforcementPlan compilation;
- hardened Secure Attention.

Trusted audio/sync/enforcement behavior stays in separate bounded services/workloads.

## 3. Supported session/user configuration

Current Omarchy documents:

- `~/.config/hypr/autostart.lua` for additional session-start processes;
- `~/.config/omarchy/shell.json` for shell/bar/plugin configuration;
- user config beneath `~/.config` rather than modifications to package-owned source.

Source: <https://omarchy.org/manual/dotfiles/>

### Qualification decision

Early native Veragensia may use supported session autostart for a development bridge, while production service ownership/lifecycle should be explicit and independently testable. Installer work must preserve unrelated user configuration.

## 4. Omarchy audio/Bluetooth operator surfaces

Current Omarchy exposes:

- `omarchy audio` CLI group;
- `omarchy bluetooth` CLI group;
- shell Audio and Bluetooth panels;
- subsystem restart/troubleshooting paths for Audio and Bluetooth.

Sources:

- <https://omarchy.org/manual/omarchy-cli/>
- <https://omarchy.org/manual/hotkeys/>
- <https://omarchy.org/manual/troubleshooting/>

### Qualification decision

`veragens doctor` should inspect actual runtime audio/Bluetooth endpoints and route/profile behavior rather than assume a connected headset implies a working bidirectional microphone profile.

Operator-facing native recovery should reuse/compose supported Omarchy controls where practical rather than invent a second Bluetooth settings stack.

## 5. Omarchy private-network support

Current Omarchy documents installation/use of Tailscale as an optional service with a native shell panel and transfer/control helpers.

Source: <https://omarchy.org/manual/networking/>

### Qualification decision

Tailscale is a strong reference transport for private Companion/Agent Computer synchronization but remains a replaceable transport adapter. Tailnet reachability is not Focusa authority.

## 6. Current Omarchy installation trust posture

Current Omarchy Getting Started documentation says Secure Boot and/or TPM must be turned off in BIOS to install Omarchy. It also installs full-disk encryption by default.

Source: <https://omarchy.org/manual/getting-started/>

### Qualification decision

Do not claim `T2_SIGNED_BOOT`, `T3_MEASURED_BOOT`, or `T4_HARDWARE_ATTESTED` merely from a normal current Omarchy installation.

The default owner-controlled native development profile begins at:

```text
T1_DEVELOPER
```

unless a separate stronger boot/attestation path is implemented and evidenced under Doc 196.

Full-disk encryption remains valuable but is not equivalent to measured/hardware-attested boot.

## 7. Android microphone/background constraints

Current Android documentation requires a microphone foreground-service type and the appropriate microphone/recording permissions for foreground microphone services. `RECORD_AUDIO` is while-in-use sensitive, and Android 14+ prevents normal creation of a microphone foreground service from background state except for defined exceptions. Android 17 further hardens background audio interactions and requires an appropriate visible/foreground-service posture for background audio operations.

Sources:

- <https://developer.android.com/develop/background-work/services/fgs/service-types>
- <https://developer.android.com/develop/background-work/services/fgs/restrictions-bg-start>
- <https://developer.android.com/about/versions/17/changes/bg-audio>

### Qualification decision

A production Android Ambient Companion cannot be specified as an immortal hidden background microphone daemon.

It needs a native platform-aware state machine with explicit user-visible/foreground behavior and states such as:

```text
ambient_ready
wake_listening
active_conversation
meeting_recording
audio_interrupted
background_restricted
suspended_by_platform
```

The existing Termux Phone Bridge remains appropriate for context-only sensor/state proving; it is not the production full-audio runtime.

## 8. iOS audio/background constraints

Apple's AVAudioSession is the supported app/system audio coordination boundary. The `playAndRecord` category supports simultaneous recording/playback and requires recording permission. Background audio execution must be declared through supported background modes; recording/playback sessions can be interrupted by calls, alarms or other nonmixable sessions.

Sources:

- <https://developer.apple.com/documentation/avfaudio/avaudiosession>
- <https://developer.apple.com/documentation/avfaudio/avaudiosession/category-swift.struct/playandrecord>
- <https://developer.apple.com/documentation/xcode/configuring-background-execution-modes>
- <https://developer.apple.com/documentation/BundleResources/Information-Property-List/UIBackgroundModes>

### Qualification decision

The iOS Companion must use supported AVAudioSession/background-mode APIs and report interruptions/suspension honestly. No private Apple APIs, jailbreak assumptions, or synthetic `always_listening` claims.

## 9. Release re-verification gate

Before qualifying a native/Companion release, re-check:

```text
Omarchy shell/plugin generation and manifest contract
Omarchy supported user configuration paths
Omarchy audio/Bluetooth controls and current runtime stack
Omarchy installation/boot trust prerequisites
Android target-SDK microphone/foreground-service rules
iOS AVAudioSession/background-mode rules
```

Record the checked upstream versions/dates in release evidence.

This dated evidence document does not itself prove the target device passes any runtime gate.
