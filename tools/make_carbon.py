#!/usr/bin/env python3
"""code/python/ 의 예제 코드를 Carbon(carbon.now.sh) 스타일 PNG로 만든다.

맥 창 모양 + 신호등 버튼 + 그림자 + 그라데이션 배경. 한글 주석도 깨지지 않는다.
결과: code/carbon/*.png 와 한눈에 보는 갤러리 code/carbon/index.html
코드를 고친 뒤 이 스크립트를 다시 실행하면 그림도 바뀐다. (인터넷 필요 없음)
사용법: python3 tools/make_carbon.py
"""
import html
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "code" / "python"
OUT = ROOT / "code" / "carbon"

FONT_FILE = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
FONT_INDEX = 6  # Noto Sans Mono CJK KR (fc-list 로 확인)
STYLE = get_style_by_name("dracula")

S = 2                        # 2배로 그려서 슬라이드·인쇄에서도 선명하게
FONT_SIZE = 17 * S
LINE_H = int(FONT_SIZE * 1.55)
OUTER = 56 * S               # 창 바깥 여백 (배경)
PAD_X, PAD_Y = 28 * S, 20 * S
BAR_H = 44 * S               # 제목 막대 높이
RADIUS = 12 * S
MIN_W = 560 * S
BG_TOP, BG_BOTTOM = (197, 26, 74), (142, 15, 51)  # 첫 화면과 같은 라즈베리색
WINDOW = (40, 42, 54)
DOTS = [(255, 95, 86), (255, 189, 46), (39, 201, 63)]

font = ImageFont.truetype(FONT_FILE, FONT_SIZE, index=FONT_INDEX)
title_font = ImageFont.truetype(FONT_FILE, 13 * S, index=FONT_INDEX)


def colour(ttype):
    """토큰 종류(키워드, 문자열, 주석 …)에 맞는 색."""
    while ttype not in STYLE.styles or not STYLE.style_for_token(ttype)["color"]:
        if ttype.parent is None:
            return (248, 248, 242)
        ttype = ttype.parent
    c = STYLE.style_for_token(ttype)["color"]
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def tokens_by_line(code):
    """코드를 줄 단위 [(색, 글자), …] 목록으로 나눈다."""
    lines = [[]]
    for ttype, text in lex(code, PythonLexer()):
        for i, part in enumerate(text.split("\n")):
            if i:
                lines.append([])
            if part:
                lines[-1].append((colour(ttype), part))
    while lines and not lines[-1]:
        lines.pop()
    return lines


def gradient(w, h):
    top = Image.new("RGB", (w, h), BG_TOP)
    bottom = Image.new("RGB", (w, h), BG_BOTTOM)
    mask = Image.linear_gradient("L").resize((w, h))
    return Image.composite(bottom, top, mask)


