"""Take three.min.js (589 KB) off Neural's critical path.

Three changes, in order of how much they save:

  1. The brain becomes a named initialiser instead of an IIFE that runs on
     parse, and three.js is fetched only when the canvas is close to the
     viewport. Someone who bounces never pays for it.
  2. It is never fetched at all for visitors who ask for reduced motion, or
     whose browser has no WebGL - both previously downloaded the whole library
     to render nothing.
  3. Point counts scale down on small or low-density screens, where the full
     6,000-point cloud was the most expensive thing on the page.

The page keeps working with the loader removed: initBrain is a plain function.
"""
import io, re, sys

P = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio\neural.html"
s = io.open(P, encoding="utf-8").read()
nl = "\r\n" if "\r\n" in s else "\n"

# ---------------------------------------------------------------- 1. unwrap
START = "(function(){" + nl + "  const canvas=document.getElementById('brain');"
assert START in s, "brain IIFE opening not found"
i0 = s.index(START)
i1 = s.index("/* ============ fleet routing viz v3 ============ */")
block = s[i0:i1]

# the block ends with the IIFE close: "  })();" on its own line, last occurrence
close_idx = block.rindex("})();")
new_block = ("function initBrain(){" + nl + "  const canvas=document.getElementById('brain');"
             + block[len(START):close_idx] + "}" + nl + nl)
s = s[:i0] + new_block + s[i1:]

# ------------------------------------------------- 2. adaptive point counts
s = s.replace(
    "  root.add(buildCloud(4200,cortexPoint,0.05,0.75));\n"
    "  root.add(buildCloud(900,cerebellumPoint,0.045,0.7));\n"
    "  root.add(buildCloud(220,stemPoint,0.045,0.65));".replace("\n", nl),
    ("  // a phone does not need six thousand points to read as a brain" + nl +
     "  const DENSITY = (innerWidth < 820 || devicePixelRatio < 1.5) ? 0.45 : 1;" + nl +
     "  const q = n => Math.round(n * DENSITY);" + nl +
     "  root.add(buildCloud(q(4200),cortexPoint,0.05,0.75));" + nl +
     "  root.add(buildCloud(q(900),cerebellumPoint,0.045,0.7));" + nl +
     "  root.add(buildCloud(q(220),stemPoint,0.045,0.65));"),
    1,
)
s = s.replace(
    "const halo=buildCloud(700,()=>cortexPoint().multiplyScalar(1.07),0.09,0.1);root.add(halo);",
    "const halo=buildCloud(q(700),()=>cortexPoint().multiplyScalar(1.07),0.09,0.1);root.add(halo);",
    1,
)

# ------------------------------------------------------- 3. drop the eager tag
s = s.replace('<script src="/vendor/three.min.js"></script>' + nl, "", 1)
s = s.replace('<script src="/vendor/three.min.js"></script>', "", 1)

# ------------------------------------------------------------- 4. the loader
LOADER = """
<script id="brain-loader">
(function(){
  const canvas=document.getElementById('brain'); if(!canvas) return;
  const box=canvas.parentElement;

  function webgl(){
    try{ return !!document.createElement('canvas').getContext('webgl'); }catch(e){ return false; }
  }
  // reduced motion or no WebGL: never fetch the library at all
  if(matchMedia('(prefers-reduced-motion: reduce)').matches || !webgl()){
    canvas.style.display='none';
    box.classList.add('brain-off');
    return;
  }

  let started=false;
  function start(){
    if(started) return; started=true;
    const s=document.createElement('script');
    s.src='/vendor/three.min.js';
    s.onload=function(){
      box.classList.remove('brain-loading');
      try{ initBrain(); }catch(e){ canvas.style.display='none'; box.classList.add('brain-off'); }
    };
    s.onerror=function(){ canvas.style.display='none'; box.classList.add('brain-off'); };
    document.head.appendChild(s);
  }

  box.classList.add('brain-loading');
  // fetch as soon as the canvas is anywhere near the viewport
  if('IntersectionObserver' in window){
    const io=new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ io.disconnect(); start(); } });
    },{rootMargin:'300px'});
    io.observe(canvas);
  } else { start(); }
  // and never later than first idle, so it is ready before anyone scrolls to it
  (window.requestIdleCallback||function(f){setTimeout(f,1200)})(start);
})();
</script>
"""

LOADER_CSS = """
<style id="brain-loader-css">
/* placeholder while the library is in flight, and a graceful empty state when
   the brain is deliberately not loaded (reduced motion, or no WebGL) */
.brainbox.brain-loading::after{
  content:"initialising cortex\\2026";
  position:absolute; left:50%; top:48%; transform:translate(-50%,-50%);
  font-family:var(--mono); font-size:.68rem; letter-spacing:.16em; color:var(--faint);
  animation:bl 1.6s ease-in-out infinite;
}
@keyframes bl{ 50%{ opacity:.35 } }
.brainbox.brain-off .tag{ display:none; }
.brainbox.brain-off::after{
  content:"26 scheduled agents \\00B7 the fleet is listed in full below";
  display:block; text-align:center; padding:3.5rem 1rem;
  font-family:var(--mono); font-size:.72rem; letter-spacing:.1em; color:var(--dim);
  border:1px dashed var(--line); border-radius:16px;
}
</style>
"""

if 'id="brain-loader-css"' not in s:
    s = s.replace("</head>", LOADER_CSS + "</head>", 1)
if 'id="brain-loader"' not in s:
    s = s.replace("</body>", LOADER + "</body>", 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("three.js deferred; brain init is now a named function; density adapts")
