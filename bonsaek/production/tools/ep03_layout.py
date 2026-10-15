"""3화 「목격자」 식자 레이아웃."""
from ep01_layout import S, T, P, B, BT, BD, SFX, BB, DARK, WHITE

STAGE = "#111220"
NIGHT = "#0d1020"
EDGE = "#3a3b55"

BLOCKS = [
    S(200, DARK),
    {"type": "logo", "h": 400, "logo_w": 300, "sub": "3화 · 목격자"},
    S(120, DARK),
    {"type": "fade", "h": 200, "from": DARK, "to": STAGE},
    T("학예회 날, 10분 전", style="date_dark", bg=STAGE),
    S(30, STAGE),
    P("E3-01", w=690, border=False, bubbles=[
        BT("진우야!!", 0.36, tail=[0.33, 0.42], kind="shout", over=0.45),
        SFX("웅성웅성", 0.13, 0.84, w=190, rot=-6),     # 앞줄 뒷모습 위(학부모 얼굴을 가리지 않게)
    ]),
    S(110),
    P("E3-02aR", w=600, x="left", border_color=EDGE),     # 뒤쪽 무대의 아이들을 지운 편집본(사고 직후 무대는 비어 있다)
    S(90),
    T("누가 묻기 전에,", style="narr_dark"),
    S(40),
    T("먼저 말해야 했다.", style="narr_dark"),
    S(90),
    P("E3-02#2", w=600, x="right", border_color=EDGE),
    S(180),
    P("E3-03M", w=690, border=False, bubbles=[
        BT("서, 선생님…", 0.84, tail=[0.67, 0.31], kind="small", over=0.42),
    ]),
    BB(150, B("진우가… 진우가\n장난치다가…", 0.62, 0.5, tail=[0.66, -1.35])),
    S(150),
    P("E3-04#1", w=600, x="right", border_color=EDGE, bubbles=[
        BT("……", 0.18, kind="small", over=0.45),
    ]),
    S(70),
    P("E3-04#2", w=690, border=False, bubbles=[
        BT("그래, 그래.\n선생님도 봤어.", 0.20, tail=[0.27, 0.13], over=0.36),
    ]),
    S(120),
    T("나는 정말로 무서웠다.", style="narr_dark"),
    S(300),
    P("E3-05N", w=690, border=False),     # 재연출: 부모님이 무대를 향해 앉고, 무대엔 장치만
    S(110),
    T("아빠의 캠코더는,", "그때도 돌아가고 있었다.", style="narr_dark"),
    S(260),
    {"type": "fade", "h": 420, "from": STAGE, "to": WHITE},
    S(60, WHITE),
    # ── 보건실 ──
    T("보건실", style="date"),
    S(30),
    P("E3-06", w=690, border=False, bubbles=[
        BT("자, 진우야.\n얼음 대고 있자.", 0.55, tail=[0.52, 0.17], over=0.22),     # 보건 선생님 바로 위
        B("넵!", 0.89, 0.10, tail=[0.75, 0.24], kind="small"),
    ]),
    S(100),
    P("E3-07#1", w=600, x="left", bubbles=[
        BT("얼음이나 잘 대.", 0.17, tail=[0.28, 0.11], kind="small", over=0.45),
        BT("선생님, 저 무대에서\n엄청 멋있게 떨어졌죠?\n헤헤", 0.68, tail=[0.74, 0.27], over=0.30),
    ]),
    S(70),
    P("E3-07#2", w=560, x="right"),
    S(130),
    T("진우는 그 말을", "다시 하지 않았다."),
    S(260),
    P("E3-08", w=600, bubbles=[
        BT("우리 세아,\n많이 놀랐지?", 0.22, tail=[0.26, 0.17], over=0.34),
    ]),
    S(120),
    T("진우는 무엇을 봤을까.", style="narr"),
    S(50),
    T("그리고 언제, 누구에게 말할까.", style="inner"),
    S(300),
    {"type": "fade", "h": 420, "from": WHITE, "to": NIGHT},
    T("그날 밤", style="date_dark", bg=NIGHT),
    S(30, NIGHT),
    P("E3-09", w=690, border=False, bubbles=[
        SFX("지이익", 0.80, 0.16, w=190, rot=-4),
    ]),
    S(90),
    P("E3-10#1", w=560, x="left", border_color=EDGE, bubbles=[
        SFX("딸깍", 0.24, 0.24, w=130, rot=-8),
    ]),
    S(60),
    P("E3-10bR", w=600, x="right", border_color=EDGE),
    S(140),
    P("E3-11", w=600, border_color=EDGE, bubbles=[
        SFX("지이익", 0.80, 0.88, w=160, rot=5),
    ]),
    S(120),
    P("E3-12#1", w=600, x="left", border_color=EDGE, bubbles=[
        SFX("철컥", 0.76, 0.16, w=160, rot=8),
    ]),
    S(60),
    P("E3-12#2", w=600, x="right", border_color=EDGE),
    S(140),
    T("그날 밤 아빠가 무엇을 보았는지,", "나는 스무 해 뒤에야 알았다.", style="narr_dark"),
    S(320),
    P("E3-13", w=690, border=False),
    S(110),
    T("그날 밤, 나는 잠들지 못했다.", style="narr_dark"),
    S(50),
    T("진우가 언제 말할지 몰라서.", style="inner_dark"),
    S(260),
    {"type": "fade", "h": 420, "from": NIGHT, "to": WHITE},
    S(60, WHITE),
    # ── 월요일 ──
    T("월요일", style="date"),
    S(30),
    P("E3-14M", w=690, border=False, bubbles=[
        BT("우와,\n진우 꿰맸대!", 0.12, tail=[0.14, 0.19], kind="small", over=0.45),     # 꼬리가 안경에 닿지 않게
        BT("하나도 안 아파!\n헤헤", 0.47, tail=[0.34, 0.17], over=0.38),
        BT("아파? 아파?", 0.79, tail=[0.60, 0.19], kind="small", over=0.45, max_len=90),   # 연보라 후드 남자아이
    ]),
    S(90),
    P("E3-15#1", w=690, border=False, bubbles=[
        BT("내가 막 이렇게\n인사하다가~", 0.44, tail=[0.42, 0.19], over=0.34),     # 진우 바로 위(옆 여자아이 대사로 읽히지 않게)
        SFX("와하하", 0.17, 0.06, w=170, rot=-6),
    ]),
    S(60),
    P("E3-15#2", w=600, x="right", bubbles=[
        SFX("뚝", 0.73, 0.50, w=120, rot=8),
    ]),
    S(120),
    T("지금이다."),
    S(40),
    T("지금 말할 것이다.", style="inner"),
    S(160),
    P("E3-16aR", w=600, x="left", bubbles=[
        BT("…그냥 내가 덤벙대서\n넘어졌어! 헤헤.", 0.30, tail=[0.46, 0.27], over=0.34),
        B("바보~", 0.89, 0.18, tail=[0.91, 0.27], kind="small"),
    ]),
    S(70),
    P("E3-16#2", w=690, border=False),
    S(130),
    T("진우는 말하지 않았다."),
    S(220),
    T("화요일", style="caption"),
    S(20),
    P("E3-17M#1", w=690, border=False),
    S(70),
    T("수요일", style="caption"),
    S(20),
    P("E3-17M#2", w=690, border=False),
    S(120),
    T("다음 날도,", "그다음 날도."),
    S(50),
    T("진우는 아무에게도 말하지 않았다."),
    S(240),
    P("E3-18", w=600),
    S(120),
    T("규칙에 없는 아이였다."),
    S(60),
    T("말하지 않는 사람은,", "무슨 생각을 하는지 알 수가 없다.", style="inner"),
    S(120),
    T("처음으로,", "모르는 것이 무서웠다."),
    S(360),
    # ── 금요일 ──
    T("금요일, 방과 후", style="date"),
    S(30),
    P("E3-19M", w=690, border=False, bubbles=[
        BT("세아야.", 0.74, tail=[0.83, 0.26], kind="small", over=0.45),
    ]),
    S(100),
    P("E3-20#1", w=690, border=False, bubbles=[
        B("비밀로 해 줄게.", 0.80, 0.66, tail=[0.70, 0.41], kind="whisper", max_len=110),   # 진우 쪽으로 끝까지
    ]),
    S(440),
    P("E3-20bF", w=690, border=False),
    BB(150, B("대신 너,\n내 편 해.", 0.58, 0.5, tail=[0.56, -0.9], kind="whisper", size=30)),
    S(560),          # 세아 눈 클로즈업(E3-21FM)은 작가 요청으로 뺐다(2026-10-15)
    T("그날,", "나도 골라졌다."),
    S(700),
    T("〈계속〉", style="end", align="right", cx=626),
    S(220),
    T("본색 3화 「목격자」", "기획·각본·콘티·연출 Claude  ·  작화 GPT Image 2.5 Sunburst  ·  식자 코드", style="credit"),
    S(120),
]
