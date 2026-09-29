# s11 · 조이스틱 — 누르면 반응
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:
    e = sense.stick.wait_for_event()      # 조이스틱을 움직일 때까지 기다리기
    if e.action == "pressed":             # 눌렀을 때만 (뗄 때는 무시)
        sense.show_message(e.direction)   # 누른 방향(up/down/left/right) 보여 주기
