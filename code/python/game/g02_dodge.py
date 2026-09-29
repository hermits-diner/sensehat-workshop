# g02 · 돌 피하기 — 좌우로 기울여 떨어지는 돌을 피하기
# Argon 케이스에서는 오른쪽으로 기울이면 x가 음수(-)입니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from random import randint       # 무작위 정수 도구 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

x0 = sense.get_accelerometer_raw()["x"]   # 시작할 때 기울기를 "평평함"으로
px = 3                           # 내 위치 (맨 아랫줄, 0~7)
rocks = []                       # 돌 목록 [x, y]
score = 0                        # 피한 돌 수

while True:
    x = sense.get_accelerometer_raw()["x"] - x0   # 좌우 기울기
    if x < -0.2 and px < 7:      # 오른쪽으로 기울였으면
        px = px + 1
    elif x > 0.2 and px > 0:     # 왼쪽으로 기울였으면
        px = px - 1

    new = []                     # 한 칸씩 떨어진 돌들을 담을 새 목록
    for r in rocks:
        if r[1] < 7:             # 아직 바닥이 아니면 한 칸 아래로
            new.append([r[0], r[1] + 1])
        else:                    # 바닥을 지나갔으면 피한 것!
            score = score + 1
    rocks = new
    if randint(1, 3) == 1:       # 세 번에 한 번꼴로 새 돌
        rocks.append([randint(0, 7), 0])

    if [px, 7] in rocks:         # 돌에 맞으면
        break                    # 게임 끝

    sense.clear()
    for r in rocks:
        sense.set_pixel(r[0], r[1], (255, 80, 0))   # 돌은 주황
    sense.set_pixel(px, 7, (0, 200, 255))           # 나는 하늘색
    sleep(max(0.08, 0.25 - score * 0.005))          # 점수가 오를수록 빨라짐

sense.clear(255, 0, 0)           # 쾅! 빨간 화면
sleep(0.5)
print("점수:", score)            # Thonny 셸 창에도 출력
sense.show_message("Score " + str(score), text_colour=(255, 255, 0))
