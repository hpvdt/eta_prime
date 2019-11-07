from __future__ import absolute_import
import time
import random

from Radio import Radio as OriginalRadio

class RFM69:
    def receiveBegin(self):
        pass
    def receiveDone(self):
        return True
    def shutdown(self):
        pass

class Radio(OriginalRadio):
    def __init__(self, selfNode, toNode, net=1, key=None,
                 sleep_interval=0.1, timeout=5, rst_pin=12):
        self.radio = RFM69()
        self.Node = selfNode
        self.ToNode = toNode
        self.key = key or "1234567891011121"
        self.sleep_interval = sleep_interval
        self.timeout = timeout

    # Spoof radio data
    def Receive(self):
        # TODO: Make more realistic outputs for this. Maybe add some randomness.
        #       t, speedKph, targetSpeedKph, cadence, distance, batteryPercentage, emergency
        time.sleep(1)
        random_offset = random.uniform(0, 10)
        return OriginalRadio.CommaSeparate(time.strftime("%H:%M:%S"), 70 + random_offset, 80, 60 + random_offset, 1.2, 80 + random_offset, 0)

    def Transmit(self, *args):
        return
