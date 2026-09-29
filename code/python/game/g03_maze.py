# g03 · 미로 탈출 — 동서남북으로 기울여 구슬을 초록 출구까지
# Argon 케이스에서는 오른쪽으로 기울이면 x가, 아래로 기울이면 y가 음수(-)입니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep, time     # 기다리기, 지금 시각(초) 도구
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

# 미로 지도: # 은 벽, . 은 길, G 는 출구 (한 줄이 LED 한 줄)
maze = [
    "...#....",
    "##.#.##.",
    "...#..#.",
    ".###.##.",
    "......#.",
    "####.##.",
    "...#....",
    ".#...##G",
]

a = sense.get_accelerometer_raw()   # 시작할 때 기울기를 "평평함"으로
x0 = a["x"]
y0 = a["y"]
px, py = 0, 0                    # 구슬은 왼쪽 위에서 출발
start = time()                   # 출발 시각 기억

while maze[py][px] != "G":       # 출구에 닿을 때까지 반복
    a = sense.get_accelerometer_raw()
    x = a["x"] - x0              # 좌우 기울기
    y = a["y"] - y0              # 앞뒤 기울기
    nx, ny = px, py              # 가려는 칸 (처음엔 제자리)
    if x < -0.2 and px < 7:      # 오른쪽(동)
        nx = px + 1
    elif x > 0.2 and px > 0:     # 왼쪽(서)
        nx = px - 1
    if y < -0.2 and py < 7:      # 아래(남)
        ny = py + 1
    elif y > 0.2 and py > 0:     # 위(북)
        ny = py - 1
    if maze[ny][nx] != "#":      # 벽이 아니면 대각선으로 한 번에
        px, py = nx, ny
    elif maze[py][nx] != "#":    # 대각선이 막혔으면 가로로만
        px = nx
    elif maze[ny][px] != "#":    # 아니면 세로로만
        py = ny

    for y in range(8):           # 미로 그리기
        for x in range(8):
            if maze[y][x] == "#":
                sense.set_pixel(x, y, (120, 60, 0))   # 벽은 갈색
            elif maze[y][x] == "G":
                sense.set_pixel(x, y, (0, 255, 0))    # 출구는 초록
            else:
                sense.set_pixel(x, y, (0, 0, 0))      # 길은 검정
    sense.set_pixel(px, py, (0, 200, 255))            # 구슬은 하늘색
    sleep(0.15)                  # 숫자를 줄이면 더 빨리 굴러감

sec = round(time() - start, 1)   # 걸린 시간(초), 소수 첫째 자리까지
print("탈출!", sec, "초")        # Thonny 셸 창에도 출력
sense.show_message(str(sec) + "s", text_colour=(0, 255, 0))
