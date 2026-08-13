import io
MC = r"C:\Brian\02_Projects\portfolio\index.html"
NU = r"C:\Brian\02_Projects\portfolio\neural.html"

MC_CSS = """
<style id="m1">
/* --- phone polish -------------------------------------------------------- */
@media(max-width:560px){
  /* the status bar was crushing the call to action onto two lines */
  .statusbar{ gap:.6rem; padding:.5rem .85rem; }
  .statusbar > span:nth-of-type(2){ display:none; }      /* "NJ · OPEN TO WORK" */
  .statusbar .id{ font-size:.7rem; }
  .statusbar .cta{ white-space:nowrap; flex:0 0 auto; padding:.4rem .7rem; }
  h1{ font-size:clamp(2.1rem,9vw,2.9rem); }
  .hero{ padding-top:2.4rem; }
  .hero p.lede{ font-size:.98rem; }
  /* the fleet strip stacks; keep it legible rather than cramming four columns */
  .fleetstrip{ gap:.6rem; padding:.75rem .9rem; }
  .fs-lane{ height:16px; }
  .fs-go{ font-size:.62rem; }
  .proj .body{ padding:1.4rem 1.25rem; }
  .demo{ min-height:260px; }
  .sec-head{ flex-wrap:wrap; gap:.5rem; }
  .sec-head .tag{ flex-basis:100%; }
  .foot-inner{ padding:3.2rem 0 2.2rem; }
}
</style>
"""

NU_CSS = """
<style id="m1n">
@media(max-width:560px){
  /* this hint line was 399px wide in a 390px viewport and clipped */
  .brainbox .tag{
    position:static; transform:none; white-space:normal; text-align:center;
    line-height:1.9; margin-top:.6rem; font-size:.58rem;
  }
  .brainbox .callout{
    position:static; transform:none; text-align:center; display:block;
    margin-bottom:.4rem; font-size:.6rem;
  }
  #brain{ height:340px; }
  h1{ font-size:clamp(2.1rem,9vw,2.9rem); }
  .hero-copy p{ font-size:.98rem; }
  .card .inner{ padding:1.5rem 1.25rem; gap:1.3rem; }
  .vis{ min-height:250px; }
  .island{ padding:2.4rem 1.3rem 2.8rem; }
  .agentpanel{ padding:1.1rem 1.15rem; }
}
</style>
"""

for path, css, key in ((MC, MC_CSS, 'id="m1"'), (NU, NU_CSS, 'id="m1n"')):
    s = io.open(path, encoding="utf-8").read()
    if key not in s:
        s = s.replace("</head>", css + "</head>", 1)
        io.open(path, "w", encoding="utf-8", newline="").write(s)
        print(path, "mobile polish added")
    else:
        print(path, "already")
