"""「본색」 연재 사이트 생성기.

python3 build_site.py
  → bonsaek/site/        (Vercel 등에 그대로 올릴 수 있는 정적 사이트)
  → production/artifact/index_body.html  (claude.ai 아티팩트용 메인 페이지 본문)
"""
import html
import importlib
import json
import pathlib
import re
import sys

import markdown
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import shots  # noqa: E402
import fixes  # noqa: E402
import compose  # noqa: E402

PROD = pathlib.Path(__file__).resolve().parents[1]
BASE = PROD.parent
SITE = BASE / "site"
PLAN = BASE / "plan"
ASSETS = SITE / "assets"
E = html.escape

SERIES = "본색"
GENRE = "심리 스릴러 · 성장 드라마"
LOGLINE = "한 번도 앞에 나선 적 없는 모범생이, 20년에 걸쳐 자기 안의 폭력과 권력욕을 알아 간다."
SYNOPSIS = ("“나서는 애들은 멍청하다.” 친구를 길들이고, 부모를 속이고, 아는 척하는 어른을 비웃으며 자란 권세아. "
            "서른 살, 어릴 적 동창인 국회의원의 연설문을 쓰는 보좌관이 된 세아는 금 간 거울 앞에서 피 묻은 손을 씻으며 "
            "처음으로 묻는다. 나는 대체 무엇이었을까.")
EPISODES = [
    {"no": 1, "title": "해설", "thumb": "assets/thumb_ep01.jpg",
     "summary": "2006년 봄, 4학년 3반. 손부터 드는 진우, 다 안다는 담임, 필통을 쏟는 유리. 학예회 「벌거벗은 임금님」에서 해설을 맡은 세아는 그날, 친구를 하나 고른다.",
     "hook": "유리는 그날부터, 말해야 할 때 말하지 못하는 아이가 되었다.", "minutes": 4},
    {"no": 2, "title": "벌거벗은 임금님", "thumb": "assets/thumb_ep02.jpg",
     "summary": "학예회 당일, 무대 위에서 얼어붙은 유리. 세아는 그 대사를 가져가고, 박수 속에서 진우가 무대 아래로 떨어진다. 그리고 보건실에서, 진우가 웃는다.",
     "hook": "진우는 그날 무엇을 봤을까. 그리고 왜, 아무에게도 말하지 않았을까.", "minutes": 4},
]
CREDIT = ("「본색」은 오리지널 창작 웹툰입니다. 기획·각본·콘티·연출은 Claude, 작화는 AI 이미지 생성"
          "(GPT Image 2.5 Sunburst · OpenRouter)으로 만들었고, 말풍선·내레이션 식자와 효과음 배치는 코드로 넣었습니다.")

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;500;600&display=swap" rel="stylesheet">')


# ───────────── 공통 조각 ─────────────
def doc(title, body, desc="", full=True, extra_head=""):
    head = ('<title>%s</title>\n<meta name="description" content="%s">\n%s\n<link rel="stylesheet" href="series.css">%s'
            % (E(title), E(desc), FONTS, extra_head))
    if not full:
        return head + "\n" + body
    return ('<!doctype html>\n<html lang="ko">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
            '%s\n</head>\n<body>\n%s\n</body>\n</html>\n' % (head, body))


def topnav(active=""):
    items = [("index.html", "작품"), ("characters.html", "등장인물"), ("plan.html", "기획·스토리보드"), ("conti.html", "1~2화 콘티")]
    links = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if k == active else "", E(k)) for h, k in items)
    return ('<header class="site-top"><div class="shell top-in"><a class="brand" href="index.html">%s</a>'
            '<nav class="top-nav" aria-label="사이트">%s</nav></div></header>' % (SERIES, links))


def footer():
    return ('<footer class="site-foot"><div class="shell"><p>%s</p><p class="foot-small">%s · 2026</p></div></footer>'
            % (E(CREDIT), SERIES))


