BOARD = 0
OUT = 1
IN = 2
HIGH = 3
LOW = 4
PUD_UP = 5
FALLING = 6

FUNC_NAMES = ['setmode', 'setup', 'output', 'add_event_detect']

for name in FUNC_NAMES:
    exec('def {}(*args, **kwargs):\n    pass'.format(name))
