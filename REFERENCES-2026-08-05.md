# Reference library — 2026-08-05

**Purpose: clear Gate 1.** Thirty-four candidates have been rejected, and not one started
from a reference Tom picked. Every one started from the model's own priors trimmed by an
avoid-list, which is why they converged. This file exists so the next one starts from
something he chose.

**How to use it:** open the ten links in Group A, spend two minutes each, and name one or
two you like — or one you hate and why. That single input is worth more than another
research pass. Non-portfolio references are *better*, because they can't be pattern-matched
to "portfolio site."

Everything below was fetched and read on 2026-08-05 unless marked otherwise.

---

## GROUP A — the ten to actually look at

| # | URL | Why this one is here |
|---|---|---|
| 1 | **wc26.bogachev.fr** | **The thesis reference.** Every match is rebuilt from ~1,500 real recorded events and rendered as a generative "portrait." Their own line: *"It's an impression, but one built entirely from data."* This is the proof that an object *derived from real telemetry* reads as credible instead of decorative. Your 26 agents and their run history are your 1,500 events. |
| 2 | **everest.suraj.work** | **The architecture reference.** Canvas terrain behind, all editorial text in DOM in front, text recolours to stay readable, user-facing quality sliders, off-screen work suspended, explicit desktop-only gate with a text fallback. Its hero opens with a live metric strip (altitude / oxygen / temp / day). Swap in agents running / tests passing / last run and that is your hero. Solo-built. |
| 3 | **monome.org** | **Tone and imagery.** One colour, documentary photographs of real machines, a photo of the actual barn, prose in a plain maker register. This is the answer to "no AI images" — nobody can prompt a photograph of the machine your agents actually run on. |
| 4 | **teenage.engineering** | **Density.** Rigid modular grid, ~two colours, high information density that reads as competence rather than clutter. The structural opposite of the airy centered-hero slop pattern — no cards, no 16px radius, no glass. |
| 5 | **lusion.co** + **labs.lusion.co** | **The quarantine strategy.** The best 3D studio on the web keeps its own homepage restrained and puts the wild work on a separate `labs` subdomain. You could do exactly this: main site loads in under 2s, `/lab` carries the unrestrained version with no load budget. Max ambition without paying for it at the front door. |
| 6 | **cerebrium.ai** | **Numbers as headlines.** Real comparative figures as section heads — *3.8s cold start vs 42–156s*. Not adjectives. "81 passing tests" only lands if framed this way. Their expensive-looking hero is a hold-to-play video, not a live scene. |
| 7 | **blumjeffrey.com** | **Positioning.** *"Shape Vision. Build Systems"* with a credentials triplet right under the hero (25+ years / 80+ launches / ∞). Closest match found to your actual pitch, done with real photography and zero dashboard costume. |
| 8 | **jhey.dev** | **Proof-of-life, cheap tier.** Live weather, real Steam, real Spotify in the footer. Same *category* of move as the living brain — machine-verified facts about a real person — at 5% of the cost. Worth building as insurance: if the 3D degrades, this still proves the system is real. `henry.codes` does it with live location + temperature. |
| 9 | **artemartemartem.com** | **Load discipline.** Awwwards SOTD *and* Developer Award (2026-07-25) — and the hero motion is animated GIFs over a DOM-text page, from someone who does CG professionally. |
| 10 | **leerob.com** (pair with **rauno.me**) | **The 15-second stopwatch.** Name, one sentence, then evidence. The test: strip the 3D — does the remaining page read as fast as this? If not, the 3D is carrying weight it shouldn't. |

---

## The finding that most changes the plan

**2026 Developer Awards are not going to polygon count.** Five independent confirmations:

- `artemartemartem.com` — SOTD + Developer Award, hero is **GIFs**, DOM text
- `trionn.com` — SOTD + Developer Award, **no WebGL evident**
- `shader.se` — Developer Award. A studio *named Shader* ships a **text-first homepage**
- `basement.studio` — "3D & Motion Design" is listed as a **service**, not used on the page
- `dogstudio.co` — award-tier studio, DOM text + an embedded Vimeo instead of a WebGL hero

And `gionatannese.com` appears on the Awwwards **Portfolio and Three.js** lists while keeping
its homepage DOM-text and putting the WebGL one click deep.

**The under-2s constraint is not a compromise. It is where the awards actually are.**
That resolves the tension this project has been stuck on: you do not have to choose between
maximum 3D and a fast, readable page. The pattern that wins is *3D as a gated, degradable
layer behind DOM text* — everest.suraj.work is the worked example.

---

## Two corrections to things previously believed

**GitHub's live pull-request globe is gone.** Fetched today: the homepage is now text-first
(*"The future of building happens together"*). The most-cited "living 3D system as a hero"
precedent was retired by its own owner. Don't build the argument on it.

**The cream-and-charcoal palette is a documented award cliché, not just a slop tell.**
`louiscuenot.com` took an Awwwards Honorable Mention in Jan 2026 running `#F4F3EC` + `#221F21`
— within one hex digit of the `#F4F1EA` already rejected here. Evidence for the rejection,
not against it.

---

## Anti-references — confirmed dead ends

- **bruno-simon.com** — the ambition *ceiling*, not the target. Verified: the DOM is a bare
  canvas. At 15 seconds it has communicated nothing hireable. It works because the site *is*
  the portfolio piece. Yours isn't.
- **activetheory.net · resn.co.nz · unfor-dev.vercel.app** — all returned near-empty to a
  fetch. Elite work, architecturally invisible to any crawler or automated screen sitting
  between you and a human. **The emptiness is the finding.**
- **robinpayot.com** — an "Enter" gate costs a click before any claim lands. Fatal here.
- **cassie.codes** — no longer a portfolio. It is now a farewell page. Archive only.
- **loganliffick.com · kommakomma.is** — both ship devices already on the rejected register
  (hairline-rule dividers; numbered `01–05` sections). Included to confirm the rejection.

---

## Three techniques worth stealing

1. **Z-axis depth scroll** (`oryzo.ai`, by Lusion) — the camera moves through *true depth*;
   one hero object with real weight and inertia. A brain with mass and momentum approached
   in Z is structurally different from parallax.
2. **WebGPU renderer with WebGL fallback via TSL** (`brand.ivress.co.jp`) — one shader source
   compiles to both backends without forked code. The fallback path protects the load budget.
3. **Honest numeric loader** (`jordan-breton.com`) — a visible `0% · Initializing…` against
   real asset counts. Never a fake spinner: a site about a real system cannot fake its own
   loading state.

---

## Galleries that worked, and the ones that block

**Worked:** Awwwards (Portfolio / Three.js / Developer Award), SiteInspire, Minimal Gallery,
personalsit.es (~1,099 sites), Utsubo's Three.js 2026 round-up, CreativeDevJobs.

**403 / blocked to fetching — open these in a browser:** Land-book, Lapa Ninja, Bestfolios,
`mitchivin.com`, `shees.dev`.

**Moved:** Godly now 301-redirects to `recent.design`. Update the bookmark.

**Codrops** carries no outbound links on its Collective index — they live inside each
newsletter issue and in `tympanus.net/codrops/webzibition/`.

A long appendix of ~180 further URLs harvested from those galleries was gathered this
session; ask and it can be written out in full.
