"""Bring the site's numbers back in line with the machine.

Verified 2026-08-19 against the live fleet and a real test run:

    agents   26 -> 29     hermes cron list, 29 active jobs
    tests    81 -> 157    pytest -q, "157 passed in 28.87s"
    dated    2026-08-05 -> 2026-08-19

Three agents were added since the page was last updated: freshness-monitor,
governance-review and autoresearch. The stale numbers *understated* the work,
which is the less damaging direction but still breaks the page's one promise -
that every number is checkable.
"""
import io, json, os, re, sys

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"
FLEET = json.load(io.open(sys.argv[2] if len(sys.argv) > 2 else os.environ["TEMP"] + r"\fleet.json", encoding="utf-8-sig"))

N = len(FLEET)                       # 29
TESTS = 157
SECS = "28.87s"
DATE = "2026-08-19"
OLD_DATE = "2026-08-05"

# hermes prints an interval form for one job; express it as the cron it runs on
for a in FLEET:
    if a["cron"].startswith("every 240m"):
        a["cron"] = "0 */4 * * *"

names = [a["n"] for a in FLEET]
crons = [a["cron"] for a in FLEET]

# ---- agents.json: the site's own record of the schedule ----------------
io.open(os.path.join(REPO, "agents.json"), "w", encoding="utf-8", newline="").write(
    json.dumps([{"n": a["n"], "cron": a["cron"]} for a in FLEET], indent=2) + "\n"
)

def js_array(vals):
    return "[" + ",".join('"%s"' % v for v in vals) + "]"

# short purpose lines for the agents Neural's panel did not know about
NEW_DESC = {
    "freshness-monitor": ("Watches for facts on the site and in the resumes that have drifted from "
                          "what the machine actually reports, and flags them before anyone else "
                          "notices.", "every 4 hours", "report only"),
    "governance-review": ("Weekly pass over agent permissions and workspace boundaries - what each "
                          "agent may read, write and reach.", "Sundays 08:00", "report only"),
    "autoresearch": ("Runs a standing research queue overnight and files what it finds where the "
                     "other agents can use it.", "daily 07:20", "research store"),
}


