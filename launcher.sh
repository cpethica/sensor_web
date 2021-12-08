#!/bin/sh
# launcher.sh

sleep 60

cd /
cd home/pi/sensor_web
sudo python3 MQTTInfluxDBBridge.py
cd /
