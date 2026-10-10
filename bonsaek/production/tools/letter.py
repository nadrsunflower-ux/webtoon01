"""「본색」 식자 v2 — 레퍼런스(네이버 「똑 닮은 딸」)의 식자 디자인을 따른 말풍선·효과음 렌더러.

디자인 규칙
  · 대사 27px(690폭 기준), 풍선은 글자보다 훨씬 넉넉하게, 살짝 불규칙한 둥근 사각-타원(초타원).
  · 꼬리는 풍선 외곽선에서 그대로 흘러나오는 휜 뿔 모양. 같은 group 의 풍선은 하나의 외곽선으로 합쳐진다.
  · 외침은 크기가 제각각인 가시 + 오목한 변, 굵은 기울임 글자.
  · 속삭임은 점선 외곽선과 작은 글자. 마이크 해설은 각진 상자와 번개 꼬리.
  · 그림 위 내레이션은 흰 명조 + 검은 외곽선. 효과음은 붓펜 손글씨 소재(sfx/*.png)를 회전·확대해 얹는다.
"""
import hashlib
import math
import pathlib
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
SFX_DIR = ROOT / "sfx"
SS = 4
INK = (20, 18, 24, 255)
WHITE = (255, 255, 255, 255)

FONT_FILES = {
    "sans": "Pretendard-Medium.otf", "sans_sb": "Pretendard-SemiBold.otf", "sans_b": "Pretendard-Bold.otf",
    "sans_x": "Pretendard-ExtraBold.otf", "serif": "NanumMyeongjo-Bold.ttf", "serif_b": "NanumMyeongjo-ExtraBold.ttf",
    "serif_l": "GowunBatang-Regular.ttf", "pen": "NanumPenScript-Regular.ttf",
}
_fonts = {}


def font(name, size):
    key = (name, int(size))
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(str(FONTS / FONT_FILES[name]), int(size))
    return _fonts[key]


def hexc(c, alpha=255):
    if isinstance(c, tuple):
        return c if len(c) == 4 else c + (alpha,)
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4)) + (alpha,)


def rng_for(text, salt=""):
    return random.Random(int(hashlib.md5((text + salt).encode()).hexdigest()[:8], 16))


# ───────────── 글자 측정·그리기 ─────────────
def ink_metrics(f):
    l, t, r, b = f.getbbox("국밥")
    return t, b  # 글자 잉크의 위/아래 오프셋


def tidy(text):
    """웹툰 식자 관례: 말줄임표는 가운데 점 세 개."""
    return text.replace("……", "······").replace("…", "···")


def measure(lines, f, lh):
    widths = [f.getlength(s) for s in lines]
    top, bot = ink_metrics(f)
    line_h = f.size * lh
    block_h = line_h * (len(lines) - 1) + (bot - top)
    return widths, line_h, block_h, top


