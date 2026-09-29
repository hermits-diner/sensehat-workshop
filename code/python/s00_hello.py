# s00 · 첫 코드 — Hello
from sense_hat import SenseHat   # SenseHAT 도구 상자 가져오기
sense = SenseHat()               # 내 SenseHAT을 sense라고 부르기
sense.set_rotation(180)          # 화면 180도 돌리기 (케이스에 거꾸로 꽂힘)
sense.clear()                    # 화면 지우기 (켜진 LED 끄기)
sense.show_message("Hello")      # 글자를 오른쪽→왼쪽으로 흘려 보여 주기
