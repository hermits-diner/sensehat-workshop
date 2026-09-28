#!/usr/bin/env python3
"""Scratch 3 예제(.sb3)를 만든다. 블록 구성은 docs/*.md 원고의 scratchblocks와 같다.

.sb3 = project.json(블록 정보) + 그림 파일을 zip으로 묶은 것.
SenseHAT 확장 ID는 'pisensehat' (Raspberry Pi판 Scratch 3에 내장).
사용법: python3 tools/make_sb3.py
"""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "code" / "scratch"

# 빈 그림 (스프라이트 모양, 무대 배경)
SPRITE_SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="2" height="2" viewBox="0 0 2 2"></svg>'
STAGE_SVG = b'<svg xmlns="http://www.w3.org/2000/svg" width="480" height="360" viewBox="0 0 480 360"><rect width="480" height="360" fill="#ffffff"/></svg>'

# 입력 칸 기본값 종류 (Scratch 내부 번호)
NUM, POS, WHOLE, INT, COLOR, TEXT = 4, 5, 6, 7, 9, 10


class Project:
    """블록을 조립하는 도우미. 각 메서드는 블록 ID를 돌려준다."""

    def __init__(self):
        self.blocks, self.variables, self.lists = {}, {}, {}
        self._n = 0
        self._top_y = 0

    # ---- 기본 ----
    def _id(self):
        self._n += 1
        return f"b{self._n}"

    def block(self, opcode, inputs=None, fields=None, shadow=False, mutation=None):
        bid = self._id()
        self.blocks[bid] = {
            "opcode": opcode, "next": None, "parent": None,
            "inputs": inputs or {}, "fields": fields or {},
            "shadow": shadow, "topLevel": False,
        }
        if mutation:
            self.blocks[bid]["mutation"] = mutation
        # 입력 칸에 끼운 블록들의 부모를 이 블록으로
        for value in (inputs or {}).values():
            for ref in value[1:]:
                if isinstance(ref, str):
                    self.blocks[ref]["parent"] = bid
        return bid

    def stack(self, *ids):
        """블록들을 위에서 아래로 연결하고 첫 블록 ID를 돌려준다."""
        for a, b in zip(ids, ids[1:]):
            self.blocks[a]["next"] = b
            self.blocks[b]["parent"] = a
        return ids[0]

    def script(self, *ids):
        """맨 위 블록을 작업 공간에 놓는다."""
        first = self.stack(*ids)
        self.blocks[first].update(topLevel=True, x=40, y=40 + self._top_y)
        self._top_y += 80 + 50 * len(ids)
        return first

    def var(self, name):
        vid = f"var_{name}"
        self.variables.setdefault(vid, [name, 0])
        return vid

    def lst(self, name):
        lid = f"list_{name}"
        self.lists.setdefault(lid, [name, []])
        return lid

    # ---- 입력 칸 값 ----
    @staticmethod
    def val(kind, v):
        return [1, [kind, str(v)]]

    @staticmethod
    def rep(block_id, kind=TEXT):
        """입력 칸에 동그란 블록(reporter)을 끼운다.
        밑에 숨은 기본값은 색 칸이면 색 코드가 있어야 한다 (빈 값이면 Scratch가 못 연다)."""
        return [3, block_id, [kind, "#000000" if kind == COLOR else ""]]

    def varrep(self, name, kind=TEXT):
        return [3, [12, name, self.var(name)], [kind, ""]]

    def sub(self, first):
        return [2, first]

    # ---- 이벤트·제어 ----
    def flag(self):
        return self.block("event_whenflagclicked")

    def wait(self, sec):
        return self.block("control_wait", {"DURATION": self.val(POS, sec)})

    def repeat(self, times_input, *body):
        return self.block("control_repeat", {"TIMES": times_input, "SUBSTACK": self.sub(self.stack(*body))})

    def forever(self, *body):
        return self.block("control_forever", {"SUBSTACK": self.sub(self.stack(*body))})

    def if_else(self, cond, then, other):
        return self.block("control_if_else", {
            "CONDITION": [2, cond], "SUBSTACK": self.sub(then), "SUBSTACK2": self.sub(other)})

    # ---- 연산 ----
    def gt(self, left_input, right):
        return self.block("operator_gt", {"OPERAND1": left_input, "OPERAND2": self.val(TEXT, right)})

    def round(self, inner):
        return self.block("operator_round", {"NUM": self.rep(inner, NUM)})

    def random(self, a, b):
        return self.block("operator_random", {"FROM": self.val(NUM, a), "TO": self.val(NUM, b)})

    # ---- 변수·리스트 ----
    def set_var(self, name, value):
        return self.block("data_setvariableto", {"VALUE": self.val(TEXT, value)},
                          {"VARIABLE": [name, self.var(name)]})

    def change_var(self, name, by):
        return self.block("data_changevariableby", {"VALUE": self.val(NUM, by)},
                          {"VARIABLE": [name, self.var(name)]})

    def delete_all(self, name):
        return self.block("data_deletealloflist", fields={"LIST": [name, self.lst(name)]})

    def add_to(self, name, item):
        return self.block("data_addtolist", {"ITEM": self.val(TEXT, item)}, {"LIST": [name, self.lst(name)]})

    def item_of(self, name, index_input):
        return self.block("data_itemoflist", {"INDEX": index_input}, {"LIST": [name, self.lst(name)]})

    def length_of(self, name):
        return self.block("data_lengthoflist", fields={"LIST": [name, self.lst(name)]})

    # ---- SenseHAT 확장 ----
    def sh(self, op, inputs=None, fields=None):
        return self.block(f"pisensehat_{op}", inputs, fields)

    def coord(self, value):
        """x·y 좌표 칸: 숫자면 드롭다운, 문자열 'var:x'면 변수를 끼운다."""
        menu = self.block("pisensehat_menu_coords", fields={"coords": ["0", None]}, shadow=True)
        if isinstance(value, str) and value.startswith("var:"):
            name = value[4:]
            self.blocks[menu]["fields"]["coords"] = ["0", None]
            return [3, [12, name, self.var(name)], menu]
        self.blocks[menu]["fields"]["coords"] = [str(value), None]
        return [1, menu]

    def text(self, msg):
        return self.sh("scroll_message", {"MESSAGE": self.val(TEXT, msg)})

    def text_rep(self, inner):
        return self.sh("scroll_message", {"MESSAGE": self.rep(inner)})

    def letter(self, ch):
        return self.sh("show_letter", {"LETTER": self.val(TEXT, ch)})

    def colour(self, hex_):
        return self.sh("set_fg", {"COLOUR": self.val(COLOR, hex_)})

    def background(self, colour_input):
        return self.sh("set_bg", {"COLOUR": colour_input})

    def pixel(self, x, y, hex_):
        return self.sh("set_pixel", {"X": self.coord(x), "Y": self.coord(y), "COLOUR": self.val(COLOR, hex_)})

    def clear(self):
        return self.sh("all_off")

    def temperature(self):
        return self.sh("get_temp")

    def start(self):
        """모든 프로그램의 시작: 초록 깃발 → 180도 회전 → 화면 지우기"""
        return [self.flag(), self.sh("set_orient", fields={"ROT": ["180", None]}), self.clear()]

    # ---- 나만의 블록 (s12) ----
    def define(self, name, arg, *body):
        arg_id = f"arg_{arg}"
        mut = {"tagName": "mutation", "children": [], "proccode": f"{name} %s",
               "argumentids": json.dumps([arg_id]), "argumentnames": json.dumps([arg]),
               "argumentdefaults": json.dumps([""]), "warp": "false"}
        arg_shadow = self.block("argument_reporter_string_number", fields={"VALUE": [arg, None]}, shadow=True)
        proto = self.block("procedures_prototype", {arg_id: [1, arg_shadow]}, shadow=True, mutation=mut)
        define = self.block("procedures_definition", {"custom_block": [1, proto]})
        return self.stack(define, *body)

    def arg(self, arg):
        return self.block("argument_reporter_string_number", fields={"VALUE": [arg, None]})

    def call(self, name, arg, value):
        arg_id = f"arg_{arg}"
        mut = {"tagName": "mutation", "children": [], "proccode": f"{name} %s",
               "argumentids": json.dumps([arg_id]), "warp": "false"}
        return self.block("procedures_call", {arg_id: self.val(TEXT, value)}, mutation=mut)

    # ---- 저장 ----
    def save(self, path):
        sprite_md5 = hashlib.md5(SPRITE_SVG).hexdigest()
        stage_md5 = hashlib.md5(STAGE_SVG).hexdigest()
        project = {
            "targets": [
                {"isStage": True, "name": "Stage", "variables": self.variables, "lists": self.lists,
                 "broadcasts": {}, "blocks": {}, "comments": {}, "currentCostume": 0,
                 "costumes": [{"name": "backdrop1", "dataFormat": "svg", "assetId": stage_md5,
                               "md5ext": f"{stage_md5}.svg", "rotationCenterX": 240, "rotationCenterY": 180}],
                 "sounds": [], "volume": 100, "layerOrder": 0, "tempo": 60,
                 "videoTransparency": 50, "videoState": "on", "textToSpeechLanguage": None},
                {"isStage": False, "name": "Sprite1", "variables": {}, "lists": {}, "broadcasts": {},
                 "blocks": self.blocks, "comments": {}, "currentCostume": 0,
                 "costumes": [{"name": "costume1", "dataFormat": "svg", "assetId": sprite_md5,
                               "md5ext": f"{sprite_md5}.svg", "rotationCenterX": 1, "rotationCenterY": 1}],
                 "sounds": [], "volume": 100, "layerOrder": 1, "visible": True, "x": 0, "y": 0,
                 "size": 100, "direction": 90, "draggable": False, "rotationStyle": "all around"},
            ],
            "monitors": [],
            "extensions": ["pisensehat"],
            "meta": {"semver": "3.0.0", "vm": "0.2.0", "agent": "sensehat-workshop"},
        }
        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("project.json", json.dumps(project, ensure_ascii=False))
            z.writestr(f"{sprite_md5}.svg", SPRITE_SVG)
            z.writestr(f"{stage_md5}.svg", STAGE_SVG)


