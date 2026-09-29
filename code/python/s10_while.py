# s10 · 무한 반복(while) — 계속 재기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:                             # 멈출 때까지 계속 반복 (정지: ■ 버튼)
    t = sense.get_temperature()
    sense.show_message(str(round(t)))
    sleep(1)                            # 1초 쉬고 다시 재기
