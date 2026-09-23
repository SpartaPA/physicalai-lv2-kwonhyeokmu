#!/usr/bin/env python3
"""OpenCR P 제어 실행 + 시리얼 로그 캡처.

사용법: run.py <Kp> <speed_deg_s> <angle_deg> [캡처초]
예:     run.py 0.5 10 15 70
"""
import sys, time, serial

kp, speed, angle = sys.argv[1:4]
window = float(sys.argv[4]) if len(sys.argv) > 4 else 70.0
cmd = f"s {kp} {speed} {angle}\n".encode()

p = serial.Serial("/dev/ttyACM0", 115200, timeout=0.5)
time.sleep(2.0)                     # 포트를 열 때 보드가 리셋되면 부팅을 기다린다
banner = p.read_all().decode("utf8", "replace").strip()
if banner:
    print(banner, flush=True)
print(f"# {time.strftime('%Y-%m-%d %H:%M:%S %Z')}  >>> {cmd.decode().strip()}", flush=True)
p.write(cmd)
try:
    t0 = time.time()
    while time.time() - t0 < window:
        line = p.readline().decode("utf8", "replace").rstrip()
        if line:
            print(line, flush=True)
            if line.startswith(("STOP", "FAULT")):
                break
finally:
    p.write(b"x")                   # Ctrl+C로 끊어도 정지 명령은 반드시 나간다
    time.sleep(0.3)
    tail = p.read_all().decode("utf8", "replace").rstrip()
    if tail:
        print(tail, flush=True)
    p.close()