# ───────────── 이미지 자산 ─────────────
def save_jpg(src, dst, width=None, crop=None, quality=84):
    im = Image.open(src).convert("RGB")
    if crop:
        l, t, r, b = crop
        im = im.crop((int(l * im.width), int(t * im.height), int(r * im.width), int(b * im.height)))
    if width and im.width > width:
        im = im.resize((width, int(im.height * width / im.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, quality=quality, optimize=True, progressive=True)
    return im.size


def build_assets():
    sizes = {}
    sizes["cover"] = save_jpg(PROD / "sheets/COVER.png", ASSETS / "cover.jpg", quality=86)
    Image.open(PROD / "sheets/LOGO.png").save(ASSETS / "logo.png", optimize=True)
    for sh in ("SH1_seah10", "SH2_yuri_jinwoo10", "SH3_adults2006", "SH4_seah30", "SH5_adults2026"):
        sizes[sh] = save_jpg(PROD / "sheets" / (sh + ".png"), ASSETS / "sheets" / (sh + ".jpg"), width=1400)
    # 회차 썸네일 16:9
    sizes["t1"] = save_jpg(PROD / "raw/E1-02F.png", ASSETS / "thumb_ep01.jpg", width=480, crop=[0.0, 0.18, 1.0, 0.60])
    sizes["t2"] = save_jpg(PROD / "raw/E2-21.png", ASSETS / "thumb_ep02.jpg", width=480, crop=[0.0, 0.05, 1.0, 0.47])
    # 콘티 썸네일: 연재에 실제로 쓴 컷만, 쓴 영역 그대로
    conti = ASSETS / "conti"
    conti.mkdir(parents=True, exist_ok=True)
    for stale in conti.glob("*.jpg"):
        stale.unlink()
    for n in (1, 2):
        lay = importlib.import_module("ep%02d_layout" % n)
        for blk in lay.BLOCKS:
            if blk["type"] != "panel":
                continue
            im = compose.load_src(blk["src"])
            if blk.get("crop"):
                l, tp, r, bt = blk["crop"]
                im = im.crop((int(l * im.width), int(tp * im.height), int(r * im.width), int(bt * im.height)))
            im = im.resize((340, int(im.height * 340 / im.width)), Image.LANCZOS)
            im.save(conti / (thumb_name(blk["src"]) + ".jpg"), quality=78, optimize=True, progressive=True)
    return sizes


def thumb_name(src):
    return src.replace("#", "_")


# ───────────── 페이지: 홈 ─────────────
def page_index(full=True):
    cards = []
    for ep in EPISODES:
        cards.append(
            '<li><a class="ep-card" href="ep%02d.html"><img src="%s" alt="%d화 %s 장면" width="480" height="270" loading="lazy">'
            '<div class="ep-meta"><span class="ep-no">%d화</span><span class="ep-title">%s</span><p>%s</p>'
            '<span class="ep-time">약 %d분</span></div></a></li>'
            % (ep["no"], ep["thumb"], ep["no"], E(ep["title"]), ep["no"], E(ep["title"]), E(ep["summary"]), ep["minutes"]))
    cast = [("임금", "전진우", "정답을 몰라도 손부터 드는 아이"), ("진실을 외치는 아이", "백유리", "거짓말을 못 하는 얼굴"),
            ("해설", "권세아", "무대 옆에 서서 이야기를 쥐는 아이"), ("연출", "정미란 선생님", "“이 연극의 교훈은 정직이에요.”")]
    cast_rows = "".join('<div class="cast-row"><dt>%s</dt><dd><strong>%s</strong><span>%s</span></dd></div>' % (E(a), E(b), E(c))
                        for a, b, c in cast)
    body = topnav("작품") + """
<main class="shell">
  <section class="hero" aria-labelledby="series-title">
    <figure class="cover"><img src="assets/cover.jpg" alt="학예회 무대 옆에 선 어린 세아와, 왕관을 쓴 그녀의 그림자" width="1024" height="1536"></figure>
    <div class="hero-info">
      <p class="eyebrow">%s</p>
      <h1 id="series-title">%s</h1>
      <p class="logline">%s</p>
      <p class="synopsis">%s</p>
      <ul class="tags"><li>15세 이용가</li><li>4부 60화 기획</li><li>1~2화 공개</li></ul>
      <div class="actions"><a class="btn primary" href="ep01.html">1화부터 보기</a><a class="btn" href="plan.html">기획서와 전체 스토리보드</a></div>
    </div>
  </section>

  <section class="block" aria-labelledby="eps">
    <div class="block-head"><h2 id="eps">회차</h2><span>1~2화 · 2026년 10월</span></div>
    <ol class="ep-list">%s</ol>
    <p class="note">3화부터 60화까지는 <a href="plan.html#storyboard">전체 스토리보드</a>에 회차별 장면과 끊는 지점까지 정리되어 있습니다.</p>
  </section>

  <section class="block program" aria-labelledby="cast">
    <div class="program-card">
      <p class="program-kicker">해원초등학교 4학년 3반 학예회 · 2006</p>
      <h2 id="cast">「벌거벗은 임금님」 배역표</h2>
      <dl class="cast">%s</dl>
      <p class="program-foot">20년 뒤, 이 배역은 여의도에서 다시 무대에 오른다.</p>
    </div>
    <div class="program-side">
      <h3>이 작품을 보는 법</h3>
      <p>내레이션은 세아의 말이고, 그림은 실제로 일어난 일입니다. 둘이 어긋나는 순간마다, 글보다 그림을 믿으세요.</p>
      <p><a href="characters.html">등장인물 보기 →</a></p>
      <p><a href="conti.html">1~2화 콘티와 작화 지시서 보기 →</a></p>
    </div>
  </section>
</main>
""" % (E(GENRE), SERIES, E(LOGLINE), E(SYNOPSIS), "".join(cards), cast_rows) + footer()
    return doc("본색", body, desc=LOGLINE, full=full)


# ───────────── 페이지: 회차 뷰어 ─────────────
def page_episode(ep):
    n = ep["no"]
    files = sorted((SITE / ("ep%02d" % n)).glob("*.jpg"))
    imgs = []
    for i, f in enumerate(files):
        w, h = Image.open(f).size
        imgs.append('<img src="ep%02d/%s" alt="" width="%d" height="%d" loading="%s" decoding="async">'
                    % (n, f.name, w, h, "eager" if i < 2 else "lazy"))
    prev_btn = ('<a class="btn" href="ep%02d.html">← %d화</a>' % (n - 1, n - 1)) if n > 1 else '<span class="btn off">첫 화</span>'
    nxt = next((e for e in EPISODES if e["no"] == n + 1), None)
    next_btn = (('<a class="btn primary" href="ep%02d.html">%d화 →</a>' % (n + 1, n + 1)) if nxt
                else '<a class="btn primary" href="plan.html#storyboard">다음 이야기(기획) →</a>')
    body = """<header class="reader-bar"><div class="reader-in"><a class="reader-title" href="index.html">본색<span>%d화</span></a>
<div class="reader-meta">약 %d분<a href="index.html">목록</a></div></div><div class="progress"><i id="prog"></i></div></header>
<section class="ep-head"><p class="ep-num">— %d —</p><h1>%s</h1><p>%s</p></section>
<main class="comic" aria-label="%d화 %s 본문">%s</main>
<footer class="ep-foot"><p class="hook">%s</p><div class="ep-nav">%s%s</div>
<a class="list-link" href="index.html">전체 목록 보기</a><p class="note">%s</p></footer>
<script>
(function(){var b=document.getElementById('prog');function u(){var h=document.documentElement.scrollHeight-window.innerHeight;
b.style.width=(h>0?Math.min(100,Math.max(0,window.scrollY/h*100)):0)+'%%';}
window.addEventListener('scroll',u,{passive:true});window.addEventListener('resize',u);u();})();
</script>""" % (n, ep["minutes"], n, E(ep["title"]), E(ep["summary"]), n, E(ep["title"]), "\n".join(imgs),
                E(ep["hook"]), prev_btn, next_btn, E(CREDIT))
    return doc("본색 %d화 · %s" % (n, ep["title"]), body, desc=ep["summary"])


# ───────────── 페이지: 등장인물 ─────────────
CHAR_SECTIONS = [
    ("SH1_seah10", "권세아 · 10세", [("권세아 (權世娥)", "주인공 · 해설",
      ["턱선 단발에 일자 앞머리, 오른쪽 눈 밑의 작은 점. 인형처럼 단정한 모범생.",
       "한 번도 손을 들지 않지만 선생님이 가장 믿는 아이. 속으로는 모든 사람을 '쓸모'로 분류한다.",
       "말버릇 “괜찮아, 내가 있잖아.” / 속말 “아무것도 모르면서.”",
       "아크: 나는 영리한 아이다 → 나는 폭력적이다 → 나는 권력을 원한다 → 나는 특별하지 않다 → 이제 나는 나를 안다."])]),
    ("SH2_yuri_jinwoo10", "백유리 · 전진우 · 10세", [
     ("백유리", "쉬운 아이, 그리고 진실을 외치는 아이",
      ["갈색 곱슬 양 갈래, 처진 눈썹, 늘 손가락에 반창고.",
       "남을 의심하지 못하는 아이. 세아에게 “너는 긴장하면 다 잊어버리잖아”라는 말을 들으며 자기 기억을 믿지 못하게 된다.",
       "학예회 날 대사를 잃은 뒤 '말해야 할 때 말하지 못하는 아이'가 되고, 훗날 날짜와 사실만 적는 일기로 세아를 기록한다."]),
     ("전진우", "나서는 아이, 그리고 임금",
      ["짧은 스포츠머리, 앞니가 큰 웃음, 빨간 체육복. 학예회 이후 턱 밑에 흉터.",
       "정답을 몰라도 손부터 드는 아이. 세아가 가장 경멸하는 타입.",
       "그러나 진우는 멍청하지 않다. 학예회 날 세아의 발을 본 유일한 사람이다."])]),
    ("SH3_adults2006", "2006년의 어른들", [
     ("정미란 선생님", "4학년 3반 담임 · 아는 척하는 어른", ["“선생님은 너희 눈만 봐도 다 알아.” 연극으로 「벌거벗은 임금님」을 고르고, 교훈은 정직이라 말한다."]),
     ("이경희", "엄마", ["반찬가게를 하는 다정한 엄마. 작은 거짓말에 능하다. “우리 세아는 착해서 걱정이 없어.”"]),
     ("권태호", "아빠", ["보험회사 만년 대리. “나서지 마라. 가만히 있으면 중간은 간다.”"])]),
    ("SH4_seah30", "권세아 · 30세", [("권세아", "국회의원 전진우 의원실 수석보좌관",
      ["앞머리를 기르고 낮게 묶은 쪽머리, 차콜 정장, 파란 줄 출입증. 같은 눈매와 같은 점.",
       "임금(진우)의 연설문을 쓰는 해설. 2026년 10월, 출마 선언식 5분 전 금 간 거울 앞에서 손을 씻는다."])]),
    ("SH5_adults2026", "2026년, 여의도", [
     ("백유리 · 30세", "탐사보도 기자", ["짧은 곱슬 단발, 뿔테 안경, 카메라 가방. “이번엔 내가 기억해.”"]),
     ("전진우 · 30세", "최연소 국회의원", ["소년 같은 웃음과 턱의 흉터. 긴장하면 흉터를 만진다."]),
     ("도창민", "5선 국회의원 · 4부의 거울", ["“너 같은 애들은 냄새가 나. 나도 그랬거든.”"])]),
]


def page_characters():
    secs = []
    for sheet, cap, people in CHAR_SECTIONS:
        cards = "".join('<article class="person"><h3>%s</h3><p class="role">%s</p><ul>%s</ul></article>'
                        % (E(n), E(r), "".join("<li>%s</li>" % E(x) for x in items)) for n, r, items in people)
        secs.append('<section class="char-sec"><figure class="sheet"><img src="assets/sheets/%s.jpg" alt="%s 설정화" '
                    'loading="lazy" width="1400" height="933"><figcaption>%s 설정화</figcaption></figure>'
                    '<div class="people">%s</div></section>' % (sheet, E(cap), E(cap), cards))
    others = markdown.markdown(_section(PLAN / "01_등장인물.md", "## 그 밖의 인물"), extensions=["tables"])
    body = topnav("등장인물") + """<main class="shell doc">
<header class="doc-head"><p class="eyebrow">등장인물</p><h1>배역과 본색</h1>
<p class="lead">설정화는 작화 엔진에 참조 이미지로 함께 넣어 컷마다 얼굴·머리·옷을 고정하는 데 썼습니다.</p></header>
%s<section class="prose">%s</section></main>""" % ("".join(secs), others) + footer()
    return doc("본색 등장인물", body, desc="권세아, 백유리, 전진우와 어른들의 설정화와 인물 소개")


def _section(path, heading):
    text = path.read_text()
    i = text.find(heading)
    return text[i:] if i >= 0 else ""


# ───────────── 페이지: 기획·스토리보드 ─────────────
def parse_storyboard(path):
    parts, cur, ep = [], None, None
    for line in path.read_text().splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            cur = {"title": m.group(1), "intro": "", "eps": []}
            parts.append(cur)
            continue
        if cur is None:
            continue
        m = re.match(r"^\*\*(\d+)화 「(.+?)」\*\*\s*(\*\((.+)\)\*)?", line)
        if m:
            ep = {"no": int(m.group(1)), "title": m.group(2), "flag": m.group(4) or "", "items": []}
            cur["eps"].append(ep)
            continue
        if line.startswith("- ") and ep is not None:
            ep["items"].append(line[2:])
        elif line.strip() and not line.startswith("---") and not cur["eps"]:
            cur["intro"] += line.strip() + " "
    return parts


def inline(s):
    s = E(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    return s


def page_plan():
    plan_md = (PLAN / "00_기획서.md").read_text()
    plan_md = re.sub(r"^# .+\n", "", plan_md, count=1)
    plan_html = markdown.markdown(plan_md, extensions=["tables"])
    parts = parse_storyboard(PLAN / "02_전체_스토리보드.md")
    blocks = []
    for k, p in enumerate(parts):
        rows = []
        for ep in p["eps"]:
            scenes = [x for x in ep["items"] if not x.startswith("끊기")]
            cut = [x for x in ep["items"] if x.startswith("끊기")]
            badge = ('<span class="made">%s</span>' % E(ep["flag"])) if ep["flag"] else ""
            link = ('<a href="ep%02d.html">%d화</a>' % (ep["no"], ep["no"])) if ep["no"] <= len(EPISODES) else "%d화" % ep["no"]
            rows.append('<li class="sb-ep"><div class="sb-no">%s</div><div class="sb-body"><h4>「%s」%s</h4>%s%s</div></li>'
                        % (link, E(ep["title"]), badge, "".join("<p>%s</p>" % inline(x) for x in scenes),
                           "".join('<p class="cut">%s</p>' % inline(x.replace("끊기:", "", 1).strip()) for x in cut)))
        blocks.append('<details class="sb-part"%s><summary><span class="sb-part-title">%s</span><span class="sb-count">%d화</span></summary>'
                      '<p class="sb-intro">%s</p><ol class="sb-list">%s</ol></details>'
                      % (" open" if k == 0 else "", E(p["title"]), len(p["eps"]), inline(p["intro"].strip()), "".join(rows)))
    body = topnav("기획·스토리보드") + """<main class="shell doc">
<header class="doc-head"><p class="eyebrow">작품 기획서</p><h1>「본색(本色)」</h1>
<p class="lead">%s</p></header>
<section class="prose">%s</section>
<section id="storyboard" class="storyboard"><h2>전체 스토리보드 — 4부 60화</h2>
<p class="sb-guide">회차마다 주요 장면과 <span class="cut-label">끊는 지점</span>(마지막 컷)을 적었습니다. 끊는 지점은 모두 같은 공식을 따릅니다: 넓은 여백 → 한 줄 반전 → 눈 클로즈업 → 〈계속〉.</p>
%s</section></main>""" % (E(LOGLINE), plan_html, "".join(blocks)) + footer()
    return doc("본색 기획서", body, desc="로그라인, 기획 의도, 연출 규칙과 4부 60화 전체 스토리보드")


# ───────────── 페이지: 1~2화 콘티 ─────────────
def resolve(src, idx):
    """수정본(E1-22aR, E1-02F …)을 원래 컷 지시로 되돌려 찾는다."""
    import retouch
    sid, _, part = src.partition("#")
    if sid in idx:
        return sid, part
    orig = (retouch.EDITS.get(sid) or (None,))[0] or retouch.FLIPS.get(sid) or {"E1-07A": "E1-07#1", "E1-09B": "E1-09"}.get(sid)
    if orig:
        o, _, pp = orig.partition("#")
        return o, pp
    return sid, part


def shot_index():
    idx = {}
    for s in shots.EP1 + shots.EP2 + fixes.FIX:
        idx[s["id"]] = s
    return idx


def page_conti():
    idx = shot_index()
    sections = []
    total_imgs = set()
    for n in (1, 2):
        lay = importlib.import_module("ep%02d_layout" % n)
        beats = []
        k = 0
        for b in lay.BLOCKS:
            if b["type"] == "panel":
                sid, _, part = b["src"].partition("#")
                total_imgs.add(sid)
                osid, part = resolve(b["src"], idx)
                s = idx.get(osid, {})
                if s.get("layout") == "stack2":
                    desc = s["panels"][int(part or 1) - 1]["desc"]
                    tag = "%s · %s컷 중 %s" % (s["ar"], 2, part)
                else:
                    desc = s.get("desc", "")
                    tag = s.get("ar", "")
                lines = [x for x in b.get("bubbles", []) if x.get("kind") not in ("hand",)]
                talk = "".join('<li class="k-%s">%s</li>' % (x.get("kind", "speech"), E(x["t"].replace("\n", " "))) for x in lines)
                k += 1
                beats.append('<li class="beat"><img src="assets/conti/%s.jpg" alt="%s 컷" loading="lazy" width="340">'
                             '<div><p class="beat-id">#%02d · %s <span>%s</span></p><p class="beat-desc">%s</p>%s</div></li>'
                             % (thumb_name(b["src"]), sid, k, sid, E(tag), E(desc), ("<ul class=\"talk\">%s</ul>" % talk) if talk else ""))
            elif b["type"] == "bubbles":
                beats.append('<li class="beat text-beat"><p>%s</p></li>' % E(" / ".join(x["t"].replace("\n", " ") for x in b["bubbles"])))
            elif b["type"] == "text" and b.get("style") not in ("credit", "end"):
                beats.append('<li class="beat text-beat"><p>%s</p></li>' % E(" / ".join(b["lines"])))
        ep = EPISODES[n - 1]
        sections.append('<section class="conti-ep"><h2>%d화 「%s」</h2><p class="lead">%s</p><ol class="beats">%s</ol></section>'
                        % (n, E(ep["title"]), E(ep["summary"]), "".join(beats)))
    ledger = PROD / "raw" / "_eps.log"
    body = topnav("1~2화 콘티") + """<main class="shell doc">
<header class="doc-head"><p class="eyebrow">콘티 · 작화 지시서</p><h1>1~2화 컷별 연출</h1>
<p class="lead">Claude가 쓴 컷 지시(구도·연기·빛·손 처리·말풍선 자리)와 실제 생성된 그림, 그리고 식자한 대사를 연재 순서대로 나열했습니다.
작화 이미지 %d장(2컷을 한 장에 그린 이미지 포함). 검수에서 걸린 27컷은 다시 그리거나 부분 수정했습니다.</p>
<div class="spec"><h3>모든 컷에 공통으로 들어간 화풍 블록</h3><p>%s</p></div></header>
%s</main>""" % (len(total_imgs), E(shots.STYLE.replace("[화풍] ", "")), "".join(sections)) + footer()
    return doc("본색 1~2화 콘티", body, desc="컷별 연출 지시와 생성 이미지, 대사")


def write_conti_md():
    idx = shot_index()
    for n in (1, 2):
        lay = importlib.import_module("ep%02d_layout" % n)
        out = ["# 「본색」 %d화 「%s」 콘티" % (n, EPISODES[n - 1]["title"]), "",
               "연재 순서대로 컷 지시(작화 지시서의 [컷] 블록), 대사, 내레이션을 정리했다.", ""]
        k = 0
        for b in lay.BLOCKS:
            if b["type"] == "panel":
                sid, _, part = b["src"].partition("#")
                osid, part = resolve(b["src"], idx)
                s = idx.get(osid, {})
                desc = s["panels"][int(part or 1) - 1]["desc"] if s.get("layout") == "stack2" else s.get("desc", "")
                k += 1
                out.append("**#%02d · %s%s** (%s)" % (k, sid, (" 컷" + part) if part else "", s.get("ar", "")))
                out.append("- 연출: " + desc)
                for x in b.get("bubbles", []):
                    out.append("- %s: %s" % ({"speech": "대사", "shout": "외침", "whisper": "속삭임", "mic": "해설(마이크)",
                                              "box": "해설(마이크)", "phone": "알림", "sfx": "효과음", "note": "내레이션", "small": "대사"}.get(x.get("kind", "speech"), "대사"),
                                             x["t"].replace("\n", " ")))
                out.append("")
            elif b["type"] == "text" and b.get("style") not in ("credit",):
                out.append("> " + " / ".join(b["lines"]))
                out.append("")
        (PLAN / ("%02d_%d화_콘티.md" % (n + 2, n))).write_text("\n".join(out))


def main():
    build_assets()
    pages = {"index.html": page_index(), "ep01.html": page_episode(EPISODES[0]), "ep02.html": page_episode(EPISODES[1]),
             "characters.html": page_characters(), "plan.html": page_plan(), "conti.html": page_conti()}
    for name, text in pages.items():
        (SITE / name).write_text(text)
    art = PROD / "artifact"
    art.mkdir(exist_ok=True)
    (art / "index_body.html").write_text(page_index(full=False))
    write_conti_md()
    print("pages", list(pages))


if __name__ == "__main__":
    main()
