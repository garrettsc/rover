#!/bin/bash


source ~/py3_env/bin/activate
python /home/pi/rover/src/rover/rover_camera_server.py &
python /home/pi/rover/src/rover/rover_command.py &
