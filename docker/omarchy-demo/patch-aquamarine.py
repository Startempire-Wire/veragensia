"""Registry version-clamp patch for Aquamarine 0.15.0.

Aquamarine binds Wayland protocol globals with hardcoded versions
(wl_compositor 6, wl_seat 9, ...) and crashes against capture compositors
advertising older globals. Clamp every bind to the advertised version —
same 0.15.0 ABI, one-line behavioral fix.
"""
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
