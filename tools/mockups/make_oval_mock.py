"""Oval-track mock-up for the weapon-truck racer (ZX Spectrum 48K). Pictures only, not game code.
Black road, dashed white limit line, black run-off, green grass: the Breakfast Run 'racetrack' look."""
import math, numpy as np
from make_arena_mock import *
CX, CY, HS, R, HW, RUN = 96, 100, 18, 46, 16, 10      # centre, half straight, bend radius, half road, run-off
LAP = 4 * HS + 2 * math.pi * R
def pos(s, off=0.0):
    """Point on the lap at distance s (clockwise, starting mid bottom straight), off = pixels towards the infield."""
    s %= LAP; r = R - off
    if s < HS: x, y, h = CX - s, CY + r, math.pi                                   # bottom straight, heading left
    elif s < HS + math.pi * R:
        a = (s - HS) / R; x, y, h = CX - HS - r * math.sin(a), CY + r * math.cos(a), math.pi + a
    elif s < 3 * HS + math.pi * R: x, y, h = CX - HS + (s - HS - math.pi * R), CY - r, 0.0
    elif s < 3 * HS + 2 * math.pi * R:
        a = (s - 3 * HS - math.pi * R) / R; x, y, h = CX + HS + r * math.sin(a), CY - r * math.cos(a), a
    else: x, y, h = CX + HS - (s - 3 * HS - 2 * math.pi * R), CY + r, math.pi
    return x, y, h
yy, xx = np.mgrid[0:192, 0:192]
dx = np.clip(xx - CX, -HS, HS); D = np.hypot(xx - CX - dx, yy - CY)                # distance to the infield spine
E = np.abs(D - R)
ang = np.arctan2(yy - CY, xx - CX - dx)
dash = ((np.where(np.abs(xx - CX) < HS, xx / 8.0, ang * R / 8.0)).astype(int) % 2) == 0
GREENM = E > HW + RUN
WHITEM = (E > HW - 2) & (E <= HW) & dash
CROWD = ["XX..XX..", "XX..XX..", "..XX..XX", "..XX..XX"] * 2
CHQ = ["XXXX....", "XXXX....", "XXXX....", "XXXX....", "....XXXX", "....XXXX", "....XXXX", "....XXXX"]
OIL = ["........", "..XXXX..", ".XX.XXX.", "XXXXXX.X", "X.XXXXXX", ".XXX.XX.", "..XXXX..", "........"]
RAMP = ["XXXXXXXX", "X......X", ".XXXXXX.", ".X....X.", "..XXXX..", "..X..X..", "...XX...", "........"]
TEAM = [('YOU', 'HAMMER', YEL), ('REX', 'SPIKE', CYN), ('MOG', 'TIPPER', MAG), ('ZED', 'SAW', WHT)]

def track(frame):
    s = Screen()
    for r in range(24):
        for c in range(24):
            g = GREENM[r * 8:r * 8 + 8, c * 8:c * 8 + 8]; w = WHITEM[r * 8:r * 8 + 8, c * 8:c * 8 + 8]
            if g.all(): s.at[r, c] = (K, GRN, 0)
            elif g.any(): s.bm[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = g; s.at[r, c] = (GRN, K, 0)
            else: s.bm[r * 8:r * 8 + 8, c * 8:c * 8 + 8] = w; s.at[r, c] = (WHT, K, 1)
    for c in range(24): s.tile(0, c, CROWD, [YEL, CYN, WHT, MAG][c % 4], BLU, 1); s.tile(1, c, BRK, WHT, RED)
    for r in (16, 17, 18, 19): s.tile(r, 12, CHQ, WHT, K, 1)                        # start / finish line
    s.tile(4, 9, BARREL, RED, K, 1); s.tile(4, 10, BARREL, RED, K, 1)               # barrels, top straight, outside
    s.tile(11, 5, OIL, BLU, K, 1)                                                    # oil, left bend
    s.text(11, 9, 'LAP  2', K, GRN); s.text(12, 9, 'OF   5', K, GRN)
    v = LAP / 48
    hit = 14 <= frame < 26                                                           # YOU's hammer catches MOG
    order = []
    for k, (name, weapon, col) in enumerate(TEAM):
        f = frame if k != 2 else (frame if frame < 14 else max(14, frame - 12))
        d = f * v + [40, 150, 64, 250][k]
        x, y, h = pos(d, [-5, -4, 5, -4][k])
        h16 = round((h + math.pi / 2) / (2 * math.pi) * 16) % 16
        if k == 2 and hit: h16 = (h16 + (frame - 14) * 3) % 16                       # MOG spins
        wf = 1 if (k == 0 and 11 <= frame < 14) or (k and (frame + k * 5) % 12 < 2) else 0
        m = turned(truck(weapon, wf), h16)
        for j in range(16):                                                          # edge squares keep their green
            for i in range(16):
                if m[j, i]:
                    a = s.at[(int(y) - 8 + j) // 8, (int(x) - 8 + i) // 8]
                    if a[0] == GRN and a[1] == K: m[j, i] = False
        s.sprite(int(x) - 8, int(y) - 8, m, col)
        order.append((-(d + (0 if k != 2 else 0)), k))
    s.cells(0, 24, 23, 31, WHT, K)
    s.text(0, 24, ' OVAL 1 ', K, YEL, 1)
    armour = [5, 4, 3 if frame < 14 else 1, 6]
    for n, (_, k) in enumerate(sorted(order)):
        name, weapon, col = TEAM[k]; r = 2 + n * 5
        s.text(r, 24, '%d %s   ' % (n + 1, name), K, col, 1)
        s.text(r + 1, 25, weapon, WHT)
        s.text(r + 2, 25, 'SPIN!' if k == 2 and hit else 'ARMOUR', RED if k == 2 and hit else CYN, K, 1)
        s.bar(r + 3, 25, armour[k], 6, col)
    s.text(22, 24, 'M = FIRE', WHT); s.text(23, 24, 'WEAPON', WHT)
    return s

if __name__ == '__main__':
    fr = [track(f).image(3) for f in range(48)]
    fr[0].save(OUT + '/oval.gif', save_all=True, append_images=fr[1:], duration=110, loop=0)
    fr[8].save(OUT + '/oval.png'); fr[16].save(OUT + '/oval_hit.png'); print('ok')
