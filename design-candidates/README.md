# design-candidates/

Rejected and superseded drafts, kept as a record. **`.vercelignore` excludes this whole folder**,
so nothing here is deployed.

## ⚠️ Most of these no longer run — 2026-08-26

The previous version of this file explained how to serve the candidates so their libraries
resolve. That advice is now obsolete: **the libraries were deleted.** The v7.1 vendor prune took
`vendor/` from 12.7 MB to 0.8 MB, and removed everything the drafts depended on.

Measured today — of 56 candidates, 18 reference `../vendor/`, and **every path they reference is
gone**:

| Referenced by | Path | Status |
|---|---|---|
| 15 candidates | `../vendor/fonts.css` | **missing** — v7 inlines `@font-face` instead |
| 7 candidates | `../vendor/gsap.min.js` | **missing** |
| 6 candidates | `../vendor/ScrollTrigger.min.js` | **missing** |
| 6 candidates | `../vendor/lenis.min.js` | **missing** |

So a candidate opened today loads with no fonts and, if it used motion, no animation. Serving it
from the repo root — the fix this file used to prescribe — does not help, because the problem is
no longer the document root. The old diagnostic (`typeof gsap === 'object'`) now fails however
you serve it.

**To actually run one**, recover its dependencies from history:

```bash
git log --oneline --diff-filter=D -- vendor/gsap.min.js     # find the deleting commit
git checkout <sha>^ -- vendor/gsap.min.js vendor/ScrollTrigger.min.js \
                       vendor/lenis.min.js vendor/fonts.css
python3 -m http.server 8801 --directory .                   # serve from the REPO ROOT
# then open http://127.0.0.1:8801/design-candidates/G-motion.html
```

Delete them again afterwards. They must not come back into `vendor/` — `vendor/README.md`
records why each was dropped.

## What still matters here

`archive/` holds the three drafts worth keeping whole:

| File | What it is |
|---|---|
| `v6-brain-hero.html` | The retired homepage — scroll-jacked cortical-mesh hero. Archived when v7 shipped. |
| `v6-main-scroll-world.html` | The scroll-world variant of the same era. |
| `v17-schedule-field.html` | A homepage whose hero geometry was **generated from the cron lines** rather than modelled — time of day across X, one agent lane per Z, a mark standing where each fires. Never shipped; kept for the technique. |

The four v7 finalists are at the top level: `mission-control-v3.html` and `neural-v3.html`
(which became `/` and `/neural`), plus `editorial-dossier.html` and `brutalist.html`, which were
not taken forward.

> Note: `docs/AUDIT-2026-08-12.md` discusses these four as `option-1-mission-control.html`
> through `option-4-brutalist.html`. Those were working names in that session and **were never
> committed** — the filenames above are what exists.