def draw_text_block(img, cx, cy, lines, f, lh, fill, align="center", stroke=0, stroke_fill=None, shear=0.0):
    """(cx, cy)를 글자 덩어리의 중심으로 삼아 그린다. shear>0 이면 기울임(오블리크)."""
    widths, line_h, block_h, top = measure(lines, f, lh)
    maxw = max(widths) if widths else 0
    pad = int(f.size * 0.6) + stroke * 2
    lw, lhh = int(maxw + pad * 2), int(block_h + pad * 2)
    layer = Image.new("RGBA", (lw, lhh), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    y = pad - top
    for s, w in zip(lines, widths):
        x = pad + {"center": (maxw - w) / 2, "left": 0, "right": maxw - w}[align]
        d.text((x, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill)
        y += line_h
    if shear:
        layer = layer.transform(layer.size, Image.AFFINE, (1, shear, -shear * lhh / 2, 0, 1, 0), resample=Image.BICUBIC)
    img.alpha_composite(layer, (int(round(cx - lw / 2)), int(round(cy - lhh / 2))))
    return maxw, block_h


# ───────────── 풍선 모양 ─────────────
def superellipse_r(theta, a, b, n):
    c, s = abs(math.cos(theta)), abs(math.sin(theta))
    return ((c / a) ** n + (s / b) ** n) ** (-1.0 / n)


def fit_shape(widths, line_h, block_h, n, pad_x, pad_y, roomy=(1.10, 1.16)):
    """글줄이 모두 들어가는 초타원 반지름(a, b). 레퍼런스처럼 넉넉하게 키운다."""
    pts = []
    for i, w in enumerate(widths):
        yc = -block_h / 2 + i * line_h + (block_h - line_h * (len(widths) - 1)) / 2
        half_line = (block_h - line_h * (len(widths) - 1)) / 2
        for yy in (yc - half_line, yc + half_line):
            pts.append((w / 2 + pad_x, abs(yy) + pad_y))
    ymax = max(p[1] for p in pts)
    text_w, text_h = max(widths), block_h
    pref = min(1.95, max(1.12, (text_w + 2 * pad_x) / (text_h + 2 * pad_y) * 0.80))
    best = None
    b = ymax + 2
    while b < ymax + 260:
        a = max(p[0] / max(1e-6, 1 - (p[1] / b) ** n) ** (1.0 / n) for p in pts)
        cost = a * b * (1 + 0.5 * abs(math.log((a / b) / pref)))
        if best is None or cost < best[0]:
            best = (cost, a, b)
        b += 2
    _, a, b = best
    return a * roomy[0], b * roomy[1]


def organic_path(cx, cy, a, b, n, seed_text, wobble=1.0, samples=260):
    rnd = rng_for(seed_text, "shape")
    ph = [rnd.uniform(0, 2 * math.pi) for _ in range(3)]
    amp = [0.020 * wobble, 0.013 * wobble, 0.006 * wobble]
    rot = math.radians(rnd.uniform(-2.5, 2.5))

    def radius(theta):
        t = theta - rot
        r = superellipse_r(t, a, b, n)
        return r * (1 + amp[0] * math.sin(2 * t + ph[0]) + amp[1] * math.sin(3 * t + ph[1]) + amp[2] * math.sin(5 * t + ph[2]))

    return radius


def tail_points(cx, cy, radius, target, base=15, max_len=62, gap=16, bend=None, seed_text=""):
    """풍선 외곽에서 target 쪽으로 뻗는 휜 꼬리. (phi, delta, 꼬리 폴리라인) 반환."""
    tx, ty = target
    phi = math.atan2(ty - cy, tx - cx)
    r0 = radius(phi)
    px, py = cx + r0 * math.cos(phi), cy + r0 * math.sin(phi)
    dist = math.hypot(tx - px, ty - py)
    L = max(22.0, min(max_len, dist - gap))
    ux, uy = math.cos(phi), math.sin(phi)
    if dist > 1:
        ux, uy = (tx - px) / dist, (ty - py) / dist
    tip = (px + ux * L, py + uy * L)
    delta = base / r0
    b1 = (cx + radius(phi - delta) * math.cos(phi - delta), cy + radius(phi - delta) * math.sin(phi - delta))
    b2 = (cx + radius(phi + delta) * math.cos(phi + delta), cy + radius(phi + delta) * math.sin(phi + delta))
    if bend is None:
        rnd = rng_for(seed_text, "tail")
        bend = rnd.choice([-1, 1]) * rnd.uniform(0.14, 0.24)
    nx, ny = -uy, ux
    k = bend * L

    def quad(p0, c, p1, steps=14):
        out = []
        for i in range(steps + 1):
            t = i / steps
            out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * c[0] + t * t * p1[0],
                        (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * c[1] + t * t * p1[1]))
        return out

    c1 = ((b1[0] + tip[0]) / 2 + nx * k, (b1[1] + tip[1]) / 2 + ny * k)
    c2 = ((b2[0] + tip[0]) / 2 + nx * k, (b2[1] + tip[1]) / 2 + ny * k)
    return phi, delta, quad(b1, c1, tip) + quad(tip, c2, b2)[1:]


def bubble_outline(cx, cy, a, b, n, seed_text, target=None, tail_kw=None, samples=260):
    radius = organic_path(cx, cy, a, b, n, seed_text)
    if target is None:
        return [(cx + radius(2 * math.pi * i / samples) * math.cos(2 * math.pi * i / samples),
                 cy + radius(2 * math.pi * i / samples) * math.sin(2 * math.pi * i / samples)) for i in range(samples)]
    phi, delta, tail = tail_points(cx, cy, radius, target, seed_text=seed_text, **(tail_kw or {}))
    pts = []
    start, end = phi + delta, phi - delta + 2 * math.pi
    for i in range(samples + 1):
        t = start + (end - start) * i / samples
        pts.append((cx + radius(t) * math.cos(t), cy + radius(t) * math.sin(t)))
    return pts + tail


def shout_outline(cx, cy, a, b, seed_text, target=None, max_len=70):
    """크기가 제각각인 가시와 오목한 변으로 된 외침 풍선. 꼬리는 좁은 가시 하나를 길게 뺀다."""
    rnd = rng_for(seed_text, "shout")
    per = math.pi * (3 * (a + b) - math.sqrt((3 * a + b) * (a + 3 * b)))
    k = max(9, int(round(per / 62)))
    base = rnd.uniform(0, 2 * math.pi)
    angs = sorted(base + 2 * math.pi * (i + rnd.uniform(-0.22, 0.22)) / k for i in range(k))
    tips = []
    for t in angs:
        r = superellipse_r(t, a, b, 2.2) * (1 + rnd.uniform(0.06, 0.22))
        tips.append((cx + r * math.cos(t), cy + r * math.sin(t), t))
    pts = []
    for i in range(k):
        x0, y0, t0 = tips[i]
        x1, y1, t1 = tips[(i + 1) % k]
        if t1 < t0:
            t1 += 2 * math.pi
        tm = (t0 + t1) / 2
        rv = superellipse_r(tm, a, b, 2.2) * rnd.uniform(0.80, 0.88)
        cxm, cym = cx + rv * math.cos(tm), cy + rv * math.sin(tm)
        for s_ in range(12):
            u = s_ / 12
            pts.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cxm + u * u * x1,
                        (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cym + u * u * y1))
    if target is None:
        return pts
    phi = math.atan2(target[1] - cy, target[0] - cx)
    r_edge = superellipse_r(phi, a, b, 2.2)
    half = 15.0 / r_edge
    dist = math.hypot(target[0] - cx, target[1] - cy)
    r_tip = min(r_edge + max_len, max(r_edge + 30, dist - 14))
    tip = (cx + r_tip * math.cos(phi), cy + r_tip * math.sin(phi))

    def rel(p):
        ang = math.atan2(p[1] - cy, p[0] - cx)
        return (ang - phi + math.pi) % (2 * math.pi) - math.pi

    kept = [p for p in pts if abs(rel(p)) > half]
    n = len(kept)
    idx = max(range(n), key=lambda i: (rel(kept[i]) < 0 and rel(kept[(i + 1) % n]) > 0, -abs(rel(kept[i]))))
    return kept[:idx + 1] + [tip] + kept[idx + 1:]


