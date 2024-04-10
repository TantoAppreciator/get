import RPi.GPIO as GPIO
from time import sleep
dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2,3,4,17,27,22,10,9]
comp = 14
troyka = 13

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def adc():
    for i in range(256):
        dac_value = decimal2binary(i)
        sleep(0.1)
        GPIO.output(dac, dac_value)
        comp_value = GPIO.input(comp)
        if comp_value:
            return i
try:
    while(1):
        num = adc()
        if num:
            print('{:.3f}'.format(float(num)/256.0*3.3), 'V')
finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()