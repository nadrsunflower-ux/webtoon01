"""3~6화 검수 수정: 원본 컷을 참조로 주고 고칠 것만 지시하는 편집(EDITS), 생성 없는 좌우 반전(FLIPS).

python3 retouch2.py prepare ID ...   → raw/_src/<ID>.png + prompts/<ID>.txt + batch_retouch36.json
python3 retouch2.py flips            → raw/<ID>.png (좌우 반전만)
1~2화용 retouch.py 의 KEEP 문구와 화면 비율 계산을 그대로 쓴다.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import compose  # noqa: E402
from PIL import Image  # noqa: E402
from retouch import KEEP, nearest_ar  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "raw" / "_src"

# id: (원본 src, 좌우반전 여부, 고칠 것, 추가 참조 이미지)
EDITS = {
    # ── 3화 ──
    "E3-10bR": ("E3-10#2", False,
                "TV 화면 속 홈비디오 장면의 두 아이만 고친다(노이즈·흐림·화질·구도·날짜 글자는 그대로). 오른쪽 나무 해설대 옆의 여자아이: 턱선 길이의 "
                "검은 단발에 일자 앞머리, 흰 칼라 블라우스 위에 남색 카디건, 회색 주름치마, 흰 무릎 양말, 검은 구두(긴 머리가 아니다). 왼쪽의 남자아이: "
                "머리에 금색 종이 왕관, 흰 반팔 티셔츠와 남색 반바지, 빨간 체육복 상의를 망토처럼 목에 묶었다(검은 조끼가 아니다). 남자아이는 객석 쪽을 "
                "보고 인사하듯 허리를 숙인 채 해설대 쪽으로 뒷걸음질 치고 있고, 남자아이의 뒤꿈치와 여자아이의 구두 사이는 한 걸음도 안 될 만큼 가깝다. "
                "두 아이 모두 화질 때문에 얼굴은 알아볼 수 없을 만큼 흐리다.", []),
    # 사고 직후의 무대는 비어 있어야 한다(E3-01 과 이어짐). 세아와 닮은 아이들이 무대에 서 있으면 헷갈린다(작가 검수 2026-10-15).
    "E3-02aR": ("E3-02#1", False,
                "배경만 고친다: 세아 뒤쪽 무대 위에 흐릿하게 서 있는 아이들을 모두 지운다. 그 자리는 아무도 없는 반들거리는 나무 무대 바닥, "
                "노란 무대 조명, 커튼, 금색 별 장식만 남는다. 세아(얼굴·표정·머리·옷·손)와 찌그러진 금색 종이 왕관은 그대로 둔다.", []),
    "E3-16aR": ("E3-16#1", False,
                "배경만 바꾼다: 야외·나무·하늘·학교 건물·철봉을 모두 없애고, 두 번째로 첨부한 그림과 같은 밝은 교실 안으로 바꾼다(초록 칠판, 나무 "
                "책상과 의자, 창밖의 연두빛 나무가 부드럽게 흐려져 보인다). 진우와 주변 아이들의 자세·표정·옷은 그대로 둔다.", ["raw/_src/E3-15a.png"]),
    # ── 4화 ──
    "E4-07R": ("E4-07", False,
               "케이크 위 초 열 개의 불꽃을 모두 없앤다: 아직 불을 붙이지 않은 새 초(심지만 있고 불꽃·빛 번짐 없음). 나머지는 그대로.", []),
    "E4-09R": ("E4-09", False,
               "여자아이(유리)의 머리 위에 분홍·흰 줄무늬 종이 고깔모자(꼭대기에 분홍 방울)를 살짝 비뚤어지게 씌운다. 첨부한 두 번째 그림의 고깔모자와 "
               "같은 모자다. 그 밖에는 아무것도 바꾸지 않는다.", ["raw/E4-10.png"]),
    # 자리 방향 통일(2026-10-15 검수): 뒤쪽 아이들이 옆·뒤를 향해 앉아 앞쪽 인물과 방향이 섞였다.
    "E4-01R": ("E4-01", False,
               "뒤쪽 배경의 아이들만 고친다. 교실의 모든 책상과 의자는 앞쪽의 유리·세아 책상과 똑같이 카메라 쪽을 향해 줄지어 놓여 있다. 뒤쪽 "
               "자리에 앉은 아이들(회색 후드 남자아이, 연보라 옷의 긴 머리 여자아이 등)은 모두 몸과 의자가 카메라 쪽을 향하게 앉고, 고개만 살짝 "
               "돌려 웃고 있는 남자아이들 쪽을 본다. 옆이나 뒤를 향해 앉은 아이, 카메라에 등이나 의자 등받이를 보이는 아이는 없다. 배경은 지금처럼 "
               "부드럽게 흐린다. 앞쪽의 유리·세아·웃는 남자아이 두 명, 창문, 책상 위 물건은 그대로 둔다.", []),
    "E4-02aR": ("E4-02#1", False,
                "뒤쪽 배경의 아이들만 고친다. 교실의 모든 책상과 의자는 세아의 책상과 똑같이 카메라 쪽을 향해 줄지어 놓여 있다. 뒤쪽 자리에 앉은 "
                "아이들은 모두 몸과 의자가 카메라 쪽을 향하게 앉아 있다(쉬는 시간이라 옆 친구와 이야기하며 고개만 돌릴 수 있다). 카메라에 등이나 "
                "의자 등받이를 보이는 아이, 옆이나 뒤를 향해 앉은 아이는 없다. 배경은 지금처럼 부드럽게 흐린다. 앞쪽의 세아와 유리(얼굴·표정·자세·"
                "옷·노란 봉투), 세아의 책상과 필통·공책, 창문은 그대로 둔다.", []),
    "E4-12R": ("E4-12", False,
               "두 가지만 고친다. ① 화면 왼쪽, 검은 머리 아이의 허리 뒤에서 삐져나온 작은 손 하나를 완전히 지우고 그 자리를 흰 원피스 천과 주름으로 "
               "자연스럽게 채운다(갈색 머리 아이의 두 손은 검은 머리 아이의 가슴 앞에서 리본을 쥔 두 손뿐이다). ② 갈색 머리 아이의 머리 위 분홍 고깔모자를 "
               "없애고 그 자리를 곱슬머리로 채운다(노란 리본 머리끈은 그대로).", []),
    # ── 5화 ──
    "E5-17aR": ("E5-17#1", False,
                "아이의 팔 소매만 고친다: 긴소매를 반소매로 바꾼다. 손과 팔뚝은 맨살이고, 화면 오른쪽 끝에 흰 바탕 남색 물방울무늬 반소매 잠옷의 "
                "프릴 소맷단이 팔꿈치 위에서 살짝 보인다. 손·MP3·가방은 그대로.", []),
    # ── 6화 ──
    "E6-15R": ("E6-15", False,
               "배경만 바꾼다: 바깥 거리·하늘·해·난간·나무를 모두 없애고, 노을이 드는 초등학교 교실 안으로 바꾼다(인물 뒤로 흐릿한 교실 창문 너머 "
               "주황빛 노을, 창틀 그림자, 초록 칠판 가장자리가 부드럽게 흐려져 보인다). 아이의 얼굴·머리·표정·옷·점·빛 방향은 그대로.", []),
}

# id: 원본 src (좌우 반전만)
FLIPS = {
    "E3-20bF": "E3-20#2",
    "E3-21F": "E3-21",
}


def prepare(ids):
    SRC.mkdir(parents=True, exist_ok=True)
    compose.load_src("E3-15#1").save(SRC / "E3-15a.png")       # 16화 배경 참고용
    jobs = []
    for eid in ids:
        src, flip, what, refs = EDITS[eid]
        im = compose.load_src(src).copy()
        if flip:
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        im.save(SRC / (eid + ".png"))
        (ROOT / "prompts" / (eid + ".txt")).write_text(KEEP + "\n[고칠 것] " + what)
        jobs.append({"out": "raw/%s.png" % eid, "prompt_file": "prompts/%s.txt" % eid, "aspect_ratio": nearest_ar(*im.size),
                     "quality": "high", "moderation": "low", "refs": ["raw/_src/%s.png" % eid] + refs})
        print(eid, src, im.size, jobs[-1]["aspect_ratio"])
    (ROOT / "batch_retouch36.json").write_text(json.dumps(jobs, ensure_ascii=False, indent=1))


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
