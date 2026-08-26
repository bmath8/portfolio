# Portfolio & Resume Hub — Master Inventory

_The one place. Everything you built across ChatGPT, Codex, and Claude, cataloged so you
can finish it and send it. Last consolidated: 2026-07-20._

This repo (`bmath8/portfolio`, live at **bmath8.vercel.app**) is the hub. The portfolio
site and the polished resume already live here — this file is the index that ties every
resume version and every project to it, with an honest status on each.


> **Update 2026-08-12 — v7.** The live site is now two designs, not one: **Mission Control**
> at `/` (`index.html`) and **Neural** at `/neural`. Both carry identical content and
> cross-link in their footers. The previous single-page build is archived at
> `design-candidates/archive/v6-brain-hero.html`. See `README.md` for structure,
> `docs/DESIGN-SYSTEM.md` for tokens and components, and `docs/CHANGELOG-v7.md` for what
> changed and why.
> **Update 2026-08-26.** Five more v6-era documents — `TECHNIQUE.md`, `DESIGN-REFERENCE.md`,
> `SCENE-BRIEF.md`, `REFERENCES-2026-08-05.md` and `RESEARCH-2026-08-11.md` — were moved to
> `docs/archive/v6/`. They described the retired mesh hero and were still sitting at the repo
> root, where they read as current. See that folder's README for what each one is still good
> for.
>
> **Update 2026-08-12 (v7.4).** `HERO-BRIEF.md`, `BRAIN-TECHNIQUE-2026-08-05.md` and
> `V6-PLAN-2026-08-05.md` describe the retired v6 brain hero and moved to
> `docs/archive/v6/` (see the README there — the licensing record is the reason
> `BRAIN-TECHNIQUE` was kept). `AGENTS.md` and `CURRENT_SESSION.md` were rewritten
> against the current two-design site.

---

## 1. Resumes — ⚠️ THIS REPO IS NO LONGER THE RESUME SOURCE (changed 2026-07-29)

**Resumes are built in `C:\Brian\03_Career\`, not here.** This repo's `resume.pdf` is now a
*copy* of canonical output. Do not hand-edit it.

| Version | Where it lives | Status |
|---|---|---|
| **The 4-lane arsenal** | `C:\Brian\03_Career\resumes\` | ✅ **CANONICAL.** Built from `evidence-bank.md` via `build_strong_resumes.py` + `render_pdfs.py`. Every build date-stamped into `resumes/versions/<date>/`. |
| `resume.pdf` (this repo) | copied from `variants/L3_strong/Brian_Mathew_AI_Builder_L3_strong.pdf` (2026-08-19) | ✅ Served by the live site. Refresh by re-copying after a canonical rebuild. |
| `resume/resume.html` | this repo | 🗄️ **SUPERSEDED** — see `resume/SUPERSEDED-2026-07-29.md`. Was a separately-maintained 5th resume. Kept as an original, not deleted. |

**Why this changed.** A 2026-07-29 machine-wide sweep found **five** competing resume systems
(three of them duplicate copies of each other). This repo's resume was one of them — it had
Best Buy and the portfolio URL that the canonical set lacked, but was missing LinkedIn, wasn't
generated from the evidence bank, and was never scored. Both gaps are now fixed upstream in the
canonical builder, so the split is over. Full register:
`C:\Brian\03_Career\_archive\ORIGINALS-FOUND-2026-07-29.md`.

**Current lane scores** (vs. representative JDs, 2026-07-29):
AI Builder **96%** · AI Trainer **92%** · Customer Ops **92%** · IT Support **88%**.

**Gaps closed 2026-07-29:** LinkedIn added to the site and all resumes; cover-letter template
existed already (4 full base letters live in `03_Career/cover-letters/`).

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

## 3. All projects (27 GitHub repos under `bmath8` — ⚠️ only 4 are PUBLIC)

> **Verified 2026-07-29 via the GitHub API.** 27 repos exist; **23 are private.** The only
> public ones are `portfolio`, `jobfit`, `pokemon-drop-intel`, and
> `fam-super-bowl-squares-2026`. **All three repos featured as case studies on the live site
> — `ai-job-hunter`, `brian-os-fleet`, `BoomBox-V.5` — are PRIVATE.** An employer who clicks
> `github.com/bmath8` cannot see any of the work the resume is built on. Fix in progress:
> public-safe showcase mirrors (fresh history, secret-scanned).

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

- ✅ Four one-page resumes, scored 88–96% against real postings
- ✅ Live portfolio site with 3 real case studies
- ✅ Four base cover letters + tailoring guide (`03_Career/cover-letters/`)
- ✅ A command center that tracks the funnel (`03_Career/command-center/index.html`)
- ⚠️ GitHub profile shows only **4 public repos**, none of them the featured three —
  corrected from the earlier false claim of "21 repos backing up the 'I build things' claim."

**You can start applying today** — pick the lane, score against the posting, log it.

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
- `brian-os-fleet` — **30 scheduled agents** on a local LLM, Telegram control, approval-gated actions, **221 tests** (green on Windows). Site cor
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
