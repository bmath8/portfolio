# Serving the candidates locally

Candidates load Lenis/GSAP from `../vendor/`, so **serve from the portfolio root**, not from
this folder:

```
cd C:\Brian\02_Projects\portfolio
python -m http.server 8801 --bind 127.0.0.1
# then open http://127.0.0.1:8801/design-candidates/G-motion.html
```

Serving from inside `design-candidates/` puts `../vendor/` above the document root. The
libraries silently 404, `gsap`/`Lenis` come back `undefined`, and the JS-off fallback makes the
page *look* fine while every animation is dead. That cost a false "verified working" once —
if you're checking motion, confirm in the console that `typeof gsap === 'object'` first.

**When a candidate is promoted to the site root as `index.html`, change `../vendor/` to
`vendor/`.**
