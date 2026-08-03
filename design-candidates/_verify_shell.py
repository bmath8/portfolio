#!/usr/bin/env python3
"""Verify the implicit brain field produces a usable point shell BEFORE judging it in a
browser. Mirrors the JS field() in hero-particles.html exactly.

Checks: fill rate, bounding box, left/right balance, midline fissure, and prints an
ASCII front + side projection so the silhouette is visible without WebGL.
"""
import math
import random

random.seed(7)


def hash3(x, y, z):
    s = math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453
    return s - math.floor(s)


def vnoise(x, y, z):
    xi, yi, zi = math.floor(x), math.floor(y), math.floor(z)
    xf, yf, zf = x - xi, y - yi, z - zi
    u = xf * xf * (3 - 2 * xf)
    v = yf * yf * (3 - 2 * yf)
    w = zf * zf * (3 - 2 * zf)
    n = 0.0
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                wt = (u if i else 1 - u) * (v if j else 1 - v) * (w if k else 1 - w)
                n += wt * hash3(xi + i, yi + j, zi + k)
    return n * 2 - 1


def field(x, y, z):
    lobe = 1 - (((abs(x) - 1.55) / 3.45) ** 2 + (y / 3.05) ** 2 + (z / 3.7) ** 2)
    cere = 1 - ((x / 2.0) ** 2 + ((y + 2.85) / 1.15) ** 2 + ((z + 1.5) / 1.5) ** 2)
    stem = 1 - ((x / 0.52) ** 2 + ((y + 3.5) / 1.5) ** 2 + ((z + 0.35) / 0.62) ** 2)
    f = max(lobe, cere * 0.94, stem * 0.9)
    return f + vnoise(x * 1.15, y * 1.15, z * 1.15) * 0.135


TARGET = 14000
pts, tries = [], 0
while len(pts) < TARGET and tries < TARGET * 260:
    tries += 1
    x = (random.random() * 2 - 1) * 5.6
    y = (random.random() * 2 - 1) * 4.9
    z = (random.random() * 2 - 1) * 4.6
    f = field(x, y, z)
    if f < 0.008 or f > 0.14:
        continue
    if abs(x) < 0.135 and random.random() < 0.82:
        continue
    pts.append((x, y, z))

print(f"points: {len(pts)} / {TARGET}   tries: {tries}   accept rate: {len(pts)/tries*100:.2f}%")
if not pts:
    raise SystemExit("FAIL: field produced no points")

xs = [p[0] for p in pts]; ys = [p[1] for p in pts]; zs = [p[2] for p in pts]
print(f"bbox  x[{min(xs):+.2f},{max(xs):+.2f}]  y[{min(ys):+.2f},{max(ys):+.2f}]  z[{min(zs):+.2f},{max(zs):+.2f}]")
L = sum(1 for x in xs if x < 0); R = len(xs) - L
print(f"hemispheres  left {L}  right {R}  skew {abs(L-R)/len(xs)*100:.1f}%")
mid = sum(1 for x in xs if abs(x) < 0.135)
print(f"midline fissure: {mid} pts ({mid/len(pts)*100:.2f}%) — want under ~2%")


def render(a, b, w=64, h=30, la="x", lb="y"):
    amin, amax = min(a), max(a); bmin, bmax = min(b), max(b)
    grid = [[0] * w for _ in range(h)]
    for av, bv in zip(a, b):
        cx = int((av - amin) / (amax - amin) * (w - 1))
        cy = int((bv - bmin) / (bmax - bmin) * (h - 1))
        grid[h - 1 - cy][cx] += 1
    mx = max(max(r) for r in grid) or 1
    ramp = " .:-=+*#%@"
    print(f"\n  {la} x {lb}")
    for row in grid:
        print("  " + "".join(ramp[min(len(ramp) - 1, int(c / mx * (len(ramp) - 1) * 2.4))] for c in row))


render(xs, ys, la="x", lb="y")   # front
render(zs, ys, la="z", lb="y")   # side
