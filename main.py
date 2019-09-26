from machine import Pin, I2C
from time import sleep
from display.SSD1306 import SSD1306
from display.SSD1306 import SH1106_I2C

i2c = I2C(0, I2C.MASTER, baudrate=200000, pins=("P9","P10"))    
i2c.init(I2C.MASTER, baudrate=200000) 

# print('--------------------------------')
# print(i2c.scan())
# print('--------------------------------')
# i2c.writeto(0x42, 'hello')

oled = SH1106_I2C(128, 64, i2c)

oled.text('Hello, World 2!', 0, 0)
# oled.text('Hello, World 3!', 0, 20)


oled.show()
