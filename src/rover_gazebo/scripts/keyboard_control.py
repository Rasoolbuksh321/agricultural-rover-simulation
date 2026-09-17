#!/usr/bin/env python3

import os
import sys
import tty
import termios
import select
import subprocess

linear_speed = 0.3
angular_speed = 0.5

def publish_cmd(linear, angular):
    cmd = [
        "gz", "topic",
        "-t", "/cmd_vel",
        "-m", "gz.msgs.Twist",
        "-p", f"linear: {{x: {linear}}}, angular: {{z: {angular}}}"
    ]
    subprocess.run(cmd)

def get_key():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)

    print("""
Keyboard Control for Wave Rover
-------------------------------
W : move forward
S : move backward
A : turn left
D : turn right
X : stop
Q : quit
""")

    try:
        while True:
            key = get_key().lower()

            if key == 'w':
                publish_cmd(linear_speed, 0.0)
                print("Forward")

            elif key == 's':
                publish_cmd(-linear_speed, 0.0)
                print("Backward")

            elif key == 'a':
                publish_cmd(0.0, angular_speed)
                print("Left")

            elif key == 'd':
                publish_cmd(0.0, -angular_speed)
                print("Right")

            elif key == 'x':
                publish_cmd(0.0, 0.0)
                print("Stop")

            elif key == 'q':
                publish_cmd(0.0, 0.0)
                print("Quit")
                break

    except Exception as e:
        print(e)

    finally:
        publish_cmd(0.0, 0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
