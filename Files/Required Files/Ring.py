from gpiozero import Buzzer
from time import sleep

bz = Buzzer(4)
bz.on()
sleep(1)
bz.off()
