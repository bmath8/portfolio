# Design Reference — studied, not guessed

Written 2026-08-04 after actually reading primary sources instead of search summaries.
**Read this before writing any hero code.** Four candidates were built without it and all
four were window dressing.

---

## The gold standard: Lusion (lusion.co)

Bristol studio, founded 2017 by **Edan Kwan** — originally a musician from Hong Kong who
**taught himself design and coding**, freelanced, worked at a NY agency, went independent.
Site of the Year at FWA, Awwwards *and* CSSDA. Clients: Coca-Cola, Porsche, Max Mara,
Google. Cannes Lions, D&AD, Webby.

### What they actually say about how they work
> *"We like building things from scratch. Not because it sounds nice on a case study, but
> because **the best ideas usually fall apart the moment you force them into a template**.
> So every project gets its own system, its own logic, and its own flavour."*

> *"Some of our work is polished and cinematic. **Some of it is weird on purpose.**"*

### THE LESSON I KEPT MISSING

**Lusion's work has a CONCEPT, not a STYLE.** Look at what they actually make:

| Project | The concept |
|---|---|
| **Oryzo AI** | A satirical launch campaign for a fictional AI product — a cork coaster — played completely straight with premium production. A joke executed with total craft. |
| **My Little Storybook** | A bird family crossing a river. Anime-inspired, hand-built 3D, drawn animation. A *story*, made in one month. |
| **Porsche: Dream Machine** | A CG short film about Ferry Porsche's dream, moving from abstraction to the silhouette of the 356. |
| **Choo Choo World** | A game. |

None of these are "a cool 3D object with effects on it." Every one is **an idea you can
say in a sentence**, executed with obsessive craft.

**All four of my candidates were "a brain, because brain = thinking."** That is a
decoration, not a concept. Swapping fonts and palettes on a decoration produces exactly
what Brian called it: window dressing masquerading as a redesign. The regression wasn't
the typography. It was that there was never an idea underneath.

### How they iterate — and how I got that wrong too
> *"Lusion Labs… our **monthly experiment series**, where we created small internal projects
> that allowed us to **test ideas quickly**."*

They iterate on **small standalone experiments**, then graduate the winners.
I rebuilt the **entire page** four times. That is why each version regressed in some
dimension while fixing another — too many variables moving at once.

**Correct process:** build 5–10 tiny single-purpose demos (one interaction each, ~80 lines,
no page around them). Judge them. Take the one that works and build the page around it.

---

## Technique sources worth reading properly (not summarising)

- **Codrops — Lusion studio spotlight** (Apr 2026) — the source of everything above.
  <https://tympanus.net/codrops/2026/04/13/lusion-where-digital-craft-meets-ambitious-experimentation/>
- **Codrops — replicating Lusion's curly tubes with light scattering in Three.js.**
  A direct, documented teardown of an actual Lusion effect. **Start here for technique.**
- **Codrops — "Coding a Simple Raymarching Scene with Three.js"** and **"Liquid Raymarching
  with Three.js Shading Language"** (2024). Raymarched SDFs are how you get liquid /
  metaball / volumetric forms that particles cannot do.
- **Maxime Heckel — "Real-time dreamy Cloudscapes with Volumetric Raymarching."**
  Best single write-up on volumetric rendering on the web.
- **Codrops — "WebGL Shader Techniques for Dynamic Image Transitions"** — circle SDFs,
  noise, smooth merging. This is the vocabulary for *transitions*, which Brian specifically
  called out as weak.
- **Three.js Journey Lesson 41** — GPGPU flow-field particles, the canonical implementation.
- **labs.lusion.co** — opened in a real browser 2026-08-04. **Result: pure `<canvas>`.**
  `get_page_text` returns nothing; the accessibility tree exposes only social links, an
  email field and a newsletter box. There is no DOM to learn from — the entire experience
  is drawn. That is itself the finding: at this tier the page *is* the render target, not
  a document with effects layered on. Studying it further requires screenshots/video, not
  text extraction.

## TYPOGRAPHY — what top portfolios ACTUALLY use (hard data, 2026-08-04)

Pulled from **maxibestof.one/websites/portfolio** via browser — a curated gallery that
records the real font stack of every site it features. This is measured, not guessed.
Corpus: 1.2k sans / 480 serif / 155 mono across the gallery.

**Most-used across the featured portfolios (by repeat appearances):**

