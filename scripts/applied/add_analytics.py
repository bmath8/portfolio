import io
for path,is_mc in ((r"C:\Brian\02_Projects\portfolio\index.html",1),(r"C:\Brian\02_Projects\portfolio\neural.html",0)):
    s=io.open(path,encoding="utf-8").read()
    if 'site.webmanifest' not in s:
        s=s.replace('<link rel="icon"','<link rel="manifest" href="/site.webmanifest">\n<link rel="apple-touch-icon" href="/favicon.svg">\n<link rel="icon"',1)
    if 'va.vercel-scripts' not in s:
        # Vercel Analytics: first-party, cookieless, no consent banner needed
        s=s.replace("</body>",'<script defer src="/_vercel/insights/script.js"></script>\n</body>',1)
    io.open(path,"w",encoding="utf-8",newline="").write(s)
    print(path,"manifest + analytics")
