# Design system — both editions

Reference for maintaining `index.html` (Mission Control) and `neural.html` (Neural).
Both are single-file pages; all tokens live in `:root` at the top of each file.

---

## Mission Control — `index.html`

**Concept.** An operations console. The page is the instrument panel of a system that is running right now. Nothing decorative that isn't also informative.

### Tokens

```
--bg0  #04060a   base
--bg1  #081019   band A (work)      ice-tinted radial
--bg2  #061410   band B (fleet)     green-tinted radial
--bg3  #0b0a18   band C (stack)     violet-tinted radial
--panel #0c1520  --panel2 #122031  --line #1d3042  --line2 #2c4a63
--txt  #eaf3fb   --dim #93aabf     --faint #4c637a
--green #4af0a0  --ice #6fd3ff     --amber #ffc44d  --red #ff6161  --violet #b39bff
```

Sections alternate tonal bands so adjacent sections never blend. Each accent owns a meaning: green = healthy/live, ice = information, amber = attention/prototype, red = now/failure, violet = tertiary.

**Type.** Archivo (500–900) for display and UI. IBM Plex Mono for anything that represents machine output — labels, cron lines, logs, captions.

**Motion.** `--ease cubic-bezier(.22,1,.36,1)` for reveals, `--spring cubic-bezier(.34,1.56,.64,1)` for hover lifts. Staggered reveal delays `.d1 .d2 .d3` at 80ms steps. Section headings draw an underline on entry.

**Atmosphere.** Fixed scanline overlay (`body::before`) and vignette (`body::after`), both non-interactive, at low opacity. Hero canvas draws a perspective grid with drifting particles.

### Components

- **Status bar** — sticky, blurred, live dot, section links, HIRE call to action.
- **Console card** — terminal chrome plus a live log that prepends a new line every 1.8s, capped at 4 rows.
- **Stat strip** — four metrics, gradient top-edge per metric, count-up on first view, source line under each number.
- **Fleet** — radar (conic-gradient sweep, trailing blips, names revealed as the beam passes) beside a process table (real cron expressions, animated load sparklines, OK/RUN/WAIT states, ticking clock); below, a 24-hour strip with SYS and DAILY lanes and a red NOW marker.
- **Project row** — copy on the left, demo pane on the right, single hairline divider between.
- **Demos** — Brian OS: tabbed console auto-cycling LOGS → PYTEST (progress bar to "81 passed") → STATE diff. Squares: 100-cell simulation with score ticker and pulsing winner, button swaps in the real deployed app. BoomBox: gradient waveform over a queue labelled REDIS·TRANSIENT / POSTGRES·DURABLE.

---

## Neural — `neural.html`

**Concept.** The brain is the argument. Each glowing node is one real scheduled agent; the visitor can spin it and name any node.

### Tokens

```
--bg   #06070f    --ink #eff1fc   --dim #9aa2c4   --faint #4c557c
--teal #3cf0c8    --violet #927bff  --rose #ff7bad  --gold #ffd166
--card rgba(146,123,255,.05)   --line rgba(146,123,255,.17)
--paper #f5f2ea   --paper-ink #16131f   --paper-dim #5b586c
```

Fixed aurora backdrop: three radial gradients (violet top-right, teal left, rose bottom). The light island uses the paper tokens and is the page's single contrast break.

**Type.** Syne (600–800) display, DM Sans body, DM Mono for machine output.

**Motion.** Same easing pair as Mission Control. Cards use `.pop` — translate plus a slight scale — so they arrive rather than slide.

### The 3D hero

Three.js r128, ~5,300 points across four clouds: cortex, cerebellum, brainstem, and a faint outer halo. The cortex sampler shapes an ellipsoid with a long front-back axis, frontal taper, occipital fullness, widened temporal lobes, a flattened underside and an interhemispheric fissure; two layered sinusoids add gyri. Points render as additive glow sprites, coloured rose → violet → teal by height.

26 agent nodes sit on the surface, joined by synapse lines under 0.85 units apart. Five sprite pulses travel between nodes on an eased path. Interaction: drag to spin with inertia decay (0.95 rotational, 0.92 vertical), idle auto-rotation, a subtle breathing scale, raycast hover that names the agent and shows its cron line, and a callout that cycles through all 26 agents every 3.6s.

Failure paths: a `try/catch` around the renderer hides the canvas if WebGL is unavailable; the page is fully readable without it.

### The light island

The capabilities section is a cream card floating on the dark page — 32px radius, coloured glow spill from two blurred circles, scale-pop entrance. This replaces the earlier full-bleed light band, which needed gradient fades to avoid a hard seam.

### Demos

- **Brian OS** — hub-and-spoke routing: `hermes` at the centre, six labelled services around it, eased packets travelling with trailing streaks.
- **Squares** — same simulation as Mission Control, violet/teal palette; button loads the real app.
- **BoomBox** — the story is the restart: Redis streaks flow continuously, Postgres blocks accumulate, and every 7 seconds a `⟳ SERVER RESTART` flash wipes the Redis lane while the Postgres blocks survive.

---

## Rules for editing

1. **Change numbers in both files.** Search for `26`, `81/81`, and the date `2026-08-05`.
2. **Keep the source line.** Every metric states where it came from. Do not add a number without one.
3. **Never claim live data.** The visualisations animate a real schedule; they are not connected to the machine. Captions say "simulation" or "replay" where relevant.
4. **Accent meanings are fixed.** Don't use green for a prototype or amber for a healthy state.
5. **Test with JS off** before shipping a change to the reveal logic — all content must remain visible.
6. **Third-party frames load only on click.** Don't autoload the Squares iframe.
