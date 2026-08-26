#!/usr/bin/env python3
"""Veragensia live wallpaper frame generator — procedural aurora + wordmark."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "frames"
N   = int(sys.argv[2]) if len(sys.argv) > 2 else 12
W,H = int(sys.argv[3]) if len(sys.argv) > 3 else 1920, int(sys.argv[4]) if len(sys.argv) > 4 else 1080

C1, C2, C3 = (91,140,255), (143,107,255), (60,160,214)   # blue, violet, cyan
G0, G1 = (11,16,32), (29,43,82)                          # background gradient
FG = (238,242,255); SUB = (159,176,232)
os.makedirs(OUT, exist_ok=True)

def between(a,b,t): return tuple(int(a[i]+(b[i]-a[i])*t) for i in range(3))

def base_gradient(w,h,c0,c1):
    img = Image.new("RGB",(w,h))
    d = img.load()
    for y in range(h):
        t = y/h
        c = between(c0,c1,t)
        for x in range(w): d[x,y]=c
    return img

def radial(size, cx, cy, r, c0, c1):
    """RGBA image with a soft radial gradient blob."""
    w,h = size
    img = Image.new("RGBA",(w,h),(0,0,0,0))
    d = img.load()
    for y in range(int(cy-r)-r, int(cy+r)+r):
        if y<0 or y>=h: continue
        for x in range(int(cx-r)-r, int(cx+r)+r):
            if x<0 or x>=w: continue
            dist = math.hypot(x-cx, y-cy)/max(r,1)
            if dist>1: continue
            t = dist**1.6
            col = between(c1,c0,1-t)
            a = int(190*(1-t))
            d[x,y] = (col[0],col[1],col[2],a)
    return img

def fontfile():
    for p in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/abattis-cantarell/Cantarell-Bold.otf",
        "/root/pi-mono/node_modules/katex/dist/fonts/KaTeX_Main-Bold.ttf",
    ):
        if os.path.exists(p): return p
    return None

for i in range(N):
    ph = i/N
    bg = base_gradient(W,H,G0,G1)
    # two moving aurora blobs
    b1 = (W*(0.25+0.5*math.sin(ph*2*math.pi)), H*(0.55+0.16*math.sin(ph*2*math.pi+1.0)), W*0.24, C1, C3)
    b2 = (W*(0.72+0.28*math.cos(ph*2*math.pi)), H*(0.30+0.20*math.cos(ph*2*math.pi+2.0)), W*0.30, C2, C1)
    comp = Image.new("RGBA",(W,H),(0,0,0,0))
    comp = Image.alpha_composite(bg.convert("RGBA"), radial((W,H),int(b1[0]),int(b1[1]),int(b1[2]),b1[3],b1[4]))
    comp = Image.alpha_composite(comp, radial((W,H),int(b2[0]),int(b2[1]),int(b2[2]),b2[3],b2[4]))
    frame = comp.filter(ImageFilter.GaussianBlur(6)).convert("RGB")
    # wordmark
    dr = ImageDraw.Draw(frame)
    fb = ImageFont.truetype(fontfile(), int(H*0.11))
    fm = ImageFont.truetype(fontfile(), int(H*0.032))
    dr.text((W*0.05, H*0.40), "Veragensia", font=fb, fill=(255,255,255))
    dr.text((W*0.05, H*0.655), "the realm of the true agent  ·  Focusa Agent OS", font=fm, fill=SUB)
    dr.rectangle([W*0.05, H*0.60, W*0.05+424, H*0.606], fill=C1 if ph<0.5 else C2)
    # vignette
    frame = Image.blend(frame, base_gradient(W,H,G0,G1), 0.16)
    frame.save(os.path.join(OUT, f"v-{i:02d}.png"))
    print(f"frame {i:02d}")
print("done")