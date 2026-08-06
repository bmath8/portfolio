# Current Session

_Updated 2026-08-06 (second entry: the load-time work)._

---

# ✅ DEPLOYED 2026-08-06 (second deploy) — BRN2 mesh, live and independently verified

**Live commit: `fd3797c` on `main` → https://bmath8.vercel.app**
**Rollback target: `f0fc046`** (the v1-mesh build, itself verified live earlier today).

## ⚠️ THE 2.86 s LOAD FIGURE WAS WRONG — corrected here

The previous entry recorded *"cold load is 2.86 s on the live URL, against a stated 2 s budget"*
and treated it as the one open performance problem. **That measurement was taken seconds after a
deploy, so it hit a COLD CDN EDGE.** It is the first-visitor-after-a-deploy number, not what any
real visitor experiences.

Re-measured on the warm edge, three consecutive runs, **fresh browser context each time so the
browser cache is empty**:

| run | load | FCP | wire |
|---|---|---|---|
| 1 | 137 ms | 132 ms | 877 KB |
| 2 | 159 ms | 124 ms | 877 KB |
| 3 | 169 ms | 132 ms | 877 KB |

**FCP ~130 ms, load ~155 ms.** Isolation runs confirm the page is not JS- or GPU-bound:
TTFB 49–55 ms, HTML complete 56–111 ms, FCP 120 ms with JavaScript disabled entirely.

**The 2 s budget is met with room to spare.** The lesson is procedural: *never benchmark
immediately after a deploy* — you measure the CDN's cold start, not the page. Report both numbers
or neither, and say which is which.

Independently verified before pushing, by decoding BRN2 **from the format spec in a separate
implementation** rather than by re-running the packer:
positions bit-identical · normals bit-identical · same triangle set, same count ·
**winding preserved on all 79,644 triangles** · byte stream consumed exactly (662,624 of 662,624).

Measured live with `curl` and an explicit `Accept-Encoding`: mesh **469,245 B** on the wire
(`content-encoding: br`) against the 469,248 predicted — a 3-byte miss. Whole page **877 KB**.
`three.core` 104 KB and `three.module` 90 KB over the wire, not the 742 KB their on-disk size
suggested. Zero third-party requests, zero console errors, zero HTTP ≥400.
`/vendor/mesh/brain-icbm152.bin`, `/vendor/mesh/brain-mni.bin` (AGPL), `/design-candidates/*` and
`/scratchpad/*` all 404.

## The finding that drove everything: the CDN compresses at brotli **q3**

The old note said delta-encoding indices "helps only if the host actually gzips
`application/octet-stream` — unverified". It does — but weakly, and the exact setting matters:

| brotli quality, run locally on the current file | bytes |
|---|---|
| q3 | **748,625** ← byte-for-byte the measured live wire size |
| q5 | 663,419 |
| q11 | 559,003 |

So Vercel is leaving ~190 KB on the table versus q11, and **no amount of choosing a cleverer
compressor helps, because we do not control the compressor.** The only lever that works is
handing q3 bytes that are already low-entropy. `Invoke-WebRequest` cannot see this — it
transparently decodes and strips `Content-Encoding`. Measure with `curl` and an explicit
`Accept-Encoding` header, or you will measure nothing.

## What shipped into the format

`vendor/mesh/brain-icbm152-v2.bin`, magic `BRN2`. Built by **`scratchpad/pack_mesh_v2.py`**,
which refuses to write the file unless 11 round-trip checks pass.

| | before | after |
|---|---|---|
| mesh on disk | 836,324 | **662,624** (−20.8%) |
| mesh on the wire (q3) | 748,625 | **469,248** (−37.3%, −279,377 B) |
| **whole page over the wire** | **1,220 KB** | **948 KB** (−22.4%) |
| JS decode cost | 0 ms | **1.9 ms** median |

- **positions** → plane-split, zigzag delta, LEB128 varint. They were *100.0% incompressible*
  as stored (brotli returned them 5 bytes larger); delta makes them 194 KB at q3.
- **indices** → each triangle cyclically rotated so its smallest index leads (winding
  preserved), triangles sorted, then three delta streams. 477,864 → 313,516 raw.
- **normals** → deliberately left alone. Delta-encoding them cost 22 KB on disk to save 4 KB
  on the wire. Not worth a second decode path.

1.9 ms of decode to save 279 KB breaks even at ~1.2 Gbps, so it is a win on every real connection.

## Vertex order is deliberately NOT optimised — this is the trap in this file

