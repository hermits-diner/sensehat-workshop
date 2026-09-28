# p01 · 기울이면 화살표 (움직임 센서)
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

while True:
    x = sense.get_accelerometer_raw()["x"]
    if x < -0.3:
        sense.show_letter("R")
    elif x > 0.3:
        sense.show_letter("L")
    else:
        sense.clear()
