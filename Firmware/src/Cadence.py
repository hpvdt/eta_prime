if __name__ == "__main__":
    import sys
    sys.modules['RPi'] = __import__('testing.RPi').RPi
    sys.modules['RPi.GPIO'] = sys.modules['RPi'].GPIO

from RunningAverageGpio import GPIOCounter

class Cadence:
    def __init__(self, pin):
        self.counter = GPIOCounter(pin, debounce=200)

    def get_cadence(self):
        '''Returns the sensed cadence, in RPM.'''
        return self.counter.get_frequency() * 60.0

if __name__ == "__main__":
    import time

    test_cadence = Cadence(0)
    assert test_cadence.get_cadence() == 0

    test_cadence.counter.log_time()
    time.sleep(0.5)
    test_cadence.counter.log_time()
    assert test_cadence.get_cadence() > 0
