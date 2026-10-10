"""1화 「해설」 식자 레이아웃 (식자 v2: 레퍼런스식 말풍선)."""

DARK = "#0c0e14"
WHITE = "#ffffff"


def S(h, bg=None):
    b = {"type": "space", "h": h}
    if bg:
        b["bg"] = bg
    return b


def T(*lines, style="narr", bg=None, **kw):
    b = {"type": "text", "lines": list(lines), "style": style}
    if bg:
        b["bg"] = bg
    b.update(kw)
    return b


def P(src, w=690, x="center", bubbles=(), **kw):
    b = {"type": "panel", "src": src, "w": w, "x": x, "bubbles": list(bubbles)}
    if src.endswith("R") and "crop" not in kw:   # 편집본 가장자리의 잔선 제거
        kw["crop"] = [0.006, 0.008, 0.994, 0.992]
    b.update(kw)
    return b


def B(t, x, y=0.0, tail=None, kind="speech", **kw):
    b = {"t": t, "x": x, "y": y, "kind": kind}
    if tail:
        b["tail"] = tail
    b.update(kw)
    return b


def BT(t, x, tail=None, over=0.38, kind="speech", **kw):
    """컷 위쪽 변에 걸치는 풍선."""
    return B(t, x, 0.0, tail, kind, ay="top", over=over, **kw)


def BD(t, x, tail=None, over=0.38, kind="speech", **kw):
    """컷 아래쪽 변에 걸치는 풍선."""
    return B(t, x, 1.0, tail, kind, ay="bottom", over=over, **kw)


def SFX(name, x, y, w=180, rot=0, **kw):
    return dict({"t": name, "x": x, "y": y, "kind": "sfx", "w": w, "rot": rot}, **kw)


def NOTE(t, x, y, **kw):
    return dict({"t": t, "x": x, "y": y, "kind": "note"}, **kw)


def BB(h, *bubbles, bg=None):
    b = {"type": "bubbles", "h": h, "bubbles": list(bubbles)}
    if bg:
        b["bg"] = bg
    return b


