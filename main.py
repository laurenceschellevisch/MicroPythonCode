from machine import Pin, I2C, Timer
import time
from display.SSD1306 import SSD1306
from display.SSD1306 import SH1106_I2C
import socket
from network import WLAN

wifi_ssid = 'mobile hotspot'

wifi_password = 'password'

wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()  # Scan all SSID networks
print('WLAN init')
for net in nets:
    print(net)
    if net.ssid == wifi_ssid:
        wlan.connect(net.ssid, auth=(
            net.sec, wifi_password), timeout=5000)
        while not wlan.isconnected():
            machine.idle()  # Save power while waiting
        print('WLAN connection succeeded!')
        break

# Get address information of site
url = 'towel.blinkenlights.nl'
addr_info = socket.getaddrinfo(url, 23)
# Get the IP and port
addr = addr_info[0][-1]

# Connect to it via socket
s = socket.socket()
s.connect(addr)

# Print content/animation in console
# Use Ctrl-C to interrupt
while True:
    data = s.recv(500)
    print(str(data, 'utf8'), end='')


i2c = I2C(0)                         # create on bus 0
i2c = I2C(0, I2C.MASTER)
# create and use non-default PIN assignments (P10=SDA, P11=SCL)
i2c = I2C(0, pins=('P9', 'P10'))
i2c.init(I2C.MASTER, baudrate=20000)

oled = SH1106_I2C(128, 64, i2c)


while True:
    echo = Pin('P14', mode=Pin.IN)
    trigger = Pin('P13', mode=Pin.OUT)
    trigger(0)

    chrono = Timer.Chrono()

    chrono.reset()

    trigger(1)
    time.sleep_us(30)
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
        oled.text("Distance {:.0f} cm".format(distance), 0, 20)
        oled.show()
    time.sleep(1)
