# s05 · 순서와 기다리기
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.show_letter("A")
sleep(1)
sense.show_letter("B")
sleep(1)
sense.clear()
