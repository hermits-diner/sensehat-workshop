# p02 · 카멜레온 (컬러 센서, SenseHAT V2 전용)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)
sense.colour.gain = 64           # 컬러 센서 감도 최대로 (1, 4, 16, 64 중)

while True:
    r, g, b, c = sense.colour.colour   # 센서가 본 빨강·초록·파랑·밝기
    sense.clear(r, g, b)               # 그 색으로 화면 채우기
