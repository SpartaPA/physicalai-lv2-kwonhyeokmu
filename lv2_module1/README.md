# 모듈 1 — 원격 환경 구성과 모터 응답 확인

## 장비

| 구분 | 내용 |
|---|---|
| SBC | 라즈베리파이 (호스트명 `pa21`), Ubuntu Server 22.04.5 LTS, `aarch64` |
| 제어기 | OpenCR 1.0 (STM32F746) |
| 모터 | DYNAMIXEL XM430-W350 (모델 1020) 1개, ID 12, Protocol 2.0, TTL 1 Mbps |
| 연결 | OpenCR ↔ 라즈베리파이 USB (`/dev/ttyACM0`, 115200 bps) |
| PC | VS Code Remote-SSH 접속 전용 |

## 환경

라즈베리파이 사용자가 `dialout` 그룹에 속해 있어야 `/dev/ttyACM0`을 열 수 있다.

```bash
id | grep dialout
ls -l /dev/ttyACM*
lsusb | grep 0483        # 0483:5740 STMicroelectronics Virtual COM Port
```

필요한 파이썬 패키지는 `pyserial` 하나다.

```bash
python3 -c "import serial; print(serial.__version__)"
```

## 펌웨어

`examples/opencr_position_p/opencr_position_p.ino`를 라즈베리파이에서
`arm-none-eabi-gcc` 10.3.1로 빌드하고, 같은 곳에서 ARM용으로 빌드한
`opencr_ld`로 업로드했다.

| 항목 | 값 |
|---|---|
| 바이너리 | `opencr_position_p.ino.bin`, 104,844 바이트 |
| SHA-256 | `6a3629a8070a5d1f55dce837cc90f073db4444b83da5c722133446608a8151e3` |

업로드 결과는 `results/upload.log`에 있으며 `CRC OK 9B55F6 9B55F6`으로
성공을 확인했다.

## 실행 방법

펌웨어의 시리얼 명령은 다음과 같다. 줄바꿈으로 구분한다.

| 입력 | 동작 |
|---|---|
| `k <Kp>` / `v <speed_deg_s>` / `a <angle_deg>` | 값 하나만 설정 |
| `s <Kp> <speed_deg_s\|max> <angle_deg>` | 설정 후 즉시 실행 |
| `s` | 현재 설정으로 실행 |
| `x` | 즉시 정지 (줄바꿈 불필요) |

목표각은 절대 각도가 아니라 **실행 시작 위치 기준 상대각**이며 −90°~+90°
범위다. 실행 후 2초 동안은 목표가 0°이고, `t = 2.0 s`에 입력한 목표각으로
바뀐다. 실행은 최소 60초 뒤 자동 정지한다.

실행과 로그 저장은 `run.py`로 한다.

```bash
# 사용법: run.py <Kp> <speed_deg_s> <angle_deg> [캡처초]
python3 lv2_module1/run.py 2.0 10 10 70 | tee lv2_module1/results/실행A.log
```

`run.py`는 명령을 보낸 뒤 시리얼 출력을 그대로 표준출력으로 흘리며, `tee`가
화면과 파일에 동시에 남긴다. 중간에 멈추려면 `Ctrl+C`를 누른다. 스크립트는
`finally` 블록에서 반드시 정지 명령 `x`를 보내므로, 강제 종료해도 모터가
계속 돌지 않는다.

**안전:** 실행 전 모터를 고정하고 이동 범위에 장애물이 없는지 확인한다.
정지 수단은 `Ctrl+C`(→ `x` 전송), 그래도 멈추지 않으면 전원 차단이다.

## 결과 파일

| 경로 | 내용 |
|---|---|
| [report.md](report.md) | 문제별 설정·증거·해석 |
| [results/환경확인.txt](results/환경확인.txt) | 호스트명, OS, 아키텍처, 포트, 권한 |
| [results/upload.log](results/upload.log) | 업로드 기록 |
| [results/실행A.log](results/실행A.log) | 실행 A 전체 604행 |
| [results/실행B.log](results/실행B.log) | 실행 B 전체 604행 (Kp 0.5) |
| [run.py](run.py) | 실행·로그 캡처 스크립트 |
