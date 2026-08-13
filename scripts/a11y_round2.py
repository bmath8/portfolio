"""Round-2 accessibility fixes, all of them measured failures.

1. #brain was focusable AND aria-hidden="true" - WCAG 4.1.2. The Tier-1 script
   marked every canvas decorative and clobbered the label the brain needs.
2. Focusable elements sat inside opacity:0 containers: project links in cards
   that had not scroll-revealed yet, and the closed agent panel's buttons.
3. The agent panel stayed in the accessibility tree when closed, announcing
   placeholder text.
4. Proof drawers had aria-expanded but no aria-controls, and collapsed content
   stayed readable to assistive tech.
5. The shortcut dialog was never hidden, had no aria-modal, no focus trap and
   no focus restore.
6. Heading outline: the panel/dialog titles were <h4> directly under <h1>.
7. The fleet strip was an <a> around four children with no accessible name,
   and external links gave no new-tab warning.
"""
import io, sys, os

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"
MC = os.path.join(REPO, "index.html")
NU = os.path.join(REPO, "neural.html")

# ---------------------------------------------------------------- shared CSS
CSS = """
<style id="a11y2">
/* a revealed-on-scroll block must not hold focusable content while invisible;
   visibility toggles with the opacity so it leaves the tab order entirely */
.js .rv{ visibility:hidden; }
.js .rv.in{ visibility:visible; }
@media (prefers-reduced-motion: reduce){ .js .rv{ visibility:visible; } }
/* keep the sr-only helper available for accessible names */
.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
</style>
"""

# ---------------------------------------------------------------- shared JS
JS = """
<script id="a11y2-js">
(function(){
  /* ---- 1. never mark the interactive brain decorative ------------------ */
  function fixCanvases(){
    document.querySelectorAll('canvas').forEach(function(c){
      if(c.id==='brain'){
        c.removeAttribute('aria-hidden');
        c.setAttribute('role','application');
        c.setAttribute('aria-label','Interactive model of 26 scheduled agents. Press Enter to inspect one, then use the arrow keys to move through the fleet.');
      }else{
        c.setAttribute('aria-hidden','true');
        c.setAttribute('role','presentation');
      }
    });
  }
  fixCanvases();
  addEventListener('load',fixCanvases);
  setTimeout(fixCanvases,600);

  /* ---- 2. reveal a block immediately if focus enters it ---------------- */
  document.addEventListener('focusin',function(e){
    var n=e.target;
    while(n && n!==document.body){
      if(n.classList && n.classList.contains('rv') && !n.classList.contains('in')) n.classList.add('in');
      n=n.parentElement;
    }
  });

  /* ---- 3. the agent panel is inert until it is opened ------------------ */
  var panel=document.getElementById('agentPanel');
  if(panel){
    var setInert=function(open){
      panel.setAttribute('aria-hidden', open?'false':'true');
      if('inert' in HTMLElement.prototype) panel.inert=!open;
      panel.querySelectorAll('button').forEach(function(b){
        if(open) b.removeAttribute('tabindex'); else b.setAttribute('tabindex','-1');
      });
    };
    setInert(false);
    new MutationObserver(function(){ setInert(panel.classList.contains('on')); })
      .observe(panel,{attributes:true,attributeFilter:['class']});
  }

  /* ---- 4. proof drawers: wire aria-controls and hide when collapsed ---- */
  var stats=document.getElementById('stats');
  if(stats){
    var drawers=stats.querySelectorAll('.proof');
    var cells=stats.querySelectorAll('.stat[role="button"]');
    drawers.forEach(function(d,i){
      d.id='proof-'+i;
      d.setAttribute('aria-hidden','true');
      if('inert' in HTMLElement.prototype) d.inert=true;
      if(cells[i]) cells[i].setAttribute('aria-controls','proof-'+i);
      new MutationObserver(function(){
        var open=d.classList.contains('open');
        d.setAttribute('aria-hidden',open?'false':'true');
        if('inert' in HTMLElement.prototype) d.inert=!open;
      }).observe(d,{attributes:true,attributeFilter:['class']});
    });
  }

  /* ---- 5. shortcut dialog: modal semantics, focus trap, focus restore -- */
  var kbd=document.querySelector('.kbd');
  if(kbd){
    kbd.setAttribute('aria-modal','true');
    kbd.setAttribute('aria-hidden','true');
    if('inert' in HTMLElement.prototype) kbd.inert=true;
    var opener=null;
    new MutationObserver(function(){
      var open=kbd.classList.contains('on');
      kbd.setAttribute('aria-hidden',open?'false':'true');
      if('inert' in HTMLElement.prototype) kbd.inert=!open;
      if(open){ opener=document.activeElement; kbd.setAttribute('tabindex','-1'); kbd.focus(); }
      else if(opener && opener.focus){ opener.focus(); opener=null; }
    }).observe(kbd,{attributes:true,attributeFilter:['class']});
    // trap tab inside while open
    kbd.addEventListener('keydown',function(e){
      if(e.key!=='Tab') return;
      var f=kbd.querySelectorAll('a[href],button,[tabindex]:not([tabindex="-1"])');
      if(!f.length){ e.preventDefault(); return; }
      var first=f[0], last=f[f.length-1];
      if(e.shiftKey && document.activeElement===first){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && document.activeElement===last){ e.preventDefault(); first.focus(); }
    });
  }

  /* ---- 6. accessible name for the fleet strip -------------------------- */
  var fs=document.querySelector('.fleetstrip');
  if(fs && !fs.getAttribute('aria-label')){
    fs.setAttribute('aria-label','Fleet status: next scheduled run is system-watchdog at 20:00. Open the full instrument.');
    fs.querySelectorAll('.fs-lane,.fs-live').forEach(function(el){ el.setAttribute('aria-hidden','true'); });
  }

  /* ---- 7. tell assistive tech which links leave the page --------------- */
  document.querySelectorAll('a[target="_blank"]').forEach(function(a){
    if(a.querySelector('.sr-only')) return;
    a.insertAdjacentHTML('beforeend','<span class="sr-only"> (opens in a new tab)</span>');
    if(!a.getAttribute('rel')) a.setAttribute('rel','noopener noreferrer');
  });
})();
</script>
"""


def patch(path):
    s = io.open(path, encoding="utf-8").read()
    orig = s
    if 'id="a11y2"' not in s:
        s = s.replace("</head>", CSS + "</head>", 1)
    if 'id="a11y2-js"' not in s:
        s = s.replace("</body>", JS + "</body>", 1)

    # 6. heading levels: panel and dialog titles are labels, not document structure
    s = s.replace('<h4 id="apName">agent</h4>', '<p class="ap-name" id="apName">agent</p>')
    s = s.replace(".agentpanel h4{", ".agentpanel .ap-name{")
    s = s.replace("<h4>KEYBOARD</h4>", '<p class="kbd-title">KEYBOARD</p>')
    s = s.replace(".kbd h4{", ".kbd .kbd-title{")

    if s != orig:
        io.open(path, "w", encoding="utf-8", newline="").write(s)
        return True
    return False


print("index.html :", patch(MC))
print("neural.html:", patch(NU))
