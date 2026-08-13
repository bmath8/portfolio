import io
P = r"C:\Brian\02_Projects\portfolio\index.html"
s = io.open(P, encoding="utf-8").read()
old = 'const LOG=[["06:00","morning-brief","compiled 7 sources \u2192 telegram draft"],["06:20","inbox-triage","14 mails classified \u00b7 2 flagged"],["07:00","health-check","cpu 12% \u00b7 mem 41% \u00b7 disks ok"],["08:40","backup-verify","checksum match \u00b7 3.2 GB"],["09:00","process-guardian","watchdog heartbeat ok"],["11:20","disk-audit","freed 412 MB temp"],["13:00","news-digest","9 items ranked \u00b7 draft only"],["15:40","dep-audit","1 advisory \u2192 ticket drafted"],["18:00","evening-brief","day summary assembled"],["20:00","system-watchdog","all 26 agents responsive"]];'
new = ('const LOG=[["06:00","morning-brief","compiled 7 sources \u2192 telegram draft"],'
 '["06:20","inbox-triage","14 mails classified \u00b7 2 flagged"],'
 '["06:45","weather-brief","forecast attached to the morning digest"],'
 '["07:00","health-check","cpu 12% \u00b7 mem 41% \u00b7 disks ok"],'
 '["07:30","cal-sync","3 events reconciled \u00b7 0 conflicts"],'
 '["08:15","todo-sync","11 tasks in, 4 closed overnight"],'
 '["08:40","backup-verify","checksum match \u00b7 3.2 GB"],'
 '["09:00","process-guardian","watchdog heartbeat ok"],'
 '["09:30","market-digest","6 tickers summarised \u00b7 draft only"],'
 '["10:10","log-rotator","rotated 4 logs \u00b7 1.1 GB reclaimed"],'
 '["11:20","disk-audit","freed 412 MB temp"],'
 '["12:00","screenshot-ocr","28 captures indexed"],'
 '["13:00","news-digest","9 items ranked \u00b7 draft only"],'
 '["14:20","net-monitor","latency nominal \u00b7 0 drops in 6h"],'
 '["15:40","dep-audit","1 advisory \u2192 ticket drafted"],'
 '["16:30","cache-cleaner","2.4 GB released"],'
 '["17:15","file-organizer","61 files filed by rule"],'
 '["18:00","evening-brief","day summary assembled"],'
 '["19:00","metrics-roll","daily counters rolled up"],'
 '["20:00","system-watchdog","all 26 agents responsive"]];')
assert old in s, "LOG array not found"
s = s.replace(old, new, 1)
# start at a random offset so two visits do not open on the same line
s = s.replace("const lv=document.getElementById('livelog');let li=0;",
              "const lv=document.getElementById('livelog');let li=Math.floor(Math.random()*LOG.length);", 1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("log stream doubled to 20 entries with a random start")
