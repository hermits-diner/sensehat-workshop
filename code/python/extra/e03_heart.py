# e03 · 두근두근 하트 — 그림 두 개를 번갈아 보여 주기
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

R = (255, 0, 60)
O = (0, 0, 0)

big = [
    O, R, R, O, O, R, R, O,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    R, R, R, R, R, R, R, R,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, O, R, R, O, O, O,
    O, O, O, O, O, O, O, O,
]
small = [
    O, O, O, O, O, O, O, O,
    O, O, R, O, O, R, O, O,
    O, R, R, R, R, R, R, O,
    O, R, R, R, R, R, R, O,
    O, O, R, R, R, R, O, O,
    O, O, O, R, R, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
]

for i in range(5):
    sense.set_pixels(big)
    sleep(0.4)
    sense.set_pixels(small)
    sleep(0.4)
sense.clear()
