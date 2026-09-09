#!/bin/bash
# Veragensia Omarchy public demo — atomic container swap with rollback.
# Root-only on the OVH demo host. Never starts or repairs a Focusa daemon.
# Requires the vkms virtual GPU: modprobe vkms (see /etc/modules-load.d/vkms.conf).
#
# Usage: first bring up a candidate container named $NEW yourself (same binds,
# env, devices as COMMON_* below; NO port bindings — the canonical ports stay
# with the running container until the swap moment), confirm the desktop chain
# (Hyprland alive, clients map, Waybar, Chromium CDP) inside it, then run this
# script: it verifies $NEW again on the canonical checks, stops and renames the
# old container to $PREV, starts the Omarchy image as $OLD, verifies, and rolls
# back automatically if the post-swap verification fails.
set -euo pipefail

IMAGE_TAG="veragensia-omarchy-demo:latest"
OLD="uiai-webtop"
PREV="uiai-webtop.prev"
NEW="uiai-webtop-omarchy-new"

HOST_PROFILE="/home/wirebot/webtop"
HOST_EXT="/home/wirebot/uiai-lab/workforce-extension"
HOST_REPO="/home/wirebot/veragensia"
HOST_DEMO="/home/wirebot/uiai-lab/veragensia-demo"

COMMON_BINDS=(-v "${HOST_PROFILE}:/config" -v "${HOST_EXT}:/extroot:ro" -v "${HOST_REPO}:/veragensia:ro" -v "${HOST_DEMO}:/veragensia-demo")
# PIXELFLUX_WAYLAND=true selects the capture compositor's Wayland mode — the
# same env the stock KDE demo runs with. Without it svc-de waits for X11 and
# the Wayland DE (svc-de → startwm_wayland.sh) never starts.
COMMON_ENV=(-e PUID=1001 -e PGID=1001 -e TZ=America/Los_Angeles -e DISPLAY=:1 -e PIXELFLUX_WAYLAND=true -e SELKIES_RENDER_DRI=/dev/dri/card0)
COMMON_PORTS=(-p 127.0.0.1:3000:3000 -p 127.0.0.1:3001:3001)
COMMON_DEVICES=(--device /dev/dri)

clean_profile_locks() {
    # Chromium singleton locks are hostname-bound; a recreated container is a
    # different host. No Chromium runs while this script holds them.
    rm -f "${HOST_PROFILE}/.config/chromium-uiai/Singleton"*
}

verify() {
    local name="$1"
    sleep 8
    docker exec "$name" bash -lc 'curl -sf http://127.0.0.1:3000/ >/dev/null' || return 1
    docker exec "$name" bash -lc 'pgrep -f Hyprland >/dev/null' || return 1
    docker exec "$name" bash -lc 'pgrep -f waybar >/dev/null' || return 1
    # Chromium + extension startup takes well over the 8 s sleep above (Wayland
    # boot, profile load, NTP override redirect). Retry the CDP check briefly
    # instead of failing the whole swap on a slow first boot.
    for _ in 1 2 3 4 5 6; do
        docker exec "$name" bash -lc 'curl -sf http://127.0.0.1:9333/json | grep -q chrome-extension' && return 0
        sleep 10
    done
    return 1
}

clean_profile_locks
echo "[omarchy-demo] verifying new container (canonical ports)..."
if verify "$NEW"; then
    echo "[omarchy-demo] new container healthy; swapping."
    docker stop "$OLD" >/dev/null
    docker rename "$OLD" "$PREV"
    docker stop "$NEW" >/dev/null
    docker rm "$NEW" >/dev/null
    clean_profile_locks
    docker run -d --name "$OLD" \
        "${COMMON_DEVICES[@]}" "${COMMON_BINDS[@]}" "${COMMON_ENV[@]}" "${COMMON_PORTS[@]}" \
        "$IMAGE_TAG" >/dev/null
    if verify "$OLD"; then
        echo "[omarchy-demo] swap complete; previous container retained as ${PREV}."
        exit 0
    else
        echo "[omarchy-demo] post-swap verification failed; rolling back."
        docker stop "$OLD" >/dev/null || true
        docker rm "$OLD" >/dev/null || true
        docker rename "$PREV" "$OLD"
        docker start "$OLD" >/dev/null
        echo "[omarchy-demo] rolled back to previous container."
        exit 1
    fi
else
    echo "[omarchy-demo] new container failed verification; discarding it."
    docker stop "$NEW" >/dev/null || true
    docker rm "$NEW" >/dev/null || true
    exit 1
fi
