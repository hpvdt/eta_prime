from __future__ import print_function, division
import time

if __name__ != "__main__":
    import RPi.GPIO as GPIO


class CircularBuffer:
    ''' Implements a circular buffer. Values are added until a predetermined
    maximum size and then the buffer begins overwriting the oldest value.'''
    def __init__(self, size):
        self.size = size
        self.values = []
        self.index = 0

    def append(self, value):
        if len(self.values) < self.size:
            self.values.append(value)
        else:
            self.values[self.index] = value
            self.index = (self.index + 1) % self.size

    def get_values(self):
        return self.values

    def get_average(self):
        if len(self.values) > 0:
            return float(sum(self.values)) / len(self.values)
        else:
            return 0

    def clear(self):
        self.values = []
        self.index = 0


# If it has been longer than this amount of time since the last event, assume
# frequency is zero
FREQUENCY_TIMEOUT = 3.0

class FrequencyCounter:
    def __init__(self, num_counts=5):
        '''Initialize a FrequencyCounter. Set num_counts to the number of
        counts to average (default 5). This class logs the times at which an
        event occurs and determines the average frequency at which it occurs.'''
        # TODO: Implement a buffer which changes size to accomodate the same
        # duration of counts instead of the same quantity of counts
        self.buffer = CircularBuffer(num_counts)
        self.first = True # Flag that this is the first measurement
        self.total_counts = 0
        self.last_time = None

    def log_time(self, *args, **kwargs):
        '''Use this as a callback for when the trigger is fired. Records the time
        of the event that is being recorded.'''
        self.total_counts += 1
        if self.first:
            self.last_time = time.time()
            self.first = False
        else:
            now = time.time()
            self.buffer.append(now - self.last_time)
            self.last_time = now

    def get_frequency(self):
        '''Returns the average frequency of the last num_counts events.'''
        # TODO: Perhaps include some derivative component to more accurately
        # determine speed at the precise time this is called.

        if self.last_time is None or time.time() - self.last_time > FREQUENCY_TIMEOUT:
            # If there have been no events in the last 2 seconds, assume the
            # event frequency is zero
            self.buffer.clear()
            return 0

        average = self.buffer.get_average()
        if average > 0:
            return 1.0 / self.buffer.get_average()
        else:
            return 0

    def get_count(self):
        return self.total_counts

    def reset(self):
        '''Reset the frequency counter.'''
        self.buffer.clear()
        self.total_counts = 0

class GPIOCounter(FrequencyCounter):
    '''Tracks the frequency and total number of digital events on a GPIO pin.'''
    def __init__(self, pin, debounce=200, num_counts=5):
        FrequencyCounter.__init__(self, num_counts)
        self.pin = pin

        # Set up switch interrupt
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, self.log_time, debounce)

if __name__ == "__main__":
    # Individual test cases for this module
    test_buffer = CircularBuffer(5)
    test_buffer.append(1)
    test_buffer.append(2)
    assert test_buffer.get_average() == 1.5

    test_buffer.append(3)
    test_buffer.append(4)
    test_buffer.append(5)
    test_buffer.append(7)
    assert test_buffer.get_average() == 4.2

    test_freq_counter = FrequencyCounter()
    assert test_freq_counter.get_frequency() == 0

    test_freq_counter.log_time()
    assert test_freq_counter.get_frequency() == 0

    time.sleep(0.5)
    test_freq_counter.log_time()
    assert test_freq_counter.get_frequency() < 2.5 and \
           test_freq_counter.get_frequency() > 1.66

    time.sleep(FREQUENCY_TIMEOUT + 0.1)
    assert test_freq_counter.get_frequency() == 0
