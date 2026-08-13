import io
P = r"C:\Brian\02_Projects\portfolio\neural.html"
s = io.open(P, encoding="utf-8").read()
css = '''
<style id="t2n">
/* --- hero proportions: the brain read small against the headline and left a
       dead gutter between the columns at wide viewports -------------------- */
@media(min-width:1100px){
  .hero{ grid-template-columns:.82fr 1.18fr; gap:.5rem; }
  #brain{ height:700px; }
  h1{ font-size:clamp(2.8rem,5vw,4.6rem); }
  .brainbox{ margin-right:-4%; }        /* let it breathe past the column edge */
}
@media(min-width:1500px){
  #brain{ height:760px; }
  .brainbox{ margin-right:-8%; }
}
/* the callout sat oddly far from the object it labels */
.brainbox .callout{ top:4%; }
/* card rhythm: alternate which side the visual sits on, so three cards in a
   row stop reading as one repeated template */
@media(min-width:900px){
  .card:nth-child(even) .inner{ grid-template-columns:1fr 1fr; }
  .card:nth-child(even) .inner > div:first-child{ order:2; }
  .card:nth-child(even) .inner > .vis{ order:1; }
}
</style>
'''
if 'id="t2n"' not in s:
    s = s.replace("</head>", css + "</head>", 1)
io.open(P,"w",encoding="utf-8",newline="").write(s)
print("neural hero + card rhythm retuned")
