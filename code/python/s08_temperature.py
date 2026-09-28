# s08 · 센서 읽기 — 온도
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

t = sense.get_temperature()
sense.show_message(str(round(t)))
