# AGENTS.md — portfolio

Guidance for AI coding agents working in this repo. Accurate as of **v7.4, 2026-08-12**.
Read `AGENT_RULES.md` for operating discipline; this file is about *this* codebase.

## What this is

Brian's employer-facing portfolio, deployed on Vercel at **bmath8.vercel.app**. Zero build
step. **Two complete designs ship**, both maintained, both carrying identical content:

| Route | Design | File |
|---|---|---|
| `/` | **Mission Control** — ops-console aesthetic | `index.html` |
| `/neural` | **Neural** — 3D cortex hero, Three.js | `neural.html` |

Each is a single self-contained HTML file with inline CSS and JS. They cross-link in their
footers. `docs/DESIGN-SYSTEM.md` is the reference for tokens, components and editing rules —
**read it before changing either page's appearance.**

## Status: PUBLIC

The site is public and indexable. The old password gate (`middleware.js`) and `ats/`
directory were removed at the 2026-06 launch and `robots.txt` allows indexing. Do not
reintroduce a gate without Brian's approval.

## ⚠️ The resume: do not edit it here

`resume.pdf` in this repo is a **copy** of canonical output built in `C:\Brian\03_Career\`.
Currently: `resumes/variants/L3_strong/Brian_Mathew_AI_Builder_L3_strong.pdf` (deployed
2026-08-19). Swap lane or strength by copying a different file from `variants/`.
Do not hand-edit it, and **do not regenerate it from `resume/resume.html`** — that file is
superseded (see `resume/SUPERSEDED-2026-07-29.md`) and rendering it would overwrite the
canonical resume with an older, incomplete one that lacks LinkedIn.

To refresh: rebuild in `C:\Brian\03_Career\`, then copy the canonical PDF over `resume.pdf`
here. See `INVENTORY.md` §1 for the full picture.

## Hard-won rules — each of these was a real bug

**Truthfulness is the product.** The page's entire argument is that every number is
checkable. Two consequences:
- Metric values live in the **markup**, not only in JavaScript. The count-up is an
  enhancement that always settles back on `data-final`. The page once reported `0` agents to
  anyone with JS disabled while claiming in its footer that it rendered without JS.
- Never claim live data. The fleet visualisations animate a *real schedule*; they are not
  connected to the machine. Captions say "simulation" or "replay".
- If a project fact changes, change it in **both** HTML files, and keep it consistent with
  `resume.pdf`. Search `26`, `81/81`, `2026-08-05`.

**Zero third-party requests.** Fonts and Three.js are self-hosted in `vendor/`. Do not add a
CDN link without also deleting the "no third-party requests" claim from both footers. The
Squares iframe loads only after an explicit click.

**`vendor/` exclusions must be by explicit filename.** Never `vendor/*` plus
`!vendor/fonts/` — Vercel did not honour that re-include and shipped a deploy with every
font 404ing. See `vendor/README.md`.

**Link to `/neural`, never `/neural.html`.** `cleanUrls` is on in `vercel.json`, so the
`.html` form 308s. Canonical tags, `og:url` and the sitemap pointing at a redirect costs
search ranking.

**Accessibility invariants** — these were measured failures, don't regress them:
- Reveal-on-scroll toggles `visibility`, not just `opacity`. Opacity alone leaves invisible
  links in the tab order.
- A focusable element must never be `aria-hidden`. The brain canvas is `role="application"`
  with a label; only decorative canvases are hidden.
- Collapsed drawers and the closed agent panel are `inert`.
- `--faint` in each page's second `:root` block is a contrast fix (6.2:1). Don't darken it.
- Every timer and animation frame honours `prefers-reduced-motion` and pauses on hidden tabs.

**Full-bleed elements pad the container, not the first and last cells.** Cell padding steals
width from equal grid columns and clips content.

## Layout

```
index.html  neural.html  404.html        the site
vercel.json                             caching, security headers, cleanUrls
sitemap.xml  robots.txt  site.webmanifest
og.png  og-neural.png                   link preview cards, one per edition
vendor/                                 self-hosted fonts + three.js  (README inside)
docs/                                   DESIGN-SYSTEM, CHANGELOG-v7, AUDIT
scripts/                                make_og*.py, build_ttf.py, verify-demos.ps1
scripts/applied/                        one-shot migrations, already applied — DO NOT RE-RUN
design-candidates/                      shipped snapshots, unshipped directions, archive/
```

`docs/`, `scripts/`, `design-candidates/`, `scratchpad/` and all `*.md` are excluded from the
deploy by `.vercelignore` — verify against the deployed URL, never against git.

## Local development

Serve over HTTP; `file://` breaks the root-relative asset paths:

```bash
python -m http.server 8080
# http://127.0.0.1:8080/  and  /neural.html
```

## Before you say you're done

- No console errors on either page.
- No horizontal overflow at 390px.
- Content still visible with JavaScript disabled.
- Metrics still show real values, not `0`.
- `/`, `/neural`, `/resume.pdf`, `/og.png`, `/favicon.svg` all 200 **on the deployed URL**.
