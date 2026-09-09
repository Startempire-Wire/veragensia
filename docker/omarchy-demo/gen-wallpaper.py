"""Generate the Veragensia public demo wallpaper (1280x760 PNG).

Pure stdlib (zlib + struct + math) so it runs anywhere without image libraries.
Design: deep navy-to-charcoal vertical gradient, a soft teal radial glow, and
the Veragensia droplet mark (teal drop with tip up) left of center. Public-safe:
no text, no private assets, deterministic output.
"""
import math
import struct
import zlib

W, H = 1280, 760
OUT = '/home/wirebot/veragensia/docker/omarchy-demo/overlay/hypr/veragensia-wallpaper.png'

# Palette (matches the Work view teal accent).
TOP = (10, 14, 26)        # deep navy
BOTTOM = (15, 12, 28)     # charcoal plum
TEAL = (45, 212, 191)     # Work view accent
GLOW = (20, 56, 66)


def droplet_field(dx: float, dy: float) -> float:
    """Approximate signed distance for a teardrop with the tip pointing up.

    (dx, dy) are normalized by the drop radius; dy grows downward. Returns the
    distance to the boundary (negative inside).
    """
    length = math.hypot(dx, dy) or 1e-9
    # Tip direction: up = dy negative. t in [0,1] grows toward the tip.
    t = max(0.0, -dy / length)
    radius = 1.0 - 0.93 * t ** 1.35
    return length - radius


def render() -> bytes:
    rows = []
    for j in range(H):
        v = j / (H - 1)
        base = tuple(int(TOP[k] + (BOTTOM[k] - TOP[k]) * v) for k in range(3))
        row = bytearray([0])  # PNG filter type 0 (None) — required per scanline
        for i in range(W):
            u = i / (W - 1)
            # Soft radial teal glow left-of-center.
            gx, gy = 0.40, 0.47
            dist = math.hypot((u - gx) * 1.4, (v - gy) * 1.9)
            glow = max(0.0, 1.0 - dist / 0.60) ** 2
            r = base[0] + GLOW[0] * glow * 0.75 + TEAL[0] * glow * 0.14
            g = base[1] + GLOW[1] * glow * 0.75 + TEAL[1] * glow * 0.14
            b = base[2] + GLOW[2] * glow * 0.75 + TEAL[2] * glow * 0.14
            # Droplet: normalized coords (drop radius ~ 0.13 of width).
            dx = (u - gx) / 0.13
            dy = (v - gy) / 0.26
            field = droplet_field(dx, dy)
            if field < 0.06:
                inside = field < 0.0
                rim = max(0.0, 1.0 - abs(field) / 0.06)
                fill = 0.10 + 0.10 * glow
                if inside:
                    r = r * (1 - fill) + 10 * fill
                    g = g * (1 - fill) + 26 * fill
                    b = b * (1 - fill) + 24 * fill
                r += TEAL[0] * rim * 1.05
                g += TEAL[1] * rim * 0.9
                b += TEAL[2] * rim * 0.9
            # Gentle vignette.
            vig = 1.0 - 0.20 * (abs(u - 0.5) * 1.5 + (0.5 - min(v, 1 - v)) * 0.30)
            row.extend((max(0, min(255, int(r * vig))), max(0, min(255, int(g * vig))), max(0, min(255, int(b * vig)))))
        rows.append(bytes(row))
    def chunk(tag: bytes, data: bytes) -> bytes:
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    raw = b''.join(rows)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw, 6)) + chunk(b'IEND', b''))


with open(OUT, 'wb') as f:
    f.write(render())
print('wrote', OUT)
