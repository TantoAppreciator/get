import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)

p = GPIO.PWM(21, 1000) 
p.start(0)

try:
    while 1:
        d = int(input())
        p.ChangeDutyCycle(d)
        print(3.3*d/100)
finally:
    p.stop()
    GPIO.cleanup()
    GPIO.output(9,0)

