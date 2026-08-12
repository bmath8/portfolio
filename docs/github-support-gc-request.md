# GitHub Support request — garbage-collect unreachable objects

**Status: NOT YET SENT.** Re-verified 2026-08-12: both SHAs below still return **HTTP 200**.
Only Brian can file this — it needs the account that owns the repo.

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

Re-run these. **All three must be 404** — the third already is, and is the control showing the
current tip is clean.

```bash
curl -s -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/bmath8/portfolio/cd2746e/vendor/mesh/brain-mni.bin
curl -s -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/bmath8/portfolio/24e1549/vendor/mesh/brain-mni.bin
curl -s -o /dev/null -w "%{http_code}\n" https://raw.githubusercontent.com/bmath8/portfolio/main/vendor/mesh/brain-mni.bin
```

## Why the rewrite alone was not enough

GitHub retains unreachable objects until it garbage-collects, and serves them by SHA over HTTPS.
Testing only the git protocol produced a **false all-clear** — `git fetch <sha>` correctly
answered "not our ref" while `raw.githubusercontent.com` was still serving the file. That is the
same shape as an earlier mistake in this project, where fixing the Vercel serving path was
mistaken for fixing the repository. Test the path the exposure was actually found on.