The textbook move is a vertex-cache optimiser, which permutes vertices. **Do not.** The page
seats its 26 agent nodes by farthest-point sampling over a *strided walk of the vertex array*
(`for i in 0..nV step floor(nV/1400)`). Permuting vertices silently moves every node on the
cortex — a visual regression with no error message. It was measured anyway (scheme "A": 672,316
on disk) and it compressed **worse** than the scheme that leaves vertex order alone.

## Verified, by running it

Round-trip, in the packer and again in Node against the decoder pasted out of `index.html`:
positions **bit-identical**, normals **bit-identical**, triangle set identical under a
rotation-invariant order-insensitive comparison, all indices in range, whole buffer consumed.
Both suites include a **negative control** — a deliberate 1-index corruption that the check is
confirmed to catch — because a check that cannot fail proves nothing.

Triangle order *does* change, and curvature is a float accumulation over triangles, so shading
is the one thing not bit-identical. Quantified rather than hand-waved: max Δ **1.8e-7**,
**0 of 39,828 vertices differ at 8-bit output precision.** Invisible, provably.

In a real browser (localhost, Chrome, not headless): mesh fetched and decoded, canvas
2545×860, WebGL fallback hidden, **zero console messages**, zero failed requests, zero
third-party requests. At 360 px: no horizontal overflow, `#stage` still `position:relative`
at 336 px — the contained exhibit, not wallpaper. A/B screenshot against the live v1 site:
indistinguishable (node and tract differences are sway phase and pulse position).

## Two defects found on the way, both fixed

1. **`scratchpad/` was not in `.vercelignore`** — the new packer would have deployed publicly.
   Added. (`build_mesh.py` was already absent, so nothing had leaked yet.)
2. **`const tmp` collided** with the `THREE.Vector3` named `tmp` at line 753. The whole module
   died with `SyntaxError`, and — exactly the documented 2026-07-29 failure mode — the page
   still *looked* fine, because the JS-off fallback renders. Caught only by asserting the mesh
   was actually requested. **Never judge this page from a screenshot alone.**

## 🚩 `build_mesh.py` DOES NOT EXIST — provenance gap, unresolved

The previous entry and the old loader comment both said to regenerate the mesh with
`scratchpad/build_mesh.py`. That file is **not on disk and has never been in git history**
(`git log --all --diff-filter=A` returns nothing). `brain-icbm152.bin` is therefore the *only*
surviving source for this geometry — which is why `.vercelignore` keeps it on disk while
excluding it from the deploy. **Do not delete it.** Regenerating would mean rewriting the
script from scratch (threshold combined GM+WM probability maps of MNI ICBM152 2009c, marching
cubes, Taubin smoothing). The false pointer is now corrected in `index.html`.

## 🔴 THE AGPL FIX WAS INCOMPLETE — GitHub was still serving it

Earlier entries recorded this as handled: excluded from `.vercelignore`, 404 on the live site.
**That only ever covered Vercel.** `github.com/bmath8/portfolio` is a **public** repo, it was
still tracking `vendor/mesh/brain-mni.bin` at `HEAD`, and the file was downloadable at
**HTTP 200, 2,703,404 bytes** from `raw.githubusercontent.com/.../main/...` — verified, not
assumed. The repo carries **no LICENSE file**. This is the same shape as the
`git-history-secret-lesson`: fixing the *serving* path says nothing about the *repo*.

Done now:
- `git rm vendor/mesh/brain-mni.bin` — gone from the tree, so it leaves `main` on the next push.
- **11 archived drafts repointed** to `brain-icbm152.bin` so nothing breaks. They needed the
  index type changed too (81,924 verts/Uint32 → 39,828 verts/Uint16). Two bugs surfaced while
  doing it: `v11-icbm.html` was already broken — still reading `Uint32Array` from a file that
  became Uint16 on 2026-08-06 — and `C/S/T` used an inlined `nT*12` stride. Repo-wide there is
  now **no `Uint32Array` and no fetch of the AGPL mesh** anywhere.
- The `.vercelignore` deny line stays as defence in depth.
- The comment in `index.html` claiming *"The old AGPL brain-mni.bin is gone"* is finally true.

**⚠️ STILL EXPOSED, AND IT NEEDS BRIAN: the blob remains in git history** (`cd2746e`,
`24e1549`) and is fetchable by commit SHA from the public repo right now. `git rm` does not
touch history. Removing it for real means `git filter-repo` (or BFG) + a **force-push that
rewrites public history**, and GitHub keeps unreachable blobs until it garbage-collects, so
Support may need to be asked to run GC. That is destructive and outward-facing — **not
something to do without an explicit yes.** The cheaper alternative is making the repo private.

