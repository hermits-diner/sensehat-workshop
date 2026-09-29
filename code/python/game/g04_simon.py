# g04 · 순서 기억 게임 — 켜진 순서대로 조이스틱을 밀기, 한 판마다 하나씩 늘어남
# Argon 케이스에서는 조이스틱 방향이 반대로 읽혀서, 읽은 방향을 뒤집어 씁니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import choice        # 목록에서 아무거나 고르는 도구
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

flip = {"up": "down", "down": "up", "left": "right", "right": "left"}   # 거꾸로 읽힘 바로잡기
colour = {"up": (255, 0, 0), "down": (0, 255, 0), "left": (0, 0, 255), "right": (255, 255, 0)}
spot = {                         # 방향마다 켤 네 칸
    "up":    [(3, 0), (4, 0), (3, 1), (4, 1)],
    "down":  [(3, 6), (4, 6), (3, 7), (4, 7)],
    "left":  [(0, 3), (1, 3), (0, 4), (1, 4)],
    "right": [(6, 3), (7, 3), (6, 4), (7, 4)],
}

def show(d, t):                  # 방향 d 자리를 t초 동안 켜기
    for x, y in spot[d]:
        sense.set_pixel(x, y, colour[d])
    sleep(t)
    sense.clear()

order = []                       # 기억해야 할 순서
ok = True                        # 지금까지 다 맞혔는지
while ok:
    order.append(choice(["up", "down", "left", "right"]))   # 하나 늘리기
    sleep(0.8)
    for d in order:              # 순서 보여 주기
        show(d, 0.5)
        sleep(0.2)

    sense.stick.get_events()     # 보는 동안 눌린 기록 지우기
    for d in order:              # 같은 순서로 밀었는지 하나씩 확인
        e = sense.stick.wait_for_event()
        while e.action != "pressed" or e.direction not in flip:
            e = sense.stick.wait_for_event()   # 누른 것이 아니면 다시 기다리기
        pushed = flip[e.direction]             # 실제로 민 방향
        show(pushed, 0.2)
        if pushed != d:          # 틀리면
            ok = False
            break

score = len(order) - 1           # 다 맞힌 판 수
sense.clear(255, 0, 0)           # 틀렸다! 빨간 화면
sleep(0.5)
print("점수:", score)            # Thonny 셸 창에도 출력
sense.show_message("Score " + str(score), text_colour=(255, 255, 0))
