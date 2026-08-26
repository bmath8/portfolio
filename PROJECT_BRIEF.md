# Project Brief — Portfolio Site

_Rewritten 2026-08-26. The previous version described a single-page site with inline CSS and
Google Fonts. None of that has been true since v7._

## Project

Brian Mathew's personal portfolio: the page a recruiter opens from a résumé, a LinkedIn
profile, or an application. **Two complete designs ship**, carrying identical content:

| Route | Edition | File |
|---|---|---|
| `/` | **Mission Control** — ops-console layout, live log, fleet radar, agent process table | `index.html` |
| `/neural` | **Neural** — 3D cortex hero built procedurally in Three.js | `neural.html` |

Plus a branded `404.html`. `cleanUrls` is on, so the second page is `/neural` — never
`/neural.html` — in every canonical URL, link and sitemap entry.

## Product goal

Be openable in seconds and survive scrutiny. A recruiter should hit a number, a claim, or a
demo and be able to check it without asking. That is the whole positioning: **everything on
the page is verifiable**, and every figure says where it came from.

## Tech stack

- **No build step, no framework, no backend.** Each page is one self-contained HTML file with
  inline CSS and inline JS.
- **Self-hosted assets only.** Fonts (`vendor/fonts/`, 21 faces) and Three.js
  (`vendor/three.min.js`, r128, lazy-loaded by Neural alone) are vendored. No Google Fonts, no
  CDN.
- Deployed on **Vercel** from `github.com/bmath8/portfolio`. `vercel.json` sets `cleanUrls`,
  security headers (CSP, Referrer-Policy, nosniff, X-Frame-Options, Permissions-Policy) and
  immutable caching for fonts and vendored JS.

## Key architectural decisions

- **Static and self-contained**, so deployment is trivial and free, and so the page has no
  runtime that can rot.
- **The page must render with JavaScript disabled.** Content is in the HTML; JS only enhances.
- **`prefers-reduced-motion` is honoured by CSS *and* JS.** A wrapper around `setInterval` and
  `requestAnimationFrame` gates every ticker and canvas loop. It must load **before** any
  ticker registers — see `docs/archive/v6/README.md`'s sibling note in `TASKS.md` for the
  load-order bug this caused on 2026-08-26.
- **Third-party requests are avoided**, with one deliberate exception: Vercel Web Analytics.
  See "Analytics" in `README.md` for the precise, honest wording of that claim.

## Constraints

- Every number on the page must be re-derivable from a command or a file. See **"The numbers"**
  in `README.md` — that is the single definition, and the reason this repo keeps drifting when
  figures are hand-copied.
- Demos must be openable, not screenshotted. The Squares app loads the real deployment in-frame
  on click.

## Definition of done

Deployed, with both editions reachable and cross-linked; every claim on the page traceable to a
source; no WCAG AA failures; renders without JS; and `resume.pdf` carrying the same figures as
the site.
