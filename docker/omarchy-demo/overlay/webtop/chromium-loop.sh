#!/usr/bin/with-contenv bash
# Chromium supervisor for the public demo: relaunch the browser with the exact
# demo flags whenever it exits (a closed last window exits the browser and
# would otherwise leave the demo without the Work view surface).
# The flags and the /extroot/dist mount path are the approved public contract —
# identical unpacked extension identity on every relaunch.
# Session defaults make manual restarts outside Hyprland work too; the uid drop
# matches the Wayland socket owner (Hyprland's children run as abc).
export XDG_RUNTIME_DIR="${XDG_RUNTIME_DIR:-/config/.XDG}"
export WAYLAND_DISPLAY="${WAYLAND_DISPLAY:-wayland-2}"
unset DISPLAY
FLAGS=(--show-component-extension-options
  --no-default-browser-check --disable-pings --media-router=0
  --disable-dev-shm-usage --enable-remote-extensions --no-sandbox
  --ozone-platform=wayland --hide-crash-restore-bubble
  --force-device-scale-factor=1.25
  --user-data-dir=/config/.config/chromium-uiai
  --load-extension=/extroot/dist --disable-extensions-except=/extroot/dist
  --remote-debugging-port=9333 --remote-debugging-address=127.0.0.1
  --no-first-run --no-default-browser-check
  --window-size=1180,700 --window-position=190,50)

while true; do
  if [ "$(id -u)" = "0" ]; then
    s6-setuidgid abc /usr/lib/chromium/chromium "${FLAGS[@]}"
  else
    /usr/lib/chromium/chromium "${FLAGS[@]}"
  fi
  code=$?
  echo "[chromium-loop] chromium exited (code $code); relaunching in 3s" >&2
  sleep 3
done
