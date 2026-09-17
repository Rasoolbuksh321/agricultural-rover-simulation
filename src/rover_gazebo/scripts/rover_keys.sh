#!/bin/bash

CMD_TOPIC="/cmd_vel"
PUB_PID=""

send_once() {
  LIN=$1
  ANG=$2
  gz topic -t $CMD_TOPIC -m gz.msgs.Twist -p "linear: {x: $LIN}, angular: {z: $ANG}" >/dev/null 2>&1
}

stop_current() {
  if [ ! -z "$PUB_PID" ]; then
    kill $PUB_PID 2>/dev/null
    wait $PUB_PID 2>/dev/null
    PUB_PID=""
  fi
}

publish_loop() {
  LIN=$1
  ANG=$2

  while true; do
    send_once $LIN $ANG
    sleep 0.05
  done
}

set_motion() {
  stop_current

  send_once $1 $2
  send_once $1 $2
  send_once $1 $2

  publish_loop $1 $2 &
  PUB_PID=$!
}

strong_stop() {
  stop_current

  for i in {1..80}; do
    send_once 0.0 0.0
    sleep 0.005
  done
}

clear
echo "Wave Rover Stable Keyboard Control"
echo "----------------------------------"
echo "w + Enter = forward"
echo "s + Enter = backward"
echo "a + Enter = left turn"
echo "d + Enter = right turn"
echo "x + Enter = stop"
echo "q + Enter = quit"
echo ""

while true; do
  read -r -p "Command w/s/a/d/x/q: " key

  case "$key" in
    w)
  echo "Forward fast"
  set_motion 0.90 0.0
  ;;
s)
  echo "Backward fast"
  set_motion -0.90 0.0
  ;;
a)
  echo "Left turn fast"
  set_motion 0.45 1.10
  ;;
d)
  echo "Right turn fast"
  set_motion 0.45 -1.10
  ;;
    x)
      echo "STOP"
      strong_stop
      ;;
    q)
      echo "Quit"
      strong_stop
      exit 0
      ;;
    *)
      echo "Only type: w, s, a, d, x, or q"
      ;;
  esac
done
