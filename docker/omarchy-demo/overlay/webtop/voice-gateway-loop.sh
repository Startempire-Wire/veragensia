#!/usr/bin/with-contenv bash
# Voice gateway supervisor: keep the push-to-talk HTTP gateway alive with the
# Hyprland session env (exec-once starts it; restart after transient failures).
set -u

export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/config/.XDG}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-2}"
GATEWAY=/veragensia/docker/omarchy-demo/overlay/webtop/voice-gateway.py
trap 'exit 0' TERM INT

while :; do
  signature="$(ls /config/.XDG/hypr 2>/dev/null | tail -1)"
  if [ -n "$signature" ]; then
    export HYPRLAND_INSTANCE_SIGNATURE="$signature"
  fi
  if [ "$(id -u)" = "0" ]; then
    s6-setuidgid abc python3 "$GATEWAY"
  else
    python3 "$GATEWAY"
  fi
  exit_code=$?
  echo "veragensia voice gateway exited ($exit_code); retrying" >&2
  sleep 1
done
