"""확대 검수 시트: python3 zoom.py out.jpg "SRC@l,t,r,b" ...  (SRC 는 compose.load_src 형식, 좌표는 0~1)"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose
from PIL import Image, ImageDraw
from letter import font
out, specs = sys.argv[1], sys.argv[2:]
H = 420
tiles = []
for sp in specs:
    src, _, box = sp.partition("@")
    im = compose.load_src(src)
    l, t, r, b = [float(v) for v in box.split(",")]
    c = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    c = c.resize((max(1, int(c.width * H / c.height)), H), Image.LANCZOS)
    d = ImageDraw.Draw(c); d.rectangle([0, 0, 118, 22], fill=(255, 230, 0)); d.text((3, 2), src, font=font("sans_b", 15), fill=(0, 0, 0))
    tiles.append(c)
rows, row, w = [], [], 0
for t in tiles:
    if row and w + t.width > 2000:
        rows.append(row); row, w = [], 0
    row.append(t); w += t.width + 8
rows.append(row)
sheet = Image.new("RGB", (max(sum(t.width + 8 for t in r) for r in rows), H * len(rows) + 8 * (len(rows) - 1)), (255, 0, 255))
y = 0
for r in rows:
    x = 0
    for t in r:
        sheet.paste(t, (x, y)); x += t.width + 8
    y += H + 8
sheet.save(out, quality=88); print(out, sheet.size)
