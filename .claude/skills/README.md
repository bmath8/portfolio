# Vendored: Meng To's Agent Skills (web-design subset)

**Source:** https://github.com/MengTo/Skills · **Licence:** MIT, © 2026 Meng To
(full text in `LICENSE-MengTo-Skills`).

85 web-design skills, vendored 2026-08-11 so Claude Code can load them as working context.

## What was and was not vendored

**Vendored:** `SKILL.md` playbooks plus their `.md` references, and any `.js` / `.css` /
`.json` / `.yaml` a skill ships. **~5.4 MB.**

**Not vendored:** the demo `.jpg` / `.webp` / `.png` screenshots and standalone `.html` demo
pages — **~87 MB** of the upstream 92 MB. They are reference imagery, not instructions, and a
portfolio repo should not carry them. Read them upstream when needed.

Excluded from the Vercel deploy in `.vercelignore`.

## The ones that apply to this project

| Skill | Why |
|---|---|
| `build-awwwards-quality-sites` | The acceptance bar, stated as a checklist |
| `build-threejs-scroll-worlds` | Scroll-driven camera through a 3D world — the core mechanism |
| `cinematic-scroll-storytelling` | Chapter pacing and shot composition |
| `editorial-portfolio-chapters` | Editorial type and chapter structure |
| `threejs` | Baseline three.js practice |

## Two standing cautions

1. **These are a bar, not a source to copy.** The skill's own words: *"Never reuse, trace, or
   closely reproduce reference assets, screenshots, source code, identity, or copy."* The
   related `Kage` project is **not** MIT — it states no licence is granted for reuse. Technique
   only, never transcription.

2. **Where a skill conflicts with `SCENE-BRIEF.md`, the brief wins.** Notably the skills assume
   GSAP + Lenis; this site is zero-dependency and vendors only three.js, and `Kage` itself ships
   neither. Do not add a dependency because a skill mentions it.
