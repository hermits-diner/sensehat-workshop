# e10 · 반응 속도 게임 — 초록불이 켜지면 조이스틱을 빨리 누르기
from sense_hat import SenseHat
from random import uniform
from time import sleep, time
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

sense.show_message("Ready", text_colour=(255, 255, 0))
sleep(uniform(1, 4))                     # 1~4초 중 아무 때나
sense.clear(0, 255, 0)
start = time()
sense.stick.get_events()                 # 미리 눌린 기록 지우기
while True:
    e = sense.stick.wait_for_event()
    if e.action == "pressed":
        break
ms = round((time() - start) * 1000)
sense.clear()
print(ms, "ms")
sense.show_message(str(ms) + "ms")
