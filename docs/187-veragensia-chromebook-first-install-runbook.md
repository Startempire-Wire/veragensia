# 187 — Chromebook First Install and Veragensia v0.1 Bring-up

**Status:** operator runbook plus explicit release blockers; not evidence that native v0.1 is already shipped.
**Prepared:** 2026-09-04. **Companion release contract:** [186](186-veragensia-v0.1-native-chromebook-release-spec.md).
**Authority:** Verious Smith III / Doc 185. Firmware changes, disk erasure, enrollment changes, and credential enrollment remain separate operator-controlled actions. This document does not authorize unattended destructive execution.

## 1. Device recovered from the Chromebook conversation

Working target: **Dell Chromebook 11 CC11260**, expected **ULDRENITE**, Intel x86_64. The earlier conversation discussed Omarchy and the required debug cable. Actual purchased RAM/storage configuration and possession of the cable were not recovered as confirmed facts; record them from the arriving device rather than assuming 4 GB, 8 GB, 64 GB, or 128 GB.

MrChromebox currently lists both `ULDRENITE` and the separate `ULDRENITE360` with UEFI Full ROM support. Firmware support is NOT a guarantee of functioning audio, suspend, Wi-Fi, touchscreen, or trackpad under Linux. Hardware identification and OS acceptance are separate gates.

## 2. Before any destructive step

Have owner authorization, charged battery and external power, a second working computer, appropriate USB installation/recovery media, and an off-device backup location. Confirm the Chromebook is not still managed/enrolled by a school or employer. Do not bypass another organization's management.

Read HWID from `chrome://system` or the recovery/developer screen; retain only the board prefix in public evidence. Record actual CPU architecture, RAM, storage capacity, and whether the machine is the clamshell or 2-in-1. Do not publish service tags, full HWIDs, MAC addresses, Wi-Fi credentials, serials, firmware backups, or private screenshots.

Back up anything to preserve **before enabling Developer Mode**; that transition wipes local data. Prepare stock recovery media and read the firmware-restoration procedure. A ChromeOS recovery USB does not by itself undo a replacement Full ROM: restoring stock firmware and restoring the OS are separate operations.

**STOP:** wrong/unlisted board; unclear ownership; no recoverable backup; inadequate power; unavailable required debug equipment; unexplained firmware warnings. Arrival-day urgency does not waive these gates.

## 3. The CCD/Ti50 gate

The supported-device table identifies CR50/Ti50 SuzyQ handling for this family. On Ti50, MrChromebox requires the CCD path to disable AP RO firmware verification, even where another method can disable write protection. Battery disconnection alone is not an adequate substitute.

Use a ChromeOS CCD debug cable (SuzyQ/SuzyQable or explicitly compatible equivalent), not an ordinary USB-C charging cable. Confirm the actual device's security-chip/CCD posture using the current upstream instructions. The cable was discussed in the recovered conversation; its delivery was not established.

Follow the official write-protection procedure interactively. Confirm physical-presence steps, the documented CCD state, and write-protection verification before flashing. Do not copy a generic write-protect-screw tutorial for an older Dell Chromebook. Do not automate firmware flashing from a Veragensia installer.

The stock firmware backup can contain device-specific data. Keep it private and off the Chromebook. Record only a backup-present check and its private integrity check result in the installation record.

## 4. Firmware and stock Omarchy

After the board and CCD gates pass, follow MrChromebox's official Firmware Utility instructions and select the supported UEFI Full ROM path for the actual board. Review the detected device and options before confirming. No hardcoded image filename or bypass of tool compatibility checks is specified here.

Download the stock Omarchy ISO from the official site and follow its current Getting Started instructions. Record the ISO version and integrity metadata available from the publisher. Do not use an arbitrary image mirror or assume a digest computed locally authenticates an image without a trusted reference.

Boot the USB through the installed UEFI. Secure Boot handling follows the actual image/firmware requirements. Do not describe Secure Boot or TPM as Windows-only features, and do not disable unrelated security mechanisms indiscriminately.

Inspect the installation target before confirming disk erasure. A stock Omarchy installation is already the Arch-based path; a separate hand-installed Arch stage is not required when using its supported ISO installer. Keep the stock base unchanged.

