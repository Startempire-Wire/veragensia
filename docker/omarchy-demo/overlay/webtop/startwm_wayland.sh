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
  # AQ_PRESENT_SHM=1 selects Aquamarine\'s wl_shm presentation path (see
  # patch-aquamarine.py): on GPU-less hosts the capture compositor cannot import
  # Hyprland\'s dmabuf output buffers and deadlocks every nested client. wl_shm
  # frames are ordinary CPU buffers the compositor composites like any other.
  WAYLAND_DISPLAY=wayland-1 AQ_PRESENT_SHM=1 /usr/bin/Hyprland -c /veragensia/docker/omarchy-demo/overlay/hypr/hyprland.conf &
  HYPID=$!
  sleep 6
  wait $HYPID
'
