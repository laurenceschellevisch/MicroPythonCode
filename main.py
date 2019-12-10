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

from network import WLAN      # For operation of WiFi network
import time                   # Allows use of time.sleep() for delays
import pycom                  # Base library for Pycom devices
from display.umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython cod



# These need to be change to suit your environment
RANDOMS_INTERVAL = 5000 # milliseconds
last_random_sent_ticks = 0  # milliseconds

# Wireless network
WIFI_SSID = "WifiBoven"
WIFI_PASS = "55229933astona" # No this is not our regular password. :)

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "lau2000"
AIO_KEY = "39a1babf997b42779099b5aaaca0e47f"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_CONTROL_FEED = "CoreChris/feeds/lights"
AIO_RANDOMS_FEED = "CoreChris/feeds/randoms"

# END SETTINGS

# RGBLED
# Disable the on-board heartbeat (blue flash every 4 seconds)
# We'll use the LED to respond to messages from Adafruit IO
pycom.heartbeat(False)
time.sleep(0.1) # Workaround for a bug.
                # Above line is not actioned if another
                # process occurs immediately afterwards
pycom.rgbled(0xff0000)  # Status red = not working

# WIFI
# We need to have a connection to WiFi for Internet access
# Code source: https://docs.pycom.io/chapter/tutorials/all/wlan.html

wlan = WLAN(mode=WLAN.STA)
wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=5000)

while not wlan.isconnected():    # Code waits here until WiFi connects
    machine.idle()

print("Connected to Wifi")
pycom.rgbled(0xffd7000) # Status orange: partially working

# FUNCTIONS

# Function to respond to messages from Adafruit IO
def sub_cb(topic, msg):          # sub_cb means "callback subroutine"
    print((topic, msg))          # Outputs the message that was received. Debugging use.
    if msg == b"ON":             # If message says "ON" ...
        pycom.rgbled(0xffffff)   # ... then LED on
    elif msg == b"OFF":          # If message says "OFF" ...
        pycom.rgbled(0x000000)   # ... then LED off
    else:                        # If any other message is received ...
        print("Unknown message") # ... do nothing but output that it happened.

def random_integer(upper_bound):
    return machine.rng() % upper_bound

def send_random():
    global last_random_sent_ticks
    global RANDOMS_INTERVAL

    if ((time.ticks_ms() - last_random_sent_ticks) < RANDOMS_INTERVAL):
        return; # Too soon since last one sent.

    some_number = random_integer(100)
    print("Publishing: {0} to {1} ... ".format(some_number, AIO_RANDOMS_FEED), end='')
    try:
        client.publish(topic=AIO_RANDOMS_FEED, msg=str(some_number))
        print("DONE")
    except Exception as e:
        print("FAILED")
    finally:
        last_random_sent_ticks = time.ticks_ms()

# Use the MQTT protocol to connect to Adafruit IO
client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT, AIO_USER, AIO_KEY)

# Subscribed messages will be delivered to this callback
client.set_callback(sub_cb)
client.connect()
client.subscribe(AIO_CONTROL_FEED)
print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_CONTROL_FEED))

pycom.rgbled(0x00ff00) # Status green: online to Adafruit IO

try:                      # Code between try: and finally: may cause an error
                          # so ensure the client disconnects the server if
                          # that happens.
    while 1:              # Repeat this loop forever
        client.check_msg()# Action a message if one is received. Non-blocking.
        send_random()     # Send a random number to Adafruit IO if it's time.
finally:                  # If an exception is thrown ...
    client.disconnect()   # ... disconnect the client and clean up.
    client = None
    wlan.disconnect()
    wlan = None
    pycom.rgbled(0x000022)# Status blue: stopped
    print("Disconnected from Adafruit IO.")
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


i2c = I2C(0)                         # create on bus 0
i2c = I2C(0, I2C.MASTER)
# create and use non-default PIN assignments (P10=SDA, P11=SCL)
# i2c = I2C(0, pins=('P9', 'P10'))
i2c = I2C(0, pins=(Pin.exp_board.G16, Pin.exp_board.G17))
i2c.init(I2C.MASTER, baudrate=30000)

oled = SH1106_I2C(129, 64, i2c)

oled.init_display()


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

    for count in range(10):
        distance_samples.append(int(distance))

    # sort the list
    distance_samples = sorted(distance_samples)
    distance_median = distance_samples[int(len(distance_samples)/2)]

    return int(distance_median)


while True:
    oled.fill(0)
    # print(distance_measure())
    print('Afstand {distance} CM'.format(distance=distance_measure()))
    oled.text('Afstand {distance} CM'.format(
        distance=distance_measure()), 5, 20)
    oled.show()

oled.show()
