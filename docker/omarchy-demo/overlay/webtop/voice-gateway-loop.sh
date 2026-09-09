#!/usr/bin/with-contenv bash
# Voice gateway supervisor: keep the push-to-talk HTTP gateway alive with the
# Hyprland session env (exec-once starts it; it self-heals like chromium-loop).
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/config/.XDG}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-2}"
export HYPRLAND_INSTANCE_SIGNATURE="$(ls /config/.XDG/hypr 2>/dev/null | tail -1)"
if [ "$(id -u)" = "0" ]; then
  exec s6-setuidgid abc python3 /veragensia/docker/omarchy-demo/overlay/webtop/voice-gateway.py
else
  exec python3 /veragensia/docker/omarchy-demo/overlay/webtop/voice-gateway.py
fi
