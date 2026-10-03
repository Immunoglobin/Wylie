import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
pwm_pin=17
GPIO.setup(pwm_pin, GPIO.OUT)

pwm=GPIO.PWM(pwm_pin,50)
pwm.start(0)

try:
	while True:
		for duty_cycle in range(0,101,5):
			pwm.ChangeDutyCycle(duty_cycle)
			time.sleep(1)
		for duty_cycle in range(100, -1, -5):
			pwm.ChangeDutyCycle(duty_cycle)
			time.sleep(1)
except KeyboardInterrupt:
	pass

pwm.stop()
GPIO.cleanup()
