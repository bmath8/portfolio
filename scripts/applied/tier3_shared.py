import io
REPO = r"C:\Brian\02_Projects\portfolio"

PRELOAD_MC = """<link rel="preload" href="/vendor/fonts/archivo-900.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/vendor/fonts/ibm-plex-mono-400.woff2" as="font" type="font/woff2" crossorigin>
"""
PRELOAD_NU = """<link rel="preload" href="/vendor/fonts/syne-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/vendor/fonts/dm-sans-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/vendor/fonts/dm-mono-400.woff2" as="font" type="font/woff2" crossorigin>
"""

JSONLD = """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"Person","name":"Brian Mathew","jobTitle":"Software Developer",
"email":"mailto:mathew.brian@gmail.com","telephone":"+1-609-815-1685","url":"https://bmath8.vercel.app/",
"address":{"@type":"PostalPlace","addressRegion":"NJ","addressCountry":"US"},
"sameAs":["https://github.com/bmath8","https://linkedin.com/in/brian-mathew-66235556"],
"knowsAbout":["Python","TypeScript","React","Next.js","Flask","Node.js","PostgreSQL","Supabase","Docker",
"Windows administration","PowerShell","job scheduling","log analysis","health monitoring","pytest","Jest"],
"seeks":{"@type":"Demand","name":"Software developer and operations roles - remote, hybrid, on-site or relocation"}}
</script>
"""

PRINT = """<style id="print" media="print">
/* recruiters print and PDF portfolios; make that produce something readable */
*{ background:#fff !important; color:#111 !important; box-shadow:none !important; text-shadow:none !important; }
canvas,.rail,.kbdtip,.kbd,.skip,.fleetstrip .fs-lane,.demo,.vis,.agentpanel{ display:none !important; }
a{ text-decoration:underline; }
a[href^="http"]::after{ content:" (" attr(href) ")"; font-size:.8em; color:#555 !important; }
.statusbar,nav{ position:static !important; border:0 !important; }
.band,.island,section{ padding:.6rem 0 !important; border:0 !important; page-break-inside:avoid; }
.proj,.card,.xp-row,.cap-card,.skill{ border:1px solid #ccc !important; page-break-inside:avoid; }
h1{ font-size:26pt !important; } h2{ font-size:15pt !important; } h3{ font-size:12pt !important; }
body{ font-size:10.5pt; }
</style>
"""

def add(path, preload, canon_og=None):
    s = io.open(path, encoding="utf-8").read()
    if 'rel="preload"' not in s:
        s = s.replace("<title>", preload + "<title>", 1)
    if 'application/ld+json' not in s:
        s = s.replace("</head>", JSONLD + "</head>", 1)
    if 'id="print"' not in s:
        s = s.replace("</head>", PRINT + "</head>", 1)
    if canon_og:
        s = s.replace('content="https://bmath8.vercel.app/og.png?v=7"', 'content="%s"' % canon_og)
    io.open(path, "w", encoding="utf-8", newline="").write(s)
    print(path, "preload + json-ld + print")

add(REPO + r"\index.html", PRELOAD_MC)
add(REPO + r"\neural.html", PRELOAD_NU, "https://bmath8.vercel.app/og-neural.png?v=1")
