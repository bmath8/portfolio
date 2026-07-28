# Demo Tier — Design Spec
**Date:** 2026-07-23 · **Owner:** Brian Mathew (`bmath8`) · **Status:** awaiting review

## Problem

Brian needs live demos he can put on a resume. Four demos were built (07-22 session) and
recorded as "LIVE — public, recruiter-ready." **Verified 07-23: none of them let a recruiter
see the product.**

### Verified findings (browser-tested, not assumed)

| Project | URL in inventory | Reality |
|---|---|---|
| BoomBox | `boom-box-v-5-git-main-…vercel.app` | **Redirects to Vercel login.** Protected preview alias. |
| Warranty Tracker | `warranty-tracker-isv8cgwec-…vercel.app` | **Redirects to Vercel login.** Protected preview alias. |
| Super Bowl Squares | `fam-super-bowl-squares-2026-4gjaeglh2-…` | Loads, but gated on name + room code. |
| Pokemon Drop Intel | `pokemon-drop-intel-nni77pvnj-…` | **HTTP 401.** Invisible. |

The inventory recorded **deployment-hash aliases**, which Vercel protects by default. The
canonical production URLs are different and mostly work:

- `boom-box-v-5.vercel.app` — loads (login wall)
- `warranty-tracker-azure.vercel.app` — loads, fully open, **but empty**
- `fam-super-bowl-squares-2026.vercel.app` — loads (room-code gate)
- `pokemon-drop-intel.vercel.app` — **401 even on production**
- `bmath8.vercel.app` — portfolio

**Had the inventory URLs reached a resume, every recruiter would have hit a Vercel auth wall.**

### Design assessment (visual, via screenshots)

- **BoomBox — good, do not redesign.** Skeuomorphic boombox: speaker cones, EQ spectrum,
  cassette reels, orange glow. Distinctive and committed. Its problem is the login wall.
- **Super Bowl Squares — competent.** Dark stadium palette, team logos, gold CTA. Excess
  dead space; no redesign needed.
- **Warranty Tracker — AI slop, needs full rebuild.** Generic indigo-navy gradient,
  purple-gradient button, four identical stat cards, default system font, rounded-rect
  everything. Violates the standing no-slop rule directly. Worse: **loads showing
  `0 · 0 · 0 · 0`** — reads as broken.
- **Pokemon Drop Intel** — could not assess; 401.

## Goal

One link a recruiter clicks that, in under 30 seconds, proves the project is real and works —
**without** exposing the full application or the source.

## Non-goals (explicitly out of scope)

- Rebuilding BoomBox's or Squares' visual design. They are good enough; effort goes elsewhere.
- Making the demos publicly discoverable / SEO-indexed.
- Shipping new product features. This is about access, first impression, and one redesign.
- Resume and cover letters — a separate project, sequenced after this.
- Fleet audit #7 — six already exist (06-17 → 07-11). Deferred; scoped to income-blockers later.
- Giveaway app — deliberately excluded (bot-automation angle is a resume liability).

## Decisions

| # | Decision | Status |
|---|---|---|
| D1 | Access via **unlisted URL + `noindex`**, not a code gate | Default — Brian may override |
| D2 | Make **`credit-repair-os` public**; other four stay private | **NEEDS EXPLICIT OK** — outward-facing, not auto-applied |
| D3 | Warranty Tracker gets a **full visual rebuild** | Approved 07-23 |
| D4 | BoomBox + Squares designs **kept as-is** | Approved 07-23 |
| D5 | Add Credit Repair OS + CreditForge as demos 5 and 6 | Approved 07-23 |

