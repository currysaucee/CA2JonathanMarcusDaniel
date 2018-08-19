import time
import sys
import signal
import telepot
from random import randint
from blynkapi import Blynk
from time import sleep
from datetime import datetime
from buzzer import buzz
from rpi_lcd import LCD
import RPi.GPIO as GPIO


def random():
	ops = ['+', '-']
	number1 = randint(1, 3)
	number2 = randint(1, 3)
	operatornumber = randint(0,2)
	operation = ""
	answer = 0
	if operatornumber == 0:
		operation = '+'
		answer = number1 + number2
		question = (str(number1) + '+' + str(number2))
		return question, answer

	if operatornumber == 1:
		operation = '-'
		answer = number1 - number2
		question = (str(number1) + '-' + str(number2))
		return question, answer

def alarmON(alarm, question, answer):
	awake = 0
	off = False
	attempt = 0
	try:
        # Loop to continuously check time, buzz the buzzer for the set alarm time
		while True:
			# Continually get's the time as an integer value
			curr_time = int(time.strftime("%H%M"))
			pressed = GPIO.input(16)
			add = GPIO.input(27)
			minus = GPIO.input(22)

			if add == True:
				attempt = attempt + 1
				print(attempt)

			if minus == True:
				attempt = attempt - 1
				print(attempt)

			if pressed == True:
				if attempt == answer:
					print('alarm is off')
					break

                # Buzzes the buzzer when the time reaches the set alarm time
			if curr_time == alarm:
				buzz(10,0.5)
				time.sleep(0.25)
				buzz(20,0.5)
				time.sleep(0.25)
				awake = 1
				lcd.text(question,1)
				display = 'Answer is now ' + str(attempt)
				lcd.text(display, 2)
    		    
                # If alarm continues past the set alarm time without being
                # snoozed, the alarm time is changed to the current time.
                # This ensures the alarm buzzes continuously until the
                # snooze button is pressed.
			elif curr_time != alarm and awake == 1:
				alarm = curr_time
				buzz(10,0.5)
				time.sleep(0.25)
				buzz(20,0.5)
				time.sleep(3)
				lcd.text(question,1)
				display = 'Answer is now ' + str(attempt)
				lcd.text(display, 2)

			sleep(3)
	finally:
		print('off')

def setAlarm(msg):
	print('listens in tele')
	chat_id = msg['chat']['id']
	alarm = msg['text']
	
	curr_time = int(time.strftime("%H%M"))
	try:
		intalarm = int(alarm)
	except:
		bot.sendMessage(chat_id, 'Not a valid time, please enter one in HHMM format')

	if curr_time >= intalarm:
		question,answer = random()
		bot.sendMessage(chat_id, ('Alarm set for tomorrow @ {}'.format(alarm)))
		buzz(500,0.1)
		print(question)
		alarmON(intalarm, question, answer)
		

	if intalarm > curr_time:
		question, answer = random()
		bot.sendMessage(chat_id, ('Alarm set for today @ {}'.format(alarm)))
		buzz(500,0.1)
		print(question)
		alarmON(intalarm, question, answer)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN)
GPIO.setup(27, GPIO.IN)
GPIO.setup(22, GPIO.IN)


lcd = LCD()
global needquestion
global question
question = ''
global answer
answer = 0
needquestion = 1
my_bot_token = "685042644:AAEBhZl5I75pIHLd2Hxgm91-SZfXDLNf6kI"
bot = telepot.Bot(my_bot_token)
bot.message_loop(setAlarm)

while True:
	sleep(1)
