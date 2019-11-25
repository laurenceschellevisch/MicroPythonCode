from machine import Pin, I2C, Timer,
from display.SSD1306 import SSD1306
from display.SSD1306 import SH1106_I2C
import socket
import utime
import pycom
import machine
from machine import Pin

# import settings
# import machine

from settings import app_eui, app_key
from network import LoRa
import struct
import binascii


# Get address information of site
# url = 'towel.blinkenlights.nl'
# addr_info = socket.getaddrinfo(url, 23)
# # Get the IP and port
# addr = addr_info[0][-1]

# # Connect to it via socket
# s = socket.socket()
# s.connect(addr)

# # Print content/animation in console
# # Use Ctrl-C to interrupt
# while True:
#     data = s.recv(500)
#     print(str(data, 'utf8'), end='')


# # Disable the heartbeat LED
# pycom.heartbeat(False)

# # Make the LED light up in black
# pycom.rgbled(0x000000)

# Initialize LoRa in LORAWAN mode.
# lora = LoRa(mode=LoRa.LORAWAN, adr=True)

# # Retrieve the dev_eui from the LoRa chip (Only needed for OTAA to retrieve once)
# dev_eui = binascii.hexlify(lora.mac()).upper().decode('utf-8')
# print(dev_eui)

# # Join a network using OTAA (Over the Air Activation)
# lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# # Wait until the module has joined the network
# count = 0
# while not lora.has_joined():
#     pycom.rgbled(0xffa500)  # Make the LED light up in orange
#     time.sleep(0.2)
#     pycom.rgbled(0x000000)  # Make the LED light up in black
#     time.sleep(2)
#     print("retry join count is:",  count)
#     count = count + 1

# print("join procedure succesfull")

# # Show that LoRa OTAA has been succesfull by blinking blue
# pycom.rgbled(0x0000ff)
# time.sleep(0.5)
# pycom.rgbled(0x000000)
# time.sleep(0.1)
# pycom.rgbled(0x0000ff)
# time.sleep(0.5)
# pycom.rgbled(0x000000)

# # Create a raw LoRa socket
# s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
# # Set the LoRaWAN data rate
# s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
# # Make the socket non-blocking
# s.setblocking(False)

# while True:

#    # send the data over LPWAN network
#     s.send('Hello world')
#     print('LoRa packet sent')

#     pycom.rgbled(0x007f00)  # Make the LED light up in green
#     time.sleep(0.2)
#     pycom.rgbled(0x000000)
#     time.sleep(2.8)

#     # Wait for 60 seconds before moving to the next iteration
#     time.sleep(60)


# i2c = I2C(0)                         # create on bus 0
# i2c = I2C(0, I2C.MASTER)
# # create and use non-default PIN assignments (P10=SDA, P11=SCL)
# i2c = I2C(0, pins=('P9', 'P10'))
# i2c.init(I2C.MASTER, baudrate=20000)

# oled = SH1106_I2C(129, 64, i2c)

# oled.init_display()
# oled.text('HElloo', 5, 20)
# oled.show()


# initialise Ultrasonic Sensor pins
# Lopy4 specific: Pin('P20', mode=Pin.IN)
echo = Pin(Pin.exp_board.G7, mode=Pin.IN)
# Lopy4 specific Pin('P21', mode=Pin.IN)
trigger = Pin(Pin.exp_board.G8, mode=Pin.OUT)
trigger(0)

# Ultrasonic distance measurment


def distance_measure():
    distance_samples = []
    # trigger pulse LOW for 2us (just in case)
    trigger(0)
    utime.sleep_us(2)
    # trigger HIGH for a 10us pulse
    trigger(1)
    utime.sleep_us(10)
    trigger(0)

    # wait for the rising edge of the echo then start timer
    while echo() == 0:
        pass
    start = utime.ticks_us()

    # wait for end of echo pulse then stop timer
    while echo() == 1:
        pass
    finish = utime.ticks_us()

    # pause for 20ms to prevent overlapping echos
    utime.sleep_ms(500)

    # calculate distance by using time difference between start and stop
    # speed of sound 340m/s or .034cm/us. Time * .034cm/us = Distance sound travelled there and back
    # divide by two for distance to object detected.
    distance = ((utime.ticks_diff(start, finish)) * .034)/2

    for count in range(20):
        distance_samples.append(int(distance))

    # sort the list
    distance_samples = sorted(distance_samples)
    distance_median = distance_samples[int(len(distance_samples)/2)]

    return int(distance_median)


while True:
    print('Afstand {distance} CM'.format(distance=distance_measure()))
