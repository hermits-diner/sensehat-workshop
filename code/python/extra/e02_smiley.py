# e02 · 웃는 얼굴 — set_pixels로 64칸을 한 번에 그리기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

Y = (255, 200, 0)   # 노랑
O = (0, 0, 0)       # 꺼짐

# 64칸 목록: 한 줄에 8칸씩, 위에서 아래로 8줄 (모양이 그대로 보임)
face = [
    O, O, Y, Y, Y, Y, O, O,
    O, Y, Y, Y, Y, Y, Y, O,
    Y, Y, O, Y, Y, O, Y, Y,
    Y, Y, Y, Y, Y, Y, Y, Y,
    Y, O, Y, Y, Y, Y, O, Y,
    Y, Y, O, O, O, O, Y, Y,
    O, Y, Y, Y, Y, Y, Y, O,
    O, O, Y, Y, Y, Y, O, O,
]
sense.set_pixels(face)   # 64칸을 한 번에 그리기
