# s09 · 조건(if) — 만약 ~라면
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

t = sense.get_temperature()
if t > 30:
    sense.clear(255, 0, 0)
else:
    sense.clear(0, 0, 255)
