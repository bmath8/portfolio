# Design system of record

Everything here is the *current* system. If something on the page disagrees with
this file, the page is wrong.

Rewritten 2026-08-12. The previous version documented a palette that had been
retracted, a matcap tuned for it, and nineteen ad-hoc font sizes.

## Palette — derived in OKLCH, shipped as hex

Authored with the OKLCH Color Picker method (designengineer.tools → Web Utility).
The point of OKLCH here is that its lightness is **perceptually uniform**, so a
five-step surface ramp steps by equal perceived amounts. The old ramp spanned
0.004–0.009 relative luminance across its first three steps — indistinguishable,
which is precisely what "dark background on dark everything else" meant.

Regenerate with `scratchpad/oklch.py`, which prints the hex and the full contrast
matrix. **Re-derive; do not nudge the hex.**

### Surface, rule, text

| token | hex | OKLCH | role |
|---|---|---|---|
| `--s0` | `#060709` | `oklch(13% 0.006 255)` | page |
| `--s1` | `#0f1215` | `oklch(18% 0.008 255)` | band |
| `--s2` | `#1a1d21` | `oklch(23% 0.009 255)` | panel |
| `--s3` | `#282c31` | `oklch(29% 0.011 255)` | raised / hover |
| `--s4` | `#393e44` | `oklch(36% 0.013 255)` | chip, minor grid rails |
| `--rule` | `#4d535b` | `oklch(44% 0.016 255)` | the one border colour |
| `--rule-q` | `#212429` | `oklch(26% 0.010 255)` | quiet divider |
| `--bracket` | `#757e89` | `oklch(59% 0.020 255)` | L-corner marks |
| `--tx0` | `#f4f5f7` | `oklch(97% 0.003 255)` | primary text |
| `--tx1` | `#c3c8ce` | `oklch(83% 0.011 255)` | body |
| `--tx2` | `#959ca5` | `oklch(73% 0.015 255)` | meta |

Measured contrast, every text token against every surface:

| | s0 | s1 | s2 | s3 | s4 |
|---|---|---|---|---|---|
| `--tx0` | 18.47 | 17.22 | 15.50 | 12.88 | 9.89 |
| `--tx1` | 11.97 | 11.16 | 10.05 | 8.34 | 6.41 |
| `--tx2` | 8.42 | 7.85 | 7.07 | 5.87 | **4.51** |

Worst pair is `--tx2` on `--s4` at 4.51 — over the 4.5 body threshold. Any new
token has to be re-run through the matrix before it ships.

### Data — the only hues in the document

Each means exactly one thing: a cron schedule class. **Nothing in the UI may use
them.** They share one lightness and one chroma and differ only in hue, which is
the whole reason to author in OKLCH — in HSL a yellow and a blue at the same
"lightness" are nowhere near equally bright.

| token | hex | OKLCH | vs `--s1` |
|---|---|---|---|
| `--d-daily` | `#62d09f` | `oklch(78% 0.125 162)` | 9.88 |
| `--d-hourly` | `#a5afff` | `oklch(78% 0.125 278)` | 9.10 |
| `--d-weekly` | `#e5ac53` | `oklch(78% 0.125 76)` | 9.27 |
| `--d-monthly` | `#fc95a2` | `oklch(78% 0.125 12)` | 8.91 |

8.91–9.88 across all four: equally loud, none shouting. A legend under the hero
metric strip names all four, because colour that encodes data and does not say so
reads as decoration — and was correctly called out as looking random.

## Motion

Named curves (Easing Functions, designengineer.tools → Web Utility). No bare
durations.

| token | curve | use |
|---|---|---|
| `--e-out` | `cubic-bezier(.22,1,.36,1)` | entrances, opacity reveals |
| `--e-in-out` | `cubic-bezier(.65,0,.35,1)` | reversible state |
| `--e-quick` | `cubic-bezier(.25,.46,.45,.94)` | hover, focus, small UI |

Everything animated sits inside a `prefers-reduced-motion` guard, and the guard
is verified by byte-comparing screenshots — not by reading the CSS.

## Type — seven steps, named

`--t-display` `clamp(38px,5.2vw,68px)` · `--t-h2` `clamp(24px,2.7vw,34px)` ·
`--t-h3` 22 · `--t-lead` 17 · `--t-body` 15 · `--t-meta` 13 · `--t-micro` 11.5

Bricolage Grotesque 800 for headings, IBM Plex Sans for body, IBM Plex Mono for
anything that is a figure, a path, a cron line or a label. All self-hosted.

## Structure

From the vendored MIT skills, not invented:

| skill | contribution |
|---|---|
| `framed-grid-layout` | bounded sections, one border colour, L-corner brackets |
| `container-lines` | thin container guides so the page has a visible measure |
| `number-details` | 01 / 02 / 03 section markers |
| `corner-diagonals` | chamfers via `clip-path`, replacing uniform border-radius |
| `technical-wireframe-info-layout` | annotations routed to what they describe |
| `background-grid-webgl` | the hero: perspective ground plane, fog falloff, drift, damped parallax |

## Rules that keep getting broken

1. **Colour is data.** Four hues, one meaning each, legend on the page. If a UI
   element needs emphasis it gets brightness, weight or position — not a hue.
2. **Re-derive the ramp, don't nudge the hex.** Every hand-tweak has taken it
   back toward arbitrary.
3. **Measure, don't look.** Contrast from computed styles, reduced motion from
   byte-identical screenshots, no-JS from a real `java_script_enabled=False`
   load. Three of the last five real defects were invisible to the eye.
4. **A number on the page is counted, not typed** wherever it can be. "Twelve
   agents fire between 06:40 and 07:00" survived several versions and was false;
   the true figure is ten.
