import RPi.GPIO as GPIO
from time import sleep


dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (leds, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

def volume(n):
    n=int(n/256*10)
    mas=[0]*8
    for i in range(n-1):
        mas[i]=1
    return mas

def adc():
    temp = 0
    for i in range(7, -1, -1):
        temp += 2**i
        GPIO.output(dac, decimal2binary(temp))
        sleep(0.001)
        if GPIO.input(comp) == 1:
            temp -= 2**i
    return temp
try:
    while(1):
        num=adc()
        if num:
            print('{:.4}'.format(float(num)/256.0*3.3), 'V')
            if num is not None:
                GPIO.output(leds,volume(num))
finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()