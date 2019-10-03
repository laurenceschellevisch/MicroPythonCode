import time
from machine import Pin, Timer
def measureDistance():
    echo = Pin('P14', mode=Pin.IN)
    trigger = Pin('P13', mode=Pin.OUT)
    trigger(0)

    chrono = Timer.Chrono()


    chrono.reset()

    trigger(1)
    time.sleep_us(10)
    trigger(0)

    while echo() == 0:
        pass

    chrono.start()

    while echo() == 1:
        pass

    chrono.stop()

    distance = chrono.read_us() / 58.0

    if distance > 400:
        print("Out of range")
    else:
        print("Distance {:.0f} cm".format(distance))

    return distance