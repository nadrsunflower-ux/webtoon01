"""4화 「생일 초대장」 식자 레이아웃."""
from ep01_layout import S, T, P, B, BT, BD, SFX, NOTE, BB, DARK, WHITE

NIGHT = "#0d1020"
EDGE = "#3a3b55"

BLOCKS = [
    S(200, DARK),
    {"type": "logo", "h": 400, "logo_w": 300, "sub": "4화 · 생일 초대장"},
    S(120, DARK),
    {"type": "fade", "h": 420, "from": DARK, "to": WHITE},
    S(60, WHITE),
    T("학예회가 끝나고 2주 뒤", style="date"),
    S(30),
    P("E4-01R", w=690, border=False, bubbles=[     # 뒤쪽 아이들도 카메라 쪽을 향해 앉게 고친 편집본
        BT("임, 임금님은…\n버, 벌거…", 0.13, tail=[0.08, 0.02], kind="small", over=0.12),   # 안경 소년 얼굴을 가리지 않게
        BT("푸하하!\n똑같다!", 0.45, tail=[0.33, 0.10], kind="shout", over=0.22),
    ]),
    S(110),
    T("학예회 이후로,", "유리는 반에서 '대사 까먹은 애'가 되었다."),
    S(60),
    T("유리는 그 말을 들을 때마다", "더 작아졌다.", style="inner"),
    S(260),
    P("E4-02aR", w=600, x="left", bubbles=[     # 뒤쪽 아이들도 카메라 쪽을 향해 앉게 고친 편집본
        BT("세, 세아야…\n나 이번 주 토요일이\n생일이거든…", 0.80, tail=[0.70, 0.05], over=0.20),   # 유리 머리 위(세아 쪽이 아니라)
    ]),
    S(70),
    P("E4-02#2", w=600, x="right", bubbles=[
        BT("근데 애들한테\n이거 주는 게 너무 떨려서…", 0.30, tail=[0.40, 0.28], kind="small", over=0.38),
        BD("또 말 못 하고\n웃음거리 될 것 같아…", 0.70, tail=[0.64, 0.80], kind="small", over=0.32),
    ]),
    S(170),
    P("E4-03M", w=690, border=False, bubbles=[
        BT("그럼 내가\n대신 전해 줄게.", 0.78, tail=[0.84, 0.15], over=0.30),     # 세아(오른쪽)
        BD("지, 진짜?\n고마워, 세아야!", 0.24, tail=[0.28, 0.80], over=0.30),     # 유리(왼쪽)
    ]),
    S(140),
    P("E4-04", w=600),
    S(110),
    T("유리는 열두 장을 썼다."),
    S(40),
    T("반 아이들 이름을 하나하나,", "삐뚤빼뚤하게.", style="inner"),
    S(300),
    P("E4-05", w=690, border=False, bubbles=[
        BT("야, 집에 가자!", 0.18, tail=[0.25, 0.35], kind="small", over=0.45),
        SFX("와글와글", 0.585, 0.15, w=150, rot=-5),     # 세아와 진우 사이 창문 자리(얼굴 피함)
    ]),
    S(90),
    P("E4-06#1", w=560, x="left", bubbles=[
        BT("그거 뭐야?", 0.70, tail=[0.50, 0.22], kind="small", over=0.40),     # 진우 머리 오른쪽 창문 위
    ]),
    S(60),
    P("E4-06#2", w=600, x="right", bubbles=[
        BD("아무것도 아니야.", 0.68, tail=[0.66, 0.84], kind="small", over=0.32),     # 세아 바로 아래(진우와 헷갈리지 않게)
    ]),
    S(400),
    # ── 토요일 ──
    T("토요일 오후 1시 50분", style="date"),
    S(30),
    P("E4-07R", w=690, border=False, bubbles=[
        BT("엄마! 컵 열두 개\n다 놨어!", 0.30, tail=[0.47, 0.14], over=0.34),
        BT("우리 유리\n신났네~", 0.86, tail=[0.77, 0.06], kind="small", over=0.15),     # 유리 엄마 얼굴을 가리지 않게
    ]),
    S(240),
    P("E4-08#1", w=560, x="right", bubbles=[
        SFX("똑딱", 0.32, 0.84, w=120, rot=-6),     # 바람 빠진 풍선을 가리지 않게
    ]),
    S(100),
    P("E4-08#2", w=600, x="left"),
    S(140),
    T("2시."),
    S(60),
    T("2시 반.", style="inner"),
    S(60),
    T("3시.", style="inner"),
    S(220),
    P("E4-09R", w=690, border=False, bubbles=[
        BT("다들 길이 막히나 보다.\n그치?", 0.74, tail=[0.66, 0.13], over=0.28),
        BD("……", 0.28, tail=[0.30, 0.60], kind="small", over=0.30),
    ]),
    S(260),
    P("E4-10#1", w=600, x="left", bubbles=[
        SFX("딩동", 0.80, 0.18, w=150, rot=8),
        BD("왔다!", 0.30, tail=[0.36, 0.62], kind="shout", over=0.30),
    ]),
    S(60),
    P("E4-10#2", w=690, border=False, bubbles=[
        BT("유리야,\n생일 축하해.", 0.70, tail=[0.62, 0.07], over=0.20),     # 꼬리가 앞머리를 뚫지 않게
    ]),
    BB(130, B("…아, 세아구나.", 0.30, 0.5, tail=[0.20, -0.7], kind="small")),
    S(300),
    P("E4-11M", w=690, border=False, bubbles=[
        BT("애들이…\n아무도 안 왔어…", 0.26, tail=[0.30, 0.42], over=0.34),
        BD("나 같은 애 생일엔\n원래 아무도 안 오나 봐…", 0.25, tail=[0.33, 0.80], kind="small", over=0.30),   # 유리(세아·엄마 위가 아니라)
    ]),
    S(150),
    P("E4-12R", w=690, border=False, bubbles=[
        BT("나는 왔잖아.", 0.22, tail=[0.34, 0.26], over=0.34),
        B("괜찮아.\n내가 있잖아.", 0.14, 0.48, tail=[0.24, 0.35], kind="whisper"),     # 세아 쪽(유리 아래가 아니라)
    ]),
    S(150),
    T("그날 나는,", "유리 곁에 있어 준 단 한 사람이었다."),
    S(300),
    P("E4-13M#1", w=690, border=False, bubbles=[
        BT("생일 축하합니다~", 0.80, tail=[0.80, 0.30], kind="small", over=0.42),
    ]),
    S(70),
    P("E4-13M#2", w=600, x="right"),
    S(120),
    T("열두 개의 종이컵은,", "끝내 하나도 쓰이지 않았다."),
    S(200),
    P("E4-14", w=600, x="left"),
    S(400),
    # ── 월요일 ──
    T("월요일, 엄마의 반찬가게", style="date"),
    S(30),
    P("E4-15", w=690, border=False, bubbles=[
        BT("토요일에 세아가\n와 줘서, 정말…", 0.20, tail=[0.20, 0.32], over=0.34),
        BT("아유, 이런 걸 뭘!", 0.82, tail=[0.80, 0.08], kind="small", over=0.22),
    ]),
    S(100),
    P("E4-16#1", w=600, x="left", bubbles=[
        BT("우리 세아가\n원래 이렇게 착해요.", 0.68, tail=[0.44, 0.07], over=0.34),
    ]),
    S(70),
    P("E4-16#2", w=600, x="right", bubbles=[
        BD("세아 같은 친구가\n있어서 다행이에요.", 0.50, tail=[0.50, 0.75], over=0.32),
    ]),
    S(320),
    {"type": "fade", "h": 420, "from": WHITE, "to": NIGHT},
    T("그날 밤", style="date_dark", bg=NIGHT),
    S(30, NIGHT),
    P("E4-17", w=600, border_color=EDGE, bubbles=[
        SFX("지익", 0.15, 0.80, w=140, rot=-6),     # 서랍 손잡이·손가락을 가리지 않게
    ]),
    S(500),
    P("E4-18", w=690, border=False),
    S(200),
    T("열두 장.", style="narr_dark"),
    S(60),
    T("한 장도 전해지지 않았다.", style="narr_dark"),
    S(560),
    P("E4-19", w=690, border=False),
    S(200),
    T("유리에게는,", "나 하나면 충분했다.", style="narr_dark"),
    S(700),
    T("〈계속〉", style="end_dark", align="right", cx=626),
    S(220),
    T("본색 4화 「생일 초대장」", "기획·각본·콘티·연출 Claude  ·  작화 GPT Image 2.5 Sunburst  ·  식자 코드", style="credit_dark"),
    S(120),
]
