# How the page is built

One static `index.html`, no build step, no framework, no runtime dependency on
anything the visitor has to trust. Everything below is checkable by opening the
file or the deployed URL.

Superseded and deleted 2026-08-12: `BRAIN-TECHNIQUE-2026-08-05.md`,
`HERO-BRIEF.md`, `SCENE-BRIEF.md`, `V6-PLAN-2026-08-05.md` and
`REFERENCES-2026-08-05.md`. All five described a cortical-mesh hero that no
longer exists in any form. Keeping documentation for a deleted object is how the
last seventeen versions ended up designing on top of each other.

## The hero object — the schedule field

There is no 3-D model. Nothing is downloaded, shipped, or authored in a modeller.
The geometry is generated at load from the 26 cron lines in `agents.json`:

| axis | meaning |
|---|---|
| X | time of day, 00:00 at the left edge through to 24:00 |
| Z | one lane per agent, 26 of them running back into the scene |
| Y | a mark stands up wherever that agent actually fires |

54 firings a day. The silhouette of the field is the shape of the day, and it is
dense at 06:40 because the crontab is dense at 06:40. Remove an agent from
`agents.json` and its lane disappears.

This replaced a downloaded MNI ICBM152 cortical surface that had been relit five
times across seventeen versions. The failure was structural, not a tuning
problem: a brain is a metaphor, so it gets judged as a picture of a brain. A
field generated from the data cannot be wrong about what it depicts.

Implementation notes that are easy to get wrong:

- **Distance falloff is `THREE.Fog`, not baked vertex alpha.** Baking it fixes
  the falloff at one camera position and then lies the moment the camera moves,
  and this camera moves through six shots.
- **Rail colours come from a `UI` map read once out of the CSS custom
  properties.** `new THREE.Color(undefined)` silently resolves to **white** —
  a missing key does not throw, it just draws every minor rail at full white and
  deletes the grid's hierarchy. That shipped once. If a rail looks wrong, check
  the key exists in `UI` before touching the colour.
- **Scroll conductor**: six authored shots keyed to `[data-cam]` elements,
  interpolated on native scroll with a smoothstep, damped frame-rate
  independently as `lerp(cur, to, 1 - exp(-dt/ease))`.
- **Drag composes with scroll.** User drag is stored as an *offset* from
  whatever the conductor is currently asking for, not as the value itself,
  or the two fight over one variable.
- **The clock line is real.** It sits at the current local time and moves.

## Colour

Derived in OKLCH, shipped as hex. See `DESIGN-REFERENCE.md`.

Hex is what ships because `THREE.Color`, canvas 2D and the contrast audit all
have to read these values and none of them parses `oklch()`. The OKLCH source
sits in a comment beside every token — re-derive the ramp rather than nudging
the hex, or it drifts back to being arbitrary.

## Vendored code

| file | why |
|---|---|
| `vendor/three.module.min.js` + `three.core.min.js` | the scene. The second is imported internally by the first; shipping only one is a hard module error. |
| `vendor/fonts/*.woff2` | six self-hosted faces, so there is no third-party request |
| `vendor/number-flow.min.js` | the four hero figures count up. npm, MIT, bundled to one ESM with esbuild because the published build has bare specifiers a no-build page cannot resolve. |

`vendor/mesh/` and `vendor/lines/` were deleted with the cortex.

## Non-negotiables, and how each is actually checked

Not asserted — measured, by rendering the page in Chromium.

| claim | how it is verified |
|---|---|
| every figure is checkable | counted from `agents.json` at run time where possible. The page claimed "twelve" agents fire between 06:40 and 07:00 for several versions; it is **ten**. Both the field annotation and the dial caption now count the window instead of asserting it, which is how that was caught. |
| WCAG AA contrast | computed styles read from the live DOM at four scroll positions, foreground against the first opaque ancestor background |
| reduced motion is honoured | two screenshots 2.6 s apart must be **byte-identical** under `prefers-reduced-motion: reduce`. A visual check passes things this catches. |
| renders without JavaScript | loaded with `java_script_enabled=False`; h1, headings and links must still be present |
| no third-party requests | every request logged on load and through a full scroll; the count must be 0 before the visitor clicks anything |

Scripts live in the session scratchpad, not in the repo — they are checks, not
shipped code. Re-run them against a **deployed** URL after any deploy: an ignore
pattern that git accepts proves nothing about how the host treats it.
