import io
P = r"C:\Brian\02_Projects\portfolio\neural.html"
s = io.open(P, encoding="utf-8").read()
old = """@media(min-width:1100px){
  .hero{ grid-template-columns:.82fr 1.18fr; gap:.5rem; }
  #brain{ height:700px; }
  h1{ font-size:clamp(2.8rem,5vw,4.6rem); }
  .brainbox{ margin-right:-4%; }        /* let it breathe past the column edge */
}
@media(min-width:1500px){
  #brain{ height:760px; }
  .brainbox{ margin-right:-8%; }
}"""
new = """@media(min-width:1100px){
  /* the text column must still hold "A cortex" on one line, or the headline
     orphans a single letter; the brain gains size from the negative margin
     instead of from stealing column width */
  .hero{ grid-template-columns:.95fr 1.05fr; gap:1rem; }
  #brain{ height:680px; }
  h1{ font-size:clamp(2.7rem,4.4vw,4.2rem); }
  .brainbox{ margin-right:-6%; }
}
@media(min-width:1500px){
  #brain{ height:740px; }
  .brainbox{ margin-right:-10%; }
  h1{ font-size:4.4rem; }
}
h1{ text-wrap:balance; }"""
assert old in s
s = s.replace(old, new, 1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("neural headline wrap fixed")
