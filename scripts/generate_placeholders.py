"""
generate_placeholders.py
Writes three placeholder PNGs to assets/images/ using only stdlib (struct + zlib).
Run from any directory: python scripts/generate_placeholders.py
"""
import struct, zlib, os, math

# ── project root is one level above this script ──────────────────────────────
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

def asset(name):
    return os.path.join(PROJECT_ROOT, 'assets', 'images', name)


# ── raw PNG writer ────────────────────────────────────────────────────────────
def write_png(path, width, height, rows, has_alpha=True):
    """rows: list of H lists, each containing W tuples of (R,G,B) or (R,G,B,A)."""
    def chunk(tag, data):
        c = tag + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xFFFFFFFF)

    color_type = 6 if has_alpha else 2          # 6=RGBA, 2=RGB
    bpp        = 4 if has_alpha else 3
    ihdr = struct.pack('>IIBBBBB', width, height, 8, color_type, 0, 0, 0)

    raw = b''
    for row in rows:
        raw += b'\x00'                          # filter byte: None
        for px in row:
            raw += bytes(px[:bpp])

    png = (
        b'\x89PNG\r\n\x1a\n'
        + chunk(b'IHDR', ihdr)
        + chunk(b'IDAT', zlib.compress(raw, 9))
        + chunk(b'IEND', b'')
    )
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        f.write(png)
    print(f'  {path}')


# ── friend.png ─── 150×150 RGBA yellow smiley face ───────────────────────────
def make_friend():
    W = H = 150
    cx = cy = W // 2
    R = 62                                      # circle radius

    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            dx, dy = x - cx, y - cy
            d       = math.hypot(dx, dy)
            left_e  = math.hypot(dx + 20, dy + 16)
            right_e = math.hypot(dx - 20, dy + 16)
            smile_r = math.hypot(dx, dy - 8)
            on_smile = (26 < smile_r < 33) and dy > 8

            if d <= R - 2:
                if left_e < 9 or right_e < 9:
                    row.append((30,  30,  30, 255))   # eyes
                elif on_smile:
                    row.append((30,  30,  30, 255))   # smile
                else:
                    row.append((255, 210,  40, 255))  # yellow face
            elif d <= R + 1.5:
                row.append((60,  60,  60, 255))       # outline
            else:
                row.append((0, 0, 0, 0))              # transparent
        rows.append(row)

    write_png(asset('friend.png'), W, H, rows, has_alpha=True)


# ── background.png ─── 400×800 RGB sky gradient ──────────────────────────────
def make_background():
    W, H = 400, 800
    # top: cornflower #87CEEB  →  bottom: pale sky #C9E8F5
    rows = []
    for y in range(H):
        t   = y / (H - 1)
        r   = int(135 + (201 - 135) * t)
        g   = int(206 + (232 - 206) * t)
        b   = int(235 + (245 - 235) * t)
        rows.append([(r, g, b)] * W)

    write_png(asset('background.png'), W, H, rows, has_alpha=False)


# ── pipe.png ─── 80×80 RGB green tile (tiled/stretched by the game) ──────────
def make_pipe():
    W = H = 80
    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            border    = x < 5 or x >= W - 5 or y < 5 or y >= H - 5
            highlight = (8 <= x <= 16) and not border
            if border:
                row.append(( 27,  94,  32))   # dark green edge
            elif highlight:
                row.append((129, 199, 132))   # light stripe
            else:
                row.append(( 56, 142,  60))   # main green
        rows.append(row)

    write_png(asset('pipe.png'), W, H, rows, has_alpha=False)


# ── ground.png ─── 400×80 RGB tan ground strip ───────────────────────────────
def make_ground():
    W, H = 400, 80
    GRASS_H = 16          # green band at top of the strip

    rows = []
    for y in range(H):
        row = []
        for x in range(W):
            if y < GRASS_H:
                # subtle checkerboard on grass for texture
                checker = ((x // 8) + (y // 8)) % 2
                r, g, b = (76, 175, 80) if checker else (66, 160, 70)
            elif y == GRASS_H:
                r, g, b = 40, 120, 40   # dark divider line
            else:
                # sandy dirt with slight noise via deterministic pattern
                stripe = ((x + y * 3) // 12) % 3
                r = 194 + stripe * 4
                g = 154 + stripe * 3
                b =  88 + stripe * 2
                r, g, b = min(r, 255), min(g, 255), min(b, 255)
            row.append((r, g, b))
        rows.append(row)

    write_png(asset('ground.png'), W, H, rows, has_alpha=False)


# ── main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Generating placeholder images...')
    make_friend()
    make_background()
    make_pipe()
    make_ground()
    print('Done — 4 files written to assets/images/')