# ======================== 예제 (원고와 같은 순서) ========================
def s00(p):
    p.script(*p.start(), p.text("Hello"))

def s01(p):
    p.script(*p.start(), p.text("Hi"))

def s02(p):
    p.script(*p.start(), p.set_var("name", "Kim"), p.sh("scroll_message", {"MESSAGE": p.varrep("name")}))

def s03(p):
    p.script(*p.start(), p.colour("#ff0000"), p.text("Hi"))

def s04(p):
    p.script(*p.start(), p.pixel(0, 0, "#00ff00"))

def s05(p):
    p.script(*p.start(), p.letter("A"), p.wait(1), p.letter("B"), p.wait(1), p.clear())

def s06(p):
    p.script(*p.start(), p.set_var("x", 0),
             p.repeat(p.val(WHOLE, 8), p.pixel("var:x", 0, "#ff0000"), p.wait(0.2), p.change_var("x", 1)))

def s07(p):
    p.script(*p.start(), p.delete_all("colors"),
             p.add_to("colors", "#ff0000"), p.add_to("colors", "#ffff00"), p.add_to("colors", "#00ff00"),
             p.set_var("i", 1),
             p.repeat(p.rep(p.length_of("colors"), WHOLE),
                      p.background(p.rep(p.item_of("colors", p.varrep("i", INT)), COLOR)),
                      p.wait(1), p.change_var("i", 1)))

