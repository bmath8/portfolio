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

**Nothing in here describes the current site.** Do not follow these documents. Every asset
they reference under `vendor/mesh/`, `vendor/lines/`, `vendor/postprocessing/` and
`vendor/hdr/` was deleted — recover from git history if you ever genuinely need one.

Current documentation: `AGENTS.md`, `docs/DESIGN-SYSTEM.md`, `docs/CHANGELOG-v7.md`.
