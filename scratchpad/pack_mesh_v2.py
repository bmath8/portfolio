"""Repack brain-icbm152.bin into the v2 wire format. Lossless - proven, not asserted.

WHY THIS EXISTS
---------------
The live CDN was measured compressing this asset with brotli **q3** (748,625 B on the wire for
an 836,324 B file - q3 reproduces that byte-for-byte locally). q3 is weak, so the only reliable
way to move the number is to hand it bytes that are *already* low-entropy. Two changes do that,
and neither touches geometry or vertex numbering:

  positions  i16 interleaved  ->  plane-split, zigzag delta, LEB128 varint
  indices    u16 triples      ->  each triangle cyclically rotated so its smallest index leads
                                  (winding preserved), triangles sorted, then three streams:
                                  delta(first), zigzag(second-first), zigzag(third-first)
  normals    i8               ->  UNCHANGED. Delta-encoding them cost 22 KB on disk to save
                                  4 KB on the wire at q3. Not worth a second decode path.

VERTEX ORDER IS DELIBERATELY UNTOUCHED. The page seats its 26 agent nodes by farthest-point
sampling over `for i in 0..nV step floor(nV/1400)`. Permuting vertices - which is what a normal
vertex-cache optimiser does, and what scheme "A" in the experiments did - silently moves every
node on the cortex. It compressed slightly *worse* than this anyway.

TRIANGLE order does change (they get sorted). That is safe for rendering and for the curvature
pass, which is an order-independent per-vertex accumulation - though float addition is not
associative, so curvature differs in the ~1e-7 range. Verified visually identical, not assumed.

Run:  python scratchpad/pack_mesh_v2.py
"""
import numpy as np, brotli, struct, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "vendor" / "mesh" / "brain-icbm152.bin"
DST = ROOT / "vendor" / "mesh" / "brain-icbm152-v2.bin"
MAGIC = b"BRN2"


def zig(a):
    a = np.asarray(a, np.int64)
    return (a << 1) ^ (a >> 63)


def unzig(z):
    z = np.asarray(z, np.int64)
    return (z >> 1) ^ -(z & 1)


def varint(a):
    a = np.asarray(a, np.int64)
    assert (a >= 0).all(), "varint takes non-negative only; zigzag first"
    out = bytearray()
    for v in a.tolist():
        while True:
            b = v & 0x7F
            v >>= 7
            if v:
                out.append(b | 0x80)
            else:
                out.append(b)
                break
    return bytes(out)


def unvarint(buf, n, start=0):
    out = np.empty(n, np.int64)
    v = 0
    s = 0
    k = 0
    i = start
    while k < n:
        byte = buf[i]
        i += 1
        v |= (byte & 0x7F) << s
        if byte & 0x80:
            s += 7
        else:
            out[k] = v
            k += 1
            v = 0
            s = 0
    return out, i


def br(b, q=3):
    return len(brotli.compress(bytes(b), quality=q))


raw = SRC.read_bytes()
nV, nT = struct.unpack_from("<II", raw, 0)
o = 8
qp = np.frombuffer(raw, "<i2", nV * 3, o).reshape(nV, 3).astype(np.int64); o += nV * 3 * 2
qn = np.frombuffer(raw, "i1", nV * 3, o).reshape(nV, 3); o += nV * 3
idx = np.frombuffer(raw, "<u2", nT * 3, o).reshape(nT, 3).astype(np.int64)
print(f"source {SRC.name}: nV={nV:,} nT={nT:,} bytes={len(raw):,}")

# ---- positions: plane-split zigzag delta ----
pos_stream = b"".join(varint(zig(np.diff(np.concatenate(([0], qp[:, k]))))) for k in range(3))

# ---- indices: rotate (winding-safe), sort, split into three delta streams ----
am = idx.argmin(axis=1)
rot = np.take_along_axis(idx, (am[:, None] + np.arange(3)[None, :]) % 3, axis=1)
tri = rot[np.lexsort((rot[:, 2], rot[:, 1], rot[:, 0]))]
idx_stream = (varint(np.diff(np.concatenate(([0], tri[:, 0]))))
              + varint(zig(tri[:, 1] - tri[:, 0]))
              + varint(zig(tri[:, 2] - tri[:, 0])))

