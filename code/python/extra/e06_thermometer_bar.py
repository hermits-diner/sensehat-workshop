# e06 · 막대 온도계 — 온도를 막대 높이로 (20℃~40℃)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:
    t = sense.get_temperature()         # 온도 읽기
    height = int((t - 20) / 20 * 8)     # 20℃ → 0칸, 40℃ → 8칸
    height = max(0, min(8, height))     # 0~8 사이로 자르기
    sense.clear()
    for y in range(8 - height, 8):      # 아래부터 채우기
        for x in range(3, 5):           # 가운데 두 칸(x=3, 4) 굵기
            sense.set_pixel(x, y, (255, 60, 0))
    print(round(t, 1), "℃")            # Thonny 아래 셸 창에도 숫자 출력
    sleep(1)
