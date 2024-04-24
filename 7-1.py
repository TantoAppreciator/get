import RPi.GPIO as gpio
import time
from matplotlib import pyplot

gpio.setmode(gpio.BCM)

led = [2, 3, 4, 17, 27, 22, 10, 9]
gpio.setup(led, gpio.OUT)

dac = [8, 11, 7, 1, 0, 5, 12, 6]
gpio.setup(dac, gpio.OUT, initial = gpio.HIGH)

comp = 14
troyka = 13
gpio.setup(troyka, gpio.OUT, initial=gpio.HIGH)
gpio.setup(comp,gpio.IN)


#перевод в двоичную
def binary(a):
    return [int (m) for m in bin(a)[2:].zfill(8)]


#напряжение
def adc():
    f = 0
    for i in range (7, -1, -1):
        f += 2**i
        gpio.output(dac, binary(f))
        time.sleep(0.005)
        if gpio.input(comp) == 1:
            f -= 2**i
    return f




try:
    u = 0
    result = []
    t = time.time()
    c = 0

    #зарядка и показания
    print('зарядка')
    while u < 256*0.8:
        u = adc()
        result.append(u)
        c += 1
        gpio.output(led, binary(u))

    gpio.setup(troyka, gpio.OUT, initial=gpio.LOW)

    #разрядка
    print('разрядка')
    while u > 256*0.02:
        u = adc()
        result.append(u)
        c += 1
        gpio.output(led, binary(u))

    #время опыта
    t_ex = time.time() - t

    #запись данных
    print('запись данных в файл')
    with open('data.txt', 'w') as k:
        for i in result:
            k.write(str(i) + '\n')
    with open('settings.txt', 'w') as k:
        k.write("Частота дискретизации (Гц): " + str(c/t_ex) + '\n')
        k.write("\n Шаг квантования АЦП (В): " + '0.01289')

    print('общая продолжительность эксперимента -{}, период одного измерения -{}, средняя частота дискретизации проведённых измерений -{}, шаг квантования АЦП -{}'.format(t_ex, t_ex/c, 1/t_ex/c, 0.013))

    #график
    y = [i/256*3.3 for i in result]
    x = [i*t_ex/c for i in range(len(result))]
    pyplot.plot(x, y)
    pyplot.xlabel('время')
    pyplot.ylabel('вольтаж')
    pyplot.show()



finally:
    gpio.output(dac, 0)
    gpio.output(led, 0)
    gpio.cleanup()