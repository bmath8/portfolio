# Hero rebuild — particle brain. Live brief.

> # ⛔ SUPERSEDED 2026-08-11 — see `SCENE-BRIEF.md`
>
> **This file is kept as a record. Do not build from it.** It said "IN PROGRESS" for eleven
> days after the approach it describes had been abandoned, which is exactly how layers
> accumulate: nothing is ever marked finished, so every session inherits all of them.
>
> What is wrong with it now:
> - It describes a **~14,000-point particle brain**. We ship a real **39,828-vertex cortical
>   mesh**. The particle approach was abandoned.
> - It says **25 named nodes**. There are **26** agents.
> - Its rule *"suggest the form, don't model it — if it needs to be anatomically correct, it's
>   wrong"* was **disproved** by `lab/03-real-mesh-opaque.html`, which showed the real
>   anatomical mesh reads correctly when rendered opaque. The material was the problem, not
>   the accuracy. That finding is what unlocked the current hero.
> - Its rule *"NEVER edit an existing candidate, new file every time"* produced 26 dead
>   candidates and is not how the current work proceeds.
>
> Still true and worth keeping: **one node per real scheduled agent, pulsing on its real
> schedule, hoverable to name it.** That idea survived everything and is what the hero is.

## Why the previous 26 candidates failed

Every attempt (J-brain, L5/L10/L11-mind, P-brain, C-contour) tried to render an
**anatomically correct cortex**. A real cortex is visually noisy — gyri and sulci fold
over each other constantly, so at hero scale it reads as mush. The last commit said it
outright: *"the technique fights the subject."* That was true of every technique tried,
because the subject was wrong, not the shader.

Second failure mode: **each pass was edited on top of the previous geometry** instead of
restarting. Twenty-six layers of accretion, unrecognizable result.

## The two rules

1. **NEVER edit an existing candidate.** New file every time.
2. **Suggest the form, don't model it.** If it needs to be anatomically correct, it's
   wrong. It must read as a brain from 3 metres away and as a particle field up close.

## The concept — why this one is Brian's and not a generic WebGL demo

**Each particle is one of the 25 agents on his real crontab.**

- ~14,000 ambient particles form the brain silhouette.
- **25 named nodes** sit inside it, larger and brighter — one per scheduled agent.
- Nodes pulse on their real schedule. Hovering names the agent.
- The hero stops being decoration and becomes the claim the resume makes: a live system
  he built and operates. No other candidate's portfolio can show that.

## Technique (researched 2026-07-31)

- **Implicit surface sampling, not a mesh.** Two hemisphere ellipsoids + cerebellum bulge
  + stem, with low-frequency noise displacement to *imply* folding. Rejection-sample
  points onto that surface → target positions.
- **CPU-side position lerp on a BufferGeometry**, ~14k points. Deliberately NOT GPGPU
  ping-pong FBO — that was over-engineering that contributed to the previous mess. 14k
  points updates comfortably at 60fps and is far easier to reason about.
- **Curl-ish noise drift** so the cloud breathes instead of sitting static.
- **Scatter → converge** on load; scroll drives a slow rotation.
- Additive blending, single hue + one accent (operational green, matching the site).

## Constraints (non-negotiable — these killed earlier versions)

- Renders **something** with JS disabled or WebGL unavailable (static fallback, never blank)
- `prefers-reduced-motion` → converged, still, no animation loop
- No horizontal overflow at 360px
- Particle count scales down on mobile / low DPR
- Pauses the RAF loop when the tab is hidden
- three.js currently from CDN for candidate speed — **self-host before shipping**, the
  live site is deliberately zero-third-party-request

## Files

| File | State |
|---|---|
| `design-candidates/hero-particles.html` | the rebuild — standalone, self-contained |
| `index.html` | live site, text version, currently deployed |

## Where to pick up

