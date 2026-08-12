# Scene brief

**The document that must exist before any more 3D work.** Deliberately short. If it grows past
two screens it has stopped being a brief and become another layer.

Written 2026-08-11, after studying Meng To's `Kage` (three.js, open source). The lesson from
that study was **not** a tool or a framework — his stack is ours almost exactly: one static
HTML file, vendored three.js, no build step, no package manager, frame-rate-independent
damping. What he has that we lack is **a written scene concept, fixed before code**, and a
camera that carries it. We have re-skinned a hero six times without ever answering "what is the
camera looking at, and where does it go."

---

## The concept, in one sentence

**A day passing through the machine Brian built and operates.**

This is not new. It is Phase 3's concept, already approved and already half-built — the tracts
are ordered by real time-of-day and the signal travels them. What was never done is letting
that concept own **the page** instead of a box in the corner of the hero.

The subject is not a brain. The subject is **his system**, and the cortex is the body it runs
on. Every mark on screen must be traceable to something really running on his machine — that is the
one thing no other portfolio can copy, and it is worth more than any amount of atmosphere.

---

## What the camera does

One continuous path, sampled by scroll. Each chapter is a **composed shot**, not a scene swap.
Waypoints are authored by hand — position, look-at, and focal length each — and interpolated
along a spline.

| # | Chapter | The shot |
|---|---|---|
| 0 | Hero — the claim | The cortex whole, lateral three-quarter, the tuned orientation. The day begins. |
| 1 | Brian OS | Push in toward the 06:40–07:00 cluster, where twelve agents genuinely wake. The storm is the story. |
| 2 | Squares | Pull back and away — the machine recedes; this chapter is about a thing that ran in front of real people. |
| 3 | BoomBox | Low and close along the surface, tracts reading as pathways — the durable/transient split. |
| 4 | Capabilities | Rise clear of the object entirely. The light band is the exhale. |
| 5 | Contact | The whole form again, further back, quiet. The day closes. |

**Portrait screens:** waypoints are composed for a wide frame. On a tall one the rig steps back
along its own view axis and opens the focal length rather than letting the sides crop away.

---

## Palette

Settled 2026-08-11 and not reopened: **neutral form, coloured data.** The mesh carries a neutral
value ramp so it belongs to the page; the only saturated things on screen are the accent-coloured
nodes and the travelling signal. One source of truth — the CSS custom properties.

Near-black ground, bone white type, cyan / violet / amber / magenta as *data* only.

---

## Motion

- Reveal headings word by word, restrained stagger, supporting elements individually.
- The 3D has its **own clock** for the signal and the sway. Scroll drives the **camera only**.
- Frame-rate independent damping everywhere. No per-frame constants.
- `prefers-reduced-motion` renders the **final composed state immediately** — not a shortened
  animation. One settled frame, then stop scheduling frames.

---

## Non-negotiables — these are ours, and they outrank the aesthetic

These are the things a temple walk does not have to care about and we do:

1. **Every number is checkable and says where it came from.** The verification lines stay.
2. **Zero third-party requests.** Nothing loads from another origin until a visitor asks.
3. **Renders with JavaScript disabled.** The reading survives without WebGL.
4. **Nothing on the page is a claim we cannot defend.** No invented metrics, no fake proof.

A cinematic page that breaks any of these is worse than the page we have now, because the
honesty *is* the pitch. Craft is the goal; it is not a licence to trade these away.

---

## Two decisions only Brian can make

**1 · Scroll-driven camera — yes or no.** It was rejected once (*"the animations as you scroll
get worse"*). Worth reopening: what was rejected was elements sliding in on scroll, which is a
different technique from a continuous camera path down a spline. **Without this, the rest of
this brief cannot happen** — it is the mechanism the whole concept rests on.

**2 · Generated imagery — yes or no.** Kage's depth comes from compositing generated stills and
alpha cutouts in front of and behind the reading. Our footer currently advertises
**"no generated images"** as a virtue. Both are defensible; they are not compatible. If the
answer is no, depth has to come from the live scene alone, and the brief above still works.

---

## What this supersedes

- **`HERO-BRIEF.md` — SUPERSEDED.** It describes a ~14,000-point *particle* brain and "25 named
  nodes." Both are wrong now: we ship a real 39,828-vertex cortical mesh and there are 26
  agents. Its two rules ("never edit an existing candidate", "suggest the form, don't model it")
  are also both obsolete — `lab/03` proved the opposite of the second, and the mesh is modelled.
- `V6-PLAN-2026-08-05.md` stays as the record of Phases 1–5, all of which shipped.
- `BRAIN-TECHNIQUE`, `REFERENCES`, `DESIGN-REFERENCE`, `TECHNIQUE` stay as reference material.

**One brief. When it changes, it changes here — not in a new file.**
