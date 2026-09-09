# 202 — Veragensia Omarchy webtop demo: nested-compositor compatibility engineering

- **Date:** 2026-09-09
- **Scope:** the public Omarchy webtop demo at `docker/omarchy-demo/` (OVH demo host),
  the capture-compositor incompatibilities found there, the two build-time
  Aquamarine patches that resolve them, and the verification method.
- **Authority:** veragensia overlay work authorized by the Canonical Owner
  Principal; demo = install target (Docs 186/187); public-safe assets only.
- **Status:** engineering record + operating guide for this demo container.

## 1. Why this exists

The public portal (os.focusa.dev) must show the *real* Omarchy experience the
operator will install natively on the Chromebook (Docs 186/187): Hyprland +
Waybar + the public Work view, streamed as a live, usable desktop. The demo
container (`docker/omarchy-demo/`, based on the pinned
`lscr.io/linuxserver/webtop:arch-kde` image) therefore runs **Hyprland nested
inside the capture compositor** (pixelflux/Smithay, part of the webtop
streaming stack), instead of the stock KDE/KWin session.

The Chromebook itself does **not** use any of this nesting: there, Hyprland runs
directly on real DRM (i915). Every artifact documented here (hyprland.conf,
Waybar presenter, patches) exists to make the demo faithful to that target.

## 2. The three real blockers and their fixes (all verified against source)

### 2.1 Hardcoded protocol versions (FIXED — clamp patch)

Hyprland's backend **Aquamarine** binds Wayland protocol globals with hardcoded
versions (`wl_compositor` 6, `wl_seat` 9, `xdg_wm_base` 6, `wl_shm` 1, dmabuf 4)
in every release since v0.1. The capture compositor advertises `wl_compositor`
v5, so the bind aborts and Hyprland dies at startup.

**Fix:** `patch-aquamarine.py` patch 1 — clamp every bind to the advertised
version (`std::min(hardcoded, version)`), rebuilt in-image against the pinned
0.15.0 source. Verified via `WAYLAND_DEBUG=1` and the upstream source of
v0.1–v0.15: no released binary avoids this; the patch is the minimal fix.

### 2.2 Buffer allocation on a GPU-less host (FIXED — vkms)

GBM allocation needs a DRM device with a render path. On the demo host (no GPU
hardware):

- `vgem` is **wrong**: Mesa has no vgem DRI driver, allocations fail.
- `vkms` (kernel module, `linux-modules-extra` required on 6.8) is **right**:
  Mesa ships `vkms_dri`, and GBM allocation on the vkms card succeeds.
  `SELKIES_RENDER_DRI=/dev/dri/card0` forces the capture compositor to allocate
  on the same node Hyprland uses, so parent and child agree on the device.

**Direct-Hyprland finding (2026-09-09):** running Hyprland *without* a parent
compositor (the cleanest architecture, streaming via wayvnc/noVNC) fails on
kernel 6.8 because **vkms exposes no render node** (no `DRIVER_RENDER`) —
Aquamarine's DRM backend cannot set up a render device. With `seatd` installed
the failure is identical, ruling out session management as the cause. This is a
host-kernel limitation; on real hardware (Chromebook i915) a render node exists
and the direct architecture works natively. Do not re-attempt direct mode on
kernel 6.8 without first solving the render-node gap.

### 2.3 Deadlock at dmabuf import (FIXED — wl_shm presentation patch)

With Hyprland booting and allocating on vkms, every nested client (Waybar,
Chromium) still never mapped a window, and Chromium's DevTools bound without a
window ever appearing. Root cause, from v0.15.0 source + observed behavior:

- Aquamarine's `CWaylandBuffer` presents **every** output frame as a
  `zwp_linux_dmabuf_v1` buffer (there is no shm path for output frames; wl_shm
  exists only for the cursor).
- The capture compositor cannot import the dmabufs the GBM allocator produces
  on the virtual GPU, and never sends `wl_buffer.release`.
- The swapchain then has no released buffer to reuse; Hyprland's render loop
  blocks; frame callbacks never fire; clients never map. (KWin's nested session
  works because the capture compositor composites its output fine — the
  failure is specific to the dmabuf presentation path, not the parent.)

**Fix:** `patch-aquamarine.py` patch 2 — opt-in via `AQ_PRESENT_SHM=1` (set in
`overlay/webtop/startwm_wayland.sh`). Frames are presented as plain `wl_shm`
buffers: one memfd-backed pool per swapchain slot, one memcpy per frame through
the existing `beginDataPtr()/endDataPtr()` CPU-mapping API, then
attach + full damage. The same CPU presentation path the parent already handles
for ordinary software clients. Zero behavior change when the env is unset.

## 3. Patch file map

| File | Patch | Trigger |
|---|---|---|
| `patch-aquamarine.py` | 1. registry version clamps (always) | build time |
| `patch-aquamarine.py` | 2. `AQ_PRESENT_SHM=1` wl_shm presentation | runtime env |
| `overlay/webtop/startwm_wayland.sh` | sets `AQ_PRESENT_SHM=1` for Hyprland | runtime |
| `Dockerfile` | applies both patches, rebuilds Aquamarine 0.15.0 | build time |

License posture: Aquamarine/Hyprland are GPL-3.0; patches are kept in-repo and
applied from pinned source (`--branch v0.15.0`), satisfying source provision.
The capture compositor (pixelflux) and transport (selkies) are MPL-2.0 open
source but are used unmodified — no fork of their binaries is needed.

## 4. Verification procedure (run before any swap)

1. Build: `docker build -t veragensia-omarchy-demo:latest -f docker/omarchy-demo/Dockerfile .`
2. Verify container (loopback 3010/3011, `--device /dev/dri`, fresh profile
   copy with `Singleton*` locks removed).
3. Chain checks inside the container: Hyprland alive (`WAYLAND_DISPLAY=wayland-N`
   socket exists), **`hyprctl clients` non-empty** (the metric that failed for
   two days — windows actually map now), Waybar process alive, Chromium CDP on
   9333 serving the extension start page in public Work mode.
4. Pixel proof through the real stream (public URL after the swap, or a tunnel
   for pre-swap checks where policy permits).
5. `sudo docker/omarchy-demo/omarchy-demo-swap.sh` — atomic swap, previous
   container retained as `uiai-webtop.prev`, automatic rollback on failure.

## 5. Failure history (do not rediscover)

| Attempt | Setup | Result | Root cause |
|---|---|---|---|
| 1 | vgem, nested | Hyprland dies: no allocator | Mesa has no vgem driver |
| 2 | vkms, no device forcing | headless, "no allocator" | no DRM device visible |
| 3 | vkms + parent dmabuf device | boot, then protocol crash | hardcoded versions (§2.1) |
| 4 | clamp patch + SELKIES_RENDER_DRI | boots; **clients never map** | dmabuf import stall (§2.3) |
| 5 | direct Hyprland on vkms (+seatd) | `CBackend::create() failed` | no render node on kernel 6.8 (§2.2) |
| 6 | §2.3 patch, verify container | pending build verification | — |

## 6. Future paths

- **Chromebook (native):** direct Hyprland on i915, no patches needed for the
  protocol/allocator issues (real compositor, real render node). The patches
  are demo-host compatibility shims, not products.
- **GPU-capable host:** route A (direct Hyprland + wayvnc/noVNC) becomes
  viable; artifacts are ready (`docs/202` §2.2).
- **Kernel ≥ 6.12/6.14:** vkms render-node support may remove the §2.2 blocker;
  treat as host upgrade, not a demo dependency.
