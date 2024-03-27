import RPi.GPIO as GPIO
from time import sleep

def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
x = 0
flag = 1
try:
    period = float(input())
    while(1):
        GPIO.output(dac,decimal2binary(x))
        print('Output voltage is', '{:.4f}'.format(float(x)/256.0*3.3), 'volts')
        if x == 0: flag = 1
        elif x == 255: flag = 0
        if flag: x += 1
        else: x -= 1
        sleep(period/512)
except ValueError:
    print("wrong period")
finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()