# s11 · 조이스틱 — 누르면 반응
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    e = sense.stick.wait_for_event()
    if e.action == "pressed":
        sense.show_message(e.direction)
