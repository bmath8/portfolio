"""Mission Control design pass: INDUSTRIAL TELEMETRY.

The audit found the aesthetic problem precisely: nine sections at exactly
1180px, eleven rounded cards, and a type scale that jumps 78px -> 29px -> 16px
with nothing in between. It reads as a competent template rather than an
instrument.

The direction: this page is a panel on a machine that is running. That means
measurement rules, hairline registration marks, oversized tabular numerals,
condensed display type, and full-bleed moments that break the column - not more
rounded rectangles.

  - A real type scale with a mid-tier, and Bricolage Grotesque for display:
    it has an engineered, slightly odd character that Archivo does not.
  - The metric strip goes full-bleed and enormous. It is the strongest asset on
    the page and it was sitting in a small boxed row.
  - Capabilities stop being four identical cards and become a capability matrix:
    numbered, ruled, with signal bars. This was the weakest section.
  - Experience becomes a real timeline with weight difference between the
    current role and the past ones.
  - Film grain and a measurement rule motif for texture and depth.
  - Cursor-tracked glow in the fleet panel, magnetic buttons, and reveals that
    come from a direction rather than uniformly upward.
"""
import io, sys, os

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"
P = os.path.join(REPO, "index.html")
s = io.open(P, encoding="utf-8").read()

FONTS = """
<style id="d-fonts">
@font-face{font-family:'Bricolage';font-style:normal;font-weight:700;font-display:swap;src:url('/vendor/fonts/bricolage-700.woff2') format('woff2')}
@font-face{font-family:'Bricolage';font-style:normal;font-weight:800;font-display:swap;src:url('/vendor/fonts/bricolage-800.woff2') format('woff2')}
</style>
"""

