import RPi.GPIO as GPIO
import matplotlib.pyplot as pyplot
import time

GPIO.setmode(GPIO.BCM)

data = []

dac = [8, 11, 7, 1, 0, 5, 12, 6]
leds = [2, 3, 4, 17, 27, 22, 10, 9]
comp = 14
troyka = 13

GPIO.setup(dac,    GPIO.OUT)
GPIO.setup(troyka, GPIO.OUT, initial = 1)
GPIO.setup(comp,   GPIO.IN)


def adc():
    num = 0
    for i in range(7, -1, -1):
        num += 2**i
        num_list = decimal2binary(num) 
        GPIO.output(dac, num_list)
        time.sleep(0.002)
        comp_value = GPIO.input(comp)
        if (comp_value >= 0.95 and comp_value <= 1.05):
            num -= 2**i
    return num



#перевод в двоичную систему
def decimal2binary(value): 
    return [int(bit) for bit in bin(value)[2:].zfill(8)]

try:
    comp_value = 0
    c = 0
    t = time.time()
    GPIO.output(troyka, 1)
    while(comp_value < 207):
        comp_value = adc()
        c+=1
        volt = comp_value / 256 * 3.3
        data.append(comp_value)
        print(comp_value, volt, "volts")
            
    GPIO.output(troyka, 0)

    while(comp_value > 192):
        comp_value = adc()
        c+=1
        volt = comp_value / 256 * 3.3
        data.append(comp_value)
        print(comp_value, volt, "volts")
    t_ex = time.time() - t
    
    data_str = [str(i) for i in data]
    #data_time_str = [str(i) for i in data_time]
    with open("data.txt", "w") as outfile:
        outfile.write("\n".join(data_str))
    with open('settings.txt', 'w') as k:
        k.write("Частота дискретизации (Гц): " + str(c/t_ex) + '\n')
        k.write("\n Шаг квантования АЦП (В): " + '0.01289')

    print('общая продолжительность эксперимента {}, период одного измерения {}, средняя частота дискретизации проведённых измерений {}, шаг квантования АЦП {}'.format(t_ex, t_ex/c, 1/t_ex/c, 0.013))

    #график
    y = [i/256*3.3 for i in data]
    x = [i*t_ex/c for i in range(len(data))]
    pyplot.plot(x, y)
    pyplot.xlabel('время')
    pyplot.ylabel('вольтаж')
    pyplot.show()


finally:
    GPIO.output (dac, 0)
    GPIO.output (leds, 0)  
    GPIO.cleanup()



