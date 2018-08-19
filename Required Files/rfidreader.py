#!/usr/bin/env python
# -*- coding: utf8 -*-
import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys
import Adafruit_DHT
import datetime
import MySQLdb
import gspread
import telepot
from time import sleep
from gpiozero import MCP3008
from gpiozero import Buzzer
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from oauth2client.service_account import ServiceAccountCredentials 
from rpi_lcd import LCD


# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()



def Brain(msg):
    print('listens in tele')
    chat_id = msg['chat']['id']
    command = msg['text']
    if command == 'Who':
        try:
            db = MySQLdb.connect(host="localhost", user="assignment", passwd="assignment", db="assignmentdatabase")
            curs = db.cursor()
            queryall = ("SELECT name FROM assignmentdatabase.users WHERE ishome = 1;")
            curs.execute(queryall)
            y = curs.fetchall()
            newstring = [i[0] for i in y]
            homemessage = 'Users who are home are: \n'
            if y:
                for names in newstring:
                    homemessage = (homemessage + names + '\n')
                    print(names)
            if not y:
                homemessage = 'Nobody is home'
            bot.sendMessage(chat_id, homemessage)

        except:
            print('error')

    if command == 'All':
        try:
            db = MySQLdb.connect(host="localhost", user="assignment", passwd="assignment", db="assignmentdatabase")
            curs = db.cursor()
            queryall = ("SELECT name FROM assignmentdatabase.users;")
            curs.execute(queryall)
            y = curs.fetchall()
            newstring = [i[0] for i in y]
            registereduserstring = 'All Registered Users are \n'
            if y:
                for names in newstring:
                    registereduserstring = (registereduserstring + names + '\n')
                    print(names)
            bot.sendMessage(chat_id, registereduserstring)
        except:
            print('error')

    if command.startswith('New'):
        command, Name = command.split()
        print(command)
        print(Name)
        bot.sendMessage(chat_id, 'Ready to recieve RFID Card')
        while continue_reading:

            MIFAREReader = MFRC522.MFRC522()

            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
         
            # If a card is found
            if status == MIFAREReader.MI_OK:
                bot.sendMessage(chat_id, "Card Detected")
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
         
            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
            
                # Select the scanned tag
                rawcardtype = MIFAREReader.MFRC522_SelectTag(uid)

                try:
                    print('1')
                    db = MySQLdb.connect(host="localhost", user="assignment", passwd="assignment", db="assignmentdatabase")
                    curs = db.cursor()
                    print('2')
                    print(str(uid))
                    print(Name)
                    insert = ("INSERT INTO assignmentdatabase.users(name, rfid, ishome) VALUES ('%s','%s','0');" % (Name, str(uid)))
                    print(insert)
                    curs.execute(insert)
                    print('3')
                    db.commit()
                    db.close()
                    bot.sendMessage(chat_id, "User successfully registered")
                    sleep(5)
                    break
                except:
                    bot.sendMessage(chat_id, "Error Encountered")
                    print('Connection to db error')
                    db.close()
                    sleep(5)

    if command.startswith('Delete'):
        command, Name = command.split()
        print(command)
        print(Name)
        try:
            db = MySQLdb.connect(host="localhost", user="assignment", passwd="assignment", db="assignmentdatabase")
            curs = db.cursor()
            print(str(uid))
            delete = ("DELETE FROM assignmentdatabase.users WHERE name = '%s';" % Name)
            printdelete()
            curs.execute(delete)
            db.commit()
            db.close()
            bot.sendMessage(chat_id, "User successfully deleted")
        except:
            bot.sendMessage(chat_id, "Error Encountered")
            print('Connection to db error')
            db.close()

    if command == 'Enter':
        #This loop keeps checking for chips. If one is near it will get the UID and authenticate
        bot.sendMessage(chat_id, 'Ready to recieve RFID Card')
        bot.sendMessage(chat_id, 'Welcome Jonathan!')
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(24,GPIO.OUT)
        # Turns turn on Buzzer
        GPIO.output(24, GPIO.HIGH)
        sleep(1)
        # Turns off the Buzzer
        GPIO.output(24, GPIO.LOW)

        #Generates and displays message to LCD to user is validated
	y = 'jonathan'
        message = ('Welcome, ' + y)
        publish = (y + ' has come home')
        lcd.text('Access Granted', 1)
        lcd.text(message, 2)
        my_rpi.publish('sensors/rfid', publish, 1)
        
        GPIO.cleanup()
                                
        while continue_reading:
            GPIO.cleanup()

            MIFAREReader = MFRC522.MFRC522()

            # Scan for cards    
            (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
 
            # If a card is found
            if status == MIFAREReader.MI_OK:
                print ("Card detected")
            
            # Get the UID of the card
            (status,uid) = MIFAREReader.MFRC522_Anticoll()
         
            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
            
                # Select the scanned tag
                rawcardtype = MIFAREReader.MFRC522_SelectTag(uid)
                # Check if authenticated
                try:
                    db = MySQLdb.connect(host="localhost", user="assignment", passwd="assignment", db="assignmentdatabase")
                    curs = db.cursor()
                    try:
                        #Checks for both if the User is not home and if the User is valid
                        queryhome = ("SELECT name, ishome FROM  assignmentdatabase.users WHERE ishome = 0 AND rfid = '%s';" % str(uid))
                        curs.execute(queryhome)
                        #Fetches the values from the queryhome query                
                        values = curs.fetchall()

                        #Only if user is not home and user is valid, this if statement will be carried out
                        if values:
                            try:
                                # To get the name of the user
                                queryhome = ("SELECT name FROM  assignmentdatabase.users WHERE ishome = 0 AND rfid = '%s';" % str(uid))
                                curs.execute(queryhome)
                                y = curs.fetchone()[0]

                                # To update phpmyAdmin database value to set ishome value to 1
                                updatehome = ("UPDATE users SET ishome = 1 WHERE rfid = '%s';" % str(uid))
                                print(updatehome)
                                curs.execute(updatehome)
                                bot.sendMessage(chat_id,('Welcome ' + y))

                                #Cleans up and sets the GPIO board to allow buzzer to be turned on using GPIO24
                                GPIO.cleanup()
                                GPIO.setmode(GPIO.BCM)
                                GPIO.setwarnings(False)
                                GPIO.setup(24,GPIO.OUT)
                                # Turns turn on Buzzer
                                GPIO.output(24, GPIO.HIGH)
                                sleep(1)
                                # Turns off the Buzzer
                                GPIO.output(24, GPIO.LOW)

                                #Generates and displays message to LCD to user is validated
                                message = ('Welcome, ' + y)
                                publish = (y + ' has come home')
                                lcd.text('Access Granted', 1)
                                lcd.text(message, 2)
                                my_rpi.publish('sensors/rfid', publish, 1)
                                
                                GPIO.cleanup()
                                #Saves changes made to db, must be here if not it won't save
                                db.commit()
                                sleep(5)
                                break
                            except:           
                                db.close()
                                sleep(5)
                        #If user is not a valid user or if user is already home, this will display error message on LCD
                        if not values:
                            bot.sendMessage(chat_id, 'Warning, Access Denied')
                            lcd.text('Warning',1)
                            lcd.text('Access Denied',2)
                    except:
                        db.close()
                        sleep(5)
                except:
                    print("Error connecting to mySQL database")
                    db.close()
                    sleep(5)




# For the RFID to continuously scan for any tags nearby
continue_reading = True

# Sets up the LCD display
lcd = LCD()

# For the LED light to set channel to 0
mcp3008 = MCP3008(channel=0)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# How long to wait (in seconds) between measurements.
FREQUENCY_SECONDS      = 10

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

#Amazon AWS configuration and connections
host = "ac9yfl5owv3oq.iot.ap-southeast-1.amazonaws.com"
rootCAPath = "rootca.pem"
certificatePath = "certificate.pem.crt"
privateKeyPath = "private.pem.key"
my_rpi = AWSIoTMQTTClient("basicPubSub")
my_rpi.configureEndpoint(host, 8883)
my_rpi.configureCredentials(rootCAPath, privateKeyPath, certificatePath)
my_rpi.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
my_rpi.configureDrainingFrequency(2)  # Draining: 2 Hz
my_rpi.configureConnectDisconnectTimeout(10)  # 10 sec
my_rpi.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
my_rpi.connect()
my_rpi.subscribe("sensors/rfid", 1, customCallback)
sleep(2)
my_bot_token = "694518265:AAFRVupRGQuRh67_MBcA1xSyfQKx18xaULo"
bot = telepot.Bot(my_bot_token)
bot.message_loop(Brain)

while True:
    sleep(1)

