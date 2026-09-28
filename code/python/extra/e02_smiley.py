# e02 · 웃는 얼굴 — set_pixels로 64칸을 한 번에 그리기
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

Y = (255, 200, 0)   # 노랑
O = (0, 0, 0)       # 꺼짐

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
sense.set_pixels(face)
