import sys, pathlib
from PIL import Image
P = pathlib.Path(__file__).resolve().parents[2]
ep = sys.argv[1]
src = P / "site" / ep
out = P / "production" / "comp" / "review"
files = sorted(src.glob("*.jpg"))
for i in range(0, len(files), 2):
    ims = [Image.open(f) for f in files[i:i+2]]
    W = sum(im.width for im in ims) + 12
    H = max(im.height for im in ims)
    sheet = Image.new("RGB", (W, H), (255, 0, 255))
    x = 0
    for im in ims:
        sheet.paste(im, (x, 0)); x += im.width + 12
    sheet.save(out / ("%s_p%02d.jpg" % (ep, i // 2 + 1)), quality=82)
print(len(files), "slices ->", (len(files) + 1) // 2, "pairs")
