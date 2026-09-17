#!/usr/bin/env python3
import sys
import tty
import termios
import select
import subprocess
import time

LIN = 0.35
ANG = 0.8
RATE = 10  # Hz
TOPIC = "/cmd_vel"

help_msg = """
Smooth keyboard control for Wave Rover
--------------------------------------
Use this terminal window and press:

W = forward
S = backward
A = turn left
D = turn right
X or SPACE = stop
Q = quit

Important: after pressing W/A/S/D, the rover keeps moving until you press X or SPACE.
"""

def publish(linear, angular):
    msg = f"linear: {{x: {linear}}}, angular: {{z: {angular}}}"
    subprocess.run(
        ["gz", "topic", "-t", TOPIC, "-m", "gz.msgs.Twist", "-p", msg],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def get_key(timeout=0.05):
    r, _, _ = select.select([sys.stdin], [], [], timeout)
    if r:
        return sys.stdin.read(1).lower()
    return None

if __name__ == "__main__":
    old_settings = termios.tcgetattr(sys.stdin)
    linear = 0.0
    angular = 0.0
    print(help_msg)
    try:
        tty.setcbreak(sys.stdin.fileno())
        last_print = ""
        while True:
            key = get_key(1.0 / RATE)
            if key:
                if key == "w":
                    linear, angular = LIN, 0.0
                    status = "Forward"
                elif key == "s":
                    linear, angular = -LIN, 0.0
                    status = "Backward"
                elif key == "a":
                    linear, angular = 0.0, ANG
                    status = "Left"
                elif key == "d":
                    linear, angular = 0.0, -ANG
                    status = "Right"
                elif key == "x" or key == " ":
                    linear, angular = 0.0, 0.0
                    status = "Stop"
                elif key == "q":
                    for _ in range(10):
                        publish(0.0, 0.0)
                        time.sleep(0.05)
                    print("Quit")
                    break
                else:
                    status = last_print
                if key in ["w", "s", "a", "d", "x", " "] and status != last_print:
                    print(status)
                    last_print = status
            publish(linear, angular)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        for _ in range(10):
            publish(0.0, 0.0)
            time.sleep(0.05)