## Still open

- **Not deployed.** Committed to `main` locally and deliberately **not pushed** — pushing to
  `main` is what triggers the Vercel deploy, and deploy is Brian's call. Rollback target
  remains `f0fc046`.
- ~~Cold load should be re-measured after deploy.~~ **DONE.** Measured on the warm edge with an
  empty browser cache, three runs: **load 137/159/169 ms, FCP 132/124/132 ms, 877 KB wire.**
  The old 2.86 s reading was a cold-CDN-edge artefact of benchmarking seconds after a deploy.
- **AGPL asset: removed from the tree, still in git history.** See the section above - purging
  it needs a history rewrite + force-push to a public repo, which is Brian's call.
  Deleting it outright remains the better fix and is still pending Brian's call.
- Remaining lever if ever needed: serving a pre-brotli-q11 `.br` file with an explicit
  `Content-Encoding` header would reach **404,898 B** (another 64 KB). Not done, because it
  breaks any client that does not send `Accept-Encoding: br` and that is a real robustness
  trade on a public job-hunt site. Brian's call, not mine.

---

# ✅ DEPLOYED 2026-08-06 — live and verified by observation

**Live commit: `f0fc046` on `main` → https://bmath8.vercel.app**
**Rollback target: `ba5166f`** (the previously-live commit). `git revert f0fc046` or reset+push.

Verified **against the deployed URL**, not against git — the 2026-08-05 font incident proved an
ignore pattern that git accepts says nothing about how the host treats it:

| Must be 200 | Result |
|---|---|
| `/` | 200 · 58,370 B |
| `/vendor/mesh/brain-icbm152.bin` | 200 · **836,324 B** |
| `/vendor/three.module.min.js` + `/vendor/three.core.min.js` | 200 · 365,552 B / 385,386 B |
| `/vendor/lines/{LineSegments2,LineSegmentsGeometry,LineMaterial}.js` | 200 (all three) |
| all 6 self-hosted fonts | 200 (all six) |
| `/agents.json` · `/resume.pdf` · `/og.png` · `/favicon.svg` | 200 |

| Must be 404 | Result |
|---|---|
| `/vendor/mesh/brain-mni.bin` (**AGPL**) | **404** |
| `/design-candidates/v11-icbm.html`, `/design-candidates/v12-ship.html` | 404 |
| `/vendor/postprocessing.module.js`, `/vendor/gsap.min.js` | 404 |
| `/CURRENT_SESSION.md` | 404 |

**Live browser smoke test:** load **2,859 ms** cold · canvas 1440×828 · WebGL fallback hidden ·
badge computing the real next run from real cron lines · 26 agents · body height 4021 px ·
**zero third-party requests** (measured via `performance.getEntriesByType('resource')`, not
assumed) · **zero console errors, zero page errors, zero HTTP ≥400.**

---

# ▶ 2026-08-06 — what shipped in `f0fc046`

`design-candidates/v12-ship.html` → copied to `index.html` with the production meta block
(canonical, OG/Twitter, favicon, `theme-color` corrected to `#08090b` — it still said the old
paper `#eef1f0`). **Everything below is verified by running it, not by reading a status file.**

## Five real defects found by screenshotting v11, all fixed in v12

1. **CSS specificity bug — every `<section class="wrap">` and the footer had ZERO vertical
   padding.** `.wrap{padding:0 32px}` is a class selector and outranked the `section{padding:88px 0}`
   and `footer{padding:80px 0 96px}` element rules. That is why Experience butted straight into
   the closing CTA. Restated as `section.wrap` / `footer.wrap`. Page height 3505 → 4021px; the
   vertical rhythm the design was drawn with had never actually rendered.
2. **The tuned orientation was being thrown away two seconds after load.** `pivot.rotation.set(-0.10,-1.75,0.06)`
   set the left-lateral three-quarter that `lab/03` proved reads as anatomy — then the animation
   loop initialised `rotY=0` and eased `rotation.y` from −1.75 toward 0, a ~100° swing, and kept
   spinning from there. **The good view existed only on the first frame.** Now `BASE_YAW=-1.75`,
   `BASE_PITCH=-0.10` (the loop had also been using the *z-roll* value 0.06 as pitch), and the
   drift is a **±9° sway over ~57s instead of an unbounded spin** — "a box with an animation that
   spins" is a documented rejection.
