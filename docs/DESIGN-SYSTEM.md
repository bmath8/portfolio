# Design system — both editions

Reference for maintaining `index.html` (Mission Control) and `neural.html` (Neural).
Both are single-file pages. Accurate as of **v7.4, 2026-08-12**.

Each page carries **three `:root` blocks**, applied in order. This is deliberate — the
later blocks are layers added by later passes, and keeping them separate makes it obvious
which decision came from where:

1. **Base palette** — colours, families, easing curves.
2. **Accessibility override** — currently just `--faint`, raised from a failing contrast
   ratio. Never fold this back into the base block; it exists to be seen.
3. **Type scale and display face** — the `--t-*` ramp added in the v7.4 design pass.

---

## Mission Control — `index.html`

**Concept.** A panel on a machine that is running. The vocabulary is measurement rules,
registration marks and oversized tabular numerals — not rounded rectangles.

### Tokens

```css
/* 1. base */
--bg0:#04060a;  --bg1:#081019;  --bg2:#061410;  --bg3:#0b0a18;
--panel:#0c1520; --panel2:#122031; --line:#1d3042; --line2:#2c4a63;
--txt:#eaf3fb;  --dim:#93aabf;
--green:#4af0a0; --ice:#6fd3ff; --amber:#ffc44d; --red:#ff6161; --violet:#b39bff;
--mono:'IBM Plex Mono',monospace;  --sans:'Archivo',sans-serif;
--ease:cubic-bezier(.22,1,.36,1);  --spring:cubic-bezier(.34,1.56,.64,1);

/* 2. accessibility override */
--faint:#8199ad;        /* was #4c637a = 2.95:1 on panel, below AA. now 6.2:1 */

/* 3. type scale, 1.28 ratio */
--t-hero:clamp(2.8rem,5.9vw,4.8rem);
--t-mega:clamp(2.6rem,5vw,4.7rem);     /* metric numerals */
--t-sec:clamp(1.9rem,3.4vw,2.9rem);
--t-card:clamp(1.35rem,2vw,1.7rem);
--t-lead:clamp(1.02rem,1.25vw,1.16rem);
--t-body:.95rem; --t-meta:.78rem; --t-micro:.68rem;
--disp:'Bricolage','Archivo',sans-serif;
--rule:rgba(147,170,191,.16);
```

Sections alternate tonal bands (`--bg1` ice-tinted, `--bg2` green-tinted, `--bg3`
violet-tinted) so adjacent sections never blend. **Each accent owns a meaning and must not
be reused decoratively:** green = healthy/live, ice = information, amber = attention or
prototype, red = now/failure, violet = tertiary.

**Type.** Bricolage Grotesque (700/800) for display — engineered and slightly odd where
Archivo is neutral. Archivo (500–900) remains the UI sans. IBM Plex Mono for anything
representing machine output: labels, cron lines, logs, captions. All self-hosted from
`/vendor/fonts/`.

**Motion.** `--ease` for reveals, `--spring` for hover lifts. Staggered delays `.d1 .d2 .d3`
at 80ms steps. Section headings draw an underline on entry. Project cards arrive from
alternating directions rather than uniformly upward.

**Texture.** Fixed scanline overlay (`body::before`) plus an SVG `feTurbulence` grain and
vignette (`body::after`), all non-interactive.

### Components

- **Status bar** — sticky, blurred, live dot, section links, HIRE action. Below 560px the
  location text drops and the name stays.
- **Console card** — terminal chrome plus a live log prepending a line every 1.8s, capped
  at 4 rows, drawn from a 20-entry set with a random start. Tilted `-0.35deg`, straightens
  on hover.
- **Metric strip** — **full-bleed**, edge to edge, `width:100vw` with the container padded
  by `max(1.5rem, calc(50vw - 590px))`. Pad the *container*, never the first/last cells:
  cell padding steals width from equal grid columns and clips the first numeral. Numerals
  at `--t-mega` with `white-space:nowrap`; "81/81" is the constraint that sets the ceiling.
- **Proof drawers** — each metric is a `role="button"` with `aria-expanded` and
  `aria-controls`; the drawer is `inert` while collapsed. Opens to the command that produced
  the number, its output, and the date it ran.
- **Fleet** — radar (conic sweep, trailing blips naming agents as the beam passes) beside a
  process table (real cron expressions, animated load sparklines, OK/RUN/WAIT, ticking
  clock); below, a 24-hour strip with SYS and DAILY lanes and a red NOW marker. Panels carry
  a cursor-tracked radial glow via `--mx/--my`.
- **Compact fleet strip** — a single ruled line under the metrics carrying a live lane and a
  real countdown to the next run, linking down to the full instrument.
- **Capability matrix** — *not cards.* Ruled rows: `CAP/` number, title, description, and
  signal bars that light in the row's accent on hover.
- **Experience spine** — a left rule with a dot per role; the current role's rule and dot are
  green with a halo, and its title is a step larger.
