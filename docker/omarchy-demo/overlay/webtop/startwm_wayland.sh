#!/usr/bin/with-contenv bash
# Veragensia Omarchy demo — DE startup: Hyprland nested in the pixelflux
# capture compositor (same pattern as the stock KDE Wayland flow, which runs
# the DE compositor against WAYLAND_DISPLAY=wayland-1 under dbus-run-session).
# Hyprland needs a seat or a parent Wayland compositor; the pixelflux
# compositor provides the parent, and the stream captures its output.
ulimit -c 0

# Focusa extension + profile contract: identical flags and mount path as the
# approved public delivery, so the unpacked extension identity is preserved.
# Ozone auto selects the Wayland backend under Hyprland.
exec dbus-run-session bash -c '
  WAYLAND_DISPLAY=wayland-1 /usr/bin/Hyprland -c /veragensia/docker/omarchy-demo/overlay/hypr/hyprland.conf &
  HYPID=$!
  sleep 6
  wait $HYPID
'
