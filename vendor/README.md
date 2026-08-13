# vendor/

Third-party assets, self-hosted so the live pages make **zero third-party requests**.

Everything in here is loaded by `index.html` or `neural.html`. If a file stops being
referenced, delete it — this folder previously grew to 12.7 MB of assets belonging to
approaches that had already been abandoned.

## Contents

| Path | Used by | Notes |
|---|---|---|
| `fonts/archivo-{500,600,700,800,900}.woff2` | `index.html` | Display and UI |
| `fonts/ibm-plex-mono-{400,500,600}.woff2` | `index.html` | Machine output, labels, cron lines |
| `fonts/syne-{600,700,800}.woff2` | `neural.html` | Display |
| `fonts/dm-sans-{400,500,700}.woff2` | `neural.html` | Body |
| `fonts/dm-mono-{400,500}.woff2` | `neural.html` | Machine output |
| `three.min.js` | `neural.html` | three.js r128 UMD build, for the 3D cortex |
| `three-LICENSE.txt` | — | MIT licence text for the above |

Total: ~0.8 MB.

## Where these came from

Installed as npm packages rather than downloaded ad hoc, so the provenance and version
are reproducible:

```bash
npm install @fontsource/archivo @fontsource/syne @fontsource/dm-sans \
            @fontsource/dm-mono @fontsource/ibm-plex-mono three@0.128.0
```

Fonts are the `latin` subset, one file per weight actually used — not the full family.
They are copied out of `node_modules/@fontsource/<family>/files/<family>-latin-<weight>-normal.woff2`
and renamed to `<family>-<weight>.woff2`. The `@font-face` blocks live inline at the top
of each page.

Licences: Archivo, Syne, DM Sans, DM Mono and IBM Plex Mono are all SIL Open Font License 1.1.
three.js is MIT.

## The 2026-08-12 prune

The v7 rebuild retired the cortical-mesh hero. The assets that served it were deleted:
the ICBM152 meshes and their `.npy` sources, the tract-line bundle, the bloom/bokeh
post-processing pipeline, the HDR environment map, MarchingCubes, GSAP, ScrollTrigger,
Lenis, the three.js module build, and the previous font set — 44 files, 11.9 MB.

The archived pages under `design-candidates/archive/` still reference some of them. Those
are kept as a record of what shipped, not as runnable pages. Recover an asset from git
history if one ever needs to run again.

## Rule

Do not exclude anything here in `.vercelignore` with a directory-level negation
(`vendor/*` plus `!vendor/fonts/`). Vercel did not honour that re-include — the deploy on
2026-08-05 returned 404 for every font and the site silently fell back to system faces.
Exclude by explicit filename if it is ever needed again.
