# e04 · 카운트다운 — range를 거꾸로 세기
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

for n in range(5, 0, -1):      # 5, 4, 3, 2, 1
    sense.show_letter(str(n), text_colour=(255, 255, 0))
    sleep(1)
sense.show_message("GO!", text_colour=(0, 255, 0))
