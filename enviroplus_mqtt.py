#!/usr/bin/env python3

import time
from pms5003 import PMS5003, ReadTimeoutError

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
    except ReadTimeoutError:
        pms5003 = PMS5003()


