# Hero rebuild — particle brain. Live brief.

**Status: IN PROGRESS, started 2026-07-31.** Update this file as work lands.

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
- [ ] Brian reviews at `http://localhost:8899/design-candidates/hero-particles.html`
- [ ] Iterate on his notes — **new file per major change**, don't layer
- [ ] Once approved: self-host three.js, integrate into `index.html`, deploy

Preview server: `cd C:\Brian\02_Projects\portfolio && python -m http.server 8899`
