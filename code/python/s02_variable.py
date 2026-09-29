# s02 · 변수 — 이름표 붙인 상자
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

name = "Kim"               # name 상자에 "Kim" 담기
sense.show_message(name)   # 상자 속 글자 보여 주기 (따옴표 없음!)
