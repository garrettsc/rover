from gpiozero import Motor
from time import sleep
import zmq
motor_1 = Motor(forward=26, backward=19)
motor_2 = Motor(forward=13, backward=20)




for i in range(2):
    motor_1.forward()
    motor_2.forward()
    sleep(5)
    motor_1.backward()
    motor_2.backward()
    sleep(5)

motor_1.stop()
motor_1.stop()

