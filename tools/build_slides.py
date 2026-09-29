#!/usr/bin/env python3
"""발표 슬라이드(slides/index.html)를 만든다.

- Python 코드·Scratch 블록은 docs/*.md 원고에서 가져온다 (교재와 항상 같게).
- LED 결과 그림은 slides/led_frames.json (실제 SenseHAT에서 읽은 값)을 쓴다.
- 인터넷 없이 열리도록 라이브러리는 slides/lib/ 에 둔다.
사용법: python3 tools/build_slides.py  →  브라우저로 slides/index.html 열기
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "slides"

# 이모지 글꼴이 없는 Pi에서도 보이도록 기호로 바꾼다
EMOJI = {"🔁": "▶", "⭐": "★", "💡": "※", "⚠️": "⚠", "🔒": "◆", "🎤": "", "🎉": ""}


def clean(text):
    for k, v in EMOJI.items():
        text = text.replace(k, v)
    return text


def md_inline(text):
    """원고의 한 줄(굵게, `코드`)을 HTML로."""
    text = html.escape(clean(text).strip())
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
    return text


# ---------------------------------------------------------------- 원고 읽기
def sections(md):
    """'## s01 · 제목' 단위로 {번호: (제목, python, scratch, 글머리 목록)}"""
    out = {}
    for m in re.finditer(r"^## ((?:s|p)\d\d) · (.+?)\n(.*?)(?=^## |\Z)", md, re.M | re.S):
        body = m.group(3)
        py = re.search(r"```python\n(.*?)```", body, re.S)
        sb = re.search(r"```scratchblocks\n(.*?)```", body, re.S)
        bullets = re.findall(r"^- (.+)$", body, re.M)
        out[m.group(1)] = (m.group(2).strip(), py and py.group(1).rstrip(),
                           sb and sb.group(1).rstrip(), bullets)
    return out


D1 = (DOCS / "01_1차시.md").read_text(encoding="utf-8")
D2 = (DOCS / "02_2차시.md").read_text(encoding="utf-8")
D3 = (DOCS / "03_3차시.md").read_text(encoding="utf-8")
S2, S3 = sections(D2), sections(D3)
FIRST_PY = re.search(r"## 5\. 첫 코드.*?```python\n(.*?)```", D1, re.S).group(1).rstrip()
FIRST_SB = re.search(r"## 5\. 첫 코드.*?```scratchblocks\n(.*?)```", D1, re.S).group(1).rstrip()
HEAD_PY = re.search(r"첫 네 줄.*?```python\n(.*?)```", D2, re.S).group(1).rstrip()
HEAD_SB = re.search(r"첫 네 줄.*?```scratchblocks\n(.*?)```", D2, re.S).group(1).rstrip()
LED = json.loads((OUT / "led_frames.json").read_text())


# ---------------------------------------------------------------- 조각
def strip_comments(py):
    """좁은 칸에 넣을 코드에서 # 주석을 뺀다 (주석은 .py 파일에서 봄).
    ※ 예제 코드의 문자열 속에는 #이 없다는 가정"""
    out = []
    for line in py.split("\n"):
        if not line.lstrip().startswith("#"):
            out.append(line.split("#")[0].rstrip())
    return "\n".join(out)


def code(py, comments=False):
    # Scratch와 나란히 놓는 좁은 칸은 글씨가 작아지지 않게 주석을 뺀다
    return f'<pre class="code"><code>{html.escape(py if comments else strip_comments(py))}</code></pre>'


def blocks(sb):
    sb = re.sub(r" *//.*$", "", sb, flags=re.M)  # 블록 옆 메모는 슬라이드에서 뺌 (아래 설명으로 대신)
    return f'<div class="sbwrap"><pre class="blocks">{html.escape(sb)}</pre></div>'


def led(key, captions=None):
    cells = []
    for i, frame in enumerate(LED[key]):
        px = "".join(
            f'<i style="--c:rgb({r},{g},{b})"{" class=off" if (r, g, b) == (0, 0, 0) else ""}></i>'
            for r, g, b in frame)
        cap = f"<span>{captions[i]}</span>" if captions else ""
        cells.append(f'<div class="ledbox"><div class="led">{px}</div>{cap}</div>')
    return '<div class="ledrow">' + '<b class="arrow">→</b>'.join(cells) + "</div>"


def img(name, cap="", cls=""):
    c = f"<figcaption>{cap}</figcaption>" if cap else ""
    return f'<figure class="{cls}"><img src="images/{name}" alt="{html.escape(cap)}">{c}</figure>'


def ul(items):
    return "<ul>" + "".join(f"<li>{md_inline(i) if isinstance(i, str) and not i.startswith('<') else i}</li>" for i in items) + "</ul>"


def qr(url, label):
    return f'<div class="qr"><div class="qrcode" data-url="{url}"></div><div class="qrlabel">{label}</div></div>'


SLIDES = []


def slide(title, body, notes="", cls="", part=""):
    SLIDES.append((title, body, notes, cls, part))


