"""python3 build_ep.py 1  →  site/ep01/001.jpg… 와 검수용 미리보기."""
import importlib, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]
SITE = ROOT.parent / "site"

def main(n):
    lay = importlib.import_module("ep%02d_layout" % n)
    logo = Image.open(ROOT / "sheets" / "LOGO.png")
    canvas = compose.compose(lay.BLOCKS, logo_img=logo)
    out = SITE / ("ep%02d" % n)
    count, sizes = compose.slice_out(canvas, out)
    canvas.save(ROOT / "comp" / ("ep%02d_full.jpg" % n), quality=85)
    k = compose.preview(canvas, ROOT / "comp" / "review" / ("ep%02d_prev.jpg" % n), cols=6, scale=0.36)
    print("ep%02d" % n, canvas.size, "slices", count, "last", sizes[-1], "previews", k)

if __name__ == "__main__":
    main(int(sys.argv[1]))
