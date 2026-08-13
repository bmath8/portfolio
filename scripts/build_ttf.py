"""Convert the self-hosted woff2 faces to TTF so Pillow can draw with them.

Pillow cannot read woff2. The OG card scripts need the exact faces the site
serves, so this produces TTF copies as a build artifact. They are not deployed.

    pip install fonttools brotli
    python scripts/build_ttf.py
"""
import glob, os, sys
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "vendor", "fonts")
DST = os.path.join(ROOT, "scratchpad", "vendorbuild", "ttf")

os.makedirs(DST, exist_ok=True)
n = 0
for f in glob.glob(os.path.join(SRC, "*.woff2")):
    name = os.path.splitext(os.path.basename(f))[0]
    try:
        t = TTFont(f)
        t.flavor = None
        t.save(os.path.join(DST, name + ".ttf"))
        n += 1
    except Exception as e:
        print("skip", name, e, file=sys.stderr)
print("converted %d faces -> %s" % (n, DST))
