# e07 · 조이스틱으로 점 옮기기 — 변수로 위치 기억하기
# Argon 케이스에서는 SenseHAT이 거꾸로 꽂혀 조이스틱 방향이 반대로 읽힙니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

x, y = 3, 3                          # 점의 처음 위치 (가운데쯤)
sense.set_pixel(x, y, (0, 255, 0))

while True:
    e = sense.stick.wait_for_event()
    if e.action != "pressed":        # 누른 것이 아니면 (뗌·계속 누름)
        continue                     # 아래는 건너뛰고 다시 기다리기
    if e.direction == "down" and y > 0:      # 위로 밀기 (거꾸로 읽힘)
        y = y - 1
    elif e.direction == "up" and y < 7:      # 아래로 밀기
        y = y + 1
    elif e.direction == "right" and x > 0:   # 왼쪽으로 밀기
        x = x - 1
    elif e.direction == "left" and x < 7:    # 오른쪽으로 밀기
        x = x + 1
    sense.clear()                        # 지우고
    sense.set_pixel(x, y, (0, 255, 0))   # 새 위치에 다시 그리기
