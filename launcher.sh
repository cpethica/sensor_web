#!/bin/sh
# launcher.sh

sleep 60

cd /
cd home/pi/sensor_web
python MQTTInfluxDBBridge.py &
python enviroplus_mqtt.py
cd /
