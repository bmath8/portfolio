import io
P = r"C:\Brian\02_Projects\portfolio\index.html"
s = io.open(P, encoding="utf-8").read()
old = """  const S=rc.offsetWidth||300;rc.width=S*devicePixelRatio;rc.height=S*devicePixelRatio;
  rx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);rx.clearRect(0,0,S,S);"""
new = """  const S=rc.offsetWidth||300;
  // only reallocate the backing store when the box actually changes size:
  // doing this every frame reallocated the canvas 60x a second
  if(rc._s!==S){rc._s=S;rc.width=S*devicePixelRatio;rc.height=S*devicePixelRatio;}
  rx.setTransform(devicePixelRatio,0,0,devicePixelRatio,0,0);rx.clearRect(0,0,S,S);"""
assert old in s, "radar resize block not found"
s = s.replace(old, new, 1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("radar resize fixed")
