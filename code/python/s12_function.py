# s12 · 함수 만들기(def) — 나만의 명령
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

def flash(color):        # flash라는 새 명령 만들기 (color는 받을 값)
    sense.clear(color)   # 받은 색으로 켜고
    sleep(0.5)
    sense.clear()        # 끄기

flash((255, 0, 0))       # 새 명령 쓰기: 빨강 번쩍
flash((0, 0, 255))       # 파랑 번쩍
