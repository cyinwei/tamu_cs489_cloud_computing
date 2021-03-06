"""
We store the state as dicts/JSON.  These are the keys for a single type of
configuration.
"""

from pathlib import Path

# keys for the dicts/JSON state objects
RACK_KEYS = ('cache size', )  # need the , to be a tuple
HARDWARE_KEYS = ('rack', 'ip', 'mem', 'disk', 'vcpu')
IMAGE_KEYS = ('size', 'path')  
FLAVOR_KEYS = ('mem', 'disk', 'vcpu')
SERVER_KEYS = ('image', 'flavor')
INSTANCE_KEYS = ('hardware', )

# directory information
STATE_DIR = Path(__file__).parent.parent / '.aggiestack'
CONFIG_DIR = STATE_DIR / 'configurations'

# configuration files
HARDWARE_FILE = CONFIG_DIR / 'hardware.json'
IMAGE_FILE = CONFIG_DIR / 'image.json'
FLAVOR_FILE = CONFIG_DIR / 'flavor.json'

# admin state (current state usage) file
ADMIN_STATE_HARDWARE_FILE = STATE_DIR / 'hardware_state.json'

# server list state file
SERVER_FILE = STATE_DIR / 'server_list.json'

# log file information
LOGFILE_NAME = 'aggiestack-log.txt'
LOGFILE = Path(__file__).parent.parent / LOGFILE_NAME
