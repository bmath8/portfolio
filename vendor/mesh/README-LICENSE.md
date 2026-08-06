# Mesh assets — licence status

## ✅ `brain-icbm152.bin` — SHIPPABLE. Use this one.

Generated 2026-08-05 from the **MNI ICBM152 2009c nonlinear symmetric** template
(`mni_icbm152_nlin_sym_09c`), by thresholding the combined grey-matter + white-matter
probability maps and running marching cubes. GM+WM is used rather than the supplied brain
mask because the mask produces a smooth bean with no gyri; the GM/WM boundary is what carries
the folds.

**39,828 vertices · 79,644 triangles · 1,314,188 bytes** — less than half the AGPL asset.

This closes option 1 of the three listed in the previous version of this file:
*"obtain the ICBM152 / CIVET surface from MNI directly, under its own terms."*

### Required attribution — reproduce this notice wherever the asset ships

> Copyright (C) 1993–2004 Louis Collins, McConnell Brain Imaging Centre,
> Montreal Neurological Institute, McGill University.
> Permission to use, copy, modify, and distribute this software and its documentation for any
> purpose and without fee is hereby granted, provided that the above copyright notice appear
> in all copies. The authors and McGill University make no representations about the
> suitability of this software for any purpose. It is provided "as is" without express or
> implied warranty.

Source: <https://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/mni_icbm152_nlin_sym_09c_nifti.zip>
Also cite Fonov et al. (2011) and Fonov et al. (2009) if used academically.

**The licence is permissive — "any purpose and without fee" — so this is safe on a public
site.** The only obligation is carrying the copyright notice above. Put it in the page source
or a credits line.

### Regenerating
`build_mesh.py` (kept with the session scratchpad; needs `nibabel`, `scikit-image`, `scipy`).
Raise `STEP` to cut triangle count. Output matches the existing binary format exactly, so no
loader change is needed:

```
uint32 nVerts, uint32 nTris
int16 [nV*3] positions  (/32767, unit-normalised)
int8  [nV*3] normals    (/127)
uint32[nT*3] indices
```

---

## 🚩 `brain-mni.bin` — AGPL-3.0. DO NOT DEPLOY.

Derived from `aces/brainbrowser` → `examples/models/brain-surface.obj.gz`, an MNI/CIVET
cortical surface. **BrainBrowser is AGPL-3.0** (verified against the GitHub API, 2026-08-05).

81,924 vertices · 163,840 triangles · 2,703,404 bytes.

**It was being served publicly** at `https://bmath8.vercel.app/vendor/mesh/brain-mni.bin` —
verified HTTP 200 on 2026-08-05 — on the URL printed on all four résumés, despite
`index.html` never referencing it. `.vercelignore` had excluded only three specific vendor JS
files, so everything else under `vendor/` shipped.

**Fixed and deployed** in commits `792de58` and `f50b67e`. The mesh now returns 404 live.

Keep this file for local comparison only, or delete it once `brain-icbm152` is confirmed good.

> Gotcha worth remembering: `vendor/*` plus `!vendor/fonts/` is correct under git's matcher
> but **Vercel does not honour the directory re-include** — that pattern silently 404'd the
> self-hosted fonts on the live site. Use explicit exclusions, and verify against the deployed
> URL rather than against git.
