# s04 · 좌표 — 점 하나 켜기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

# set_pixel(x, y, 색): x는 가로 0~7, y는 세로 0~7
sense.set_pixel(0, 0, (0, 255, 0))   # 왼쪽 위 첫 칸을 초록으로
