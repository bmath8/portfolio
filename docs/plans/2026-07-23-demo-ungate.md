# Demo Un-gate Implementation Plan (Plan 2 of 4)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax.

**Goal:** Let a recruiter reach the actual product in BoomBox and Super Bowl Squares in one click — no login, no name, no room code — while real auth stays intact underneath.

**Architecture:** Neither app gets its real auth removed. Squares gains a `?demo=1` URL path that auto-joins the finished public game as a guest. BoomBox gains a one-click "Enter demo" button on its existing (good) login screen that signs in with the existing demo account. The verification script is extended so each newly un-gated demo is asserted as a *product*, not a gate.

**Tech stack:** Squares — single `index.html` (React UMD + htm + Firebase RTDB). BoomBox — Next.js App Router + Supabase auth, deployed via git integration.

## Global Constraints

- Real authentication paths are NOT removed or weakened. Demo entry is additive.
- No secret committed. BoomBox demo creds (`demo@boombox.app` / `BoomBoxDemo2026`) are a
  deliberately-public demo account — acceptable in client source, same posture as the Pokemon
  gate. Do not treat them as secrets, but do not scatter them either — one constant.
- Canonical Squares working copy is **`C:\Users\mathe\Dev\fam-super-bowl-squares-2026`** (Vercel-
  linked, newer HEAD `c65cbb8`). The `C:\Brian\02_Projects\` clone is STALE — do not edit it.
- No visual redesign in this plan. BoomBox and Warranty full redesigns are their own later design
  rounds. This plan only un-gates.
- Every deploy stops for Brian's approval (standing rule from Plan 1).
- Verified production aliases unchanged from Plan 1.

## Open decision — MUST resolve before Task 2 executes

**BoomBox has a deliberate Redis rate limiter** (`RATE_LIMITING.md`, `REDIS_RATE_LIMIT_MIGRATION.md`).
The final review of Plan 1 observed it returning HTTP 429 after ~12 requests/IP with a 15-min
lockout. Recruiters on shared corporate egress IPs, plus link-preview bots, can trip it before a
human clicks. One-click demo entry makes this WORSE (each click is a real auth round-trip).
Options, for Brian:
- (a) Exempt the demo account / demo path from the limiter.
- (b) Raise the limit and lengthen the window for the login+demo routes only.
- (c) Accept as-is and document the risk.
Recommendation: (a) — scoped exemption for the demo flow, real abuse protection intact elsewhere.
This decision shapes Task 2's Step set; do not start Task 2 until it is made.

---

### Task 1: Squares one-click demo entry

**Files:**
- Modify: `C:\Users\mathe\Dev\fam-super-bowl-squares-2026\index.html` (`SetupScreen`, ~line 870-880)

**Interfaces:**
- Produces: visiting `…/?demo=1` auto-joins room `MAIN` as a guest, showing the finished LX game,
  with no name entry.

**Context (verified 2026-07-23):** `SetupScreen` (line 870) holds `name` and `room` (room already
defaults to `MAIN` from `?room=`). `go()` (line 875) blocks on empty name (`if (!n) return`) then
calls `onJoin(n, room…)`. The only real barrier is the required name. The finished game already
lives in Firebase's `MAIN` room. This is a single-file, client-only change.

- [ ] **Step 1: Add a demo auto-join effect**

In `SetupScreen`, immediately after the `go` definition (line 880), add:

```javascript
      // Demo: ?demo=1 auto-joins the finished public game as a guest — no name gate.
      useEffect(() => {
        const p = new URLSearchParams(window.location.search);
        if (p.get("demo") === "1") {
          onJoin("Guest (demo)", (p.get("room") || "MAIN").toUpperCase());
        }
      }, []);