3. **Mobile turned the brain back into wallpaper.** At ≤940px `.hero-right` was hidden but
   `#stage` stayed `inset:0` behind the copy, so the cortex became a washed-out background under
   the headline — the exact thing rejected once before. It is now a **contained exhibit above the
   copy** (`position:relative`, 42vh), and the mobile camera keeps the lateral character instead
   of sitting dead-on at x=0 showing a frontal view. Contact bar stacks below 620px.
4. **"3 public repos" was false** — there are 8 public repos on the account. Replaced with
   **"3 systems shipped"**, which is what the three case studies below it actually argue, matches
   the OG alt text, and cannot rot when a repo is published or made private.
5. **JS-off badge said "next run loading…" forever.** Now reads "26 agents scheduled on real
   cron lines" and JS upgrades it to the real next run.

## Verified, by running it

| Check | Result |
|---|---|
| Console errors | **0** (the earlier one was a `favicon.ico` 404 in the candidate file only) |
| Local load | 30–240 ms |
| JS disabled | full page renders — **3,868 chars** of visible text, not a blank page |
| 360px | `scrollWidth` 360, **no horizontal overflow** |
| Referenced assets | **14/14 exist on disk and all ship** — simulated against `.vercelignore` |
| AGPL `brain-mni.bin` | excluded by name; appears in `index.html` only inside a comment |

## ⚠️ `.vercelignore` REWRITTEN — this was a shipping blocker

The old file excluded `vendor/three*`, `vendor/lines/` and `vendor/mesh/` outright, because the
old `index.html` loaded only `fonts.css`. **The new page needs all of them.** Deploying v12 under
the old manifest would have produced a page with no brain and a hard module error. Now every
exclusion is explicit (no negation — Vercel does not honour directory re-includes, learned
2026-08-05), and `vendor/mesh/brain-mni.bin` is excluded **by name** while its directory ships.

Note `three.module.min.js` internally imports `./three.core.min.js`; both must ship. Shipping
only the first is a silent hard failure.

## ✅ Mesh optimised — 1,314,188 → 836,324 bytes, 36.4% off, provably lossless

**The indices were `Uint32` for a mesh with 39,828 vertices.** Every index fit in 16 bits with
25,000 to spare, so the top two bytes of all 238,932 indices were always zero. They were
**72.7% of the entire file**.

Rebuilt as `Uint16`. Verified lossless *before* swapping the file: the round trip was checked
bit-identical on positions, normals **and** indices (`np.array_equal` on all three) — this is not
a quantization tradeoff, it is deleting bytes that carried no information. Loader now reads
`new Uint16Array(buf.slice(o, o+nT*3*2))`. Re-rendered and compared: **visually identical, zero
page errors.**

⚠️ **If the mesh is ever regenerated above 65,535 vertices this must revert to `Uint32Array`.**
`scratchpad/build_mesh.py`'s `STEP` controls the vertex count. The loader comment says so.

Notably this beat the researched option. `meshoptimizer`/`gltfpack -cc` was the top
recommendation, but it would have meant converting to glTF, adding `GLTFLoader` (~100 KB) and a
WASM decoder (~25 KB) — to compress data whose single biggest redundancy was removable with a
one-line type change and no new dependency. **Check the format before reaching for a compressor.**

Page weight now **1.68 MB on disk** (was 2.32 MB), of which 223 KB is `resume.pdf` — a download,
not part of page load. Over the wire it is roughly 836 KB mesh + ~190 KB gzipped JS + 268 KB
fonts. The headline still paints before any of it; the module graph is deferred.

Remaining, if more is ever needed: vertex-cache reorder + delta-encoded indices (helps only if
the host actually gzips `application/octet-stream` — unverified), or oct-encoded normals
(119 KB → 80 KB, small win, real precision risk). Neither is worth doing now. **Do not decimate
the mesh** — the gyre legibility is the entire point of the hero.

## Honest limitations, stated
- **`vendor/mesh/brain-mni.bin` (AGPL) is still on disk.** It is excluded from the deploy and
  404s on the live site, but deleting it outright is the better fix and is pending Brian's call.
