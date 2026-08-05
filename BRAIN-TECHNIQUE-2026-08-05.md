# Brain hero — technique and licensing, verified 2026-08-05

Supersedes the plan in `TECHNIQUE.md` where they conflict. Everything marked ✅ was executed
or fetched this session, not recalled.

---

## 🚩 THE URGENT ONE — the shipped mesh is AGPL and was publicly served

`vendor/mesh/brain-mni.bin` is derived from `aces/brainbrowser`, which is **AGPL-3.0**
(verified live via the GitHub API). `vendor/mesh/README-LICENSE.md` already said
DO-NOT-DEPLOY. It was deploying anyway.

✅ Verified 2026-08-05: `https://bmath8.vercel.app/vendor/mesh/brain-mni.bin` returned
**HTTP 200, 2,703,404 bytes** — a public distribution of an AGPL asset, on the site printed
on all four resumes. `index.html` never referenced it; it shipped because `.vercelignore`
excluded only three specific vendor JS files.

**Fixed locally, not yet deployed.** `.vercelignore` now denies `vendor/*` and re-allows only
`vendor/fonts.css` and `vendor/fonts/` — the only two things `index.html` actually loads.
Pattern semantics were verified through git's matcher: fonts ship, mesh and the whole 3D
stack do not. **This needs a deploy to take effect.**

Bonus: that also stops several MB of unused three.js / postprocessing / HDR from being
served by a site whose entire argument is that it loads fast.

---

## ✅ Environment — all executed, not assumed

**Blender 5.2.0 LTS works headless.** Exact invocation:

```bash
"C:/Brian/tools/blender-5.2.0-windows-x64/blender.exe" --background --factory-startup \
  --python "C:/Brian/tools/blender_smoketest.py"
```

Real output this session: geometry OK (642 verts) → **voxel remesh** OK (642 → 2,936) →
named part + material OK → **Draco .glb export** OK, 54,116 bytes, **5.98× compression**.
Both the **Draco and MeshOptimizer bridge DLLs ship in this portable build** — no extra
install. Keep `--factory-startup` for reproducibility.

Voxel remesh matters specifically: it is the operation that kills sulcal noise while keeping
the silhouette — the exact failure mode behind "reads as mush at hero scale."

**three.js vendored is r185.** `nibabel`, `dipy`, `nilearn`, `trimesh`, `scikit-image` are
**all missing** — `pip install` needed before any neuroimaging conversion.

---

## ❗ The experiment everyone thinks failed was never actually run

| Lab file | Loads the real 81,924-vertex mesh? | What it really does |
|---|---|---|
| `lab/01-sdf-brain.html` | **NO** | Pure fragment-shader SDF **volumetric raymarch**. Zero geometry. This is the one rejected as fog. |
| `lab/02-mesh-parcellated.html` | **NO** | Procedurally displaced `SphereGeometry` blobs — 8 ellipsoids + a capsule + a torus. Its own comment claims it tests "does an opaque, flat-parcellated, depth-tested mesh read as anatomy." **It never tested that**, because it used blobs, not the real cortical surface sitting in `vendor/`. |
| `P-brain.html`, `C-contour.html`, `S-frame.html`, `T-day.html` | **YES** | These decode `brain-mni.bin` correctly. |

**So the rejection of lab 02 is not evidence that a real opaque anatomical mesh fails.**

### ✅ RUN IT — and the answer is YES

`lab/03-real-mesh-opaque.html`, built and screenshotted 2026-08-05.

**The real opaque mesh reads unmistakably as a brain.** Gyri and sulci legible, hard
silhouette, sculptural. It is nobody's idea of a cloud. Mesh decode 17–23ms, per-vertex
curvature 85ms — both trivial.

**The premise behind 26 point-cloud candidates and the volumetric raymarch was wrong.**
`HERO-BRIEF.md` concluded *"the technique fights the subject"* and `TECHNIQUE.md` concluded
*"everything I built was a shell of points."* Both then changed the *subject* — suggest the
form, don't model it; fake the gyri with fbm. **The subject was fine. It was the material.**
Opaque + depth-tested + curvature-shaded is the whole fix. Anatomical accuracy was never the
problem; transparency, additive blending and sampling were.

Three findings from the run, all visible in the screenshots:

1. **The inverted-hull outline at 0.018 is too thick** — it bleeds dark halos into every
   sulcus and pokes black spikes through the surface, because the hull offset exceeds the
   width of the folds. Anatomy this convoluted does not want an inverted hull. Drop to
   ~0.004 or use a depth/normal discontinuity pass. **Outline OFF is the best read.**
2. **A clip plane without a stencil cap makes it look broken, not sectioned** — you see
   through into a hollow shell with jagged edges. This *confirms* the cap face is the entire
   device; a bare clipping plane is worse than none. Build the stencil group before showing
   a cutaway to anyone.