def box_outline(cx, cy, a, b, seed_text, target=None):
    """마이크·방송 음성용 각진 상자. 모서리가 살짝 어긋난 손그림 사각형 + 번개 꼬리."""
    rnd = rng_for(seed_text, "box")
    j = lambda: rnd.uniform(-3.0, 3.0)
    tl, tr = (cx - a + j(), cy - b + j()), (cx + a + j(), cy - b + j())
    br, bl = (cx + a + j(), cy + b + j()), (cx - a + j(), cy + b + j())
    pts = [tl, tr]
    if target is None:
        return pts + [br, bl]
    tx, ty = target
    # 꼬리는 target 에 가장 가까운 변에서 번개 모양으로
    side = "bottom" if ty > cy + b else "top" if ty < cy - b else ("right" if tx > cx else "left")
    def bolt(p, q, away):
        # 변의 가운데에서 target 쪽으로 꺾이는 번개 모양(밑변 → 꺾임 → 끝 → 꺾임 → 밑변)
        t_ = 0.5
        if side in ("bottom", "top"):
            t_ = min(0.82, max(0.18, (tx - min(p[0], q[0])) / (abs(q[0] - p[0]) or 1)))
            if p[0] > q[0]:
                t_ = 1 - t_
        mx, my = p[0] + (q[0] - p[0]) * t_, p[1] + (q[1] - p[1]) * t_
        dx, dy = tx - mx, ty - my
        d = math.hypot(dx, dy) or 1
        L = min(66, max(38, d - 12))
        ux, uy = dx / d, dy / d
        nx, ny = -uy, ux
        w = 13
        return [(mx - away[0] * w, my - away[1] * w),
                (mx + ux * L * 0.52 - nx * 5, my + uy * L * 0.52 - ny * 5),
                (mx + ux * L * 0.42 + nx * 13, my + uy * L * 0.42 + ny * 13),
                (mx + ux * L, my + uy * L),
                (mx + ux * L * 0.50 + nx * 3, my + uy * L * 0.50 + ny * 3),
                (mx + ux * L * 0.60 - nx * 13, my + uy * L * 0.60 - ny * 13),
                (mx + away[0] * w, my + away[1] * w)]
    if side == "bottom":
        return [tl, tr, br] + bolt(br, bl, (-1, 0)) + [bl]
    if side == "top":
        return [tl] + bolt(tl, tr, (1, 0)) + [tr, br, bl]
    if side == "right":
        return [tl, tr] + bolt(tr, br, (0, 1)) + [br, bl]
    return [tl, tr, br, bl] + bolt(bl, tl, (0, -1))


