# Current Session

_Working state for whoever picks this repo up next — human or agent._
_Last updated: **2026-08-26**, end of a documentation-accuracy pass._

`AGENT_RULES.md` asks that this file be updated after each milestone. The previous 35 KB of
content described the v6 brain-hero build, which was retired on 2026-08-12; it is archived at
`docs/archive/v6/`.

---

## Where the site stands

**Two designs ship, both maintained.** `/` is Mission Control (ops console), `/neural` is the
Neural edition (3D cortex, Three.js). Identical content, cross-linked in their footers.

Live and verified on the deployed URL:

- No console errors on either page. **CLS 0**, DCL ~376ms, TTFB ~145ms.
- **No third-party requests until the visitor asks.** Fonts and Three.js are self-hosted from
  `vendor/` (21 faces, 0.89 MB). Three.js is lazy-loaded and never fetched at all under
  `prefers-reduced-motion` or without WebGL. Two deliberate exceptions, both stated rather
  than buried: Vercel Web Analytics reports to `vitals.vercel-insights.com` at runtime (the
  script itself is same-origin, so a host-based audit reports zero — see README), and the
  Squares demo iframes the real app, but only on click.
- No WCAG failures outstanding. AA contrast, focus rings, `<main>`, skip link, inert
  collapsed regions.
- **Reduced motion is now genuinely honoured by every timer and animation frame — as of
  2026-08-26.** It was not before. The `setInterval`/`requestAnimationFrame` wrapper was
  correct but loaded *after* the main page script, so 8 of 11 tickers on Mission Control and
  4 of 5 on Neural bound to the unwrapped originals and kept running under `reduce`. Moving
  the wrapper above the page script fixed it. Re-verified by byte-comparing frames: identical
  under `reduce`, still different with motion on.
- Security headers set (CSP, Referrer-Policy, nosniff, X-Frame-Options, Permissions-Policy);
  fonts and vendored JS immutable for a year.
- `sitemap.xml`, branded `404.html`, `site.webmanifest`, one OG card per edition.
- Vercel Web Analytics enabled and collecting.
- Phone layout verified at 390×844, no horizontal overflow.

**Git:** `main` is the deploying branch. `hero-v17` carries the same work and is pushed in
parallel. Both were at `8531a6c` / `9109e9c` after the documentation pass.

---

## The v7 arc, in one paragraph

v7 replaced a scroll-jacked single-page brain hero with two designs. v7.1 self-hosted the
assets and pruned `vendor/` from 12.7 MB to 0.8 MB. v7.2 fixed a credibility bug (metrics
rendered `0` without JS while the footer claimed otherwise), closed accessibility gaps, pulled
the projects ~560px up the page, and added proof drawers, clickable agent nodes and keyboard
navigation. v7.3 was a second measured audit: seven accessibility failures — several caused by
v7.2 — plus caching and security headers, sitemap, 404, per-project tech tags, the availability
line, and the process-guardian incident promoted from one bullet to its own block. v7.4 gave
each page an aesthetic point of view and then brought the documentation back in line with
reality. Full detail with reasoning is in `docs/CHANGELOG-v7.md`.

---

## Open items

Nothing is broken or half-applied. Genuinely open:

- [ ] **Decide whether Neural stays a second page** or becomes a toggle on one page. Two
      pages means every content change must be made twice — currently handled by discipline
      and a note in `AGENTS.md`, not by tooling.
- [ ] **Confirm the leaked Tenor/Google API key is revoked and not in public history.**
      Logged against `boombox-v5` (not public). `boombox` **is** public and linked from the
      site; if they share history the key is readable. Scan and revoke — see `TASKS.md`.
- [x] ~~Public-safe showcase mirrors~~ — **not needed.** All three featured repos were
      verified public on 2026-08-12; every "read the source" link resolves anonymously.
- [ ] Two v7.4 judgement calls worth a second opinion: the fleet cursor-glow and tilted
      console are subtle enough to miss, and Neural's alternating card offsets are a
      deliberate asymmetry some dislike. Both are one-line reverts.

## Things that will bite you if you don't know them

Read the "Hard-won rules" section of `AGENTS.md` before editing either page — every rule
there is a bug that actually happened. The three most expensive:

1. Metric values must live in the **markup**. Not only in JS.
2. `vendor/` exclusions by explicit filename only — never a directory-level negation.
3. Link to `/neural`, not `/neural.html`.

And do not regenerate `resume.pdf` from `resume/resume.html` — that source is superseded.

---

## 2026-08-26 — documentation accuracy pass

The site was in good shape; the documentation around it was not. Three kinds of drift, all
fixed:

**1. Numbers.** Six files still quoted 25/26/29 agents and 81/157 tests. The machine reports
**30 and 221**, and `resume.pdf` already said so — verified by extracting the PDF's own text,
which made an "Open" task in `TASKS.md` demonstrably stale. Corrected in `README.md`,
`AGENTS.md`, `INVENTORY.md`, `docs/DESIGN-SYSTEM.md`, `cover-letter-template.md`, `TASKS.md`.

Root cause, now addressed: the figures were hand-copied into every file with no single
definition. `README.md` gained a **"The numbers"** section that is now the one place they are
defined, with the command to re-derive each. `AGENTS.md` and `docs/DESIGN-SYSTEM.md` point at
it instead of listing their own search tokens.

**2. Five v6 documents were still at the repo root**, where they read as current:
`TECHNIQUE.md`, `DESIGN-REFERENCE.md`, `SCENE-BRIEF.md`, `REFERENCES-2026-08-05.md`,
`RESEARCH-2026-08-11.md`. All describe the retired cortical-mesh hero. Moved to
`docs/archive/v6/` alongside the three already there, and that folder's README now says what
each is still good for.

**3. `PROJECT_BRIEF.md` described a different project** — "a single-page portfolio", "inline
CSS, Google Fonts". Rewritten: two editions, self-hosted everything, no build step.

Also corrected an internal contradiction: this file claimed "Zero third-party requests" eight
lines above "Vercel Web Analytics enabled and collecting." Both pages do make one third-party
*connection* at runtime. The claim is now stated precisely rather than reassuringly.