nrm_bytes = qn.astype("i1").tobytes()
out = (MAGIC + struct.pack("<IIII", nV, nT, len(pos_stream), len(idx_stream))
       + pos_stream + nrm_bytes + idx_stream)

# ------------------------------------------------------------------ verification
fail = []


def check(label, ok):
    print(f"  {'PASS' if ok else 'FAIL'}  {label}")
    if not ok:
        fail.append(label)


print("\nverifying (decoding the produced bytes back, not the in-memory arrays):")
p = len(MAGIC) + 16
dnV, dnT, plen, ilen = struct.unpack_from("<IIII", out, len(MAGIC))
check("header round-trips", (dnV, dnT) == (nV, nT))

planes = []
cur = p
for _ in range(3):
    vals, cur = unvarint(out, nV, cur)
    planes.append(np.cumsum(unzig(vals)))
dqp = np.stack(planes, axis=1)
check("positions decode bit-identical", np.array_equal(dqp, qp))
check("positions fit int16", int(dqp.min()) >= -32768 and int(dqp.max()) <= 32767)

cur = p + plen
dqn = np.frombuffer(out, "i1", nV * 3, cur).reshape(nV, 3)
check("normals decode bit-identical", np.array_equal(dqn, qn))

cur = p + plen + nV * 3
f, cur = unvarint(out, nT, cur)
o1, cur = unvarint(out, nT, cur)
o2, cur = unvarint(out, nT, cur)
first = np.cumsum(f)
dtri = np.stack([first, first + unzig(o1), first + unzig(o2)], axis=1)
check("indices decode to the packed triangle array", np.array_equal(dtri, tri))
check("indices fit uint16", int(dtri.max()) <= 65535 and int(dtri.min()) >= 0)
check("stream consumed exactly", cur == len(out))

# geometry identity, insensitive to triangle order and to which corner leads
cyc = np.stack([np.roll(idx, -k, axis=1) for k in range(3)], axis=1)
check("every rotation is cyclic, so winding is preserved",
      bool((cyc == rot[:, None, :]).all(axis=2).any(axis=1).all()))


def geo(t):
    """Order-insensitive, rotation-invariant, winding-SENSITIVE canonical form.

    Each triangle becomes its three per-corner (position, normal) 6-vectors. Cyclic rotation
    must not register as a difference (it is the same triangle, same winding) but a reflection
    must, so we take the lexicographically smallest of the three CYCLIC layouts only - never
    the reversed ones. Then sort the triangles, so triangle order does not register either.
    """
    v = np.concatenate([qp[t.reshape(-1)], qn[t.reshape(-1)].astype(np.int64)],
                       axis=1).reshape(len(t), 3, 6)
    cyc = np.stack([np.roll(v, -k, axis=1).reshape(len(t), 18) for k in range(3)], axis=1)
    keys = np.lexsort(cyc.reshape(-1, 18).T[::-1]).argsort().reshape(len(t), 3)
    canon = cyc[np.arange(len(t)), keys.argmin(axis=1)]
    return canon[np.lexsort(canon.T[::-1])]


check("decoded triangle geometry == source geometry (positions AND normals)",
      np.array_equal(geo(dtri), geo(idx)))

# Negative control: a check that cannot fail proves nothing. Corrupt one corner of one
# triangle and confirm the comparison above actually notices.
_bad = dtri.copy()
_bad[7, 1] = (_bad[7, 1] + 1) % nV
check("^ that check is real (a 1-index corruption is detected)",
      not np.array_equal(geo(_bad), geo(idx)))
# ...and confirm a pure cyclic rotation is NOT flagged (or the check would be over-strict)
check("^ and is not over-strict (a cyclic rotation is accepted)",
      np.array_equal(geo(np.roll(dtri, 1, axis=1)), geo(idx)))

if fail:
    sys.exit(f"\nREFUSING TO WRITE - {len(fail)} check(s) failed: {fail}")

DST.write_bytes(out)
print(f"\nwrote {DST.name}")
print(f"  disk  {len(raw):>9,} -> {len(out):>9,}   ({100*(1-len(out)/len(raw)):.1f}% off)")
print(f"  br3   {br(raw):>9,} -> {br(out):>9,}   ({100*(1-br(out)/br(raw)):.1f}% off)  <- q3 = the measured CDN setting")
print(f"  br11  {br(raw,11):>9,} -> {br(out,11):>9,}")
