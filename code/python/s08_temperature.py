# s08 · 센서 읽기 — 온도
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

t = sense.get_temperature()         # 온도(℃)를 읽어 t에 담기
sense.show_message(str(round(t)))   # 반올림 → 글자로 바꿔(str) 보여 주기
