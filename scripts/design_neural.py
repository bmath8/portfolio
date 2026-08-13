"""Neural design pass: LUMINOUS SPECIMEN.

Same structural problem as Mission Control - one column, uniform cards, a type
scale with no middle - but this page wants the opposite answer. Mission Control
is an instrument; this one is a specimen under glass, so the moves are
editorial: generous negative space, real typographic contrast, and one serif
that only ever appears in the light.

  - Fraunces enters exactly once, in the light island, so the break from dark to
    light is a change of voice and not just a change of background. That is the
    page's single strongest moment and it was set in the same sans as everything
    around it.
  - The metric orbs lose their boxes and become a ruled row of oversized Syne
    numerals - the numbers are the evidence, the card chrome was noise.
  - The timeline spine becomes a luminous gradient that fades as it descends,
    since the recent role is the one that matters.
  - Cards drift off-axis slightly on alternating rows, and a soft grain sits
    over the aurora so the gradients have tooth instead of looking like flat CSS.
"""
import io, sys, os

REPO = sys.argv[1] if len(sys.argv) > 1 else r"C:\Brian\02_Projects\portfolio"
P = os.path.join(REPO, "neural.html")
s = io.open(P, encoding="utf-8").read()

FONTS = """
<style id="d-fonts-n">
@font-face{font-family:'Fraunces';font-style:normal;font-weight:400;font-display:swap;src:url('/vendor/fonts/fraunces-400.woff2') format('woff2')}
@font-face{font-family:'Fraunces';font-style:normal;font-weight:600;font-display:swap;src:url('/vendor/fonts/fraunces-600.woff2') format('woff2')}
@font-face{font-family:'Fraunces';font-style:normal;font-weight:700;font-display:swap;src:url('/vendor/fonts/fraunces-700.woff2') format('woff2')}
</style>
"""