Where a live environment permits it, test display/input/network/storage before committing to an installation. After the installed boot, test:

| Area | Required observation |
|---|---|
| Display | Native panel resolution/scaling, brightness adjustment, stable redraw |
| Input | Keyboard/search key, trackpad click/scroll, usable login and recovery console |
| Network | Wi-Fi connection, reconnect, and availability after resume |
| Audio | Speaker, headphone, microphone behavior; do not assume firmware support proves this |
| Power | Battery reporting, charger detection, idle behavior, repeated suspend/resume |
| Storage | Correct capacity, writable home, adequate free space, usable encrypted boot |
| Optional hardware | Touchscreen, Bluetooth, camera as equipped; record unsupported functions |

An unresolved critical input/storage/display failure blocks the native overlay. Audio or suspend defects must be explicit device limitations, not hidden by a successful login.

Useful read-only inventory commands after installing Omarchy:

```bash
uname -m
uname -r
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
pacman -Q omarchy hyprland quickshell
omarchy plugin list --json
```

A missing package or plugin command is evidence of a platform-generation mismatch; it is not permission to edit `/usr/share/omarchy` or install a second shell blindly. Keep raw output local and redact before publishing.

## 5. Inspect Veragensia before running any installer

```bash
git clone https://github.com/Startempire-Wire/veragensia.git
cd veragensia
git status --short
git rev-parse HEAD
cat config/v0.1-release-candidate.json
```

Read Docs 186 and 188. At the baseline used for this planning change, the native installer and `veragens` CLI **do not exist**. `overlay/install.sh` is for the public KDE/webtop stack; **do not run it on the Chromebook as a native installer**.

The candidate manifest's `release_ready: false` and null compatibility/evidence fields are intentional. Cloning these specifications does not install Veragensia v0.1. Never substitute the public `os.focusa.dev` demo for a private local installation.

## 6. A real dependency that can be staged now

The inspected published Focusa release is **v0.9.184**, with Linux x86_64 `focusa` and `focusa-daemon` assets. A newer draft was visible to the connected account, but a draft is not selected as an installation dependency. The following stages the published candidate under a versioned private user directory; it does not start a daemon, enroll credentials, or claim native integration is complete.

The expected digests below were read from the GitHub release API on 2026-09-04. They provide a pinned integrity check against that source, not a claim of an independently signed software attestation. A changed/mismatched artifact is a hard failure.

```bash
set -euo pipefail
umask 077
case "$(uname -m)" in
  x86_64) ;;
  *) printf '%s\n' 'This candidate is for Linux x86_64 only.' >&2; exit 1 ;;
esac
command -v curl >/dev/null
command -v sha256sum >/dev/null
command -v install >/dev/null
stage=$(mktemp -d)
trap 'rm -rf -- "$stage"' EXIT
base='https://github.com/Startempire-Wire/focusa/releases/download/v0.9.184'
curl --proto '=https' --tlsv1.2 --fail --location \
  --connect-timeout 15 --max-time 300 "$base/focusa" -o "$stage/focusa"
curl --proto '=https' --tlsv1.2 --fail --location \
  --connect-timeout 15 --max-time 300 "$base/focusa-daemon" -o "$stage/focusa-daemon"
(
  cd "$stage"
  printf '%s\n' \
    '7e72c30d37e77b592127841e592035a84406e0eff34b6edc98225aec84dbd004  focusa' \
    '1703fedf6317d8cdb39cbc349ce6b3237e778c16225bfead9a7cb51a2dc849b7  focusa-daemon' \
    | sha256sum --check --strict -
)
dest="${XDG_DATA_HOME:-$HOME/.local/share}/veragensia/dependencies/focusa/v0.9.184"
if [ -e "$dest" ]; then
  printf '%s\n' "Already exists; inspect instead of overwriting: $dest" >&2
  exit 1
fi
mkdir -p -- "$dest"
install -m 0755 "$stage/focusa" "$dest/focusa"
install -m 0755 "$stage/focusa-daemon" "$dest/focusa-daemon"
printf '%s\n' "Candidate binaries staged at: $dest"
"$dest/focusa" --version
"$dest/focusa-daemon" --version
```

Run this as the normal user, not root. It deliberately refuses to overwrite an existing version directory. Failed partial staging may leave that new directory; inspect its two files and checksums before operator-directed cleanup or retry. The temporary directory cleanup removes only the directory this command created.

