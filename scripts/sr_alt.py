import io
REPO = r"C:\Brian\02_Projects\portfolio"
SR = """<style id="sr">.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}</style>"""

s = io.open(REPO + r"\index.html", encoding="utf-8").read()
if 'id="sr"' not in s:
    s = s.replace("</head>", SR + "</head>", 1)
if "sr-fleet" not in s:
    s = s.replace('<canvas id="radar" width="600" height="600"></canvas>',
      '<canvas id="radar" width="600" height="600"></canvas>\n        <p class="sr-only" id="sr-fleet">Scheduler radar and agent process table: a visualisation of 26 scheduled agents, each with the cron expression it actually runs on. The same schedule is listed as text in the table beside it.</p>', 1)
io.open(REPO + r"\index.html","w",encoding="utf-8",newline="").write(s)

n = io.open(REPO + r"\neural.html", encoding="utf-8").read()
if 'id="sr"' not in n:
    n = n.replace("</head>", SR + "</head>", 1)
if "sr-brain" not in n:
    n = n.replace('<canvas id="brain"></canvas>',
      '<canvas id="brain"></canvas>\n    <p class="sr-only" id="sr-brain">An interactive three-dimensional model of a brain. Each of its 26 glowing nodes represents one real scheduled agent running on Brian\'s machine; hovering a node names the agent and shows its cron line. The same 26 agents and their schedules are described in the Selected work section below.</p>', 1)
io.open(REPO + r"\neural.html","w",encoding="utf-8",newline="").write(n)
print("sr-only alternatives added")
