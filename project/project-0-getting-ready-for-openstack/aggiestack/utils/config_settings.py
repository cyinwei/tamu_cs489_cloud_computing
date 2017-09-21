"""
We store the state as dicts/JSON.  These are the keys for a single type of
configuration.
"""

from pathlib import Path

# keys for the dicts/JSON state objects
HARDWARE_KEYS = ('ip', 'mem', 'disk', 'vcpu')
IMAGE_KEYS = ('path')
FLAVOR_KEYS = ('mem', 'disk', 'cvpu')

# directory information
STATE_DIR = Path(__file__).parent / '.aggiestack'
HARDWARE_FILE = STATE_DIR / 'hardware.json'
IMAGE_FILE = STATE_DIR / 'image.json'
FLAVOR_FILE = STATE_DIR / 'flavor.json'

# log file informatin
LOGFILE_NAME = 'aggiestack-log.txt' 
LOGFILE = Path(__file__).parent / LOGFILE_NAME 
