"""Build og.png (1200x630) in the Mission Control palette.

Uses the same self-hosted faces the live page uses, so the link preview and the
page agree. No network, no generated imagery -- everything below is drawn.
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG      = (4, 6, 10)
PANEL   = (12, 21, 32)
LINE    = (29, 48, 66)
LINE2   = (44, 74, 99)
TXT     = (234, 243, 251)
DIM     = (147, 170, 191)
FAINT   = (76, 99, 122)
GREEN   = (74, 240, 160)
ICE     = (111, 211, 255)
AMBER   = (255, 196, 77)
VIOLET  = (179, 155, 255)

FONTS = sys.argv[1] if len(sys.argv) > 1 else "vendor/fonts"
def f(name, size):
    return ImageFont.truetype(f"{FONTS}/{name}.woff2", size)

# Pillow can't read woff2 directly -- convert first (done by the caller).
def ttf(name, size):
    return ImageFont.truetype(f"{FONTS}/_ttf/{name}.ttf", size)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# ---- atmosphere: green glow top-right, ice glow bottom-left ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r in range(560, 0, -8):
    a = int(16 * (1 - r / 560) ** 2)
    gd.ellipse([880 - r, -160 - r, 880 + r, -160 + r], fill=(74, 240, 160, a))
for r in range(460, 0, -8):
    a = int(10 * (1 - r / 460) ** 2)
    gd.ellipse([80 - r, 700 - r, 80 + r, 700 + r], fill=(111, 211, 255, a))
img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- perspective grid, echoing the hero canvas ----
HZ = 430
for i in range(30):
    x = i / 29 * W
    d.line([(x, H), (W / 2 + (x - W / 2) * 0.10, HZ)], fill=(74, 240, 160, 18), width=1)
for i in range(1, 11):
    p = i / 10
    y = HZ + (H - HZ) * (p ** 2.2)
    d.line([(0, y), (W, y)], fill=(111, 211, 255, int(10 + p * 20)), width=1)

# ---- scanlines ----
for y in range(0, H, 3):
    d.line([(0, y), (W, y)], fill=(255, 255, 255, 4), width=1)

PAD = 72

# ---- status line ----
mono = ttf("ibm-plex-mono-500", 19)
d.ellipse([PAD, 62, PAD + 10, 72], fill=GREEN)
d.text((PAD + 22, 56), "BRIAN MATHEW", font=ttf("ibm-plex-mono-600", 19), fill=TXT)
d.text((PAD + 222, 56), "NJ  ·  OPEN TO WORK", font=mono, fill=DIM)

# ---- headline ----
h1 = ttf("archivo-900", 78)
d.text((PAD, 122), "I build systems,", font=h1, fill=TXT)
d.text((PAD, 210), "then I ", font=h1, fill=TXT)
w_then = d.textlength("then I ", font=h1)
# accent phrase with a soft glow behind it
acc = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ad = ImageDraw.Draw(acc)
ad.text((PAD + w_then, 210), "keep them", font=h1, fill=(74, 240, 160, 255))
ad.text((PAD, 298), "running.", font=h1, fill=(74, 240, 160, 255))
blur = acc.filter(__import__("PIL.ImageFilter", fromlist=["ImageFilter"]).GaussianBlur(18))
img = Image.alpha_composite(img.convert("RGBA"), blur)
img = Image.alpha_composite(img, acc).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")

# ---- sub line ----
sub = ttf("archivo-500", 23)
d.text((PAD, 402), "26 scheduled agents run unattended on my machine right now.", font=sub, fill=DIM)
d.text((PAD, 434), "Every number says where it came from.", font=sub, fill=DIM)

# ---- metric strip ----
BX, BY, BW, BH = PAD, 486, W - PAD * 2, 92
d.rounded_rectangle([BX, BY, BX + BW, BY + BH], radius=10, fill=PANEL, outline=LINE, width=1)
cells = [("26", "AGENTS LIVE", GREEN),
         ("81/81", "TESTS GREEN", ICE),
         ("3", "SYSTEMS SHIPPED", AMBER),
         ("0", "MANUAL TRIGGERS", VIOLET)]
cw = BW / 4
num_f = ttf("archivo-800", 38)
lbl_f = ttf("ibm-plex-mono-500", 15)
for i, (num, lbl, col) in enumerate(cells):
    cx = BX + cw * i
    # gradient top edge
    for gx in range(int(cw) - 2):
        a = int(230 * (1 - gx / (cw - 2)) ** 1.5)
        d.line([(cx + 1 + gx, BY + 1), (cx + 1 + gx, BY + 3)], fill=col + (a,))
    d.text((cx + 26, BY + 20), num, font=num_f, fill=col)
    d.text((cx + 27, BY + 64), lbl, font=lbl_f, fill=DIM)
    if i:
        d.line([(cx, BY + 1), (cx, BY + BH - 1)], fill=LINE, width=1)

# ---- right side: radar mark ----
CX, CY, R = 1010, 250, 118
for i in range(1, 5):
    d.ellipse([CX - R * i / 4, CY - R * i / 4, CX + R * i / 4, CY + R * i / 4],
              outline=(74, 240, 160, 40 + i * 14), width=1)
d.line([(CX - R, CY), (CX + R, CY)], fill=(74, 240, 160, 40), width=1)
d.line([(CX, CY - R), (CX, CY + R)], fill=(74, 240, 160, 40), width=1)
# sweep wedge
sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(sweep)
for k in range(46):
    a0 = -34 - k
    sd.pieslice([CX - R, CY - R, CX + R, CY + R], a0, a0 + 2,
                fill=(74, 240, 160, int(52 * (1 - k / 46))))
img = Image.alpha_composite(img.convert("RGBA"), sweep).convert("RGB")
d = ImageDraw.Draw(img, "RGBA")
# blips
import random
random.seed(7)
for i in range(9):
    ang = math.radians(i / 9 * 360 + 18)
    rr = R * (0.3 + ((i * 41) % 62) / 100)
    bx, by = CX + math.cos(ang) * rr, CY + math.sin(ang) * rr
    hot = i in (1, 2)
    d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=GREEN if hot else (74, 240, 160, 150))
    if hot:
        d.ellipse([bx - 8, by - 8, bx + 8, by + 8], outline=(74, 240, 160, 90), width=1)
d.text((CX - 96, CY + R + 22), "SCHEDULER · SWEEP 6H", font=ttf("ibm-plex-mono-400", 14), fill=FAINT)

# ---- url ----
d.text((PAD, H - 46), "bmath8.vercel.app", font=ttf("ibm-plex-mono-500", 17), fill=GREEN)
d.text((PAD + 205, H - 46), "·  github.com/bmath8", font=ttf("ibm-plex-mono-400", 17), fill=FAINT)

img.save(sys.argv[2] if len(sys.argv) > 2 else "og.png", "PNG", optimize=True)
print("wrote", sys.argv[2] if len(sys.argv) > 2 else "og.png")
