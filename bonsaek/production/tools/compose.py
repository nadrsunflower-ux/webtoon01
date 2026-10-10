"""「본색」 식자·편집 엔진.

레이아웃(블록 목록)을 받아 690px 폭의 긴 원고를 그리고, 1600px 단위로 잘라 저장한다.

블록 종류
  space  : {"type":"space","h":300}
  panel  : {"type":"panel","src":"E1-07#1","w":600,"x":"right","crop":[l,t,r,b],"border":True,"bubbles":[...]}
  text   : {"type":"text","lines":["…"],"style":"narr|inner|caption|big|end|date|credit","align":"center"}
  logo   : {"type":"logo","h":360,"sub":"1화 · 해설"}
모든 블록은 "bg"(배경색)를 가질 수 있다. 생략하면 직전 블록의 배경을 이어 쓴다(처음엔 흰색).

말풍선 좌표(x, y, tail)는 패널 상자 기준 0~1 비율. 0보다 작거나 1보다 크면 패널 밖(여백)으로 나간다.
  kind: speech | shout | whisper | mic | box | phone | sfx | hand | float
"""
import math
import pathlib
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import letter  # noqa: E402
from letter import font, hexc  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
FONTS = ROOT / "fonts"
W = 690


# ───────────── 원본 이미지 다루기 ─────────────
_img_cache = {}


