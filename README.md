# Brian Mathew — Portfolio

Live: **https://bmath8.vercel.app/**

Static site, no build step. Two complete, independently maintainable designs ship in this repo.

| Route | Design | File |
|---|---|---|
| `/` | **Mission Control** — ops-console aesthetic | `index.html` |
| `/neural` | **Neural** — 3D cortex hero (Three.js) | `neural.html` |

Both pages carry the same content and the same claims. Each links to the other in its footer, so a visitor can switch editions without leaving the site.

---

## Why two designs

Mission Control is the default because it matches the pitch — *I build systems, then I keep them running* — and it is the fastest page for a recruiter to scan: proof metrics land in the first screen, live demos sit beside every project.

Neural is the visual-impact edition. It keeps the original brain concept but fixes what never worked about it: no scroll-jacking, no page-dominating 3D, and the payoff (each node is a real scheduled agent) is legible in the first few seconds.

Both are kept current. If a number changes, change it in both files.

---

## Structure

```
index.html                      Mission Control (homepage)
neural.html                     Neural edition            -> /neural
404.html                        Branded not-found page
vercel.json                     Caching, security headers, cleanUrls
sitemap.xml  robots.txt         Discoverability
site.webmanifest  favicon.svg   Install / icon
og.png  og-neural.png           Link preview cards, one per edition
resume.pdf                      Linked from both pages
vendor/
  fonts/*.woff2                 21 self-hosted faces (see vendor/README.md)
  three.min.js                  r128, lazy-loaded by neural.html only
docs/
  DESIGN-SYSTEM.md              Tokens, components, rules for editing
  CHANGELOG-v7.md               v7 through v7.4, with the reasoning
  AUDIT-2026-08-12.md           The audit that started the rebuild
scripts/
  make_og.py  make_og_neural.py Regenerate the link preview cards
  verify-demos.ps1              Check the live demo links resolve
  applied/                      One-shot migrations, already applied - do not re-run
design-candidates/
  mission-control-v3.html       Snapshot of the shipped homepage
  neural-v3.html                Snapshot of the shipped neural page
  editorial-dossier.html        Light editorial direction (not shipped)
  brutalist.html                Brutalist direction (not shipped)
  archive/                      Previous production homepages
```

---

## Local development

No toolchain required. Serve the folder over HTTP (needed because both pages load fonts and three.js from `/vendor/`, which are root-relative paths):

```bash
cd C:\Brian\02_Projects\portfolio
python -m http.server 8080
# then open http://127.0.0.1:8080/  and  http://127.0.0.1:8080/neural.html
```

Opening the files directly with `file://` will not work properly: the root-relative asset paths (`/vendor/fonts/*`, `/vendor/three.min.js`, `/favicon.svg`, `/resume.pdf`) resolve against the drive root and 404, so you get fallback fonts and no 3D brain. Use the server.

---

## Deployment

Vercel, connected to `github.com/bmath8/portfolio`. Static output, no framework. `vercel.json` sets caching (fonts and vendored JS immutable for a year), a security header set (CSP, Referrer-Policy, nosniff, X-Frame-Options, Permissions-Policy) and `cleanUrls`, which is why the Neural edition is linked as **`/neural`** and not `/neural.html` — the `.html` form 308s, so pointing canonical tags or the sitemap at it would send crawlers through a redirect. Push to the default branch to deploy.

Web Analytics is enabled in the Vercel dashboard; both pages load the first-party, cookieless script, so no consent banner is required.

---

## Technical notes

**No build, no dependencies to install.** Each page is one self-contained HTML file with inline CSS and JS. Fonts and three.js are self-hosted from `vendor/`, so the pages make **zero third-party requests** — the only outbound traffic is a link a visitor clicks, or the Super Bowl Squares iframe, which loads only after an explicit click. See `vendor/README.md` for what is vendored and how it was installed.

**Graceful degradation.** Both pages set a `.js` class at runtime; reveal animations only apply when JS is on, so all content is visible with JS disabled. If WebGL is unavailable the neural page hides the canvas and the rest of the page is unaffected. `prefers-reduced-motion` disables reveal transitions.

**Demos load on request.** The Super Bowl Squares card shows a self-contained simulation by default; the real deployed app is only iframed after the visitor clicks the button. Nothing third-party loads unprompted.

**Above-the-fold reveal.** An IntersectionObserver drives scroll reveals, with a load-time pass that reveals anything already in view — so the hero never sits blank waiting for a scroll.

**Accessibility.** Semantic headings in document order, real `<a>` elements for all navigation, visible focus via browser defaults, and text contrast checked against WCAG AA on both palettes.

---

## Claims and their sources

Every number on both pages is checkable and states its origin inline:

- **26 agents live** — count from `hermes cron list`, 2026-08-05
- **81/81 tests green** — live `pytest` run, 31.02s, 2026-08-05
- **3 systems shipped** — Brian OS, Super Bowl LX Squares, BoomBox
- **0 manual triggers** — every agent runs on a cron line

The agent names and cron expressions rendered in the fleet visualisations are the real schedule. The process table, radar, live log and project demos are animated presentations of that schedule — they are visualisations, not a live socket to the machine, and the page never claims otherwise.

---

## Projects featured

- **Brian OS** — 26-agent native-Windows fleet in Python. https://github.com/bmath8/brian-os
- **Super Bowl LX Squares** — live real-time app. https://fam-super-bowl-squares-2026.vercel.app · https://github.com/bmath8/fam-super-bowl-squares-2026
- **BoomBox** — Next.js/TypeScript prototype. https://github.com/bmath8/boombox

---

## Contact

Brian Mathew · New Jersey · open to work
mathew.brian@gmail.com · (609) 815-1685
https://github.com/bmath8 · https://linkedin.com/in/brian-mathew-66235556
