# s05 · 순서와 기다리기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

sense.show_letter("A")     # 글자 한 개 보여 주기
sleep(1)                   # 1초 기다리기
sense.show_letter("B")
sleep(1)
sense.clear()              # 화면 끄기