- **Headless screenshots stall on this page** — `Page.screenshot: Timeout 30000ms` with
  `GPU stall due to ReadPixels`. It is a headless-Chromium capture issue, **not a page fault**:
  the page evaluates clean (canvas 1440×828, `glfail` hidden, live badge computing the real next
  run, zero page errors). Capture with `--use-gl=swiftshader --enable-unsafe-swiftshader` and a
  raised timeout. Do not "fix" the page in response to this.
- ~~Cold load is 2.86 s against a 2 s budget.~~ **RETRACTED — see the top of this file.**
  That was a cold-CDN-edge measurement taken right after a deploy. Real figure on a warm edge
  with an empty browser cache is **~155 ms load / ~130 ms FCP**.

---

# ✅ DEPLOYED 2026-08-05 — live state recorded

**Live commit: `ba5166f` on `main` → https://bmath8.vercel.app**
**Rollback target if ever needed: `c668400`** (`git revert` or reset + force push).

Four commits shipped, each verified against the deployed URL, not assumed:

1. `792de58` — **stopped serving the AGPL mesh.** `/vendor/mesh/brain-mni.bin` now 404s
   (was HTTP 200, 2,703,404 bytes). The whole unused three.js/postprocessing/HDR stack is
   also gone from the deploy.
2. `f50b67e` — **fixed fonts that commit 1 broke.** `vendor/*` + `!vendor/fonts/` is valid
   under git's matcher (I verified it there) but **Vercel did not honour the directory
   re-include** — `/vendor/fonts/IBMPlexSans-400.woff2` returned 404 and the live site
   silently dropped to system fonts. Post-deploy checks caught it. Now an explicit exclusion
   list with no negation. **Lesson: verifying an ignore pattern against git does not prove
   how the host treats it. Verify against the deployed URL.**
3. `058844f` — **corrected the site to 26 agents** and added the missing `career-scout`
   (`15 7 * * *`) to the `JOBS` array. The dial had been plotting a fleet that no longer
   matched the machine.
4. `ba5166f` — **two remaining bare `25`s**: the dial's own readout and the Brian OS agent
   row. The dial was plotting 26 while its label said 25. My first check missed these because
   the regex required 40 chars of context on both sides and `.` doesn't cross newlines.

**Verified live:** all 7 self-hosted fonts 200 · homepage 200 · resume.pdf 200 · og.png 200 ·
AGPL mesh 404 · three.js 404 · HDR 404 · `design-candidates/` 404 · 26 JOBS entries ·
zero stale `25`s outside rgba colour values.

---

# 🎨 PALETTE RETRACTED 2026-08-05 — read before touching colour

Brian **retracted his earlier "I like the color scheme"** later the same day. Verbatim:

> *"The blue background and color scheme need to be changed. I like the dark theme but
> everything is blue and blends into eachother. There is no contrast, flow, clear distinct
> areas and borders. It can have that dark theme but has to have contrasts with light,
> accents, differences to appreciate other parts, color scheme, shades."*

**What is retracted:** the near-monochrome blue ramp (`#050a12`/`#0a1420`/`#0e1c2b`/`#1b2f44`).
Every surface was the same hue at slightly different lightness, so nothing separated.

**What is NOT retracted — still endorsed:** the **dark theme itself**, the brain hero, the
contact header, the metric strip, real telemetry, verification blocks, the demos, the type
pairing. Do not rebuild the page. **This is a palette change, not a redesign.**

**The tension to resolve carefully:** he asked for *"each part to flow into each other"*
earlier and *"clear distinct areas and borders"* now. These are not contradictory — **flow is
not mush.** Major bands should still dissolve into each other via gradient seams (Phase 4),
while **cards and panels must become clearly distinct surfaces** with real value separation
and visible borders. Section transitions flow; content surfaces separate.

---

# ▶ START HERE — resuming 2026-08-05, 4:30pm

**Working file: `design-candidates/v11-icbm.html`. ALL FIVE PHASES DONE, AND THE MESH IS
NOW LEGALLY SHIPPABLE.** What remains is folding v11 into `index.html` and deploying.

### v11 — the mesh swap (2026-08-05) ✅ the last blocker is gone
`vendor/mesh/brain-icbm152.bin` — **39,828 verts / 79,644 tris / 1.31 MB**, less than half
the AGPL asset. Built from the **MNI ICBM152 2009c** template by thresholding combined
grey+white matter probability maps and running marching cubes, then Taubin-smoothed (shrink-
free, so the silhouette survives where plain Laplacian would deflate it).

**Licence: permissive.** *"Permission to use, copy, modify, and distribute … for any purpose
and without fee … provided that the above copyright notice appear in all copies."* The
notice is now in the page footer and in `vendor/mesh/README-LICENSE.md`. This closes option 1
of the three the old README listed.

