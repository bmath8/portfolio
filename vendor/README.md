# vendor/ — what is here, and why

**Every file in this folder is either fetched by the live page or load-bearing at build time.
There is no third category.** Keep it that way: this folder had accumulated 2.3 MB of libraries
from abandoned approaches, and the cost was not bytes — nothing here ships — but that every
session opening it reasonably concluded the project used a bloom pipeline and HDR lighting.

Verified 2026-08-11 by loading the page and recording every request it makes.

## Fetched at runtime — 1.4 MB

| File | Size | Why |
|---|---|---|
| `three.core.min.js` + `three.module.min.js` | 740 KB | The renderer. ~r168–r175 (contains WebGPU + TSL, lacks `ClippingGroup`). |
| `lines/LineSegments2.js`, `lines/LineSegmentsGeometry.js`, `lines/LineMaterial.js` | 36 KB | The tract bundle — one instanced draw call regardless of segment count. |
| `mesh/brain-icbm152-v2.bin` | 648 KB | The cortical mesh, `BRN2` format, 39,828 verts. |
| `fonts/*.woff2` (6 faces) + `fonts.css` | 336 KB | Self-hosted — the zero-third-party-request rule depends on this. |

## ⛔ NOT fetched, and MUST NOT BE DELETED

**`mesh/brain-icbm152.bin` (820 KB).** Nothing requests it, so every dead-code sweep flags it.
It is the **only surviving source** for building `brain-icbm152-v2.bin`: the `build_mesh.py` that
generated it **has never existed in git history** (`git log --all --diff-filter=A` returns
nothing). `scratchpad/pack_mesh_v2.py` reads this file to produce the v2 mesh. Delete it and the
mesh becomes unregenerable — it would mean rewriting the pipeline from scratch (threshold
combined GM+WM probability maps of MNI ICBM152 2009c, marching cubes, Taubin smoothing).

Licence notice for both meshes: `mesh/README-LICENSE.md`. The notice must travel with the asset —
that is the licence condition, and it is why the footer carries it.

## Kept deliberately, not yet wired

| File | Size | Why kept |
|---|---|---|
| `gsap.min.js` + `ScrollTrigger.min.js` | 116 KB | GSAP became **100% free including every plugin** at v3.13 under Webflow's sponsorship. `RESEARCH-2026-08-11.md` recommends it for the DOM choreography (word-by-word heading reveals) that is still hand-rolled. Use it or remove it — do not let it sit here for another six months. |

## Removed 2026-08-11, and why — do not re-add without a reason

| Removed | Size | Why it was dead |
|---|---|---|
| `postprocessing.module.js`, `postprocessing/`, `shaders/` | 720 KB | A bloom/bokeh pipeline. **"no bloom" is a documented rejection** in `V6-PLAN` and the page's own DELIBERATELY ABSENT list. |
| `hdr/`, `loaders/RGBELoader.js`, `loaders/HDRLoader.js`, `RoomEnvironment.js` | 1.6 MB | Image-based lighting, abandoned when the matcap approach was adopted. |
| `objects/MarchingCubes.js` | 40 KB | The particle-brain era. Dead since `lab/03` proved the real mesh reads. |
| `lines/Line2.js`, `lines/LineGeometry.js` | 8 KB | Superseded by the `LineSegments2` pair above. |
| `lenis.min.js` | 16 KB | Smooth-scroll hijacking. Specced in Phase 4, never wired, and recommended against — it carries an accessibility cost that sits badly beside a `prefers-reduced-motion` fix. |

All recoverable from git history if a decision changes.


## 2026-08-12 — the mesh and the line library are gone

`vendor/mesh/` (brain-icbm152.bin, brain-icbm152-v2.bin, README-LICENSE.md) and
`vendor/lines/` (LineSegments2, LineSegmentsGeometry, LineMaterial) were deleted.

The page no longer downloads or ships a 3-D model at all. The hero object is
generated at run time from the cron lines in `agents.json`: time of day across
X, one agent lane per Z, a mark standing up wherever that agent fires. There is
no geometry to vendor because the data is the geometry.

That deletes a whole class of problem these files created:

* an AGPL-derived asset (`brain-mni.bin`) that had already been served publicly
  once, at HTTP 200 and 2,703,404 bytes, on 2026-08-05;
* a v1/v2 pair that had to be kept straight by name in `.vercelignore` forever,
  because v1 was the only surviving source for v2 and could not be deleted;
* 1.5 MB on disk and 469 KB on the wire, for a decoration.

`vendor/lines/` went with the instanced tract bundle it drew. Nothing imports it.

## Added: number-flow.min.js

`number-flow` 0.6.2 from npm (MIT, Maxwell Barvian), bundled to a single ESM
file with esbuild — the published `lite.mjs` has bare specifiers (`esm-env`,
its own `ssr` chunk) that a no-build page cannot resolve. 16 KB.

It animates the four hero figures. It is applied progressively: the number is
real text in the HTML and is only upgraded once the custom element is defined,
so a failed module load costs the animation and nothing else.
