# e01 · 무지개 채우기 — 이중 for와 리스트
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

# 줄마다 쓸 색 8개: 빨·주·노·초·파·남·보·흰
colors = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 0),
          (0, 0, 255), (75, 0, 130), (148, 0, 211), (255, 255, 255)]

for y in range(8):                         # 세로 줄 0~7 (바깥 반복)
    for x in range(8):                     # 가로 칸 0~7 (안쪽 반복)
        sense.set_pixel(x, y, colors[y])   # 줄마다 다른 색
        sleep(0.03)
