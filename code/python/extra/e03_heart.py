# e03 · 두근두근 하트 — 그림 두 개를 번갈아 보여 주기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

R = (255, 0, 60)    # 빨강
O = (0, 0, 0)       # 꺼짐

big = [             # 큰 하트
    O, R, R, O, O, R, R, O,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, O, R, R, O, O, O,
    O, O, O, O, O, O, O, O,
]
small = [           # 작은 하트
    O, O, O, O, O, O, O, O,
    O, O, R, O, O, R, O, O,
    O, R, R, R, R, R, R, O,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, O, R, R, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
]

for i in range(5):           # 5번 두근두근
    sense.set_pixels(big)    # 크게
    sleep(0.4)
    sense.set_pixels(small)  # 작게
    sleep(0.4)
sense.clear()
