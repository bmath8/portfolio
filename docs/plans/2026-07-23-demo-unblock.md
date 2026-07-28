# Demo Unblock Implementation Plan (Plan 1 of 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every live demo URL reachable and non-empty, so nothing linked from the resume looks broken.

**Architecture:** A single reusable verification script is written first and must fail; each subsequent task makes one more assertion pass. No visual redesign, no new demo infrastructure — that is Plans 2–4. This plan only stops the bleeding.

**Tech Stack:** PowerShell (verification), Next.js middleware (pokemon-drop), vanilla JS + localStorage (warranty-tracker), static HTML (portfolio).

## Global Constraints

- Demo gate pages MUST return **HTTP 200**, never 401/403. A non-200 makes link previews and corporate proxies treat the URL as dead.
- Only **production aliases** may be recorded anywhere. Deployment-hash URLs (`*-<hash>-bmath8s-projects.vercel.app`) are protected and MUST NOT appear in any doc, resume, or portfolio.
- No secret may be committed. The pokemon access code moves to env-only; no source fallback.
- No demo may render an empty/zero state on first load.
- `credit-repair-os` visibility is NOT changed in this plan (spec decision D2 — needs explicit approval).
- Verified production aliases (confirmed 2026-07-23):
  - `https://boom-box-v-5.vercel.app`
  - `https://warranty-tracker-azure.vercel.app`
  - `https://fam-super-bowl-squares-2026.vercel.app`
  - `https://pokemon-drop-intel.vercel.app`
  - `https://bmath8.vercel.app`

---

### Task 1: Verification script (the failing test)

**Files:**
- Create: `C:\Brian\02_Projects\portfolio\scripts\verify-demos.ps1`

**Interfaces:**
- Produces: `verify-demos.ps1` — exits 0 when all demo URLs return 200, exits 1 otherwise. Tasks 2–4 rely on this as the gate.

- [ ] **Step 1: Write the verification script**

```powershell
# verify-demos.ps1 — asserts every demo URL is reachable (AC1).
$urls = @(
  'https://boom-box-v-5.vercel.app',
  'https://warranty-tracker-azure.vercel.app',
  'https://fam-super-bowl-squares-2026.vercel.app',
  'https://pokemon-drop-intel.vercel.app',
  'https://bmath8.vercel.app'
)
$fail = 0
foreach ($u in $urls) {
  try {
    $r = Invoke-WebRequest -Uri $u -MaximumRedirection 5 -SkipHttpErrorCheck -TimeoutSec 20
    $code = $r.StatusCode
    $final = $r.BaseResponse.RequestMessage.RequestUri.AbsoluteUri
  } catch { $code = 0; $final = 'ERROR' }

  $sso = $final -like '*vercel.com/login*'
  if ($code -eq 200 -and -not $sso) {
    "PASS  $code  $u"
  } else {
    $why = if ($sso) { 'SSO WALL' } else { "HTTP $code" }
    "FAIL  $why  $u"
    $fail++
  }
}
if ($fail -gt 0) { "`n$fail of $($urls.Count) FAILED"; exit 1 }
"`nAll $($urls.Count) demos reachable"; exit 0
```

- [ ] **Step 2: Run it and confirm it FAILS**

Run: `powershell -File C:\Brian\02_Projects\portfolio\scripts\verify-demos.ps1`
Expected: `FAIL  HTTP 401  https://pokemon-drop-intel.vercel.app` and `1 of 5 FAILED`, exit code 1.

- [ ] **Step 3: Commit**

```bash
cd "C:\Brian\02_Projects\portfolio"
git add scripts/verify-demos.ps1
git commit -m "test: add demo reachability verification script (pokemon currently fails)"
```

---

### Task 2: Pokemon gate returns 200, code moves to env

**Files:**
- Modify: `C:\Brian\02_Projects\pokemon-drop\middleware.ts:3` and `:39`

**Interfaces:**
- Consumes: `verify-demos.ps1` from Task 1.
- Produces: gate page served at HTTP 200; access code read only from `process.env.SITE_PASSWORD`.

**Context:** The gate is intentional and well-built — `?code=` sets a cookie and clean-redirects, so the resume→portfolio→demo chain has no second prompt. Keep all of that. Two defects: it returns 401 (looks dead to link previews and proxies), and the code has a hardcoded source fallback.

- [ ] **Step 1: Change the status code**

In `middleware.ts`, line 39, replace:

```typescript
  return new NextResponse(page, { status: 401, headers: { "Content-Type": "text/html; charset=utf-8" } });
```

with:

```typescript
  // 200, not 401: a non-200 makes link-preview bots and corporate proxies treat
  // this URL as dead. The page still gates; only the wire status changes.
  return new NextResponse(page, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
```

- [ ] **Step 2: Remove the hardcoded fallback**

Replace line 3:

```typescript
const CODE = process.env.SITE_PASSWORD || "<the value of SITE_PASSWORD>";
```

with:

```typescript
const CODE = process.env.SITE_PASSWORD;
```

and change the code check on line 17 so a missing env var never grants access:

