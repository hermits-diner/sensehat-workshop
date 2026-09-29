# e12 · 색 이름 맞히기 — 컬러 센서 (SenseHAT V2 전용)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

sense.colour.gain = 64                   # 컬러 센서 감도 최대로 (1, 4, 16, 64 중)
while True:
    r, g, b, c = sense.colour.colour     # 센서가 본 빨강·초록·파랑·밝기
    if r > g and r > b:                  # 빨강이 가장 크면
        sense.show_letter("R", text_colour=(255, 0, 0))
    elif g > r and g > b:                # 초록이 가장 크면
        sense.show_letter("G", text_colour=(0, 255, 0))
    else:                                # 나머지는 파랑으로
        sense.show_letter("B", text_colour=(0, 0, 255))
    print(r, g, b)                       # 셸 창에서 실제 값 확인
    sleep(0.5)
