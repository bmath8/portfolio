"""og-neural.png - the Neural edition's own link card."""
import math, random, io
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1200,630
BG=(6,7,15); INK=(239,241,252); DIM=(154,162,196); FAINT=(128,135,176)
TEAL=(60,240,200); VIOLET=(146,123,255); ROSE=(255,123,173); GOLD=(255,209,102)
F=r"C:\Brian\02_Projects\portfolio\scratchpad\vendorbuild\ttf"
def f(n,s): return ImageFont.truetype(F+"\\"+n+".ttf", s)

img=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(img,"RGBA")
# aurora
g=Image.new("RGBA",(W,H),(0,0,0,0)); gd=ImageDraw.Draw(g)
for r in range(620,0,-8):
    gd.ellipse([900-r,-60-r,900+r,-60+r],fill=(146,123,255,int(15*(1-r/620)**2)))
for r in range(520,0,-8):
    gd.ellipse([60-r,620-r,60+r,620+r],fill=(60,240,200,int(11*(1-r/520)**2)))
img=Image.alpha_composite(img.convert("RGBA"),g).convert("RGB"); d=ImageDraw.Draw(img,"RGBA")

# brain point cloud, same sampler idea as the page
random.seed(11)
CX,CY=975,325
pts=[]
for _ in range(2600):
    while True:
        x,y,z=random.uniform(-1,1),random.uniform(-1,1),random.uniform(-1,1)
        l=x*x+y*y+z*z
        if 0.05<l<=1: break
    l=math.sqrt(l); x/=l; y/=l; z/=l
    th=math.atan2(z,x); ph=math.acos(max(-1,min(1,y)))
    wr=1+0.05*math.sin(th*11+ph*3)*math.sin(ph*9)
    shell=0.86+0.14*random.random()**0.35
    px,py,pz=x*0.95,y*0.78,z*1.28
    if pz>0.6: px*=0.88; py*=0.92
    if py<0 and py>-0.45 and abs(pz)<0.6: px*=1.22
    if py<-0.4: py*=0.62
    px*=wr*shell; py*=wr*shell; pz*=wr*shell
    px += 0.05 if px>=0 else -0.05
    # simple projection
    sx=CX+px*158+pz*34; sy=CY-py*172+pz*10
    m=max(0.0,min(1.0,(py+1)/1.9))
    if m>0.62: c=TEAL
    elif m>0.34: c=VIOLET
    else: c=ROSE
    pts.append((sx,sy,c,0.35+0.5*random.random()))
layer=Image.new("RGBA",(W,H),(0,0,0,0)); ld=ImageDraw.Draw(layer)
for sx,sy,c,a in pts:
    ld.ellipse([sx-1.3,sy-1.3,sx+1.3,sy+1.3],fill=c+(int(210*a),))
layer=layer.filter(ImageFilter.GaussianBlur(0.6))
img=Image.alpha_composite(img.convert("RGBA"),layer).convert("RGB"); d=ImageDraw.Draw(img,"RGBA")
# a few bright agent nodes
random.seed(4)
for i in range(26):
    sx,sy,_,_=pts[random.randrange(len(pts))]
    glow=Image.new("RGBA",(W,H),(0,0,0,0)); gd2=ImageDraw.Draw(glow)
    gd2.ellipse([sx-9,sy-9,sx+9,sy+9],fill=(191,255,234,70))
    gd2.ellipse([sx-3,sy-3,sx+3,sy+3],fill=(220,255,245,255))
    img=Image.alpha_composite(img.convert("RGBA"),glow.filter(ImageFilter.GaussianBlur(2))).convert("RGB")
d=ImageDraw.Draw(img,"RGBA")

PAD=72
d.ellipse([PAD,60,PAD+10,70],fill=TEAL)
d.text((PAD+22,54),"26 AGENTS SCHEDULED",font=f("dm-mono-500",18),fill=TEAL)
h=f("syne-800",62)
d.text((PAD,116),"A cortex that",font=h,fill=INK)
acc=Image.new("RGBA",(W,H),(0,0,0,0)); ad=ImageDraw.Draw(acc)
ad.text((PAD,196),"actually works.",font=h,fill=TEAL+(255,))
img=Image.alpha_composite(img.convert("RGBA"),acc.filter(ImageFilter.GaussianBlur(16)))
img=Image.alpha_composite(img,acc).convert("RGB"); d=ImageDraw.Draw(img,"RGBA")
sub=f("dm-sans-400",22)
d.text((PAD,300),"Every glowing node is one real scheduled agent",font=sub,fill=DIM)
d.text((PAD,332),"running on my machine right now.",font=sub,fill=DIM)

cells=[("26","AGENTS LIVE",TEAL),("81/81","TESTS GREEN",VIOLET),("3","SYSTEMS SHIPPED",ROSE),("0","MANUAL TRIGGERS",GOLD)]
BY=430; cw=176
for i,(n,l,c) in enumerate(cells):
    x=PAD+i*(cw+14)
    d.rounded_rectangle([x,BY,x+cw,BY+104],radius=14,fill=(255,255,255,8),outline=(146,123,255,60))
    d.text((x+18,BY+18),n,font=f("syne-800",34),fill=c)
    d.text((x+19,BY+70),l,font=f("dm-mono-400",12),fill=DIM)
d.text((PAD,H-46),"bmath8.vercel.app/neural",font=f("dm-mono-500",17),fill=TEAL)
img.save(r"C:\Brian\02_Projects\portfolio\og-neural.png","PNG",optimize=True)
print("og-neural.png written")

