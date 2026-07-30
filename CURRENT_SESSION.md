# Current Session

## Last known state (2026-07-30)
The redesign is **finished and committed**. Eleven candidates (A–K) were abandoned; the
decision was to re-skin the real `index.html` rather than ship a twelfth candidate.

- **Palette** moved off warm-cream + serif-italic + terracotta — that exact combination is
  the most common AI-generated portfolio look, and it was what this site wore. Now cool
  paper / graphite / one operational green.
- **Content paints instantly.** The old reveal-on-scroll started every section at
  `opacity:0`; the page read as blank for ~2s. Removed, not patched.
- **AI Job Hunter is off the site.** It is the tool used to apply to the employers reading
  the page. Its repo stays private by Tom's decision (2026-07-30).
- **Case studies now link to real public source** — `brian-os` and `boombox` were published
  that day. Super Bowl Squares was promoted to Case 02 because it is the only case with a
  live, publicly usable app.
- **Hero dial is real.** 25 nodes read from `hermes cron list`. Candidate F's version had
  invented two agents (`inbox-pm`, `fleet-health-pm`) and dropped the real `system-watchdog`
  — caught before shipping. 81 tests confirmed by a live `pytest` run the same day.
- **Zero third-party requests.** Fonts self-hosted (latin subset, 160KB). No Google Fonts.
- **OG tags + `og.png`** added. The link used to unfurl as a bare URL.
- **`resume.pdf` switched to the AI Builder lane** (96%) so the download matches the page.
- **`.vercelignore` now excludes `design-candidates/`** — 11 rejected drafts had been
  deploying publicly and were crawlable.

Verified before commit: no horizontal overflow at 360px · no `opacity:0` anywhere, so it
renders with JS disabled · reduced-motion respected · focus-visible outlines · all six
outbound links return 200 · 6 same-origin requests total.

## Not done
1. **Deploy.** Everything above is local + committed. Vercel still serves the old page,
   which still shows the unverifiable Best Buy sales-ranking claim. Needs Tom's go.
2. **Pin repos on the GitHub profile** — GitHub exposes no API for pinning; it is a manual
   UI step. See `FOR TOM.md` in `C:\Brian\03_Career\`.
3. **Revoke the Tenor/Google API key** still in `boombox-v5` git history (the *private*
   original — the public mirror uses an env var and is clean).

## Where the rest of the work lives
`C:\Brian\03_Career\` — resumes, cover letters, evidence bank, tracker, command center.
Start there: `C:\Brian\03_Career\FOR TOM.md`.