# ================================================================ 1차시
slide("", f"""
<div class="cover">
  <div class="cover-text">
    <p class="kicker">초·중·고 교사 연수 · 3차시 150분</p>
    <h1>라즈베리파이와 SenseHAT으로<br>배우는 <em>피지컬 컴퓨팅</em></h1>
    <p class="who">강사 <b>오정훈</b> · 부산동고등학교</p>
  </div>
  <div class="cover-art">{led("s04")}{img("web_pi4_product.png", "", "cover-img")}</div>
</div>""", cls="cover-slide")

slide("오늘의 여정", f"""
<div class="cards3">
  <div class="card"><div class="num">1차시</div><h3>시작하기</h3>{img("imager_01_device.png")}<p>OS 설치 · 한글 설정 · 첫 코드</p></div>
  <div class="card"><div class="num">2차시</div><h3>파이썬 기초 12단계</h3>{led("s06")}<p>한 단계 = 새 개념 1개</p></div>
  <div class="card"><div class="num">3차시</div><h3>미니 프로젝트</h3>{led("p03")}<p>기울기 · 컬러 · 주사위 + 수업 적용</p></div>
</div>
<p class="big center">코드를 몰라도 괜찮습니다. <b>한 번에 한 가지씩!</b></p>""",
      "오늘은 코드를 거의 몰라도 괜찮습니다. 한 번에 한 가지씩만 배웁니다.", part="1차시")

slide("지금 바로! SD카드 굽기 시작", f"""
<div class="two">
  <div>
    <p class="big">설치할 OS: <b>Raspberry Pi OS Full (64-bit)</b><br><small>Scratch 3 · Thonny · SenseHAT 라이브러리 포함</small></p>
    <div class="flow"><span>장치</span><span>운영 체제</span><span>저장소</span><span>사용자 지정</span><span>기록</span></div>
    <table class="settings">
      <tr><th>호스트 이름</th><td><code>raspberrypi</code> (그대로)</td></tr>
      <tr><th>지역화</th><td>수도 도시 <b>Seoul</b> → 시간대·키보드 자동</td></tr>
      <tr><th>사용자</th><td><code>pi</code> / <code>11111111</code></td></tr>
      <tr><th>Wi‑Fi</th><td><code>SWAI_5G</code> / <code>swai2024</code></td></tr>
    </table>
  </div>
  <div>{img("imager_01_device.png", "Raspberry Pi Imager 2.0")}</div>
</div>""", "굽는 데 10분 넘게 걸리니, 시작 버튼만 누르고 앞을 봐 주세요. 이미지 파일은 USB 메모리로 나눠 드립니다.")

slide("Imager 따라 하기 ① 장치 · 운영 체제", f"""
<div class="gallery3">
  {img("imager_01_device.png", "① Raspberry Pi 4")}
  {img("imager_02_os_list.png", "② Raspberry Pi OS (other)")}
  {img("imager_03_os_full.png", "③ Full (64-bit)")}
</div>
<p class="note">USB로 받은 파일을 쓸 때는 목록 맨 아래 <b>사용자 정의 이미지 사용</b></p>""")

slide("Imager 따라 하기 ② 저장소 · 이름 · 지역", f"""
<div class="gallery3">
  {img("imager_04_storage.png", "④ 내 SD카드")}
  {img("imager_05_hostname.png", "⑤ raspberrypi")}
  {img("imager_06_locale.png", "⑥ 수도 도시 Seoul")}
</div>
<p class="note warn">⚠ 저장소는 반드시 <b>SD카드</b>! 다른 USB 저장장치를 고르면 지워집니다.</p>""")

slide("Imager 따라 하기 ③ 사용자 · Wi‑Fi", f"""
<div class="gallery3">
  {img("imager_07_user.png", "⑦ pi / 11111111")}
  {img("imager_08_wifi.png", "⑧ SWAI_5G / swai2024")}
  {img("imager_09_ssh.png", "⑨ SSH는 켜지 않음")}
</div>
<p class="note">Wi‑Fi 칸에 지금 연결된 이름이 미리 채워져 있으면 지우고 <code>SWAI_5G</code> 입력</p>""")

slide("Imager 따라 하기 ④ 기록", f"""
<div class="two">
  <div>{img("imager_10_connect.png", "⑩ 라즈베리 파이 커넥트: 켜지 않음")}</div>
  <div>{img("imager_11_write.png", "⑪ 요약 확인 → 기록")}</div>
</div>
<p class="note warn">⚠ 기록하면 SD카드의 내용이 <b>모두 지워집니다</b></p>""")

slide("참고 영상 · OS 설치 (Imager 2.0)", f"""
<div class="qrs">
  {qr("https://www.youtube.com/watch?v=RV0saVGXQ5k", "How to Install Raspberry Pi OS<br>Using Imager 2.0<br><small>Gadgets Pod · 2025.11</small>")}
  {qr("https://www.youtube.com/watch?v=MepM1juFYzA", "Raspberry Pi Imager 2.0:<br>Set Up in Minutes<br><small>Gary Explains · 2025.11</small>")}
</div>
<p class="note">Imager는 2025년 10월 2.0으로 크게 바뀌었습니다. 예전(1.x) 영상은 화면이 다릅니다.</p>""")

