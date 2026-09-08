#!/usr/bin/with-contenv bash
# Veragensia Omarchy demo — DE startup: Hyprland (X11 backend on Xvfb) + Waybar.
# Hyprland uses Aquamarine, which needs a seat (absent in containers) or a
# parent display. Xvfb provides the parent display; selkies captures :1.
ulimit -c 0

export XDG_RUNTIME_DIR="/tmp/xdg-runtime-abc"
mkdir -p -m700 "${XDG_RUNTIME_DIR}"
chown abc:abc "${XDG_RUNTIME_DIR}"

rm -f /tmp/.X1-lock /tmp/.X11-unix/X1
Xvfb :1 -screen 0 1280x760x24 -nolisten tcp &
for i in $(seq 1 20); do [ -f /tmp/.X11-unix/X1 ] && break; sleep 0.3; done
export DISPLAY=:1

# Focusa extension + profile contract: identical flags and mount path as the
# approved public delivery, so the unpacked extension identity is preserved.
exec dbus-run-session -- /usr/bin/Hyprland -c /veragensia/docker/omarchy-demo/overlay/hypr/hyprland.conf
