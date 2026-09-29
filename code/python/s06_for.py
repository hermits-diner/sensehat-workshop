# s06 · 반복(for) — 같은 일을 여러 번
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

for x in range(8):                       # x = 0, 1, 2, … 7 차례로
    sense.set_pixel(x, 0, (255, 0, 0))   # 맨 윗줄 x번째 칸 켜기 (들여쓰기 4칸)
    sleep(0.2)
