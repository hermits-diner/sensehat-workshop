# s07 · 리스트 — 여러 개를 한 줄로
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]   # 빨강, 노랑, 초록
for c in colors:     # 리스트에서 하나씩 꺼내 c에 담기
    sense.clear(c)   # 화면 전체를 c 색으로 채우기
    sleep(1)
