if __name__ == "__main__":
    import sys
    sys.modules['RPi'] = __import__('testing.RPi').RPi
    sys.modules['RPi.GPIO'] = sys.modules['RPi'].GPIO

from RunningAverageGpio import GPIOCounter

#############
# Constants #
#############
TARGET_SPEED = 120 # km/hr
TARGET_SPEED_SCALE_FACTOR = TARGET_SPEED / 128.748 # Sets the maximum target speed

WHEEL_CIRCUMFERENCE = 1.937 # meters

# WHEEL_CIRCUMFERENCE * 3600s/hr * 1/1000 km/m
FREQ_TO_KPH = WHEEL_CIRCUMFERENCE * 3.6
MILES_PER_KM = 0.621371

class SpeedAndDistance:
    def __init__(self, pin):
        self.counter = GPIOCounter(pin, debounce=30)

    def get_speed(self):
        '''Returns the speed, in km/hr.'''
        magnet_frequency = self.counter.get_frequency()
        return magnet_frequency * FREQ_TO_KPH

    def get_speed_mph(self):
        '''Returns the speed, in mi/hr.'''
        return self.get_speed() * MILES_PER_KM

    def get_distance(self):
        '''Returns the current distance down the course, in meters.'''
        return self.counter.get_count() * WHEEL_CIRCUMFERENCE

    def get_distance_miles(self):
        '''Returns the current distance down the course, in miles.'''
        return self.get_distance() * MILES_PER_KM / 1000.0

    def get_target_speed(self):
        '''Returns the target speed at the current point along the course in km/hr.'''
        distance = self.get_distance()

        # Polynomial taken from speed profile calculator spreadsheet.
        target_speed = ((0.02172162962963 * distance) - \
                       (6.9841256622019e-06 * distance**2) + \
                       (1.2239499085829e-09 * distance**3) - \
                       (1.0724598136691e-13 * distance**4) + \
                       (3.7048315202615e-18 * distance**5)) * TARGET_SPEED_SCALE_FACTOR

        return target_speed

    def get_target_speed_mph(self):
        '''Returns the target speed at the current point along the course in mi/hr.'''
        return self.get_target_speed() * MILES_PER_KM

    def reset(self):
        self.counter.reset()


if __name__ == "__main__":
    import time

    test_speed = SpeedAndDistance(0)
    assert test_speed.get_speed() == 0
    assert test_speed.get_distance() == 0

    test_speed.counter.log_time()
    assert test_speed.get_distance() == WHEEL_CIRCUMFERENCE
    assert test_speed.get_target_speed() > 0
    assert test_speed.get_target_speed() * MILES_PER_KM == \
           test_speed.get_target_speed_mph()

    time.sleep(0.5)
    test_speed.counter.log_time()
    assert test_speed.get_speed() > 0
    assert test_speed.get_speed() * MILES_PER_KM == \
           test_speed.get_speed_mph()
