from gpiozero import Motor
from time import sleep

motor = Motor(forward=4, backward=14)

for i in range(2):
    motor.forward()
    sleep(5)
    motor.backward()
    sleep(5)

motor.stop()

