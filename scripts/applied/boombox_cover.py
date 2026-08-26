"""Give BoomBox a real product cover instead of an abstract diagram.

The other two projects show something a person recognises immediately - a live
app and a running console. BoomBox showed a state-lifecycle animation, which is
the most interesting thing about it architecturally and the least legible thing
about it visually. A recruiter scanning the page could not tell what the product
*is*.

So: a designed auth screen. Product mark, tagline, a room-code entry, social
sign-in, and a live equaliser behind it. It reads as a real product in half a
second, and it shows interface work, which the rest of the page does not.

Built as markup and CSS only - no image files, nothing to 404, works with the
existing self-hosted fonts.
"""
import io, os, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"

CSS_MC = """
<style id="bbcover">
.bbx{position:absolute;inset:0;overflow:hidden;border-radius:0;
  background:radial-gradient(120% 90% at 20% 0%,#241b3d 0%,#12101f 45%,#080a12 100%);}
.bbx .glow{position:absolute;width:340px;height:340px;border-radius:50%;filter:blur(60px);opacity:.55;pointer-events:none}
.bbx .g1{background:#7d5cff;top:-120px;left:-70px;animation:bbf 9s ease-in-out infinite alternate}
.bbx .g2{background:#22d3a7;bottom:-140px;right:-60px;animation:bbf 11s ease-in-out infinite alternate-reverse}
@keyframes bbf{to{transform:translate3d(40px,26px,0) scale(1.15)}}
.bbx .eqbg{position:absolute;left:0;right:0;bottom:0;height:38%;display:flex;align-items:flex-end;gap:3px;padding:0 8px;opacity:.16}
.bbx .eqbg i{flex:1;background:linear-gradient(180deg,#a78bfa,#22d3a7);border-radius:2px 2px 0 0;animation:bbeq 1.1s ease-in-out infinite alternate}
@keyframes bbeq{from{height:10%}to{height:90%}}
.bbx .card{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  padding:1.4rem;text-align:center}
.bbx .mark{display:flex;align-items:center;gap:.5rem;margin-bottom:.15rem}
.bbx .mark b{font-family:var(--disp,'Archivo',sans-serif);font-weight:800;font-size:1.32rem;letter-spacing:-.03em;color:#fff}
.bbx .mark .dotmk{width:9px;height:9px;border-radius:50%;background:#22d3a7;box-shadow:0 0 12px #22d3a7}
.bbx .tag{font-family:var(--mono,monospace);font-size:.6rem;letter-spacing:.2em;color:#a99fd6;margin-bottom:1.1rem;text-transform:uppercase}
.bbx .field{display:flex;align-items:center;gap:.5rem;width:min(240px,84%);
  background:rgba(255,255,255,.07);border:1px solid rgba(167,139,250,.35);border-radius:9px;
  padding:.55rem .7rem;margin-bottom:.55rem}
.bbx .field span{font-family:var(--mono,monospace);font-size:.62rem;color:#c9c2ec;letter-spacing:.22em}
.bbx .field .car{width:1px;height:12px;background:#22d3a7;animation:bbc 1.05s steps(2) infinite;margin-left:-2px}
@keyframes bbc{50%{opacity:0}}
.bbx .go{width:min(240px,84%);border:0;border-radius:9px;padding:.55rem;cursor:default;
  font-family:var(--disp,sans-serif);font-weight:700;font-size:.78rem;color:#0b0a14;
  background:linear-gradient(110deg,#22d3a7,#7d5cff);box-shadow:0 8px 22px -10px #7d5cff}
.bbx .or{font-family:var(--mono,monospace);font-size:.54rem;color:#7d75a6;letter-spacing:.2em;margin:.6rem 0 .45rem}
.bbx .socials{display:flex;gap:.4rem}
.bbx .socials i{width:30px;height:26px;border-radius:7px;background:rgba(255,255,255,.08);
  border:1px solid rgba(255,255,255,.12);display:grid;place-items:center;
  font-family:var(--mono,monospace);font-size:.58rem;color:#cfc9ea;font-style:normal}
.bbx .listeners{position:absolute;top:.7rem;right:.8rem;display:flex;align-items:center;gap:.35rem}
.bbx .listeners u{width:17px;height:17px;border-radius:50%;border:1.5px solid #12101f;margin-left:-6px;text-decoration:none}
.bbx .listeners u:nth-child(1){background:#7d5cff}.bbx .listeners u:nth-child(2){background:#22d3a7}
.bbx .listeners u:nth-child(3){background:#f472b6}.bbx .listeners u:nth-child(4){background:#fbbf24}
.bbx .listeners em{font-family:var(--mono,monospace);font-size:.55rem;color:#a99fd6;font-style:normal;letter-spacing:.1em;margin-left:.2rem}
@media(max-width:560px){ .bbx .tag{margin-bottom:.7rem} .bbx .mark b{font-size:1.1rem} }
</style>
"""

