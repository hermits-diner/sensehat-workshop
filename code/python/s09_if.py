# s09 · 조건(if) — 만약 ~라면
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

t = sense.get_temperature()
if t > 30:                  # 30℃보다 높으면 (줄 끝에 : 꼭)
    sense.clear(255, 0, 0)  # 빨강
else:                       # 그렇지 않으면
    sense.clear(0, 0, 255)  # 파랑
