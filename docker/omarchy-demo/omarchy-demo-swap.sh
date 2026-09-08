#!/bin/bash
# Veragensia Omarchy public demo — atomic container swap with rollback.
# Root-only on the OVH demo host. Never starts or repairs a Focusa daemon.
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
COMMON_ENV=(-e PUID=1001 -e PGID=1001 -e TZ=America/Los_Angeles)
COMMON_PORTS=(-p 127.0.0.1:3000:3000 -p 127.0.0.1:3001:3001)

verify() {
    local name="$1"
    sleep 8
    docker exec "$name" bash -lc 'curl -sf http://127.0.0.1:3000/ >/dev/null' || return 1
    docker exec "$name" bash -lc 'pgrep -f Hyprland >/dev/null' || return 1
    docker exec "$name" bash -lc 'pgrep -f waybar >/dev/null' || return 1
    docker exec "$name" bash -lc 'curl -sf http://127.0.0.1:9333/json | grep -q chrome-extension' || return 1
    return 0
}

echo "[omarchy-demo] verifying new container (canonical ports)..."
if verify "$NEW"; then
    echo "[omarchy-demo] new container healthy; swapping."
    docker stop "$OLD" >/dev/null
    docker rename "$OLD" "$PREV"
    docker stop "$NEW" >/dev/null
    docker rm "$NEW" >/dev/null
    docker run -d --name "$OLD" \
        "${COMMON_BINDS[@]}" "${COMMON_ENV[@]}" "${COMMON_PORTS[@]}" \
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
