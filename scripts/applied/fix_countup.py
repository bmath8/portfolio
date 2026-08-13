import io, re
OLD = """  if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  e.target.querySelectorAll('b[data-n]').forEach(b=>{
    const n=+b.dataset.n,suf=b.dataset.suffix||'';const t0=performance.now();
    (function f(t){const p=Math.min((t-t0)/1200,1);b.textContent=Math.round(EASE(p)*n)+suf;if(p<1)requestAnimationFrame(f)})(t0);
  });"""
NEW = """  e.target.querySelectorAll('b[data-n]').forEach(b=>{
    // the markup already holds the true value, so it is correct with JS off.
    // animate only as an enhancement, and guarantee we land back on the truth.
    const truth=b.dataset.final||(b.dataset.final=b.textContent);
    const settle=()=>{b.textContent=truth};
    if(document.hidden||matchMedia('(prefers-reduced-motion: reduce)').matches){settle();return}
    const n=+b.dataset.n,suf=b.dataset.suffix||'';const t0=performance.now();
    setTimeout(settle,2000);                       // safety net, never strand on 0
    document.addEventListener('visibilitychange',settle,{once:true});
    (function f(t){
      const p=Math.min((t-t0)/1200,1);
      b.textContent=p<1?(Math.round(EASE(p)*n)+suf):truth;
      if(p<1)requestAnimationFrame(f);
    })(t0);
  });"""
for path in (r"C:\Brian\02_Projects\portfolio\index.html", r"C:\Brian\02_Projects\portfolio\neural.html"):
    s = io.open(path, encoding="utf-8").read()
    if NEW in s: print(path, "already"); continue
    assert OLD in s, "count-up block not found in " + path
    s = s.replace(OLD, NEW, 1)
    io.open(path,"w",encoding="utf-8",newline="").write(s)
    print(path, "count-up made fail-safe")