- **Demos** — Brian OS: tabbed console auto-cycling LOGS → PYTEST (progress bar to "81
  passed") → STATE diff. Squares: 100-cell simulation with score ticker and pulsing winner;
  the button swaps in the real deployed app. BoomBox: gradient waveform over a queue labelled
  REDIS·TRANSIENT / POSTGRES·DURABLE.

---

## Neural — `neural.html`

**Concept.** A specimen under glass. Same structural problem as Mission Control, opposite
answer: the moves are editorial — negative space, typographic contrast, and one serif that
only ever appears in the light.

### Tokens

```css
/* 1. base */
--bg:#06070f;   --ink:#eff1fc;  --dim:#9aa2c4;
--teal:#3cf0c8; --violet:#927bff; --rose:#ff7bad; --gold:#ffd166;
--card:rgba(146,123,255,.05);  --line:rgba(146,123,255,.17);
--paper:#f5f2ea; --paper-ink:#16131f; --paper-dim:#5b586c;
--disp:'Syne',sans-serif; --body:'DM Sans',sans-serif; --mono:'DM Mono',monospace;
--ease:cubic-bezier(.22,1,.36,1); --spring:cubic-bezier(.34,1.56,.64,1);

/* 2. accessibility override */
--faint:#8087b0;        /* was #4c557c = 2.77:1, below AA */

/* 3. type scale + the serif */
--t-hero:clamp(2.7rem,5.4vw,4.5rem);
--t-mega:clamp(2rem,3.4vw,3.2rem);     /* metric numerals */
--t-sec:clamp(2rem,3.6vw,3rem);
--t-card:clamp(1.35rem,2vw,1.75rem);
--t-lead:clamp(1.02rem,1.2vw,1.14rem);
--serif:'Fraunces',Georgia,serif;
```

Fixed aurora backdrop: three radial gradients (violet top-right, teal left, rose bottom),
with an SVG grain layer over it so the gradients have tooth.

**Type.** Syne (600–800) display, DM Sans body, DM Mono for machine output. **Fraunces
appears exactly once — inside the light island.** That is the point: the break from dark to
light is a change of *voice*, not just a change of background. Do not use Fraunces anywhere
in the dark sections.

### The 3D hero

Three.js r128, self-hosted, **lazy-loaded**. The brain is a named `initBrain()` function, not
an IIFE; `#brain-loader` fetches the library when the canvas comes within 300px of the
viewport, or at first idle. It is **never fetched** for `prefers-reduced-motion` or when WebGL
is unavailable — those visitors get a text statement pointing at the same 26 agents below.

Four point clouds — cortex, cerebellum, brainstem, halo — with density scaled to 45% when
`innerWidth < 820` or `devicePixelRatio < 1.5`. The cortex sampler shapes an ellipsoid with a
long front-back axis, frontal taper, occipital fullness, widened temporal lobes, a flattened
underside and an interhemispheric fissure; two layered sinusoids add gyri. Additive glow
sprites, coloured rose → violet → teal by height.

26 agent nodes on the surface, joined by synapse lines under 0.85 units apart, with five
sprite pulses travelling eased paths. Drag to spin with inertia (0.95 rotational, 0.92
vertical), idle rotation, breathing scale, raycast hover naming the agent and its cron line,
and a callout cycling all 26 every 3.6s.

**Clicking a node opens the agent panel** — cron line, purpose, write scope, guardrail, with
prev/next through the fleet. The canvas is `role="application"`, focusable, and answers Enter
and the arrow keys. The panel is `inert` when closed.

### Components

- **Metric row** — no boxes. A ruled row of oversized Syne numerals; the numbers are the
  evidence and the card chrome was noise.
- **Project cards** — drift off-axis on alternating rows using `translateX(±1.8rem)`. Use
  transforms, **not margins**: margins push past the container and create a horizontal
  scrollbar at some widths. The visual pane also alternates sides.
- **Light island** — a cream card floating on the dark page, 32px radius, glow spill from two
  blurred circles, scale-pop entrance. Headline and skill titles in Fraunces; skills are ruled
  columns, not boxes.
- **Timeline** — spine is a gradient fading as it descends, since the recent role is the one
  that matters.
- **Demos** — hub-and-spoke routing with eased packets; the squares simulation; and a
  durable-vs-transient visualisation with a recurring `⟳ SERVER RESTART` that wipes the Redis
  lane while the Postgres blocks survive.

---

## Rules for editing

1. **Change numbers in both files.** Search `26`, `81/81`, and the date `2026-08-05`.
2. **Keep the source line.** Every metric states where it came from. Never add a number
   without one.
3. **The markup must hold the true value.** Metrics render correctly with JavaScript off;
   the count-up is an enhancement that always settles back on `data-final`. This was a real
   bug once — the page reported `0` agents to anyone without JS.
4. **Never claim live data.** The visualisations animate a real schedule; they are not
   connected to the machine. Captions say "simulation" or "replay" where relevant.
5. **Accent meanings are fixed.** Don't use green for a prototype or amber for a healthy state.
6. **Test with JS off** before shipping changes to reveal logic — all content must stay visible.
7. **Reveals toggle `visibility`, not just `opacity`.** Opacity alone leaves invisible links in
   the tab order. Focus entering a hidden block reveals it.
8. **Third-party frames load only on click.** Don't autoload the Squares iframe.
9. **Keep the pages request-free.** Fonts and three.js are self-hosted. Do not reintroduce a
   CDN link without also removing the "no third-party requests" claim from both footers.
10. **Don't exclude anything in `vendor/` with a directory-level negation** — see
    `vendor/README.md`. Vercel did not honour the re-include and shipped fonts 404ing.
11. **Full-bleed elements pad the container, not the first and last cells.**
12. **`cleanUrls` is on.** Link to `/neural`, never `/neural.html`, or canonical URLs and the
    sitemap end up pointing at 308s.
