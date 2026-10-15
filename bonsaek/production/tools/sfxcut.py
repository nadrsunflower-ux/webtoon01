"""효과음 시트(투명 배경, 위 4개·아래 4개)를 낱말별 PNG로 자른다.

python3 sfxcut.py sfx/SFX_C.png 지이익 딸깍 철컥 뚝 똑딱 딩동 후우 훌쩍   →  sfx/<낱말>.png
"""
import pathlib
import sys

import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[1]


def runs(occ, min_gap):
    """occ(bool 배열)에서 차 있는 구간들을 [시작, 끝) 목록으로. min_gap보다 짧은 빈칸은 이어 붙인다."""
    segs, start, gap = [], None, 0
    for i, v in enumerate(occ):
        if v:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= min_gap:
                segs.append([start, i - gap + 1])
                start, gap = None, 0
    if start is not None:
        segs.append([start, len(occ) - gap])
    return segs


def split_band(mask, n):
    occ = mask.any(axis=0)
    for g in (40, 28, 18, 12, 8):
        segs = runs(occ, g)
        if len(segs) == n:
            return segs
    segs = runs(occ, 8)
    while len(segs) > n:            # 가장 좁은 틈부터 합친다
        gaps = [segs[i + 1][0] - segs[i][1] for i in range(len(segs) - 1)]
        k = int(np.argmin(gaps))
        segs[k:k + 2] = [[segs[k][0], segs[k + 1][1]]]
    colsum = mask.sum(axis=0)
    while len(segs) < n:            # 붙어 있는 낱말: 가장 넓은 구간을 가장 비어 있는 세로줄에서 가른다
        k = int(np.argmax([b - a for a, b in segs]))
        a, b = segs[k]
        lo, hi = a + (b - a) // 5, b - (b - a) // 5
        cut = lo + int(np.argmin(colsum[lo:hi]))
        segs[k:k + 1] = [[a, cut], [cut, b]]
    return segs


def main(sheet, words):
    im = Image.open(ROOT / sheet).convert("RGBA")
    a = np.array(im)[..., 3]
    mask = a >= 100
    h = mask.shape[0]
    rows = mask.any(axis=1)
    mid_lo, mid_hi = int(h * 0.30), int(h * 0.70)
    mid = mid_lo + int(np.argmin([mask[y].sum() for y in range(mid_lo, mid_hi)]))
    out = []
    for (y0, y1), band_words in (((0, mid), words[:4]), ((mid, h), words[4:])):
        band = mask[y0:y1]
        for (x0, x1), w in zip(split_band(band, len(band_words)), band_words):
            sub = band[:, x0:x1]
            ys = np.where(sub.any(axis=1))[0]
            pad = 8
            box = (max(x0 - pad, 0), max(y0 + ys[0] - pad, 0), min(x1 + pad, im.width), min(y0 + ys[-1] + pad + 1, im.height))
            im.crop(box).save(ROOT / "sfx" / ("%s.png" % w))
            out.append((w, box))
    for w, box in out:
        print(w, box)
    del rows


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
