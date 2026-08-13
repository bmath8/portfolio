import io
EXTRA = """
<style id="c2b">
.incident{ margin:0 0 1.6rem; }
.incident ol{ grid-template-columns:repeat(2,1fr); gap:1.1rem 2rem; }
@media(max-width:820px){ .incident ol{ grid-template-columns:1fr; } }
</style>
"""
for path in (r"C:\Brian\02_Projects\portfolio\index.html", r"C:\Brian\02_Projects\portfolio\neural.html"):
    s=io.open(path,encoding="utf-8").read()
    if 'id="c2b"' not in s:
        s=s.replace("</head>", EXTRA+"</head>",1)
        io.open(path,"w",encoding="utf-8",newline="").write(s)
    print(path,"incident width tuned")
