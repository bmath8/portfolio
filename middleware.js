export const config = { matcher: "/((?!favicon.ico|robots.txt).*)" };

const CODE = "brian2026";
const COOKIE = "bm_access=granted";

// Recruiter-friendly gate (2026-07-06): one-click unlock via ?code= link on the
// resume (sets a cookie, then clean-redirects), or a branded code page - no more
// raw browser Basic-auth popup. Rotate CODE anytime; visitors re-enter after.
export default function middleware(request) {
  const url = new URL(request.url);
  const cookies = request.headers.get("cookie") || "";
  if (cookies.includes(COOKIE)) return;

  if (url.searchParams.get("code") === CODE) {
    url.searchParams.delete("code");
    return new Response(null, {
      status: 302,
      headers: {
        Location: url.pathname + (url.search || ""),
        "Set-Cookie": COOKIE + "; Path=/; Max-Age=2592000; SameSite=Lax",
      },
    });
  }

  const page = `<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>Brian Mathew — private preview</title>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900&family=IBM+Plex+Mono&display=swap" rel="stylesheet">
<style>body{margin:0;min-height:100vh;display:flex;align-items:center;justify-content:center;background:#f1ecdf;color:#211d17;font-family:"IBM Plex Mono",monospace}
.card{text-align:center;padding:44px 40px;max-width:440px;border:1px solid #211d17;box-shadow:6px 6px 0 #dfd8c4;background:#f1ecdf}
h1{font-family:"Fraunces",serif;font-weight:560;font-size:2.3rem;margin:0 0 6px;letter-spacing:-.01em}
h1 i{font-style:italic;color:#bf3b1f;font-weight:440}
.doc{font-size:.56rem;letter-spacing:.2em;text-transform:uppercase;color:#847b6c;margin-bottom:22px}
p{color:#4a443a;font-size:.8rem;line-height:1.7;margin:0 0 26px}
input{background:transparent;border:1px solid #211d17;color:#211d17;font-family:inherit;font-size:1rem;padding:13px 16px;width:190px;text-align:center;letter-spacing:.1em}
input:focus{outline:none;border-color:#bf3b1f}button{background:#211d17;color:#f1ecdf;border:1px solid #211d17;font-family:inherit;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;padding:14px 20px;cursor:pointer;margin-left:8px}
button:hover{background:#bf3b1f;border-color:#bf3b1f}</style></head><body><div class="card">
<h1>Operator's <i>Manual</i></h1>
<div class="doc">Doc. BM-2026-07 · restricted distribution</div>
<p>Enter the access code printed on Brian's resume or message.</p>
<form onsubmit="location.href=location.pathname+'?code='+encodeURIComponent(document.getElementById('c').value);return false">
<input id="c" placeholder="access code" autofocus autocomplete="off"><button>Enter →</button></form>
</div></body></html>`;
  return new Response(page, { status: 401, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
