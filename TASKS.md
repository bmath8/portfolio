# Active Tasks

## Current task
Portfolio supports the job search — it is not the resume source. Keep it accurate and public-safe.

## Done 2026-08-12 — v7 dual-design rebuild
- [x] **Full top-to-bottom redesign shipped.** Two complete designs now live in the repo:
      Mission Control at `/` (`index.html`) and Neural at `/neural.html`. Previous homepage
      archived to `design-candidates/archive/v6-brain-hero.html`.
- [x] **Fixed the v6 problems** that made the old page feel wrong: scroll-jacked hero,
      multi-viewport dead zones between sections, a duplicated header and white-bar artifact,
      metrics stranded below the fold, and a 3D brain that outcompeted the headline.
- [x] **Metrics moved into the first screen** on both pages, with count-up and a source line
      under every number.
- [x] **Live demos beside every project.** Squares loads the real deployed app on click;
      Brian OS and BoomBox have purpose-built visualisations.
- [x] **Docs rewritten** — new `README.md`, `docs/DESIGN-SYSTEM.md`, `docs/CHANGELOG-v7.md`,
      `docs/AUDIT-2026-08-12.md`.

## Open — follow-ups from v7
- [ ] **Self-host the fonts** (and Three.js) to restore the old "no third-party requests"
      property. Both new pages currently pull Google Fonts, and `neural.html` pulls Three.js
      r128 from cdnjs. `vendor/` already holds self-hosted faces from the v6 build.
- [ ] **Refresh og.png** — it still advertises the v6 hero.
- [ ] **Decide whether Neural stays a second page** or becomes a toggle on one page.

## Done 2026-07-29
- [x] **LinkedIn added** to the site (hero + contact). It was never actually blocked — the
      handle had been sitting in `03_Career/evidence-bank.md` since 2026-07-24 while this file
      said "waiting on Brian." Unblocked, closed.
- [x] **Resume source unified.** `resume.pdf` is now a copy of canonical
      `Brian_Mathew_Customer_Ops.pdf`. The separate `resume/resume.html` is superseded (kept).
- [x] **Removed an unverifiable claim** from the live site: Best Buy "ranked first in the
      territory for sales." Best Buy and the Department Lead title are confirmed true and stay;
      the performance metric is not defensible and is gone.
- [x] **Fixed education framing** — "ADDITIONAL EDUCATION / additional undergraduate study"
      implied a completed primary degree. Now plainly "undergraduate coursework."
- [x] **Corrected INVENTORY.md** — the "21 repos backing up the claim" line was false; there
      are 27 repos and only 4 are public.

## Open — needs Brian
- [ ] **Public-safe showcase mirrors.** All 3 featured case studies are private repos, so the
      resume points at work nobody can open. Plan approved: clean mirrors with fresh history.
      Secret scan is done (see below). Awaiting per-repo go-ahead.
- [ ] **Revoke the leaked Tenor/Google API key** — it was hardcoded in
      `boombox-v5 frontend/src/components/gif-picker.tsx` and remains in that repo's git
      history (already gone from HEAD). Rotate it regardless of what goes public.
- [ ] **Positioning call.** The site sells "product/IT/customer support," but the strongest
      lane is AI Builder (96%) and the three case studies are engineering projects. Decide
      whether to re-aim the site developer-forward. `resume.pdf` currently matches the existing
      support framing.
- [ ] Real screenshots in each featured repo (`docs/screenshot.png`) — only Brian can take these.
- [ ] Optional 4th case study: `pokemon-drop-intel` (already public, has a demo mode).

## Secret scan result — 2026-07-29 (full git history, all commits)
- `ai-job-hunter` — **clean** (29 commits; only `.env.example`).
- `brian-os-fleet` — **clean** (119 commits; the two "hits" are `tests/test_guardrails.py`
  fixtures: AWS's own `AKIAIOSFODNN7EXAMPLE` doc placeholder and an obvious dummy key).
- `boombox-v5` — **one real finding**, the Tenor key above. `SUPABASE_SERVICE_ROLE_KEY`
  matches are variable *names*, not values — harmless.
