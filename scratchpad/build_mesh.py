"""Rebuild the cortical surface from the MNI ICBM152 2009c template.

WHY THIS EXISTS
---------------
The mesh that shipped had lost its folds. Measured 2026-08-07:
    71.4% of the surface essentially flat (per-vertex normal spread < 0.01)
    surface area 940 cm^2 against ~1800 cm^2 for a real folded cortex  (0.52x)
Brian's complaint that "the colors erased all the definition" was only half the
story - roughly half the fold geometry was not in the mesh at all, and no shader
recovers geometry that is not there.

The previous pipeline (per notes; the script itself never existed in git) leaned on
Taubin smoothing to keep the silhouette clean. Taubin is shrink-free but it is still
a low-pass filter: it removes exactly the high-frequency detail that IS the gyri.

THIS PIPELINE
    threshold combined GM+WM probability  ->  marching cubes at full 1 mm
    -> keep the largest connected component
    -> QUADRIC DECIMATION to the vertex budget   (feature-preserving)
    -> at most a token smoothing pass, chosen by measurement, not by taste

Decimation rather than smoothing is the whole point: quadric error metrics collapse
flat regions first and defend creases, which is the opposite of what a low-pass
filter does.

BUDGET: the BRN2 wire format uses Uint16 indices, so the hard ceiling is 65,535
vertices. The old mesh had 39,828 with a 1.77 mm median edge - already fine enough
to carry gyri. Resolution was never the problem; smoothing was.

Source: mni_icbm152_nlin_sym_09c, Copyright (C) 1993-2004 Louis Collins, McConnell
Brain Imaging Centre, MNI, McGill. Permissive - "permission to use, copy, modify and
distribute ... without fee ... provided that the above copyright notice appear in all
copies." That notice is in the page footer and vendor/mesh/README-LICENSE.md.

Usage:  python scratchpad/build_mesh.py <dir-with-the-nii-files> [--verts 62000]
"""
import argparse, pathlib, sys
import numpy as np

TARGET_VERTS = 62000          # under the 65,535 Uint16 ceiling, with headroom
ISO = 0.5                     # GM+WM probability isosurface


def stats(v, f, label):
    """Fold-retention metrics. These are the numbers that decide the pipeline."""
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    L = np.linalg.norm(v[e[:, 0]] - v[e[:, 1]], axis=1)
    fn = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
    area = 0.5 * np.linalg.norm(fn, axis=1).sum() / 100.0        # mm^2 -> cm^2
    fn /= (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    acc = np.zeros((len(v), 3)); cnt = np.zeros(len(v))
    for k in range(3):
        np.add.at(acc, f[:, k], fn); np.add.at(cnt, f[:, k], 1)
    acc /= (cnt[:, None] + 1e-9)
    rough = 1.0 - np.linalg.norm(acc, axis=1)
    flat = (rough < 0.01).mean()
    print(f"  {label:<26} V={len(v):>7,} T={len(f):>7,} "
          f"edge={np.median(L):4.2f}mm area={area:6.0f}cm2 flat={100*flat:5.1f}% "
          f"rough={rough.mean():.4f}")
    return dict(area=area, flat=flat, rough=rough.mean(), edge=float(np.median(L)))


def largest_component(v, f):
    """Marching cubes on a probability map leaves specks. Keep only the brain."""
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    g = sp.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(v),) * 2)
    n, lab = connected_components(g, directed=False)
    if n == 1:
        return v, f
    keep = np.argmax(np.bincount(lab))
    vmask = lab == keep
    remap = -np.ones(len(v), np.int64); remap[vmask] = np.arange(vmask.sum())
    fmask = vmask[f].all(axis=1)
    print(f"  dropped {n-1} disconnected component(s)")
    return v[vmask], remap[f[fmask]]