CSS = """
<style id="design-nu">
:root{
  --t-hero:clamp(2.7rem,5.4vw,4.5rem);
  --t-mega:clamp(2.5rem,4.6vw,4.2rem);
  --t-sec:clamp(2rem,3.6vw,3rem);
  --t-card:clamp(1.35rem,2vw,1.75rem);
  --t-lead:clamp(1.02rem,1.2vw,1.14rem);
  --serif:'Fraunces',Georgia,serif;
}

/* grain over the aurora so the gradients have tooth */
.aurora::after{
  content:""; position:absolute; inset:0; pointer-events:none; opacity:.5;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='.045'/%3E%3C/svg%3E");
}

/* ---------- type ------------------------------------------------------ */
h1{ font-size:var(--t-hero); letter-spacing:-.028em; }
h2{ font-size:var(--t-sec); letter-spacing:-.025em; }
.card h3{ font-size:var(--t-card); letter-spacing:-.018em; line-height:1.14; }
.hero-copy p{ font-size:var(--t-lead); line-height:1.62; }
.sub{ font-size:1.02rem; line-height:1.62; }
.eyebrow{ font-size:.68rem; letter-spacing:.26em; }

/* ---------- metric row: lose the boxes, keep the numbers -------------- */
.orbs{
  grid-template-columns:repeat(4,1fr); gap:0;
  border-top:1px solid var(--line); border-bottom:1px solid var(--line);
  margin:1.5rem 0 0; padding:0;
}
.orb{
  border:0; border-right:1px solid var(--line); border-radius:0;
  background:none; padding:1.9rem 1.4rem 1.7rem;
  transition:background .4s var(--ease);
}
.orb:last-child{ border-right:0; }
.orb:hover{ transform:none; background:linear-gradient(180deg,rgba(146,123,255,.06),transparent); }
.orb::before{ display:none; }
.orb b{
  font-size:var(--t-mega); line-height:.88; letter-spacing:-.045em;
  white-space:nowrap; display:block; margin-bottom:.55rem;
}
.orb span{ font-size:.66rem; }
.orb small{ font-size:.64rem; }
@media(max-width:900px){
  .orbs{ grid-template-columns:repeat(2,1fr); }
  .orb:nth-child(2){ border-right:0; }
  .orb:nth-child(1),.orb:nth-child(2){ border-bottom:1px solid var(--line); }
  .orb b{ font-size:clamp(2.2rem,11vw,3rem); }
}

/* ---------- cards drift off-axis -------------------------------------- */
@media(min-width:1000px){
  .card{ transition:transform .5s var(--ease),border-color .35s,box-shadow .35s; }
  .card:nth-child(even){ margin-left:2.6rem; margin-right:-2.6rem; }
  .card:nth-child(odd){ margin-right:2.6rem; margin-left:-2.6rem; }
  .card:hover{ transform:translateY(-5px); }
}

/* ---------- THE LIGHT ISLAND: a change of voice ----------------------- */
.island{ padding:5rem 4rem 5.4rem; }
.island .eyebrow{ color:#9a4a24; letter-spacing:.28em; }
.island h2{
  font-family:var(--serif); font-weight:600; font-size:clamp(2.3rem,4.4vw,3.6rem);
  letter-spacing:-.02em; line-height:1.04; font-variation-settings:'SOFT' 30,'WONK' 1;
}
.island .sub{
  font-family:var(--serif); font-weight:400; font-size:1.18rem; line-height:1.6;
  color:#4a4757; max-width:34rem;
}
.skill{ border-radius:0; border:0; border-top:1px solid #ddd7c8; background:none; box-shadow:none; padding:1.5rem 0 0; }
.skill:hover{ transform:none; box-shadow:none; }
.skill h3{ font-family:var(--serif); font-weight:600; font-size:1.22rem; letter-spacing:-.01em; }
.skill p{ font-size:.88rem; line-height:1.6; }
@media(max-width:900px){ .island{ padding:3rem 1.5rem 3.4rem; } }

/* ---------- timeline: a spine that fades as it descends --------------- */
.tl{ border-left:0; position:relative; padding-left:2.2rem; }
.tl::before{
  content:""; position:absolute; left:0; top:.3rem; bottom:.3rem; width:1px;
  background:linear-gradient(180deg,var(--teal),var(--violet) 40%,transparent 100%);
}
.tl-item::before{ left:calc(-2.2rem - 4px); width:9px; height:9px; }
.tl-item b{ font-size:1.1rem; letter-spacing:-.015em; }
.tl-item:first-child b{ font-size:1.25rem; }

/* ---------- section headers get air ----------------------------------- */
section{ padding-top:6rem; }
.sub{ margin-bottom:2.6rem; }

/* ---------- footer: left aligned, editorial --------------------------- */
.f-inner{ text-align:left; }
.f-inner h2{ font-size:clamp(2.2rem,5vw,3.8rem); line-height:1.0; }
.f-links,.availability{ justify-content:flex-start; }
.fine{ text-align:left; }

/* ---------- shimmer on the primary action ----------------------------- */
.b1,.f-links a.hi{ position:relative; overflow:hidden; }
.b1::after,.f-links a.hi::after{
  content:""; position:absolute; inset:0; transform:translateX(-101%);
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.4),transparent);
  transition:transform .75s var(--ease);
}
.b1:hover::after,.f-links a.hi:hover::after{ transform:translateX(101%); }
</style>
"""

if 'id="d-fonts-n"' not in s:
    s = s.replace("</head>", FONTS + "</head>", 1)
if 'id="design-nu"' not in s:
    s = s.replace("</head>", CSS + "</head>", 1)

s = s.replace(
    '<link rel="preload" href="/vendor/fonts/syne-800.woff2" as="font" type="font/woff2" crossorigin>',
    '<link rel="preload" href="/vendor/fonts/syne-800.woff2" as="font" type="font/woff2" crossorigin>\n'
    '<link rel="preload" href="/vendor/fonts/fraunces-600.woff2" as="font" type="font/woff2" crossorigin>',
    1,
)

io.open(P, "w", encoding="utf-8", newline="").write(s)
print("neural design layer applied")
