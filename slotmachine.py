# Importing modules and classes
import tm1637
import time
import numpy as np
import RPi.GPIO as GPIO
from gpiozero import Button
from signal import pause
import random
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
last_press_time = 0
runone = True
jackpot = False
jackpot_num = 0
rig = False
# Creating 4-digit 7-segment display object
tm = tm1637.TM1637(clk=18, dio=17)  # Using GPIO pins 18 and 17
clear = [0, 0, 0, 0]  # Defining values used to clear the display
tm.write(clear) # Clear display, if anything was pre-exisitng
# Setup LED Light
GPIO.setup(21, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
def touched():
	# Getting Global Values (Values from above so that the function can directly change them)
	global jackpot
	global jackpot_num
	global last_press_time
	global touch
	global runone
	current_time = time.time()
	if (current_time - last_press_time) > 0.2:
		GPIO.setup(21, GPIO.OUT)
		if rig  == True:
			rnum = tm.encode_string(str(random.randint(0,9)))
			D1 = rnum
			D2 = rnum
			D3 = rnum
			D4 = rnum
		else:
			D1 = tm.encode_string(rand_num())
			D2 = tm.encode_string(rand_num())
			D3 = tm.encode_string(rand_num())
			D4 = tm.encode_string(rand_num())
		# Visual function cycles through numbers for a visual effect
		visual(0)
		# Write encoded string into designated spot on the 4-Digit Display
		tm.write(D1, pos = 0)
		visual(1)
		tm.write(D2, pos = 1)
		visual(2)
		tm.write(D3, pos = 2)
		visual(3)
		tm.write(D4, pos = 3)
		# Check if a jackpot
		if D1 == D2 == D3 == D4:
			i = 0
			while i < 5: # Set to 10 for 10 second blinking
				# Flash the light
				GPIO.output(21,GPIO.HIGH)
				time.sleep(0.5)
				GPIO.output(21, GPIO.LOW)
				time.sleep(0.5)
				i += 1
				continue
				if i == 4: # Set to 9 for 10 second blinking, initial light on counts as one.
					GPIO.output(21, GPIO.LOW)
					break
		# Reset the variables and 4 Digit Display to run again
		time.sleep(2)
		jackpot_num = 0
		jackpot = False
		tm.write(clear)
		runone = True
def rig():
	global rig
	if rig == False:
		rig = True
		print("RIG: TRUE")
	else:
		rig = False
		print("RIG: FALSE")
def visual(p):
	for digit_value in range(10):
		tm.write(tm.encode_string(str(digit_value)),pos=p)
		time.sleep(0.05)
def rand_num():
	global runone
	global jackpot
	global jackpot_num
	global rig
	jackpot_chance = 0.8
	chance = random.random()
	# Determine if a jackpot or not
	if runone == True:
		if chance < jackpot_chance:
			num = str(random.randint(0,9))
			return(num)
			jackpot = False
		elif chance >= jackpot_chance:
			jackpot = True
			jackpot_num = str(random.randint(0,9))
		runone = False
	# Returns number after inital run
	if jackpot == True:
		return(jackpot_num)
	elif jackpot == False:
		num = str(random.randint(0,9))
		return(num)
def not_touched():
	pass
# Button setups and corresponding functions
touch_sensor = Button(20,bounce_time=0.04,  pull_up=None, active_state = True,)
touch_sensor2 = Button(19, bounce_time=0.02, pull_up=None, active_state = True,)
touch_sensor2.when_pressed = rig
touch_sensor.when_pressed = touched
touch_sensor.when_released = not_touched
# Pause to detect for button presses/Indefitely run
pause()

