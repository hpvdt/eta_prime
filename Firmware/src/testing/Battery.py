from __future__ import absolute_import
from Battery import Battery as OriginalBattery

class Battery(OriginalBattery):
    def __init__(self, spiBus=0, spiDevice=1):
        if spiBus != 0 or spiDevice != 1:
            raise RuntimeError("spiBus or spiDevice has changed! See Battery Testing!")

    def _readAdc(self):
        return 3.7

    def _getCellVoltages(self):
        return [3.7]*3

    def getBatteryPercentage(self):
        ''' Redefining this will prevent all calls to _readAdc and
        _getCellVoltages. Just returns a battery percentage of 90%.'''
        return 90.0
