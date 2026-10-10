"""패널 좌표 격자 미리보기: 말풍선·꼬리 좌표(0~1)를 정확히 읽기 위한 검수용 그림.

python3 gridview.py out.jpg  SRC[@l,t,r,b] ...     (SRC 예: E1-07#2, E1-09B@0.14,0.30,0.90,0.88)
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402
from letter import font  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]


def panel(src):
    name, _, crop = src.partition("@")
    im = compose.load_src(name).copy()
    if crop:
        l, t, r, b = [float(v) for v in crop.split(",")]
        im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    return name, im


def gridded(src, width=690):
    name, im = panel(src)
    im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS).convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    f = font("sans_b", 15)
    for i in range(1, 10):
        x = int(im.width * i / 10)
        y = int(im.height * i / 10)
        d.line([(x, 0), (x, im.height)], fill=(255, 40, 40, 150), width=1)
        d.line([(0, y), (im.width, y)], fill=(40, 90, 255, 150), width=1)
        d.text((x + 2, 2), ".%d" % i, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(200, 0, 0, 255))
        d.text((2, y + 1), ".%d" % i, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(0, 40, 200, 255))
    im.alpha_composite(ov)
    d = ImageDraw.Draw(im)
    d.rectangle([im.width - 150, im.height - 26, im.width, im.height], fill=(255, 230, 0, 255))
    d.text((im.width - 146, im.height - 24), "%s %dx%d" % (name, im.width, im.height), font=f, fill=(0, 0, 0, 255))
    return im.convert("RGB")


if __name__ == "__main__":
    out = sys.argv[1]
    ims = [gridded(s) for s in sys.argv[2:]]
    H = max(i.height for i in ims)
    sheet = Image.new("RGB", (sum(i.width for i in ims) + 10 * (len(ims) - 1), H), (255, 0, 255))
    x = 0
    for i in ims:
        sheet.paste(i, (x, 0))
        x += i.width + 10
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    print(out, sheet.size)