def stroke_path(d, pts, color, width, dashed=None):
    closed = pts + [pts[0]]
    if not dashed:
        d.line(closed, fill=color, width=width, joint="curve")
        r = width / 2
        for x, y in pts[::6]:
            d.ellipse([x - r, y - r, x + r, y + r], fill=color)
        return
    on, off = dashed
    acc, draw_on, seg = 0.0, True, [closed[0]]
    for p, q in zip(closed, closed[1:]):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        pos = 0.0
        while pos < L:
            lim = on if draw_on else off
            step = min(lim - acc, L - pos)
            pos += step
            acc += step
            pt = (p[0] + dx * pos / L, p[1] + dy * pos / L)
            if draw_on:
                seg.append(pt)
            if acc >= lim - 1e-6:
                if draw_on and len(seg) > 1:
                    d.line(seg, fill=color, width=width, joint="curve")
                    r = width / 2
                    for x, y in (seg[0], seg[-1]):
                        d.ellipse([x - r, y - r, x + r, y + r], fill=color)
                draw_on = not draw_on
                acc = 0.0
                seg = [pt]
    if draw_on and len(seg) > 1:
        d.line(seg, fill=color, width=width, joint="curve")


# ───────────── 풍선 종류별 설정 ─────────────
KIND = {
    #            font      size lh    n     pad      line  roomy
    "speech":  ("sans_sb",  27, 1.44, 2.90, (22, 15), 2.8, (1.08, 1.16)),
    "small":   ("sans_sb",  22, 1.44, 2.90, (18, 13), 2.5, (1.08, 1.16)),
    "whisper": ("sans",     22, 1.44, 2.90, (18, 13), 2.2, (1.08, 1.16)),
    "shout":   ("sans_x",   30, 1.38, 2.20, (22, 16), 3.0, (1.06, 1.10)),
    "box":     ("serif",    25, 1.50, 2.00, (22, 16), 2.6, (1.0, 1.0)),
}


