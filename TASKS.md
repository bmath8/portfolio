# Active Tasks

## Current task
Portfolio supports the job search — it is not the resume source. Keep it accurate and public-safe.

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

## Done 2026-08-10 (verified this session)
- [x] **Public-safe showcase mirrors — SHIPPED.** `bmath8/brian-os` and `bmath8/boombox` are
      public. Every case-study link on the live site resolves to public source.
- [x] **Positioning call — RESOLVED developer-forward.** Both artifacts already moved: the site
      leads "I build systems, then I keep them running" with three engineering case studies, and
      `resume.pdf` is the AI/Full-Stack Developer lane, not Customer Ops. This item was stale.
- [x] **Tenor key is not publicly exposed.** Scanned every blob in the public `boombox` mirror's
      history: no hits. The mirror has fresh history (2 commits) and reads the key from
      `process.env['NEXT_PUBLIC_TENOR_API_KEY']`. See the still-open rotation item below.

## Open — needs Brian
- [ ] 🚩 **BLOCKING BEFORE SENDING: `resume.pdf` says "25 scheduled agents." The verified count
      is 26.** `agents.json` lists 26, `hermes cron list` returned 26 on 2026-08-05, and the live
      site says 26 in four places. The resume is the one artifact still carrying the old number,
      and it is the one that goes to employers. Fix upstream — correct
      `C:\Brian\03_Career\evidence-bank.md`, re-run `build_strong_resumes.py` + `render_pdfs.py`,
      then re-copy the built PDF over `resume.pdf` here. **Do not hand-edit the PDF.**
- [ ] **Rotate the leaked Tenor/Google API key.** No longer urgent — it is not in any public repo
      (verified above) — but it is still in the private `BoomBox-V.5` git history. Rotate it.
- [ ] **`ai-job-hunter` has no public mirror** and is the lead bullet on `resume.pdf`. Either
      mirror it the way `brian-os` and `boombox` were done, or accept that the resume's strongest
      project is unopenable. Its 2026-07-29 secret scan came back clean, so a mirror is low-risk.
- [ ] Real screenshots in each featured repo (`docs/screenshot.png`) — only Brian can take these.
- [ ] Optional 4th case study: `pokemon-drop-intel` (already public, has a demo mode).

## Secret scan result — 2026-07-29 (full git history, all commits)
- `ai-job-hunter` — **clean** (29 commits; only `.env.example`).
- `brian-os-fleet` — **clean** (119 commits; the two "hits" are `tests/test_guardrails.py`
  fixtures: AWS's own `AKIAIOSFODNN7EXAMPLE` doc placeholder and an obvious dummy key).
- `boombox-v5` — **one real finding**, the Tenor key above. `SUPABASE_SERVICE_ROLE_KEY`
  matches are variable *names*, not values — harmless.
