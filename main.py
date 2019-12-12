from machine import Pin, I2C, Timer,
from display.SSD1306 import SSD1306
from display.SSD1306 import SH1106_I2C
import socket
import utime
import pycom
import machine
from machine import Pin
import network
# import settings
# import machine

from network import WLAN      # For operation of WiFi network
import time                   # Allows use of time.sleep() for delays
import pycom                  # Base library for Pycom devices
from display.umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython cod


#callback from adafruit feed
def sub_cb(topic, msg): 
   print(msg) 
 
#creates adafruit connection
print(machine.unique_id())
client = MQTTClient(machine.unique_id(), "io.adafruit.com",user="lau2000", password="39a1babf997b42779099b5aaaca0e47f", port=1883) 
client.set_callback(sub_cb) 
client.connect()
client.subscribe(topic="lau2000/feeds/Chart") 


    
#making a output pin for the sound detection sensor
adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P16')   # create an analog pin on P16
val = apin.voltage() 
#initialise 2 pins for the display screen
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
    utime.sleep_ms(200)

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
    
    speed1 = distance_measure()
    print("speed1 = {} CM".format(speed1))
    time.sleep(3) 
    speed2 = distance_measure()
    print("speed2 = {} CM".format(speed2))
    distance = (speed1/100) - (speed2/100) # converting the centimeters measured in the 2 timestamps to meters AND getting the total distance
    distance = -distance if distance < 0 else distance #converting minus numbers so it works both away from the distance measure ment and towards it
    speed = (distance / 3) #making from the distance traveled the speed (distance traveled/ time = speed)
    print("distance traveled in 3 seconds = {} in meters".format(distance))
    client.publish(topic="lau2000/feeds/Chart", msg=str(speed)) #publishing the data to the adafruit server
    print("Snelheid {snelheid} M/S".format(snelheid=speed))
    oled.text("{snelheid} M/S".format(snelheid=speed),5,20)
    if val > 1000: # if the voltage is 1 volt the sound sensor detects sound and sends a voltage ifso a 1 will be send to adafruit 
        client.publish(topic="lau2000/feeds/sound", msg="1")
    else:
        client.publish(topic="lau2000/feeds/sound", msg="0")
    if distance_measure() > 50:
        oled.fill(0)
        oled.text('{distance} '.format(
        distance=distance_measure()), 5, 20)

    
    oled.show()

