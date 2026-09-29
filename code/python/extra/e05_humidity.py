# e05 · 습도 알리미 — 습도에 따라 색 바꾸기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:
    h = sense.get_humidity()     # 습도(%) 읽기
    if h > 60:
        color = (0, 0, 255)      # 습함: 파랑
    elif h < 30:
        color = (255, 128, 0)    # 건조: 주황
    else:
        color = (0, 255, 0)      # 알맞음: 초록
    # 숫자를 글자로 바꾸고 "%"를 + 로 이어 붙이기
    sense.show_message(str(round(h)) + "%", text_colour=color)
    sleep(1)