**Why GM+WM and not the supplied brain mask:** the mask yields a smooth bean with no gyri.
The grey/white boundary is what carries the folds.

**Output matches the existing binary format exactly**, so the page loader needed no change —
only the fetch path. Regenerate with `scratchpad/build_mesh.py` (needs `nibabel`,
`scikit-image`, `scipy`, all now installed); raise `STEP` to cut triangle count.

**Two fixes the new mesh forced:**
- **Curvature normalisation moved from min/max to 3rd/97th percentile.** Min/max is hostage
  to a few outlier vertices; on this smoother surface it pushed most of the mesh into the
  bright band and the shading blew out to white. Ceiling also pulled 1.28 → 1.06.
- **Orientation** re-set to `(-0.10, -1.75, 0.06)` for a left-lateral three-quarter. The
  first attempt showed it from underneath.

The NIH 3D CC-BY model (`3DPX-021161`) was tried first and abandoned: its asset lives behind
a signed S3 URL that returns 403 to anything but the site's own session.

### v10 — Phase 3, the 3D upgrade (2026-08-05)
**Concept: the hero shows a day passing through the machine.**
- **Tracts.** Agents are sorted by the time they *actually* run, and a bezier tract connects
  each to the next — so the line network is literally the shape of his day. Built as one
  `LineSegments2`; `LineSegmentsGeometry extends InstancedBufferGeometry`, so the whole bundle
  is **one instanced draw call** regardless of segment count.
- **Travelling signal.** The dash discard is replaced with a Gaussian on `vLineDistance`, so a
  pulse *travels* while the resting tract stays dim and keeps describing the path. `uHead`
  sweeps 0→1 over ~14s = one simulated day. Nodes swell as the signal reaches their turn.
- **Hover interaction.** Raycast against the node `InstancedMesh`; the label names the real
  agent and prints its real cron line. The hero claim becomes checkable in the hero itself.
- **Cursor parallax with weight** — eases toward the pointer and carries momentum instead of
  snapping. Float-and-bob was the thing to avoid.
- **Scroll does NOT drive the 3D.** Rejected once already; the brain keeps its own clock.

**Tuning notes worth keeping:** the first pass used a lift proportional to node distance,
which sent long hops (consecutive agents on opposite sides of the brain) swinging out into
space where they read as stray lines. Clamped to `min(0.085, 0.055 * dist)` so tracts hug the
surface. Resting alpha also raised 0.085 → 0.20, or the network was invisible between pulses.

**Honest limitation:** in a still frame the tracts read subtly — the pulse is the point, and
it only makes sense in motion. Judge this one live, not from a screenshot.

**Not yet done in Phase 3:** GSAP is still not wired (the loop is hand-rolled rather than a
GSAP master timeline), and there is no staged intro lighting nodes in cron order. Both were
specced; neither is required for the piece to work.

### v9 — the palette rework (2026-08-05)
- **Base is neutral now, not blue.** `#08090b` / `#0d0f13` / `#15181d` / `#1d2128`. A faint
  cool cast, no dominant hue — which is what lets an accent read as an accent.
- **Real value steps** between surfaces, so a card is obviously a card on a page.
- **Borders you can actually see:** `--edge:#2d333d`. The old `#1b2f44` was barely
  distinguishable from the panel it was meant to bound.
- **A genuinely light band** (`--lift:#eef1f5`) under "What I actually do" — he asked for
  *"contrasts with light"*, and he endorsed a light/dark rhythm back in v3. One light surface
  mid-page does more for contrast than any amount of tuning within the darks.
- **Accents warmed and brightened:** `#2ee6c6` cyan, `#ffb340` amber, `#ff5c8a` magenta,
  `#9b8cff` violet — one cool, one warm, so the page isn't all one temperature.
- The brain keeps its blue-cyan shading, which now reads as a deliberate coloured object
  against a neutral base rather than one more blue on blue.
Serve it and look at it first:
```
cd C:\Brian\02_Projects\portfolio && python -m http.server 8899
# http://localhost:8899/design-candidates/v7-contrast.html
```

**Do this next, in this order:**

