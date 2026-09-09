# Veragensia Omarchy public demo image.
# Base: pinned arch-kde webtop digest (selkies/pixelflux streaming stack kept intact).
# Adds Hyprland + Waybar presenter; replaces the stock KDE Wayland DE startup.
FROM lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a60c161b5d45a0d0137a5c47ecd136964c57791bf3151d01ad41ac6b988

# Hyprland stack + portals + audio + build tooling for the compatibility patches.
# swaybg serves the generated Veragensia wallpaper on the demo desktop.
# ENABLE_RESIZE=False: every connecting browser otherwise resizes the whole
# capture pipeline (resolution churn = the resize-transition glitches and
# pipeline restarts). The demo desktop stays at its native 1280x760 and the
# client letterboxes. MPL-2.0 patch to the installed selkies package.
RUN pacman -Syu --noconfirm --ignore docker-compose \
        hyprland \
        swaybg \
        waybar \
        foot \
        xdg-desktop-portal-hyprland \
        pipewire \
        wireplumber \
        cmake \
        ninja \
        git \
        gcc \
        libdisplay-info \
    && pacman -Scc --noconfirm || true \
    && sed -i 's/^ENABLE_RESIZE = True$/ENABLE_RESIZE = False/' /lsiopy/lib/python3*/site-packages/selkies/selkies.py

# Two build-time patches (see patch-aquamarine.py for rationale and design notes):
#   1. Registry version clamp — Aquamarine binds Wayland protocol globals with
#      hardcoded versions and crashes against capture compositors advertising
#      older globals. Clamp every bind to the advertised version.
#   2. wl_shm presentation path (opt-in at runtime via AQ_PRESENT_SHM=1) — lets
#      Hyprland present output frames as plain shared-memory buffers so the
#      capture compositor can composite them on GPU-less hosts (startwm_wayland.sh
#      sets the env for this image).
COPY docker/omarchy-demo/patch-aquamarine.py /tmp/patch-aquamarine.py
RUN git clone --depth 1 --branch v0.15.0 https://github.com/hyprwm/aquamarine /tmp/aq-src \
    && python3 /tmp/patch-aquamarine.py \
    && cmake -B /tmp/aq-build -S /tmp/aq-src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr >/dev/null \
    && cmake --build /tmp/aq-build -j4 >/dev/null \
    && cmake --install /tmp/aq-build >/dev/null \
    && ldconfig \
    && rm -rf /tmp/aq-src /tmp/aq-build /tmp/patch-aquamarine.py

# Voice client and same-origin gateway route are image-owned so a container
# restart cannot erase the mobile control. The runtime patch remains available
# for the mounted source overlay and future base-image changes.
COPY --chown=abc:abc docker/omarchy-demo/overlay/selkies-web/veragensia-voice.js /usr/share/selkies/selkies-dashboard/src/veragensia-voice.js
COPY docker/omarchy-demo/overlay/webtop/voice-page-patch.py /usr/local/bin/veragensia-voice-page-patch.py
RUN VERAGENSIA_VOICE_INDEX=/usr/share/selkies/selkies-dashboard/index.html \
    VERAGENSIA_VOICE_TARGET=/usr/share/selkies/selkies-dashboard/src/veragensia-voice.js \
    VERAGENSIA_VOICE_NGINX=/defaults/default.conf \
    python3 /usr/local/bin/veragensia-voice-page-patch.py \
    && chmod 0644 /usr/share/selkies/selkies-dashboard/src/veragensia-voice.js

# Public-safe overlays: Hyprland config, Waybar presenter, custom DE startup.
COPY --chown=abc:abc docker/omarchy-demo/overlay/webtop/startwm_wayland.sh /defaults/startwm_wayland.sh
COPY --chown=abc:abc docker/omarchy-demo/overlay/hypr/ /veragensia/docker/omarchy-demo/overlay/hypr/
COPY --chown=abc:abc docker/omarchy-demo/overlay/waybar/ /veragensia/docker/omarchy-demo/overlay/waybar/
RUN chmod +x /defaults/startwm_wayland.sh /veragensia/docker/omarchy-demo/overlay/waybar/veragens-public-waybar.sh

ENV DISPLAY=:1 \
    TITLE="Veragensia — Omarchy Public Demo" \
    SELKIES_MANUAL_WIDTH=1280 \
    SELKIES_MANUAL_HEIGHT=760
