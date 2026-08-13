# v7 — Dual-design rebuild (2026-08-12)

Full top-to-bottom redesign. Two complete designs now ship: Mission Control at `/`, Neural at `/neural.html`. The previous homepage is archived at `design-candidates/archive/v6-brain-hero.html`.

## Why the rebuild

The v6 homepage had strong content and a weak vehicle. Audit findings:

1. **Scroll-jacked hero.** The pinned 3D brain consumed several viewports before any project appeared. Recruiters spend seconds on a portfolio; the delay cost interviews.
2. **Dead zones.** Multiple full viewports of black between sections. Paging with PageDown landed on empty screens, and reveal-on-scroll content could stay invisible if observers didn't fire.
3. **Render artifacts.** A duplicated header and a white bar appeared mid-page during review.
4. **The brain fought the message.** At hero scale it competed with the headline for contrast, and its payoff — hover a node to name an agent — was buried.
5. **Flat below the fold.** All personality lived in the hero; everything after it collapsed into uniform dark cards.
6. **Metrics below the fold.** The four proof numbers, the page's strongest asset, sat behind the animation.

## What shipped

### Both editions
- Metrics visible in the first screen, with count-up on entry and a source line under every number.
- Live demo panes beside every project; the real Squares app loads in-frame on click.
- Distinct tonal treatment per section so nothing blends.
- Eased reveal transitions with staggered delays; `prefers-reduced-motion` respected.
- Load-time reveal pass so above-the-fold content never waits for a scroll.
- Full SEO/OG/Twitter meta, canonical URLs, favicon, theme-color per palette.
- Cross-links between editions in both footers.

### Mission Control (`index.html`)
- Ops-console layout: sticky status bar, terminal card with a live log stream.
- Fleet section rebuilt: radar with conic sweep and trailing named blips, agent process table with real cron expressions and animated load sparklines, 24-hour lane strip with a NOW marker.
- Demo upgrades: tabbed LOGS/PYTEST/STATE console, playable squares simulation with score ticker, BoomBox waveform with durable/transient labelling.
- Palette widened to five accents with fixed meanings; scanline and vignette atmosphere.

### Neural (`neural.html`)
- Brain rebuilt in Three.js with anatomical shaping — frontal taper, temporal lobes, cerebellum, brainstem, interhemispheric fissure, layered gyri — rendered as additive glow sprites rather than flat squares.
- Drag-to-spin with inertia, idle drift, breathing scale, hover tooltips showing agent name and cron line, and a callout cycling all 26 agents.
- Light contrast break reworked from a full-bleed band into a floating cream island with glow spill and a scale-pop entrance.
- Demos: hub-and-spoke message routing, squares simulation, and a durable-vs-transient visualisation with a recurring server-restart event.

## Not shipped, kept for reference
- `design-candidates/editorial-dossier.html` — light editorial/Swiss direction.
- `design-candidates/brutalist.html` — loud brutalist direction.

## Verification
- Both pages served over HTTP and loaded end to end; no console errors.
- `/`, `/neural.html`, `/favicon.svg`, `/og.png`, `/resume.pdf` all return 200.
- Fleet visualisations, all three demo panes, count-ups, reveals and cross-links confirmed working.
