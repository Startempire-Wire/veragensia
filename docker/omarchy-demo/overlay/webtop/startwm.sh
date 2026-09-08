#!/usr/bin/with-contenv bash
# Veragensia Omarchy demo — DE startup: Hyprland (X11 backend) + Waybar.
# Hyprland uses Aquamarine, which needs a seat (absent in containers) or a
# parent display. The webtop base already runs Xvfb on :1 and selkies captures
# that display, so Hyprland connects to it as its backend target.
ulimit -c 0

export XDG_RUNTIME_DIR="/tmp/xdg-runtime-abc"
mkdir -p -m700 "${XDG_RUNTIME_DIR}"
chown abc:abc "${XDG_RUNTIME_DIR}"
export DISPLAY=:1

# Focusa extension + profile contract: identical flags and mount path as the
# approved public delivery, so the unpacked extension identity is preserved.
exec dbus-run-session -- /usr/bin/Hyprland -c /veragensia/docker/omarchy-demo/overlay/hypr/hyprland.conf
