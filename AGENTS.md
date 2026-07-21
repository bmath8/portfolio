# AGENTS.md — portfolio

Guidance for AI coding agents working in this repo.

## What this is
Brian's employer-facing portfolio site: a single static `index.html` (inline CSS, no build),
deployed on Vercel at bmath8.vercel.app. `resume.pdf` (linked from the site) is generated from
the editable source at `resume/resume.html`. See `INVENTORY.md` for the full catalog of resumes
and projects.

## Status: PUBLIC
As of the 2026-06 launch the site is **public and indexable** — the old password gate
(`middleware.js`) and access drafts were removed, and `robots.txt` allows indexing. There is no
longer a `middleware.js` or `ats/` directory. Do not reintroduce a gate without Brian's approval.

## Rules (see AGENT_RULES.md for the full set)
- Keep it a zero-build static site — no frameworks/bundlers unless Brian asks.
- Keep the site, `resume.pdf`, and `resume/resume.html` consistent with each other — the project
  facts (agent counts, test numbers, stack) must match across all three and stay truthful.
- To change the resume: edit `resume/resume.html`, then re-render:
  `chromium --headless --print-to-pdf=resume.pdf --no-pdf-header-footer file://…/resume/resume.html`
  (keep it to one page). The `resume/` source is excluded from the Vercel deploy.
