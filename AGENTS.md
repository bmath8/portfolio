# AGENTS.md — portfolio

Guidance for AI coding agents working in this repo (added by the 07-06 audit).

## What this is
Brian's employer-facing portfolio site (static `index.html` + Vercel `middleware.js` password gate), deployed at bmath8.vercel.app. `ats/` holds ATS-related assets.

## Rules (see AGENT_RULES.md for the full set)
- The site is PASSWORD-GATED and unindexed by Brian's explicit rule ("nothing public unless I say so"). Never remove or weaken `middleware.js` or `robots.txt` without his approval.
- Keep it a zero-build static site — no frameworks/bundlers unless Brian asks.
- Test the password gate after any middleware change before calling work done.
