import time
import RPi.GPIO as GPIO
import threading
import subprocess

# Define Globals
threads = []

# Configure GPIO pins
GPIO.setmode(GPIO.BCM)
pulse_pin=17
GPIO.setup(pulse_pin, GPIO.OUT)
direction_pin=5
GPIO.setup(direction_pin, GPIO.OUT)
enable_pin=6
GPIO.setup(enable_pin, GPIO.OUT)
estop_pin=12
GPIO.setup(estop_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Upper Bounds 0.001
step_time=0.005
bouncetime=200

def command_motor(delay,direction):
	target_time = delay*1000000 + time.clock_gettime_ns(time.CLOCK_MONOTONIC)
	GPIO.output(enable_pin, GPIO.LOW)
	time.sleep(step_time)
	GPIO.output(direction_pin, direction)
	time.sleep(step_time)
	while time.clock_gettime_ns(time.CLOCK_MONOTONIC) < target_time:
		GPIO.output(pulse_pin, GPIO.HIGH)
		time.sleep(step_time)
		GPIO.output(pulse_pin, GPIO.LOW)
		time.sleep(step_time)
	GPIO.output(enable_pin, GPIO.HIGH)

def step_motor(steps,direction):
	GPIO.output(enable_pin, GPIO.LOW)
	time.sleep(step_time)
	GPIO.output(direction_pin, direction)
	time.sleep(step_time)
	for i in range(steps):
		GPIO.output(pulse_pin, GPIO.HIGH)
		time.sleep(step_time)
		GPIO.output(pulse_pin, GPIO.LOW)
		time.sleep(step_time)
	GPIO.output(enable_pin, GPIO.HIGH)

def run_motor(delay,direction):
	t = threading.Thread(target=command_motor, args=(delay,direction,))
	threads.append(t)
	t.start()

def position_motor(steps,direction):
	t = threading.Thread(target=step_motor, args=(steps,direction,))
	threads.append(t)
	t.start()

def estop(self):
	GPIO.output(enable_pin, GPIO.HIGH)

GPIO.add_event_detect(
	estop_pin,
	GPIO.RISING,
	callback=estop,
	bouncetime=bouncetime
)

direction = GPIO.LOW
while True:
	#command_motor(2000)
	if direction == GPIO.HIGH:
		direction = GPIO.LOW
	else:
		direction = GPIO.HIGH
	#position_motor(12500,direction)
	run_motor(1000,direction)
	#t = threading.Thread(target=command_motor, args=(2000,direction,))
	#t.start()
	if direction == GPIO.HIGH:
		subprocess.run(["aplay","-D","default:CARD=Device","Domestic_Fight_Between_Alpha_Female_and_Alpha_Male2.wav"])
	else:
		subprocess.run(["aplay","-D","default:CARD=Device","heydeer2.wav"])
		subprocess.run(["aplay","-D","default:CARD=Device","heydeer2.wav"])
		subprocess.run(["aplay","-D","default:CARD=Device","heydeer2.wav"])
	#time.sleep(5)

GPIO.cleanup()
