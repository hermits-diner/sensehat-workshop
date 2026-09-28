#!/usr/bin/env python3
"""docs/*.md 원고를 PDF로 만든다.

md → HTML(marked.js로 변환, scratchblocks로 블록 그림) → chromium 헤드리스 인쇄.
사용법: python3 tools/build_pdf.py
"""
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "pdf"

# PDF 이름: (넣을 원고 목록, 용지 방향)
# 교재는 Python과 Scratch를 나란히 놓기 위해 가로(landscape)로 인쇄한다
BOOKS = {
    "연수교재.pdf": (["00_연수개요.md", "01_1차시.md", "02_2차시.md", "03_3차시.md", "@extra"], "landscape"),
    "슬라이드원고.pdf": (["slides_outline.md"], "portrait"),
}

# 이모지 글꼴이 없어서 나눔고딕에 있는 기호로 바꾼다 (md 원고는 그대로 둠)
EMOJI = {
    "🔁": "▶", "⭐": "★", "💡": "※", "⚠️": "⚠", "🔒": "◆", "📦": "◆",
    "⏱": "◆", "🎉": "", "🎤": "강사:", "✅": "○", "❌": "×",
    # "0~50분"의 ~ 두 개가 취소선(~글자~)으로 해석되지 않도록 전각 물결표로
    "~": "～",
}

MARKED = "https://cdnjs.cloudflare.com/ajax/libs/marked/4.3.0/marked.min.js"
SCRATCHBLOCKS = "https://cdn.jsdelivr.net/npm/scratchblocks@3.6.4/build/scratchblocks.min.js"

CSS = """
body { font-family: 'NanumGothic', sans-serif; font-size: 10.5pt; line-height: 1.6; color: #222; }
h1 { font-size: 20pt; border-bottom: 3px solid #c51a4a; padding-bottom: 4px; margin-top: 0; }
h2 { font-size: 14pt; color: #c51a4a; margin-top: 1.4em; break-after: avoid; }
h3 { font-size: 12pt; break-after: avoid; }
.doc + .doc { break-before: page; }
table { border-collapse: collapse; width: 100%; margin: .6em 0; }
tr { break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 4px 7px; vertical-align: top; }
th { background: #f3e4e8; }
code { font-family: 'NanumGothicCoding', monospace; background: #f4f4f4; padding: 0 3px; border-radius: 3px; }
pre { background: #f6f8fa; border: 1px solid #ddd; border-left: 4px solid #c51a4a;
      padding: 8px 10px; border-radius: 4px; break-inside: avoid; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
pre.blocks { background: none; border: none; padding: 0 0 0 4px; }
blockquote { margin: .6em 0; padding: 6px 12px; background: #fff8e6; border-left: 4px solid #f0ad00; }
blockquote p { margin: .2em 0; }
hr { border: none; border-top: 1px dashed #ccc; margin: 1.2em 0; }
img { display: block; max-width: 58%; max-height: 72mm; margin: .5em 0 .8em;
      border: 1px solid #ccc; border-radius: 4px; break-inside: avoid; }
/* Python ↔ Scratch 나란히 */
.compare { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: .6em 0; break-inside: avoid; }
.compare > div { min-width: 0; }
.compare .label { font-weight: bold; font-size: 9.5pt; margin-bottom: 3px; }
.compare .py .label { color: #306998; }
.compare .sc .label { color: #cc7a00; }
.compare pre { margin: 0; }
.compare .sc { background: #fbfaf5; border: 1px solid #e6dfcc; border-radius: 4px; padding: 6px; }
/* 부록: Python ↔ LED 결과 */
.compare.extra { grid-template-columns: 1fr 64mm; }
.compare.extra .ledrow { flex-direction: row; align-items: flex-start; }
.compare.extra .ledrow > b { transform: none; margin-top: 11mm; }
.compare.extra .led { width: 27mm; }
.compare .out .label { color: #2e7d32; }
.ledrow { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.ledrow > b { color: #888; font-weight: normal; transform: rotate(90deg); }
.ledbox { display: flex; flex-direction: column; align-items: center; font-size: 8.5pt; color: #666; }
.led { display: grid; grid-template-columns: repeat(8, 1fr); gap: 2px; width: 30mm; padding: 2mm; background: #15191e; border-radius: 3mm; }
.led i { aspect-ratio: 1; border-radius: 1px; background: #2d333b; }
"""

JS = """
marked.setOptions({ gfm: true });
for (const el of document.querySelectorAll('script[type="text/markdown"]')) {
  const div = document.createElement('div');
  div.className = 'doc';
  div.innerHTML = marked.parse(el.textContent);
  el.replaceWith(div);
}
// ```scratchblocks 코드 블록 → 실제 블록 그림
for (const code of document.querySelectorAll('code.language-scratchblocks')) {
  const pre = document.createElement('pre');
  pre.className = 'blocks';
  pre.textContent = code.textContent;
  code.parentElement.replaceWith(pre);
}
// 같은 ## 단계 안의 첫 Python 코드와 첫 Scratch 블록을 두 칸 상자로 나란히 놓는다
for (const h2 of document.querySelectorAll('.doc h2')) {
  let py = null, sc = null;
  for (let el = h2.nextElementSibling; el && el.tagName !== 'H2'; el = el.nextElementSibling) {
    if (!py && el.tagName === 'PRE' && el.querySelector('code.language-python')) py = el;
    if (!sc && el.matches('pre.blocks')) sc = el;
  }
  if (!py || !sc) continue;
  const box = document.createElement('div');
  box.className = 'compare';
  box.innerHTML = '<div class="py"><div class="label">Python</div></div><div class="sc"><div class="label">Scratch</div></div>';
  py.replaceWith(box);
  box.children[0].appendChild(py);
  box.children[1].appendChild(sc);
}
scratchblocks.renderMatching('pre.blocks', { style: 'scratch3', languages: ['en'], scale: 0.75 });
"""


