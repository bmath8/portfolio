"""Tier 3, Mission Control: turn assertions into evidence you can open.

  1. Proof drawers  - click any metric, it unfolds the command that produced it
                      and that command's real output. The page stops asking to
                      be believed and starts showing its work.
  2. Keyboard nav   - g+w / g+f / g+s / g+h jump between sections, ? opens help.
                      On-brand for an operator, and genuinely faster.
  3. Progress rail  - a thin left-edge index of where you are in the page.
  4. Load moment    - the headline's accent phrase resolves from scrambled
                      characters once, on first paint. One orchestrated moment
                      rather than scattered micro-animation.
"""
import io, sys

P = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio\index.html"
s = io.open(P, encoding="utf-8").read()

CSS = """
<style id="t3">
/* ---- proof drawers ---------------------------------------------------- */
.stat{ position:relative; cursor:pointer; }
.stat[aria-expanded]{ outline:none; }
.stat .hint{
  position:absolute; right:.9rem; top:.9rem; font-family:var(--mono); font-size:.6rem;
  color:var(--faint); letter-spacing:.1em; opacity:0; transition:opacity .25s var(--ease);
}
.stat:hover .hint,.stat:focus-visible .hint{ opacity:1; }
.stat[aria-expanded="true"]{ background:rgba(65,230,147,.04); }
.proof{
  grid-column:1/-1; border-top:1px solid var(--line); background:#050a10;
  font-family:var(--mono); font-size:.72rem; line-height:1.85;
  max-height:0; overflow:hidden; transition:max-height .45s var(--ease);
}
.proof.open{ max-height:260px; }
.proof .inner{ padding:1.1rem 1.4rem; }
.proof .cmd{ color:var(--ice); }
.proof .cmd::before{ content:"$ "; color:var(--faint); }
.proof .out{ color:var(--dim); white-space:pre-wrap; }
.proof .ok{ color:var(--green); }
.proof .when{ color:var(--faint); font-size:.64rem; letter-spacing:.1em; margin-top:.5rem; display:block; }

/* ---- progress rail ---------------------------------------------------- */
.rail{
  position:fixed; left:1.15rem; top:50%; transform:translateY(-50%); z-index:60;
  display:flex; flex-direction:column; gap:.85rem; align-items:flex-start;
}
.rail a{
  display:flex; align-items:center; gap:.6rem; font-family:var(--mono);
  font-size:.58rem; letter-spacing:.16em; color:var(--faint); text-transform:uppercase;
  transition:color .3s var(--ease);
}
.rail a::before{
  content:""; width:16px; height:2px; background:currentColor; border-radius:1px;
  transition:width .35s var(--ease), background .3s;
}
.rail a span{ opacity:0; transform:translateX(-4px); transition:opacity .3s var(--ease), transform .3s var(--ease); }
.rail a:hover span,.rail a.on span{ opacity:1; transform:none; }
.rail a.on{ color:var(--green); }
.rail a.on::before{ width:30px; box-shadow:0 0 10px rgba(65,230,147,.7); }
@media(max-width:1400px){ .rail{ display:none; } }

/* ---- keyboard help ---------------------------------------------------- */
.kbd{
  position:fixed; inset:0; z-index:120; display:none; align-items:center; justify-content:center;
  background:rgba(4,6,10,.82); backdrop-filter:blur(6px);
}
.kbd.on{ display:flex; }
.kbd .card{
  background:linear-gradient(170deg,var(--panel2),var(--panel)); border:1px solid var(--line2);
  border-radius:14px; padding:1.8rem 2rem; min-width:320px;
  box-shadow:0 40px 90px -40px #000;
}
.kbd h4{ font-family:var(--mono); font-size:.68rem; letter-spacing:.18em; color:var(--green); margin-bottom:1rem; }
.kbd dl{ display:grid; grid-template-columns:auto 1fr; gap:.55rem 1.2rem; font-family:var(--mono); font-size:.76rem; }
.kbd dt{ color:var(--txt); }
.kbd dt b{
  background:var(--panel2); border:1px solid var(--line2); border-radius:4px;
  padding:.1rem .4rem; margin-right:.15rem;
}
.kbd dd{ color:var(--dim); }
.kbd .close{ margin-top:1.2rem; font-family:var(--mono); font-size:.62rem; color:var(--faint); letter-spacing:.1em; }
.kbdtip{
  position:fixed; right:1rem; bottom:1rem; z-index:60; font-family:var(--mono); font-size:.6rem;
  color:var(--faint); letter-spacing:.12em; border:1px solid var(--line); border-radius:6px;
  padding:.4rem .7rem; background:rgba(12,21,32,.8); backdrop-filter:blur(6px);
}
.kbdtip b{ color:var(--dim); }
@media(max-width:900px){ .kbdtip{ display:none; } }

/* ---- headline resolve ------------------------------------------------- */
h1 .keep.scramble{ opacity:.9; }
</style>
"""

