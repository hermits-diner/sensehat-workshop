# s04 · 좌표 — 점 하나 켜기
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.set_pixel(0, 0, (0, 255, 0))