# ---------------------------------------------------------------- 부록: 추가 예제
HEADER = ["from sense_hat import SenseHat", "sense = SenseHat()", "sense.set_rotation(180)", "sense.clear()"]
CAPS = {"e03": ["크게", "작게"], "e04": ["5 → 1", "GO!"], "e05": ["예: 43%", ""], "e06": ["25℃쯤", "35℃쯤"],
        "e07": ["처음", "위로 밀면"], "e08": ["가운데", "오른쪽으로"], "e09": ["기다림", "흔들면"],
        "e10": ["초록불!", "반응 시간"], "e11": ["기록 중", "Saved"], "e12": ["빨간 물체", "파란 물체"]}


def led_html(frames, caps=None):
    """실제 SenseHAT에서 읽은 LED 장면을 8×8 격자 HTML로"""
    out = []
    for i, frame in enumerate(frames):
        cells = "".join(f'<i style="background:rgb({r},{g},{b})"></i>' if (r, g, b) != (0, 0, 0) else "<i></i>"
                        for r, g, b in frame)
        cap = f"<span>{caps[i]}</span>" if caps and caps[i] else ""
        out.append(f'<div class="ledbox"><div class="led">{cells}</div>{cap}</div>')
    return '<div class="ledrow">' + '<b>→</b>'.join(out) + "</div>"


def extra_md():
    """code/python/extra/*.py 로 부록 원고(Markdown + HTML)를 만든다"""
    frames = json.loads((ROOT / "slides" / "led_frames.json").read_text())
    md = ["# 부록 · 더 해 보기: 추가 Python 예제 12개", "",
          "> 기초 12단계를 마친 뒤 해 볼 수 있는 예제입니다. 파일 위치: `code/python/extra/`",
          "> 모든 파일은 **첫 네 줄**(`import` → `SenseHat()` → `set_rotation(180)` → `clear()`)로 시작하며, 아래에서는 생략합니다.",
          "> LED 결과 그림은 실제 SenseHAT에서 읽은 장면입니다.", ""]
    for path in sorted((ROOT / "code" / "python" / "extra").glob("e*.py")):
        lines = path.read_text(encoding="utf-8").rstrip().split("\n")
        key, rest = lines[0].lstrip("# ").split(" · ", 1)
        title, concept = rest.split(" — ", 1)
        body = lines[1:]
        for h in HEADER:
            body.remove(h)
        while body and not body[0].strip():
            body.pop(0)
        code = "\n".join(body)
        if len(body) > 30:   # 64칸 그림 리스트가 여러 개면 속을 줄여 보여 준다
            code = re.sub(r"^(\w+) = \[\n(?:    .*\n)+\]", r"\1 = [ … 8줄 × 8칸 그림 (전체는 파일에) … ]", code, flags=re.M)
        md += [f"## {key} · {title}", "",
               # 빈 줄이 있으면 Markdown이 HTML을 끊으므로 줄바꿈을 &#10;로 바꿔 한 줄로 만든다
               f'<div class="compare extra"><div class="py"><div class="label">Python · <code>{path.name}</code></div>'
               f'<pre><code class="language-python">{html.escape(code).replace(chr(10), "&#10;")}</code></pre></div>'
               f'<div class="out"><div class="label">LED 결과</div>{led_html(frames[key], CAPS.get(key))}</div></div>', "",
               f"- 새로 나오는 것: **{concept}**", ""]
    return "\n".join(md)


def build(pdf_name, md_files, orientation):
    parts = []
    for name in md_files:
        text = extra_md() if name == "@extra" else (DOCS / name).read_text(encoding="utf-8")
        for k, v in EMOJI.items():
            text = text.replace(k, v)
        # <script> 안의 글자는 그대로 읽히므로 이스케이프하지 않고, 태그가 닫히는 것만 막는다
        text = text.replace("</script", "<\\/script")
        parts.append(f'<script type="text/markdown">{text}</script>')

    # 원고 속 그림 경로(images/...)가 docs 폴더 기준으로 찾아지도록
    page = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<base href="{DOCS.as_uri()}/">
<style>@page {{ size: A4 {orientation}; margin: 14mm 15mm; }}{CSS}</style>
<script src="{MARKED}"></script><script src="{SCRATCHBLOCKS}"></script>
</head><body>{''.join(parts)}<script>{JS}</script></body></html>"""

    html_path = OUT / (Path(pdf_name).stem + ".html")
    html_path.write_text(page, encoding="utf-8")
    pdf_path = OUT / pdf_name
    subprocess.run([
        "chromium", "--headless", "--disable-gpu", "--no-pdf-header-footer",
        "--virtual-time-budget=15000", f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ], check=True, capture_output=True)
    print("만듦:", pdf_path)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for pdf_name, (md_files, orientation) in BOOKS.items():
        build(pdf_name, md_files, orientation)