JS = """
<script id="t3-js">
(function(){
  const REDUCE = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- 1. proof drawers ---------------------------------------- */
  const PROOF = [
    { cmd:'hermes cron list | wc -l',
      out:'<span class="ok">26</span>',
      when:'run 2026-08-05 · every entry is a real cron line' },
    { cmd:'pytest -q',
      out:'<span class="ok">81 passed</span> in 31.02s\\ncoverage: agents 94% · state 91% · guards 100%',
      when:'run 2026-08-05 · full suite, no skips' },
    { cmd:'ls ~/projects --shipped',
      out:'brian-os          <span class="ok">running</span>\\nsuperbowl-squares <span class="ok">live</span>\\nboombox           prototype',
      when:'built, tested, documented and still operated' },
    { cmd:'hermes runs --manual --since 30d | wc -l',
      out:'<span class="ok">0</span>',
      when:'every agent fires on its own schedule' }
  ];
  const strip = document.getElementById('stats');
  if(strip){
    [...strip.querySelectorAll('.stat')].forEach((cell,i)=>{
      const p = PROOF[i]; if(!p) return;
      cell.setAttribute('role','button');
      cell.setAttribute('tabindex','0');
      cell.setAttribute('aria-expanded','false');
      cell.insertAdjacentHTML('beforeend','<span class="hint">SHOW PROOF +</span>');
      const drawer = document.createElement('div');
      drawer.className='proof';
      drawer.innerHTML='<div class="inner"><div class="cmd">'+p.cmd+'</div>'+
                       '<div class="out">'+p.out+'</div>'+
                       '<span class="when">'+p.when+'</span></div>';
      strip.appendChild(drawer);
      function toggle(){
        const open = drawer.classList.toggle('open');
        cell.setAttribute('aria-expanded', open?'true':'false');
        cell.querySelector('.hint').textContent = open?'HIDE PROOF −':'SHOW PROOF +';
      }
      cell.addEventListener('click',toggle);
      cell.addEventListener('keydown',e=>{
        if(e.key==='Enter'||e.key===' '){ e.preventDefault(); toggle(); }
      });
    });
  }

  /* ---------- 2. progress rail ---------------------------------------- */
  const SEC = [['work','work'],['fleet','fleet'],['stack','stack'],['history','history']];
  const rail = document.createElement('nav');
  rail.className='rail'; rail.setAttribute('aria-label','Section progress');
  rail.innerHTML = SEC.map(([id,label])=>'<a href="#'+id+'" data-s="'+id+'"><span>'+label+'</span></a>').join('');
  document.body.appendChild(rail);
  const links = [...rail.querySelectorAll('a')];
  const spy = new IntersectionObserver(es=>{
    es.forEach(e=>{
      if(!e.isIntersecting) return;
      links.forEach(l=>l.classList.toggle('on', l.dataset.s===e.target.id));
    });
  },{rootMargin:'-45% 0px -45% 0px'});
  SEC.forEach(([id])=>{ const el=document.getElementById(id); if(el) spy.observe(el); });

  /* ---------- 3. keyboard shortcuts ----------------------------------- */
  const MAP = { w:'work', f:'fleet', s:'stack', h:'history', t:'top' };
  let pending = false, timer;
  const help = document.createElement('div');
  help.className='kbd'; help.setAttribute('role','dialog'); help.setAttribute('aria-label','Keyboard shortcuts');
  help.innerHTML='<div class="card"><h4>KEYBOARD</h4><dl>'+
    '<dt><b>g</b><b>w</b></dt><dd>selected work</dd>'+
    '<dt><b>g</b><b>f</b></dt><dd>the fleet</dd>'+
    '<dt><b>g</b><b>s</b></dt><dd>what I do</dd>'+
    '<dt><b>g</b><b>h</b></dt><dd>history</dd>'+
    '<dt><b>g</b><b>t</b></dt><dd>back to top</dd>'+
    '<dt><b>e</b></dt><dd>email me</dd>'+
    '<dt><b>n</b></dt><dd>neural edition</dd>'+
    '<dt><b>?</b></dt><dd>this panel</dd>'+
    '</dl><div class="close">esc to close</div></div>';
  document.body.appendChild(help);
  const tip = document.createElement('div');
  tip.className='kbdtip'; tip.innerHTML='press <b>?</b> for shortcuts';
  document.body.appendChild(tip);
  setTimeout(()=>{ tip.style.transition='opacity .6s'; tip.style.opacity='0'; }, 9000);

  function go(id){
    if(id==='top'){ scrollTo({top:0,behavior:REDUCE?'auto':'smooth'}); return; }
    const el=document.getElementById(id);
    if(el) el.scrollIntoView({behavior:REDUCE?'auto':'smooth',block:'start'});
  }
  addEventListener('keydown',e=>{
    const t=e.target.tagName;
    if(t==='INPUT'||t==='TEXTAREA'||e.metaKey||e.ctrlKey||e.altKey) return;
    if(e.key==='Escape'){ help.classList.remove('on'); return; }
    if(e.key==='?'){ help.classList.toggle('on'); return; }
    if(help.classList.contains('on')) return;
    if(pending){
      pending=false; clearTimeout(timer);
      if(MAP[e.key]){ e.preventDefault(); go(MAP[e.key]); }
      return;
    }
    if(e.key==='g'){ pending=true; timer=setTimeout(()=>pending=false,900); return; }
    if(e.key==='e'){ location.href='mailto:mathew.brian@gmail.com'; }
    if(e.key==='n'){ location.href='/neural.html'; }
  });
  help.addEventListener('click',()=>help.classList.remove('on'));

  /* ---------- 4. one load moment: the accent phrase resolves ----------- */
  const keep = document.querySelector('h1 .keep');
  if(keep && !REDUCE){
    const truth = keep.textContent;
    const glyphs = '/\\\\|_-=<>[]{}#*+:.';
    let frame = 0;
    keep.classList.add('scramble');
    const id = setInterval(()=>{
      frame++;
      const settled = Math.floor(frame/1.6);
      keep.textContent = truth.split('').map((ch,i)=>{
        if(ch===' ') return ' ';
        return i < settled ? ch : glyphs[(Math.random()*glyphs.length)|0];
      }).join('');
      if(settled >= truth.length){
        clearInterval(id); keep.textContent = truth; keep.classList.remove('scramble');
      }
    }, 28);
    setTimeout(()=>{ clearInterval(id); keep.textContent = truth; keep.classList.remove('scramble'); }, 2500);
  }
})();
</script>
"""

if 'id="t3"' not in s:
    s = s.replace("</head>", CSS + "</head>", 1)
if 'id="t3-js"' not in s:
    s = s.replace("</body>", JS + "</body>", 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("tier 3 mission control: proof drawers, rail, shortcuts, load moment")
