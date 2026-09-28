# e11 · 환경 기록기 — 온도·습도·기압을 CSV 파일로 저장 (엑셀로 열기)
from sense_hat import SenseHat
from time import sleep, strftime
sense = SenseHat()
sense.set_rotation(180)
sense.clear()

f = open("data.csv", "w")
f.write("time,temp,humidity,pressure\n")
for i in range(10):                      # 10번, 2초마다
    t = round(sense.get_temperature(), 1)
    h = round(sense.get_humidity(), 1)
    p = round(sense.get_pressure(), 1)
    f.write(strftime("%H:%M:%S") + "," + str(t) + "," + str(h) + "," + str(p) + "\n")
    print(i + 1, t, h, p)
    sense.set_pixel(i % 8, 0, (0, 255, 0))   # 기록할 때마다 점 하나
    sleep(2)
f.close()
sense.show_message("Saved")
