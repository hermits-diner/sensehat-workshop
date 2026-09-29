# e08 · 구슬 굴리기 — 기울이는 쪽으로 구슬이 굴러감
# Argon 케이스에서는 오른쪽으로 기울이면 x가 음수(-)입니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

pos = 3                          # 구슬의 가로 위치 (0~7)
while True:
    x = sense.get_accelerometer_raw()["x"]   # 좌우 기울기
    if x < -0.2 and pos < 7:     # 오른쪽으로 기울였고, 끝이 아니면
        pos = pos + 1            # 오른쪽으로
    elif x > 0.2 and pos > 0:    # 왼쪽으로 기울였고, 끝이 아니면
        pos = pos - 1            # 왼쪽으로
    sense.clear()
    sense.set_pixel(pos, 7, (0, 200, 255))   # 맨 아랫줄(y=7)에 구슬
    sleep(0.1)                   # 숫자를 줄이면 더 빨리 굴러감
