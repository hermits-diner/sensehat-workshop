# e08 · 구슬 굴리기 — 기울이는 쪽으로 구슬이 굴러감
# Argon 케이스에서는 오른쪽으로 기울이면 x가 음수(-)입니다.
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

pos = 3
while True:
    x = sense.get_accelerometer_raw()["x"]
    if x < -0.2 and pos < 7:
        pos = pos + 1            # 오른쪽으로
    elif x > 0.2 and pos > 0:
        pos = pos - 1            # 왼쪽으로
    sense.clear()
    sense.set_pixel(pos, 7, (0, 200, 255))
    sleep(0.1)
