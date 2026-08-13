import io
P=r"C:\Brian\02_Projects\portfolio\index.html"
s=io.open(P,encoding="utf-8").read()

old_pad = """.stats > .stat{ padding:2.1rem 1.6rem 1.9rem; }
.stats > .stat:first-child{ padding-left:max(1.6rem,calc(50vw - 590px + 1.6rem)); }
.stats > .stat:last-child{ padding-right:max(1.6rem,calc(50vw - 590px + 1.6rem)); }"""
new_pad = """/* pad the full-bleed container, not the first and last cells: padding on the
   cells stole width from equal grid columns and clipped the first number */
.stats{ padding-inline:max(1.5rem,calc(50vw - 590px)); }
.stats > .stat{ padding:2.1rem 1.5rem 1.9rem; }
.stats > .stat:first-child{ padding-left:0; }
.stats > .stat:last-child{ padding-right:0; }"""
assert old_pad in s
s=s.replace(old_pad,new_pad,1)

s=s.replace("""@media(max-width:920px){
  .stats > .stat:first-child,.stats > .stat:last-child{ padding-left:1.3rem; padding-right:1.3rem; }
  .stat b{ font-size:clamp(2.6rem,13vw,4rem); }
}""","""@media(max-width:920px){
  .stats{ padding-inline:1.3rem; }
  .stats > .stat{ padding:1.5rem 1rem; }
  .stat b{ font-size:clamp(2.4rem,12vw,3.6rem); }
}""",1)

# headline was orphaning "I build" on its own line
s=s.replace("--t-hero:clamp(3rem,7.2vw,5.6rem);","--t-hero:clamp(2.8rem,5.9vw,4.8rem);",1)
s=s.replace("h1{ font-family:var(--disp); font-size:var(--t-hero); letter-spacing:-.035em; line-height:.96; }",
            "h1{ font-family:var(--disp); font-size:var(--t-hero); letter-spacing:-.035em; line-height:1.0; max-width:15ch; }",1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("metric strip + headline fixed")
