#!/usr/bin/with-contenv bash
# Veragensia Omarchy demo — Wayland DE startup (Hyprland headless + Waybar presenter).
# Replaces the stock KDE startwm_wayland.sh in the webtop base. No X11 session.
ulimit -c 0

export XDG_RUNTIME_DIR="/tmp/xdg-runtime-abc"
mkdir -p -m700 "${XDG_RUNTIME_DIR}"
chown abc:abc "${XDG_RUNTIME_DIR}"

# Hyprland runs headless (no DRM); selkies/PIXELFLUX captures the compositor output.
export WLR_BACKENDS=headless
export WLR_LIBINPUT_NO_DEVICES=1
export WLR_RENDERER_ALLOW_SOFTWARE=1
export XDG_SESSION_TYPE=wayland

# Focusa extension + profile contract: identical flags and mount path as the
# approved public delivery, so the unpacked extension identity is preserved.
exec dbus-run-session -- /usr/bin/Hyprland -c /veragensia/docker/omarchy-demo/overlay/hypr/hyprland.conf
