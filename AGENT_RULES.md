# Agent Rules
_For any AI tool working in this repo (this assistant, Codex, Cline, Aider, Ollama). Keep context lean, output tight._

## Operating principles
- Prefer the smallest sufficient context. Read only the files needed for the current task.
- Do not preload large folders, generated assets, or dependencies (`node_modules`, `.next`, `dist`, `venv`).
- Before major edits, restate goal, constraints, and success criteria in 5 bullets or fewer.
- After each milestone, summarize what changed and update `CURRENT_SESSION.md`.
- When uncertain, inspect before editing.
- When a task becomes repo-wide, produce an escalation packet (`ESCALATION_PACKET.md`) instead of dragging all prior chat forward.

## Editing rules
- Make the minimum viable change.
- Preserve existing style and architecture unless `TASKS.md` says otherwise.
- Prefer patches/diffs over full-file rewrites.
- Keep outputs concise: plan, action, result, next step.

## Tool rules
- Use search/grep/listing before full file reads.
- Use one external connector or MCP server only when the task requires it.
- If a tool returns large output, summarize it before continuing.

## Model routing (cost discipline)
- **Tier 1 — local Ollama** for repo scan, grep, classify, summarize, boilerplate, small edits.
- **Tier 2 — cheap cloud** (GPT-5 mini / Haiku 4.5 / Gemini Flash-Lite) for medium multi-file work.
- **Tier 3 — frontier** (Sonnet 4.6 / GPT-5.2-Codex / Opus 4.8 / Gemini 3.1 Pro) only with a compact escalation packet.
- One AI driver at a time on this repo. Never two agents editing the same files concurrently.