def s08(p):
    p.script(*p.start(), p.text_rep(p.round(p.temperature())))

def s09(p):
    p.script(*p.start(), p.if_else(p.gt(p.rep(p.temperature()), 30),
                                   p.background(p.val(COLOR, "#ff0000")),
                                   p.background(p.val(COLOR, "#0000ff"))))

def s10(p):
    p.script(*p.start(), p.forever(p.text_rep(p.round(p.temperature())), p.wait(1)))

def s11(p):
    p.script(*p.start())
    p.script(p.sh("when_joystick", fields={"STICK": ["up arrow", None]}), p.text("up"))
    p.script(p.sh("when_joystick", fields={"STICK": ["down arrow", None]}), p.text("down"))

def s12(p):
    first = p.define("flash", "color",
                     p.background(p.rep(p.arg("color"), COLOR)),
                     p.wait(0.5),
                     p.background(p.val(COLOR, "#000000")))
    p.blocks[first].update(topLevel=True, x=380, y=40)
    p.script(*p.start(), p.call("flash", "color", "#ff0000"), p.call("flash", "color", "#0000ff"))

def p01(p):
    # SenseHAT이 거꾸로 꽂혀 있어서 기울기 left/right가 반대
    p.script(*p.start())
    p.script(p.sh("when_tilted", fields={"TILT": ["right", None]}), p.letter("L"))
    p.script(p.sh("when_tilted", fields={"TILT": ["left", None]}), p.letter("R"))

def p03(p):
    p.script(*p.start())
    p.script(p.sh("when_moved"), p.sh("show_letter", {"LETTER": p.rep(p.random(1, 6))}))


EXAMPLES = {
    "s00_hello": s00, "s01_message": s01, "s02_variable": s02, "s03_colour": s03,
    "s04_pixel": s04, "s05_sequence": s05, "s06_for": s06, "s07_list": s07,
    "s08_temperature": s08, "s09_if": s09, "s10_while": s10, "s11_joystick": s11,
    "s12_function": s12, "p01_tilt": p01, "p03_dice": p03,
}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in EXAMPLES.items():
        p = Project()
        build(p)
        p.save(OUT / f"{name}.sb3")
        print("만듦:", (OUT / f"{name}.sb3").relative_to(ROOT), f"(블록 {len(p.blocks)}개)")
