# e11 · 환경 기록기 — 온도·습도·기압을 CSV 파일로 저장 (엑셀로 열기)
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep, strftime  # 기다리기, 시각을 글자로 만들기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

f = open("data.csv", "w")                # 파일 열기 ("w" = 새로 쓰기, 이 코드와 같은 폴더)
f.write("time,temp,humidity,pressure\n") # 첫 줄: 제목 (\n = 줄 바꿈)
for i in range(10):                      # 10번, 2초마다
    t = round(sense.get_temperature(), 1)   # 온도(℃), 소수 첫째 자리까지
    h = round(sense.get_humidity(), 1)      # 습도(%)
    p = round(sense.get_pressure(), 1)      # 기압(hPa)
    # 한 줄 = 시각,온도,습도,기압 (쉼표로 구분 → 엑셀에서 칸이 나뉨)
    f.write(strftime("%H:%M:%S") + "," + str(t) + "," + str(h) + "," + str(p) + "\n")
    print(i + 1, t, h, p)                # 셸 창에서 확인
    sense.set_pixel(i % 8, 0, (0, 255, 0))   # 기록할 때마다 점 하나
    sleep(2)
f.close()                                # 파일 닫기 (꼭 해야 저장이 마무리됨)
sense.show_message("Saved")
