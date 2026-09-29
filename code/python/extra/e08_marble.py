# e08 · 구슬 굴리기 — 기울이는 쪽(동서남북)으로 구슬이 굴러감
# Argon 케이스에서는 오른쪽으로 기울이면 x가, 아래로 기울이면 y가 음수(-)입니다.
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

a = sense.get_accelerometer_raw()   # 시작할 때의 기울기를 재서
x0 = a["x"]                      # "평평함"의 기준으로 삼기
y0 = a["y"]                      # (책상이 조금 기울어 있어도 괜찮음)

px = 3                           # 구슬의 가로 위치 (0~7)
py = 3                           # 구슬의 세로 위치 (0~7)
while True:
    a = sense.get_accelerometer_raw()
    x = a["x"] - x0              # 좌우 기울기
    y = a["y"] - y0              # 앞뒤 기울기
    if x < -0.2 and px < 7:      # 오른쪽(동)으로 기울였고, 끝이 아니면
        px = px + 1              # 오른쪽으로
    elif x > 0.2 and px > 0:     # 왼쪽(서)으로 기울였고, 끝이 아니면
        px = px - 1              # 왼쪽으로
    if y < -0.2 and py < 7:      # 아래(남)로 기울였고, 끝이 아니면
        py = py + 1              # 아래로
    elif y > 0.2 and py > 0:     # 위(북)로 기울였고, 끝이 아니면
        py = py - 1              # 위로
    sense.clear()
    sense.set_pixel(px, py, (0, 200, 255))   # 구슬 그리기
    sleep(0.1)                   # 숫자를 줄이면 더 빨리 굴러감
