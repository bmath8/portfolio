# Technique — what to actually build, from primary sources

Read 2026-08-04 from the tutorials themselves, not summaries. This is the file that
should have existed before candidate #1.

---

## THE CORE REALISATION

**Everything I built for Brian was a shell of points.** Particles sampled onto a surface.
A shell can only ever look like a shell — that is why the cortex "can be significantly
improved" and why no amount of colour or font work fixed it.

The technique that actually produces depth is **volumetric raymarching**, and the
distinction is one sentence, from Maxime Heckel:

> *"Instead of stopping the raymarched loop once the ray hits a surface, **we push through
> and continue the process to sample the inside of an object**."*

That is the difference between a point cloud and a thing with *interior*. Clouds, smoke,
and — for our purposes — a brain with real density, light scattering through it, and
depth that reads at any zoom.

---

## 1. Raymarching + SDFs (the form)

Source: Codrops, *"How to Create a Liquid Raymarching Scene Using Three.js Shading
Language"* (Ben McCormick, Jul 2024).

- Raymarching renders complex 2D/3D scenes **in a single fragment shader** — no models,
  no materials, no geometry. The whole form is math.
- Built on **Signed Distance Fields**: a function returning the distance from any point in
  space to the surface of an object. Combine SDFs with smooth-min and you get **metaballs**
  — "gloopy, liquid shapes that absorb into each other."
- Lineage worth reading in order:
  1. Kishimisu — *An Introduction to Raymarching*
  2. Inigo Quilez — *3D SDF Resources* (the canonical function library) and *Painting a
     Character with Maths*
  3. Maxime Heckel — *Painting with Math: A Gentle Study of Raymarching*
- **TSL** (Three.js Shading Language) compiles to WGSL on WebGPU and falls back to GLSL.
  Lower barrier than raw GLSL. Requires `WebGPURenderer`. Current as of three r168.

**Why this matters for the brain:** an SDF brain is *defined*, not *sampled*. Two lobe
ellipsoids + cerebellum + stem combined with `smin()` gives an organic fused form with no
seams — and it can deform, breathe, and split without regenerating geometry.

## 2. Volumetric rendering (the depth)

Source: Maxime Heckel, *"Real-time dreamy Cloudscapes with Volumetric Raymarching."*

- March through the object, accumulating density instead of stopping at the surface.
- Lineage: Shadertoy scenes — Inigo Quilez *"Clouds"*, al-ro *"Starry Night"*, Suyoku
  *"Volumetric Raymarching sample."*
- Serious references cited: EA Frostbite physically-based sky/cloud rendering (Sébastien
  Hillaire), *Horizon Zero Dawn*'s volumetric cloudscapes (Andrew Schneider), SimonDev's
  *How Big Budget AAA Games Render Clouds*, blue-noise masks for sampling.
- Blue noise is the standard fix for banding artefacts in volumetric sampling.

**Why this matters:** this is how the brain gets soft interior glow and scattering rather
than 14,000 hard dots. It is also inherently *not* neon — density accumulates smoothly
instead of additive-blending to white.

## 3. Dithering (the texture — and the fix for "too bright")

Source: Codrops, *"Efecto: Building Real-Time ASCII and Dithering Effects with WebGL
Shaders"* (Pablo Stanley, Jan 2026).

- Dithering creates the illusion of more colours than you have by arranging pixels in a
  pattern the eye blends. Descends from 1869 newspaper halftones → MacPaint → modern
  algorithms.
- **Floyd–Steinberg (1976):** when you round a pixel to the nearest available colour you
  get an error; **spread that error to neighbouring pixels** instead of discarding it.
  Produces organic patterns rather than harsh bands.
- Algorithm family to try: Floyd–Steinberg, Atkinson, Jarvis-Judice-Ninke, Stucki, Burkes,
  Sierra. Each has a distinct grain.