```typescript
  if (CODE && url.searchParams.get("code") === CODE) {
```

- [ ] **Step 3: Confirm SITE_PASSWORD is set in Vercel production**

Run: `vercel env ls --scope bmath8s-projects`
Expected: `SITE_PASSWORD` listed for Production. If absent, add it:
`vercel env add SITE_PASSWORD production` (enter the value of `$env:SITE_PASSWORD`).
This step is required — without it, Step 2 locks the demo out entirely.

- [ ] **Step 4: Deploy**

```bash
cd "C:\Brian\02_Projects\pokemon-drop"
vercel --prod --yes
```

- [ ] **Step 5: Verify the gate returns 200 and still gates**

Run: `curl.exe -s -o NUL -w "%{http_code}\n" https://pokemon-drop-intel.vercel.app`
Expected: `200`

Run: `curl.exe -s https://pokemon-drop-intel.vercel.app | Select-String "access code"`
Expected: a match — the gate page is still served (it gates, it just doesn't 401).

- [ ] **Step 6: Verify the code path still grants access**

Run: `curl.exe -s -o NUL -w "%{http_code}\n" -L "https://pokemon-drop-intel.vercel.app/?code=$env:SITE_PASSWORD"`
Expected: `200`, and the response is the app, not the gate page.

- [ ] **Step 7: Run the Task 1 script — now fully green**

Run: `powershell -File C:\Brian\02_Projects\portfolio\scripts\verify-demos.ps1`
Expected: `All 5 demos reachable`, exit 0.

- [ ] **Step 8: Commit**

```bash
cd "C:\Brian\02_Projects\pokemon-drop"
git add middleware.ts
git commit -m "fix: gate returns 200 not 401; access code is env-only

A 401 made link previews and corporate proxies treat the demo as dead.
The gate still gates - only the wire status changed. Removed the
hardcoded fallback so the code never ships in source."
```

---

### Task 3: Warranty Tracker seeds on first load

**Files:**
- Modify: `C:\Users\mathe\Dev\warranty-tracker\index.html`

**Interfaces:**
- Consumes: nothing from prior tasks.
- Produces: a populated dashboard on first visit; no empty state.

**Context:** The app is a single static `index.html` using localStorage. It currently renders `0 · 0 · 0 · 0` and "No items yet" on first load, which reads as broken. A "Load sample data" button exists, but visitors do not click buttons on a stranger's demo. Seed automatically when storage is empty; a real user's data is never overwritten because the seed only runs on empty.

**Verified facts (read 2026-07-23, no lookup needed):**
- Storage key is `const KEY='wt_items_v1'` (line 144).
- The seed data lives in an anonymous handler at line 243: `document.getElementById('seedBtn').onclick=()=>{...}`. There is **no named `loadSampleData` function** — do not call one.
- The handler already ends with `save(); render();`.
- The app's initial render is a bare `render();` at line 257 (last line of the script).

- [ ] **Step 1: Add the auto-seed call**

At line 257, replace:

```javascript
render();
```

with:

```javascript
// Demo: seed on first visit so the dashboard is never an empty zero-state.
// Reuses the existing seedBtn handler so the sample data lives in exactly one
// place. Only fires when storage is empty, so a returning user is never clobbered.
if(!localStorage.getItem(KEY)) document.getElementById('seedBtn').onclick();
render();
```

- [ ] **Step 2: Verify locally in a clean profile**

Open `index.html` in a private/incognito window.
Expected: stat cards show non-zero values immediately; the "No items yet" empty state does not appear.

- [ ] **Step 4: Verify a returning user is not clobbered**

In the same window: delete an item, reload.
Expected: the deleted item stays deleted — the seed does not re-run.

- [ ] **Step 5: Deploy**

```bash
cd "C:\Users\mathe\Dev\warranty-tracker"
vercel --prod --yes
```

- [ ] **Step 6: Verify live**

Run: `curl.exe -s https://warranty-tracker-azure.vercel.app | Select-String "No items yet"`
Expected: **no match** in the served HTML's initial state, or if the string exists in markup, confirm visually in an incognito browser that it is not rendered.

- [ ] **Step 7: Commit**

```bash
cd "C:\Users\mathe\Dev\warranty-tracker"
git add index.html
git commit -m "fix: seed sample data on first load so the demo is never empty

A recruiter landing on 0-0-0-0 reads the app as broken. Seeds only when
localStorage is empty, so returning users keep their data."
```

---

### Task 4: Portfolio links the demos; inventory URLs corrected

**Files:**
- Modify: `C:\Brian\02_Projects\portfolio\index.html` (Selected Work section)
- Modify: `C:\Users\mathe\AppData\Roaming\Claude\local-agent-mode-sessions\52e71c47-4a45-4526-a44e-639409b19116\67ddf914-605b-4282-ab56-f6db50fdec62\local_4631ed5c-d28f-41f4-9810-60638ae693da\outputs\MASTER_PROJECT_INVENTORY.md`

**Interfaces:**
- Consumes: the verified production aliases in Global Constraints; the working `?code=` chain from Task 2.
- Produces: a portfolio whose Selected Work entries link to reachable demos.

**Context — SCOPE CORRECTION (discovered during plan self-review):** the portfolio's
Selected Work does **not** contain cards for the four demos. It contains exactly three
editorial case studies:

- `CASE 01` — AI Job Hunter (panel states "Not yet publicly hosted")
- `CASE 02` — Brian OS
- `CASE 03` — BoomBox

Only **BoomBox** overlaps with the live demos. Warranty Tracker, Super Bowl Squares, and
Pokemon Drop Intel have no cards at all. Each card is a substantial editorial unit — role,
problem & decisions, tags, and a Verification panel with test counts and status — written in
an established voice.

Therefore this task adds a demo link **only to CASE 03 (BoomBox)**, which is a real, small
change. Authoring three new case studies is content work in an established voice and is
deferred to Plan 2. `portfolio/index.html` currently contains zero demo links, which is
exactly why the pokemon `?code=` chain never worked — the gate was designed to be entered
from the portfolio, and the portfolio never linked to it.

- [ ] **Step 1: Read CASE 03's markup**

Run: `Select-String -Path "C:\Brian\02_Projects\portfolio\index.html" -Pattern "CASE 03" -Context 2,30`
Expected: the BoomBox `<article class="case rv">` block, including its `<aside class="panel">`
with `<div class="row">` entries and a `<p class="status">`. Reuse these exact classes — do
not invent new ones.

- [ ] **Step 2: Add a demo row to CASE 03's Verification panel**

Inside BoomBox's `<aside class="panel">`, alongside the existing `<div class="row">` entries,
add:

```html
<div class="row"><span>LIVE DEMO</span><b><a href="https://boom-box-v-5.vercel.app">boom-box-v-5.vercel.app</a></b></div>
```

Match the surrounding rows' markup exactly. If the panel's `<p class="status">` claims the
project is not hosted, update that sentence to reflect that a live demo now exists.

- [ ] **Step 3: Verify the link resolves**

Run: `curl.exe -s -o NUL -w "%{http_code}\n" -L https://boom-box-v-5.vercel.app`
Expected: `200`

- [ ] **Step 4: Correct the inventory doc**

In `MASTER_PROJECT_INVENTORY.md`, replace every deployment-hash URL in the "Live / deployed" table with the production alias from Global Constraints, and add a dated note:

```markdown
> **Corrected 2026-07-23:** this table previously listed deployment-hash aliases
> (`*-<hash>-bmath8s-projects.vercel.app`). Those are protected by Vercel and
> redirect to a login wall. Only the production aliases below are public.
```

- [ ] **Step 5: Run the full verification**

Run: `powershell -File C:\Brian\02_Projects\portfolio\scripts\verify-demos.ps1`
Expected: `All 5 demos reachable`, exit 0.

- [ ] **Step 6: Commit**

```bash
cd "C:\Brian\02_Projects\portfolio"
git add index.html
git commit -m "feat: link live demos from Selected Work

The portfolio had zero demo links, which is why the pokemon ?code= chain
never worked - the gate was designed to be entered from here."
```

---

## Not in this plan (Plans 2-4)

- BoomBox login-wall bypass and Squares room-code bypass — need the demo-tier infrastructure (Plan 2).
- Shared `demo-bar.js` chrome — Plan 2.
- Warranty Tracker visual rebuild — Plan 3, and it needs its own design round first.
- Credit Repair OS / CreditForge deploys — Plan 4.
- Making `credit-repair-os` public — blocked on spec decision D2.
- LinkedIn URL — still missing from Brian; blocks the `PROJECT_BRIEF.md` definition of done.

## Acceptance criteria covered

- **AC1** (all URLs 200, no SSO) — Task 1 script, run in Tasks 2 and 4.
- **AC2** (non-empty within 3s) — Task 3 for Warranty Tracker. BoomBox/Squares remain gated until Plan 2.
- **AC8** (portfolio links all demos) — **PARTIAL.** Task 4 links BoomBox only. Warranty
  Tracker, Squares, and Pokemon have no portfolio cards; authoring them is Plan 2. LinkedIn
  still blocked on Brian.
- **AC9** (no deployment-hash URLs recorded) — Task 4 Step 4.

Not covered here: AC3, AC4, AC5, AC6, AC7, AC10 — all belong to Plans 2–4.

## Plan self-review notes (2026-07-23)

Three defects found and fixed before handoff:

1. Task 3 originally said "substitute the real key and function name found in Step 1" — a
   placeholder. Replaced with verified values (`KEY='wt_items_v1'`, seed handler at line 243)
   and exact code.
2. Task 3 referenced a `loadSampleData()` function that **does not exist**; the seed logic is
   an anonymous handler on `seedBtn`. Rewritten to reuse that handler so seed data stays in
   one place.
3. Task 4 assumed the portfolio had cards for all four demos. It has three cases, only one of
   which (BoomBox) is a demo. Scope corrected and the case-study writing deferred to Plan 2.
