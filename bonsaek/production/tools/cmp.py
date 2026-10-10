"""수정 전/후 비교 시트: python3 cmp.py out.jpg ID [ID ...]"""
import pathlib, sys
from PIL import Image, ImageDraw
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from letter import font
ROOT = pathlib.Path(__file__).resolve().parents[1]
out, ids = sys.argv[1], sys.argv[2:]
H = 560
rows = []
for n in ids:
    a = Image.open(ROOT / "raw" / "_src" / (n + ".png")).convert("RGB")
    b = Image.open(ROOT / "raw" / (n + ".png")).convert("RGB")
    a = a.resize((int(a.width * H / a.height), H)); b = b.resize((int(b.width * H / b.height), H))
    r = Image.new("RGB", (a.width + b.width + 8, H), (255, 0, 255)); r.paste(a, (0, 0)); r.paste(b, (a.width + 8, 0))
    d = ImageDraw.Draw(r); d.rectangle([0, 0, 120, 26], fill=(255, 230, 0)); d.text((4, 3), n, font=font("sans_b", 16), fill=(0, 0, 0))
    rows.append(r)
W = max(r.width for r in rows)
sheet = Image.new("RGB", (W, sum(r.height for r in rows) + 8 * (len(rows) - 1)), (255, 0, 255))
y = 0
for r in rows:
    sheet.paste(r, (0, y)); y += r.height + 8
sheet.save(out, quality=86); print(out, sheet.size)