slide("피지컬 컴퓨팅이란?", f"""
<svg class="diagram" viewBox="0 0 1400 330">
  <defs><marker id="ar" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#c51a4a"/></marker></defs>
  <g font-size="34" text-anchor="middle">
    <rect x="20" y="60" width="360" height="200" rx="24" fill="#e8f4ff" stroke="#306998" stroke-width="4"/>
    <text x="200" y="135" font-weight="bold" fill="#306998">입력</text><text x="200" y="190">센서 · 버튼</text><text x="200" y="235" font-size="26" fill="#555">온도 · 기울기 · 조이스틱</text>
    <rect x="520" y="60" width="360" height="200" rx="24" fill="#fdecef" stroke="#c51a4a" stroke-width="4"/>
    <text x="700" y="135" font-weight="bold" fill="#c51a4a">처리</text><text x="700" y="190">라즈베리파이</text><text x="700" y="235" font-size="26" fill="#555">우리가 짠 프로그램</text>
    <rect x="1020" y="60" width="360" height="200" rx="24" fill="#eefbe8" stroke="#3c8d1f" stroke-width="4"/>
    <text x="1200" y="135" font-weight="bold" fill="#3c8d1f">출력</text><text x="1200" y="190">LED · 화면 · 소리</text><text x="1200" y="235" font-size="26" fill="#555">8×8 컬러 LED</text>
  </g>
  <path d="M390 160 H505" stroke="#c51a4a" stroke-width="8" marker-end="url(#ar)"/>
  <path d="M890 160 H1005" stroke="#c51a4a" stroke-width="8" marker-end="url(#ar)"/>
</svg>
<p class="big center">컴퓨터가 <b>세상을 느끼고</b> <b>반응</b>하는 것 → 생활 속 예: 자동문 · 스마트 가로등 · 체온계</p>""")

slide("공식 홈페이지", f"""
<div class="two">
  <div>
    <p class="url">raspberrypi<b>.com</b></p><p>라즈베리파이 회사<br>제품 · OS 다운로드 · 설명서</p>
    <p class="url">raspberrypi<b>.org</b></p><p>라즈베리파이 재단<br><b>무료</b> 수업 자료 · 교사 연수 · 코드 클럽</p>
  </div>
  <div>{img("web_raspberrypi_com.png", "출처: raspberrypi.com")}</div>
</div>""")

slide("영국 교실의 컴퓨팅 수업", f"""
<div class="two">
  <div>{img("web_rpf_teach_hero.png", "출처: raspberrypi.org/teach")}</div>
  <div>{img("web_rpf_teach_classroom.png", "출처: raspberrypi.org/teach")}</div>
</div>
<p class="big center">영국은 초등학생부터 컴퓨팅을 배우고, 재단은 수업 자료와 교사 연수를 <b>무료</b>로 제공합니다</p>""")

TIMELINE = [("2009", "재단 설립", "영국 케임브리지"), ("2012", "Pi 1", "35달러"), ("2015", "Pi Zero · Astro Pi", "우주정거장에!"),
            ("2016", "Pi 3", "Wi‑Fi 내장"), ("2019", "Pi 4", "오늘 쓰는 보드"), ("2021", "Pico", "마이크로컨트롤러"), ("2023", "Pi 5", "최신")]
tl = "".join(
    f'<g transform="translate({90 + i * 205},0)"><circle cy="150" r="{24 if y == "2019" else 16}" fill="{"#c51a4a" if y == "2019" else "#6cc04a"}"/>'
    f'<text y="{95 if i % 2 else 225}" text-anchor="middle" font-size="34" font-weight="bold">{y}</text>'
    f'<text y="{55 if i % 2 else 265}" text-anchor="middle" font-size="26">{t}</text>'
    f'<text y="{20 if i % 2 else 300}" text-anchor="middle" font-size="22" fill="#666">{d}</text></g>'
    for i, (y, t, d) in enumerate(TIMELINE))
slide("라즈베리파이의 역사", f"""
<svg class="diagram" viewBox="0 0 1420 330"><line x1="40" y1="150" x2="1380" y2="150" stroke="#bbb" stroke-width="8"/>{tl}</svg>
<p class="big center">"학생들이 <b>싸고 쉽게</b> 프로그래밍을 배울 컴퓨터" → 전 세계 <b>수천만 대</b></p>""",
      "2009년 케임브리지 대학의 에벤 업튼 등이 재단을 세웠습니다. 2015년에는 SenseHAT을 단 Astro Pi가 우주정거장에 갔습니다.")

slide("Raspberry Pi 4B 제원", f"""
<div class="two">
  <div>{img("web_pi4_product.png", "출처: raspberrypi.com")}</div>
  <div><table class="spec">
    <tr><th>CPU</th><td>4코어 ARM Cortex‑A72 · 1.8GHz</td></tr>
    <tr><th>메모리</th><td><b>8GB</b></td></tr>
    <tr><th>무선</th><td>Wi‑Fi 2.4/5GHz · 블루투스 5.0</td></tr>
    <tr><th>USB</th><td>USB 3.0 ×2 · USB 2.0 ×2</td></tr>
    <tr><th>화면</th><td>HDMI ×2 (4K)</td></tr>
    <tr><th>저장</th><td>microSD 카드</td></tr>
    <tr><th>전원</th><td>USB‑C 5V 3A</td></tr>
    <tr class="hl"><th>GPIO</th><td><b>40핀</b> → SenseHAT을 꽂는 곳</td></tr>
  </table></div>
</div>""")

