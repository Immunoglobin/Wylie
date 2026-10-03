from gpiozero import AngularServo
from time import sleep

# Initialize servo on GPIO 17
servo = AngularServo(17, min_pulse_width=0.0006, max_pulse_width=0.0025)

while True:
    servo.angle = 90
    sleep(5)
    servo.angle = 0
    sleep(5)
    servo.angle = -90
    sleep(5)

