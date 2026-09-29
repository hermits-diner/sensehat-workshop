# p03 · 전자 주사위 (조이스틱 + 무작위)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import randint       # 무작위 수 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:
    e = sense.stick.wait_for_event()            # 조이스틱을 기다리기
    if e.action == "pressed":                   # 누르면
        sense.show_letter(str(randint(1, 6)))   # 1~6 중 아무 수 보여 주기
