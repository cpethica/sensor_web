# Complete project details at https://RandomNerdTutorials.com
import machine
from machine import Pin, I2C, ADC

import BME280
import network
import urequests
from time import sleep

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'boringname'
password = 'Digisteph40br'

api_key = 'l4L-zx0hRGh-HrT2uH7nU3XgwsqZygKbxmptIEHNjKP'

ms_sleep_time = 600000

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

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

try:
  bme = BME280.BME280(i2c=i2c)
  temp = bme.temperature
  hum = bme.humidity
  pres = bme.pressure
  
  voltage = vpin.read()

  sensor_readings = {'value1':temp[:-1], 'value2':voltage, 'value3':pres[:-3]}
  print(sensor_readings)

  request_headers = {'Content-Type': 'application/json'}

  request = urequests.post(
    'https://maker.ifttt.com/trigger/bme_280_readings/with/key/' + api_key,
    json=sensor_readings,
    headers=request_headers)
  print(request.text)
  request.close()

except OSError as e:
  print('Failed to read/publish sensor readings.')

sleep(10)

#ESP8266
deep_sleep(ms_sleep_time)

#ESP32
#machine.deepsleep(ms_sleep_time)