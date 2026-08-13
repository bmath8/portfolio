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


---

# v7.1 - Self-hosted assets, new OG card, vendor prune (2026-08-12)

Three follow-ups from v7, all closed.

## Fonts and three.js are self-hosted

v7 shipped pulling Google Fonts on both pages and three.js r128 from cdnjs. That broke a
property the old site had been careful about, so the "no third-party requests" claim was
removed rather than left false. It is now true again and the claim is back.

Installed as npm packages so provenance and versions are reproducible:
`@fontsource/{archivo,syne,dm-sans,dm-mono,ibm-plex-mono}` and `three@0.128.0`. Sixteen
latin-subset woff2 faces - one per weight each page actually uses - plus the r128 UMD build
now live in `vendor/`, with `@font-face` blocks inline at the top of each page.

Verified in-browser: the Resource Timing API reports an empty list of non-origin requests on
both pages. The only outbound traffic left is a link a visitor clicks, or the Super Bowl
Squares iframe, which still loads only after an explicit click.

## og.png regenerated

The old card advertised the retired hero. The new one is drawn by `scripts/make_og.py` -
1200x630, Mission Control palette, the same self-hosted faces the page serves, with the
headline, the four metrics and the scheduler radar. Nothing generated, nothing stock.

Meta on both pages points at `og.png?v=7`, because LinkedIn and Twitter cache aggressively
by URL and would otherwise keep serving the old card.

## vendor/ pruned

Neither live page referenced anything in `vendor/` after the v7 rebuild. Forty-four files
were deleted: the ICBM152 meshes and their `.npy` sources, the tract-line bundle, the
bloom and bokeh post-processing pipeline, the HDR environment map, MarchingCubes, GSAP,
ScrollTrigger, Lenis, the three.js module build, and the previous font set.

12.7 MB -> 0.8 MB.

`.vercelignore` was rewritten as a consequence: every exclusion rule in it guarded a file
that no longer exists. The one hard-won rule is preserved - never use a directory-level
negation like `vendor/*` plus `!vendor/fonts/`, because Vercel did not honour the
re-include and shipped a deploy with every font 404ing. A new `vendor/README.md` records
what is vendored, how it was installed, and its licences.

The archived pages under `design-candidates/archive/` still reference some deleted assets.
They are kept as a record of what shipped, not as runnable pages; recover from git history if
one ever needs to run again.

## Verification

Both pages: no console errors, zero external resource requests, correct fonts applied
(Archivo/IBM Plex Mono and Syne/DM Sans/DM Mono), three.js r128 loaded from `/vendor/`, the
3D cortex rendering. `/`, `/neural.html`, `/og.png`, `/resume.pdf`, `/favicon.svg`
and every vendored font return 200.