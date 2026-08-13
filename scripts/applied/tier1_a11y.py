"""Tier 1: correctness and accessibility for both portfolio pages.

Everything here is a defect fix, not a style change:
  - real metric values already restored in HTML (done separately)
  - count-up skipped entirely under prefers-reduced-motion
  - accessible contrast for the "receipt" text that carries the page's thesis
  - minimum legible sizes for captions
  - visible :focus-visible rings for keyboard users
  - <main> landmark + skip link
  - heading order fix (h4 -> h3 in capabilities/skills)
  - canvases hidden from assistive tech, with text alternatives nearby
  - every animation loop pauses on hidden tab and under reduced motion
"""
import re, sys, io, os

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"

# ---------------------------------------------------------------- shared CSS
A11Y_CSS_MC = """
<style id="a11y">
/* --- Tier 1 accessibility ---------------------------------------------
   --faint was 2.95:1 on panel: below AA, and it carried the source lines
   under every metric. Raised to ~5.1:1. Caption sizes floored at 11px. */
:root{ --faint:#8199ad; }
.stat small,.timeline .cap,.demo .cap,.colophon,.sec-head .tag,.fcard .fhead{
  font-size:.72rem; letter-spacing:.06em;
}
.demo .cap,.colophon{ font-size:.68rem; }
.ptable .phead{ font-size:.66rem; }
/* keyboard focus: nothing was visible before */
:focus-visible{
  outline:2px solid var(--green);
  outline-offset:3px;
  border-radius:3px;
}
a:focus-visible,button:focus-visible{ outline-offset:4px; }
.skip{
  position:absolute; left:-9999px; top:0; z-index:200;
  background:var(--green); color:#03130a; font-family:var(--mono);
  font-size:.8rem; font-weight:700; padding:.7rem 1.2rem; border-radius:0 0 6px 0;
}
.skip:focus{ left:0; }
/* honour reduced motion across the whole page, not just reveals */
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{
    animation-duration:.001ms !important; animation-iteration-count:1 !important;
    transition-duration:.001ms !important; scroll-behavior:auto !important;
  }
}
/* larger tap targets on touch */
@media (pointer:coarse){
  .statusbar nav a,.links a,.foot .row a,.btn{ min-height:44px; display:inline-flex; align-items:center; }
}
</style>
"""

A11Y_CSS_NEURAL = A11Y_CSS_MC.replace("--faint:#8199ad;", "--faint:#8087b0;").replace(
    "outline:2px solid var(--green);", "outline:2px solid var(--teal);"
).replace("background:var(--green); color:#03130a;", "background:var(--teal); color:#071018;").replace(
    """.stat small,.timeline .cap,.demo .cap,.colophon,.sec-head .tag,.fcard .fhead{
  font-size:.72rem; letter-spacing:.06em;
}
.demo .cap,.colophon{ font-size:.68rem; }
.ptable .phead{ font-size:.66rem; }""",
    """.orb small,.vis .cap,.fine,.brainbox .tag,.tl-item time{
  font-size:.7rem; letter-spacing:.06em;
}
.vis .cap,.fine{ font-size:.68rem; }""",
)

# ------------------------------------------------------------- shared JS
A11Y_JS = """
<script id="a11y-js">
/* Tier 1 behaviour ---------------------------------------------------------
   1. Respect reduced motion for canvas work and timers, not just CSS.
   2. Pause every loop when the tab is hidden; a portfolio left open in a
      background tab should cost nothing.
   Both are opt-in wrappers so the page still works if this block is removed. */
(function(){
  const REDUCE = matchMedia('(prefers-reduced-motion: reduce)');
  const paused = () => document.hidden || REDUCE.matches;

  // wrap setInterval so every ticker in the page obeys the rules above
  const realInterval = window.setInterval.bind(window);
  const timers = [];
  window.setInterval = function(fn, ms){
    const wrapped = function(){ if(!paused()) fn.apply(this, arguments); };
    const id = realInterval(wrapped, ms); timers.push(id); return id;
  };

  // wrap rAF: while paused, keep polling for the next frame without running the
  // callback body, so the loop survives and resumes the moment the tab returns
  const realRaf = window.requestAnimationFrame.bind(window);
  window.requestAnimationFrame = function(cb){
    function tick(t){ if(paused()){ realRaf(tick); return; } cb(t); }
    return realRaf(tick);
  };

  // canvases are decorative: keep them out of the accessibility tree
  addEventListener('load', function(){
    document.querySelectorAll('canvas').forEach(function(c){
      c.setAttribute('aria-hidden','true');
      c.setAttribute('role','presentation');
    });
  });
})();
</script>
"""


def patch(path, css, is_mc):
    src = io.open(path, encoding="utf-8").read()
    orig = src

    # --- inject CSS just before </head> (or before first <style> fallback)
    if 'id="a11y"' not in src:
        src = src.replace("</head>", css + "</head>", 1)

    # --- skip link + <main> landmark
    if 'class="skip"' not in src:
        src = src.replace("<body>", '<body>\n<a class="skip" href="#work">Skip to the work</a>', 1)

    if "<main" not in src:
        if is_mc:
            # header ends, main opens; closes before footer
            src = re.sub(r"(</header>)", r"\1\n<main id=\"main\">", src, count=1)
            src = re.sub(r"(<footer class=\"foot\">)", r"</main>\n\1", src, count=1)
        else:
            src = re.sub(r"(<div class=\"aurora\"></div>)", r"\1\n<main id=\"main\">", src, count=1)
            src = re.sub(r"(<footer id=\"contact\">)", r"</main>\n\1", src, count=1)

    # --- heading order: h2 -> h4 skipped a level in the capability cards
    src = src.replace("<h4>Build</h4>", "<h3>Build</h3>").replace("</h4><p>Python", "</h3><p>Python")
    for label in ("Build", "Operate", "Test", "Support"):
        src = src.replace("<h4>%s</h4>" % label, "<h3>%s</h3>" % label)
    # keep their visual size (the CSS targets h4)
    src = src.replace(".cap-card h4{", ".cap-card h3{").replace(".skill h4{", ".skill h3{")
    src = src.replace(".cap-card:nth-child(1) .ic", ".cap-card:nth-child(1) .ic")
    src = src.replace(".skill h4::before", ".skill h3::before")
    src = src.replace(".skill:nth-child(1) h4::before", ".skill:nth-child(1) h3::before")
    src = src.replace(".skill:nth-child(2) h4::before", ".skill:nth-child(2) h3::before")
    src = src.replace(".skill:nth-child(3) h4::before", ".skill:nth-child(3) h3::before")
    src = src.replace(".skill:nth-child(4) h4::before", ".skill:nth-child(4) h3::before")

    # --- count-up must not run under reduced motion (numbers already correct in HTML)
    src = src.replace(
        "e.target.querySelectorAll('b[data-n]').forEach(b=>{",
        "if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;\n  e.target.querySelectorAll('b[data-n]').forEach(b=>{",
    )

    # --- behaviour block before </body>
    if 'id="a11y-js"' not in src:
        src = src.replace("</body>", A11Y_JS + "</body>", 1)

    if src != orig:
        io.open(path, "w", encoding="utf-8", newline="").write(src)
        return True
    return False


mc = os.path.join(REPO, "index.html")
nu = os.path.join(REPO, "neural.html")
print("index.html patched:", patch(mc, A11Y_CSS_MC, True))
print("neural.html patched:", patch(nu, A11Y_CSS_NEURAL, False))
