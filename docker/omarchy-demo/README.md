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
- `patch-aquamarine.py` — registry version-clamp patch (see below).
- `omarchy-demo-swap.sh` — atomic container swap with verification and
  automatic rollback (previous container retained as `uiai-webtop.prev`).

## Why the Aquamarine patch

Aquamarine (Hyprland's backend) binds Wayland protocol globals with hardcoded
versions and crashes against capture compositors advertising older globals.
`patch-aquamarine.py` clamps every bind to the advertised version; the image
rebuilds Aquamarine 0.15.0 with it (same ABI; Hyprland stays current).

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
| Compositor | Hyprland nested in the capture compositor (vkms virtual GPU) | Hyprland directly on real DRM/GPU (i915) |
| Chrome extension | Same unpacked dist, same `/extroot/dist` mount path = same extension identity; public build opens the Work view on the default new tab | Same dist via the first-install runbook (docs/187) |

The base image is pinned (`lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a…`),
the selkies/pixelflux streaming stack is kept intact, and the swap script never
starts or repairs a Focusa daemon.

## Build and deploy (OVH demo host)

```bash
cd /home/wirebot/veragensia
docker build -t veragensia-omarchy-demo:latest -f docker/omarchy-demo/Dockerfile .
# verification container on temporary loopback ports 3010/3011 first, then:
sudo docker/omarchy-demo/omarchy-demo-swap.sh
```
