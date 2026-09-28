# s06 · 반복(for) — 같은 일을 여러 번
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

for x in range(8):
    sense.set_pixel(x, 0, (255, 0, 0))
    sleep(0.2)
