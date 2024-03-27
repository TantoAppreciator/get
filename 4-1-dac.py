import RPi.GPIO as GPIO
#import time

def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

dac = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)

try:
    while(1):
        num = input()
        try:
            num = int(num)
            GPIO.output(dac, decimal2binary(num))
            print('Output voltage is', '{:.4f}'.format(float(num)/256.0*3.3), 'volts')
        except ValueError:
            if num == "q": break
            print("type a number from 0 to 255")
            continue
        except Exception:
            if num < 0: print("the number must be positive")
            if num > 255: print("the number must be less than 256")
finally:
    GPIO.output (dac, 0)
    GPIO.cleanup()
