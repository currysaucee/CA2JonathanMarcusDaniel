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

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


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

my_rpi.connect()
my_rpi.subscribe("sensors/rfid", 1, customCallback)
sleep(2)

while True:
    sleep(1)
