import io
P=r"C:\Brian\02_Projects\portfolio\neural.html"
s=io.open(P,encoding="utf-8").read()
s=s.replace("--t-mega:clamp(2.5rem,4.6vw,4.2rem);","--t-mega:clamp(2rem,3.4vw,3.2rem);",1)
old="""@media(min-width:1000px){
  .card{ transition:transform .5s var(--ease),border-color .35s,box-shadow .35s; }
  .card:nth-child(even){ margin-left:2.6rem; margin-right:-2.6rem; }
  .card:nth-child(odd){ margin-right:2.6rem; margin-left:-2.6rem; }
  .card:hover{ transform:translateY(-5px); }
}"""
new="""@media(min-width:1000px){
  /* offset with transforms, not negative margins: margins would push past the
     container and create a horizontal scrollbar at some widths */
  .card{ transition:transform .5s var(--ease),border-color .35s,box-shadow .35s; }
  .card:nth-child(odd){ transform:translateX(-1.8rem); }
  .card:nth-child(even){ transform:translateX(1.8rem); }
  .card:nth-child(odd):hover{ transform:translateX(-1.8rem) translateY(-5px); }
  .card:nth-child(even):hover{ transform:translateX(1.8rem) translateY(-5px); }
  .cards{ overflow:visible; }
}"""
assert old in s
s=s.replace(old,new,1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("orb numerals sized to fit; offsets use transforms")
