# Veragensia Omarchy public demo (Docker)

The os.focusa.dev public demo desktop is built from the **same Omarchy overlay and
specs as the native Chromebook install target** (docs/186, docs/187, overlay/omarchy).
Demo = install target; one source of truth.

## Files

- `overlay/webtop/startwm.sh` — replaces the webtop base's DE startup:
  Xvfb hosts Hyprland's X11 backend (Aquamarine needs a seat or parent display;
  containers have neither), then Hyprland starts Waybar + Chromium.
- `overlay/hypr/hyprland.conf` — Hyprland config derived from the pinned Omarchy
  revision structure (presenter autostart, Omarchy-styled decorations).
- `overlay/waybar/config.jsonc` + `style.css` — Waybar presenter.
- `overlay/waybar/veragens-public-waybar.sh` — public-safe presenter renderer:
  reads the dated, curated public Work snapshot packaged with the Chrome
  extension (`/extroot/dist/public-work.json`). **No Focusa daemon connection,
  no private state, no credentials.**
- `omarchy-demo-swap.sh` — atomic container swap with verification and
  automatic rollback (previous container retained as `uiai-webtop.prev`).

## Demo presenter vs native install

| Aspect | Public demo (this directory) | Native Chromebook install |
|---|---|---|
| Work view feed | `/extroot/dist/public-work.json` (curated, dated snapshot packaged with the extension) | `scripts/veragens status --waybar` against the local Focusa daemon |
| Waybar | Presenter of the public snapshot | Live Work status via the Focusa daemon |
| Compositor | Hyprland (X11 backend on Xvfb) captured by selkies on `:1` | Hyprland on real DRM/GPU |
| Chrome extension | Same unpacked dist, same `/extroot/dist` mount path = same extension identity | Same dist via the first-install runbook (docs/187) |

The base image is pinned (`lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a…`),
the selkies streaming stack is kept intact (X11 capture on `:1`), and the swap
script never starts or repairs a Focusa daemon.

## Build and deploy (OVH demo host)

```bash
cd /home/wirebot/veragensia
docker build -t veragensia-omarchy-demo:latest -f docker/omarchy-demo/Dockerfile .
# verification container on temporary loopback ports 3010/3011 first, then:
sudo docker/omarchy-demo/omarchy-demo-swap.sh
```