def patch(path, is_mc):
    s = io.open(path, encoding="utf-8").read()
    before = s

    # --- headline counts ------------------------------------------------
    s = s.replace("26 agents scheduled", "%d agents scheduled" % N)
    s = s.replace("26 scheduled agents run unattended", "%d scheduled agents run unattended" % N)
    s = s.replace("A 26-agent fleet that runs my day", "A %d-agent fleet that runs my day" % N)
    s = s.replace("26 scheduled agents &mdash; count", "%d scheduled agents &mdash; count" % N)
    s = s.replace("26 scheduled agents — count", "%d scheduled agents — count" % N)
    s = s.replace('<b data-n="26">26</b>', '<b data-n="%d">%d</b>' % (N, N))
    s = s.replace('<b data-n="81" data-suffix="/81">81/81</b>',
                  '<b data-n="%d" data-suffix="/%d">%d/%d</b>' % (TESTS, TESTS, TESTS, TESTS))
    s = s.replace("81/81 tests passing", "%d/%d tests passing" % (TESTS, TESTS))
    s = s.replace("all 26 agents responsive", "all %d agents responsive" % N)
    s = s.replace("[scheduler] tick — 26 cron entries loaded",
                  "[scheduler] tick — %d cron entries loaded" % N)
    s = s.replace("one real scheduled agent on my machine", "one real scheduled agent on my machine")

    # --- provenance: date and duration ----------------------------------
    s = s.replace(OLD_DATE, DATE)
    s = s.replace("live <code>pytest</code> run, 31s", "live <code>pytest</code> run, %s" % SECS)
    s = s.replace("live pytest run · 31s", "live pytest run · %s" % SECS)
    s = s.replace("live pytest · 31s", "live pytest · %s" % SECS)
    s = s.replace("81 passed</span> <span class=\"a\">in 31.02s",
                  "%d passed</span> <span class=\"a\">in %s" % (TESTS, SECS))
    s = s.replace("81 passed in 31.02s", "%d passed in %s" % (TESTS, SECS))
    s = s.replace("[pytest] 81 passed in 31.02s", "[pytest] %d passed in %s" % (TESTS, SECS))
    s = s.replace("hermes cron list · 2026", "hermes cron list · 2026")

    # --- proof drawer payloads (Mission Control) ------------------------
    s = s.replace("out:'<span class=\"ok\">26</span>'", "out:'<span class=\"ok\">%d</span>'" % N)
    s = s.replace("<span class=\"ok\">81 passed</span> in 31.02s",
                  "<span class=\"ok\">%d passed</span> in %s" % (TESTS, SECS))
    s = s.replace("coverage: agents 94% · state 91% · guards 100%",
                  "coverage: agents 94% · state 91% · guards 100%")

    # --- the incident block references the suite size -------------------
    s = s.replace("It is part of the 81 that run on every change",
                  "It is part of the %d that run on every change" % TESTS)
    s = s.replace("part of the 81 that run", "part of the %d that run" % TESTS)

    # --- JS data arrays --------------------------------------------------
    s = re.sub(r'const AGENTS=\[[^\]]*\];', 'const AGENTS=%s;' % js_array(names), s)
    s = re.sub(r'const CRON=\[[^\]]*\];', 'const CRON=%s;' % js_array(crons), s)

    # --- Neural: agent panel counter and DESC table ----------------------
    if not is_mc:
        s = s.replace("'/ 26'", "'/ %d'" % N)
        s = s.replace("+' / 26'", "+' / %d'" % N)
        s = s.replace("String(cur+1).padStart(2,'0')+' / 26'",
                      "String(cur+1).padStart(2,'0')+' / %d'" % N)
        s = s.replace("(i+26)%26", "(i+%d)%%%d" % (N, N))
        s = s.replace("Math.floor(rnd()*26)", "Math.floor(rnd()*%d)" % N)
        s = s.replace("Math.floor(Math.random()*26)", "Math.floor(Math.random()*%d)" % N)
        s = s.replace("for(let i=0;i<26;i++)", "for(let i=0;i<%d;i++)" % N)
        s = s.replace("for(let j=i+1;j<26;j++)", "for(let j=i+1;j<%d;j++)" % N)
        s = s.replace("new Float32Array(26*3)", "new Float32Array(%d*3)" % N)
        s = s.replace("its 26 glowing nodes", "its %d glowing nodes" % N)
        s = s.replace("26 glowing nodes", "%d glowing nodes" % N)
        s = s.replace("all 26 every", "all %d every" % N)
        s = s.replace("through all 26", "through all %d" % N)
        s = s.replace("model of 26 scheduled agents", "model of %d scheduled agents" % N)
        s = s.replace("same 26 agents", "same %d agents" % N)
        # extend DESC with entries for the new agents, in fleet order
        m = re.search(r'const DESC=\[', s)
        if m:
            end = s.index("];", m.start())
            body = s[m.end():end]
            rows = body.rstrip().rstrip(",")
            for nm in names:
                if nm in NEW_DESC and ('"%s"' % NEW_DESC[nm][0][:24]) not in s:
                    d, when, writes = NEW_DESC[nm]
                    rows += ',\n   ["%s","%s","%s"]' % (d.replace('"', "'"), when, writes)
            s = s[:m.end()] + rows + s[end:]

    # --- meta descriptions ----------------------------------------------
    s = s.replace("26-agent Windows automation fleet with 81 passing tests",
                  "%d-agent Windows automation fleet with %d passing tests" % (N, TESTS))
    s = s.replace("26 scheduled agents running unattended. 81 tests passing.",
                  "%d scheduled agents running unattended. %d tests passing." % (N, TESTS))
    s = s.replace("26 agents live, 81/81 tests green",
                  "%d agents live, %d/%d tests green" % (N, TESTS, TESTS))
    s = s.replace("26 agents live, 81 tests green", "%d agents live, %d tests green" % (N, TESTS))

    io.open(path, "w", encoding="utf-8", newline="").write(s)
    return s != before


print("index.html  changed:", patch(os.path.join(REPO, "index.html"), True))
print("neural.html changed:", patch(os.path.join(REPO, "neural.html"), False))
print("agents.json rewritten with %d agents" % N)
