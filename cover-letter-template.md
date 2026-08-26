# Cover Letter — Reusable Template

Brian's honest-builder voice. Fill the **[BRACKETS]**, keep it to ~250–300 words / one page.
Rule of thumb: 1 opening + 3 body paragraphs + 1 close. Never invent a fact.

## Pick the lane first — it must match the resume you attach

| Lane | Use when | Pairs with |
|---|---|---|
| **A · Developer / AI Builder** | Software, full-stack, AI-application, junior dev roles | `resume.pdf` in this repo (the AI/Full-Stack Developer lane) — **this is the default** |
| **B · Customer Ops / Support** | Support engineer, IT support, customer operations roles | The Customer Ops resume from `C:\Brian\03_Career\resumes\` |

Sending Lane B's letter with the developer resume is the most common way to weaken a strong
application — the letter talks about support instinct while the resume leads with shipped
software. Match them.

> **Fact check before sending:** the agent-fleet count is **26**, not 25. If the resume PDF you
> are attaching still says 25, rebuild it first (see `TASKS.md`).

---

# Lane A · Developer / AI Builder  ← default

Brian Mathew
New Jersey · (609) 815-1685 · mathew.brian@gmail.com
github.com/bmath8 · bmath8.vercel.app · linkedin.com/in/brian-mathew-66235556

[DATE]

Dear [HIRING MANAGER / "Hiring Team"],

I'm applying for the **[ROLE TITLE]** role at **[COMPANY]**. I'm a self-taught developer who
ships working software and then keeps it running — Python and TypeScript, React/Next.js front
ends, Flask and Node back ends, Postgres, Docker, and real test suites. Everything I claim
below is code you can open today at bmath8.vercel.app.

What I'd bring to **[COMPANY]**: [PICK 1–2 THAT MATCH THE POSTING]
- **I ship end to end.** I've taken ideas from first commit to running software: design,
  implementation, tests, deployment, and the operating afterwards. No hand-offs to hide behind.
- **I test what I build.** Brian OS carries an 81-test suite; BoomBox has Jest/RTL tests and
  Docker Compose. I write the suite, run it, and fix what it catches before shipping.
- **I make architectural calls and can defend them.** In BoomBox, Postgres holds what must
  survive a restart and Redis Pub/Sub carries what must not outlive the session — a split I
  chose deliberately and can walk you through.
- **I integrate LLMs into real products,** not demos: provider-agnostic AI calls, local-model
  routing through Ollama, and guardrails that require human approval before anything sends.

One example: Brian OS is a native-Windows agent fleet running **30 scheduled agents** on r
cron lines with local-LLM routing and Telegram control. While operating it, a failed process
guardian silently left orphan processes that exhausted the machine's disk. I traced the root
cause, recovered the system, restored monitoring, and added liveness checks so it cannot recur.
Building it was half the work; keeping it alive taught me the other half.

I'd welcome the chance to bring that to **[COMPANY]**. My resume and live, source-linked case
studies are at **bmath8.vercel.app**. Thank you for your time.

Sincerely,
Brian Mathew

---

# Lane B · Customer Ops / Support

Brian Mathew
New Jersey · (609) 815-1685 · mathew.brian@gmail.com
github.com/bmath8 · bmath8.vercel.app · linkedin.com/in/brian-mathew-66235556

[DATE]

Dear [HIRING MANAGER / "Hiring Team"],

I'm applying for the **[ROLE TITLE]** role at **[COMPANY]**. I'm a customer-focused
technical builder: I've led a retail sales team and worked directly with customers for
years, and more recently I've built, tested, and operated real software from scratch — so I
can sit between a frustrated user and a broken system and actually move things forward.

What I'd bring to **[COMPANY]**: [PICK 1–2 THAT MATCH THE POSTING]
- **Troubleshooting that isolates the real problem.** In my projects I separate a system into
  independently testable parts so a failure can be found and fixed one stage at a time — the
  same instinct that makes a good support engineer.
- **Clear communication under pressure.** Years of high-consideration retail sales taught me
  to explain technical things plainly and keep a customer confident while I work the issue.
- **Follow-through and honest status.** I document what I build, test it, and say plainly what
  works and what's still in progress — no overselling.

One example: while operating my Windows automation fleet, a failed process guardian silently
left orphan processes that exhausted the machine's disk. I traced the root cause, recovered
the system, restored monitoring, and added liveness checks to prevent it from happening again.
That's the loop I bring to support work — reproduce, isolate, fix, and harden.

I'd welcome the chance to bring that mix of customer skill and hands-on technical work to
**[COMPANY]**. My resume and a live portfolio of my projects are at **bmath8.vercel.app**.
Thank you for your time.

Sincerely,
Brian Mathew

---

## Quick-fill checklist
- [ ] **Picked the lane (A or B) and attached the matching resume**
- [ ] Role title + company pasted in (3 places: opening, body, close)
- [ ] Picked the 1–2 bullets that match *this* posting's keywords
- [ ] Swapped the example paragraph if the job wants a different strength
- [ ] Under one page / ~300 words
- [ ] Re-read: every claim is true — and the agent count says **26**

## Voice notes
- First person, plain, confident-not-boastful. Short sentences.
- **Lane A:** lead with what you shipped, back it with how you operate it.
- **Lane B:** lead with the customer angle, back it with the building.
- The honesty ("what works and what's in progress") is a feature — it matches the resume.
- Never claim a live deployment BoomBox doesn't have. The site says "no live deployment"
  plainly; the letter must not contradict it.
