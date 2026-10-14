"""작은 점(얼굴 점) 옮기기: python3 molefix.py SRC OUT 지울x,지울y 새x,새y [반지름]"""
import math, sys
from PIL import Image, ImageDraw, ImageFilter

src, out = sys.argv[1], sys.argv[2]
ex, ey = [float(v) for v in sys.argv[3].split(",")]
nx, ny = [float(v) for v in sys.argv[4].split(",")]
r_new = float(sys.argv[5]) if len(sys.argv) > 5 else 1.8
im = Image.open(src).convert("RGB")
px = im.load()

# 지울 점의 가장 어두운 색(새 점 색으로 씀)
dark = min((px[int(ex) + dx, int(ey) + dy] for dx in range(-3, 4) for dy in range(-3, 4)), key=sum)
# 고리(반지름 6~8)의 평균 피부색으로 덮고, 가장자리는 부드럽게
ring = [px[int(ex + r * math.cos(t)), int(ey + r * math.sin(t))] for r in (6, 7, 8) for t in [i * math.pi / 12 for i in range(24)]]
skin = tuple(sum(c[i] for c in ring) // len(ring) for i in range(3))
R = 5.0
for y in range(int(ey - R - 1), int(ey + R + 2)):
    for x in range(int(ex - R - 1), int(ex + R + 2)):
        d = math.hypot(x + 0.5 - ex, y + 0.5 - ey)
        if d < R:
            a = 1.0 if d < R - 2 else (R - d) / 2
            o = px[x, y]
            px[x, y] = tuple(int(o[i] * (1 - a) + skin[i] * a) for i in range(3))

# 새 점: 4배로 그려 줄여 붙인다
S = 4
box = 6
patch = im.crop((int(nx) - box, int(ny) - box, int(nx) + box, int(ny) + box)).resize((box * 2 * S, box * 2 * S), Image.BICUBIC)
mask = Image.new("L", patch.size, 0)
cx, cy = (nx - (int(nx) - box)) * S, (ny - (int(ny) - box)) * S
ImageDraw.Draw(mask).ellipse([cx - r_new * S, cy - r_new * S, cx + r_new * S, cy + r_new * S], fill=235)
mask = mask.filter(ImageFilter.GaussianBlur(S * 0.5))
patch.paste(Image.new("RGB", patch.size, dark), (0, 0), mask)
im.paste(patch.resize((box * 2, box * 2), Image.LANCZOS), (int(nx) - box, int(ny) - box))
im.save(out)
print("erased", (ex, ey), "skin", skin, "new", (nx, ny), "color", dark)
