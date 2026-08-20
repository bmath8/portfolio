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

## Done 2026-08-12 - v7.1 follow-ups
- [x] **Fonts and Three.js self-hosted.** Installed via npm (@fontsource + three@0.128.0);
      16 latin-subset woff2 faces and the r128 UMD build copied into `vendor/`. Both pages
      now make **zero third-party requests** - verified in-browser with the Resource Timing
      API returning an empty external list. The "no third-party requests" line is back in
      both footers, and it is true again.
- [x] **og.png regenerated** for the new hero - 1200x630, Mission Control palette, drawn by
      `scripts/make_og.py` using the same self-hosted faces the page serves. Meta points at
      `og.png?v=7` so LinkedIn and Twitter refetch instead of serving the cached old card.
- [x] **vendor/ pruned** - 44 files deleted (meshes and .npy sources, tract lines, bloom and
      bokeh pipeline, HDR map, MarchingCubes, GSAP, ScrollTrigger, Lenis, three module build,
      old font set). 12.7 MB -> 0.8 MB. `.vercelignore` rewritten, since every rule in it
      guarded a file that no longer exists, and `vendor/README.md` added.

## Open
- [ ] **Rebuild the resume arsenal with the current numbers.** The 16 variants were built
      2026-08-05 and say 26 agents / 81 tests; the machine now reports 29 and 157. Update
      `resumes/variants/facts.py`, then `build_variants.py --all` and `render_variants.py`
      (Word COM - needs a desktop session). Then re-copy the chosen lane over
      `portfolio/resume.pdf`. Until then the deployed resume understates by 3 agents and
      76 tests.
- [ ] **Decide whether Neural stays a second page** or becomes a toggle on one page.
- [ ] **Confirm the old Tenor/Google API key is revoked, and that it is not in the public
      `boombox` history.** The key was logged against `boombox-v5`, which is not public
      (404). `boombox` **is** public and is linked from the live site. If the two share
      history the key is publicly readable. Run GitHub secret scanning or gitleaks against
      `bmath8/boombox`, and revoke the key in the Google console regardless - a key that
      was ever committed should be treated as burned.

## Verified 2026-08-12
- [x] **All three "read the source" links resolve for an anonymous visitor.** Checked
      unauthenticated: `brian-os`, `fam-super-bowl-squares-2026` and `boombox` all return
      200, and the Super Bowl Squares app is live. This matters more than it looks - the
      page's central claim is *"Everything below is code you can open"*, and that claim is
      now checked rather than assumed. The older concern that the featured case studies
      were private repos is resolved; no public-safe mirrors are needed.
      (LinkedIn returns 403 to unauthenticated requests. That is LinkedIn blocking bots,
      not a broken link - it opens normally for a human.)

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
