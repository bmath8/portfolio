"""Derive the palette in OKLCH, ship it as hex.

From the OKLCH Color Picker / Color.review entries on designengineer.tools.
The reason to author in OKLCH rather than hex: lightness is perceptually
uniform, so a five-step surface ramp actually steps by equal perceived
amounts, and four data hues at the SAME L and C are equally loud - none
of them shouts over the others. That is not true of HSL, where a yellow
at 50% L is far brighter than a blue at 50% L.

It ships as hex because everything downstream has to read it: THREE.Color
does not parse oklch(), nor does canvas 2D, nor does the contrast audit.
The OKLCH source values stay in the CSS as comments so the ramp can be
re-derived instead of nudged.
"""
import math

def oklch_to_srgb(L, C, H):
    h = math.radians(H)
    a, b = C*math.cos(h), C*math.sin(h)
    l_ = L + 0.3963377774*a + 0.2158037573*b
    m_ = L - 0.1055613458*a - 0.0638541728*b
    s_ = L - 0.0894841775*a - 1.2914855480*b
    l, m, s = l_**3, m_**3, s_**3
    r = +4.0767416621*l - 3.3077115913*m + 0.2309699292*s
    g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s
    bl= -0.0041960863*l - 0.7034186147*m + 1.7076147010*s
    def enc(u):
        u = max(0.0, min(1.0, u))
        return 12.92*u if u <= 0.0031308 else 1.055*u**(1/2.4) - 0.055
    return tuple(round(enc(v)*255) for v in (r, g, bl))

def hexof(L, C, H):
    return "#%02x%02x%02x" % oklch_to_srgb(L/100, C, H)

def lum(rgb):
    def f(v):
        v /= 255
        return v/12.92 if v <= 0.03928 else ((v+0.055)/1.055)**2.4
    r, g, b = (f(c) for c in rgb)
    return .2126*r + .7152*g + .0722*b

def ratio(a, b):
    la, lb = lum(a), lum(b)
    return (max(la, lb)+.05)/(min(la, lb)+.05)

HUE_N = 255          # neutrals: a hint of cool, not enough to read as blue
TOK = [
    # name        L     C      H
    ("s0",       13,  0.006, HUE_N),   # page
    ("s1",       18,  0.008, HUE_N),   # band
    ("s2",       23,  0.009, HUE_N),   # panel
    ("s3",       29,  0.011, HUE_N),   # raised / hover
    ("s4",       36,  0.013, HUE_N),   # chip
    ("rule",     44,  0.016, HUE_N),
    ("rule-q",   26,  0.010, HUE_N),
    ("bracket",  59,  0.020, HUE_N),
    ("tx0",      97,  0.003, HUE_N),
    ("tx1",      83,  0.011, HUE_N),
    ("tx2",      73,  0.015, HUE_N),
]
# The four data hues share ONE lightness and ONE chroma. Only hue varies.
DATA_L, DATA_C = 78, 0.125
DATA = [("d-daily", 162), ("d-hourly", 278), ("d-weekly", 76), ("d-monthly", 12)]

vals = {}
print("/* ---- SURFACE / RULE / TEXT ---- */")
for n, L, C, H in TOK:
    hx = hexof(L, C, H); vals[n] = hx
    print(f"  --{n:<9}{hx};   /* oklch({L}% {C} {H}) */")
print("\n/* ---- DATA (one L, one C, four hues) ---- */")
for n, H in DATA:
    hx = hexof(DATA_L, DATA_C, H); vals[n] = hx
    print(f"  --{n:<9}{hx};   /* oklch({DATA_L}% {DATA_C} {H}) */")

def rgb(h): return tuple(int(h[i:i+2], 16) for i in (1, 3, 5))

print("\nCONTRAST (need 4.5 body / 3.0 large):")
worst = 99
for t in ("tx0", "tx1", "tx2"):
    row = []
    for g in ("s0", "s1", "s2", "s3", "s4"):
        r = ratio(rgb(vals[t]), rgb(vals[g])); row.append(f"{g} {r:5.2f}")
        worst = min(worst, r)
    print(f"  {t:<5}" + "  ".join(row))
print("\nDATA hue vs s1 (dots/marks, non-text):")
for n, _ in DATA:
    print(f"  {n:<11}{ratio(rgb(vals[n]), rgb(vals['s1'])):5.2f}")
print(f"\nworst text pair: {worst:.2f}  ->  {'PASS' if worst >= 4.5 else 'FAIL'}")