- The author is a **designer who didn't write shaders** and learned from Shadertoy +
  *The Book of Shaders* (Patricio Gonzalez Vivo) + the `postprocessing` library.

**Why this matters:** Brian rejected v1 as "neon lights, not readable, too bright." Bloom
on additive particles clips to white. **Dithering does the opposite** — it quantises to a
limited palette, so highlights *can't* blow out, and it produces "that crunchy texture
that feels both old and new." It gives the render a material identity instead of a glow.

## 4. Motion (the transitions Brian called weak)

Source: Codrops, *"How to Animate WebGL Shaders with GSAP"* (Andrea Biason / Adoratorio
Studio, Oct 2025).

- The professional pattern is **GSAP timelines driving shader uniforms** — not ad-hoc
  `lerp` calls in the RAF loop, which is what all four of my candidates did.
- A `Stage` class owns renderer/scene/camera; HTML and canvas are kept in sync; GSAP
  `ScrollTrigger` and `Draggable` drive interaction.
- Effects covered: ripples on click, mask reveals, scroll/drag-reactive blur.

**Why this matters:** proper easing and orchestration live in the timeline. That is the
missing craft layer in every version so far — my motion was linear damping, which always
reads as "floaty" rather than designed.

---

## THE SYNTHESIS — what v5 should be

**A volumetric raymarched brain, rendered through a dither pass, driven by GSAP.**

| Layer | Technique | Fixes |
|---|---|---|
| Form | SDF (ellipsoid lobes + cerebellum + stem, fused with `smin`) | "the cortex can be significantly improved" — a defined form, not a sampled shell |
| Depth | volumetric raymarch, accumulate density, blue-noise sampling | flatness; gives real interior and scattering |
| Surface | Floyd–Steinberg / Atkinson dither post-pass | "too bright / neon / not readable" — quantised, cannot blow out, and gives a real material identity |
| Motion | GSAP timelines → shader uniforms | "animations for the sake of" — orchestrated easing instead of linear damping |

This is **not another restyle.** It replaces the renderer, the form definition, the
lighting model and the motion system. It is the first genuinely different approach in the
whole sequence.

### Build order (experiments first, per the Lusion Labs model)
1. `lab/01-sdf-brain.html` — SDF form only, flat shading, no volume. Just get the
   silhouette right in a fragment shader.
2. `lab/02-volumetric.html` — add the density march + scattering.
3. `lab/03-dither.html` — add the dither post-pass, tune the algorithm and palette.
4. `lab/04-motion.html` — GSAP timeline on the uniforms.
5. Only then assemble the page.

Each is standalone, ~80–150 lines, one variable at a time.

### Known risks
- Raymarching is **fragment-shader bound** — cost scales with screen pixels and step
  count. On a 4070 SUPER at 12GB this is fine, but must be capped on mobile (fewer steps,
  lower internal resolution, then upscale).
- TSL needs `WebGPURenderer`; GLSL fallback is fine and more portable. **Start in GLSL.**
- Dither at low resolution then upscale, or the pattern is invisible.

## Sources
- [Codrops — Liquid Raymarching with TSL](https://tympanus.net/codrops/2024/07/15/how-to-create-a-liquid-raymarching-scene-using-three-js-shading-language/)
- [Maxime Heckel — Volumetric Raymarching Cloudscapes](https://blog.maximeheckel.com/posts/real-time-cloudscapes-with-volumetric-raymarching/)
- [Codrops — Efecto: ASCII & Dithering shaders](https://tympanus.net/codrops/2026/01/04/efecto-building-real-time-ascii-and-dithering-effects-with-webgl-shaders/)
- [Codrops — Animating WebGL Shaders with GSAP](https://tympanus.net/codrops/2025/10/08/how-to-animate-webgl-shaders-with-gsap-ripples-reveals-and-dynamic-blur-effects/)
- Inigo Quilez — 3D SDF resources · Kishimisu — Intro to Raymarching · The Book of Shaders
