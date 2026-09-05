# 189 — Dell Chromebook 11 CC11260 Reference Hardware Profile

**Status:** reference hardware evidence for the Veragensia v0.1 bring-up target; device-arrival verification still required.
**Prepared:** 2026-09-04.
**Authority:** Verious Smith III / Doc 185.
**Companions:** 186 (v0.1 release), 187 (first install), 188 (integration contracts).

## 1. Purchased configuration now identified

The seller-provided shipment screenshot identifies the incoming machine as:

```text
Dell Chromebook 11 CC11260
Intel Processor N150
4 GB RAM
64 GB eMMC
11.6-inch Chromebook
```

Do **not** commit the screenshot, tracking state, seller transaction information, delivery location, serial/service tag, or other shipment metadata to this repository. This document retains only the hardware facts needed for engineering.

Dell's current official CC11260 configuration confirms the matching clamshell base specification: Intel N150, 4 GB LPDDR5, 64 GB onboard eMMC, and an 11.6-inch non-touch HD display. The platform is a low-power four-core/four-thread N150 design and is therefore the actual constrained-hardware target for v0.1 performance work, not an assumed higher-memory Chromebook.

Primary reference: <https://www.dell.com/en-us/shop/dell-laptops/dell-chromebook-11-laptop-or-2-in-1/spd/chromebook-cc11260-2-in-1-laptop>

## 2. Firmware board mapping

MrChromebox's supported-device table and device database map the clamshell **Dell Chromebook 11 CC11260** to board/HWID family **`ULDRENITE`**. The separate CC11260 2-in-1 maps to **`ULDRENITE360`**. The clamshell `ULDRENITE` entry currently lists RW_LEGACY and UEFI Full ROM support and CR50/Ti50 (SuzyQ) write-protection handling.

Primary references:

- <https://docs.mrchromebox.tech/docs/supported-devices.html>
- <https://github.com/MrChromebox/scripts/blob/main/device-db.sh>

This mapping is strong external evidence, but the actual incoming Chromebook's HWID remains the destructive-operation gate. Read the real board prefix on arrival before any firmware write. If it does not begin with the expected supported family, stop and re-evaluate.

## 3. v0.1 engineering consequences

This machine fixes the first native performance envelope at **4 GB RAM / 64 GB eMMC**. That changes the implementation posture from “support constrained hardware someday” to “prove the first complete experience here.”

Required consequences:

- no mandatory resident local LLM;
- exactly one Focusa daemon for the local owner context;
- one lightweight Veragensia session bridge, not one service per cognitive primitive;
- at most one active governed agent run in v0.1;
- Focusa constrained/LowMem behavior must remain available and must be exercised during acceptance;
- no browser fleet, local Firecracker requirement, or multiple always-running agent runtimes;
- bounded projection/event queues and compact UI state;
- foreground input and shell responsiveness have priority over background cognition;
- eMMC write amplification and free-space pressure must be measured, including logs, browser profile, Focusa persistence, build/output staging, and rollback metadata;
- compilation of large Rust/browser stacks is not an installation requirement on this device; consume pinned build artifacts where the existing projects support them.

## 4. Device-arrival facts still unknown

Do not mark G01 hardware acceptance complete until the physical unit establishes:

- actual HWID/board prefix;
- actual RAM visible to Linux and usable memory after boot;
- actual eMMC capacity/free space and health behavior;
- firmware/security-chip/write-protection state and CCD prerequisites;
- display panel behavior and scaling;
- keyboard and trackpad behavior;
- Wi-Fi and Bluetooth behavior;
- speaker, headphone and microphone behavior;
- battery/charger reporting;
- repeated suspend/resume;
- camera and any other equipped hardware;
- stock recovery and firmware-backup readiness before destructive work.

Seller/OEM specifications establish the reference configuration. They do not prove the shipped unit is healthy or that every peripheral works under Linux.

## 5. Performance evidence to collect on first Omarchy boot

Record private raw evidence and publish only redacted summaries:

```bash
uname -m
uname -r
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
lscpu
pacman -Q omarchy hyprland quickshell
systemd-analyze
systemd-analyze blame
```

Then record idle and interactive memory separately for: base desktop/session, Focusa daemon, Veragensia bridge/plugin, Chromium + Workforce, and one bounded agent worker. Measure browser/profile disk usage and free eMMC space before and after the reference work cycle.

Do not derive a general “4 GB supported” product claim from a single successful boot. v0.1 acceptance proves this exact reference workload and hardware profile; broader minimum requirements need repeated hardware evidence.

## 6. Relationship to Docs 186 and 187

The earlier statements in Docs 186/187 that RAM and storage had not yet been recovered are superseded by this evidence: the purchased listing provides **4 GB RAM and 64 GB eMMC**, and Dell corroborates the matching configuration. The remaining warnings in those documents about actual-board, firmware and Linux-functional verification still apply unchanged.
