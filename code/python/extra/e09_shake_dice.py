# e09 · 흔들면 주사위 — 가속도 크기로 흔들림 알아내기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import randint       # 무작위 수 도구 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

sense.show_letter("?")           # 흔들기를 기다리는 중
while True:
    a = sense.get_accelerometer_raw()   # x·y·z 세 방향의 힘 (가만히 두면 1 이하)
    # abs()는 부호(-)를 없앤 크기. 어느 방향이든 1.5보다 크면 흔든 것
    if abs(a["x"]) > 1.5 or abs(a["y"]) > 1.5 or abs(a["z"]) > 1.5:
        sense.show_letter(str(randint(1, 6)), text_colour=(255, 255, 0))
        sleep(1)                 # 한 번 흔들 때 한 번만