```

Confirm `useEffect` is in scope (the file uses React UMD; other components use it — e.g. the
countdown hook). If `React.useEffect` must be qualified, match the file's existing convention.

- [ ] **Step 2: Verify locally**

Open `index.html?demo=1` in a browser. Expected: the setup screen does not block; the app lands
directly in the MAIN room showing the finished Seahawks–Patriots board, no typing required.
Open `index.html` (no param). Expected: the normal name/room setup screen still appears.

- [ ] **Step 3: Commit (canonical clone only)**

```bash
cd "C:\Users\mathe\Dev\fam-super-bowl-squares-2026"
git add index.html
git commit -m "feat: ?demo=1 auto-joins the finished public game (recruiter demo entry)"
```

- [ ] **Step 4: Reconcile the stale clone**

Record in the ledger that `C:\Brian\02_Projects\fam-super-bowl-squares-2026` (HEAD `ece7261`) is
behind the canonical Dev clone. Do NOT edit or deploy from it. Recommend to Brian: delete it, or
`git pull` it to match, so future sessions don't touch the wrong copy. (No code action this task.)

---

### Task 2: BoomBox one-click demo entry + login-page cleanup

**Files:**
- Modify: `C:\Brian\02_Projects\boombox-v5\frontend\src\app\login\page.tsx`
- Modify: `C:\Brian\02_Projects\boombox-v5\frontend\src\components\boombox\BoomboxFrame.tsx` (add a demo button to the existing frame)
- Possibly modify: the rate-limit config identified by the Open Decision above.

**Interfaces:**
- Consumes: existing `handleLogin(email, password)` in `login/page.tsx:22`.
- Produces: a visible "Enter demo" control on the login screen that calls
  `handleLogin("demo@boombox.app", "BoomBoxDemo2026")` and lands on `/radio`.

**Context (verified 2026-07-23):** `LoginPage` (login/page.tsx:9) renders `<BoomboxFrame onLogin={handleLogin} onSpotifyLogin={…} isLoading={…} />`. `handleLogin` (line 22) already does
`signInWithPassword` then routes to `/radio` on success. Adding demo entry = a thin wrapper +
one button in `BoomboxFrame`. **Do NOT rebuild the frame — the skeuomorphic design is good and its
redesign is a separate later round.**

Also present and worth fixing while here (adjacent cleanup, same file):
- Lines 23-25, 34, 41, 53, 61: `console.log` of auth internals (email, password length, the
  supabase client, sign-in results). Debug logging of credentials in a production client bundle.
- Lines 109-112: a `BUILD v4` marker whose own comment says "remove after verifying deployment."

- [ ] **Step 1: Add a demo constant and handler in `login/page.tsx`**

Near the top of `LoginPage`, add:

```typescript
    const DEMO_EMAIL = "demo@boombox.app";
    const DEMO_PASSWORD = "BoomBoxDemo2026";
    const handleDemoLogin = () => handleLogin(DEMO_EMAIL, DEMO_PASSWORD);