D1 rationale: a gate that fails (Pokemon's 401 today) looks like incompetence. Obscurity gives
most of the privacy benefit at none of the friction cost.

D2 rationale: all five repos are private. Hiring managers ask for code. One clean public repo
with green CI answers that; the rest stay closed. **Publishing a repo is irreversible in
practice — will not be done without a separate explicit go-ahead.**

## Architecture — the four properties

Every demo implements the same four. This is what makes six apps read as one portfolio.

1. **Lands populated.** Seeded realistic data at load. No empty states, no "click to load
   sample data," ever. (Fixes Warranty Tracker's zero-dashboard.)
2. **Sandboxed writes.** Visitors can add/edit/filter; writes go to a per-session sandbox that
   resets. No visitor can corrupt state for the next one.
3. **Bounded surface.** Only capability-demonstrating flows. Settings, billing, integrations,
   admin, and anything touching real credentials or personal data are hidden — not merely
   disabled — in demo mode.
4. **Shared demo chrome.** One persistent bar across all six: what this is, what's limited,
   who built it, contact link. Built once, reused. Converts "a random app" into "a portfolio
   piece" and puts contact at peak interest.

   *Implementation note:* the six demos span four stacks (Next.js, static HTML + React UMD,
   Vite/React, Python/FastAPI). A shared React component will not work across all of them.
   The chrome ships as a **single self-contained `demo-bar.js` + CSS** served from the
   portfolio origin and included with one `<script>` tag per app. No build-step coupling, no
   framework dependency, one file to restyle all six. Design tokens inline in that file.

## Per-project scope

| Project | Work | Effort |
|---|---|---|
| Pokemon Drop Intel | Unblock 401; seed sample drops | S |
| Warranty Tracker | Full visual rebuild + seeded load | L |
| BoomBox | Demo entry past login; seed content | M |
| Super Bowl Squares | Bypass room gate into finished game; tighten dead space | S |
| Credit Repair OS | Deploy (Render/Fly — Dockerized); optional public repo | M |
| CreditForge | Vercel deploy + seeded Supabase + demo login | M |
| Portfolio `index.html` | Wire in real demo links (currently has **zero**) + LinkedIn | S |

## Sequence

1. **Fix URLs + unblock Pokemon** — stops actively-broken links. ~1 hour.
2. **Demo-tier infrastructure** — shared chrome + seeding pattern, built once.
3. **Warranty Tracker rebuild** — the real design work.
4. **Credit Repair OS + CreditForge** deploys — adds Python/FastAPI range.
5. **Portfolio wiring** — demo links into `index.html`.

After step 1, nothing on the resume is broken.

## Acceptance criteria

Each is verifiable by a command or a browser check. No claim of completion without evidence.

- **AC1** Each of the six demo URLs returns HTTP 200 in a clean browser profile with no
  Vercel/SSO redirect. Verified by navigation, not assumption.
- **AC2** Each demo renders **non-empty, realistic content within 3 seconds of first load**,
  with no user interaction required.
- **AC3** No demo requires typing a credential, code, or name to reach the product.
- **AC4** Every demo shows the shared demo chrome with a working contact link.
- **AC5** In demo mode, no route exposes settings/billing/admin/integrations or any real
  personal data. Verified by walking every nav item.
- **AC6** Sandbox reset works: mutate state, reload in a fresh session, original seed returns.
- **AC7** `robots.txt` / meta `noindex` present on all six; confirmed not indexed.
- **AC8** `portfolio/index.html` links all six live demos plus LinkedIn. (Today: zero demo links.)
- **AC9** Every URL recorded in `MASTER_PROJECT_INVENTORY.md` matches a verified-200 production
  alias — no deployment-hash URLs anywhere.
- **AC10** Warranty Tracker rebuild uses no generic gradient, no Inter/Roboto/system-default
  stack, and no centered-hero-with-stat-cards layout.

## Risks

| Risk | Mitigation |
|---|---|
| Deployment Protection re-enables on new Vercel projects | Verify AC1 after every deploy, not once |
| Seeded demo data leaks real personal data | Seed from synthetic fixtures only; AC5 walk |
| Warranty rebuild slips and blocks the resume | It is step 3; steps 1–2 already unblock the resume |
| Supabase free-tier projects auto-pause after 90 days idle | Known: two projects already died this way. Note revival steps in each README |
| Public repo exposes secrets | Secret-scan before D2; repos were hardened 07-22 but re-verify |

## Open items requiring Brian

- **D2 go-ahead** — make `credit-repair-os` public? (irreversible; not auto-applied)
- Confirm D1 (unlisted) vs keeping a resume-code gate.
- LinkedIn URL — required by `PROJECT_BRIEF.md`'s definition of done, still missing.

## Provenance

Supersedes the demo-status claims in `MASTER_PROJECT_INVENTORY.md` (07-22), which recorded
protected preview aliases as public URLs. That file must be corrected as part of AC9.
