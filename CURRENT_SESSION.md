# Current Session

_Updated 2026-08-05. Supersedes the 2026-07-30 entry (kept at the bottom)._

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
