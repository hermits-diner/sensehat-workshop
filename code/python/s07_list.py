# s07 · 리스트 — 여러 개를 한 줄로
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
for c in colors:
    sense.clear(c)
    sleep(1)