BARS = [("1GB", 35, 35), ("4GB", 55, 100), ("8GB", 75, 165)]
bars = "".join(
    f'<g transform="translate({140 + i * 400},0)">'
    f'<rect x="0" y="{360 - a * 1.9}" width="120" height="{a * 1.9}" fill="#9bb7d4"/><text x="60" y="{350 - a * 1.9}" text-anchor="middle" font-size="30">${a}</text>'
    f'<rect x="140" y="{360 - b * 1.9}" width="120" height="{b * 1.9}" fill="#c51a4a"/><text x="200" y="{350 - b * 1.9}" text-anchor="middle" font-size="30" font-weight="bold">${b}</text>'
    f'<text x="130" y="405" text-anchor="middle" font-size="32" font-weight="bold">{m}</text></g>'
    for i, (m, a, b) in enumerate(BARS))
slide("가격: 35달러 컴퓨터가 비싸진 이유", f"""
<div class="two wide-left">
  <svg class="diagram" viewBox="0 0 1260 440"><line x1="80" y1="360" x2="1240" y2="360" stroke="#999" stroke-width="3"/>{bars}
    <rect x="880" y="10" width="28" height="28" fill="#9bb7d4"/><text x="918" y="34" font-size="26">출시 가격</text>
    <rect x="880" y="50" width="28" height="28" fill="#c51a4a"/><text x="918" y="74" font-size="26">2026년 4월 이후</text></svg>
  <div>{ul(["**AI 데이터센터**가 고성능 메모리를 대량으로 씀", "메모리 공장이 그쪽 생산으로 몰림", "LPDDR4 메모리 값 1년 새 **약 7배**", "메모리가 큰 모델일수록 많이 오름"])}
  <p class="src">라즈베리파이 공식 발표 (2025.12 · 2026.2 · 2026.4)</p></div>
</div>""", "AI 발전이 교실 컴퓨터 값에도 영향을 줍니다. 학생들과 반도체 수요와 공급 이야기를 나눠 보세요.")

slide("소개 영상", f"""
<div class="qrs">
  {qr("https://www.youtube.com/watch?v=uXUjwk2-qx4", "What is a Raspberry Pi?<br><small>공식 채널 · 영어</small>")}
  {qr("https://www.youtube.com/watch?v=5Oz78pxED80", "What is a Raspberry Pi 4<br><small>공식 채널 · 영어</small>")}
  {qr("https://www.youtube.com/watch?v=rFtrC11zcsc", "라즈베리 파이 소개 및 설치 방법<br><small>다두이노 · 한국어</small>")}
</div>""", "시간이 되면 2~3분 정도 보여 줍니다.")

slide("Argon One V2 케이스", f"""
<div class="two">
  <svg class="diagram" viewBox="0 0 700 460">
    <rect x="60" y="80" width="580" height="300" rx="30" fill="#d9dde2" stroke="#8a929b" stroke-width="5"/>
    <rect x="150" y="120" width="400" height="90" rx="12" fill="#3a3f45"/><text x="350" y="175" text-anchor="middle" font-size="28" fill="#fff">자석 덮개 → GPIO 40핀</text>
    <text x="350" y="275" text-anchor="middle" font-size="30" fill="#333">알루미늄 케이스 + 냉각 팬</text>
    <rect x="60" y="380" width="580" height="46" fill="#8a929b"/><text x="350" y="413" text-anchor="middle" font-size="26" fill="#fff">뒤쪽: 모든 단자 (전원 · HDMI ×2 · USB · LAN)</text>
    <circle cx="610" cy="355" r="14" fill="#c51a4a"/><text x="560" y="345" text-anchor="end" font-size="24">전원 버튼</text>
  </svg>
  <div>{ul(["단자가 **뒤쪽**으로 모여 있음", "HDMI는 **일반 크기** (micro‑HDMI 케이블 필요 없음)", "위쪽 **자석 덮개**를 열고 SenseHAT 장착", "전원 버튼: 짧게 = 켜기, 길게 = 끄기", "SenseHAT이 **거꾸로** 꽂힘 → 코드에서 화면 180° 회전"])}</div>
</div>""")

slide("SenseHAT 한눈에 보기", f"""
<div class="two">
  <div>{img("web_sensehat_product.png", "출처: raspberrypi.com")}</div>
  <div><table class="spec">
    <tr><th>8×8 RGB LED</th><td>64개 점으로 글자·그림</td></tr>
    <tr><th>조이스틱</th><td>상하좌우 + 누르기</td></tr>
    <tr><th>온도·습도</th><td>℃, %</td></tr>
    <tr><th>기압</th><td>hPa</td></tr>
    <tr><th>움직임</th><td>기울기 · 흔들림 · 방향</td></tr>
    <tr class="hl"><th>컬러 (V2)</th><td>물체의 색</td></tr>
  </table></div>
</div>""", "원래 우주정거장에 간 보드입니다(Astro Pi).")