3. `RoomEnvironment.js` imports the bare specifier `three`, so an **import map is required**
   even with everything self-hosted. Also: rAF throttles to ~1fps in a background tab — the
   fps readout is meaningless unless focused.

---

## Licensing — the table that decides what can ship

| Asset | License | Ship it? |
|---|---|---|
| **MNI ICBM152 2009c** | MIT-like: *"permission to use, copy, modify, and distribute… for any purpose and without fee"* | ✅ **BEST.** Needs a copyright notice + Fonov citation. Ships as a NIfTI volume, so needs marching-cubes → surface. |
| **NIH 3D `3DPX-021161`** ("Detailed Human Brain") | **CC-BY 4.0** | ✅ **FAST PATH.** Already a mesh — no conversion. Inspect topology before committing. |
| **Z-Anatomy** | CC BY-SA 4.0 | ✅ with attribution + ShareAlike on the derivative. 5,000+ labelled structures, native `.blend`. Best if you want *named parts*. |
| **BodyParts3D** | CC BY-SA 2.1 JP | ✅ with the required credit line. |
| **FreeSurfer / fsaverage / Desikan-Killiany / Destrieux** | *"non-commercial, non-clinical, academic research purposes only"*; *"for-profit organizations explicitly prohibited"* | 🚩 **BLOCKED.** |
| **HCP via BALSA** (incl. Glasser HCP-MMP1) | *"re-distribution… outside of your institution is NOT PERMITTED"* | 🚩 **BLOCKED** — a public site is redistribution. |
| **IIT Human Brain Atlas** | non-commercial educational/research only | 🚩 **BLOCKED.** |
| **NIH 3D `3DPX-000320`** | CC-BY-**NC**-SA | 🚩 **BLOCKED** — proof that NIH 3D licenses are *per model*. Never assume government = public domain. |
| **DSI-Studio HCP-1065 tracts** | conflicting statements (CC BY-SA 4.0 vs WU-Minn HCP terms) | ⚠️ **UNRESOLVED** — do not ship until settled. |
| **brainbrowser** (current asset) | AGPL-3.0 | 🚩 **REPLACE.** |

---

## 🔑 The key technical finding — signals along tracts, one draw call

`LineSegmentsGeometry extends InstancedBufferGeometry`. **N tract segments = ONE instanced
draw call regardless of N.** The forum complaints about `LineSegments2` past ~1,000 are people
creating 1,000 *separate objects*; put every tract into one geometry and it goes away.

The vendored `LineMaterial.js` already has the animation machinery — `dashOffset`, `dashScale`,
`dashSize`, `gapSize` uniforms, the `USE_DASH` define, and `computeLineDistances()` on
`LineSegments2.js:283`. **Nothing new needs vendoring.**

Discrete travelling pulse (not a repeating dash) — patch the discard with a Gaussian:

```js
mat.onBeforeCompile = (s) => {
  s.uniforms.uHead = { value: 0 };
  s.fragmentShader = s.fragmentShader
    .replace('uniform float dashOffset;', 'uniform float dashOffset;\nuniform float uHead;')
    .replace(
      'if ( mod( vLineDistance + dashOffset, dashSize + gapSize ) > dashSize ) discard;',
      `float d = abs(fract(vLineDistance * 0.25 - uHead) - 0.5);
       float pulse = exp(-d * d * 90.0);
       diffuseColor.rgb += pulse * 2.2;
       diffuseColor.a = 0.14 + pulse * 0.86;`
    );
  mat.userData.shader = s;
};
```

The resting tract stays dim and still describes the anatomy; the pulse is the activity.
Requires `mat.resolution.set(w, h)` and `computeLineDistances()` or lines vanish silently.

Prior art: `vasturiano/three-globe` (MIT, 1.6k★, maintained) — its arc layer is the canonical
version of this. Steal its `% 1e9` float-precision guard for long-running animations.

## The anti-cloud device: stencil cutaway

Real code verified from three.js `dev` (`examples/webgl_clipping_stencil.html`). Back faces
increment the stencil, front faces decrement, and a cap plane fills where the count is
non-zero. Needs `renderer = new WebGLRenderer({ stencil: true })` and
`renderer.localClippingEnabled = true`.

**This is the highest-leverage move available: a clean filled cut face is something no fog,
glow, blob or point cloud can ever produce.** It is proof of solidity, not a style.

Supporting devices: **matcap** (zero lights, one texture fetch, unmistakably solid);
**per-vertex curvature** computed in Blender and exported as a custom attribute — makes sulci
read as *grooves* rather than noise, and skips UVs, baking and a texture download entirely;
**inverted-hull outline** for a hard silhouette at one extra draw call.

**Ship without UnrealBloom.** It is 5+ passes and it is the direct cause of the glow/cloud
read rejected twice.

## Plunder target: NiiVue

