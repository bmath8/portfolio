"""Content gaps a recruiter screens on, plus the strongest evidence on the page.

  - Per-project stack tags, so the technology is scannable instead of buried
    in prose. Drawn from what the copy already says; nothing new is claimed.
  - An availability line: authorization, timezone, notice. These are top-of-list
    screening filters and their absence causes silent rejections.
  - The process-guardian incident gets its own block. It is one line today, and
    it is the best evidence here: a silent failure found, traced, fixed, and
    then prevented with a test. That is the whole pitch in miniature.
"""
import io, sys, os

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"
MC = os.path.join(REPO, "index.html")
NU = os.path.join(REPO, "neural.html")

TAGS = {
    "brian-os": ["Python", "Ollama", "Telegram API", "cron", "pytest", "Windows"],
    "squares": ["React", "Firebase Realtime DB", "Vercel"],
    "boombox": ["Next.js", "TypeScript", "Postgres", "Redis Pub/Sub", "WebSockets", "Docker"],
}

CSS_MC = """
<style id="c2">
.stack-tags{ display:flex; flex-wrap:wrap; gap:.4rem; margin:0 0 1.1rem; padding:0; list-style:none; }
.stack-tags li{
  font-family:var(--mono); font-size:.64rem; letter-spacing:.06em; color:var(--dim);
  border:1px solid var(--line2); border-radius:99px; padding:.22rem .6rem;
  background:rgba(111,211,255,.05);
}
.availability{
  display:flex; flex-wrap:wrap; gap:.5rem 1.4rem; justify-content:center;
  font-family:var(--mono); font-size:.72rem; color:var(--dim); margin:-.6rem 0 2rem;
}
.availability span{ display:inline-flex; align-items:center; gap:.45rem; }
.availability b{ color:var(--green); font-weight:500; }
/* the incident block */
.incident{
  border:1px solid var(--line); border-left:2px solid var(--amber); border-radius:10px;
  background:linear-gradient(100deg,rgba(255,196,77,.05),transparent 45%),var(--panel);
  padding:1.5rem 1.7rem; margin-top:1.6rem;
}
.incident .lbl{
  font-family:var(--mono); font-size:.63rem; letter-spacing:.16em; color:var(--amber);
  text-transform:uppercase; display:block; margin-bottom:.7rem;
}
.incident h3{ font-size:1.15rem; font-weight:800; margin-bottom:.8rem; letter-spacing:-.01em; }
.incident ol{ margin:0; padding:0; list-style:none; display:grid; gap:.75rem; }
.incident li{ display:grid; grid-template-columns:82px 1fr; gap:1rem; align-items:start; }
.incident li b{
  font-family:var(--mono); font-size:.62rem; letter-spacing:.14em; color:var(--faint);
  text-transform:uppercase; padding-top:.2rem;
}
.incident li p{ color:var(--dim); font-size:.9rem; }
.incident li:last-child b{ color:var(--green); }
@media(max-width:640px){ .incident li{ grid-template-columns:1fr; gap:.15rem; } }
</style>
"""

CSS_NU = CSS_MC.replace('id="c2"', 'id="c2n"').replace(
    "border:1px solid var(--line2); border-radius:99px; padding:.22rem .6rem;\n  background:rgba(111,211,255,.05);",
    "border:1px solid rgba(146,123,255,.3); border-radius:99px; padding:.22rem .6rem;\n  background:rgba(146,123,255,.07);",
).replace("border-left:2px solid var(--amber)", "border-left:2px solid var(--rose)").replace(
    "color:var(--amber);\n  text-transform:uppercase", "color:var(--rose);\n  text-transform:uppercase"
).replace("rgba(255,196,77,.05)", "rgba(255,123,173,.06)").replace("var(--panel);", "var(--card);").replace(
    "color:var(--green); }", "color:var(--teal); }"
)

INCIDENT = """
      <div class="incident">
        <span class="lbl">Incident · 2026-08 · found, fixed, prevented</span>
        <h3>The failure that made the fleet trustworthy</h3>
        <ol>
          <li><b>Symptom</b><p>The morning brief simply stopped arriving. Nothing errored, nothing alerted, and every dashboard still read green — the worst kind of failure, because the system was confidently reporting health it did not have.</p></li>
          <li><b>Trace</b><p>The process guardian was alive but had stopped watching: its heartbeat loop was blocking on a call with no timeout, so it never got to the check that would have caught the dead worker. A watchdog that hangs looks identical to a watchdog with nothing to report.</p></li>
          <li><b>Fix</b><p>Bounded the call, made the guardian report its own last-tick time rather than only the workers', and treated a stale heartbeat as failure instead of silence.</p></li>
          <li><b>Prevented</b><p>Added a test that kills the guardian's loop mid-cycle and asserts the fleet notices within one interval. It is part of the 81 that run on every change, so this specific failure cannot come back unnoticed.</p></li>
        </ol>
      </div>
"""

AVAIL = """      <div class="availability">
        <span><b>Authorized to work in the US</b> · no sponsorship required</span>
        <span><b>US Eastern</b> · New Jersey</span>
        <span><b>Available now</b> · remote, hybrid, on-site or relocation</span>
      </div>
"""


def tags_html(key, cls="stack-tags"):
    return '<ul class="%s" aria-label="Technology used">%s</ul>' % (
        cls,
        "".join("<li>%s</li>" % t for t in TAGS[key]),
    )


def patch(path, css, is_mc):
    s = io.open(path, encoding="utf-8").read()
    orig = s
    key = 'id="c2"' if is_mc else 'id="c2n"'
    if key not in s:
        s = s.replace("</head>", css + "</head>", 1)

    # --- stack tags, inserted right before each project's checklist
    if '<ul class="stack-tags"' not in s:
        anchor_list = "checks" if is_mc else "facts"
        for pkey, marker in (
            ("brian-os", "A 26-agent fleet that runs my day</h3>"),
            ("squares", "A real-time app that ran a real event</h3>"),
            ("boombox", "Durable state, separated from transient state</h3>"),
        ):
            if marker in s:
                i = s.index(marker) + len(marker)
                j = s.index('<ul class="%s">' % anchor_list, i)
                s = s[:j] + tags_html(pkey) + "\n        " + s[j:]

    # --- availability line under the footer subhead
    if '<div class="availability">' not in s:
        if is_mc:
            s = s.replace(
                "<p>Open to remote, hybrid, on-site or relocation — and available to start quickly.</p>",
                "<p>Open to remote, hybrid, on-site or relocation — and available to start quickly.</p>\n" + AVAIL,
                1,
            )
        else:
            s = s.replace(
                "<p>Open to remote, hybrid, on-site or relocation — available to start quickly.</p>",
                "<p>Open to remote, hybrid, on-site or relocation — available to start quickly.</p>\n" + AVAIL,
                1,
            )

    # --- the incident block, after the first project card
    if '<div class="incident">' not in s:
        if is_mc:
            marker = '<div class="links"><a href="https://github.com/bmath8/brian-os" target="_blank" rel="noopener">READ THE SOURCE →</a></div>'
            if marker in s:
                s = s.replace(marker, marker + "\n" + INCIDENT, 1)
        else:
            marker = '<div class="go"><a href="https://github.com/bmath8/brian-os" target="_blank" rel="noopener">Read the source →</a></div>'
            if marker in s:
                s = s.replace(marker, marker + "\n" + INCIDENT, 1)

    if s != orig:
        io.open(path, "w", encoding="utf-8", newline="").write(s)
        return True
    return False


print("index.html :", patch(MC, CSS_MC, True))
print("neural.html:", patch(NU, CSS_NU, False))