def layout_bubble(bub, box):
    """풍선 하나의 기하를 계산한다(전역 좌표)."""
    kind = bub.get("kind", "speech")
    fname, size, lh, n, pad, line, roomy = KIND[kind]
    size = bub.get("size", size)
    f = font(bub.get("font", fname), size)
    lines = tidy(bub["t"]).split("\n")
    widths, line_h, block_h, top = measure(lines, f, lh)
    x0, y0, bw, bh = box
    cx, cy = x0 + bub["x"] * bw, y0 + bub["y"] * bh
    if kind == "box":
        a, b = max(widths) / 2 + pad[0], block_h / 2 + pad[1]
    else:
        a, b = fit_shape(widths, line_h, block_h, n, pad[0], pad[1], roomy)
        a, b = max(a, size * 2.1), max(b, size * 1.45)
    a *= bub.get("sx", 1.0)
    b *= bub.get("sy", 1.0)
    # ay: 패널 위/아래 변에 걸치기. over = 풍선 높이 중 패널 안으로 들어오는 비율(0~1), dy = 추가 이동(px)
    if bub.get("ay") == "top":
        cy = y0 + b * (2 * bub.get("over", 0.35) - 1) + bub.get("dy_px", 0)
    elif bub.get("ay") == "bottom":
        cy = y0 + bh - b * (2 * bub.get("over", 0.35) - 1) + bub.get("dy_px", 0)
    if "px" in bub:
        cx = x0 + bub["px"]
    target = None
    if bub.get("tail"):
        target = (x0 + bub["tail"][0] * bw, y0 + bub["tail"][1] * bh)
    return {"kind": kind, "font": f, "lh": lh, "n": n, "line": bub.get("line", line), "lines": lines,
            "cx": cx, "cy": cy, "a": a, "b": b, "target": target, "bub": bub}


def geometry(g):
    b = g["bub"]
    seed = b["t"] + str(round(g["cx"])) + str(round(g["cy"]))
    kw = {k: b[k] for k in ("max_len", "base", "gap", "bend") if k in b}
    if g["kind"] == "shout":
        return shout_outline(g["cx"], g["cy"], g["a"], g["b"], seed, g["target"], max_len=b.get("max_len", 70))
    if g["kind"] == "box":
        return box_outline(g["cx"], g["cy"], g["a"], g["b"], seed, g["target"])
    return bubble_outline(g["cx"], g["cy"], g["a"], g["b"], g["n"], seed, g["target"], kw)


def clamp_into_canvas(g, width, margin=6):
    """풍선이 원고 좌우 밖으로 나가지 않게 민다."""
    ext = g["a"] * (1.28 if g["kind"] == "shout" else 1.04)
    if g["cx"] - ext < margin:
        g["cx"] = margin + ext
    if g["cx"] + ext > width - margin:
        g["cx"] = width - margin - ext


