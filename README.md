# 본색 (本色)

한 번도 앞에 나선 적 없는 모범생 권세아가, 20년에 걸쳐 자기 안의 폭력과 권력욕을 알아 가는 심리 스릴러 웹툰입니다. 4부 60화로 기획했고 1~2화를 제작했습니다.

기획·각본·콘티·연출은 Claude가, 작화는 GPT Image 2.5 Sunburst(OpenRouter)가 맡았고, 말풍선·내레이션·효과음 배치는 코드로 넣었습니다.

## 보기

연재 사이트: https://webtoon01.vercel.app

로컬에서는 정적 파일을 그대로 띄우면 됩니다.

```bash
cd bonsaek/site && python3 -m http.server 8765
# http://127.0.0.1:8765/
```

## 폴더

| 경로 | 내용 |
|---|---|
| `bonsaek/plan/` | 기획서, 등장인물, 4부 60화 전체 스토리보드, 1~2화 콘티 |
| `bonsaek/site/` | 연재 사이트(정적 HTML, 690px 세로 슬라이스). 배포 대상 |
| `bonsaek/production/prompts/` | 컷별 작화 지시서 |
| `bonsaek/production/raw/`, `sheets/`, `sfx/` | 원화, 인물 설정화, 붓글씨 효과음 |
| `bonsaek/production/tools/` | 지시서 생성, 식자, 원고 조립, 사이트 빌드 스크립트 |

## 다시 만들기

Python 3.9 이상과 Pillow, markdown 패키지가 필요합니다.

```bash
cd bonsaek/production/tools
./fetch_fonts.sh          # 식자용 폰트 받기(처음 한 번)
python3 build_ep.py 1     # 1화 원고 조립 → ../../site/ep01/
python3 build_ep.py 2
python3 build_site.py     # 사이트 페이지와 썸네일 다시 만들기
```

- 컷 배치와 대사는 `ep01_layout.py`, `ep02_layout.py`에서 고칩니다. `gridview.py`로 컷에 좌표 격자를 얹어 말풍선 위치를 잡습니다.
- 새 컷을 그리려면 `shots.py`(지시서)와 `retouch.py`(부분 수정)가 만든 batch JSON을 OpenRouter Images API로 돌립니다. `OPENROUTER_API_KEY`가 필요합니다.

## 배포

`vercel.json`이 `bonsaek/site`를 빌드 없이 그대로 내보냅니다.

```bash
vercel deploy --prod
```
