# e07 · 조이스틱으로 점 옮기기 — 변수로 위치 기억하기
# Argon 케이스에서는 SenseHAT이 거꾸로 꽂혀 조이스틱 방향이 반대로 읽힙니다.
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

x, y = 3, 3
sense.set_pixel(x, y, (0, 255, 0))

while True:
    e = sense.stick.wait_for_event()
    if e.action != "pressed":
        continue
    if e.direction == "down" and y > 0:      # 위로 밀기 (거꾸로 읽힘)
        y = y - 1
    elif e.direction == "up" and y < 7:      # 아래로 밀기
        y = y + 1
    elif e.direction == "right" and x > 0:   # 왼쪽으로 밀기
        x = x - 1
    elif e.direction == "left" and x < 7:    # 오른쪽으로 밀기
        x = x + 1
    sense.clear()
    sense.set_pixel(x, y, (0, 255, 0))
