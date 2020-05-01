import sys
import zmq
from gpiozero import Motor

motor_1 = Motor(forward=26, backward=19)
motor_2 = Motor(forward=13, backward=20)


port = "5555"

context = zmq.Context()
socket = context.socket(zmq.SUB)

#socket.connect("tcp://linuxbook.local:%s" % port)
socket.connect("tcp://apple.local:%s" % port)

SPEED = 0.4

topicfilter = 'rover1'
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)
socket.RCVTIMEO = 50

while True:
    try:
        string = socket.recv_string()
        print(string)
    except:
        motor_1.stop()
        motor_2.stop()
        continue

    topic, m1, m2 = string.split(',')

    if int(m1)>0:
        motor_1.forward(SPEED)
    else:
        motor_1.backward(SPEED)

    if int(m2)>0:
        motor_2.forward(SPEED)
    else:
        motor_2.backward(SPEED)