BLOCKS = [
    # ── 프롤로그 2026 ──
    S(240, DARK),
    T("2026년 10월, 국회 의원회관", style="date_dark"),
    S(40),
    P("E1-01#1", w=600, border_color="#2b2e3a"),
    S(80),
    P("E1-01#2", w=560, x="right", border_color="#2b2e3a", bubbles=[
        B("보좌관님 어디 계세요?\n의원님 무대 5분 전입니다.", 0.30, 0.20, kind="phone", size=21),
        SFX("지이잉", 0.26, 0.74, w=190, rot=-5),
    ]),
    S(180),
    P("E1-02F", w=690, border=False),
    S(130),
    T("사람들은 나를", "'괜찮은 사람'이라고 불렀다.", style="narr_dark"),
    S(80),
    P("E1-03F", w=690, border=False),
    S(150),
    T("나도 그런 줄 알았다.", style="narr_dark"),
    S(160),
    P("E1-04R", w=500, border_color="#2b2e3a"),
    S(150),
    T("서른 살이 될 때까지는.", style="narr_dark"),
    S(300),
    {"type": "logo", "h": 440, "logo_w": 380, "sub": "1화 · 해설"},
    S(200),
    {"type": "fade", "h": 520, "from": DARK, "to": WHITE},
    S(60, WHITE),
    # ── 2006 봄 ──
    T("2006년 봄, 해원초등학교", style="date"),
    S(30),
    P("E1-05", w=690, border=False),
    S(150),
    P("E1-06", w=690, border=False, bubbles=[
        BT("자, 이 문제\n풀어 볼 사람?", 0.79, tail=[0.86, 0.20], over=0.36),
        BT("저요! 저요!!", 0.26, tail=[0.48, 0.32], kind="shout", over=0.45),
    ]),
    S(120),
    P("E1-07A", w=620, x="left", bubbles=[
        BT("어? 아닌가?\n헤헤", 0.19, tail=[0.62, 0.20], over=0.22, max_len=44),
        BD("ㅋㅋㅋ 또 틀렸대~", 0.30, tail=[0.26, 0.74], kind="small", over=0.42),
    ]),
    S(60),
    P("E1-07#2", w=690, border=False),
    S(120),
    T("나서는 애들은 멍청하다."),
    S(10),
    T("모르면서 손부터 들고,", "틀리면 웃고,", "웃으면 다 괜찮은 줄 안다.", style="inner"),
    S(180),
    P("E1-08#1", w=620, bubbles=[
        BT("괜찮아, 괜찮아.\n진우는 용기가 있잖니.", 0.68, tail=[0.42, 0.18], over=0.40),
    ]),
    S(50),
    P("E1-08#2", w=620, bubbles=[
        BD("선생님은 너희 눈만 봐도\n다 알아.", 0.66, tail=[0.56, 0.62], over=0.34),
    ]),
    S(120),
    T("아무것도 모르면서.", style="inner"),
    S(40),
    T("아는 척하는 어른과는", "가까이하지 않는다."),
    S(150),
    P("E1-09B", w=690, border=False),
    S(100),
    T("규칙은 하나씩 늘어 갔다.", style="inner"),
    S(280),
    P("E1-10R", w=690, border=False, bubbles=[
        BT("미, 미안해!\n미안…", 0.62, tail=[0.57, 0.24], over=0.26),
        BT("백유리 또야?", 0.20, tail=[0.27, 0.20], kind="small", over=0.36),
        SFX("와르르", 0.20, 0.915, w=235, rot=-7),
    ]),
    S(50),
    P("E1-10#2", w=690, border=False),
    S(100),
    T("쉬운 애는 한눈에 보인다."),
    S(150),
    P("E1-11", w=690, border=False, bubbles=[
        BT("괜찮아?\n내가 주워 줄게.", 0.47, tail=[0.66, 0.24], over=0.34),
        BT("…고마워.", 0.115, tail=[0.21, 0.28], kind="small", over=0.55),
    ]),
    S(110),
    T("그날, 나는 친구를 골랐다."),
    S(480),
    # ── 배역 ──
    P("E1-12", w=690, border=False, bubbles=[
        BT("이번 학예회 연극은\n「벌거벗은 임금님」이에요!", 0.70, tail=[0.42, 0.22], over=0.30),
        BD("이 연극의 교훈은 뭘까요?\n바로, 정직이에요.", 0.31, tail=[0.33, 0.55], over=0.36),
    ]),
    S(140),
    P("E1-13", w=560, bubbles=[
        BT("임금님 할 사람?", 0.17, tail=[-0.10, -0.03], kind="small", over=0.30),
        B("저요!!\n제가 임금님 할래요!!", 0.10, 0.40, tail=[0.47, 0.30], kind="shout", size=25),
    ]),
    S(160),
    P("E1-14#1", w=600, x="left", bubbles=[
        BT("그리고 '임금님은 벌거벗었어요!'\n하고 외치는 아이는…\n유리가 해 볼까?", 0.60, tail=[1.12, 0.04], kind="small", over=0.25),
        BD("제, 제가요?", 0.24, tail=[0.46, 0.52], over=0.45),
        BD("유리는 거짓말을\n못 하는 얼굴이잖니.", 0.78, tail=[1.12, 0.96], kind="small", over=0.30),
    ]),
    S(120),
    P("E1-14#2", w=600, x="right", bubbles=[
        BT("해설은 세아가 해 줄래?\n세아는 목소리가 차분하니까.", 0.36, tail=[-0.10, 0.02], kind="small", over=0.30),
        B("네, 선생님.", 0.88, 0.36, tail=[0.63, 0.41], kind="small"),
    ]),
    S(140),
    T("해설은 무대 옆에 선다.", "아무도 해설을 보지 않는다."),
    S(90),
    P("E1-15", w=690, border=False, bubbles=[
        NOTE("하지만 이야기는,\n해설이 한다.", 0.50, 0.90, size=33),
    ]),
    S(480),
    # ── 저녁 식탁 ──
    T("그날 저녁", style="date"),
    S(30),
    P("E1-16", w=690, border=False, bubbles=[
        BT("학예회? 우리 세아는\n무슨 역 하는데?", 0.29, tail=[0.25, 0.34], over=0.30),
        BT("해설이요.", 0.66, tail=[0.56, 0.40], kind="small", over=0.42),
    ]),
    S(130),
    P("E1-17#1", w=600, x="left", bubbles=[
        BT("잘했다.", 0.22, tail=[0.56, 0.42], kind="small", over=0.50),
        BD("괜히 나서는 역 하지 마.\n가만히 있으면 중간은 가.", 0.50, tail=[0.70, 0.56], over=0.30),
    ]),
    S(130),
    P("E1-17R", w=600, x="right", bubbles=[
        BT("우리 세아는 착해서\n걱정이 없어.", 0.28, tail=[0.58, 0.30], over=0.30),
        B("응.", 0.06, 0.52, tail=[0.20, 0.52], kind="small"),
    ]),
    S(130),
    T("엄마 아빠에게는", "괜찮은 딸만 보여 준다."),
    S(260),
    P("E1-18#1", w=620, bubbles=[
        BT("세아야, 혹시 엄마 지갑에서\n만 원짜리 한 장 못 봤어?", 0.42, tail=[0.80, 0.22], kind="small", over=0.30),
        BD("아니? 엄마가 또\n어디 뒀겠지.", 0.26, tail=[0.46, 0.60], over=0.34),
        BD("그런가…?\n엄마가 요즘 정신이 없네.", 0.80, tail=[0.88, 0.40], kind="small", over=0.28),
    ]),
    S(150),
    P("E1-18#2", w=690, border=False),
    S(120),
    T("돈이 필요했던 건 아니다."),
    S(30),
    T("엄마가 '내가 잊어버렸나 보다' 하고", "웃는 얼굴이, 좋았을 뿐이다."),
    S(500),
    # ── 첫 연습 ──
    T("일주일 뒤, 첫 연습", style="date"),
    S(30),
    P("E1-19", w=690, border=False, bubbles=[
        BT("임금님은\n벌거벗었어요!", 0.47, tail=[0.33, 0.24], kind="shout", over=0.34),
        BD("와아, 유리 잘한다!", 0.20, tail=[0.20, 0.72], kind="small", over=0.40),
    ]),
    S(120),
    P("E1-20#1", w=560, x="left", bubbles=[
        BT("나… 잘했어?", 0.76, tail=[0.58, 0.44], over=0.34),
    ]),
    S(60),
    P("E1-20#2", w=560, x="right", bubbles=[
        SFX("꾸깃", 0.20, 0.60, w=165, rot=-6),
    ]),
    S(120),
    T("유리는 잘했다."),
    S(100),
    T("너무 잘했다."),
    S(580),
    # ── 신발장 ──
    P("E1-21", w=690, border=False, bubbles=[
        B("유리야.", 0.87, 0.14, tail=[0.73, 0.13], kind="small"),
        B("응?", 0.12, 0.25, tail=[0.27, 0.40], kind="small"),
    ]),
    S(130),
    P("E1-22aR", w=600, x="right", bubbles=[
        BT("아까 너 대사할 때…\n애들이 웃었던 거 알아?", 0.30, tail=[0.70, 0.60], over=0.40),
    ]),
    S(60),
    P("E1-22bR", w=600, x="left", bubbles=[
        BT("…어?", 0.82, tail=[0.62, 0.46], kind="small", over=0.50),
        BD("나, 잘했는데…\n다들 박수 쳤잖아…", 0.66, tail=[0.56, 0.74], over=0.30),
    ]),
    S(140),
    P("E1-23aR", w=620, bubbles=[
        BT("그거, 웃겨서 친 거야.", 0.24, tail=[0.42, 0.26], over=0.26),
        BT("너 목소리 엄청 떨렸어.", 0.76, tail=[0.52, 0.27], over=0.26),
        BD("진우가 뒤에서 흉내도 냈어.", 0.34, tail=[0.44, 0.40], over=0.34),
    ]),
    S(130),
    P("E1-23bR", w=560, bubbles=[
        BT("진짜…?", 0.16, tail=[0.42, 0.50], kind="small", over=0.50),
        BD("나… 몰랐어…", 0.82, tail=[0.60, 0.62], kind="small", over=0.45),
    ]),
    S(150),
    P("E1-24", w=690, border=False, bubbles=[
        B("내가 연습\n도와줄게.", 0.17, 0.115, tail=[0.56, 0.17], kind="small", group="h"),
        B("대신 이건 우리 둘만의\n비밀이야.", 0.21, 0.243, kind="small", group="h"),
        SFX("꼬옥", 0.26, 0.58, w=150, rot=-8),
        BD("괜찮아,\n내가 있잖아.", 0.20, tail=[0.56, 0.30], kind="whisper", over=0.34),
    ]),
    S(780),
    P("E1-25", w=690, border=False),
    S(540),
    T("아무도 웃지 않았다.", style="big"),
    S(660),
    T("〈계속〉", style="end", align="right", cx=626),
    S(220),
    T("본색 1화 「해설」", "기획·각본·콘티·연출 Claude  ·  작화 GPT Image 2.5 Sunburst  ·  식자 코드", style="credit"),
    S(120),
]
