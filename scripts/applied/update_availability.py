import io

OLD = """      <div class="availability">
        <span><b>Authorized to work in the US</b> \u00b7 no sponsorship required</span>
        <span><b>US Eastern</b> \u00b7 New Jersey</span>
        <span><b>Available now</b> \u00b7 remote, hybrid, on-site or relocation</span>
      </div>"""

NEW = """      <div class="availability">
        <span><b>US citizen</b> \u00b7 authorized to work in the US without sponsorship</span>
        <span><b>New Jersey</b> \u00b7 US Eastern</span>
        <span><b>Available now</b> \u00b7 remote, hybrid or on-site</span>
        <span><b>Will relocate</b> \u00b7 anywhere in the US, and internationally</span>
      </div>"""

# the footer sub-line should say the same thing as the badges
FOOT_MC = "<p>Open to remote, hybrid, on-site or relocation \u2014 and available to start quickly.</p>"
FOOT_MC_NEW = "<p>Open to remote, hybrid or on-site, and willing to relocate anywhere \u2014 including internationally. Available to start quickly.</p>"
FOOT_NU = "<p>Open to remote, hybrid, on-site or relocation \u2014 available to start quickly.</p>"
FOOT_NU_NEW = "<p>Open to remote, hybrid or on-site, and willing to relocate anywhere \u2014 including internationally. Available to start quickly.</p>"

# structured data should carry it too: recruiters and AI screeners read this
LD_OLD = '"seeks":{"@type":"Demand","name":"Software developer and operations roles - remote, hybrid, on-site or relocation"}'
LD_NEW = ('"nationality":{"@type":"Country","name":"United States"},'
          '"seeks":{"@type":"Demand","name":"Software developer and operations roles - remote, hybrid or on-site. '
          'US citizen, authorized to work in the US without sponsorship, and willing to relocate anywhere including internationally."}')

for path in (r"C:\Brian\02_Projects\portfolio\index.html", r"C:\Brian\02_Projects\portfolio\neural.html"):
    s = io.open(path, encoding="utf-8").read(); o = s
    s = s.replace(OLD, NEW, 1)
    s = s.replace(FOOT_MC, FOOT_MC_NEW, 1).replace(FOOT_NU, FOOT_NU_NEW, 1)
    s = s.replace(LD_OLD, LD_NEW, 1)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "changed" if s != o else "NO CHANGE")
