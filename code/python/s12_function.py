# s12 · 함수 만들기(def) — 나만의 명령
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

def flash(color):
    sense.clear(color)
    sleep(0.5)
    sense.clear()

flash((255, 0, 0))
flash((0, 0, 255))
