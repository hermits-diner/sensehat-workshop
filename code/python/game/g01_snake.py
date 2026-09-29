# g01 · 뱀 게임 — 조이스틱으로 뱀을 움직여 빨간 사과 먹기
# Argon 케이스에서는 조이스틱 방향이 반대로 읽혀서, 움직일 방향을 반대로 적어 둡니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import randint       # 무작위 정수 도구 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

# 조이스틱이 알려 준 방향 → 실제로 움직일 칸 (x 변화, y 변화)
move = {"up": (0, 1), "down": (0, -1), "left": (1, 0), "right": (-1, 0)}

snake = [(3, 4), (2, 4)]         # 뱀 몸통 좌표 목록 (맨 앞이 머리)
dx, dy = 1, 0                    # 처음에는 오른쪽으로 감
apple = (6, 2)                   # 사과 위치

while True:
    for e in sense.stick.get_events():         # 그동안 누른 조이스틱 기록
        if e.action == "pressed" and e.direction in move:
            ndx, ndy = move[e.direction]
            if (ndx, ndy) != (-dx, -dy):       # 정반대로는 못 돌기
                dx, dy = ndx, ndy
    x, y = snake[0]                            # 지금 머리 위치
    head = ((x + dx) % 8, (y + dy) % 8)        # 새 머리 (벽을 넘으면 반대편으로)
    if head in snake:                          # 내 몸에 부딪히면
        break                                  # 게임 끝
    snake.insert(0, head)                      # 앞에 머리 붙이기
    if head == apple:                          # 사과를 먹었으면 꼬리를 그대로 둬서 길어짐
        while apple in snake:                  # 뱀과 겹치지 않는 곳에 새 사과
            apple = (randint(0, 7), randint(0, 7))
    else:
        snake.pop()                            # 안 먹었으면 꼬리 한 칸 떼기

    sense.clear()
    for x, y in snake:
        sense.set_pixel(x, y, (0, 255, 0))     # 뱀은 초록
    sense.set_pixel(apple[0], apple[1], (255, 0, 0))   # 사과는 빨강
    sleep(0.3)                                 # 숫자를 줄이면 뱀이 빨라짐

score = len(snake) - 2                         # 먹은 사과 수
print("점수:", score)                          # Thonny 셸 창에도 출력
sense.show_message("Score " + str(score), text_colour=(255, 255, 0))
