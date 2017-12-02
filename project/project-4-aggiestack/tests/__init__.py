"""
Our testing module for Aggiestack (project 0).
"""
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent / 'fixtures'
HARDWARE_CONFIG_TXT = (FIXTURES_DIR / 'success' / 'config' / 
                       'hdwr-config.txt')
FLAVOR_CONFIG_TXT = (FIXTURES_DIR / 'success' / 'config' / 
                     'flavor-config.txt')
IMAGE_CONFIG_TXT = (FIXTURES_DIR / 'success' / 'config' / 
                    'image-config.txt')

BAD_MEM_HARDWARE_TXT = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                        'bad-mem.txt')
BAD_IP_HARDWARE_TXT = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                       'bad-ip.txt')
BAD_DISK_HARDWARE_TXT = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                         'bad-disk.txt')
BAD_VCPU_HARDWARE_TXT = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                         'bad-vcpu.txt')

TEST_JSON = Path(__file__).parent / 'fixtures' / 'state' / 'test.json'


def read_file(path):
    """
    loads a file from a pathlib.Path and returns the lines of the file.
    """
    lines = []
    with path.open() as read_only_file:
        lines = read_only_file.readlines()

    return lines