grid = "".join(
    f'<i class="{"g" if (x, y) == (0, 0) else "r" if (x, y) == (7, 7) else ""}">{"0,0" if (x, y) == (0, 0) else "7,7" if (x, y) == (7, 7) else ""}</i>'
    for y in range(8) for x in range(8))
slide("LED 좌표", f"""
<div class="two">
  <div class="coord"><div class="xlab">x →&nbsp;&nbsp;0 1 2 3 4 5 6 7</div><div class="ylab">y ↓</div><div class="cgrid">{grid}</div></div>
  <div>{ul(["왼쪽 위가 **(0, 0)**", "오른쪽 아래가 **(7, 7)**", "x는 오른쪽으로, y는 **아래로** 커짐", "`set_pixel(x, y, 색)`으로 점 하나 켜기"])}</div>
</div>""")

slide("첫 부팅", f"""
<div class="two">
  <div class="rainbow-wrap"><div class="led rainbow"></div><p class="center">부팅할 때 잠깐 켜지는 <b>무지개</b></p></div>
  <div>{ul(["SD카드 꽂고 전원 연결", "SenseHAT에 **무지개 LED** → 정상", "바탕화면이 나오면 **Wi‑Fi** 확인", "무지개가 안 켜지면 전원을 끄고 핀 확인"])}</div>
</div>""")

slide("한글 설정 ① 글꼴과 입력기 설치", f"""
<div class="two">
  <div><pre class="code term"><code>sudo apt update
sudo apt install -y fonts-nanum fcitx5-hangul</code></pre>
  {ul(["비밀번호 `11111111` (화면에 안 보이는 게 정상)", "틀리면 “다시 시도하십시오” → 다시 입력"])}</div>
  <div>{img("terminal_install.png", "터미널 화면")}</div>
</div>""")

slide("한글 설정 ② 화면 언어를 한국어로", f"""
<div class="two">
  <div>{img("locale_01_localisation.png", "Preferences → Control Centre → Localisation")}</div>
  <div>{img("locale_02_set_locale.png", "Set Locale: ko (Korean) · KR · UTF-8")}</div>
</div>
<pre class="code term center-code"><code>sudo reboot</code></pre>
<p class="note">Imager의 Seoul 설정은 시간대·키보드만 바꿉니다. 화면 언어는 여기서!</p>""")

slide("한글 설정 ③ 입력기에 한글 추가", f"""
<div class="two">
  <div>{ul(["키보드 아이콘 **오른쪽 클릭** → 설정", "**입력기 검색**에 `한글` → 선택", "가운데 **◀** 로 추가 → **적용**", "**한/영 키**로 전환 확인"])}</div>
  <div>{img("fcitx5_config.png", "Fcitx 구성: 현재 입력기에 한글")}</div>
</div>""")


def compare(title, py, sb, key, lines="", notes="", captions=None, part=""):
    body = f"""<div class="cmp">
  <div class="col py"><div class="tag">Python</div>{code(py)}</div>
  <div class="col sc"><div class="tag">Scratch</div>{blocks(sb) if sb else '<p class="nosb">Scratch 블록 없음<br>(Python만)</p>'}</div>
  <div class="col out"><div class="tag">LED 결과</div>{led(key, captions)}</div>
</div>{lines}"""
    slide(title, body, notes, part=part)


compare("첫 코드 — Hello!", FIRST_PY, FIRST_SB, "s00",
        '<p class="note warn">⚠ LED에는 <b>영문·숫자</b>만 나옵니다. 한글은 깨져요.</p>',
        "메뉴 → 프로그래밍 → Thonny, Scratch는 확장 기능에서 Raspberry Pi Sense HAT 추가")

# ================================================================ 2차시
slide("", '<div class="divider"><p>2차시</p><h1>SenseHAT으로 배우는<br>파이썬 기초 12단계</h1></div>', cls="div-slide", part="2차시")

slide("규칙과 첫 네 줄", f"""
<div class="two">
  <div><p class="big">한 단계 = <b>새 개념 1개</b></p><div class="flow small"><span>입력</span><span>▶ 실행</span><span>바꿔 보기</span></div>
  {code(HEAD_PY)}<p class="note">이 네 줄은 <b>모든 코드의 맨 위</b>에 (이후 슬라이드에서는 생략)</p></div>
  <div>{blocks(HEAD_SB)}<p class="note">Scratch도 초록 깃발 아래에 항상 먼저</p></div>
</div>""", "set_rotation(180)은 Argon 케이스에서 SenseHAT이 거꾸로 꽂히기 때문입니다.")

