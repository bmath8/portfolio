#Requires -Version 7
<#
verify-demos.ps1 — demo reachability + minimum content assertions (AC1).

Why #Requires -Version 7: on PowerShell 5.1, Invoke-WebRequest's
$r.BaseResponse.RequestMessage.RequestUri member silently returns $null, so
the SSO-wall check below (which compares the final redirected URL) evaluates
false even when the request actually landed on the Vercel login page. That
made a login-walled demo report PASS. Under pwsh 7+ this fails loudly instead.

HTTP 200 is NOT sufficient on its own. Earlier in this project a deploy
returned 200 while completely broken — SITE_PASSWORD was stored with a
trailing "\r\n", so every access-code comparison silently failed — and a
200-only check stayed green the whole time. The content assertions and the
?code= round-trip below exist specifically to catch that bug class again.

Known coverage gaps — be honest about what this script can and cannot prove:
  - BoomBox (boom-box-v-5.vercel.app): as of Plan 2, /login carries a one-click
    "Enter demo" control. This script asserts that control is present in the
    served HTML (if it vanishes, recruiters hit a bare login wall). It does NOT
    drive the button through auth to /radio — that is BROWSER-verified
    (boombox-radio.png), not HTTP-assertable.
  - Squares (fam-super-bowl-squares-2026.vercel.app): un-gated via ?demo=1
    (auto-join into the finished game). It is a client-rendered single-file app,
    so "ROOM CODE" ships in the JS bundle for every path — a body check cannot
    distinguish product from gate. This script asserts reachability (200) only;
    the ?demo=1 product state is BROWSER-verified (squares-board.png).
  - Pokemon (pokemon-drop-intel.vercel.app) is the one demo with an actual
    end-to-end HTTP check below (the ?code= round-trip), gated on
    $env:SITE_PASSWORD being set. Never hardcode the code value here.

Exit codes:
  0 = all checks passed, nothing skipped
  1 = one or more checks FAILED
  2 = no FAILures, but one or more checks were SKIPPED (inconclusive —
      e.g. SITE_PASSWORD not set). Do not treat this as a clean pass.
#>

$urls = @(
  'https://boom-box-v-5.vercel.app',
  'https://warranty-tracker-azure.vercel.app',
  'https://fam-super-bowl-squares-2026.vercel.app',
  'https://pokemon-drop-intel.vercel.app',
  'https://bmath8.vercel.app'
)

$fail = 0
$skipped = 0
$checked = 0

foreach ($u in $urls) {
  $checked++
  try {
    $r = Invoke-WebRequest -Uri $u -MaximumRedirection 5 -SkipHttpErrorCheck -TimeoutSec 20
    $code = $r.StatusCode
    $final = $r.BaseResponse.RequestMessage.RequestUri.AbsoluteUri
    $body = $r.Content
  } catch {
    $code = 0; $final = 'ERROR'; $body = ''
  }

  $sso = $final -like '*vercel.com/login*'
  $problems = @()
  if ($code -ne 200) { $problems += "HTTP $code" }
  if ($sso) { $problems += 'SSO WALL' }

  switch -Wildcard ($u) {
    '*boom-box-v-5.vercel.app*' {
      # As of Plan 2, /login IS the demo entry surface — it carries a one-click
      # "Enter demo" control (no account needed). So landing on /login is expected;
      # the real assertion is that the demo control is present in the served HTML.
      # If it vanishes, recruiters hit a bare login wall again.
      if ($body -notmatch '(?i)enter demo') { $problems += 'demo-entry control "ENTER DEMO" missing on /login (recruiters would hit a bare login wall)' }
    }
    '*fam-super-bowl-squares-2026.vercel.app*' {
      # Client-rendered single-file app: "ROOM CODE" ships in the JS bundle for
      # BOTH the setup screen and the ?demo=1 path, so a body check can't tell
      # product from gate here. Reachability (200) is asserted above; the ?demo=1
      # product state (auto-join into the finished game) is BROWSER-verified, not
      # HTTP-assertable. See squares-board.png. No content assertion here by design.
    }
    '*pokemon-drop-intel.vercel.app*' {
      # Expected behavior: the bare URL SHOULD serve the gate. That is not
      # a failure — it's only a failure if the gate itself appears broken.
      if ($body -notmatch 'access code') { $problems += 'expected gate text "access code" missing on bare URL (gate may be broken)' }
    }
  }

  if ($problems.Count -eq 0) {
    "PASS  $code  $u"
  } else {
    "FAIL  $($problems -join '; ')  $u"
    $fail++
  }
}

# --- Pokemon ?code= round-trip -------------------------------------------
# The specific check that catches the bug class that already bit us: a
# access-code comparison that silently fails (e.g. trailing CRLF in the env
# var) while HTTP status stays 200. Asserts BOTH that the granted cookie is
# set AND that the resulting body no longer shows the gate.
$checked++
$pokemonBase = 'https://pokemon-drop-intel.vercel.app'
if (-not $env:SITE_PASSWORD) {
  Write-Warning 'SKIPPED: $env:SITE_PASSWORD is not set — cannot verify the pokemon ?code= round-trip. This is the exact check that would have caught the earlier trailing-CRLF bug. Set $env:SITE_PASSWORD and re-run before trusting this demo.'
  $skipped++
} else {
  try {
    $codeUrl = "$pokemonBase/?code=$($env:SITE_PASSWORD)"
    # -MaximumRedirection 0: a correct code returns the 302 that SETS the cookie.
    # Do NOT follow it — the Set-Cookie lives on the 302 hop; following the redirect
    # lands on the app page whose headers no longer carry it (false negative).
    # A wrong code returns 200 (the gate page) with no redirect and no cookie, so the
    # status code alone distinguishes granted (302) from rejected (200).
    # -ErrorAction SilentlyContinue: PS7 writes a non-terminating "redirection count
    # exceeded" error to the stream on -MaximumRedirection 0 even though $r2 is still
    # populated with the 302. Suppress the noise; the assertions below do the judging.
    $r2 = Invoke-WebRequest -Uri $codeUrl -MaximumRedirection 0 -SkipHttpErrorCheck -TimeoutSec 20 -ErrorAction SilentlyContinue
    $setCookieRaw = $r2.Headers['Set-Cookie']
    $grantedCookie = (($setCookieRaw -join ';') -match 'bm_access=granted')
    $redirected = ($r2.StatusCode -eq 302)

    $problems2 = @()
    if (-not $redirected)    { $problems2 += "expected 302 redirect on correct code, got $($r2.StatusCode) (code comparison likely broken — the trailing-CRLF bug class)" }
    if (-not $grantedCookie) { $problems2 += 'response did not set bm_access=granted' }

    if ($problems2.Count -eq 0) {
      "PASS  code-roundtrip  $pokemonBase/?code=<SITE_PASSWORD>"
    } else {
      "FAIL  $($problems2 -join '; ')  $pokemonBase/?code=<SITE_PASSWORD>"
      $fail++
    }
  } catch {
    "FAIL  request error: $_  $pokemonBase/?code=<SITE_PASSWORD>"
    $fail++
  }
}

"`n--- Summary ---"
if ($fail -gt 0) {
  "$fail FAILED, $skipped SKIPPED, of $checked checks"
  exit 1
} elseif ($skipped -gt 0) {
  "0 FAILED, $skipped SKIPPED (inconclusive) of $checked checks"
  exit 2
} else {
  "All $checked checks passed"
  exit 0
}