def render(path):
    code = path.read_text(encoding="utf-8").expandtabs(4)
    lines = tokens_by_line(code)
    text_w = max((sum(font.getlength(t) for _, t in ln) for ln in lines), default=0)
    win_w = max(MIN_W, int(text_w) + 2 * PAD_X)
    win_h = BAR_H + len(lines) * LINE_H + 2 * PAD_Y
    img = gradient(win_w + 2 * OUTER, win_h + 2 * OUTER)

    # 그림자: 창 모양을 흐리게 해서 조금 아래에 깐다
    shadow = Image.new("L", img.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle(
        (OUTER, OUTER + 14 * S, OUTER + win_w, OUTER + win_h + 14 * S), RADIUS, fill=150)
    shadow = shadow.filter(ImageFilter.GaussianBlur(24 * S))
    img.paste((0, 0, 0), mask=shadow)

    d = ImageDraw.Draw(img)
    d.rounded_rectangle((OUTER, OUTER, OUTER + win_w, OUTER + win_h), RADIUS, fill=WINDOW)
    for i, dot in enumerate(DOTS):
        cx, cy = OUTER + 22 * S + i * 20 * S, OUTER + BAR_H // 2
        d.ellipse((cx - 6 * S, cy - 6 * S, cx + 6 * S, cy + 6 * S), fill=dot)
    d.text((OUTER + win_w // 2, OUTER + BAR_H // 2), path.name,
           font=title_font, fill=(150, 152, 170), anchor="mm")

    y = OUTER + BAR_H + PAD_Y
    for ln in lines:
        x = OUTER + PAD_X
        for rgb, text in ln:
            d.text((x, y), text, font=font, fill=rgb)
            x += font.getlength(text)
        y += LINE_H
    return img


GROUPS = [
    ("기초 12단계", "s"), ("미니 프로젝트", "p"), ("추가 예제", "e"),
]


def gallery(items):
    sections = []
    for label, prefix in GROUPS:
        cards = []
        for name, title in items:
            if not name.startswith(prefix):
                continue
            cards.append(
                f'<figure><a href="{name}.png" target="_blank">'
                f'<img src="{name}.png" alt="{html.escape(title)}" loading="lazy"></a>'
                f'<figcaption>{html.escape(title)}'
                f'<a class="dl" href="{name}.png" download>PNG 저장</a></figcaption></figure>')
        sections.append(f'<h2>{label}</h2>\n<div class="grid">\n' + "\n".join(cards) + "\n</div>")
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>예제 코드 그림</title>
<style>
  body {{ margin: 0; font-family: 'NanumSquare', 'NanumGothic', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif; background: #fbfaf8; color: #1f2328; }}
  header {{ background: linear-gradient(135deg, #c51a4a, #8e0f33); color: #fff; padding: 40px 16px 32px; text-align: center; }}
  header h1 {{ margin: 0 0 8px; font-size: clamp(24px, 4vw, 36px); }}
  header p {{ margin: 0; opacity: .85; }}
  header a {{ color: #fff; }}
  main {{ max-width: 1200px; margin: 0 auto; padding: 16px 16px 48px; }}
  h2 {{ color: #c51a4a; border-bottom: 2px solid #eadde1; padding-bottom: 6px; margin-top: 36px; }}
  .grid {{ display: grid; gap: 20px; align-items: start; grid-template-columns: repeat(auto-fill, minmax(min(100%, 360px), 1fr)); }}
  figure {{ margin: 0; background: #fff; border-radius: 12px; padding: 10px; box-shadow: 0 4px 18px rgba(0,0,0,.07); }}
  figure img {{ width: 100%; display: block; border-radius: 8px; }}
  figcaption {{ display: flex; justify-content: space-between; gap: 8px; align-items: center; padding: 10px 4px 2px; font-size: 15px; }}
  .dl {{ flex: none; font-size: 13px; color: #c51a4a; text-decoration: none; border: 1px solid #c51a4a; border-radius: 999px; padding: 3px 10px; }}
</style>
</head>
<body>
<header>
  <h1>예제 코드 그림</h1>
  <p>그림을 누르면 크게 보입니다 · 슬라이드·학습지에 붙여 쓰세요 · <a href="../../">처음으로</a></p>
</header>
<main>
{chr(10).join(sections)}
</main>
</body>
</html>
"""


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = sorted(SRC.glob("[sp]*.py")) + sorted((SRC / "extra").glob("e*.py")) + sorted((SRC / "game").glob("g*.py"))
    items = []
    for path in files:
        render(path).save(OUT / f"{path.stem}.png", optimize=True)
        first = path.read_text(encoding="utf-8").splitlines()[0]
        title = first.lstrip("# ").strip() if first.startswith("#") else path.stem
        items.append((path.stem, title))
        print("만듦:", f"code/carbon/{path.stem}.png")
    (OUT / "index.html").write_text(gallery(items), encoding="utf-8")
    print(f"그림 {len(items)}개 + code/carbon/index.html")


if __name__ == "__main__":
    main()
