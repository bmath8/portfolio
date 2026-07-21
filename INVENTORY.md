# Portfolio & Resume Hub — Master Inventory

_The one place. Everything you built across ChatGPT, Codex, and Claude, cataloged so you
can finish it and send it. Last consolidated: 2026-07-20._

This repo (`bmath8/portfolio`, live at **bmath8.vercel.app**) is the hub. The portfolio
site and the polished resume already live here — this file is the index that ties every
resume version and every project to it, with an honest status on each.

---

## 1. Resumes

| Version | Where it lives | Date | Status |
|---|---|---|---|
| **`resume.pdf`** (current) | This repo — linked from the live site | 2026 | ✅ **FINAL / SENDABLE.** Rebuilt 2026-07-20 from an editable source (`resume/resume.html`) — one page, ATS-safe (real text, single column), now includes the portfolio URL and sharpened, verified project bullets. |
| `resume/resume.html` | This repo | 2026-07-20 | ✏️ **Editable source** for the PDF. Edit this, re-render with headless Chromium `--print-to-pdf`. No more locked binary. |
| BMAT Resume.docx | Google Drive | 2018 | 🗄️ Legacy — pre-AI, outdated. Keep for reference only. |
| BMAT RESUME.doc / "BMAT RESUME" | Google Drive | 2012 | 🗄️ Legacy — very old. Archive. |

**The current resume is done.** It positions you as a *"Customer-focused technical builder"*
targeting **Product Support / IT Support / Customer Support & Implementation**, with three
projects, a skills block, Best Buy + Uber experience, and education. One page, clean, ATS-friendly.

> Note: Resumes you drafted inside ChatGPT/Codex/Claude *chat histories* aren't reachable by
> file scan — but their finished output is what became `resume.pdf`. A Drive scan for any
> post-2025 resume/cover-letter docs found none, so nothing recent is stranded outside this repo.

**Gap to close:** no LinkedIn URL and no cover-letter template yet. See §5.

---

## 2. Portfolio site — `index.html`

- **Status:** ✅ Publicly launched. Access gate removed, indexing allowed, live on Vercel.
- **Design:** "Editorial Engineering" system (IBM Plex, single static file, zero build).
- **Features 3 case studies** — the same three on the resume:
  1. **AI Job Hunter** — truth-constrained application workflow (Flask/SQLAlchemy)
  2. **Brian OS** — Windows automation & operational-recovery fleet (Python/PowerShell/Ollama)
  3. **BoomBox** — real-time collaborative music prototype (Next.js/React/Postgres/Redis)
- **Sendable now?** Yes. This is the link to put on the resume, LinkedIn, and applications.

---

## 3. All projects (21 GitHub repos under `bmath8`)

Classified by portfolio value. Tier 1 = already shipped on the site. Tier 2 = real apps worth
featuring or linking once cleaned up. Tier 3 = infra / experiments / scratch — not front-line.

### Tier 1 — Featured on site + resume (DONE)
| Repo | Stack | What it is |
|---|---|---|
| `ai-job-hunter` | Python | AI Job Hunter — resume/cover-letter tailoring, no fabrication |
| `brian-os-fleet` | Python | Brian OS — always-on Windows agent fleet |
| `BoomBox-V.5` | TypeScript | BoomBox — social/collaborative music app |

### Tier 2 — Portfolio candidates (real apps; review + polish → feature or link)
| Repo | Stack | What it is | Note |
|---|---|---|---|
| `pokemon-drop-intel` | TypeScript / Next.js | Pokémon TCG collection & drop-intel dashboard (sample-data demo) | **Strongest unfeatured candidate** — has a demo mode, recently active. Good 4th case study. |
| `luxescape-travel-agent` | Python | AI travel-planning agent | Feb 2026 |
| `ai-bible-study-app` | Python | AI Bible study app | Jan 2026 |
| `DentalPro` | TypeScript | Dental office manager | Oct 2025 |
| `prediction-trader-frontend` | TypeScript | Prediction-market trading UI | Jun 2026 |
| `viral-forge` | Python | Content/virality tool | Jun 2026 |
| `AI-Automated-Income-Engine` | — | Automated social-media clipper | Oct 2025 |
| `fam-super-bowl-squares-2026` | JavaScript | Super Bowl squares web app | small but complete, real users |
| `giveaway-app` / `Giveaway-Automation-Zenith` | Python | Giveaway automation | two versions |

### Tier 3 — Infra / experiments / scratch (not portfolio front-line)
| Repo | Stack | Note |
|---|---|---|
| `jarvis` / `jarvis-backup` | TypeScript | assistant experiments |
| `brian-os-standards` | PowerShell | Brian OS standards/infra |
| `MCP-GearBox` | — | MCP tooling |
| `money-maker`, `Credit-Repair`, `JustTrying` | — | likely scratch/empty |

> Tier 2/3 classification is from repo metadata (name, language, description, dates) — file
> contents of repos other than `portfolio` aren't readable in this session. To pull any repo
> in for a real look and possible feature, say "add `<repo>`" and I'll scan it.

---

## 4. What's sendable RIGHT NOW

You are not starting from zero — you're basically done for a first application wave:

- ✅ One-page resume (`resume.pdf`)
- ✅ Live portfolio site with 3 real case studies
- ✅ GitHub profile with 21 repos backing up the "I build things" claim

**You can start applying today** to product-support / IT-support / customer-support roles.

---

## 5. To reach "final final" (recommended, in order)

1. **LinkedIn** — provide the handle; it goes back on the resume contact line + site hero.
   (Removed from the shipped PDF for now so there's no broken placeholder.)
2. ✅ **Cover-letter template** — done: `cover-letter-template.md` (reusable, matches resume voice).
3. **Screenshots** — the three featured repos already have solid, honest READMEs (written by a
   prior session) with screenshot *placeholders*. Drop a real screenshot/GIF into each repo's
   `docs/screenshot.png` — the one thing only you can do (they're your running apps).
4. **Pick a 4th case study** (optional) — `pokemon-drop-intel` is the strongest candidate. A
   strong trio is fine; don't pad. Decide later.
5. **Housekeeping** — `AGENTS.md` still says the site is password-gated; it isn't anymore.

### Verified during consolidation (2026-07-20)
The three featured projects are **substantial and real**, not throwaway:
- `ai-job-hunter` — ~30k lines Python, 21 test modules, Docker + Render, GPT-4/Claude, ATS scorer. README status: ~85% (v0.9).
- `brian-os-fleet` — **25 scheduled agents** on a local LLM, Telegram control, approval-gated actions, **81 tests** (green on Windows). Site corrected 24 → 25 agents.
- `boombox-v.5` — ~48k lines TypeScript, Next.js/Supabase/Redis/WebSockets, 20 test files, production-grade infra.

> "Unfinished" is fine and honest — the site already labels each project's true status. The goal
> was never to finish 21 projects; it's 3 legible ones + apply. That bar is met.

---

## 6. Where to work from now

Everything is here in `bmath8/portfolio`:
- `index.html` — the site
- `resume.pdf` — the resume
- `INVENTORY.md` — this catalog (the map of everything)
- `PROJECT_BRIEF.md`, `TASKS.md`, `CURRENT_SESSION.md` — working notes

No more hunting across ChatGPT / Codex / Claude / Drive / GitHub. This file is the index; the
repo is the home.
