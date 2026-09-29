# e10 · 반응 속도 게임 — 초록불이 켜지면 조이스틱을 빨리 누르기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import uniform       # 무작위 소수 도구 가져오기
from time import sleep, time     # 기다리기, 지금 시각(초) 도구
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

sense.show_message("Ready", text_colour=(255, 255, 0))
sleep(uniform(1, 4))                     # 1~4초 중 아무 때나
sense.clear(0, 255, 0)                   # 초록불!
start = time()                           # 초록불 켜진 시각 기억
sense.stick.get_events()                 # 미리 눌린 기록 지우기
while True:
    e = sense.stick.wait_for_event()
    if e.action == "pressed":
        break                            # 누르면 반복 빠져나가기
ms = round((time() - start) * 1000)      # 걸린 시간(초) → 밀리초(ms)
sense.clear()
print(ms, "ms")                          # Thonny 셸 창에도 출력
sense.show_message(str(ms) + "ms")
