# Portfolio & Resume Hub — Master Inventory

_The one place. Everything you built across ChatGPT, Codex, and Claude, cataloged so you
can finish it and send it. Last consolidated: 2026-07-20._

This repo (`bmath8/portfolio`, live at **bmath8.vercel.app**) is the hub. The portfolio
site and the polished resume already live here — this file is the index that ties every
resume version and every project to it, with an honest status on each.

---

## 1. Resumes — ⚠️ THIS REPO IS NO LONGER THE RESUME SOURCE (changed 2026-07-29)

**Resumes are built in `C:\Brian\03_Career\`, not here.** This repo's `resume.pdf` is now a
*copy* of canonical output. Do not hand-edit it.

| Version | Where it lives | Status |
|---|---|---|
| **The 4-lane arsenal** | `C:\Brian\03_Career\resumes\` | ✅ **CANONICAL.** Built from `evidence-bank.md` via `build_strong_resumes.py` + `render_pdfs.py`. Every build date-stamped into `resumes/versions/<date>/`. |
| `resume.pdf` (this repo) | copied from the canonical **AI/Full-Stack Developer** lane | ✅ Served by the live site. Refresh by re-copying after a canonical rebuild. **Verified 2026-08-10** by extracting the PDF text: the headline reads "AI Application Developer · Full-Stack Developer · Junior Software Developer". This file previously claimed the copy was `Brian_Mathew_Customer_Ops.pdf` — that was wrong. |
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
- **Features 3 case studies** (⚠️ **no longer the same three as the resume** — AI Job Hunter was
  dropped from the site but is still the resume's lead bullet):
  1. **Brian OS** — Windows automation & operational-recovery fleet (Python/PowerShell/Ollama)
  2. **Super Bowl LX Squares** — real-time app that ran a real event (React/Firebase RTDB)
  3. **BoomBox** — real-time collaborative music prototype (Next.js/React/Postgres/Redis)
- **Sendable now?** Yes. This is the link to put on the resume, LinkedIn, and applications.
  All three case-study links resolve to public source (verified 2026-08-10).

---

## 3. All projects (31 GitHub repos under `bmath8` — 7 PUBLIC)

> **Re-verified 2026-08-10.** 31 repos exist; 24 are private. Public: `portfolio`, `brian-os`,
> `boombox`, `pokemon-drop-intel`, `fam-super-bowl-squares-2026`, `bmath8` (profile README),
> and `claude-code-templates` (a fork). Note `jobfit` is **private** now, not public as the
> 2026-07-29 entry claimed.
>
> ✅ **The showcase-mirror fix is DONE.** `bmath8/brian-os` and `bmath8/boombox` are public
> mirrors with fresh history, and every case-study link on the live site resolves to public
> source. The originals (`brian-os-fleet`, `BoomBox-V.5`) stay private.
>
> ⚠️ `ai-job-hunter` is **still private** and has no mirror — it is off the site, but it is
> still the **lead bullet on `resume.pdf`**, so a recruiter reading the resume cannot open it.

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
- ✅ Live portfolio site with 3 real case studies, all linking to public source
- ✅ Four base cover letters + tailoring guide (`03_Career/cover-letters/`), plus the
  two-lane template in this repo (`cover-letter-template.md`)
- ✅ A command center that tracks the funnel (`03_Career/command-center/index.html`)
- ✅ GitHub profile now shows the featured work: `brian-os` and `boombox` are public mirrors.
- ⚠️ **One blocker before sending:** `resume.pdf` says "25 scheduled agents"; the verified count
  is **26** (`agents.json`, `hermes cron list`, and the live site all say 26). Fix upstream in
  the evidence bank and re-copy — see `TASKS.md`.

**You can start applying today** — pick the lane, score against the posting, log it.

---

## 5. To reach "final final" (recommended, in order)

1. ✅ **LinkedIn** — done. `linkedin.com/in/brian-mathew-66235556` is live on both the site
   (hero + contact) and the shipped PDF.
2. ✅ **Cover-letter template** — done: `cover-letter-template.md`, now with **two lanes**
   (Developer/AI Builder + Customer Ops/Support) so the letter matches whichever resume is sent.
3. **Screenshots** — the three featured repos already have solid, honest READMEs (written by a
   prior session) with screenshot *placeholders*. Drop a real screenshot/GIF into each repo's
   `docs/screenshot.png` — the one thing only you can do (they're your running apps).
4. **Pick a 4th case study** (optional) — `pokemon-drop-intel` is the strongest candidate. A
   strong trio is fine; don't pad. Decide later.
5. ✅ **Housekeeping** — done. `AGENTS.md` no longer claims a password gate, and (2026-08-10)
   no longer tells agents to re-render the resume from the superseded `resume/resume.html`.

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
