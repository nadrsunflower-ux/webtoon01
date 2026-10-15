"""얼굴의 작은 점 찾기/지우기.

python3 spots.py find RAW x0 y0 x1 y1        → 범위 안 작은 어두운 점 후보(피부 위)
python3 spots.py erase RAW OUT x,y[,r] ...   → 점을 주변 피부색으로 메운다(확산 채우기)
"""
import sys
import numpy as np
from PIL import Image


def find(path, x0, y0, x1, y1):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    g = a.mean(axis=2)
    out = []
    for y in range(y0 + 8, y1 - 8):
        row = g[y]
        for x in range(x0 + 8, x1 - 8):
            v = row[x]
            if v > 110:
                continue
            ring = np.concatenate([g[y - 7, x - 7:x + 8], g[y + 7, x - 7:x + 8], g[y - 7:y + 8, x - 7], g[y - 7:y + 8, x + 7]])
            r, gg, b = a[y - 7:y + 8:14, x - 7:x + 8:14].reshape(-1, 3).mean(axis=0)
            if ring.min() > 150 and v < ring.mean() - 60 and r > gg:      # 밝은 피부 한가운데의 어두운 점
                if g[y - 2:y + 3, x - 2:x + 3].min() >= v:
                    out.append((x, y, int(v), int(ring.mean())))
    for o in out:
        print(*o)


def erase(src, dst, pts):
    im = np.asarray(Image.open(src).convert("RGB")).astype(float)
    for p in pts:
        x, y, *rest = [float(v) for v in p.split(",")]
        r = rest[0] if rest else 5.0
        x0, y0, x1, y1 = int(x - r - 3), int(y - r - 3), int(x + r + 4), int(y + r + 4)
        patch = im[y0:y1, x0:x1].copy()
        yy, xx = np.mgrid[y0:y1, x0:x1]
        hole = np.hypot(xx + 0.5 - x, yy + 0.5 - y) < r
        for _ in range(400):                                     # 가장자리 색이 안쪽으로 번지도록
            avg = (np.roll(patch, 1, 0) + np.roll(patch, -1, 0) + np.roll(patch, 1, 1) + np.roll(patch, -1, 1)) / 4
            patch[hole] = avg[hole]
        im[y0:y1, x0:x1] = patch
    Image.fromarray(im.clip(0, 255).astype("uint8")).save(dst)
    print("erased", len(pts), "→", dst)


if __name__ == "__main__":
    if sys.argv[1] == "find":
        find(sys.argv[2], *[int(v) for v in sys.argv[3:7]])
    else:
        erase(sys.argv[2], sys.argv[3], sys.argv[4:])
