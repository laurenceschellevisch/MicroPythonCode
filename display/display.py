from machine import Pin, I2C
from display.SSD1306 import SH1106_I2C
def init():
    i2c = I2C(0)                         # create on bus 0
    i2c = I2C(0, I2C.MASTER)  
    i2c = I2C(0, pins=('P9','P10'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)
    i2c.init(I2C.MASTER, baudrate=20000)

    oled = SH1106_I2C(128, 64, i2c)

def showOnDisplay(text):
    oled.text(text, 0, 20)
    oled.show()
