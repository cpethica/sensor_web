# Complete project details at https://RandomNerdTutorials.com
import machine
from machine import Pin, I2C, ADC

import config       # add passwords etc
import BME280
import ubinascii
import network
from umqttsimple import MQTTClient
import esp
import micropython
import time

import esp
esp.osdebug(None)

import gc
gc.collect()

ms_sleep_time = 60000
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(config.ssid, config.password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def deep_sleep(msecs) :
  # configure RTC.ALARM0 to be able to wake the device
  rtc = machine.RTC()
  rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

  # set RTC.ALARM0 to fire after X milliseconds (waking the device)
  rtc.alarm(rtc.ALARM0, msecs)

  # put the device to sleep
  machine.deepsleep()

# ESP8266 - Pin assignement
i2c = I2C(scl=Pin(5),sda=Pin(4), freq=10000)
vpin = ADC(0)
bme = BME280.BME280(i2c=i2c)

# MQTT setup
client_id = ubinascii.hexlify(machine.unique_id())
mqtt_server = config.MQTT_ADDRESS
topic_pub_temp = b'esp/bme280/temperature'
topic_pub_hum = b'esp/bme280/humidity'
topic_pub_pres = b'esp/bme280/pressure'
topic_pub_volt = b'esp/bme280/voltage'

def connect_mqtt():
  global client_id, mqtt_server
  client = MQTTClient(client_id, mqtt_server, user=config.MQTT_USER, password=config.MQTT_PASSWORD)
  client.connect()
  print('Connected to %s MQTT broker' % (config.MQTT_ADDRESS))
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

def read_bme_sensor():
  try:
    temp = b'%s' % bme.temperature[:-1]
    time.sleep(2)
    hum = b'%s' % bme.humidity[:-1]
    time.sleep(2)
    pres = b'%s'% bme.pressure[:-3]

    return temp, hum, pres
    #else:
    #  return('Invalid sensor readings.')
  except OSError as e:
    return('Failed to read sensor.')

def voltage():
  try:
    v = vpin.read()
    # 4.35V = HIGH (1023) on analog pin - V = vpin x (4.35/1023)
    v = v * (4.35/1023)
    v = b'%s' % v
    q
    return v
  except OSError as e:
    return('Failed to read sensor.')

try:
  client = connect_mqtt()
except OSError as e:
  restart_and_reconnect()

try:
    temp, hum, pres = read_bme_sensor()
    volts = voltage()
    client.publish(topic_pub_temp, temp)
    client.publish(topic_pub_hum, hum)      
    client.publish(topic_pub_pres, pres)
    client.publish(topic_pub_volt, volts)
    print(temp)
    print(hum)
    print(pres)
    print(volts)

except OSError as e:
    restart_and_reconnect()

time.sleep(10)

#ESP8266
deep_sleep(ms_sleep_time)

#ESP32
#machine.deepsleep(ms_sleep_time)