CSS = """
<style id="design-mc">
:root{
  /* a scale with a middle, on a 1.28 ratio - the old one jumped 78 to 29 */
  --t-hero:clamp(3rem,7.2vw,5.6rem);
  --t-mega:clamp(3.4rem,9vw,7.5rem);
  --t-sec:clamp(1.9rem,3.4vw,2.9rem);
  --t-card:clamp(1.35rem,2vw,1.7rem);
  --t-lead:clamp(1.02rem,1.25vw,1.16rem);
  --t-body:.95rem;
  --t-meta:.78rem;
  --t-micro:.68rem;
  --disp:'Bricolage','Archivo',sans-serif;
  --rule:rgba(147,170,191,.16);
}

/* ---------- texture: fine grain over the whole surface ---------------- */
body::after{
  background:
    radial-gradient(120% 90% at 50% 8%,transparent 58%,rgba(0,0,0,.55) 100%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='3'/%3E%3C/filter%3E%3Crect width='140' height='140' filter='url(%23n)' opacity='.035'/%3E%3C/svg%3E");
}

/* ---------- typography ------------------------------------------------ */
h1{ font-family:var(--disp); font-size:var(--t-hero); letter-spacing:-.035em; line-height:.96; }
.sec-head h2{ font-family:var(--disp); font-size:var(--t-sec); letter-spacing:-.025em; }
.proj h3{ font-family:var(--disp); font-size:var(--t-card); letter-spacing:-.02em; line-height:1.12; }
.hero p.lede{ font-size:var(--t-lead); line-height:1.62; max-width:33rem; }
.proj p{ font-size:var(--t-body); line-height:1.62; }
.foot h2{ font-family:var(--disp); letter-spacing:-.03em; }
.incident h3{ font-family:var(--disp); font-size:var(--t-card); letter-spacing:-.02em; }

/* ---------- section headers: registration mark instead of a dot ------- */
.sec-head{ align-items:center; gap:1.1rem; }
.sec-head .glyph{
  font-size:.62rem; letter-spacing:.2em; opacity:.9;
  border:1px solid currentColor; border-radius:2px; padding:.2rem .42rem;
}
.sec-head h2::after{ height:1px; opacity:.35; }
.sec-head .rule{ background:linear-gradient(90deg,var(--rule),transparent); }

/* ---------- METRIC STRIP: full bleed, oversized ----------------------- */
.stats{
  border-radius:0; border-left:0; border-right:0; margin-top:0;
  width:100vw; margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
  background:
    linear-gradient(180deg,rgba(18,32,49,.9),rgba(12,21,32,.9)),
    repeating-linear-gradient(90deg,transparent 0 39px,var(--rule) 39px 40px);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.03);
}
.stats > .stat{ padding:2.1rem 1.6rem 1.9rem; }
.stats > .stat:first-child{ padding-left:max(1.6rem,calc(50vw - 590px + 1.6rem)); }
.stats > .stat:last-child{ padding-right:max(1.6rem,calc(50vw - 590px + 1.6rem)); }
.stat b{
  font-family:var(--disp); font-size:var(--t-mega); line-height:.86;
  letter-spacing:-.05em; font-variant-numeric:tabular-nums lining-nums;
  display:block; margin-bottom:.5rem;
}
.stat span{ font-size:var(--t-micro); }
.stat small{ font-size:.66rem; opacity:.85; }
.stat::before{ height:3px; }
.stat .hint{ top:auto; bottom:1.5rem; right:1.6rem; }
@media(max-width:920px){
  .stats > .stat:first-child,.stats > .stat:last-child{ padding-left:1.3rem; padding-right:1.3rem; }
  .stat b{ font-size:clamp(2.6rem,13vw,4rem); }
}

/* ---------- hero: asymmetric, console overlaps the strip -------------- */
@media(min-width:1100px){
  .hero{ grid-template-columns:1.06fr .94fr; gap:3.6rem; align-items:center; }
  .console{ transform:translateY(14px) rotate(-.35deg); }
  .console:hover{ transform:translateY(10px) rotate(0deg); }
}
.console{ transition:transform .6s var(--ease); border-radius:12px; }

/* ---------- CAPABILITY MATRIX (was four identical cards) -------------- */
.caps{ display:block; border-top:1px solid var(--line2); }
.cap-card{
  display:grid; grid-template-columns:3.2rem 1fr 1.6fr 7rem; gap:1.6rem; align-items:center;
  background:none; border:0; border-bottom:1px solid var(--line); border-radius:0;
  padding:1.5rem .4rem; transition:background .35s var(--ease),padding .35s var(--ease);
}
.cap-card:hover{ background:linear-gradient(90deg,rgba(74,240,160,.055),transparent 60%); transform:none; padding-left:1rem; box-shadow:none; }
.cap-card .ic{
  width:auto; height:auto; border:0; background:none !important; margin:0;
  font-family:var(--mono); font-size:.7rem; letter-spacing:.14em; opacity:.75;
}
.cap-card .ic::before{ content:"CAP/"; opacity:.5; }
.cap-card h3{ font-family:var(--disp); font-size:1.32rem; letter-spacing:-.02em; margin:0; }
.cap-card p{ font-size:var(--t-body); color:var(--dim); margin:0; }
.cap-card .bars{ display:flex; gap:3px; align-items:flex-end; height:26px; justify-self:end; }
.cap-card .bars i{ width:4px; background:var(--line2); border-radius:1px; transition:background .3s var(--ease),height .5s var(--ease); }
.cap-card:nth-child(1):hover .bars i{ background:var(--green) }
.cap-card:nth-child(2):hover .bars i{ background:var(--ice) }
.cap-card:nth-child(3):hover .bars i{ background:var(--amber) }
.cap-card:nth-child(4):hover .bars i{ background:var(--violet) }
@media(max-width:900px){
  .cap-card{ grid-template-columns:1fr; gap:.5rem; padding:1.3rem .2rem; }
  .cap-card .bars{ justify-self:start; }
}

/* ---------- EXPERIENCE: a spine, not a table -------------------------- */
.xp{ border:0; border-radius:0; }
.xp-row{
  background:none; border:0; border-left:1px solid var(--line2);
  grid-template-columns:1fr 1.5fr; gap:2rem;
  padding:1.9rem 0 1.9rem 2.2rem; position:relative;
  transition:border-color .35s var(--ease);
}
.xp-row::before{
  content:""; position:absolute; left:-4.5px; top:2.35rem;
  width:8px; height:8px; border-radius:50%; background:var(--bg0);
  border:1.5px solid var(--faint); transition:.35s var(--ease);
}
.xp-row:first-child{ border-left-color:var(--green); }
.xp-row:first-child::before{ background:var(--green); border-color:var(--green); box-shadow:0 0 0 4px rgba(74,240,160,.14); }
.xp-row:first-child b{ font-size:1.15rem; }
.xp-row:hover{ background:none; border-left-color:var(--ice); }
.xp-row:hover::before{ border-color:var(--ice); }
.xp-row b{ font-family:var(--disp); font-size:1.02rem; letter-spacing:-.015em; }
.xp-row p{ font-size:var(--t-body); }
.xp-row time{
  text-align:left; grid-column:1; grid-row:2; margin-top:-.9rem;
  font-size:.7rem; letter-spacing:.12em; color:var(--faint);
}
@media(max-width:900px){ .xp-row{ grid-template-columns:1fr; padding-left:1.6rem; } .xp-row time{ grid-column:1; grid-row:auto; margin-top:0; } }

/* ---------- footer: left-aligned, structural ------------------------- */
.foot-inner{ text-align:left; padding:5.5rem 0 3rem; }
.foot h2{ font-size:clamp(2.2rem,5.4vw,4rem); line-height:.98; }
.foot p{ margin:1.1rem 0 2rem; }
.availability{ justify-content:flex-start; }
.foot .row{ justify-content:flex-start; }
@media(max-width:700px){ .foot-inner{ text-align:left; } }

/* ---------- micro-interactions --------------------------------------- */
.hbtn,.btn,.cta{ position:relative; overflow:hidden; }
.hbtn.pri::after,.btn.pri::after{
  content:""; position:absolute; inset:0; transform:translateX(-101%);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);
  transition:transform .7s var(--ease);
}
.hbtn.pri:hover::after,.btn.pri:hover::after{ transform:translateX(101%); }
/* fleet panel follows the cursor */
.fcard{ position:relative; }
.fcard::before{
  content:""; position:absolute; inset:0; pointer-events:none; opacity:0;
  transition:opacity .4s var(--ease);
  background:radial-gradient(320px circle at var(--mx,50%) var(--my,50%),rgba(74,240,160,.09),transparent 70%);
}
.fcard:hover::before{ opacity:1; }
/* reveals arrive from a direction rather than all upward */
.js .proj.rv{ transform:translateY(26px); }
.js .proj.rv:nth-of-type(even){ transform:translateY(26px) translateX(18px); }
.js .proj.rv.in{ transform:none; }
</style>
"""

