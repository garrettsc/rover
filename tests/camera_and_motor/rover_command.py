import sys
import zmq
from gpiozero import Motor

motor_1 = Motor(forward=26, backward=19)
motor_2 = Motor(forward=13, backward=20)


port = "5555"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)


socket.connect("tcp://apple.local:%s" % port)

topicfilter = "rover1"
socket.setsockopt_string(zmq.SUBSCRIBE, topicfilter)

while True:
    string = socket.recv_string()
    print(string)
    topic, m1, m2 = string.split(',')

    if int(m1)>0:
        motor_1.forward()
    else:
        motor_1.reverse()

    if int(m2)>0:
        motor_2.forward()
    else:
        motor_2.reverse()


