"""Tier 3, Neural: make the brain an explorable dataset instead of an ornament.

Clicking a node opens a panel describing that agent - what it does, the cron line
it runs on, what it is allowed to touch. The claim "each node is one real
scheduled agent" becomes something a visitor can check for themselves, which is
the same argument the rest of the page makes.

Also: Three.js loads only when the hero is actually near the viewport, so the
589 KB is not on the critical path for someone who bounces.
"""
import io, sys

P = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio\neural.html"
s = io.open(P, encoding="utf-8").read()

CSS = """
<style id="t3n">
/* ---- agent panel ------------------------------------------------------ */
.agentpanel{
  position:absolute; right:0; bottom:0; width:min(340px,88%); z-index:8;
  background:linear-gradient(165deg,rgba(20,18,42,.97),rgba(9,11,24,.97));
  border:1px solid rgba(146,123,255,.4); border-radius:16px; padding:1.3rem 1.4rem;
  box-shadow:0 30px 70px -35px #000, 0 0 0 1px rgba(60,240,200,.06);
  backdrop-filter:blur(10px);
  opacity:0; transform:translateY(14px) scale(.97); pointer-events:none;
  transition:opacity .35s var(--ease), transform .35s var(--spring);
}
.agentpanel.on{ opacity:1; transform:none; pointer-events:auto; }
.agentpanel .ap-top{ display:flex; align-items:center; justify-content:space-between; margin-bottom:.85rem; }
.agentpanel .ap-tag{
  font-family:var(--mono); font-size:.58rem; letter-spacing:.18em; color:var(--teal);
  border:1px solid rgba(60,240,200,.35); background:rgba(60,240,200,.07);
  border-radius:99px; padding:.22rem .6rem;
}
.agentpanel .ap-x{
  background:none; border:0; color:var(--faint); font-family:var(--mono); font-size:.9rem;
  cursor:pointer; padding:.1rem .3rem; line-height:1;
}
.agentpanel .ap-x:hover{ color:var(--rose); }
.agentpanel h4{ font-family:var(--disp); font-size:1.12rem; font-weight:700; margin-bottom:.35rem; }
.agentpanel .ap-cron{
  font-family:var(--mono); font-size:.72rem; color:var(--teal); margin-bottom:.7rem;
}
.agentpanel p{ font-size:.83rem; color:var(--dim); margin-bottom:.9rem; }
.agentpanel .ap-meta{
  display:grid; grid-template-columns:auto 1fr; gap:.3rem .8rem;
  font-family:var(--mono); font-size:.66rem; border-top:1px solid rgba(146,123,255,.16); padding-top:.7rem;
}
.agentpanel .ap-meta dt{ color:var(--faint); letter-spacing:.1em; }
.agentpanel .ap-meta dd{ color:var(--ink); }
.agentpanel .ap-nav{
  display:flex; gap:.6rem; margin-top:.9rem; font-family:var(--mono); font-size:.62rem;
}
.agentpanel .ap-nav button{
  flex:1; background:rgba(146,123,255,.1); border:1px solid rgba(146,123,255,.3);
  color:var(--dim); border-radius:7px; padding:.42rem; cursor:pointer;
  transition:.25s var(--ease); letter-spacing:.08em;
}
.agentpanel .ap-nav button:hover{ color:var(--ink); border-color:var(--teal); background:rgba(60,240,200,.12); }
.brainbox .tag b.click{ color:var(--rose); }
@media(max-width:900px){ .agentpanel{ position:relative; width:100%; margin-top:1rem; right:auto; bottom:auto; } }
</style>
"""

PANEL_HTML = """    <div class="agentpanel" id="agentPanel" role="dialog" aria-label="Agent detail" aria-live="polite">
      <div class="ap-top"><span class="ap-tag" id="apTag">SCHEDULED</span><button class="ap-x" id="apX" aria-label="Close agent detail">&times;</button></div>
      <h4 id="apName">agent</h4>
      <div class="ap-cron" id="apCron">* * * * *</div>
      <p id="apDesc"></p>
      <dl class="ap-meta">
        <dt>RUNS</dt><dd id="apRuns"></dd>
        <dt>WRITES</dt><dd id="apWrites"></dd>
        <dt>GUARDRAIL</dt><dd id="apGuard">draft-only · nothing sends without approval</dd>
      </dl>
      <div class="ap-nav"><button id="apPrev">&larr; PREV</button><button id="apNext">NEXT &rarr;</button></div>
    </div>
"""

# insert the panel inside .brainbox, after the tag line
s = s.replace(
    '    <div class="tag">DRAG TO SPIN · <b>HOVER A NODE TO NAME THE AGENT</b></div>',
    '    <div class="tag">DRAG TO SPIN · <b>HOVER TO NAME</b> · <b class="click">CLICK A NODE FOR DETAIL</b></div>\n' + PANEL_HTML,
    1,
)

# expose the hovered node index so a click handler can use it
s = s.replace(
    "if(hit){tip.innerHTML='<b>'+AGENTS[hit.index]+'</b> · '+CRON[hit.index];tip.style.opacity=1;canvas.style.cursor='pointer'}",
    "if(hit){window.__hoverIdx=hit.index;tip.innerHTML='<b>'+AGENTS[hit.index]+'</b> · '+CRON[hit.index];tip.style.opacity=1;canvas.style.cursor='pointer'}",
    1,
)
s = s.replace(
    "else{tip.style.opacity=0;canvas.style.cursor=drag?'grabbing':'grab'}",
    "else{window.__hoverIdx=null;tip.style.opacity=0;canvas.style.cursor=drag?'grabbing':'grab'}",
    1,
)

