# s10 · 무한 반복(while) — 계속 재기
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    t = sense.get_temperature()
    sense.show_message(str(round(t)))
    sleep(1)
