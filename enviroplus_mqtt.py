#!/usr/bin/env python3

import time
from pms5003 import PMS5003, ReadTimeoutError
from enviroplus import gas
from bme280 import BME280
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import paho.mqtt.client as mqtt
import logging
logger = logging.getLogger()
logger.setLevel(logging.ERROR) 

#Load configuration from .ini file
import configparser
import sys
# make sure config file exists
try:
    f = open('config.ini')
except FileNotFoundError:
    print("config.ini file not found")
    sys.exit()
# read config file
config = configparser.ConfigParser()
config.read('config.ini')

MQTT_ADDRESS = config.get('MQTT', 'MQTT_ADDRESS')
MQTT_USER = config.get('MQTT', 'MQTT_USER')
MQTT_PASSWORD = config.get('MQTT', 'MQTT_PASSWORD')
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'enviroplus'

def on_disconnect(mqtt_client, userdata, rc):
    logging.info("disconnecting reason  "  +str(rc))
    mqtt_client.connected_flag=False
    mqtt_client.disconnect_flag=True

def on_connect(mqtt_client, userdata, flags, rc):
    if rc==0:
        mqtt_client.connected_flag=True
    else:
        print('bad connection')

mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.on_connect= on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.connect(MQTT_ADDRESS, 1883)
mqtt_client.loop_start()


bme280 = BME280()
pms5003 = PMS5003()
time.sleep(1.0)

# get values from readings object (class PMS5003Data)

# pm_ug_per_m3(1.0)
# pm_ug_per_m3(2.5)
# pm_ug_per_m3(10))

while True:

    if not mqtt_client.connected_flag:
        try:
            mqtt_client.connect(MQTT_ADDRESS, 1883)
        except:
            print('Disconnected')

    try:
        # wake sensor from low power mode and wait to stabilise
        GPIO.output(22, 1)
        time.sleep(30)
        pms_readings = pms5003.read()
        gas_readings = gas.read_all()
        pres = bme280.get_pressure()
        temp = bme280.get_temperature()
        hum = bme280.get_humidity()

        mqtt_client.publish("home/indoor/PM1", pms_readings.pm_ug_per_m3(1.0))
        mqtt_client.publish("home/indoor/PM2.5", pms_readings.pm_ug_per_m3(2.5))
        mqtt_client.publish("home/indoor/PM10", pms_readings.pm_ug_per_m3(10))
        mqtt_client.publish("home/indoor/pressure", pres)
        mqtt_client.publish("home/indoor/temperature", temp)
        mqtt_client.publish("home/indoor/humidity", hum)

        mqtt_client.publish("home/indoor/gas_reducing", gas_readings.reducing)
        mqtt_client.publish("home/indoor/gas_oxidising", gas_readings.oxidising)
        mqtt_client.publish("home/indoor/gas_nh3", gas_readings.nh3)

    except ReadTimeoutError:
        pms5003 = PMS5003()

    # put sensor in low power mode and sleep until next reading
    GPIO.output(22, 0)
    time.sleep(30)