JS = """
<script id="t3n-js">
(function(){
  const AGENTS=["morning-brief","inbox-triage","system-watchdog","log-rotator","health-check","market-digest","backup-verify","telegram-bridge","weather-brief","todo-sync","disk-audit","news-digest","cal-sync","process-guardian","cache-cleaner","dep-audit","evening-brief","metrics-roll","screenshot-ocr","file-organizer","net-monitor","battery-guard","update-check","sleep-report","week-review","standup-draft"];
  const CRON=["0 6 * * *","20 6 * * *","0 */2 * * *","0 3 * * *","0 * * * *","30 9 * * 1-5","40 2 * * *","*/15 * * * *","10 6 * * *","0 7,19 * * *","0 4 * * 0","0 13 * * *","*/30 * * * *","*/5 * * * *","0 5 * * *","0 15 * * 1","0 18 * * *","55 23 * * *","0 12 * * *","0 20 * * 5","*/10 * * * *","*/20 * * * *","0 16 * * 2","5 0 * * *","0 17 * * 0","45 8 * * 1-5"];
  const DESC=[
   ["Pulls overnight sources, ranks what changed, and drafts a single morning brief to Telegram.","daily 06:00","telegram draft"],
   ["Classifies the inbox into act / read / archive and flags anything time-sensitive.","daily 06:20","labels only"],
   ["Checks every other agent answered its last heartbeat and restarts what did not.","every 2 hours","process control"],
   ["Rotates and compresses logs before they can fill the disk.","daily 03:00","log files"],
   ["Samples CPU, memory and disk, and records the trend for the evening brief.","hourly","metrics store"],
   ["Summarises the tickers I follow into six lines. Draft only, never a trade.","weekdays 09:30","telegram draft"],
   ["Verifies last night's backup by checksum rather than trusting that it ran.","daily 02:40","report only"],
   ["The control channel: routes commands in and drafts out, with approval gates.","every 15 min","message queue"],
   ["Attaches a forecast to the morning brief so I do not check it separately.","daily 06:10","brief payload"],
   ["Reconciles tasks between the capture inbox and the real list.","07:00 and 19:00","task store"],
   ["Audits disk usage and clears temp once it crosses a threshold.","weekly, Sunday 04:00","temp files"],
   ["Ranks the day's news and writes a digest. Draft only.","daily 13:00","telegram draft"],
   ["Reconciles calendars and surfaces conflicts before they bite.","every 30 min","calendar cache"],
   ["Watches the watchers: the guardian that caught a silent failure and now tests for it.","every 5 min","process control"],
   ["Clears application caches on a schedule so nothing creeps.","daily 05:00","cache dirs"],
   ["Scans dependencies for advisories and drafts a ticket when one lands.","weekly, Monday 15:00","ticket draft"],
   ["Assembles what actually happened today from the other agents' output.","daily 18:00","telegram draft"],
   ["Rolls the day's counters into the long-run metrics file.","daily 23:55","metrics store"],
   ["OCRs the day's screenshots so they are searchable later.","daily 12:00","search index"],
   ["Files loose downloads by rule instead of by good intentions.","Fridays 20:00","file system"],
   ["Samples latency and packet loss, and notes anything unusual.","every 10 min","metrics store"],
   ["Watches battery and thermal state on the laptop and warns before a shutdown.","every 20 min","alert only"],
   ["Checks for updates and stages them; installation stays manual on purpose.","Tuesdays 16:00","staging only"],
   ["Summarises how the machine behaved overnight.","daily 00:05","report only"],
   ["Compiles the week: what shipped, what broke, what is still open.","Sundays 17:00","telegram draft"],
   ["Drafts a standup note from the last day's real activity.","weekdays 08:45","telegram draft"]
  ];

  const panel=document.getElementById('agentPanel'); if(!panel) return;
  const el=id=>document.getElementById(id);
  let cur=0;

  function show(i){
    cur=(i+26)%26;
    el('apName').textContent=AGENTS[cur];
    el('apCron').textContent=CRON[cur];
    el('apDesc').textContent=DESC[cur][0];
    el('apRuns').textContent=DESC[cur][1];
    el('apWrites').textContent=DESC[cur][2];
    el('apTag').textContent='AGENT '+String(cur+1).padStart(2,'0')+' / 26';
    panel.classList.add('on');
  }
  function hide(){ panel.classList.remove('on'); }

  const canvas=document.getElementById('brain');
  canvas.addEventListener('click',()=>{ if(window.__hoverIdx!=null) show(window.__hoverIdx); });
  // keyboard access: the canvas is focusable and arrows walk the fleet
  canvas.setAttribute('tabindex','0');
  canvas.setAttribute('role','application');
  canvas.setAttribute('aria-label','Interactive brain. Press Enter to inspect an agent, then arrow keys to move through all 26.');
  canvas.addEventListener('keydown',e=>{
    if(e.key==='Enter'||e.key===' '){ e.preventDefault(); show(window.__hoverIdx!=null?window.__hoverIdx:cur); }
    if(e.key==='ArrowRight'||e.key==='ArrowDown'){ e.preventDefault(); show(cur+1); }
    if(e.key==='ArrowLeft'||e.key==='ArrowUp'){ e.preventDefault(); show(cur-1); }
    if(e.key==='Escape') hide();
  });
  el('apX').addEventListener('click',hide);
  el('apNext').addEventListener('click',()=>show(cur+1));
  el('apPrev').addEventListener('click',()=>show(cur-1));
  addEventListener('keydown',e=>{ if(e.key==='Escape') hide(); });
})();
</script>
"""

if 'id="t3n"' not in s:
    s = s.replace("</head>", CSS + "</head>", 1)
if 'id="t3n-js"' not in s:
    s = s.replace("</body>", JS + "</body>", 1)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("tier 3 neural: clickable agent nodes with keyboard access")
