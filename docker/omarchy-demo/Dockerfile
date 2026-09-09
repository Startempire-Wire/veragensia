# Veragensia Omarchy public demo image.
# Base: pinned arch-kde webtop digest (selkies/pixelflux streaming stack kept intact).
# Adds Hyprland + Waybar presenter; replaces the stock KDE Wayland DE startup.
FROM lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a60c161b5d45a0d0137a5c47ecd136964c57791bf3151d01ad41ac6b988

# Hyprland stack + portals + audio + build tooling for the compatibility patch.
RUN pacman -Syu --noconfirm \
        hyprland \
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
    && pacman -Scc --noconfirm || true

# Registry version-clamp patch: Aquamarine binds Wayland protocol globals with
# hardcoded versions and crashes against capture compositors advertising older
# globals. Clamp every bind to the advertised version (same 0.15.0 ABI).
COPY docker/omarchy-demo/patch-aquamarine.py /tmp/patch-aquamarine.py
RUN git clone --depth 1 --branch v0.15.0 https://github.com/hyprwm/aquamarine /tmp/aq-src \
    && python3 /tmp/patch-aquamarine.py \
    && cmake -B /tmp/aq-build -S /tmp/aq-src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr >/dev/null \
    && cmake --build /tmp/aq-build -j4 >/dev/null \
    && cmake --install /tmp/aq-build >/dev/null \
    && ldconfig \
    && rm -rf /tmp/aq-src /tmp/aq-build /tmp/patch-aquamarine.py

# Public-safe overlays: Hyprland config, Waybar presenter, custom DE startup.
COPY --chown=abc:abc docker/omarchy-demo/overlay/webtop/startwm_wayland.sh /defaults/startwm_wayland.sh
COPY --chown=abc:abc docker/omarchy-demo/overlay/hypr/ /veragensia/docker/omarchy-demo/overlay/hypr/
COPY --chown=abc:abc docker/omarchy-demo/overlay/waybar/ /veragensia/docker/omarchy-demo/overlay/waybar/
RUN chmod +x /defaults/startwm_wayland.sh /veragensia/docker/omarchy-demo/overlay/waybar/veragens-public-waybar.sh

ENV DISPLAY=:1 \
    TITLE="Veragensia — Omarchy Public Demo"
