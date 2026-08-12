# GitHub Support request — garbage-collect unreachable objects

**Status: NOT YET SENT.** Only Brian can file this — it needs the account that owns the repo.

Independently confirmed on Brian's machine, 2026-08-12, which is the measurement that matters
because it runs outside this project's network:

```
200  cd2746e   <- blob still served
200  24e1549   <- blob still served
404  main      <- control passes, current tip is clean
```

The rewrite is holding — `main` is clean. The two unreachable commits are what GC has to clear.

Support: https://support.github.com/contact → "Repository management".

---

## Copy-paste body

> **Subject:** Purge unreachable objects after history rewrite — bmath8/portfolio
>
> I rewrote the history of my public repository `bmath8/portfolio` on 2026-08-12 using
> `git filter-repo` to remove a file that was included under a licence I could not comply with
> (`vendor/mesh/brain-mni.bin`, AGPL-3.0). The rewritten history was force-pushed to every branch
> that contained it — `main`, `hero-v17`, and one feature branch.
>
> The file is gone from all branch tips and from all reachable history, and the old commits are
> no longer served over the git protocol. However, the blob is **still publicly downloadable** by
> commit SHA via `raw.githubusercontent.com`:
>
> - `https://raw.githubusercontent.com/bmath8/portfolio/cd2746e/vendor/mesh/brain-mni.bin`
> - `https://raw.githubusercontent.com/bmath8/portfolio/24e1549/vendor/mesh/brain-mni.bin`
>
> Both currently return HTTP 200 with 2,703,404 bytes.
>
> Please run garbage collection on the repository to purge the unreachable objects, so that these
> URLs return 404. Please also confirm whether any forks or network caches retain the object.
>
> Thank you.

---

## How to confirm it worked

**All three must return 404.** The third already does — it is the control proving the current
tip is clean, so if it ever returns anything else the test itself is wrong.

### Windows PowerShell — use this one

⚠️ **`curl` in Windows PowerShell 5.1 is an alias for `Invoke-WebRequest`, not curl.** The bash
flags below get parsed as PowerShell parameters (`-s` becomes `-SessionVariable`) and it fails
with "Missing an argument for parameter 'SessionVariable'". Call `curl.exe` explicitly, and use
`NUL` rather than `/dev/null`:

```powershell
@("cd2746e","24e1549","main") | ForEach-Object {
  $sha = $_                                    # see note below - do not use $_ in the catch
  $u = "https://raw.githubusercontent.com/bmath8/portfolio/$sha/vendor/mesh/brain-mni.bin"
  try   { "$((Invoke-WebRequest $u -Method Head -UseBasicParsing).StatusCode)  $sha" }
  catch { "$($_.Exception.Response.StatusCode.value__)  $sha" }
}
```

> **Why `$sha` and not `$_`:** inside `catch`, PowerShell rebinds `$_` to the *error record*, so
> using it there prints the exception message instead of the commit. Right now only one URL 404s
> so it barely shows — but **after Support runs GC all three will 404**, and the whole point of
> the test is knowing which SHA each line refers to. Capture the loop variable first.

### bash / macOS / Linux

```bash
for r in cd2746e 24e1549 main; do
  curl -s -o /dev/null -w "%{http_code}  $r\n" \
    "https://raw.githubusercontent.com/bmath8/portfolio/$r/vendor/mesh/brain-mni.bin"
done
```

## Why the rewrite alone was not enough

GitHub retains unreachable objects until it garbage-collects, and serves them by SHA over HTTPS.
Testing only the git protocol produced a **false all-clear** — `git fetch <sha>` correctly
answered "not our ref" while `raw.githubusercontent.com` was still serving the file. That is the
same shape as an earlier mistake in this project, where fixing the Vercel serving path was
mistaken for fixing the repository. Test the path the exposure was actually found on.
