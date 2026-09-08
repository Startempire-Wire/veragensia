# Veragensia Omarchy public demo image.
# Base: pinned arch-kde webtop digest (selkies/PIXELFLUX streaming stack kept intact).
# Adds Hyprland + Waybar presenter; replaces the stock KDE Wayland DE startup.
FROM lscr.io/linuxserver/webtop:arch-kde@sha256:ed197a60c161b5d45a0d0137a5c47ecd136964c57791bf3151d01ad41ac6b988

# Hyprland stack + portals + audio (matches the pinned Omarchy dependency set).
RUN pacman -Syu --noconfirm \
        hyprland \
        waybar \
        foot \
        xdg-desktop-portal-hyprland \
        pipewire \
        wireplumber \
    && pacman -Scc --noconfirm || true

# Public-safe overlays: Hyprland config, Waybar presenter, custom DE startup.
COPY --chown=abc:abc docker/omarchy-demo/overlay/webtop/startwm_wayland.sh /defaults/startwm_wayland.sh
COPY --chown=abc:abc docker/omarchy-demo/overlay/hypr/ /veragensia/docker/omarchy-demo/overlay/hypr/
COPY --chown=abc:abc docker/omarchy-demo/overlay/waybar/ /veragensia/docker/omarchy-demo/overlay/waybar/
RUN chmod +x /defaults/startwm_wayland.sh /veragensia/docker/omarchy-demo/overlay/waybar/veragens-public-waybar.sh

ENV DISPLAY=:1 \
    TITLE="Veragensia — Omarchy Public Demo"
