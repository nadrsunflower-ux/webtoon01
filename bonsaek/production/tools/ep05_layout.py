"""5화 「엄마의 거짓말」 식자 레이아웃."""
from ep01_layout import S, T, P, B, BT, BD, SFX, BB, DARK, WHITE

NIGHT = "#0d1020"
DAWN = "#141a33"
EDGE = "#3a3b55"

BLOCKS = [
    S(200, DARK),
    {"type": "logo", "h": 400, "logo_w": 300, "sub": "5화 · 엄마의 거짓말"},
    S(120, DARK),
    {"type": "fade", "h": 420, "from": DARK, "to": WHITE},
    S(60, WHITE),
    T("5월 마지막 주, 엄마의 반찬가게", style="date"),
    S(30),
    P("E5-01", w=690, border=False),
    S(110),
    T("엄마는 아파트 상가에서", "작은 반찬가게를 했다."),
    S(220),
    P("E5-02#1", w=600, x="left"),
    S(70),
    P("E5-02#2", w=690, border=False, bubbles=[
        BT("이 멸치볶음,\n사장님이 직접\n볶은 거예요?", 0.20, tail=[0.24, 0.40], over=0.32),
        BT("그럼요~ 새벽같이\n일어나서 제가\n직접 볶았죠!", 0.68, tail=[0.60, 0.18], over=0.30),   # 꼬리가 엄마 눈을 찌르지 않게
    ]),
    S(150),
    P("E5-03M", w=690, border=False, bubbles=[
        BT("이건 착한 거짓말이야.", 0.32, tail=[0.30, 0.26], kind="whisper", over=0.34),
        B("손님도 기분 좋고,\n엄마도 좋고.", 0.70, 0.15, tail=[0.47, 0.24], kind="whisper", max_len=40),   # 엄마 얼굴 오른쪽에서 엄마를 가리킴
    ]),
    S(150),
    T("엄마에게서 배웠다."),
    S(50),
    T("착한 거짓말에는", "문법이 있다."),
    S(300),
    {"type": "fade", "h": 300, "from": WHITE, "to": DAWN},
    T("새벽 4시, 도매시장", style="date_dark", bg=DAWN),
    S(30, DAWN),
    P("E5-04", w=690, border=False),
    S(110),
    T("하나, 진짜를 하나 섞을 것.", style="narr_dark"),
    S(60),
    T("엄마는 정말로 새벽에 일어났다.", "도매시장에 가려고.", style="inner_dark"),
    S(220),
    {"type": "fade", "h": 300, "from": DAWN, "to": WHITE},
    S(60, WHITE),
    P("E5-05", w=690, border=False, bubbles=[
        BT("할아버지, 이거\n엄마가 새벽에\n직접 만든 거예요!", 0.44, tail=[0.43, 0.22], over=0.26, max_len=95),   # 세아(엄마 위가 아니라 세아 머리 위로)
        BT("허허, 고 녀석\n참 싹싹하네.", 0.85, tail=[0.76, 0.20], kind="small", over=0.40),
    ]),
    S(120),
    T("둘, 웃으면서 말할 것."),
    S(50),
    T("셋, 듣는 사람이 기분 좋을 것."),
    S(400),
    # ── 신발장 ──
    T("다음 날, 하교 시간", style="date"),
    S(30),
    P("E5-06M", w=690, border=False, bubbles=[
        BT("권세아.", 0.30, tail=[0.24, 0.08], over=0.30, max_len=26),   # 꼬리가 보미 얼굴로 내려오지 않게
    ]),
    S(90),
    P("E5-07#1", w=600, x="left", bubbles=[
        BT("너 학예회 때 무대 뒤에서\n유리한테 뭐라고 했어?", 0.80, tail=[0.70, 0.18], over=0.26),   # 꼬리가 이마를 찌르지 않게
        BD("내가 다 봤어.\n반장으로서 선생님한테\n말할 거야!", 0.70, tail=[0.62, 0.80], kind="shout", over=0.30),
    ]),
    S(80),
    P("E5-07#2", w=600, x="right"),
    S(140),
    T("두 번째였다."),
    S(60),
    T("누가 말하기 전에,", "먼저 말해야 했다.", style="inner"),
    S(400),
    # ── MP3 ──
    T("그다음 날, 쉬는 시간", style="date"),
    S(30),
    P("E5-08", w=690, border=False, bubbles=[
        BT("없어…\n내 MP3가 없어…", 0.40, tail=[0.33, 0.30], over=0.34),
        BT("도둑\n맞았대!", 0.07, tail=[0.03, 0.30], kind="small", over=0.40, max_len=34),
        SFX("웅성웅성", 0.86, 0.10, w=170, rot=6),
    ]),
    S(100),
    P("E5-09#1", w=600, x="left", bubbles=[
        BT("세아야, 울지 말고\n말해 봐.\n선생님은 다 알 수 있어.", 0.70, tail=[0.62, 0.20], over=0.30),
    ]),
    S(70),
    P("E5-09#2", w=690, border=False, bubbles=[
        BD("아까… 쉬는 시간에…\n보미가 제 사물함 앞에\n있었어요…", 0.62, tail=[0.52, 0.80], kind="small", over=0.30),
    ]),
    S(140),
    T("진짜를 하나 섞을 것.", style="inner"),
    S(220),
    P("E5-10N", w=690, border=False, bubbles=[     # 재연출: 책상 전부 교실 앞(카메라) 방향
        BT("아니야!\n나는 반장이라서\n사물함 검사한 거야!", 0.73, tail=[0.56, 0.30], kind="shout", over=0.26),   # 보미 머리 오른쪽 위
        B("반장이\n훔쳤대…", 0.14, 0.17, tail=[0.12, 0.40], kind="whisper"),
        B("진짜?", 0.90, 0.25, tail=[0.84, 0.40], kind="whisper"),
    ]),
    S(130),
    T("보미는 진짜를 말했다."),
    S(50),
    T("그래서 더 거짓말 같았다.", style="inner"),
    S(320),
    P("E5-11", w=690, border=False, bubbles=[
        # 아빠·엄마 머리가 컷 위 변에 닿아 있어 풍선은 아래 변에 건다(얼굴을 가리지 않게)
        BD("엄마!", 0.38, tail=[0.42, 0.55], kind="shout", over=0.42),               # 세아
        BD("헉… 헉… 세아야!\n괜찮아?", 0.78, tail=[0.71, 0.60], over=0.34),       # 아빠
    ]),
    S(100),
    T("아빠는 회사에서,", "엄마는 가게에서", "달려왔다.", size=30),
    S(200),
    P("E5-12#1", w=600, x="left", bubbles=[
        BT("우리 보미가\n그럴 애가 아니에요!\n증거 있어요?", 0.80, tail=[0.74, 0.18], over=0.24),
    ]),
    S(70),
    P("E5-12#2", w=600, x="right", bubbles=[
        BT("우리 세아가\n거짓말할 리가\n없지요!", 0.80, tail=[0.70, 0.14], over=0.28),
    ]),
    S(120),
    P("E5-13#1", w=600, x="left", bubbles=[
        BT("아이고, 다들 진정하시고…\n죄송합니다, 죄송합니다…", 0.76, tail=[0.64, 0.14], kind="small", over=0.25),
    ]),
    S(60),
    P("E5-13#2", w=600, x="right", bubbles=[
        BT("세아는 거짓말할\n아이가 아니에요.\n선생님은 눈만 봐도 알아요.", 0.28, tail=[0.36, 0.15], over=0.18),
    ]),
    S(200),
    P("E5-14", w=600),
    S(120),
    T("MP3는 끝내 나오지 않았다."),
    S(50),
    T("증거는 없었다.", "소문이면 충분했다."),
    S(60),
    T("진우는 이번에도, 아무 말 하지 않았다.", style="inner"),
    S(300),
    P("E5-15", w=690, border=False),
    S(110),
    T("그 주에 보미는", "반장을 그만두었다."),
    S(300),
    {"type": "fade", "h": 420, "from": WHITE, "to": NIGHT},
    T("그날 밤", style="date_dark", bg=NIGHT),
    S(30, NIGHT),
    P("E5-16", w=600, border_color=EDGE, bubbles=[
        SFX("지익", 0.80, 0.62, w=140, rot=6),
    ]),
    S(400),
    P("E5-17aR", w=690, border=False),
    S(160),
    T("엄마 말이 맞았다.", style="narr_dark"),
    S(60),
    T("착한 거짓말은,", "모두를 기분 좋게 한다.", style="narr_dark"),
    S(200),
    P("E5-17#2", w=600, border_color=EDGE),
    S(560),
    P("E5-18", w=690, border=False),
    S(200),
    T("보미만 빼고.", style="narr_dark"),
    S(700),
    T("〈계속〉", style="end_dark", align="right", cx=626),
    S(220),
    T("본색 5화 「엄마의 거짓말」", "기획·각본·콘티·연출 Claude  ·  작화 GPT Image 2.5 Sunburst  ·  식자 코드", style="credit_dark"),
    S(120),
]
