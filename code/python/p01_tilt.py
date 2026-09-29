# p01 · 기울이면 화살표 (움직임 센서)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

while True:
    x = sense.get_accelerometer_raw()["x"]   # 좌우 기울기 (-1 ~ 1)
    if x < -0.3:                 # 오른쪽으로 기울이면 (케이스 때문에 음수)
        sense.show_letter("R")
    elif x > 0.3:                # 왼쪽으로 기울이면
        sense.show_letter("L")
    else:                        # 거의 평평하면
        sense.clear()
