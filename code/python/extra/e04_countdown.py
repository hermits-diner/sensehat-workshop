# e04 · 카운트다운 — range를 거꾸로 세기
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
from time import sleep           # 기다리기(sleep) 도구 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)

for n in range(5, 0, -1):      # range(시작, 끝, 간격): 5, 4, 3, 2, 1 (끝 0은 빠짐)
    # 숫자는 str()로 글자로 바꿔야 보여 줄 수 있음
    sense.show_letter(str(n), text_colour=(255, 255, 0))
    sleep(1)
sense.show_message("GO!", text_colour=(0, 255, 0))
