import io
files = [r"C:\Brian\02_Projects\portfolio\index.html",
         r"C:\Brian\02_Projects\portfolio\neural.html",
         r"C:\Brian\02_Projects\portfolio\404.html",
         r"C:\Brian\02_Projects\portfolio\sitemap.xml"]
n=0
for f in files:
    s=io.open(f,encoding="utf-8").read(); o=s
    s=s.replace("https://bmath8.vercel.app/neural.html","https://bmath8.vercel.app/neural")
    s=s.replace('href="/neural.html"','href="/neural"')
    s=s.replace("location.href='/neural.html'","location.href='/neural'")
    if s!=o:
        io.open(f,"w",encoding="utf-8",newline="").write(s); n+=1
        print("updated",f)
print("files changed:",n)
