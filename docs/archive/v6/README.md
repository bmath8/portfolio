# docs/archive/v6/

These describe the **v6 brain-hero build, retired on 2026-08-12** and replaced by the two
designs documented in `docs/DESIGN-SYSTEM.md`. They are kept, not deleted, because they record
research and decisions that a diff cannot — and in one case, licensing provenance that still
matters.

| File | Why it is still here |
|---|---|
| `BRAIN-TECHNIQUE-2026-08-05.md` | **The licensing record.** Documents that `vendor/mesh/brain-mni.bin` was AGPL-3.0 (derived from aces/brainbrowser), that it was served publicly once, and why it was replaced with a permissively-licensed ICBM152 surface. Keep this: it is the paper trail for a real licensing problem, even though every mesh it names was deleted in the v7.1 vendor prune. |
| `V6-PLAN-2026-08-05.md` | The five-phase plan of record for the retired hero. Useful as an example of how the work was scoped. |
| `HERO-BRIEF.md` | The particle-brain brief. Its conclusion — *"the technique fights the subject"* — is the reasoning that eventually led to abandoning the scroll-jacked 3D hero, so it is the origin of the v7 rebuild. |

| `TECHNIQUE.md` | *(archived 2026-08-26)* What to build for the v6 hero, read 2026-08-04 from primary sources. Its techniques — matcap shading, thresholded edge contours, instanced tract lines — belong to a mesh that no longer exists. |
| `DESIGN-REFERENCE.md` | *(archived 2026-08-26)* The 2026-08-04 design study behind v6. Still quotes 25 agents and 81/81, and a palette that was retracted. Superseded entirely by `docs/DESIGN-SYSTEM.md`. |
| `SCENE-BRIEF.md` | *(archived 2026-08-26)* "The document that must exist before any more 3D work" — for the cortical-mesh scene. That scene was deleted; the brief now describes nothing that ships. |
| `REFERENCES-2026-08-05.md` | *(archived 2026-08-26)* Thirty-four analysed sites, shortlisted for the v6 hero. Historically interesting, but chosen against a brief that no longer applies. |
| `RESEARCH-2026-08-11.md` | *(archived 2026-08-26)* Frontend and 3D research from 2026-08-11, current *as of that date*. Names `brain-mni` and matcap work that has since been deleted. |

**Nothing in here describes the current site.** Do not follow these documents. Every asset
they reference under `vendor/mesh/`, `vendor/lines/`, `vendor/postprocessing/` and
`vendor/hdr/` was deleted — recover from git history if you ever genuinely need one.

Current documentation: `README.md` (what ships, and **the numbers**), `AGENTS.md` (how to
work in the repo), `docs/DESIGN-SYSTEM.md` (tokens and editing rules), `docs/CHANGELOG-v7.md`
(why it looks the way it does), `TASKS.md` (what is still open).
