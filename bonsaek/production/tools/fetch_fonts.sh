#!/bin/sh
# 식자에 쓰는 폰트(모두 SIL OFL)를 production/fonts 에 받는다.
set -e
DIR="$(cd "$(dirname "$0")/.." && pwd)/fonts"
mkdir -p "$DIR"
PRETENDARD="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/packages/pretendard/dist/public/static"
GFONTS="https://github.com/google/fonts/raw/main/ofl"
for w in Medium SemiBold Bold ExtraBold; do
  curl -fsSL -o "$DIR/Pretendard-$w.otf" "$PRETENDARD/Pretendard-$w.otf"
done
curl -fsSL -o "$DIR/NanumMyeongjo-Bold.ttf" "$GFONTS/nanummyeongjo/NanumMyeongjo-Bold.ttf"
curl -fsSL -o "$DIR/NanumMyeongjo-ExtraBold.ttf" "$GFONTS/nanummyeongjo/NanumMyeongjo-ExtraBold.ttf"
curl -fsSL -o "$DIR/GowunBatang-Regular.ttf" "$GFONTS/gowunbatang/GowunBatang-Regular.ttf"
curl -fsSL -o "$DIR/NanumPenScript-Regular.ttf" "$GFONTS/nanumpenscript/NanumPenScript-Regular.ttf"
ls -l "$DIR"
