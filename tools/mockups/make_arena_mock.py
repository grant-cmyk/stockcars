"""First-look mock-ups for the arena truck-battle game (ZX Spectrum 48K). Nothing here is game code.
Every picture is a true Spectrum screen: 256x192 pixels, one ink + one paper colour per 8x8 square.
Writes arena.gif, builder.png, weapons.png next to this script."""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.dirname(os.path.abspath(__file__))
PAL = [(0,0,0),(0,0,0xD7),(0xD7,0,0),(0xD7,0,0xD7),(0,0xD7,0),(0,0xD7,0xD7),(0xD7,0xD7,0),(0xD7,0xD7,0xD7)]
PALB = [(0,0,0),(0,0,0xFF),(0xFF,0,0),(0xFF,0,0xFF),(0,0xFF,0),(0,0xFF,0xFF),(0xFF,0xFF,0),(0xFF,0xFF,0xFF)]
K, BLU, RED, MAG, GRN, CYN, YEL, WHT = range(8)
FNT = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf', 8)
_gl = {}
def glyph(ch):
    if ch not in _gl:
        im = Image.new('1', (8, 8), 0); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((1, -1), ch, font=FNT, fill=1); _gl[ch] = np.array(im, dtype=bool)
    return _gl[ch]

class Screen:
    def __init__(s, paper=K, ink=WHT):
        s.bm = np.zeros((192, 256), bool)
        s.at = np.zeros((24, 32, 3), np.uint8); s.at[:, :] = (ink, paper, 0)
    def cells(s, r0, c0, r1, c1, ink, paper, br=0): s.at[r0:r1 + 1, c0:c1 + 1] = (ink, paper, br)
    def text(s, r, c, t, ink=WHT, paper=K, br=0):
        for i, ch in enumerate(t):
            s.bm[r * 8:r * 8 + 8, (c + i) * 8:(c + i) * 8 + 8] = glyph(ch); s.at[r, c + i] = (ink, paper, br)
    def tile(s, r, c, rows, ink, paper, br=0):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row): s.bm[r * 8 + j, c * 8 + i] = ch != '.'
        s.at[r, c] = (ink, paper, br)
    def sprite(s, x, y, m, ink, br=1):
        """OR a sprite in; every square it touches takes the sprite's ink (the real machine's rule)."""
        h, w = m.shape
        for j in range(h):
            for i in range(w):
                if m[j, i] and 0 <= y + j < 192 and 0 <= x + i < 256:
                    s.bm[y + j, x + i] = True; a = s.at[(y + j) // 8, (x + i) // 8]
                    if a[1] == K: a[0] = ink; a[2] = br
    def bar(s, r, c, n, full, ink, br=1):
        for i in range(full):
            s.bm[r * 8 + 2:r * 8 + 6, (c + i) * 8:(c + i) * 8 + 7] = i < n
            if i >= n: s.bm[r * 8 + 3:r * 8 + 5, (c + i) * 8 + 3] = True
            s.at[r, c + i] = (ink, K, br)
    def image(s, scale=3, border=K):
        rgb = np.zeros((192, 256, 3), np.uint8)
        for r in range(24):
            for c in range(32):
                i, p, b = s.at[r, c]; pal = PALB if b else PAL
                blk = s.bm[r * 8:r * 8 + 8, c * 8:c * 8 + 8]
                rgb[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = np.where(blk[..., None], pal[i], pal[p])
        im = Image.fromarray(rgb).resize((256 * scale, 192 * scale), Image.NEAREST)
        fr = Image.new('RGB', (im.width + 16 * scale, im.height + 16 * scale), PAL[border]); fr.paste(im, (8 * scale, 8 * scale))
        return fr

# ---- the truck: 16x16, nose up. Big wheels at the corners, cab in the middle, weapon on the nose ----
BODY = ["................",
        "................",
        "................",
        ".XXX..XXXX..XXX.",
        ".X.XXXXXXXXXX.X.",
        ".XXX.XX..XX.XXX.",
        ".X.X.X....X.X.X.",
        ".XXX.X....X.XXX.",
        ".....XXXXXX.....",
        ".....XX..XX.....",
        ".XXX.XXXXXX.XXX.",
        ".X.XXXXXXXXXX.X.",
        ".XXX.XXXXXX.XXX.",
        ".X.X..XXXX..X.X.",
        ".XXX........XXX.",
        "................"]
WEAPONS = {
 'SPIKE':  [["......X..X......", "......XXXX......", ".....XXXXXX....."],      # twin prongs
            ["......X..X......", "......XXXX......", ".....XXXXXX....."]],
 'HAMMER': [["...XXXXXXXXXX...", "...XXXXXXXXXX...", ".......XX......."],      # head down on the nose
            ["................", ".....XXXXXX.....", ".....XXXXXX....."]],     # head raised (drawn smaller)
 'TIPPER': [["..XXXXXXXXXXXX..", "...X........X...", "....XXXXXXXX...."],      # scoop flat
            ["...XXXXXXXXXX...", "...XXXXXXXXXX...", "....XXXXXXXX...."]],     # scoop flipped up
 'SAW':    [["....X.XXXX.X....", ".....XX..XX.....", "....X.XXXX.X...."],      # disc, teeth one way
            [".....XXXXXX.....", "....XX....XX....", ".....XXXXXX....."]],     # teeth the other way
}
def truck(weapon, frame=0):
    rows = WEAPONS[weapon][frame] + BODY[3:]
    return np.array([[ch == 'X' for ch in r] for r in rows])
def turned(m, heading16):
    im = Image.fromarray((m * 255).astype(np.uint8)).rotate(-heading16 * 22.5, resample=Image.NEAREST)
    return np.array(im) > 127

HAZ = ["XXXX....", ".XXXX...", "..XXXX..", "...XXXX.", "....XXXX", "X....XXX", "XX....XX", "XXX....X"]
BRK = ["XXXXXXX.", "XXXXXXX.", "XXXXXXX.", "........", "XXX.XXXX", "XXX.XXXX", "XXX.XXXX", "........"]
BARREL = ["..XXXX..", ".X....X.", "XXXXXXXX", "X.XXXX.X", "X.XXXX.X", "XXXXXXXX", ".X....X.", "..XXXX.."]
TYRE = ["..XXXX..", ".XXXXXX.", "XXX..XXX", "XX....XX", "XX....XX", "XXX..XXX", ".XXXXXX.", "..XXXX.."]
PIT = ["X.X.X.X.", ".X.X.X.X"] * 4
SPK = ["........", "...X....", "...X....", "..XXX...", "..XXX...", ".XXXXX..", ".XXXXX..", "XXXXXXX."]
FLAME = ["...X....", "..XX..X.", "..XXX.X.", ".XXXXXX.", ".XX.XXX.", "XXX..XXX", "XX....XX", ".XXXXXX."]

TEAM = [('YOU', 'HAMMER', YEL), ('REX', 'SPIKE', CYN), ('MOG', 'TIPPER', MAG), ('ZED', 'SAW', GRN)]

def arena(frame, dmg):
    s = Screen()
    for c in range(24):                                              # wall: brick, with hazard corners
        s.tile(0, c, BRK, WHT, RED); s.tile(23, c, BRK, WHT, RED)
    for r in range(24):
        s.tile(r, 0, BRK, WHT, RED); s.tile(r, 23, BRK, WHT, RED)
    for r, c in [(0, 0), (0, 23), (23, 0), (23, 23)]: s.tile(r, c, HAZ, K, YEL, 1)
    for r in range(10, 14):                                          # the pit, hazard-edged
        for c in range(10, 14):
            edge = r in (10, 13) or c in (10, 13)
            s.tile(r, c, HAZ if edge else PIT, K if edge else BLU, YEL if edge else K, 1 if edge else 0)
    for r, c in [(2, 2), (2, 3), (3, 2)]: s.tile(r, c, BARREL, RED, K, 1)             # barrels
    for r, c in [(21, 21), (21, 20), (20, 21)]: s.tile(r, c, BARREL, RED, K, 1)
    for r, c in [(2, 21), (3, 21), (2, 20)]: s.tile(r, c, TYRE, WHT, K)               # tyre stacks
    for r, c in [(21, 2), (20, 2), (21, 3)]: s.tile(r, c, TYRE, WHT, K)
    for c in (11, 12): s.tile(1, c, SPK[::-1], WHT, K, 1); s.tile(22, c, SPK, WHT, K, 1)   # wall spikes
    fl = FLAME if frame % 4 < 2 else [r[::-1] for r in FLAME]
    for r in (11, 12): s.tile(r, 1, fl, YEL, RED, 1); s.tile(r, 22, fl, YEL, RED, 1)       # flame jets
    # trucks on two rings round the pit, the inner ring the other way
    N = 48
    rings = [(76, 70, 1, 0.0), (56, 52, -1, 0.25), (76, 70, 1, 0.5), (56, 52, -1, 0.75)]
    for k, ((name, weapon, col), (rx, ry, way, ph)) in enumerate(zip(TEAM, rings)):
        out = dmg[k] == 0
        t = (0.5 if out and k == 3 else (frame / N * way + ph)) * 2 * math.pi
        if out: t = (20 / N * way + ph) * 2 * math.pi                # a stopped truck stays where it stopped
        x, y = 96 + rx * math.cos(t), 96 + ry * math.sin(t)
        hd = math.atan2(ry * math.cos(t) * way, -rx * math.sin(t) * way)
        h16 = round((hd + math.pi / 2) / (2 * math.pi) * 16) % 16
        wf = 1 if (frame + k * 5) % 12 < 3 and not out else 0
        if out and frame % 4 < 2: continue                           # a stopped truck blinks
        s.sprite(int(x) - 8, int(y) - 8, turned(truck(weapon, wf), h16), WHT if out else col)
    # side panel
    s.cells(0, 24, 23, 31, WHT, K)
    s.text(0, 24, ' ARENA 1', K, YEL, 1)
    s.text(2, 25, 'TIME', WHT); s.text(3, 25, '1:%02d' % (47 - frame // 8), YEL, K, 1)
    for k, (name, weapon, col) in enumerate(TEAM):
        r = 5 + k * 4
        s.text(r, 24, ' ' + name + '    ', K, col, 1)
        s.text(r + 1, 25, weapon if dmg[k] else 'STOPPED', WHT if dmg[k] else RED, K, 0 if dmg[k] else 1)
        s.bar(r + 2, 25, dmg[k], 6, col)
    s.text(22, 24, 'LAST ONE', WHT); s.text(23, 24, 'MOVING!', YEL, K, 1)
    return s

def builder():
    s = Screen()
    s.text(0, 0, '        BUILD YOUR TRUCK        ', K, YEL, 1)
    big = truck('HAMMER')                                            # preview at 4x: 2x2 art pixels a square
    for j in range(16):
        for i in range(16):
            if big[j, i]: s.bm[24 + j * 4:28 + j * 4, 16 + i * 4:20 + i * 4] = True
    s.cells(3, 2, 10, 9, YEL, K, 1)
    s.cells(2, 1, 11, 10, WHT, BLU); s.cells(3, 2, 10, 9, YEL, K, 1)
    s.text(12, 1, 'CRUSHER 1 ', WHT, BLU)
    rows = [('BODY', ['LIGHT', 'HEAVY', 'TANK'], 1), ('WHEELS', ['GRIP', 'BIG', 'SPIKED'], 1),
            ('WEAPON', ['SPIKE', 'HAMMER', 'TIPPER', 'SAW'], 1), ('DEFENCE', ['NONE', 'PLATE', 'RAM BAR'], 1),
            ('COLOUR', ['YELLOW', 'CYAN', 'PINK', 'GREEN'], 0)]
    for k, (lab, opts, sel) in enumerate(rows):
        r = 2 + k * 2
        s.text(r, 12, lab, CYN, K, 1)
        on = k == 2
        s.text(r, 19, ('<' + opts[sel].center(9) + '>') if on else (' ' + opts[sel].center(9) + ' '), K if on else WHT, YEL if on else K, 1 if on else 0)
    s.text(13, 12, 'SPEED', WHT); s.bar(13, 19, 3, 8, GRN)
    s.text(14, 12, 'TURN', WHT); s.bar(14, 19, 4, 8, GRN)
    s.text(15, 12, 'HIT', WHT); s.bar(15, 19, 7, 8, RED)
    s.text(16, 12, 'TOUGH', WHT); s.bar(16, 19, 5, 8, CYN)
    s.text(18, 12, 'WEIGHT 9 OF 10', YEL, K, 1)
    s.text(14, 1, 'HAMMER:', YEL, K, 1); s.text(15, 1, 'big hit,', WHT); s.text(16, 1, 'slow to', WHT); s.text(17, 1, 'swing', WHT)
    for k, (w, col) in enumerate([('SPIKE', CYN), ('HAMMER', YEL), ('TIPPER', MAG), ('SAW', GRN)]):
        s.sprite(24 + k * 56, 164, truck(w), col); s.text(23, 2 + k * 7, w, col, K, 1)
    s.text(20, 0, ' Q A choose   O P change   ENTER'[:32], K, WHT)
    return s

def weapons():
    """Each weapon at 16 headings would be drawn once and turned; here: nose-up, both frames, 6x."""
    W = 4 * 2 * 16 * 6 + 9 * 12; im = Image.new('RGB', (W, 16 * 6 + 24), (0, 0, 0)); x = 12
    for (w, col) in [('SPIKE', CYN), ('HAMMER', YEL), ('TIPPER', MAG), ('SAW', GRN)]:
        for f in (0, 1):
            a = np.zeros((16, 16, 3), np.uint8); a[truck(w, f)] = PALB[col]
            im.paste(Image.fromarray(a).resize((96, 96), Image.NEAREST), (x, 12)); x += 96 + 12
    return im

if __name__ == '__main__':
    frames = []
    for f in range(48):
        dmg = [5, 4 if f < 30 else 3, 2 if f < 14 else (1 if f < 20 else 0), 6]
        frames.append(arena(f, dmg).image(3))
    frames[0].save(OUT + '/arena.gif', save_all=True, append_images=frames[1:], duration=110, loop=0)
    frames[6].save(OUT + '/arena.png')
    builder().image(3).save(OUT + '/builder.png'); weapons().save(OUT + '/weapons.png')
    print('ok')
