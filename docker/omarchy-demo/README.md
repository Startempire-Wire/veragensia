# Veragensia Omarchy public demo (Docker)

The os.focusa.dev public demo desktop is built from the **same Omarchy overlay and
specs as the native Chromebook install target** (docs/186, docs/187, overlay/omarchy).
Demo = install target; one source of truth.

## Files

- `overlay/webtop/startwm_wayland.sh` — replaces the webtop base's DE startup:
  Hyprland runs **nested inside the pixelflux capture compositor** (the same
  pattern the stock KDE flow uses: the DE compositor connects to
  `WAYLAND_DISPLAY=wayland-1`; the stream captures the parent).
- `overlay/hypr/hyprland.conf` — Hyprland config derived from the pinned Omarchy
  revision structure (presenter autostart, Omarchy-styled decorations).
- `overlay/waybar/config.jsonc` + `style.css` — Waybar presenter.
- `overlay/waybar/veragens-public-waybar.sh` — public-safe presenter renderer:
  reads the dated, curated public Work snapshot packaged with the Chrome
  extension (`/extroot/dist/public-work.json`). **No Focusa daemon connection,
  no private state, no credentials.**
- `patch-aquamarine.py` — build-time patches (see below and `docs/202`).
- `omarchy-demo-swap.sh` — atomic container swap with verification and
  automatic rollback (previous container retained as `uiai-webtop.prev`).

## Why the Aquamarine patches (two independent fixes)

**1. Registry version clamp (always applied at build time).** Aquamarine binds
Wayland protocol globals with hardcoded versions and crashes against capture
compositors advertising older globals. `patch-aquamarine.py` clamps every bind
to the advertised version; the image rebuilds Aquamarine 0.15.0 with it (same
ABI; Hyprland stays current).

**2. wl_shm output presentation (runtime opt-in, `AQ_PRESENT_SHM=1` — set in
`overlay/webtop/startwm_wayland.sh`).** Aquamarine presents every output frame
as a dmabuf buffer; a GPU-less capture compositor cannot import them. With the
env set, frames are presented as plain shared-memory buffers — one memcpy per
frame, the same CPU path ordinary clients use. Without the env, behavior is
identical to upstream.

**3. Initial-configure ack ordering (always applied at build time).** Aquamarine
commits the first real output buffer from its render thread before the
compositor's initial `xdg_surface.configure` is dispatched — a fatal xdg-shell
violation that makes capture compositors kill the connection (~1 s in), leaving
a black stream with no buffer releases. The patch acks first, then kicks the
first frame, and gates real commits on the ack. This — not buffer import — was
the root cause of the black stream; full analysis in
`docs/202-veragensia-omarchy-webtop-nested-compositor-engineering.md`.

## Host requirements (demo host)

- `modprobe vkms` (virtual KMS GPU; persist via `/etc/modules-load.d/vkms.conf`).
  The container needs `--device /dev/dri` and `SELKIES_RENDER_DRI=/dev/dri/card0`
  so the capture compositor and Hyprland allocate buffers on the same node.
- Chromium runs as a Wayland client (`--ozone-platform=wayland`); the extension
  identity comes from the unpacked mount path (`/extroot/dist`), unchanged.

## Demo presenter vs native install

| Aspect | Public demo (this directory) | Native Chromebook install |
|---|---|---|
| Work view feed | `/extroot/dist/public-work.json` (curated, dated snapshot packaged with the extension) | `scripts/veragens status --waybar` against the local Focusa daemon |
| Waybar | Presenter of the public snapshot | Live Work status via the Focusa daemon |
| Compositor | Hyprland nested in the capture compositor (vkms virtual GPU; registry-clamp + `AQ_PRESENT_SHM` wl_shm presentation patches — `docs/202`) | Hyprland directly on real DRM/GPU (i915) — no patches, no nesting |
| Chrome extension | Same unpacked dist, same `/extroot/dist` mount path = same extension identity; public build opens the Work view on the default new tab | Same dist via the first-install runbook (docs/187) |

The base image is pinned (`lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a…`),
the selkies/pixelflux streaming stack is kept intact, and the swap script never
starts or repairs a Focusa daemon.

Full engineering record — failure history (seven documented attempts), the
direct-Hyprland-on-vkms finding, and the verification procedure:
`docs/202-veragensia-omarchy-webtop-nested-compositor-engineering.md`.

## Build and deploy (OVH demo host)

```bash
cd /home/wirebot/veragensia
docker build -t veragensia-omarchy-demo:latest -f docker/omarchy-demo/Dockerfile .
# verification container on temporary loopback ports 3010/3011 first, then:
sudo docker/omarchy-demo/omarchy-demo-swap.sh
```
