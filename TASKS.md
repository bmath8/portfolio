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

## AGPL mesh — the working tree is clean; the history is not

**2026-08-12, the design change that closed most of this:** the page no longer
uses a 3-D model at all. The hero object is generated from the cron lines in
`agents.json`. `vendor/mesh/` was deleted outright — `brain-icbm152.bin`,
`brain-icbm152-v2.bin` and its README — along with `vendor/lines/`. Nothing in
the repo now references a mesh, and there is no longer a v1/v2 pair that has to
be kept straight by name in `.vercelignore` forever.

- [x] **LICENSE added.** The repo has one.
- [x] **Mesh assets removed from the working tree.** 1.5 MB on disk, 469 KB on
      the wire, gone with the object they drew.
- [x] **History rewritten.** `vendor/mesh/brain-mni.bin` purged with
      `git filter-repo` and force-pushed to all three refs that carried it —
      `main`, `hero-v17`, the working branch. 0 occurrences across remote refs,
      file trees byte-identical, old commits not fetchable over the git protocol.

**🚩 STILL OPEN, and re-measured 2026-08-12 22:1x UTC — not assumed:**

| URL | Result |
|---|---|
| `raw.githubusercontent.com/bmath8/portfolio/cd2746e/vendor/mesh/brain-mni.bin` | **HTTP 200 · 2,703,404 bytes** |
| `raw.githubusercontent.com/bmath8/portfolio/24e1549/vendor/mesh/brain-mni.bin` | **HTTP 200 · 2,703,404 bytes** |
| `raw.githubusercontent.com/bmath8/portfolio/main/vendor/mesh/brain-mni.bin` | 404 — the tip is clean |

GitHub keeps unreachable objects until it garbage-collects, and it has not.
Deleting the file and rewriting history were both necessary and neither is
sufficient.

- [ ] **Brian: ask GitHub Support to garbage-collect the repository.** Wording:
      *"I rewrote history to remove a file. Please run `git gc` to purge
      unreachable objects."* Full request in `docs/github-support-gc-request.md`.
      **Until they do, the AGPL asset is still publicly downloadable by SHA.**

Re-test by re-running the three URLs above. Only all-404 closes this.

## Open — needs Brian
- [x] ✅ **`resume.pdf` now says 26 — FIXED HERE 2026-08-12, applications are unblocked.**
      Patched surgically: the single text operator carrying the digit was edited, so every other
      glyph, font and coordinate is untouched. Verified by rendering both versions and diffing —
      **the only changed pixels are a 12×16 px region**, one page still, and the extracted text
      is otherwise byte-identical.
      ⚠️ **This file is now AHEAD of the canonical builder, which still says 25.** Correct
      `C:\Brian\03_Career\evidence-bank.md` before the next rebuild or it will regress.
- [ ] **Correct `evidence-bank.md` upstream to 26** so the canonical build matches. Until then,
      do not re-copy a freshly built PDF over this one.
- [ ] ~~🚩 BLOCKING: `resume.pdf` says "25 scheduled agents."~~ superseded by the two items above.
      Original note: **The verified count
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