- [x] Research technique, diagnose why the old ones failed
- [x] Build `hero-particles.html` — particle brain, 25 agent nodes
- [x] **Geometry verified numerically** via `_verify_shell.py` (commit `8785f07`).
      14,000/14,000 points at 4.42% accept rate. Hemisphere skew **2.6%**, midline
      fissure **0.53%**, bbox x±5.0 y[-4.9,+3.1] z±3.7. ASCII front/side projections
      show two lobes, a clean fissure, and the cerebellum/stem — a readable silhouette
      *before* any shading. Re-run this after ANY change to `field()`.
- [ ] **← YOU ARE HERE.** Brian reviews at
      `http://localhost:8899/design-candidates/hero-particles.html`
- [ ] Iterate on his notes — **new file per major change** (`hero-particles-2.html`…),
      never edit in place. That is what produced the 26-candidate mess.
- [ ] Once approved: self-host three.js (drop the CDN importmap), fold into `index.html`,
      keep the `.vercelignore` exclusion on `design-candidates/`, deploy.

## Candidate 2 — `hero-gpgpu.html` (commit `a8c9326`) ← THE AMBITIOUS ONE

**65,536 particles, simulated entirely on the GPU, morphing between three forms.**

Research that drove it (2026-07-31):
- Awwwards Q1 2026: **29 of 47** Site-of-the-Day winners used Three.js. The stated pattern
  in the winners is *"pick one hard idea and execute it cleanly rather than stacking
  effects"* — a drivable physics world, audio-reactive fluid, one object with real weight.
- The wow technique in current showcases is **GPGPU ping-pong FBO simulation + curl noise
  + bloom that peaks mid-transition** (three.js forum "Particles Transition Bloom";
  Codrops "Crafting a Dreamy Particle Effect with Three.js and GPGPU"; Three.js Journey
  Lesson 41 flow-field particles). One reference runs 1,048,576 particles on a 1024² FBO.

**The one hard idea here:** the particles morph **cortex → network → the real crontab**.
The final form is 25 rings, one per actual scheduled agent. The effects have a job —
turbulence and bloom spike at the *moment of change*, marking the transition rather than
decorating it. Nothing is on screen that isn't carrying meaning.

Architecture: 256² RGBA32F ping-pong render targets · curl-noise velocity in the sim
shader · three DataTexture target forms · additive points with depth fog ·
UnrealBloomPass whose strength tracks `burst = sin(segment·π)` · scroll drives morph 0→2 ·
`prefers-reduced-motion` pins to form 0, static · SVG fallback if WebGL is unavailable ·
mobile drops to 128² (16k particles) and DPR caps at 1.75.

### The honest tension (Brian should decide with this in mind)
Research on the *hiring* side says the opposite of the Awwwards side: recruiters report
heavy animation reading as **gimmicky**, mobile experience mattering enormously, and case
studies out-performing effects. Brian is applying to **IT support roles at $50–60k** — a
ProCat hiring manager is not an Awwwards juror.

Counter-argument, and why this was still built: the final morph target is his *real
system*. That makes it evidence, not decoration — and it is the single most direct
demonstration of "I can build things" available to someone with no degree and no
professional dev history. Risk is real; so is the upside.

**Mitigation if he ships it:** keep the text hero readable with JS off, keep the mobile
particle count low, and make sure the case studies are one scroll away.

## Candidate 3 — `hero-gpgpu-2.html` (commit `e689836`) ← CURRENT BEST

Built from Brian's review of v1. His verdict, verbatim: *"the animations as you scroll get
worse and just are animations for the sake of… transitioned into neon lights that's not
readable and too bright and basically shows off nothing. The cortex is fine. The rest of
the page the designs from before was better."*

**What changed and why**

