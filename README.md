# 라즈베리파이와 SenseHAT으로 배우는 피지컬 컴퓨팅

초·중·고 교사 연수 자료입니다. (3차시 · 50분 × 3 = 150분)

- 강사: 오정훈 (부산동고등학교)
- 장비: Raspberry Pi 4B (8GB) + Argon One V2 케이스 + Sense HAT (V2)
- OS: Raspberry Pi OS Full (64-bit), 2026-09-15 (Debian 13 Trixie)
- 코드: **Python**과 **Scratch 3**를 나란히 비교

## 바로 보기

- **발표 슬라이드**: https://hermits-diner.github.io/sensehat-workshop/slides/
- 첫 화면 (슬라이드 · 교재 PDF · 예제 코드 모음): https://hermits-diner.github.io/sensehat-workshop/

## 무엇이 있나요

| 폴더 | 내용 |
|---|---|
| [`pdf/`](pdf/) | **교사용 교재** `연수교재.pdf` (A4 가로, Python·Scratch 비교), `슬라이드원고.pdf` |
| [`slides/`](slides/) | **발표 슬라이드** `index.html` (48장, 인터넷 없이 열림) |
| [`code/python/`](code/python/) | Python 예제 16개 (s00~s12 기초, p01~p03 프로젝트) |
| [`code/scratch/`](code/scratch/) | Scratch 3 예제 15개 (`.sb3`) |
| [`docs/`](docs/) | 교재 원고 (Markdown)와 캡처 그림 |
| [`tools/`](tools/) | 원고에서 코드·PDF·슬라이드를 만드는 스크립트 |

## 차시 구성

| 차시 | 주제 | 내용 |
|---|---|---|
| 1차시 | 시작하기 | OS 설치(Imager 2.0), 한글 설정, 라즈베리파이·SenseHAT 소개, 첫 코드 |
| 2차시 | 파이썬 기초 12단계 | 한 단계에 새 개념 1개: 명령 → 변수 → 색 → 좌표 → 순서 → for → 리스트 → 센서 → if → while → 조이스틱 → 함수 |
| 3차시 | 미니 프로젝트 | 기울이면 화살표 · 카멜레온(컬러 센서) · 전자 주사위, 학교급별 수업 적용 |

## 사용법

**슬라이드**: 웹에서 [바로 보기](https://hermits-diner.github.io/sensehat-workshop/slides/)로 열거나, 인터넷이 없을 때는 `slides` 폴더를 통째로 받아서 `index.html`을 브라우저로 엽니다.

| 키 | 동작 |
|---|---|
| → / Space | 다음 |
| ← | 이전 |
| F | 전체 화면 |
| N | 강사 메모 |

**예제 코드**: 라즈베리파이에서 Thonny로 `.py`를 열거나, Scratch 3에서 `.sb3`를 불러옵니다.

> Argon One V2 케이스에서는 SenseHAT이 거꾸로 꽂히므로, 모든 코드가 `sense.set_rotation(180)`으로 시작합니다.

## 자료 다시 만들기

원고(`docs/*.md`)를 고친 뒤 라즈베리파이에서 실행합니다.

```bash
python3 tools/make_code.py      # Python 예제
python3 tools/make_sb3.py       # Scratch 예제
python3 tools/build_pdf.py      # PDF (chromium 필요)
python3 tools/build_slides.py   # 슬라이드
```

## 출처

- `docs/images/web_*.png`(`slides/images/`에도 같은 파일)는 라즈베리파이 웹사이트를 캡처한 것입니다.
  - [raspberrypi.com](https://www.raspberrypi.com), [raspberrypi.org/teach](https://www.raspberrypi.org/teach/)
  - 저작권은 Raspberry Pi Ltd · Raspberry Pi Foundation에 있습니다.
- 가격 정보: 라즈베리파이 공식 발표 (2019.6, 2020.5, 2025.12, 2026.2, 2026.4)
- 슬라이드는 [scratchblocks](https://github.com/scratchblocks/scratchblocks)와 [qrcodejs](https://github.com/davidshimjs/qrcodejs)를 사용합니다.

> 교재 속 Wi‑Fi와 계정 비밀번호는 연수용입니다. 학교에서 쓸 때는 바꾸세요.
