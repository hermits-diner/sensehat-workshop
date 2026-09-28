# e09 · 흔들면 주사위 — 가속도 크기로 흔들림 알아내기
from sense_hat import SenseHat
from random import randint
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.show_letter("?")
while True:
    a = sense.get_accelerometer_raw()
    if abs(a["x"]) > 1.5 or abs(a["y"]) > 1.5 or abs(a["z"]) > 1.5:
        sense.show_letter(str(randint(1, 6)), text_colour=(255, 255, 0))
        sleep(1)                 # 한 번 흔들 때 한 번만
