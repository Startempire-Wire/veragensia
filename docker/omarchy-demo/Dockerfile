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

# Registry version-clamp patch: Aquamarine binds protocol globals with hardcoded
# versions (wl_compositor 6, wl_seat 9, ...) and crashes against capture
# compositors advertising older globals. Clamp every bind to the advertised
# version — same 0.15.0 ABI, one-line behavioral fix (upstream-hyprwm issue).
RUN git clone --depth 1 --branch v0.15.0 https://github.com/hyprwm/aquamarine /tmp/aq-src \
    && python3 - <<'PY'
import pathlib
p = pathlib.Path('/tmp/aq-src/src/backend/Wayland.cpp')
src = p.read_text()
pairs = [
    ('&wl_seat_interface, 9)', '&wl_seat_interface, std::min(9u, version))'),
    ('&xdg_wm_base_interface, 6)', '&xdg_wm_base_interface, std::min(6u, version))'),
    ('&wl_compositor_interface, 6)', '&wl_compositor_interface, std::min(6u, version))'),
    ('&wl_shm_interface, 1)', '&wl_shm_interface, std::min(1u, version))'),
    ('&zwp_linux_dmabuf_v1_interface, 4)', '&zwp_linux_dmabuf_v1_interface, std::min(4u, version))'),
]
count = 0
for old, new in pairs:
    if old in src:
        src = src.replace(old, new)
        count += 1
assert count == 5, f'expected 5 bind sites, patched {count}'
p.write_text(src)
print(f'patched {count} bind sites')
PY \
    && cmake -B /tmp/aq-build -S /tmp/aq-src -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr >/dev/null \
    && cmake --build /tmp/aq-build -j4 >/dev/null \
    && cmake --install /tmp/aq-build >/dev/null \
    && ldconfig \
    && rm -rf /tmp/aq-src /tmp/aq-build

# Public-safe overlays: Hyprland config, Waybar presenter, custom DE startup.
COPY --chown=abc:abc docker/omarchy-demo/overlay/webtop/startwm_wayland.sh /defaults/startwm_wayland.sh
COPY --chown=abc:abc docker/omarchy-demo/overlay/hypr/ /veragensia/docker/omarchy-demo/overlay/hypr/
COPY --chown=abc:abc docker/omarchy-demo/overlay/waybar/ /veragensia/docker/omarchy-demo/overlay/waybar/
RUN chmod +x /defaults/startwm_wayland.sh /veragensia/docker/omarchy-demo/overlay/waybar/veragens-public-waybar.sh

ENV DISPLAY=:1 \
    TITLE="Veragensia — Omarchy Public Demo"
