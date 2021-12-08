#!/usr/bin/env python3

import time
from pms5003 import PMS5003, ReadTimeoutError

import paho.mqtt.client as mqtt

MQTT_ADDRESS = '192.168.1.101'
MQTT_USER = 'sensor_web'
MQTT_PASSWORD = 'envirosense!mqtt'
MQTT_TOPIC = 'home/+/+'
MQTT_REGEX = 'home/([^/]+)/([^/]+)'
MQTT_CLIENT_ID = 'enviroplus'

mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
mqtt_client.connect(MQTT_ADDRESS, 1883)

pms5003 = PMS5003()
time.sleep(1.0)





# get values from readings object (class PMS5003Data)

# pm_ug_per_m3(1.0)
# pm_ug_per_m3(2.5)
# pm_ug_per_m3(10))


while True:
    try:
        readings = pms5003.read()
        print(f"PM10 ug/m3 (combustion particles, organic compounds, metals): {readings.pm_ug_per_m3(10)}")

        mqtt_client.publish("home/indoor/PM10", readings.pm_ug_per_m3(10))


    except ReadTimeoutError:
        pms5003 = PMS5003()


