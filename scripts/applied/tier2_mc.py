import io, re
P = r"C:\Brian\02_Projects\portfolio\index.html"
s = io.open(P, encoding="utf-8").read()

# 1. lift the whole fleet section out
m = re.search(r'<!-- FLEET -->.*?</section>\n', s, re.S)
fleet = m.group(0)
s = s.replace(fleet, "", 1)

# 2. drop a compact live strip where the fleet used to sit (right under the metrics)
strip = '''
<!-- COMPACT FLEET STRIP -->
<div class="wrap">
  <a class="fleetstrip rv" href="#fleet">
    <span class="fs-live"><span class="dot"></span>FLEET</span>
    <span class="fs-lane" id="fsLane"></span>
    <span class="fs-next">NEXT <b id="fsNext">system-watchdog</b> <i id="fsIn">20:00</i></span>
    <span class="fs-go">OPEN THE INSTRUMENT &darr;</span>
  </a>
</div>
'''
s = s.replace('<!-- WORK -->', strip + '\n<!-- WORK -->', 1)

# 3. re-insert the full fleet section AFTER the work section
work_end = s.index('<!-- CAPABILITIES -->')
s = s[:work_end] + fleet + "\n" + s[work_end:]

# 4. styles for the strip + a taller, better-proportioned hero
css = '''
<style id="t2">
/* --- compact fleet strip: the proof, one line, above the fold ------------- */
.fleetstrip{
  display:grid; grid-template-columns:auto 1fr auto auto; gap:1.4rem; align-items:center;
  margin-top:1.1rem; padding:.85rem 1.2rem; border:1px solid var(--line); border-radius:10px;
  background:linear-gradient(90deg,rgba(65,230,147,.05),transparent 40%),var(--panel);
  font-family:var(--mono); font-size:.72rem; color:var(--dim);
  transition:border-color .3s var(--ease), transform .3s var(--ease);
}
.fleetstrip:hover{ border-color:var(--green); transform:translateY(-2px); }
.fs-live{ display:inline-flex; align-items:center; gap:.5rem; color:var(--green); letter-spacing:.16em; }
.fs-lane{ display:flex; align-items:flex-end; gap:3px; height:22px; overflow:hidden; }
.fs-lane i{ width:3px; border-radius:1px; background:var(--line2); }
.fs-lane i.on{ background:var(--green); box-shadow:0 0 6px rgba(65,230,147,.6); }
.fs-next{ letter-spacing:.06em; white-space:nowrap; }
.fs-next b{ color:var(--txt); font-weight:500; }
.fs-next i{ color:var(--ice); font-style:normal; }
.fs-go{ color:var(--green); letter-spacing:.1em; white-space:nowrap; }
@media(max-width:820px){
  .fleetstrip{ grid-template-columns:auto 1fr; gap:.8rem; }
  .fs-next,.fs-go{ grid-column:1/-1; }
}
/* --- hero proportions: it was 571px in a 1271px viewport ----------------- */
.hero{ min-height:min(78vh,760px); align-content:center; }
@media(min-width:1100px){
  h1{ font-size:clamp(3rem,5.2vw,4.9rem); }
  .console{ transform:scale(1.04); transform-origin:right center; }
}
</style>
'''
s = s.replace("</head>", css + "</head>", 1)

# 5. script for the strip
js = '''
<script id="t2-js">
(function(){
  const lane=document.getElementById('fsLane');
  if(!lane) return;
  // 48 ticks = one per half hour; light the ones that carry an agent
  const active=new Set([0,4,12,13,14,20,26,27,33,36,40,41,44,47,7,18,30]);
  for(let i=0;i<48;i++){
    const b=document.createElement('i');
    b.style.height=(active.has(i)? 8+((i*7)%14) : 4)+'px';
    if(active.has(i)) b.className='on';
    lane.appendChild(b);
  }
  // countdown to the next scheduled run
  function tick(){
    const n=new Date(), t=new Date(n); t.setHours(20,0,0,0);
    if(t<n) t.setDate(t.getDate()+1);
    const d=t-n, h=Math.floor(d/36e5), m=Math.floor(d%36e5/6e4);
    const el=document.getElementById('fsIn');
    if(el) el.textContent = h>0 ? ('in '+h+'h '+m+'m') : ('in '+m+'m');
  }
  tick(); setInterval(tick,30000);
})();
</script>
'''
s = s.replace("</body>", js + "</body>", 1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("fleet moved below work; strip added; hero retuned")