```

Pass `onDemoLogin={handleDemoLogin}` to `<BoomboxFrame … />`.

- [ ] **Step 2: Add the demo button in `BoomboxFrame.tsx`**

Read `BoomboxFrame.tsx` first to match its styling system exactly. Add an optional
`onDemoLogin?: () => void` prop and render a clearly-labelled "▶ Enter demo — no account needed"
control within the existing frame (near the login CTA). Match existing classes; introduce no new
design language. Guard: only render it when the prop is provided.

- [ ] **Step 3: Remove credential debug logging and the BUILD marker**

In `login/page.tsx`, delete the `console.log` lines that print auth details (23-25, 34, 41, 53,
61) and the `BUILD v4` marker block (109-112). Leave genuine `console.error` handlers.

- [ ] **Step 4: Exempt the demo flow from the auth limiter (Brian chose: exempt)**

**Root cause (verified 2026-07-23):** `frontend/src/middleware.ts:15-23` runs `redisAuthLimiter`
on EVERY request to `/login` and `/auth`, including plain GET page loads. `redisAuthLimiter`
(`lib/redis-rate-limit.ts:249-253`) is **max 5 / 15 min, keyed by IP**. So 5 page views from one
IP (two people behind a corporate NAT, or Slack+LinkedIn+Gmail link-preview bots) = a 15-minute
429 lockout. The real sign-in runs client→Supabase directly and never passes through this
middleware, so the limiter provides ~zero brute-force protection here while breaking the demo.

**Fix — apply the auth limiter only to mutating methods, not GET navigations.** In
`middleware.ts`, change the guard at line 15 from:

```typescript
    if (request.nextUrl.pathname.startsWith('/auth') || request.nextUrl.pathname === '/login') {
```

to:

```typescript
    // Only throttle mutating auth requests, not GET page loads. A login-screen
    // navigation is not a brute-force attempt; rate-limiting it locked out demo
    // traffic (5/15min/IP) while providing no real protection — the actual sign-in
    // goes client->Supabase, never through here.
    if (request.method !== 'GET' && (request.nextUrl.pathname.startsWith('/auth') || request.nextUrl.pathname === '/login')) {
```

Leave `redisApiLimiter` (API routes) and the Spotify/health limiters untouched — those guard real
server endpoints. Do NOT delete the limiter or its tests; only narrow the middleware guard.
If `lib/__tests__/rate-limit.test.ts` asserts GET /login is limited, update that expectation to
match the corrected behavior and note it in the report.

- [ ] **Step 5: Build locally**

```bash
cd "C:\Brian\02_Projects\boombox-v5\frontend"
npm install --include=dev
npm run build
```
Expected: exit 0, `/login` route compiles.

- [ ] **Step 6: Commit** (branch `demo-unblock`, do not push)

```bash
cd "C:\Brian\02_Projects\boombox-v5"
git add frontend/src/app/login/page.tsx frontend/src/components/boombox/BoomboxFrame.tsx
git commit -m "feat: one-click demo entry on BoomBox login; drop credential debug logs"
```

---

### Task 3: Extend verify-demos.ps1 to assert the un-gated demos

**Files:**
- Modify: `C:\Brian\02_Projects\portfolio\scripts\verify-demos.ps1`

**Context:** Plan 1 left BoomBox (→`/login`) and Squares (`ROOM CODE`) correctly FAILing the
product assertion. Once un-gated, those assertions must be updated to reflect the new reality:
the demo *entry point* reaches a product.

- [ ] **Step 1: Update assertions**
  - Squares: `…/?demo=1` — final rendered state must NOT be the setup screen. Since the app is
    client-rendered, an HTTP body check is insufficient; assert the `?demo=1` URL returns 200 and
    document that full confirmation is the browser check in Step 2. Do not fake coverage.
  - BoomBox: the bare `/login` is expected (it is the demo entry surface); assert it returns 200
    and its body contains the demo-entry control text. Do NOT assert past auth over HTTP.
  - Add a header note: these two are browser-confirmed, not fully HTTP-assertable.

- [ ] **Step 2: Browser-verify both** (Playwright), screenshot each landed product state.

- [ ] **Step 3: Commit.**

---

## Not in this plan (Plans 3-4 and design rounds)

- **BoomBox frontend redesign** — Brian wants it upgraded with current design principles. Its own
  reference-driven design round, then a plan. NOT this plan.
- **Warranty Tracker visual rebuild** — approved earlier; its own design round.
- **Credit Repair OS + CreditForge** deploys — Plan 4.
- Portfolio case-study cards for Warranty / Squares / Pokemon — content work, later.
- Making `credit-repair-os` public — spec D2, still needs explicit approval.
- LinkedIn URL — still missing; blocks the portfolio definition of done.

## Acceptance criteria

- **AC-P2-1** `…/fam-super-bowl-squares-2026.vercel.app/?demo=1` lands directly in the finished
  game with no name entry (browser-verified, screenshot).
- **AC-P2-2** BoomBox `/login` shows a one-click demo control that reaches `/radio` with the
  seeded demo account (browser-verified, screenshot).
- **AC-P2-3** Both apps' normal auth still works unchanged.
- **AC-P2-4** No `console.log` of credentials remains in `login/page.tsx`; BUILD marker gone.
- **AC-P2-5** The demo flow survives >12 rapid requests from one IP without a 15-min lockout
  (verifies the rate-limit decision actually took).
- **AC-P2-6** `verify-demos.ps1` reflects the new reality without faking client-render coverage.
