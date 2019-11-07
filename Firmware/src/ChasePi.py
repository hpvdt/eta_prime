#!/usr/bin/env python2

from __future__ import print_function
from Radio import Radio
from datetime import datetime
import time
from random import random
from numpy import array, append
import matplotlib
matplotlib.use('tkagg')
import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.widgets import Button
import os

#############
# Initialization
#############
logFileName = "{}.log".format(time.strftime('%y%m%d-%H%M%S', time.localtime()))
logFile = open(logFileName, "w+")

radio = Radio(2, 1)

timeList = array([0])
speedKphList = array([0])
speedMphList = array([0])
targetSpeedKphList = array([0])
targetSpeedMphList = array([0])
cadenceList = array([0])
distanceList = array([0])

#TODO: Ideally the receive function would try to decode as many values as
# possible and use the ones that are correct to partially update the graph.

def receive_value():
    invalidValue = True
    while invalidValue:
        try:
            message = radio.Receive()
            if message == None:
                print("Timed out while waiting to receive.")
            else:
                values  = message.split(",")
                t = datetime.strptime(values[0], '%H:%M:%S')
                speedKph, targetSpeedKph, cadence, distance, batteryPercentage, emergency = map(float, values[1:])
                invalidValue = False
        except ValueError:
            print("Received bad transmission: {}".format(message))
    return t, speedKph, targetSpeedKph, cadence, distance, batteryPercentage, emergency


print("Waiting for First Radio Transmission from Bike...")
starttime = receive_value()[0]

# Plots
plt.ion()
fig = plt.figure(figsize=(12, 10))
speed_subplot = plt.subplot(311)
plt.title('Speed')
plt.axis([0, 600, 0, 150])
speedKphLine, targetSpeedKphLine = plt.plot(
    timeList, speedKphList, 'b-',
    timeList, targetSpeedKphList, 'r-')

distance_subplot = plt.subplot(312)
plt.title('Distance')
plt.axis([0, 600, 0, 7])
distanceLine, = plt.plot(timeList, distanceList, 'c-')

cadence_subplot = plt.subplot(313)
plt.title('Cadence')
plt.axis([0, 600, 0, 300])
cadenceLine, = plt.plot(timeList, cadenceList, 'm-')

plt.style.use('ggplot')
plt.tight_layout()
plt.subplots_adjust(right=0.8)

# Axes rectangle is [Left, Bottom, Width, Height]
shutdown_axes = plt.axes([0.825, 0.1, 0.15, 0.07])
shutdown_button = Button(shutdown_axes, "Shutdown", color="#FF9999")
def shutdown_func(_):
    os.system("sudo shutdown -h now")
shutdown_button.on_clicked(shutdown_func)

#############
# Main
#############
xiter = xrange(1000).__iter__()

try:
    while True:
        t, speedKph, targetSpeedKph, cadence, distance, batteryPercentage, emergency = receive_value()
        # Update all the x-axes
        delta = t - starttime
        timeList = append(timeList, delta.seconds)
        speedKphLine.set_xdata(timeList)
        targetSpeedKphLine.set_xdata(timeList)
        distanceLine.set_xdata(timeList)
        cadenceLine.set_xdata(timeList)

        speedKphList = append(speedKphList, speedKph)
        speedKphLine.set_ydata(speedKphList)


        targetSpeedKphList = append(targetSpeedKphList, targetSpeedKph)
        targetSpeedKphLine.set_ydata(targetSpeedKphList)

        cadenceList = append(cadenceList, cadence)
        cadenceLine.set_ydata(cadenceList)

        distanceList = append(distanceList, distance)
        distanceLine.set_ydata(distanceList)

        fig.canvas.flush_events()

finally:
    radio.radio.shutdown()
