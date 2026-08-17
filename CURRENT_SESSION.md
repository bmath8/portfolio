# Current Session

_Working state for whoever picks this repo up next — human or agent._
_Last updated: **2026-08-12**, end of the v7.4 documentation pass._

`AGENT_RULES.md` asks that this file be updated after each milestone. The previous 35 KB of
content described the v6 brain-hero build, which was retired on 2026-08-12; it is archived at
`docs/archive/v6/`.

---

## Where the site stands

**Two designs ship, both maintained.** `/` is Mission Control (ops console), `/neural` is the
Neural edition (3D cortex, Three.js). Identical content, cross-linked in their footers.

Live and verified on the deployed URL:

- No console errors on either page. **CLS 0**, DCL ~376ms, TTFB ~145ms.
- **Zero third-party requests** — fonts and Three.js self-hosted from `vendor/` (21 faces,
  0.89 MB total). Three.js is lazy-loaded and never fetched at all under
  `prefers-reduced-motion` or without WebGL.
- No WCAG failures outstanding. AA contrast, focus rings, `<main>`, skip link, inert
  collapsed regions, reduced-motion honoured by every timer and animation frame.
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
- [ ] **Public-safe showcase mirrors** for the private case-study repos (pre-existing item,
      see `TASKS.md`). The resume points at work nobody can open.
- [ ] **Revoke the leaked Tenor/Google API key** still in `boombox-v5` git history
      (pre-existing, `TASKS.md`).
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
