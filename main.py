from display import accelerometer
from display import display
import time
from machine import Pin, I2C, Timer
from display import SSD1306

while True:
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
    i2c = I2C(0)                         # create on bus 0
    i2c = I2C(0, I2C.MASTER)  
    i2c = I2C(0, pins=('P9','P10'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)
    i2c.init(I2C.MASTER, baudrate=20000)

    oled = SSD1306.SH1106_I2C(128, 64, i2c)

    oled.text(distance, 0, 20)
    oled.show()
    time.sleep(1)