def render_bubbles(canvas, bubs, box, report=None):
    """한 패널(또는 풍선 블록)의 풍선들을 그린다. group 이 같은 풍선은 외곽선이 합쳐진다."""
    geos = []
    for bub in bubs:
        if bub.get("kind", "speech") in KIND:
            g = layout_bubble(bub, box)
            clamp_into_canvas(g, canvas.width)
            geos.append(g)
    groups = {}
    for i, g in enumerate(geos):
        groups.setdefault(g["bub"].get("group", "_%d" % i), []).append(g)
    for grp in groups.values():
        outlines = [geometry(g) for g in grp]
        xs = [p[0] for o in outlines for p in o]
        ys = [p[1] for o in outlines for p in o]
        m = 14
        lx, ly = int(min(xs)) - m, int(min(ys)) - m
        lw, lh_ = int(max(xs)) + m - lx, int(max(ys)) + m - ly
        layer = Image.new("RGBA", (lw * SS, lh_ * SS), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        scaled = [[((x - lx) * SS, (y - ly) * SS) for x, y in o] for o in outlines]
        for g, o in zip(grp, scaled):
            ink = hexc(g["bub"].get("ink", "#141218"))
            w = int(round(g["line"] * SS * 2))
            if g["kind"] == "whisper":
                continue
            stroke_path(d, o, ink, w)
        for g, o in zip(grp, scaled):
            d.polygon(o, fill=hexc(g["bub"].get("fill", "#ffffff")))
        for g, o in zip(grp, scaled):
            if g["kind"] == "whisper":
                stroke_path(d, o, hexc(g["bub"].get("ink", "#2a2730")), int(round(g["line"] * SS)), dashed=(11 * SS, 7 * SS))
        small = layer.resize((lw, lh_), Image.LANCZOS)
        canvas.alpha_composite(small, (lx, ly))
        for g in grp:
            b = g["bub"]
            col = hexc(b.get("color", "#141218"))
            shear = 0.16 if g["kind"] == "shout" else 0.0
            draw_text_block(canvas, g["cx"], g["cy"] + b.get("dy", 0), g["lines"], g["font"], g["lh"], col, shear=shear)
            if report is not None:
                report.append((g["cx"] - g["a"], g["cy"] - g["b"], g["cx"] + g["a"], g["cy"] + g["b"], b["t"].replace("\n", " ")))
    # 풍선이 아닌 요소
    for bub in bubs:
        k = bub.get("kind", "speech")
        x0, y0, bw, bh = box
        cx, cy = x0 + bub["x"] * bw, y0 + bub["y"] * bh
        if k == "note":      # 그림 위 내레이션: 흰 명조 + 검은 외곽선(또는 반대)
            f = font(bub.get("font", "serif_b"), bub.get("size", 31))
            draw_text_block(canvas, cx, cy, tidy(bub["t"]).split("\n"), f, bub.get("lh", 1.5), hexc(bub.get("color", "#ffffff")),
                            align=bub.get("align", "center"), stroke=bub.get("stroke", 4),
                            stroke_fill=hexc(bub.get("stroke_color", "#16141c")))
        elif k == "plain":   # 외곽선 없는 글자(손글씨 등)
            f = font(bub.get("font", "pen"), bub.get("size", 26))
            draw_text_block(canvas, cx, cy, bub["t"].split("\n"), f, bub.get("lh", 1.3), hexc(bub.get("color", "#3c3a48")),
                            align=bub.get("align", "center"))
        elif k == "phone":
            draw_phone_card(canvas, cx, cy, bub)
        elif k == "sfx":
            draw_sfx(canvas, cx, cy, bub)
        elif k == "mark":
            draw_mark(canvas, cx, cy, bub)


def draw_phone_card(canvas, cx, cy, bub):
    f = font("sans_sb", bub.get("size", 22))
    fa = font("sans", 15)
    lines = bub["t"].split("\n")
    widths, line_h, block_h, top = measure(lines, f, 1.42)
    w, h = max(widths) + 44, block_h + 62
    x0, y0 = cx - w / 2, cy - h / 2
    layer = Image.new("RGBA", (int(w + 40) * SS, int(h + 40) * SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = 20 * SS
    d.rounded_rectangle([20 * SS, 24 * SS, (w + 20) * SS, (h + 24) * SS], radius=r, fill=(0, 0, 0, 90))
    layer = layer.filter(ImageFilter.GaussianBlur(7 * SS))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([20 * SS, 20 * SS, (w + 20) * SS, (h + 20) * SS], radius=r, fill=(236, 238, 243, 246))
    canvas.alpha_composite(layer.resize((int(w + 40), int(h + 40)), Image.LANCZOS), (int(x0 - 20), int(y0 - 20)))
    d2 = ImageDraw.Draw(canvas)
    d2.rounded_rectangle([x0 + 18, y0 + 14, x0 + 36, y0 + 32], radius=5, fill=(52, 199, 89, 255))
    d2.text((x0 + 44, y0 + 13), bub.get("app", "메시지"), font=fa, fill=(96, 99, 110, 255))
    tw = fa.getlength("지금")
    d2.text((x0 + w - 18 - tw, y0 + 13), "지금", font=fa, fill=(128, 131, 142, 255))
    y = y0 + 42 - top
    for s in lines:
        d2.text((x0 + 20, y), s, font=f, fill=(24, 24, 30, 255))
        y += line_h


def draw_mark(canvas, cx, cy, bub):
    """작은 만화 기호. t: 'startle'(놀람 선 세 개) | 'shake'(떨림 물결선 두 줄)."""
    S = SS
    size = bub.get("size", 30)
    rot = math.radians(bub.get("rot", 0))
    col = hexc(bub.get("color", "#141218"))
    edge = hexc(bub.get("stroke_color", "#ffffff"))
    L = Image.new("RGBA", (int(size * 4) * S, int(size * 4) * S), (0, 0, 0, 0))
    d = ImageDraw.Draw(L)
    o = size * 2 * S
    segs = []
    if bub["t"] == "startle":
        for ang, r0, r1 in ((-0.55, 0.35, 1.0), (0.0, 0.42, 1.18), (0.55, 0.35, 1.0)):
            a = rot + ang - math.pi / 2
            segs.append([(o + math.cos(a) * size * r0 * S, o + math.sin(a) * size * r0 * S),
                         (o + math.cos(a) * size * r1 * S, o + math.sin(a) * size * r1 * S)])
    else:
        for k_ in (-1, 1):
            pts = []
            for i in range(13):
                t = i / 12 - 0.5
                x, y = k_ * size * 0.42 + math.sin(t * 9) * size * 0.07, t * size * 1.1
                pts.append((o + (x * math.cos(rot) - y * math.sin(rot)) * S, o + (x * math.sin(rot) + y * math.cos(rot)) * S))
            segs.append(pts)
    for w, c in ((int(size * 0.26 * S), edge), (int(size * 0.12 * S), col)):
        for seg in segs:
            d.line(seg, fill=c, width=max(2, w), joint="curve")
            for x, y in (seg[0], seg[-1]):
                d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=c)
    L = L.resize((L.width // S, L.height // S), Image.LANCZOS)
    canvas.alpha_composite(L, (int(cx - L.width / 2), int(cy - L.height / 2)))


_sfx_cache = {}


def draw_sfx(canvas, cx, cy, bub):
    name = bub["t"]
    if name not in _sfx_cache:
        _sfx_cache[name] = Image.open(SFX_DIR / (name + ".png")).convert("RGBA")
    im = _sfx_cache[name]
    w = bub.get("w", 180)
    im = im.resize((int(w), int(im.height * w / im.width)), Image.LANCZOS)
    if bub.get("flip"):
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if bub.get("rot"):
        im = im.rotate(bub["rot"], resample=Image.BICUBIC, expand=True)
    if bub.get("alpha", 1.0) < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * bub["alpha"]))
        im.putalpha(a)
    canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


if __name__ == "__main__":
    # 시험 렌더: 레퍼런스와 나란히 비교할 견본
    W = 690
    cv = Image.new("RGBA", (W, 1500), (255, 255, 255, 255))
    d = ImageDraw.Draw(cv)
    d.rectangle([40, 300, 650, 760], fill=(196, 208, 226, 255), outline=(20, 18, 24, 255), width=3)
    box = (40, 300, 610, 460)
    rep = []
    render_bubbles(cv, [
        {"t": "아, 물론 다\n진짜 명품은 아니고\n레플리카도 있어!", "x": 0.48, "y": -0.22, "tail": [0.25, 0.20], "group": "a"},
        {"t": "아무튼, 다 모델들이\n소품으로 쓰는 거란\n말이야.", "x": 0.25, "y": 0.42, "tail": [0.48, 0.75], "group": "a"},
        {"t": "지난번에 소명이가\n촬영장 놀러온 후에\n그 가방이 사라졌더라구.", "x": 0.72, "y": 1.22, "tail": [0.60, 0.85]},
    ], box, rep)
    box2 = (40, 980, 610, 380)
    d.rectangle([40, 980, 650, 1360], fill=(40, 40, 62, 255), outline=(20, 18, 24, 255), width=3)
    render_bubbles(cv, [
        {"t": "내 에이폰이\n사라졌어!!", "x": 0.30, "y": 0.05, "kind": "shout", "tail": [0.55, 0.45]},
        {"t": "괜찮아.\n내가 있잖아.", "x": 0.80, "y": 0.30, "kind": "whisper", "tail": [0.62, 0.62]},
        {"t": "옛날 옛적, 새 옷을 무척 좋아하는\n임금님이 살았습니다.", "x": 0.42, "y": 0.72, "kind": "box", "tail": [0.85, 0.95]},
        {"t": "…그래, 내가 참으면.", "x": 0.35, "y": 1.10, "kind": "note", "color": "#16141c", "stroke_color": "#ffffff"},
        {"t": "…뭘?", "x": 0.86, "y": 1.02, "kind": "small"},
    ], box2, rep)
    out = ROOT / "comp" / "qa" / "letter_test.png"
    cv.convert("RGB").save(out)
    print(out, rep[:2])
