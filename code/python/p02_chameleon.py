# p02 · 카멜레온 (컬러 센서, SenseHAT V2 전용)
from sense_hat import SenseHat
sense = SenseHat()
sense.set_rotation(180)
sense.clear()
sense.colour.gain = 64

while True:
    r, g, b, c = sense.colour.colour
    sense.clear(r, g, b)
