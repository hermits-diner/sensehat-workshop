#!/usr/bin/env python3
"""docs/*.md 원고의 python 코드 블록을 code/python/*.py 파일로 만든다.

원고가 기준이다. 원고를 고친 뒤 이 스크립트를 다시 실행하면 코드 파일도 바뀐다.
사용법: python3 tools/make_code.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = ROOT / "code" / "python"

HEADER = [
    "from sense_hat import SenseHat",
    "sense = SenseHat()",
    "sense.set_rotation(180)",
    "sense.clear()",
]

# 단계 번호 → 파일 이름
NAMES = {
    "s00": "s00_hello", "s01": "s01_message", "s02": "s02_variable",
    "s03": "s03_colour", "s04": "s04_pixel", "s05": "s05_sequence",
    "s06": "s06_for", "s07": "s07_list", "s08": "s08_temperature",
    "s09": "s09_if", "s10": "s10_while", "s11": "s11_joystick",
    "s12": "s12_function", "p01": "p01_tilt", "p02": "p02_chameleon",
    "p03": "p03_dice",
}


def sections(md_text):
    """'## s01 · 제목' 또는 '## p01 · 제목' 단위로 (번호, 제목, 첫 python 코드) 돌려준다."""
    for m in re.finditer(r"^## ((?:s|p)\d\d) · (.+?)\n(.*?)(?=^## |\Z)", md_text, re.M | re.S):
        code = re.search(r"```python\n(.*?)```", m.group(3), re.S)
        if code:
            yield m.group(1), m.group(2).strip(), code.group(1).rstrip("\n")


def with_header(code):
    """생략된 첫 네 줄을 붙인다. 코드 속 import 줄은 맨 위 import 옆으로 올린다."""
    lines = code.split("\n")
    imports = [l for l in lines if l.startswith(("from ", "import "))]
    body = [l for l in lines if l not in imports]
    return "\n".join([HEADER[0], *imports, *HEADER[1:], "", *body])


def write(key, title, code):
    path = OUT / f"{NAMES[key]}.py"
    path.write_text(f"# {key} · {title}\n{code}\n", encoding="utf-8")
    print("만듦:", path.relative_to(ROOT))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)

    # 1차시 첫 코드 (전체 코드가 원고에 있음)
    first = (DOCS / "01_1차시.md").read_text(encoding="utf-8")
    write("s00", "첫 코드 — Hello", re.search(r"```python\n(.*?)```", first, re.S).group(1).rstrip("\n"))

    # 2차시: 첫 네 줄이 생략되어 있으므로 붙인다
    for key, title, code in sections((DOCS / "02_2차시.md").read_text(encoding="utf-8")):
        write(key, title, with_header(code))

    # 3차시: 전체 코드가 원고에 있음
    for key, title, code in sections((DOCS / "03_3차시.md").read_text(encoding="utf-8")):
        write(key, title, code)