| Font | Seen on | Type |
|---|---|---|
| **Suisse Int'l** / Suisse Neue / Suisse Int'l Mono | Fiona Yumi Kayayan, Pena Design, Satoshi Watanabe, Clémence Guillemot, Ravi Klaassens | Swiss neo-grotesque — **the single most-used face in this corpus** |
| **Monument Grotesk** / Monument Grotesk Mono | Ervin Latimer, Bas Strien, Extreme Present | grotesque + its mono companion |
| **ABC Diatype** | Postnew, Viacheslav Novoseltsev | contemporary grotesque |
| **ABC Arizona / Arizona Flare** | Jack Mcentee, Jules Andrieu | serif with real character |
| **PP Neue Montreal** | Alexandre Araujo | |
| **Neue Haas Grotesk** (+ Display) | Krabb | |
| **Instrument Serif** | Northzone | ← the one I used in v4. It *is* current. |
| **LL Replica · Reckless Neue** | Ravi Klaassens | |
| Fraktion Mono · SF Mono · Roboto Mono | Nicolas Alain, Eugene Serpokrylov, Postnew | mono as an accent voice |
| GT Canon · Louize · TWK Lausanne · Greed · General Sans · Aktiv Grotesk · Mercure · Animo | various | |

**Two things this data contradicts:**
1. The `frontend-design` skill says *never* use Inter/Arial. In practice **Konolee, Will
   Phan (Inter) and Jordan Robson (Arial)** are all in a curated best-of gallery. The real
   rule is not "avoid these fonts" — it is *"don't use them as a default because you didn't
   choose."* A deliberate Arial portfolio is fine; an accidental system-font one is not.
2. **Pairing pattern is consistent:** one grotesque for structure + one mono for data +
   optionally one serif for voice. That is the actual convention, and v4's serif-heavy
   approach was off-pattern.

**Concrete recommendation for Brian's site:** Suisse Int'l is the corpus favourite but is
commercial. Free equivalents with the same energy: **Inter Display** (used by Artem
Astakhov alongside Instrument Sans), **General Sans**, or **Aktiv Grotesk**. Pair with a
mono for all the measurements (25 agents, 81/81, cron times) — that half of v4 was right.

**Gallery is worth revisiting** — it filters by font and has an MCP server of its own
(`maxibestof.one` → MCP). Worth wiring up.

## Other studios to study (named by 2026 round-ups, not yet opened)
- **Active Theory** — advanced motion, immersive environments, technical storytelling;
  cited for proving performance and spectacle can coexist.
- **Resn** — experimental interaction, surreal visuals; study for **creative risk-taking**.
- **Immersive Garden** — elegance + technical polish; project pages give real context on
  the creative challenge.
- **Unseen Studio** — Hubtown, Awwwards SOTD June 2026 (glowing 3D monolith over a dark
  reflective landscape).
- **Vide Infra** — "Springs", SOTD + Developer Award, March 2026.
- **OFF+BRAND** — Steven.com, SOTD + Developer Award, June 2026.
- **Locomotive**, **Femme Fatale Studio** — also named.

## Awwwards signal (Q1 2026)
- **29 of 47** Site-of-the-Day winners used Three.js.
- Winners *"pick one hard idea and execute it cleanly rather than stacking effects"* —
  a drivable physics world, audio-reactive fluid, one object with real weight.
- Recent SOTD: Vide Infra "Springs", OFF+BRAND "Steven.com", Unseen Studio's Hubtown
  (glowing 3D monolith over a dark reflective landscape).

## Counter-signal — do not ignore this
Hiring-side research says heavy animation reads as **gimmicky**, mobile experience matters
enormously, and case studies beat effects. Brian is applying to **IT support / junior dev
roles**. A hiring manager at ProCat is not an Awwwards juror. The resolution is not "less
craft" — it is that **the craft must carry meaning about him**, so it reads as evidence
rather than decoration.

---

## What a real v5 process looks like

1. **Find the concept first.** One sentence, about Brian, that isn't "he thinks." Candidates
   worth exploring: *the machine that runs while he sleeps* (25 agents, real crontab, a
   night that passes); *the incident* (the disk filled, he traced it, he fixed it — a
   story with tension and resolution); *everything here is checkable* (the whole site as a
   verification instrument).
2. **Study one technique properly** from the list above. Read the actual tutorial. Build
   the tutorial's example first.
3. **Build 5–10 tiny experiments**, one interaction each, in `design-candidates/lab/`.
   No page. No content. Just the interaction.
4. **Judge the experiments with Brian.** Pick one.
5. **Then** build the page around the winner.

## Rules learned the hard way in this session
- Never edit an existing candidate — new file, always. (26 layered candidates → mush.)
- Never change more than one variable per iteration.
- Additive blending + bloom clips to white where particles overlap. Cap alpha ~0.30.
- Anatomical accuracy is the wrong goal; a cortex is visually noisy and reads as mush.
- A theme swap is not a redesign.
- **If you can't say the concept in one sentence, don't open an editor.**
