import sys
TOPLEVEL_MODULES = {'BikePi.py': 'BikePi', 'ChasePi.py': 'ChasePi'}

def print_usage():
    print('Usage: {} {{BikePi.py|ChasePi.py}}'.format(sys.argv[0]))

if len(sys.argv) < 2:
    print_usage()
    sys.exit(1)

if sys.argv[1] not in TOPLEVEL_MODULES:
    print_usage()
    sys.exit(1)

# Load the spoofed testing modules to shadow the originals
sys.modules['RPi'] = __import__('testing.RPi').RPi
sys.modules['RPi.GPIO'] = sys.modules['RPi'].GPIO

sys.modules['spidev'] = __import__('testing.spidev').spidev

sys.modules['picamera'] = __import__('testing.picamera').picamera

sys.modules['Battery'] = __import__('testing.Battery').Battery

sys.modules['Radio'] = __import__('testing.Radio').Radio
sys.modules['RFM69.RFM69registers'] = sys.modules['Radio'] # It doesnt matter what this is equal to, as long as it exists.

# Run the main program
__import__(TOPLEVEL_MODULES[sys.argv[1]])