def taubin(v, f, iters, lam=0.5, mu=-0.53):
    """Shrink-free smoothing. Used sparingly here, and only if it measurably helps."""
    if iters == 0:
        return v
    import scipy.sparse as sp
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    e = np.concatenate([e, e[:, ::-1]])
    n = len(v)
    A = sp.coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(n, n)).tocsr()
    A.data[:] = 1.0
    deg = np.asarray(A.sum(1)).ravel(); deg[deg == 0] = 1
    v = v.copy()
    for _ in range(iters):
        for w in (lam, mu):
            v += w * ((A @ v) / deg[:, None] - v)
    return v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src", help="directory containing mni_icbm152_*_tal_nlin_sym_09c.nii")
    ap.add_argument("--verts", type=int, default=TARGET_VERTS)
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parents[1]
                                        / "vendor" / "mesh" / "brain-icbm152-v3.bin"))
    a = ap.parse_args()

    import nibabel as nib
    from skimage import measure

    src = pathlib.Path(a.src)
    gm = next(src.rglob("*_gm_tal_nlin_sym_09c.nii"))
    wm = next(src.rglob("*_wm_tal_nlin_sym_09c.nii"))
    print(f"GM {gm.name}\nWM {wm.name}")
    g, w = nib.load(str(gm)), nib.load(str(wm))
    vol = np.asarray(g.dataobj, dtype=np.float32) + np.asarray(w.dataobj, dtype=np.float32)
    zoom = np.abs(np.diag(g.affine))[:3]
    print(f"volume {vol.shape}  voxel {np.round(zoom,2)} mm  range {vol.min():.2f}..{vol.max():.2f}")

    # NO pre-blur. A gaussian here is the same mistake as smoothing afterwards:
    # it rounds off the sulcal walls before they are ever meshed.
    v, f, _, _ = measure.marching_cubes(vol, level=ISO, spacing=tuple(zoom))
    print("\nfold-retention metrics at each stage:")
    stats(v, f, "raw marching cubes")

    v, f = largest_component(v, f)
    st_raw = stats(v, f, "largest component")

    import fast_simplification as fsimp
    ratio = max(0.0, 1.0 - a.verts / len(v))
    v2, f2 = fsimp.simplify(v.astype(np.float32), f.astype(np.int32), ratio)
    v2 = v2.astype(np.float64); f2 = f2.astype(np.int64)
    st_dec = stats(v2, f2, f"quadric-decimated")

    # Pick the smoothing level that RETAINS THE MOST FOLD, by measurement.
    # Selecting on "area did not drop much" was the bug that let 5 passes win on the
    # first run: every level passed that test, so the loop just kept the last one.
    # The objective is explicit now - minimise the flat fraction.
    trials = []
    for it in (0, 1, 2, 5):
        vs = taubin(v2, f2, it)
        s = stats(vs, f2, f"  + taubin x{it}")
        trials.append((s["flat"], -s["area"], it, vs))
    trials.sort(key=lambda t: (t[0], t[1]))
    best_flat, _, best, best_v = trials[0]
    print(f"\nchosen smoothing: {best} taubin pass(es)  "
          f"(lowest flat fraction, {100*best_flat:.1f}%)")
    if best == 0:
        print("  i.e. none. Taubin is a low-pass filter and the gyri ARE the high"
              " frequencies -\n  every pass measurably flattened the surface.")
    v2 = best_v

    if len(v2) > 65535:
        sys.exit(f"REFUSING: {len(v2):,} vertices exceeds the Uint16 ceiling of 65,535")

    # ---- orientation + scale, matched to the mesh already on the page ----
    # The loader divides by 32767 and the camera is tuned to that framing, so the new
    # mesh must land in the same box. Axes remapped (x, z, -y) as the old one was.
    P = np.stack([v2[:, 0], v2[:, 2], -v2[:, 1]], axis=1)
    P -= (P.min(0) + P.max(0)) / 2
    P /= np.abs(P).max()
    fn = np.cross(P[f2[:, 1]] - P[f2[:, 0]], P[f2[:, 2]] - P[f2[:, 0]])
    fn /= (np.linalg.norm(fn, axis=1, keepdims=True) + 1e-12)
    N = np.zeros_like(P)
    for k in range(3):
        np.add.at(N, f2[:, k], fn)
    N /= (np.linalg.norm(N, axis=1, keepdims=True) + 1e-12)
    # outward-facing check: on a closed blob the normal should point away from centre
    if np.mean(np.sum(N * P, axis=1)) < 0:
        N = -N
        f2 = f2[:, ::-1]
        print("  flipped winding so normals point outward")

    # Report on the mm-scale mesh, not on the normalised one. (Multiplying the
    # unit-normalised positions by max(|v2|) was wrong and inflated area ~5x.)
    st_fin = stats(v2, f2, "final (true mm scale)")
    print(f"\nvs THE MESH THAT SHIPPED:  flat 71.4% -> {100*st_fin['flat']:.1f}%   "
          f"area 940 -> {st_fin['area']:.0f} cm2   "
          f"({st_fin['area']/940:.2f}x the fold surface)")

    out = pathlib.Path(a.out)
    np.save(out.with_suffix(".pos.npy"), P)
    np.save(out.with_suffix(".nrm.npy"), N)
    np.save(out.with_suffix(".idx.npy"), f2)
    print(f"\nwrote intermediate arrays next to {out.name}; pack with pack_mesh_v2.py")


if __name__ == "__main__":
    main()
