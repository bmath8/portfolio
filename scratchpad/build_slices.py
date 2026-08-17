"""Bake the real ICBM152 T1 volume into a tiled slice atlas the browser can sample.

WHY
---
The hero was a grey shell with effects layered on it. Rendering the ACTUAL scan is a
different piece of work: a cross-section plane moving through the cortex, sampling real
T1-weighted voxels, trilinearly interpolated between slices. It is the same dataset the
surface mesh was generated from, so the section always agrees with the anatomy around it.

HOW IT IS PACKED
A 3D texture would be cleaner but costs a WebGL2-only path and a bigger upload. Instead
the volume is tiled into one 2D atlas - GRID x GRID cells, each cell one sagittal slice -
which any WebGL version can sample, and the shader blends between two adjacent cells to
get the third dimension. That is the standard pre-WebGL2 volume trick and it is exact
enough here because the plane is axis-aligned.

Brain-masked, so no skull, eyes or scalp - the mask ships with the template.
Cropped to the brain's bounding box so no atlas space is wasted on empty air.

Output: vendor/mesh/t1-atlas.png  plus the geometry constants the shader needs.
"""
import json, pathlib, sys
import numpy as np

GRID = 10          # 10x10 = 100 slices, plenty for a smooth sweep
CELL = 160         # px per slice cell -> 1600x1600 atlas


def main():
    if len(sys.argv) < 2:
        sys.exit("usage: build_slices.py <dir-with-nii>")
    src = pathlib.Path(sys.argv[1])
    root = pathlib.Path(__file__).resolve().parents[1]
    import nibabel as nib
    from PIL import Image

    t1 = next(src.rglob("*_t1_tal_nlin_sym_09c.nii"))
    mk = next(src.rglob("*_t1_tal_nlin_sym_09c_mask.nii"))
    print(f"T1   {t1.name}\nmask {mk.name}")
    vol = np.asarray(nib.load(str(t1)).dataobj, dtype=np.float32)
    mask = np.asarray(nib.load(str(mk)).dataobj) > 0
    vol = vol * mask                       # strip skull/scalp/eyes

    # crop to the brain so the atlas spends its pixels on anatomy
    nz = np.argwhere(mask)
    lo, hi = nz.min(0), nz.max(0) + 1
    vol = vol[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    print(f"cropped volume {vol.shape}  (was {mask.shape})")

    # window the intensities the way a radiologist would, on the brain voxels only
    inside = vol[vol > 0]
    p2, p98 = np.percentile(inside, 2), np.percentile(inside, 99.5)
    vol = np.clip((vol - p2) / (p98 - p2), 0, 1)
    print(f"intensity window {p2:.1f}..{p98:.1f}")

    # The mesh was remapped (x, z, -y). Sagittal slices step along the mesh's X, which is
    # the volume's first axis, so the atlas indexes that axis directly.
    nS = GRID * GRID
    xs = np.linspace(0, vol.shape[0] - 1, nS)
    atlas = Image.new("L", (GRID * CELL, GRID * CELL), 0)
    for i, x in enumerate(xs):
        x0, x1 = int(np.floor(x)), min(int(np.ceil(x)), vol.shape[0] - 1)
        f = x - x0
        sl = vol[x0] * (1 - f) + vol[x1] * f              # (Y, Z)
        # orient to match the mesh axis remap (x, z, -y): rows = -y, cols = z
        img = np.flipud(sl.T)
        im = Image.fromarray((img * 255).astype(np.uint8)).resize((CELL, CELL), Image.LANCZOS)
        atlas.paste(im, ((i % GRID) * CELL, (i // GRID) * CELL))

    # WebP: 284 KB against 876 KB for the same 100 slices as PNG, visually identical
    # at this bit depth. Lossless PNG buys nothing on data that is already smoothed.
    out = root / "vendor" / "mesh" / "t1-atlas.webp"
    atlas.save(out, "WEBP", quality=88, method=6)
    kb = out.stat().st_size / 1024
    print(f"\nwrote {out.name}  {GRID}x{GRID} cells of {CELL}px  {kb:.0f} KB")

    meta = {"grid": GRID, "cell": CELL, "slices": nS,
            "shape": [int(v) for v in vol.shape],
            "note": "sagittal slices along the mesh X axis; cols=z, rows=-y"}
    (root / "vendor" / "mesh" / "t1-atlas.json").write_text(json.dumps(meta, indent=1))
    print(json.dumps(meta))


if __name__ == "__main__":
    main()