| v1 problem | v2 fix |
|---|---|
| 3-form morph was motion without meaning | **Morph deleted.** One form: the cortex. |
| Network/crontab forms read as unreadable neon | **Those forms are gone entirely.** |
| Too bright / blown out | **Bloom pass removed.** Additive blending + UnrealBloom is what clipped highlights to white. Peak particle alpha now **0.30** — additive stacking means anything higher clips where particles overlap. |
| Scroll hijacked into a performance | Scroll does nothing to the 3D. Slow constant drift + gentle mouse parallax only. |
| Agent dots competed with the headline | 25 agents now render as a **readable labelled bar** at the base of the hero. Hover names each one. Data, not glow. |
| Page below the fold was weaker than the old design | **Rebuilt on the previous structure** — 01 Selected Work (3 cases with verification blocks + real links), 02 Capabilities, 03 Experience, 04 Contact. Flat, high-contrast, zero 3D below the fold. |

Design principle now enforced: **the 3D lives only in the hero.** Everything below it is a
document. That is the split the earlier design got right and v1 abandoned.

### Still open on v2
- Brian says the cortex itself "can be significantly improved" — next iteration should
  work on the *silhouette and density*, not add effects. Ideas not yet tried: rim-lit
  edge density so the outline reads harder, a subtle two-tone hemisphere split, slower
  and larger-scale drift so it feels like breathing rather than shimmer.
- three.js still on CDN — self-host before shipping.

## Candidate 4 — `hero-v3.html` (commit `bf28d35`) ← CURRENT BEST

Brian's v2 review: *"no 3D animations showing our skills off… not sure having the brain in
the background is the best design… want my initials and all contact info top right, easy
clickable buttons… needs contrast, everything is just blue and dark, lighten it up… want
live demos along with my projects so employers can visualize it not just words."*

| Note | What v3 does |
|---|---|
| Brain as background is wrong | **Contained in a square dark panel** beside the headline. It's an exhibit, not wallpaper. Mouse parallax works inside the panel only. |
| No contrast, all blue/dark | **Light paper theme** (`#f4f2ee`) as the base, with the hero panel and the Capabilities/Experience band as **dark inserts**. Light → dark → light rhythm. |
| Contact info | **Sticky header**: `BM` monogram + name top-left, five icon buttons top-right (Email, Phone, GitHub, LinkedIn, Resume). Inline SVG icons, no icon font. Labels collapse to icons under 860px. Contact block repeats at the bottom. |
| Words, not visuals | **Three real demos** — see below. |

### The demos (this is the point of v3)
1. **Squares — a real `<iframe>` of the live app.** Employers interact with the actual
   thing that ran on game day, without leaving the page. This is the strongest asset on
   the site and it was previously just a link.
2. **Brian OS — interactive 24-hour schedule canvas.** All 25 agents plotted at their real
   cron times; hover a bar and it names the agent and time. Real data, not a picture.
3. **BoomBox — animated architecture diagram.** Packets flow along the edges, showing the
   durable-Postgres / transient-WebSocket split the case study describes. It's a prototype
   with nothing deployable, so the diagram *is* the demo.

### Cortex improvements in v3
Per Brian's "the cortex can be significantly improved" — worked on silhouette, not effects:
- **Rim-density shading.** New `aEdge` attribute = distance from the surface shell.
  Particles near the rim are larger and shift from body-blue to green, so the outline
  reads hard instead of dissolving.
- Slower drift (0.26 vs 0.33) and larger scale — breathing, not shimmer.
- Alpha stays capped (0.20 + edge 0.22) so nothing clips.
- `IntersectionObserver` pauses the loop when the panel is off-screen.

### Still open
- three.js on CDN — self-host before shipping.
- The Squares iframe adds a third-party request; acceptable for a candidate, needs a
  decision before ship (a click-to-load poster frame would preserve the zero-request goal).
- Schedule canvas is hard-coded from `hermes cron list`; could read a generated JSON.

## Known open items on candidate 1
- three.js loads from **cdnjs** — must be self-hosted before shipping (live site is
  deliberately zero-third-party-request).
- Agent pulse is currently a **decorative sine per node**, not the real crontab schedule.
  Wiring it to actual next-run times is a follow-up; the 25 names in `AGENTS[]` are real
  and come from `hermes cron list`.
- Raycast hover threshold (0.22) may need tuning on mobile.

Preview server: `cd C:\Brian\02_Projects\portfolio && python -m http.server 8899`