MARKUP = """<div class="bbx" aria-hidden="true">
          <span class="glow g1"></span><span class="glow g2"></span>
          <div class="eqbg" id="bbEq"></div>
          <div class="listeners"><u></u><u></u><u></u><u></u><em>14 listening</em></div>
          <div class="card">
            <div class="mark"><span class="dotmk"></span><b>BoomBox</b></div>
            <div class="tag">listen together, anywhere</div>
            <div class="field"><span>ROOM&nbsp;&nbsp;<b id="bbCode">7K4Q</b></span><i class="car"></i></div>
            <button class="go" tabindex="-1">Join the room</button>
            <div class="or">— or continue with —</div>
            <div class="socials"><i>G</i><i>@</i><i>&#9835;</i></div>
          </div>
        </div>
        <p class="sr-only">Mock-up of the BoomBox sign-in screen: a room code entry, a join button, and social sign-in options.</p>"""

JS = """
<script id="bbcover-js">
(function(){
  var eq=document.getElementById('bbEq');
  if(eq && !eq.children.length){
    for(var i=0;i<28;i++){var b=document.createElement('i');
      b.style.animationDelay=(i*0.07)+'s';
      b.style.animationDuration=(0.75+((i*13)%40)/50)+'s';eq.appendChild(b);}
  }
  // the room code cycles, so the mock-up reads as live rather than a screenshot
  var code=document.getElementById('bbCode');
  if(code){
    var A='ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    setInterval(function(){
      if(document.hidden) return;
      var s='';for(var i=0;i<4;i++)s+=A[(Math.random()*A.length)|0];
      code.textContent=s;
    },4200);
  }
})();
</script>
"""

# ---- Mission Control: replace the waveform/queue pane -------------------
P = os.path.join(REPO, "index.html")
s = io.open(P, encoding="utf-8").read()
start = s.find('<div class="bb">')
if start != -1:
    end = s.find('<div class="cap">', start)
    s = s[:start] + MARKUP + "\n        " + s[end:]
    s = s.replace("THE BEAT IS TRANSIENT — THE PLAYLIST SURVIVES A RESTART",
                  "BOOMBOX — SIGN-IN SCREEN · POSTGRES KEEPS THE ROOM, REDIS CARRIES THE BEAT")
if 'id="bbcover"' not in s:
    s = s.replace("</head>", CSS_MC + "</head>", 1)
if 'id="bbcover-js"' not in s:
    s = s.replace("</body>", JS + "</body>", 1)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("index.html: boombox cover installed")

# ---- Neural: replace the stateviz canvas -------------------------------
P2 = os.path.join(REPO, "neural.html")
t = io.open(P2, encoding="utf-8").read()
t = t.replace('<canvas id="stateviz"></canvas>', MARKUP, 1)
t = t.replace("WATCH THE RESTART — POSTGRES SURVIVES, REDIS DOESN'T",
              "BOOMBOX — SIGN-IN SCREEN · POSTGRES KEEPS THE ROOM, REDIS CARRIES THE BEAT")
css_n = CSS_MC.replace('id="bbcover"', 'id="bbcovern"')
if 'id="bbcovern"' not in t:
    t = t.replace("</head>", css_n + "</head>", 1)
if 'id="bbcover-js"' not in t:
    t = t.replace("</body>", JS + "</body>", 1)
io.open(P2, "w", encoding="utf-8", newline="").write(t)
print("neural.html: boombox cover installed")
