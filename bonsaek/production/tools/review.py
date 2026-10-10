import sys, pathlib
from PIL import Image, ImageDraw, ImageFont
P = pathlib.Path(__file__).resolve().parents[1]
f = ImageFont.truetype(str(P/'fonts'/'Pretendard-Bold.otf'), 28)
names = sys.argv[2:]
out = sys.argv[1]
H = 760
ims = []
for n in names:
    im = Image.open(P/'raw'/(n+'.png')).convert('RGB')
    im = im.resize((int(im.width*H/im.height), H))
    d = ImageDraw.Draw(im); d.rectangle([0,0,130,40], fill=(255,230,0)); d.text((6,4), n, font=f, fill=(0,0,0))
    ims.append(im)
W = sum(i.width for i in ims) + 10*(len(ims)-1)
sheet = Image.new('RGB', (W, H), (255,0,255)); x=0
for i in ims: sheet.paste(i,(x,0)); x+=i.width+10
sheet.save(P/'comp'/'review'/out, quality=85)
print(out, sheet.size)