def white_rows(im, thr=244, frac=0.985):
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    step = max(1, w // 300)
    out = []
    for y in range(h):
        cnt = tot = 0
        for x in range(0, w, step):
            tot += 1
            cnt += px[x, y] >= thr
        out.append(cnt / tot >= frac)
    return out


def trim_white(im):
    rows = white_rows(im, thr=238, frac=0.96)
    top = next((i for i, v in enumerate(rows) if not v), 0)
    bot = len(rows) - next((i for i, v in enumerate(reversed(rows)) if not v), 0)
    im = im.crop((0, top, im.width, bot))
    cols = white_rows(im.transpose(Image.Transpose.ROTATE_90), thr=238, frac=0.96)  # 세로줄 검사(회전)
    # ROTATE_90: 원래 x=0 열이 맨 아래 행이 된다
    cols = list(reversed(cols))
    left = next((i for i, v in enumerate(cols) if not v), 0)
    right = len(cols) - next((i for i, v in enumerate(reversed(cols)) if not v), 0)
    return im.crop((left, 0, right, im.height))


def shave_border(im, maxpx=10):
    """모델이 그린 검은 테두리를 깎아 낸다(이후 코드로 균일한 테두리를 다시 그림)."""
    g = im.convert("L")
    w, h = g.size

    def dark_row(y):
        return sum(g.getpixel((x, y)) for x in range(0, w, 7)) / len(range(0, w, 7)) < 110

    def dark_col(x):
        return sum(g.getpixel((x, y)) for y in range(0, h, 7)) / len(range(0, h, 7)) < 110

    t = 0
    while t < maxpx and dark_row(t):
        t += 1
    b = 0
    while b < maxpx and dark_row(h - 1 - b):
        b += 1
    l = 0
    while l < maxpx and dark_col(l):
        l += 1
    r = 0
    while r < maxpx and dark_col(w - 1 - r):
        r += 1
    pad = 2 if (t or b or l or r) else 0
    return im.crop((l + pad if l else 0, t + pad if t else 0, w - (r + pad if r else 0), h - (b + pad if b else 0)))


def split_stack(im):
    rows = white_rows(im, thr=235, frac=0.95)
    h = len(rows)
    best, run, start = (0, 0, 0), 0, 0
    for y in range(int(h * 0.2), int(h * 0.85)):
        if rows[y]:
            if run == 0:
                start = y
            run += 1
            if run > best[0]:
                best = (run, start, y)
        else:
            run = 0
    if best[0] < 7:
        raise ValueError("stack 이미지에서 흰 여백을 찾지 못함")
    _, g0, g1 = best
    return [im.crop((0, 0, im.width, g0)), im.crop((0, g1 + 1, im.width, h))]


def load_src(src):
    """'E1-07#2' → 2컷 이미지의 두 번째 컷. 'E1-02' → 단일 컷."""
    if src in _img_cache:
        return _img_cache[src]
    name, _, idx = src.partition("#")
    path = ROOT / "raw" / (name + ".png")
    if not path.exists():
        path = ROOT / "sheets" / (name + ".png")
    im = Image.open(path).convert("RGB")
    if idx:
        parts = split_stack(im)
        im = parts[int(idx) - 1]
        im = shave_border(trim_white(im))
    _img_cache[src] = im
    return im


# ───────────── 글자 블록 스타일 ─────────────
TEXT_STYLE = {
    #            font       size  lh    color
    "narr":       ("serif_b", 35, 1.60, "#17151c"),
    "narr_dark":  ("serif_b", 35, 1.60, "#f1eef7"),
    "inner":      ("serif",   28, 1.60, "#625d6e"),
    "inner_dark": ("serif",   28, 1.60, "#b3aec4"),
    "caption":    ("serif",   21, 1.55, "#625d6e"),
    "caption_dark": ("serif", 21, 1.55, "#a6a1b6"),
    "big":        ("serif_b", 46, 1.55, "#111016"),
    "big_dark":   ("serif_b", 46, 1.55, "#f4f1fa"),
    "end":        ("sans_x",  38, 1.5, "#111016"),
    "byline_k":   ("sans_x",  26, 1.5, "#111016"),
    "byline":     ("sans",    24, 1.5, "#6f6a7a"),
    "credit":     ("sans",    14, 1.7, "#8a8597"),
    "date":       ("serif",   22, 1.5, "#4b4757"),
    "date_dark":  ("serif",   22, 1.5, "#bdb8cc"),
}


def text_block_height(b):
    fname, size, lh, _ = TEXT_STYLE[b.get("style", "narr")]
    f = font(fname, b.get("size", size))
    _, line_h, block_h, _ = letter.measure([letter.tidy(x) for x in b["lines"]], f, lh)
    return int(block_h + b.get("pad", 44) * 2)


def block_height(b):
    t = b["type"]
    if t == "space":
        return b["h"]
    if t == "panel":
        im = load_src(b["src"])
        if b.get("crop"):
            l, tp, r, bt = b["crop"]
            im = im.crop((int(l * im.width), int(tp * im.height), int(r * im.width), int(bt * im.height)))
        w = b.get("w", W)
        return int(round(im.height * w / im.width)) + b.get("pad", 0) * 2
    if t == "text":
        return text_block_height(b)
    if t == "logo":
        return b.get("h", 420)
    if t in ("fade", "bubbles"):
        return b["h"]
    raise ValueError(t)


def panel_geom(b):
    im = load_src(b["src"])
    if b.get("crop"):
        l, tp, r, bt = b["crop"]
        im = im.crop((int(l * im.width), int(tp * im.height), int(r * im.width), int(bt * im.height)))
    w = b.get("w", W)
    return w, int(round(im.height * w / im.width))


def overflow(b):
    """블록의 풍선·효과음이 블록 위/아래로 넘치는 길이(px)."""
    if b["type"] == "panel":
        w, h = panel_geom(b)
    elif b["type"] == "bubbles":
        w, h = W, b["h"]
    else:
        return 0, 0
    top, bot = 0.0, 0.0
    for bub in b.get("bubbles", []):
        k = bub.get("kind", "speech")
        if k in letter.KIND:
            g = letter.layout_bubble(bub, (0, 0, w, h))
            ext = g["b"] * (1.30 if k == "shout" else 1.04)
            t0, t1 = g["cy"] - ext, g["cy"] + ext
            if g["target"] and not (0 <= g["target"][1] <= h):
                t0, t1 = min(t0, g["target"][1]), max(t1, g["target"][1])
        elif k == "sfx":
            im = Image.open(letter.SFX_DIR / (bub["t"] + ".png"))
            hh = im.height * bub.get("w", 180) / im.width * 0.62
            cy = bub["y"] * h
            t0, t1 = cy - hh, cy + hh
        elif k in ("note", "plain", "phone"):
            cy = bub["y"] * h
            t0, t1 = cy - 34, cy + 34
        else:
            continue
        top, bot = min(top, t0), max(bot, t1 - h)
    return max(0.0, -top), max(0.0, bot)


def auto_gutters(blocks, min_gap=34):
    """풍선이 컷 밖으로 나온 만큼 컷 사이 여백을 넓혀, 풍선이 이웃 컷이나 글자와 부딪히지 않게 한다."""
    out = [dict(b) for b in blocks]
    pending = 0.0      # 앞 블록에서 아래로 넘친 길이
    run = []           # 마지막 내용 블록 이후의 space 인덱스
    i = 0
    while i < len(out):
        b = out[i]
        if b["type"] == "space":
            run.append(i)
            i += 1
            continue
        up, down = overflow(b)
        need = pending + up + (min_gap if (pending or up) else 0)
        have = sum(out[j]["h"] for j in run)
        if need > have:
            if run:
                out[run[-1]]["h"] = int(out[run[-1]]["h"] + need - have)
            else:
                out.insert(i, {"type": "space", "h": int(need)})
                i += 1
        pending, run = down, []
        i += 1
    if pending:
        out.append({"type": "space", "h": int(pending + min_gap)})
    return out


def compose(blocks, logo_img=None):
    blocks = auto_gutters(blocks)
    heights = [block_height(b) for b in blocks]
    H = sum(heights)
    canvas = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    d = ImageDraw.Draw(canvas)
    y = 0
    bg = "#ffffff"
    boxes = []
    # 1단계: 배경, 그림, 글자 블록
    for b, h in zip(blocks, heights):
        bg = b.get("bg", bg)
        d.rectangle([0, y, W, y + h], fill=hexc(bg))
        if b["type"] == "panel":
            im = load_src(b["src"])
            if b.get("crop"):
                l, tp, r, bt = b["crop"]
                im = im.crop((int(l * im.width), int(tp * im.height), int(r * im.width), int(bt * im.height)))
            w = b.get("w", W)
            ph = h - b.get("pad", 0) * 2
            im = im.resize((w, ph), Image.LANCZOS)
            xs = b.get("x", "center")
            x = {"center": (W - w) // 2, "left": b.get("margin", 24), "right": W - w - b.get("margin", 24)}.get(xs, xs)
            py = y + b.get("pad", 0)
            canvas.paste(im, (x, py))
            if b.get("border", w < W):
                d.rectangle([x, py, x + w - 1, py + ph - 1], outline=hexc(b.get("border_color", "#15131a")), width=3)
            boxes.append((b, (x, py, w, ph), bg))
        elif b["type"] == "text":
            fname, size, lh, col = TEXT_STYLE[b.get("style", "narr")]
            f = font(fname, b.get("size", size))
            align = b.get("align", "center")
            cx = b.get("cx", W / 2)
            lines = [letter.tidy(x) for x in b["lines"]]
            if align != "center":
                maxw = max(f.getlength(x) for x in lines)
                cx = cx + maxw / 2 if align == "left" else cx - maxw / 2
            letter.draw_text_block(canvas, cx, y + h / 2, lines, f, lh, hexc(b.get("color", col)), align=align)
            d = ImageDraw.Draw(canvas)
        elif b["type"] == "bubbles":
            boxes.append((b, (0, y, W, h), bg))
        elif b["type"] == "fade":
            c0, c1 = hexc(b["from"]), hexc(b["to"])
            for yy in range(h):
                t_ = (yy / max(1, h - 1)) ** 1.6
                col = tuple(int(c0[i] + (c1[i] - c0[i]) * t_) for i in range(3)) + (255,)
                d.line([(0, y + yy), (W, y + yy)], fill=col)
            bg = b["to"]
        elif b["type"] == "logo" and logo_img is not None:
            lg = logo_img
            lw = b.get("logo_w", 360)
            lg = lg.resize((lw, int(lg.height * lw / lg.width)), Image.LANCZOS)
            canvas.alpha_composite(lg.convert("RGBA"), ((W - lw) // 2, int(y + h * 0.36 - lg.height / 2)))
            if b.get("sub"):
                letter.draw_text_block(canvas, W / 2, y + h * 0.76, [b["sub"]], font("serif_b", 27), 1.4,
                                       hexc(b.get("sub_color", "#d9d4e6")))
                d = ImageDraw.Draw(canvas)
        y += h
    # 2단계: 말풍선·효과음(패널 밖으로 나갈 수 있으므로 마지막에)
    report = []
    for b, box, bgc in boxes:
        letter.render_bubbles(canvas, b.get("bubbles", []), box, report)
    warn_overlaps(report)
    return canvas.convert("RGB")


def warn_overlaps(report):
    """풍선끼리 겹치거나 원고 밖으로 나가면 알려 준다(같은 group 은 report 에서 구분할 수 없으므로 참고용)."""
    n = 0
    for i in range(len(report)):
        x0, y0, x1, y1, t = report[i]
        if x0 < 2 or x1 > W - 2:
            print("  [밖] %s (x %.0f~%.0f, y %.0f)" % (t[:18], x0, x1, y0)); n += 1
        for j in range(i + 1, len(report)):
            a0, b0, a1, b1, u = report[j]
            ox = min(x1, a1) - max(x0, a0)
            oy = min(y1, b1) - max(y0, b0)
            if ox > 14 and oy > 14:
                print("  [겹침] %s × %s (y %.0f, 겹침 %dx%d)" % (t[:14], u[:14], max(y0, b0), ox, oy)); n += 1
    print("  풍선 %d개, 경고 %d건" % (len(report), n))


def slice_out(canvas, outdir, h=1600, quality=88):
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for old in outdir.glob("*.jpg"):
        old.unlink()
    n = 0
    sizes = []
    for i, top in enumerate(range(0, canvas.height, h), 1):
        part = canvas.crop((0, top, W, min(canvas.height, top + h)))
        part.save(outdir / ("%03d.jpg" % i), quality=quality, optimize=True, progressive=True)
        sizes.append(part.height)
        n = i
    return n, sizes


def preview(canvas, path, cols=6, scale=0.32):
    """검수용 축소 미리보기: 원고를 세로 단으로 잘라 나란히."""
    sw = int(W * scale)
    col_h = 2600
    small = canvas.resize((sw, int(canvas.height * scale)), Image.LANCZOS)
    ncol = math.ceil(small.height / col_h)
    sheets = []
    for s in range(0, ncol, cols):
        img = Image.new("RGB", (cols * (sw + 8), col_h), (255, 0, 255))
        for c in range(cols):
            k = s + c
            if k >= ncol:
                break
            img.paste(small.crop((0, k * col_h, sw, min(small.height, (k + 1) * col_h))), (c * (sw + 8), 0))
        sheets.append(img)
    for i, im in enumerate(sheets, 1):
        im.save(str(path).replace(".jpg", "_%d.jpg" % i), quality=80)
    return len(sheets)


if __name__ == "__main__":
    print("import this module from build_ep.py")