1. **Phase 3 — the 3D upgrade.** The only remaining design phase, and the highest-risk.
   Full spec in `V6-PLAN-2026-08-05.md`. Concept: *the hero shows a day passing through his
   machine* — `LineSegments2` tracts between related agents (one instanced draw call regardless
   of count), Gaussian travelling pulses on `vLineDistance`, fired on the real cron schedule so
   the **06:40–07:00 cluster becomes a visible storm**. Hover a node → agent, cron line, last
   run. GSAP master timeline. **Scroll must NOT drive the 3D** — already rejected once.
2. **Swap the AGPL mesh** — do it during Phase 3 at the latest. The shading is now tuned to
   this specific mesh, so a later swap means redoing Phase 1.
3. **Deploy** — the `.vercelignore` fix has been ready since the morning of 2026-08-05 and the
   AGPL asset stays public until it ships.

**Two small things left over from Phase 4:** the cyan `.thread` element is currently too
subtle to see (z-index 0, 0.22 alpha, sitting behind `.wrap` content) — either raise it or cut
it. And **Lenis is still not wired up** for scroll momentum; it is vendored and unused.

**Rules that are not negotiable here:** never edit `v6-instrument.html` (the approved base);
new file per change; one variable at a time; screenshot before showing Brian anything.

---

## 🏁 THE HEADLINE: after 34 rejections, there is an approved base

`design-candidates/v6-instrument.html` is the **first candidate Brian has ever approved.**
His words, verbatim:

> *"Yes, this is a good start and first time we can use and build and improve upon."*
> *"I like the color scheme."* · *"Now that we have a great brain design…"*

**⛔ Never start from a blank editor again.** Copy the latest approved file, change one named
thing, screenshot it. The documented failure mode is a *partial* criticism triggering a full
rebuild, which reverts to generic priors and loses approved ground.

**Approved and load-bearing — do not silently drop any of these:**
the Claude Design palette (`#050a12`/`#0a1420`/`#0e1c2b`/`#1b2f44` + cyan/magenta/amber/violet),
Bricolage Grotesque display + IBM Plex Sans body + Plex Mono **for real numbers only**,
the brain as hero centrepiece, the sticky contact header (monogram left, icon buttons right),
the live metric strip, real telemetry from `agents.json`, accent-bordered project cards,
and the verification blocks that state each claim's source inline.

## What unlocked it — the finding that overturned 26 candidates

`lab/03-real-mesh-opaque.html`, built and screenshotted this session, proved that **the real
81,924-vertex cortical mesh rendered opaque with per-vertex curvature reads unmistakably as a
brain.** Decode 17–23ms, curvature 85ms.

Two earlier docs concluded *"the technique fights the subject"* and *"everything I built was a
shell of points"*, then changed the **subject** — *suggest the form, don't model it*, fake the
gyri with noise. **That was the wrong lesson. Anatomical accuracy was never the problem; the
material was.** Transparency, additive blending, bloom and surface-sampling made it fog.

Neither lab 01 nor lab 02 had ever loaded the real mesh — 01 is a shader with zero geometry,
02 is displaced spheres. The experiment everyone believed had failed had never been run.

## Where the build is right now

| File | State |
|---|---|
| `v6-instrument.html` | **APPROVED BASE.** Do not edit in place. |
| `v7-contrast.html` | **Phases 1 + 2 complete, 2026-08-05.** Current working file. |
| `lab/03-real-mesh-opaque.html` | The proof. Keep — it settles the material question. |
| `V6-PLAN-2026-08-05.md` | The 5-phase plan of record. |

### Phase 1 — make it pop ✅
**Diagnosis:** the matcap spent most of its area in `#33566f`–`#12283c`, within ~10% luminance
of the `#050a12` page. The mesh was *the same value as its background*. A value problem, not a
colour problem — so the approved palette did not change, only its range.
- Matcap widened to a true `#ffffff` → `#04101d` ramp
- **Cyan fresnel rim** — the single most effective separation device; puts the accent *on the
  object* rather than only in the UI
- Cavity spread widened to `smoothstep(0.24, 0.76)`
- Camera to `x = -1.58, z = 3.18` — further right, ~12% larger

### Phase 2 — make the nodes read ✅
They were invisible: placed by *scaling the position vector*, which buries them in sulci, and
seated by name-hash, which clustered them.
- **Lift along the vertex normal** (0.030) — the actual fix
- **Farthest-point sampling** over a 1,400-vertex candidate set, so all 26 are separated
- Depth-tested, so back-facing nodes vanish — that occlusion is what proves the mesh is solid
- Coloured by real schedule class: cyan daily · violet hourly · amber weekly · magenta monthly

