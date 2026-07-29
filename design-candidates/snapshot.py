#!/usr/bin/env python3
"""Snapshot design candidates before iterating, so a good state is never lost.

Git already versions these, but git history is awkward to eyeball when you're
comparing visual states. This keeps browsable, dated copies you can open side by
side in a browser.

    python snapshot.py              # snapshot every candidate
    python snapshot.py G            # snapshot just G-*.html
    python snapshot.py --list       # show what snapshots exist
"""
import os
import sys
import glob
import shutil
import datetime
import hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
VERS = os.path.join(HERE, "_versions")


def digest(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:10]


def latest_snapshot_of(base):
    """Most recent snapshot for a candidate, so we can skip no-op saves."""
    hits = sorted(glob.glob(os.path.join(VERS, "*", base + "_*.html")))
    return hits[-1] if hits else None


def snapshot(prefix=None):
    stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    dest = os.path.join(VERS, stamp)
    pattern = f"{prefix}*.html" if prefix else "[A-Z]-*.html"
    files = sorted(glob.glob(os.path.join(HERE, pattern)))
    if not files:
        sys.exit(f"no candidates matched {pattern}")

    saved, skipped = [], []
    for f in files:
        base = os.path.splitext(os.path.basename(f))[0]
        prev = latest_snapshot_of(base)
        # Don't pile up identical copies — only snapshot real changes.
        if prev and digest(prev) == digest(f):
            skipped.append(base)
            continue
        os.makedirs(dest, exist_ok=True)
        shutil.copy2(f, os.path.join(dest, f"{base}_{stamp}.html"))
        saved.append(base)

    if saved:
        print(f"snapshot -> _versions/{stamp}/")
        for s in saved:
            print(f"   saved   {s}")
    for s in skipped:
        print(f"   skipped {s} (unchanged since last snapshot)")
    if not saved:
        print("nothing changed — no snapshot written")
    return dest


def listing():
    days = sorted(glob.glob(os.path.join(VERS, "*")))
    if not days:
        print("no snapshots yet")
        return
    for d in days:
        files = sorted(os.path.basename(x) for x in glob.glob(os.path.join(d, "*.html")))
        print(f"{os.path.basename(d)}  ({len(files)})")
        for f in files:
            print(f"    {f}")


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    if "--list" in args:
        listing()
    else:
        snapshot(args[0] if args else None)
