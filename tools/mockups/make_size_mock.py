"""TRUCK SIZES (SC=1, 1.5 or 2: 16, 24 or 32 pixel trucks on the 88 pixel road; writes size_<n>.png) - from the
scrolling mock-up: the oval is bigger than the screen and the view follows your truck. Pictures only.
Two versions of the same drive: SMOOTH (the view moves a pixel at a time) and STEP (it moves 8 pixels at a time)."""
import math, numpy as np
from make_arena_mock import *
import os
SC = float(os.environ.get("SC", "1"))
HS, R, HW, RUN = 66, 146, 44, 10
WW, WH = 2 * (HS + R + HW + RUN) + 192, 2 * (R + HW + RUN) + 192
CX, CY = WW // 2, WH // 2
LAP = 4 * HS + 2 * math.pi * R
def pos(s, off=0.0):
    s %= LAP; r = R - off
    if s < HS: return CX - s, CY + r, math.pi
    if s < HS + math.pi * R:
        a = (s - HS) / R; return CX - HS - r * math.sin(a), CY + r * math.cos(a), math.pi + a
    if s < 3 * HS + math.pi * R: return CX - HS + (s - HS - math.pi * R), CY - r, 0.0
    if s < 3 * HS + 2 * math.pi * R:
        a = (s - 3 * HS - math.pi * R) / R; return CX + HS + r * math.sin(a), CY - r * math.cos(a), a
    return CX + HS - (s - 3 * HS - 2 * math.pi * R), CY + r, math.pi
yy, xx = np.mgrid[0:WH, 0:WW]
dx = np.clip(xx - CX, -HS, HS); D = np.hypot(xx - CX - dx, yy - CY); E = np.abs(D - R)
ang = np.arctan2(yy - CY, xx - CX - dx)
dash = ((np.where(np.abs(xx - CX) < HS, xx / 8.0, ang * R / 8.0)).astype(int) % 2) == 0
GREENM = E > HW + RUN
WHITEM = ((E > HW - 2) & (E <= HW) & dash) | ((np.abs(xx - CX) < 4) & (yy > CY) & (E < HW - 2) & (((xx // 4) + (yy // 4)) % 2 == 0))
OIL = np.array([[c == 'X' for c in r] for r in ["........", "..XXXX..", ".XX.XXX.", "XXXXXX.X", "X.XXXXXX", ".XXX.XX.", "..XXXX..", "........"]])
BAR = np.array([[c == 'X' for c in r] for r in BARREL])
x0, y0, _ = pos(HS + 0.9 * R, 12); x1, y1, _ = pos(HS + 2.2 * R, -14); x2, y2, _ = pos(2 * HS + math.pi * R, -16)
THINGS = [(int(x0), int(y0), OIL, BLU), (int(x1), int(y1), BAR, RED), (int(x1) + 8, int(y1), BAR, RED), (int(x2), int(y2), BAR, RED)]
TEAM = [('YOU', 'HAMMER', YEL, 0, -22), ('REX', 'SPIKE', CYN, 78, -20), ('MOG', 'TIPPER', MAG, 40, 20), ('ZED', 'SAW', WHT, 60, 0)]

def frame(f, step):
    s = Screen(); d0 = 20 + f * 5
    px, py, _ = pos(d0, -22); cx, cy = int(px) - 96, int(py) - 96
    if step: cx, cy = cx // 8 * 8, cy // 8 * 8
    for r in range(24):
        for c in range(24):
            g = GREENM[cy + r * 8:cy + r * 8 + 8, cx + c * 8:cx + c * 8 + 8]; w = WHITEM[cy + r * 8:cy + r * 8 + 8, cx + c * 8:cx + c * 8 + 8]
            if g.any(): s.bm[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = g; s.at[r, c] = (GRN, K, 0)
            else: s.bm[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = w; s.at[r, c] = (WHT, K, 1)
    def put(x, y, m, col):
        h, w = m.shape; x, y = int(x) - cx - w // 2, int(y) - cy - h // 2
        if x < 0 or y < 0 or x + w > 192 or y + h > 192: return
        m = m.copy()
        for j in range(h):
            for i in range(w):
                a = s.at[(y + j) // 8, (x + i) // 8]
                if a[0] == GRN: m[j, i] = False
        s.sprite(x, y, m, col)
    for (x, y, m, col) in THINGS: put(x, y, m, col)
    spots = []
    for k, (name, weapon, col, lead, off) in enumerate(TEAM):
        d = d0 + lead
        x, y, h = pos(d, off); spots.append((x, y, col))
        h16 = round((h + math.pi / 2) / (2 * math.pi) * 16) % 16
        m = truck(weapon, 0); n = int(16 * SC)
        m = np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((n, n), Image.NEAREST)) > 127
        put(x, y, turned(m, h16), col)
    s.cells(0, 24, 23, 31, WHT, K)
    s.text(0, 24, ' OVAL 1 ', K, YEL, 1); s.text(2, 25, 'LAP 2/5', WHT)
    for k, (name, weapon, col, lead, off) in enumerate(TEAM):
        s.text(4 + k * 3, 24, ' ' + name + '    ', K, col, 1); s.bar(5 + k * 3, 25, [5, 4, 2, 6][k], 6, col)
    mx, my = 196, 136                                                # mini-map: the whole oval, 56 x 44
    for a in range(0, 400):
        x, y, _ = pos(a * LAP / 400); s.bm[my + int(y * 44 / WH), mx + int(x * 56 / WW)] = True
    for (x, y, col) in spots[:1] if f % 4 < 2 else []:
        u, v = mx + int(x * 56 / WW), my + int(y * 44 / WH); s.bm[v - 1:v + 3, u - 1:u + 3] = True
    for (x, y, col) in spots[1:]:
        u, v = mx + int(x * 56 / WW), my + int(y * 44 / WH); s.bm[v:v + 2, u:u + 2] = True
    s.text(23, 24, '%d x %d' % (int(16 * SC), int(16 * SC)), K, WHT)
    return s

if __name__ == '__main__':
    frame(34, 0).image(2).save(OUT + '/size_%d.png' % int(16 * SC)); print('ok')
