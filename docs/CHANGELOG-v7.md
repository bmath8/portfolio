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

---

# v7.2 - Design audit follow-through (2026-08-12)

A measured audit of both live pages found one credibility bug, a set of
accessibility failures, and a pacing problem. Fixed in three tiers.

## Tier 1 - correctness and accessibility

**The metrics read 0 without JavaScript.** The footer claimed "core content
renders with JavaScript disabled" while every metric was hardcoded to `0` in
the markup and only filled in by the count-up. With JS off the page reported
0 agents, 0 tests, 0 systems - understating itself to nothing while claiming
otherwise. Real values now live in the HTML; the animation is an enhancement
that always settles back on them, with a safety timeout and a visibilitychange
handler so a hidden tab can never strand a number mid-count.

**Contrast.** `--faint` measured 2.95:1 on Mission Control and 2.77:1 on
Neural, both below AA - and it was the colour carrying the source line under
every metric. The receipts the page is built on were its least readable text.
Now 6.2:1, with caption sizes floored (the smallest was 9.28px).

**Focus.** Neither page defined a single focus style. Added `:focus-visible`
rings in each palette, plus a skip link and a `<main>` landmark, and fixed an
h2 to h4 heading jump.

**Motion.** `prefers-reduced-motion` only stopped CSS reveals; every canvas
and ticker kept running. Now all of them honour it, and pause on a hidden tab.

## Tier 2 - composition

Mission Control put 840px of fleet instrument between the metrics and the first
project, so the work began 1,721px down. A compact live strip now carries the
proof under the metrics and the full instrument moved below the work: first
project at 1,165px, about 560px sooner. The hero fills the viewport properly,
the radar stopped reallocating its canvas 60 times a second, and the log grew
to 20 entries with a random start.

Neural's brain gained roughly 100px and bleeds past its column, taking size from
the margin rather than the text column - which has to stay wide enough to hold
"A cortex" on one line. Project cards alternate sides so three cards stop
reading as one template.

## Tier 3 - craft

- **Proof drawers**: every Mission Control metric opens to show the command
  behind it and that command's output.
- **Clickable agent nodes**: Neural's 26 nodes each open a panel with the cron
  line, purpose, write scope and guardrail, walkable with prev/next and reachable
  by keyboard.
- **Keyboard navigation** on Mission Control (`g`+section, `?` for help).
- A left progress rail, and a single scramble-resolve load moment.
- Font preloading, schema.org Person JSON-LD, a print stylesheet, and a dedicated
  OG card for the Neural edition.

## Known follow-up

three.min.js (589 KB) still loads on the critical path for Neural. Deferring it
behind an intersection check would help mobile, but it needs the brain module
restructured rather than a one-line change, so it is deliberately not in this
pass.

---

# v7.3 — Second audit: accessibility, headers, discoverability, content (2026-08-12)

A measured re-audit of both live pages. Performance was already good — TTFB 145ms, DCL
303ms, CLS 0, no long tasks, 21KB HTML — so this pass is everything else.

## Accessibility — seven measured failures, several self-inflicted

- **`#brain` was focusable *and* `aria-hidden="true"`** — a WCAG 4.1.2 violation. The v7.2
  pass marked every canvas decorative and clobbered the label the interactive brain needs.
  It is now `role="application"` with a real description, and only the decorative canvases
  are hidden.
- **Eight focusable elements sat inside `opacity:0` containers.** Five were project links in
  cards that had not scroll-revealed yet — the reveal animation was putting invisible links
  in the tab order. Reveals now toggle `visibility` as well as opacity, and focus entering a
  hidden block reveals it immediately.
- **The agent panel stayed in the accessibility tree when closed**, announcing its
  placeholder text. It is now `inert` with its buttons out of the tab order.
- **Proof drawers** gained `aria-controls` and are `inert` while collapsed; `max-height:0`
  hides nothing from assistive tech.
- **The shortcut dialog** had `role="dialog"` but was never hidden, had no `aria-modal`, no
  focus trap and no focus restore. All four fixed.
- **Heading outline:** the panel and dialog titles were `<h4>` directly under `<h1>`. They
  are labels, not document structure, so they are no longer headings.