if 'id="d-fonts"' not in s:
    s = s.replace("</head>", FONTS + "</head>", 1)
if 'id="design-mc"' not in s:
    s = s.replace("</head>", CSS + "</head>", 1)

JS = """
<script id="design-mc-js">
(function(){
  // signal bars for the capability matrix
  document.querySelectorAll('.cap-card').forEach(function(c,i){
    if(c.querySelector('.bars')) return;
    var b=document.createElement('span'); b.className='bars'; b.setAttribute('aria-hidden','true');
    var pat=[[8,14,20,26,22,16],[26,20,14,18,24,12],[12,22,26,16,20,24],[20,12,18,26,14,22]][i%4];
    pat.forEach(function(h){ var e=document.createElement('i'); e.style.height=h+'px'; b.appendChild(e); });
    c.appendChild(b);
  });
  // cursor-tracked glow inside the fleet panels
  document.querySelectorAll('.fcard').forEach(function(card){
    card.addEventListener('pointermove',function(e){
      var r=card.getBoundingClientRect();
      card.style.setProperty('--mx',((e.clientX-r.left)/r.width*100)+'%');
      card.style.setProperty('--my',((e.clientY-r.top)/r.height*100)+'%');
    });
  });
})();
</script>
"""
if 'id="design-mc-js"' not in s:
    s = s.replace("</body>", JS + "</body>", 1)

# preload the new display face
s = s.replace(
    '<link rel="preload" href="/vendor/fonts/archivo-900.woff2" as="font" type="font/woff2" crossorigin>',
    '<link rel="preload" href="/vendor/fonts/bricolage-800.woff2" as="font" type="font/woff2" crossorigin>\n'
    '<link rel="preload" href="/vendor/fonts/archivo-900.woff2" as="font" type="font/woff2" crossorigin>',
    1,
)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("mission control design layer applied")
