import time
from blynkapi import Blynk
from gpiozero import LED
from time import sleep
import sys

auth_tokens = sys.argv[1]
led = LED(4)

def airconOn():
    led.on()

def airconOff():
    led.off()

for auth_token in auth_tokens:
    try:
        button = Blynk(auth_token, pin = "V0")
        button_val = str(button.get_val()[0])
        if button_val=="1":
            airconOn()
        else:
            airconOff()
    except Exception:
        sys.exit(1)