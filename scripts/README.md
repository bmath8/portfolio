# scripts/

Two kinds of thing live here, and the distinction matters.

## Reusable tools — run these whenever you need them

| Script | What it does |
|---|---|
| `make_og.py` | Regenerates `og.png` (1200×630, Mission Control palette). Run after any change to the headline or the four metrics. |
| `make_og_neural.py` | Regenerates `og-neural.png` for the Neural edition. |
| `verify-demos.ps1` | Checks the live demo links still resolve. |
| `build_ttf.py` | Converts the self-hosted woff2 faces to TTF so Pillow can draw with them. Run this first if either OG script complains. |

Both OG scripts draw with the exact faces the site serves. Pillow cannot read woff2, so
they use TTF copies built from `vendor/fonts/`:

```bash
pip install pillow fonttools brotli
python scripts/build_ttf.py                      # woff2 -> scratchpad/vendorbuild/ttf
python scripts/make_og.py vendor/fonts og.png    # Mission Control card
python scripts/make_og_neural.py                 # Neural card
```

The TTF copies are build artifacts and are not deployed. `make_og.py` looks for them in
`scratchpad/vendorbuild/ttf/` and falls back to `vendor/fonts/_ttf/`; if neither exists it
tells you to run `build_ttf.py` rather than failing with a Pillow error.

## `applied/` — historical record, do not re-run

Everything in `applied/` is a **one-shot migration that has already been applied to
`index.html` and `neural.html`.** The results are committed in those two files. Running one
again will either do nothing (most are guarded) or corrupt the markup by inserting a second
copy of a block.

They are kept because each one documents *why* a change was made, in a way a diff does not.
The v7.2–v7.4 arc in particular was a sequence of measured fixes, and the reasoning lives in
these headers — the brain's `aria-hidden` conflict, the reveal animation putting invisible
links in the tab order, the count-up that could strand a metric on `0`, the full-bleed
padding that clipped the first numeral.

If you want to know why something is the way it is, read the docstring at the top of the
relevant script, then `docs/CHANGELOG-v7.md`.

### Rough order they were applied

```
tier1_a11y.py  fix_main.py  sr_alt.py  fix_countup.py     v7.2 correctness + a11y
tier2_mc.py  tier2_neural.py  tier2_log.py                v7.2 composition
fix_radar_perf.py  fix_neural_wrap.py
tier3_mc.py  tier3_neural.py  tier3_shared.py             v7.2 craft features
tier3_lazy_three.py                                       three.js off the critical path
mobile_polish.py                                          phone layout
a11y_round2.py                                            v7.3 the seven failures
content_round2.py  move_incident.py  incident_width.py    v7.3 content
add_analytics.py  fix_cleanurls.py  update_availability.py
design_mc.py  fix_design_mc.py                            v7.4 design pass
design_neural.py  fix_design_nu.py
```

A `fix_*` script always follows the pass it corrects — those are the mistakes caught in
verification, kept deliberately rather than squashed, because the correction is often the
more interesting half of the story.