CONCEPT = {
    "s01": "명령은 <code>sense.명령(...)</code>", "s02": "변수 = 이름표 붙인 상자", "s03": "(빨강, 초록, 파랑) 0~255",
    "s04": "<code>set_pixel(x, y, 색)</code>", "s05": "위에서 아래로 한 줄씩, <code>sleep</code>은 기다리기",
    "s06": "들여쓰기 4칸 = 반복할 부분", "s07": "<code>[ ]</code>에 여러 개를 순서대로", "s08": "<code>round</code> 반올림, <code>str</code> 글자로",
    "s09": "<code>:</code>과 들여쓰기", "s10": "멈출 때는 Thonny의 Stop ■", "s11": "<code>==</code>는 “같은가?”", "s12": "<code>def</code>로 나만의 명령",
}
CAPS = {"s05": ["1초", "1초 뒤"], "s07": ["1초", "", ""], "s08": ["예: 28℃", ""], "s09": ["30℃ 넘으면", "아니면"],
        "s10": ["1초마다", "계속"], "s11": ["up 누르면", ""], "s12": ["flash(빨강)", "flash(파랑)"]}
for key in [f"s{i:02d}" for i in range(1, 13)]:
    title, py, sb, bullets = S2[key]
    try_it = next((b for b in bullets if b.startswith("🔁")), "")
    warn = next((b for b in bullets if b.startswith("⚠️")), "")
    lines = f'<div class="concept"><span>새 개념</span> {CONCEPT[key]}</div>'
    if try_it:
        lines += f'<p class="try">{md_inline(try_it)}</p>'
    if warn:
        lines += f'<p class="note warn">{md_inline(warn)}</p>'
    compare(f"{key} · {title}", py, sb, key, lines, captions=CAPS.get(key))

slide("정리: 오늘 배운 문법", f"""
<table class="summary">
<tr><th>문법</th><th>뜻</th><th>단계</th></tr>
<tr><td><code>명령(...)</code></td><td>일 시키기</td><td>s01</td></tr>
<tr><td><code>이름 = 값</code></td><td>변수에 담기</td><td>s02</td></tr>
<tr><td><code>(R, G, B)</code></td><td>색</td><td>s03</td></tr>
<tr><td><code>for ... in range()</code></td><td>정해진 횟수 반복</td><td>s06</td></tr>
<tr><td><code>[a, b, c]</code></td><td>리스트</td><td>s07</td></tr>
<tr><td><code>str()</code> · <code>round()</code></td><td>글자로 · 반올림</td><td>s08</td></tr>
<tr><td><code>if / else</code></td><td>조건</td><td>s09</td></tr>
<tr><td><code>while True</code></td><td>무한 반복</td><td>s10</td></tr>
<tr><td><code>def</code></td><td>함수 만들기</td><td>s12</td></tr>
</table>""")

slide("자주 나는 오류 3가지", f"""
<div class="cards3 errors">
  <div class="card"><h3>IndentationError</h3><p>들여쓰기가 맞지 않음</p><pre class="code"><code>for x in range(8):
sense.set_pixel(x, 0, (255, 0, 0))</code></pre><p>→ 스페이스 4칸</p></div>
  <div class="card"><h3>SyntaxError</h3><p><code>:</code> 또는 따옴표가 빠짐</p><pre class="code"><code>if t > 30
    sense.clear(255, 0, 0)</code></pre><p>→ 줄 끝에 <code>:</code></p></div>
  <div class="card"><h3>NameError</h3><p>철자·대소문자가 다름</p><pre class="code"><code>sense = sensehat()</code></pre><p>→ <code>SenseHat</code></p></div>
</div>
<p class="big center">빨간 오류 메시지의 <b>마지막 줄</b>부터 읽어 보세요</p>""")

# ================================================================ 3차시
slide("", '<div class="divider"><p>3차시</p><h1>미니 프로젝트와<br>수업 적용</h1></div>', cls="div-slide", part="3차시")

slide("프로젝트 고르기", f"""
<div class="cards3">
  <div class="card"><div class="num">p01</div><h3>기울이면 화살표</h3>{led("p01")}<p>움직임 센서 · <code>elif</code></p></div>
  <div class="card"><div class="num">p02</div><h3>카멜레온</h3>{led("p02")}<p>컬러 센서 (V2) · Python만</p></div>
  <div class="card"><div class="num">p03</div><h3>전자 주사위</h3>{led("p03")}<p>조이스틱 · 무작위</p></div>
</div>
<p class="big center">2차시에서 배운 것만 조합합니다. 끝나면 다른 것도!</p>""")

for key, caps, extra in [
    ("p01", ["왼쪽", "오른쪽"], '<p class="note warn">⚠ SenseHAT이 거꾸로라 센서의 왼쪽·오른쪽도 반대 → Scratch는 <code>right</code>에 L</p>'),
    ("p02", None, '<p class="note">어두우면 색이 잘 안 나옵니다 → <b>휴대폰 손전등</b>으로 비추기</p>'),
    ("p03", None, '<p class="note">Python은 조이스틱, Scratch는 <b>흔들면</b> 주사위</p>'),
]:
    title, py, sb, bullets = S3[key]
    compare(f"{key} · {title}", py, sb, key, extra, captions=caps)