`niivue/niivue` — **BSD-2-Clause**, maintained (pushed 2026-07-08). Its
`packages/niivue/src/nvmesh-loaders.ts` implements `readTRK()`, `readTCK()`, `readTRX()`,
`readTT()`. **Don't embed NiiVue** — it has its own renderer and a medical-tool aesthetic.
**Lift the streamline parsers under BSD-2 attribution**, then render with `LineSegments2`.
Neuroglancer (Apache-2.0) is architecturally too far away to be worth porting.

---

## Blender → web: the five settings that silently break things

`bpy.ops.export_scene.gltf()` defaults, introspected from the installed 5.2 binary:

- **`export_apply=False`** — Geometry Nodes output is a *modifier evaluation*. Without
  `True` you export the base mesh and lose everything the node tree made. The #1 silent
  failure in this pipeline.
- **`export_attributes=False`** — set `True` to carry per-vertex parcellation ID or curvature
  into Three.js as a named attribute.
- **`export_vertex_color='MATERIAL'`** — colours only come through if a material references
  them. Use `'ACTIVE'` for raw colour attributes.
- **KTX2/Basis is not offered** (AUTO/JPEG/WEBP only) — must be done post-export.
- **Draco and meshopt are effectively exclusive.** For an LCP-bound hero, **meshopt wins** —
  it decodes near-instantly where Draco compresses harder but decodes slower.

⚠️ **`gltf-transform optimize` defaults `--simplify true`.** On an 81k-vertex cortical
surface it will quietly eat the sulci — which is exactly the "reads as a blob" failure
already rejected twice. Always `--simplify false` on the first pass and compare visually.

glTF has **no curve primitive**. Don't export tracts as geometry: export the polylines as a
raw `Float32Array` `.bin` (the same pattern `brain-mni.bin` already uses) and build one
`LineSegmentsGeometry` at runtime. 2,000 tubed tracts would be ~2.3M triangles — far over budget.

---

## Performance budget

| Item | Budget |
|---|---|
| Total 3D payload | **≤ 700 KB** transferred |
| Cortical mesh | 40–70k triangles (down from 163,840) |
| Tract segments | 40–80k, **quantised to int16** and dequantised on load |
| Draw calls | **≤ 25** (this architecture needs ~6) |
| DPR | `Math.min(devicePixelRatio, 1.5)` — lab 02 uses 2, which is ~1.8× the fill rate for no visible gain |
| Post-processing | **≤ 1 full-screen pass**, and not bloom |

**Load order doubles as the explanation:** poster image first so LCP fires on it → mesh
(structure) → tracts (pathways) → signals (activity).

Degradation: no WebGL2 → static poster; `prefers-reduced-motion` → one frame, no RAF;
`document.hidden` → stop the loop (lab 02 does this, **lab 01 does not** — fix before shipping).

---

## Ranked approaches

**🥇 Opaque anatomical mesh + stencil cutaway + instanced tracts with travelling pulses.**
Attacks the failure mode structurally rather than cosmetically: a cloud has no cut face, a fog
has no silhouette, a point cloud has no occlusion — and occlusion is the strongest cue that
something is a solid object. 3–5 days, **risk LOW-MEDIUM** (every piece verified working; the
real risk is art direction — a sectioned brain can read clinical). Blocked on replacing the
AGPL asset.

**🥈 Parcellated hard-surface mesh + surface node graph, no cutaway.** What lab 02 claimed to
test but didn't. Simpler, no stencil, unambiguously reads as "a system that works" — but the
mechanism is only on the outside. 2–3 days, **risk LOW**.

**🥉 Full Blender-baked hero with pre-authored fibre geometry.** Highest visual ceiling,
lowest runtime cost, but it fights the brief: baked tubes make travelling pulses much harder,
the triangle count explodes, and every visual tweak is a Blender round-trip — the wrong
property for a design that has already been rejected 34 times. 5–8 days, **risk MEDIUM-HIGH**.

---

## Next actions, in order

1. **Deploy the `.vercelignore` fix** — the AGPL asset is public until then.
2. **Run the never-run experiment** — real `brain-mni.bin` + opaque matcap, 30 minutes. Locally
   only; do not deploy that asset.
3. **Replace the asset** — `pip install nibabel scikit-image scipy` and build from ICBM152, or
   download NIH 3D `3DPX-021161` (CC-BY 4.0) and skip the volume→surface step.
4. **Prototype the pulse shader** on synthetic tracts — it runs today, no real tract data needed.
5. `npm i -g @gltf-transform/cli` (v4.4.2, needs Node ≥20 — you have 24.11) and grab the
   `gltfpack` v1.2 Windows binary.

## Unverified — stated as such
- Blender 5.2-vs-4.x glTF exporter delta (blender.org and docs.blender.org both refuse
  fetching). The *current* API surface is verified by direct introspection.
- Compressed size for the 81k mesh under meshopt (~500–800 KB) is an estimate. The 5.98×
  Draco ratio is measured, on a much smaller test object.
- Topology and anatomical fidelity of NIH 3D `3DPX-021161` — download and inspect.
