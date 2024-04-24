import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from time import sleep

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setmode (GPIO.BCM)
GPIO.setup (leds, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (dac, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

data = []
data_time = []
#перевод в двоичную систему
def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]
#напряжение
def adc():
    temp = 0
    for i in range(7, -1, -1):
        temp += 2**i
        GPIO.output(leds, decimal2binary(temp))
        sleep(0.001)
        if GPIO.input(comp) == 1:
            temp -= 2**i
    return temp
try:
    t = time.time()

    

   

finally:
    GPIO.output (dac, 0)
    GPIO.output (leds, 0)  
    GPIO.cleanup()
data_str = [str(i) for i in data]
data_time_str = [str(i) for i in data_time]
with open("data.txt", "w") as outfile:
        outfile.write("\n".join(data_str))

plt.plot(data)
plt.show()

