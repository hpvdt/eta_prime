from __future__ import division
import spidev
import RPi.GPIO as GPIO
import time

# Constants
V_REF = 5.0
LSB_SIZE = 2 * V_REF / 8192

A0_PIN = 3
A1_PIN = 5

# Source:
#   https://learn.sparkfun.com/tutorials/battery-technologies/lithium-polymer
CELL_PERCENTAGE = [(3.0, 0),
                   (3.1, 1),
                   (3.3, 5),
                   (3.4, 9),
                   (3.42, 10),
                   (3.47, 20),
                   (3.5, 30),
                   (3.52, 40),
                   (3.55, 50),
                   (3.58, 60),
                   (3.61, 70),
                   (3.65, 80),
                   (3.7, 90),
                   (4.3, 100)]


class Battery:
    def __init__(self, spiBus=0, spiDevice=1):
        self.spiBus = spiBus
        self.spiDevice = spiDevice

        # Initialize SPI
        self.spi = spidev.SpiDev()
        self.spi.open(self.spiBus, self.spiDevice)
        self.spi.max_speed_hz = 1000000
        self.spi.mode = 0b00

        # Initialize MUX select pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(A0_PIN, GPIO.OUT)
        GPIO.setup(A1_PIN, GPIO.OUT)

    def _readAdc(self):
        data1, data0 = self.spi.xfer2([0, 0])

        # MCP3301 Data Format:
        #   ? ? 0 SB B11 B10 B9 B8 B7 B6 B5 B4 B3 B2 B1 B0
        # | ------- data1 ------- | ------- data0 ------- |

        return (((data1 & 0B00001111) << 8) + data0) * LSB_SIZE

    def _getCellVoltages(self):
        batteryVoltages = []

        # Loop through MUX select
        for i in range(3):
            if i == 0:
                a0, a1 = GPIO.LOW, GPIO.LOW
            elif i == 1:
                a0, a1 = GPIO.LOW, GPIO.HIGH
            elif i == 2:
                a0, a1 = GPIO.HIGH, GPIO.LOW
            elif i == 3:
                a0, a1 = GPIO.HIGH, GPIO.HIGH

            GPIO.output(A0_PIN, a0)
            GPIO.output(A1_PIN, a1)

            time.sleep(0.0001)

            batteryVoltages.append(self._readAdc())

        return batteryVoltages

    def _getCellPercentage(self, cellVoltage):
        if cellVoltage <= CELL_PERCENTAGE[0][0]:
            return 0

        index = 1
        while index < len(CELL_PERCENTAGE) and cellVoltage > CELL_PERCENTAGE[index][0]:
            index += 1

        if index >= len(CELL_PERCENTAGE):
            return 100.0

        # Interpolate
        low = CELL_PERCENTAGE[index - 1]
        high = CELL_PERCENTAGE[index]
        return (cellVoltage - low[0]) / (high[0] - low[0]) * (high[1] - low[1]) + low[1]

    def getBatteryPercentage(self):
        cellVoltages = self._getCellVoltages()
        cellPercentages = []
        for voltage in cellVoltages:
            cellPercentages.append(self._getCellPercentage(voltage))
            break
        return sum(cellPercentages) / len(cellPercentages)
