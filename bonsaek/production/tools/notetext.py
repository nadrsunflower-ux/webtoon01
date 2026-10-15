"""그림 속 종이에 연필 글씨를 써 넣는다(이미지 모델이 못 그리는 경우용).

E6-03: 모델은 '왼손 + 글줄 끝에 닿은 연필'을 끝내 그리지 못했다(왼손이면 연필을 글줄 첫머리에 둔다).
그래서 빈 쪽지에 왼손만 그리게 하고(restage.py E6-03U), 글씨는 여기서 연필 끝에서 끝나도록 써 넣는다.
글씨는 종이 색 픽셀에만 곱하기로 얹어서, 손·연필 위로는 올라가지 않고 연필 그림자 안에서는 같이 어두워진다.

python3 notetext.py SRC OUT            (설정은 아래 JOBS)
"""
import math
import pathlib
import random
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"

JOBS = {
    # id: 원본, 글, 연필 끝(px), 글줄 기울기(도, +는 오른쪽으로 내려감), 글자 크기, 글꼴, 난수 씨앗
    # 연필 끝 (776,481), 쪽지 왼쪽 끝 x≈465, 손가락 마디 꼭대기 (550,467) → 글줄 길이 305px(쪽지 왼쪽 끝에서 12px 안쪽), 기울기 5.6°면 마디 위로 10px 이상 뜬다.
    "E6-03UW": dict(src="E6-03U", text="다들 그렇게 생각해요", tip=(779, 484), angle=5.6, maxw=305,
                    font="Gaegu-Regular.ttf", seed=7),
}

GRAPHITE = np.array([0.36, 0.35, 0.40])     # 연필심 색(곱하기용)


def render_line(text, font, size, seed):
    """글자마다 크기·기울기·높이를 조금씩 흔든 서툰 글줄. (알파 층, 글줄 끝의 기준점, 글줄 길이) 반환.
    글자는 글꼴의 기준선(anchor ls)에 맞춰 놓는다(잉크 상자 아래 끝에 맞추면 '렇'처럼 키 큰 글자가 떠 보인다)."""
    rnd = random.Random(seed)
    pad = size
    W, H = int(size * 1.1 * len(text) + pad * 2), int(size * 2.6)
    layer = Image.new("L", (W, H), 0)
    x, base = float(pad), int(H * 0.70)
    end = (x, base)
    for ch in text:
        if ch == " ":
            x += size * rnd.uniform(0.28, 0.38)
            continue
        s = size * rnd.uniform(0.94, 1.06)
        gf = ImageFont.truetype(str(FONTS / font), int(round(s)))
        adv = gf.getlength(ch)
        box = int(s * 2.4)
        g = Image.new("L", (box, box), 0)
        ox, oy = s * 0.5, s * 1.6                                  # 글자 상자 안의 기준선 시작점
        ImageDraw.Draw(g).text((ox, oy), ch, font=gf, fill=255, anchor="ls")
        g = g.rotate(rnd.uniform(-4, 4), resample=Image.BICUBIC, center=(ox + adv / 2, oy - s * 0.35))
        dy = rnd.uniform(-1.2, 1.2)
        layer.paste(255, (int(round(x - ox)), int(round(base + dy - oy))), g)
        x += adv * rnd.uniform(0.96, 1.04)
        end = (x, base + dy)
        x += size * rnd.uniform(0.02, 0.06)
    return layer, end, end[0] - pad


def fit_line(text, font, maxw, seed):
    """글줄 길이가 maxw 를 넘지 않는 가장 큰 글자 크기로 그린다."""
    for size in range(60, 12, -1):
        layer, end, width = render_line(text, font, size, seed)
        if width <= maxw:
            return layer, end, size
    raise ValueError("too long")


def write(job):
    src = Image.open(ROOT / "raw" / (job["src"] + ".png")).convert("RGB")
    layer, (ax, ay), size = fit_line(job["text"], job["font"], job["maxw"], job["seed"])
    print("  글자 크기", size)
    layer = layer.filter(ImageFilter.GaussianBlur(0.45))
    tx, ty = job["tip"]
    phi = math.radians(job["angle"])
    c, s = math.cos(phi), math.sin(phi)
    data = (c, s, ax - c * tx - s * ty, -s, c, ay + s * tx - c * ty)   # 원고 좌표 → 글줄 층 좌표
    alpha = np.asarray(layer.transform(src.size, Image.AFFINE, data, resample=Image.BICUBIC)).astype(float) / 255
    rng = np.random.default_rng(job["seed"])
    alpha *= 0.80 + 0.20 * rng.random(alpha.shape)                  # 연필 결
    alpha *= 0.86
    a = np.asarray(src).astype(float) / 255
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    paper = np.clip((lum - 0.62) / 0.10, 0, 1) * np.clip((0.20 - sat) / 0.06, 0, 1)   # 종이(밝고 무채색에 가까움)만
    alpha *= paper
    out = a * (1 - alpha[..., None] + alpha[..., None] * GRAPHITE)
    return Image.fromarray((out * 255).clip(0, 255).astype("uint8"))


if __name__ == "__main__":
    for jid in (sys.argv[1:] or list(JOBS)):
        im = write(JOBS[jid])
        im.save(ROOT / "raw" / (jid + ".png"))
        print("wrote raw/%s.png" % jid, im.size)
