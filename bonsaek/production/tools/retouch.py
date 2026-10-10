"""검수에서 걸린 컷을 '편집'으로 고친다: 원본 컷을 참조 이미지로 주고, 고칠 항목만 지시한다.

python3 retouch.py prepare [ID ...]   → raw/_src/<ID>.png (필요하면 좌우 반전) + prompts/<ID>.txt + batch_retouch.json
이후 openrouter-image 스킬로 batch 를 돌리면 raw/<ID>.png 가 생긴다.
FLIPS 에 적힌 컷은 생성 없이 좌우 반전만 해서 raw/<ID>.png 로 저장한다.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose  # noqa: E402
from PIL import Image  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "raw" / "_src"

KEEP = ("[편집] 첨부한 첫 번째 그림을 그대로 유지한다: 구도, 화면 비율, 인물의 얼굴·표정·머리 모양·옷·자세, 선의 느낌, 색감, 조명, 화풍을 "
        "모두 똑같이 둔다. 아래 [고칠 것]에 적은 부분만 바꾼다. 테두리·여백·말풍선·글자·서명은 새로 넣지 않는다. 손가락은 손마다 다섯 개.")

CROWN = "금색 색종이를 접어 만든 수수한 종이 왕관(뾰족한 삼각 톱니 다섯 개가 빙 둘러 있고, 보석·구슬·방울 장식은 전혀 없음)"
ENTRANCE = ("배경만 바꾼다: 야외·옥상·난간·하늘·도시 풍경을 모두 없애고, 학교 중앙 현관의 실내로 바꾼다. 인물 뒤로 낡은 나무 신발장"
            "(칸마다 실내화와 운동화가 놓임)과 커다란 유리 현관문이 부드럽게 흐려져 보이고, 유리문을 통해 노을빛 주황 역광이 길게 들어온다. "
            "두 번째로 첨부한 그림과 같은 장소다(그 그림의 인물 배치는 따라 하지 않는다). 인물은 손대지 않는다.")

# id: (원본 src, 좌우반전 여부, 고칠 것, 추가 참조 이미지)
EDITS = {
    # ── 1화 ──
    "E1-04R": ("E1-04", False,
               "오른손: 손목시계를 없애고(오른 손목에는 아무것도 없다), 오른손 손등과 손바닥에 흰 손수건을 붕대처럼 한 바퀴 감아 쥔 모습으로 바꾼다. "
               "왼손은 몸에 가려 보이지 않는다.", []),
    "E1-10R": ("E1-10#1", False,
               "그림 안에 그려진 글자 효과음(왼쪽 아래의 '와르르')을 완전히 지우고 그 자리는 바닥 타일과 흩어진 연필로 자연스럽게 채운다. "
               "화면 오른쪽 끝에 앉은 아이는 주인공과 닮지 않게: 길게 땋은 갈색 머리에 연두색 티셔츠를 입은 평범한 여자아이로 바꾼다.", []),
    "E1-17R": ("E1-17#2", True,
               "여자아이(세아)의 얼굴 점을 바로잡는다: 점은 아이의 오른쪽 눈 바로 아래, 즉 화면에서 보았을 때 얼굴의 왼쪽 눈 아래에 작게 하나만 있다. "
               "반대쪽 눈 아래에는 점이 없다.", []),
    "E1-22aR": ("E1-22#1", False, ENTRANCE, ["raw/E1-21.png"]),
    "E1-22bR": ("E1-22#2", False, ENTRANCE, ["raw/E1-21.png"]),
    "E1-23aR": ("E1-23#1", False, ENTRANCE + " 두 아이는 현관 바닥(회색 타일)에 있다.", ["raw/E1-21.png"]),
    "E1-23bR": ("E1-23#2", False, ENTRANCE, ["raw/E1-21.png"]),
    # ── 2화 ──
    "E2-01R": ("E2-01", False,
               "피아노만 바꾼다: 갈색 업라이트 피아노를 뚜껑을 닫은 검은색 그랜드 피아노로 바꾼다. 세아는 그 앞의 검은 가죽 피아노 의자에 같은 자세로 앉아 있다.", []),
    "E2-05R": ("E2-05#1", False,
               "남자아이가 쓴 왕관만 바꾼다: 흰 바탕에 점무늬가 있는 왕관을 " + CROWN + "으로 바꾼다. 삐뚤게 얹힌 각도는 그대로.", []),
    "E2-07R": ("E2-07", False,
               "오른쪽 여자(엄마)의 얼굴에서 안경을 완전히 없앤다. 맨얼굴, 다정한 눈웃음은 그대로.", []),
    "E2-11R": ("E2-11#2", False,
               "① 그림 안에 그려진 글자 효과음('와하하')을 완전히 지우고 그 자리는 무대 조명과 배경으로 채운다. ② 맨 앞에서 행진하는 왕관 쓴 남자아이의 "
               "긴 트레이닝 바지를 무릎 위까지 오는 남색 반바지로 바꾼다. 맨다리가 드러나고, 오른쪽 무릎에 살구색 밴드, 흰 발목 양말과 흰 운동화. "
               "③ 왕관은 " + CROWN + ".", []),
    "E2-14R": ("E2-14#2", False,
               "뒤쪽 무대 한가운데에 흐리게 서 있는 인물만 바꾼다: 밝은 갈색 곱슬머리를 양 갈래로 낮게 묶은 10살 여자아이(노란 후드 티셔츠, 연청색 멜빵바지, "
               "분홍 운동화)가 고개를 푹 숙이고 서 있는 흐린 실루엣으로. 앞쪽의 단발 여자아이와 마이크는 그대로.", ["sheets/SH2_yuri_jinwoo10.png"]),
    "E2-15R": ("E2-15", False,
               "① 그림 안의 글자 효과음('짝짝짝' 세 군데)을 모두 지우고 그 자리는 객석과 사람들로 자연스럽게 채운다. ② 왼쪽 위에서 박수 치는 안경 쓴 "
               "파마머리 여자를, 안경을 쓰지 않은 검은 생머리 단발의 평범한 학부모로 바꾼다(안경줄 없음, 하늘색 셔츠). ③ 가운데 남자(아빠)가 든 카메라는 "
               "2006년식 짙은 회색 캠코더(옆으로 펼친 작은 액정 화면)로, 오른손을 손잡이 끈에 끼워 들고 있다.", ["raw/E2-07.png"]),
    "E2-16R": ("E2-16#2", True,
               "오른쪽 위 구석, 조명이 비치는 나무 해설대 뒤에 흐리게 서 있는 인물만 바꾼다: 어른이 아니라 10살 여자아이다. 검은 단발머리, 남색 카디건, "
               "키가 작아 해설대 위로 어깨와 머리만 보인다. 앞쪽의 고개 숙인 아이는 그대로.", []),
    "E2-18R": ("E2-18", False,
               "왼쪽의 흰 운동화 위쪽만 바꾼다: 긴 흰 바지가 아니라 맨 종아리(아이의 살색 다리)가 보이고, 발목에는 짧은 흰 양말이 접혀 있다. "
               "운동화와 오른쪽의 검은 구두, 무대 바닥은 그대로.", []),
    "E2-19R": ("E2-19", True,
               "허공에 날아가는 왕관만 바꾼다: " + CROWN + ". 날아가는 위치와 각도는 그대로.", []),
    "E2-20R": ("E2-20#2", False,
               "바닥의 왕관만 바꾼다: " + CROWN + ", 한쪽이 살짝 찌그러져 있다. 놓인 위치와 크기, 조명 반사는 그대로. 오른쪽의 검은 구두와 흰 양말은 그대로.", []),
    "E2-22R": ("E2-22", False,
               "서랍 속 왕관만 바꾼다: 오래되어 빛이 바래고 구겨진 " + CROWN + ". 위치와 크기는 그대로.", []),
    "E2-23R": ("E2-23#1", False,
               "① 가운데 여자(세아 엄마)의 체크무늬 앞치마를 없앤다: 베이지색 니트와 긴 갈색 치마 차림이고 두 손은 몸 앞에서 모은다. ② 오른쪽 여자(유리 엄마)의 "
               "머리를 바꾼다: 밝은 갈색 곱슬머리를 목 뒤에서 낮게 하나로 묶었다. 얼굴과 연노랑 니트는 그대로.", []),
    "E2-24R": ("E2-24", False,
               "침대에 걸터앉은 남자아이의 하의만 바꾼다: 긴 트레이닝 바지 대신 무릎 위까지 오는 남색 반바지. 맨다리가 드러나고 오른쪽 무릎에 살구색 밴드, "
               "흰 발목 양말과 흰 운동화. 빨간 체육복 상의와 턱의 흰 거즈, 웃는 얼굴은 그대로.", []),
}

# 생성 없이 좌우 반전만 하는 컷: id → 원본 src
FLIPS = {"E1-02F": "E1-02", "E1-03F": "E1-03", "E2-06F": "E2-06#2"}


def nearest_ar(w, h):
    cands = {"1:1": 1.0, "3:2": 1.5, "2:3": 2 / 3, "4:3": 4 / 3, "3:4": 0.75, "16:9": 16 / 9, "9:16": 9 / 16, "21:9": 21 / 9}
    r = w / h
    return min(cands, key=lambda k: abs(cands[k] - r) / cands[k])


def prepare(ids):
    SRC.mkdir(parents=True, exist_ok=True)
    jobs = []
    for eid in ids:
        src, flip, what, refs = EDITS[eid]
        im = compose.load_src(src).copy()
        if flip:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        path = SRC / (eid + ".png")
        im.save(path)
        (ROOT / "prompts" / (eid + ".txt")).write_text(KEEP + "\n[고칠 것] " + what)
        jobs.append({"out": "raw/%s.png" % eid, "prompt_file": "prompts/%s.txt" % eid, "aspect_ratio": nearest_ar(*im.size),
                     "quality": "high", "moderation": "low", "refs": ["raw/_src/%s.png" % eid] + refs})
        print(eid, src, im.size, jobs[-1]["aspect_ratio"], "flip" if flip else "")
    (ROOT / "batch_retouch.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=1))


def flips():
    for fid, src in FLIPS.items():
        im = compose.load_src(src).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im.save(ROOT / "raw" / (fid + ".png"))
        print("flip", fid, im.size)


if __name__ == "__main__":
    if sys.argv[1] == "prepare":
        prepare(sys.argv[2:] or list(EDITS))
    elif sys.argv[1] == "flips":
        flips()
