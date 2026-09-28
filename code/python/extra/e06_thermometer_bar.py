# e06 · 막대 온도계 — 온도를 막대 높이로 (20℃~40℃)
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    t = sense.get_temperature()
    height = int((t - 20) / 20 * 8)     # 20℃ → 0칸, 40℃ → 8칸
    height = max(0, min(8, height))     # 0~8 사이로 자르기
    sense.clear()
    for y in range(8 - height, 8):      # 아래부터 채우기
        for x in range(3, 5):
            sense.set_pixel(x, y, (255, 60, 0))
    print(round(t, 1), "℃")
    sleep(1)
