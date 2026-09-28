# e05 · 습도 알리미 — 습도에 따라 색 바꾸기
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    h = sense.get_humidity()
    if h > 60:
        color = (0, 0, 255)      # 습함: 파랑
    elif h < 30:
        color = (255, 128, 0)    # 건조: 주황
    else:
        color = (0, 255, 0)      # 알맞음: 초록
    sense.show_message(str(round(h)) + "%", text_colour=color)
    sleep(1)