The selected daemon source explicitly implements `--help` and `--version` without startup. Verify the reported version. Staging is not compatibility certification; API/auth/entitlement and real-device smoke tests still apply.

## 7. Daemon activation is a separate gate

Before installing a new service, discover an existing Focusa instance and its data directory. Reuse a compatible owner-controlled instance; never create a second daemon just because the shell failed to connect. Do not delete an existing lock or database to force startup.

The selected source documents `FOCUSA_BIND`, `FOCUSA_DATA_DIR`, and `FOCUSA_AUTH_TOKEN`, with default bind `127.0.0.1:8787`. The native integration must bind privately, enforce/test authentication, preserve the established data directory, and record a safe shutdown/checkpoint path. Do not expose `8787` on LAN/tailnet, put a token in shell history, or assume localhost equals authorization.

The native installer must use an explicit unit/drop-in or the existing Focusa installer contract after it has been checked against the selected release. No guessed daemon startup command, auth bypass, test entitlement, or copied live-server environment is part of this runbook. A valid existing license/provider setup should be enrolled through supported private owner flows.

## 8. Native activation procedure after implementation exists

These are **future acceptance commands**, not currently available functionality:

```text
bash overlay/omarchy/install.sh --check
bash overlay/omarchy/install.sh --apply
veragens doctor --json
veragens status --json
veragens resume --project-root <chosen-root> --continuity-id <existing-id>
```

Before using them, the release manifest must name the actual installer revision, compatible Omarchy version set, Focusa artifact digests, Workforce artifact, tested agent adapter, and evidence. `--check` must make no system changes. Do not fill missing values by guessing.

After activation, execute the Doc 186 reference journey. Test repeat installation, disconnect, shell restart, bounded real-agent work, source-change conflict, cancellation, and rollback. Ordinary desktop use must remain available if Focusa or the bridge is down.

## 9. Arrival-day outcome labels

Use exactly the label supported by evidence:

- **Stock Omarchy ready:** hardware/base acceptance passed; Veragensia not yet integrated.
- **Focusa dependency staged:** verified binaries are present; daemon/native behavior still unproven.
- **Native integration preview:** the actual bridge/plugin work; one or more release gates remain open.
- **Veragensia v0.1 accepted:** all required gates in Doc 186 passed on the recorded hardware/configuration.

A missing SuzyQ/CCD prerequisite can block native firmware installation even when all software is ready. In that case preserve the working ChromeOS installation and continue preparation on the existing development computer; do not weaken firmware checks to meet an arrival date. The user-requested native target remains unchanged.

## 10. Recovery and evidence

Overlay recovery restores only Veragensia-owned changes. It must preserve Focusa state, user projects, credentials, and unrelated Omarchy configuration. Root/OS snapshots, Focusa checkpoints, and run working-directory copies are different objects; do not roll them back indiscriminately together.

Keep a private installation record containing exact versions/digests, hardware checks, failures, and rollback results. Publish only redacted summaries and non-sensitive evidence references. Firmware backup contents, raw journals carrying identity information, and personal browser screenshots never belong in this public repository.

## 11. Primary sources

Checked 2026-09-04; recheck hardware instructions before flashing:

- [MrChromebox supported boards](https://docs.mrchromebox.tech/docs/supported-devices.html).
- [Write protection, CCD, and Ti50 requirements](https://docs.mrchromebox.tech/docs/firmware/wp/disabling.html).
- [MrChromebox prerequisites and warnings](https://docs.mrchromebox.tech/docs/getting-started.html).
- [Firmware Utility](https://docs.mrchromebox.tech/docs/fwscript.html).
- [Omarchy Getting Started](https://omarchy.org/manual/getting-started/).
- [Omarchy plugin contract](https://omarchy.org/manual/shell-plugins/).
- [Focusa published candidate](https://github.com/Startempire-Wire/focusa/releases/tag/v0.9.184) and [release metadata](https://api.github.com/repos/Startempire-Wire/focusa/releases/latest).
- [Selected daemon source and environment/CLI contract](https://github.com/Startempire-Wire/focusa/blob/v0.9.184/crates/focusa-api/src/main.rs).
