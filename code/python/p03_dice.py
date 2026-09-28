# p03 · 전자 주사위 (조이스틱 + 무작위)
from sense_hat import SenseHat
from random import randint
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    e = sense.stick.wait_for_event()
    if e.action == "pressed":
        sense.show_letter(str(randint(1, 6)))
