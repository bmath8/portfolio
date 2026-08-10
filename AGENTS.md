# AGENTS.md — portfolio

Guidance for AI coding agents working in this repo.

## What this is
Brian's employer-facing portfolio site: a single static `index.html` (inline CSS, no build),
deployed on Vercel at bmath8.vercel.app. `resume.pdf` (linked from the site) is a **copy of
canonical output built outside this repo** — see the resume rule below. `resume/resume.html` is
a superseded original, kept but no longer the source of anything. See `INVENTORY.md` for the
full catalog of resumes and projects.

## Status: PUBLIC
As of the 2026-06 launch the site is **public and indexable** — the old password gate
(`middleware.js`) and access drafts were removed, and `robots.txt` allows indexing. There is no
longer a `middleware.js` or `ats/` directory. Do not reintroduce a gate without Brian's approval.

## Rules (see AGENT_RULES.md for the full set)
- Keep it a zero-build static site — no frameworks/bundlers unless Brian asks.
- Keep the site, `resume.pdf`, and `resume/resume.html` consistent with each other — the project
  facts (agent counts, test numbers, stack) must match across all three and stay truthful.
- **Do not edit the resume in this repo.** `resume.pdf` is a copy of canonical output; hand-editing
  it or re-rendering from `resume/resume.html` resurrects the 5th competing resume system that the
  2026-07-29 consolidation deliberately killed (`resume/SUPERSEDED-2026-07-29.md`). To change the
  resume: edit the evidence bank `C:\Brian\03_Career\evidence-bank.md`, rebuild via
  `resumes\build_strong_resumes.py` + `render_pdfs.py`, then re-copy the built PDF over
  `resume.pdf` here. Both `resume/` and the PDF's source are excluded from the Vercel deploy.