### ⚠️ One correction made mid-phase, worth remembering
The violet two-tone was first set to `vec3(0.70,0.63,1.18)` and **turned the whole brain
purple** — overcooked, and purple-dominant is close to the AI-gradient tell. Pulled back to
`vec3(0.90,0.88,1.05)`, where violet is a hint in the deepest folds only. **The two-tone must
stay subtle.**

## Next: Phases 3–5, in this order

**Phase 5 (demos) → Phase 4 (flow) → Phase 3 (the 3D upgrade, last and highest-risk).**

- **5 · Demos.** All three are thin canvas sketches. Squares is the big win: replace the fake
  coloured grid with a **click-to-load `<iframe>` of the live app** behind a poster frame — real
  interaction, still zero third-party requests until asked. Brian OS → interactive timeline
  with hover-to-name. BoomBox → a diagram that actually explains durable-vs-transient.
- **4 · Flow.** Brian: *"I want each part to flow into each other."* Kill the hard 1px section
  borders, replace with long gradient seams; let the hero's dark bleed into Selected Work; run
  a thin cyan thread down the page. Lenis is vendored and unused.
- **3 · The 3D upgrade.** *"Turn that into an amazing 3D animation and interaction."* Concept:
  **the hero shows a day passing through his machine.** `LineSegments2` tracts between related
  agents (one instanced draw call regardless of count), Gaussian travelling pulses on
  `vLineDistance`, fired on the real cron schedule so the **06:40–07:00 cluster becomes a
  visible storm because twelve agents genuinely wake in those twenty minutes**. Hover a node →
  agent name, cron line, last run. Cursor parallax with weight. GSAP master timeline (vendored,
  never used) instead of ad-hoc lerps.
  **Explicitly NOT doing: scroll will not drive the 3D.** Rejected once already.
  Budget: ≤700KB, ≤25 draw calls, DPR ≤1.5, no bloom, paused when hidden, static poster with
  JS off, reduced-motion honoured.

## 🚩 Blocking before anything ships

1. **The AGPL asset.** `vendor/mesh/brain-mni.bin` derives from `aces/brainbrowser` (AGPL-3.0)
   and **was being served publicly** — verified HTTP 200, 2,703,404 bytes, 2026-08-05, on the
   URL printed on all four resumes. `index.html` never referenced it; `.vercelignore` excluded
   only three vendor JS files.
   **Fixed locally** (deny `vendor/*`, re-allow `fonts.css` + `fonts/`; pattern verified
   through git's matcher). **Still public until a deploy happens.**
   Replace with **MNI ICBM152 2009c** (MIT-like) or **NIH 3D `3DPX-021161`** (CC-BY).
   FreeSurfer/fsaverage, HCP/BALSA and the IIT atlas are all licence-blocked — table in
   `BRAIN-TECHNIQUE-2026-08-05.md`.
2. **Deploy approval** — Brian's call.

## Reference docs written this session
- `REFERENCES-2026-08-05.md` — 40+ analysed sites, the 10-item shortlist, anti-references.
  Key finding: **2026 Developer Awards are going to interaction craft on readable pages, not
  polygon count** (five independent confirmations). The under-2s budget is not a compromise.
- `BRAIN-TECHNIQUE-2026-08-05.md` — licensing table, the `LineSegments2` pulse technique, the
  stencil-cutaway code, Blender 5.2 headless pipeline, performance budget.
- `V6-PLAN-2026-08-05.md` — the phase plan.
- `../../03_Career/docs/HIRING-RESEARCH-2026-08-05.md` — ATS reality, cover letters, NJ EO 327.

Preview: `cd C:\Brian\02_Projects\portfolio && python -m http.server 8899`

---

## Earlier — 2026-07-30 (still accurate where not superseded)

The re-skin of the real `index.html` was finished and committed; eleven candidates A–K were
abandoned. Palette moved off warm-cream/serif-italic/terracotta. Content paints instantly (the
old reveal-on-scroll started every section at `opacity:0`). AI Job Hunter is off the site by
Tom's decision. Case studies link to real public source. Hero dial reads from `hermes cron
list`. Zero third-party requests; fonts self-hosted. OG tags + `og.png` added.

**Superseded:** that entry said the Best Buy *"ranked first in the territory"* claim was still
live and awaiting deploy. **It is not live** — the deployed HTML was fetched and searched on
2026-08-05 for `territory`, `ranked`, `#1`, `top sales`: zero matches. That item is done.
Also stale: **8 public repos now, not 4.**
