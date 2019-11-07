#!/usr/bin/env python2
from __future__ import division, print_function

from Cadence import Cadence
from Osd import Osd
from SpeedAndDistance import SpeedAndDistance
from Radio import Radio
from Battery import Battery
import time

#############
# Constants
#############
CADENCE_PIN = 31 # GPIO.BOARD
SPEED_PIN = 29 # GPIO.BOARD
UPDATE_INTERVAL = 0.5 # Target amount of time between OSD updates
TX_INTERVAL = 3 # Time between radio transmits

#############
# Setup
#############
cadenceModule = Cadence(CADENCE_PIN)
speedAndDistanceModule = SpeedAndDistance(SPEED_PIN)
osdModule = Osd()
radioModule = Radio(1, 2)
batteryModule = Battery()

txIntervalCount = 0

emergency = 0

logFileName = "{}.log".format(time.strftime('%y%m%d-%H%M%S', time.localtime()))
logFile = open(logFileName, "w+")

#############
# Main
#############
try:
    while True:
        start_time = time.clock()
        speedKph = speedAndDistanceModule.get_speed()
        speedMph = speedAndDistanceModule.get_speed_mph()
        targetSpeedKph = speedAndDistanceModule.get_target_speed()
        targetSpeedMph = speedAndDistanceModule.get_target_speed_mph()
        cadence = cadenceModule.get_cadence()
        distance = speedAndDistanceModule.get_distance_miles()
        batteryPercentage = batteryModule.getBatteryPercentage()

        osdModule.Display(
            speedKph=speedKph,
            speedMph=speedMph,
            targetSpeedKph=targetSpeedKph,
            targetSpeedMph=targetSpeedMph,
            cadence=cadence,
            distance=distance,
            batteryPercentage=batteryPercentage)

        logFile.write(",".join(map(str,(
            time.strftime('%H:%M:%S'),
            round(speedKph, 2),
            round(targetSpeedKph, 2),
            round(cadence, 1),
            round(distance, 2),
            round(batteryPercentage, 1),
            emergency))) + "\n")


        # Transmit every TX_INTERVAL seconds
        if txIntervalCount >= TX_INTERVAL:
            radioModule.Transmit(
                    time.strftime('%H:%M:%S'),
                    round(speedKph, 2),
                    round(targetSpeedKph, 2),
                    round(cadence, 1),
                    round(distance, 2),
                    round(batteryPercentage, 1),
                    emergency)
            txIntervalCount = 0

        duration = time.clock() - start_time
        if duration < UPDATE_INTERVAL:
            txIntervalCount += UPDATE_INTERVAL
            time.sleep(UPDATE_INTERVAL - duration)
        else:
            txIntervalCount += duration

except KeyboardInterrupt:
    radioModule.radio.shutdown()