slide("센서 이야기: 온도는 왜 높을까?", f"""
<div class="two">
  <svg class="diagram" viewBox="0 0 640 420">
    <rect x="60" y="260" width="520" height="70" rx="10" fill="#2f7d32"/><text x="320" y="305" text-anchor="middle" font-size="28" fill="#fff">라즈베리파이 (CPU ~50℃)</text>
    <rect x="60" y="120" width="520" height="70" rx="10" fill="#1b5e20"/><text x="320" y="165" text-anchor="middle" font-size="28" fill="#fff">SenseHAT 온도 센서</text>
    <g stroke="#e53935" stroke-width="7" fill="none" stroke-linecap="round">
      <path d="M180 250 q -18 -15 0 -30 q 18 -15 0 -30"/><path d="M320 250 q -18 -15 0 -30 q 18 -15 0 -30"/><path d="M460 250 q -18 -15 0 -30 q 18 -15 0 -30"/></g>
    <text x="320" y="80" text-anchor="middle" font-size="34" font-weight="bold" fill="#e53935">열이 위로!</text>
  </svg>
  <div>{ul(["방 온도계와 비교 → SenseHAT이 **5~15℃ 높음**", "CPU 열이 바로 위의 센서로 올라감", "해결: 떨어뜨리기 또는 **차이만큼 빼기**", "`t = sense.get_temperature() - 10`"])}</div>
</div>""", "센서 값도 확인하고 보정해야 한다는 것 자체가 좋은 과학 수업 소재입니다.")

slide("학교급별 적용", f"""
<div class="cards3">
  <div class="card"><div class="num">초등</div><h3>Scratch</h3>{led("s04")}<p>LED 픽셀아트 이름표<br>흔들면 주사위 · 신호등</p></div>
  <div class="card"><div class="num">중학교</div><h3>Scratch → Python</h3>{led("s09")}<p>순차 · 반복 · 조건<br>온도 알리미</p></div>
  <div class="card"><div class="num">고등학교</div><h3>Python</h3>{led("s08")}<p>온습도 측정·기록<br>센서 보정 실험 · 함수</p></div>
</div>""")

slide("수업 팁", f"""
<div class="two">
  <div>{ul(["**짝 코딩**: 한 명은 입력, 한 명은 읽어 주기 → 5분마다 교대", "처음에는 **완성 코드 → 바꿔 보기**부터", "오류 메시지 **마지막 줄**을 같이 읽기", "끝나면 `sense.clear()`로 LED 끄기"])}</div>
  <div>{img("web_rpf_teach_classroom.png", "출처: raspberrypi.org/teach")}</div>
</div>""")

slide("마무리", f"""
<div class="two">
  <div>{ul(["자료 폴더 `sensehat-workshop/`", "교재 PDF · Python 16개 · Scratch 15개", "라즈베리파이 재단 무료 수업 자료"])}
  <p class="big">질문 있으신가요?</p><p class="who">오정훈 · 부산동고등학교</p></div>
  <div class="qrs">{qr("https://www.raspberrypi.org/teach/", "재단 교사용 자료<br><small>raspberrypi.org/teach</small>")}
  {qr("https://www.raspberrypi.com/documentation/accessories/sense-hat.html", "SenseHAT 공식 문서<br><small>raspberrypi.com</small>")}</div>
</div>""")


# ================================================================ 부록: 추가 예제
HEADER = ["from sense_hat import SenseHat", "sense = SenseHat()", "sense.set_rotation(180)", "sense.clear()"]


def extra(path, shrink=True):
    """예제 파일 → (번호, 제목, 새 개념, 첫 네 줄을 뺀 코드)"""
    lines = path.read_text(encoding="utf-8").rstrip().split("\n")
    key, rest = lines[0].lstrip("# ").split(" · ", 1)
    title, concept = rest.split(" — ", 1)
    body = lines[1:]
    for h in HEADER:                    # 맨 위의 첫 네 줄만 뺀다 (본문 속 clear()는 남김, 주석은 무시)
        body.remove(next(l for l in body if l.split("#")[0].rstrip() == h))
    while body and not body[0].strip():
        body.pop(0)
    code_text = "\n".join(body)
    if shrink and len(body) > 30:       # 너무 길면 64칸 그림 리스트 속을 한 줄로 줄여 보여 준다
        code_text = re.sub(r"^(\w+) = \[.*\n(?:    .*\n)+\]", r"\1 = [ … 8줄 × 8칸 그림 (전체는 파일에) … ]", code_text, flags=re.M)
    return key, title, concept, code_text


EXTRAS = [extra(p) for p in sorted((ROOT / "code" / "python" / "extra").glob("e*.py"))]
EXTRA_CAPS = {
    "e03": ["크게", "작게"], "e04": ["5 → 1", "GO!"], "e05": ["예: 43%", ""], "e06": ["25℃쯤", "35℃쯤"],
    "e07": ["처음", "위로 밀면"], "e08": ["가운데", "오른쪽으로 기울이면"], "e09": ["기다림", "흔들면"],
    "e10": ["초록불!", "반응 시간(ms)"], "e11": ["기록 중", "Saved"], "e12": ["빨간 물체", "파란 물체"],
}

