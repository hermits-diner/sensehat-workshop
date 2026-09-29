# s03 · 색 — 빨강·초록·파랑 섞기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

# text_colour=(빨강, 초록, 파랑) → 각각 0~255
sense.show_message("Hi", text_colour=(255, 0, 0))
