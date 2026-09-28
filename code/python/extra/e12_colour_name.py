# e12 · 색 이름 맞히기 — 컬러 센서 (SenseHAT V2 전용)
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.colour.gain = 64
while True:
    r, g, b, c = sense.colour.colour
    if r > g and r > b:
        sense.show_letter("R", text_colour=(255, 0, 0))
    elif g > r and g > b:
        sense.show_letter("G", text_colour=(0, 255, 0))
    else:
        sense.show_letter("B", text_colour=(0, 0, 255))
    print(r, g, b)
    sleep(0.5)