slide("", '<div class="divider"><p>부록</p><h1>더 해 보기<br>추가 Python 예제 12개</h1></div>', cls="div-slide", part="부록")

cards = "".join(
    f'<div class="mini"><div class="num">{k}</div>{led(k)}<h4>{html.escape(t)}</h4></div>'
    for k, t, c, _ in EXTRAS)
slide("추가 예제 한눈에 보기", f'<div class="minis">{cards}</div>'
      '<p class="note">파일 위치: <code>code/python/extra/</code> · 모두 첫 네 줄(회전·지우기)로 시작</p>')

def extra_slides(items, concept_label):
    for k, t, c, py in items:
        slide(f"{k} · {t}", f"""<div class="cmp only-py">
  <div class="col py"><div class="tag">Python <small>(첫 네 줄 생략)</small></div>{code(py, comments=True)}</div>
  <div class="col out"><div class="tag">LED 결과</div>{led(k, EXTRA_CAPS.get(k))}</div>
</div><div class="concept"><span>{concept_label}</span> {html.escape(c)}</div>""")


extra_slides(EXTRAS, "새로 나오는 것")

# ---------------------------------------------------------------- 부록: 게임
GAMES = [extra(p, shrink=False) for p in sorted((ROOT / "code" / "python" / "game").glob("g*.py"))]   # 미로 지도는 줄이지 않음
EXTRA_CAPS.update({
    "g01": ["처음", "사과 3개 먹은 뒤"], "g02": ["피하는 중", "맞으면 쾅!"], "g03": ["출발", "출구 가까이"],
    "g04": ["① 위", "② 왼쪽"],
})

slide("", '<div class="divider"><p>부록</p><h1>더 해 보기<br>게임 4개</h1></div>', cls="div-slide", part="부록")

cards = "".join(
    f'<div class="mini"><div class="num">{k}</div>{led(k)}<h4>{html.escape(t)}</h4></div>'
    for k, t, c, _ in GAMES)
slide("게임 한눈에 보기", f'<div class="minis">{cards}</div>'
      '<p class="note">파일 위치: <code>code/python/game/</code> · 기울기 게임은 시작할 때 기기를 가만히 두기</p>')



MAX_LINES = 26   # 슬라이드 한 장에 읽을 만한 크기로 들어가는 코드 줄 수


def pieces(py):
    """긴 게임 코드를 빈 줄에서 끊어, 가장 적은 장 수로 나눈다 (그중 가장 긴 장이 가장 짧게)"""
    lines = py.split("\n")
    cuts = [i for i, l in enumerate(lines) if not l.strip()]
    # best[i] = lines[:i]를 나누는 (장 수, 가장 긴 장의 줄 수, 끊는 자리들)
    best = {0: (0, 0, [])}
    for end in cuts + [len(lines)]:
        options = [(n + 1, max(m, end - start), at + [end]) for start, (n, m, at) in best.items()
                   if start < end and end - start <= MAX_LINES]
        if options:
            best[end + 1] = min(options)
    n, m, at = best[len(lines) + 1]
    starts = [0] + [e + 1 for e in at[:-1]]
    return ["\n".join(lines[a:b]) for a, b in zip(starts, at)]


# 게임 코드는 한 장에 다 들어가지 않으므로 여러 장으로 나눠 보여 준다
for k, t, c, py in GAMES:
    parts = pieces(py)
    for n, part in enumerate(parts, 1):
        slide(f"{k} · {t} ({n}/{len(parts)})", f"""<div class="cmp only-py">
  <div class="col py"><div class="tag">Python <small>({"첫 네 줄 생략" if n == 1 else "이어서"})</small></div>{code(part, comments=True)}</div>
  <div class="col out"><div class="tag">LED 결과</div>{led(k, EXTRA_CAPS.get(k))}</div>
</div><div class="concept"><span>게임 방법</span> {html.escape(c)}</div>""")


# ---------------------------------------------------------------- 출력
CSS = (ROOT / "tools" / "slides.css").read_text(encoding="utf-8")
JS = (ROOT / "tools" / "slides.js").read_text(encoding="utf-8")

parts = []
for i, (title, body, notes, cls, part) in enumerate(SLIDES, 1):
    head = f'<header><h2>{html.escape(title)}</h2></header>' if title else ""
    note = f'<aside class="notes">강사: {html.escape(clean(notes))}</aside>' if notes else ""
    parts.append(f'<section class="slide {cls}" data-n="{i}">{head}<div class="body">{body}</div>{note}</section>')

page = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>라즈베리파이와 SenseHAT으로 배우는 피지컬 컴퓨팅</title>
<style>{CSS}</style>
<script src="lib/scratchblocks.min.js"></script><script src="lib/qrcode.min.js"></script>
</head><body>
<div id="stage">{''.join(parts)}</div>
<div id="bar"><span id="count"></span><span class="keys">← → 넘기기 · F 전체 화면 · N 강사 메모</span></div>
<script>{JS}</script>
</body></html>"""
(OUT / "index.html").write_text(page, encoding="utf-8")
print(f"만듦: slides/index.html (슬라이드 {len(SLIDES)}장)")