- The fleet strip is an `<a>` around four children and had no accessible name; external
  links now announce that they open a new tab.

## Delivery

`vercel.json` added. Fonts and vendored JS were being served with `Cache-Control: max-age=0`,
so every visit revalidated all eight woff2 files; they are now immutable for a year. Added
CSP, `Referrer-Policy`, `X-Content-Type-Options`, `X-Frame-Options` and `Permissions-Policy`
— only HSTS was set before.

## Discoverability

`sitemap.xml` referenced from `robots.txt`; `site.webmanifest` and an apple-touch-icon; and a
real 404 page in the Mission Control palette that resolves the path that missed and routes
back to the work, instead of Vercel's generic page.

## Content

- Per-project stack tags, so the technology is scannable rather than buried in prose.
  Nothing new is claimed — the tags come from the existing copy.
- An availability line: US citizen, authorized to work in the US without sponsorship, US
  Eastern, available now, and **willing to relocate anywhere including internationally**.
  These are top-of-list screening filters and their absence causes silent rejections.
- **The process-guardian incident**, previously one bullet, now has its own full-width block:
  symptom, trace, fix, prevented. It is the strongest evidence on the page — a silent failure
  found, traced, fixed, and then covered by a test that is part of the 81 — and it was buried.

## Analytics

Vercel Analytics (first-party, cookieless, no consent banner). There was previously no way to
tell whether anyone opened the site or the résumé.

## One self-inflicted regression, caught and fixed

`cleanUrls` in the new `vercel.json` made `/neural.html` a 308 to `/neural`, which turned the
canonical tags, `og:url`, the sitemap entry, both footer cross-links, the 404 route listing
and the `n` keyboard shortcut into redirects. A canonical URL that redirects quietly costs
search ranking. All references now point at the clean URL.

---

# v7.4 — Design pass: an aesthetic point of view for each page (2026-08-12)

The functional work was done; the design was not. Measured, the page was **nine sections at
exactly 1180px, eleven rounded cards, and a type scale that jumped 78px → 29px → 16px with
nothing in the middle.** Competent, and anonymous.

Two directions, deliberately different, because the pages argue differently.

## Mission Control — industrial telemetry

The page is a panel on a machine that is running, so the vocabulary is measurement rules,
registration marks and oversized tabular numerals rather than more rounded rectangles.

- **Bricolage Grotesque** for display — engineered and slightly odd where Archivo is neutral,
  and it holds up at the sizes this page now uses.
- A real type scale with a middle, on a 1.28 ratio.
- **The metric strip goes full-bleed**, edge to edge, with numerals up to 4.7rem. It is the
  strongest asset on the page and it was sitting in a small boxed row.
- **Capabilities became a capability matrix** — ruled rows, `CAP/` numbering, and signal bars
  that light in the accent colour of the row on hover. This was the weakest section: four
  identical cards with 13.6px text.
- **Experience became a spine** with a live marker on the current role, instead of a flat
  table with the dates right-aligned in grey.
- Film grain over the whole surface, the console tilted slightly off-axis, a cursor-tracked
  glow in the fleet panels, and shimmer on the primary actions.

## Neural — luminous specimen

Same structural problem, opposite answer: this page is a specimen under glass, so the moves
are editorial.

- **Fraunces enters exactly once, in the light island**, so the break from dark to light is a
  change of voice and not just a change of background. That is the page's strongest moment
  and it was set in the same sans as everything around it.
- The metric orbs lose their boxes and become a ruled row of oversized numerals. The numbers
  are the evidence; the card chrome was noise.
- Cards drift off-axis on alternating rows, using transforms rather than margins so nothing
  can push past the container.
- The timeline spine became a gradient that fades as it descends, since the recent role is the
  one that matters.
- Grain over the aurora so the gradients have tooth instead of reading as flat CSS.

## Verification

Both pages at 1568px and 390×844: no horizontal overflow, no console errors, CLS 0, DCL
376ms, zero external requests. The accessibility work from v7.2 and v7.3 is untouched.

Two judgement calls worth revisiting if they don't land: the fleet cursor-glow and the tilted
console are subtle enough to be missed until hover, and the alternating card offsets on
Neural are a deliberate asymmetry some people dislike. Both are one-line reverts.
