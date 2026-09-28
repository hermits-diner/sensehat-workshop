# e01 · 무지개 채우기 — 이중 for와 리스트
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
          (0, 0, 255), (75, 0, 130), (148, 0, 211), (255, 255, 255)]

for y in range(8):
    for x in range(8):
        sense.set_pixel(x, y, colors[y])   # 줄마다 다른 색
        sleep(0.03)
