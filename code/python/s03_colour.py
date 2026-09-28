# s03 · 색 — 빨강·초록·파랑 섞기
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.show_message("Hi", text_colour=(255, 0, 0))
