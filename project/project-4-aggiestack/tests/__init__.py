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

# Bad files with errors in them
BAD_MEM_HARDWARE_TXT_NAN = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                            'bad_mem_nan.txt')
BAD_MEM_HARDWARE_TXT_NEG = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                            'bad_mem_neg.txt') 
BAD_IP_HARDWARE_TXT_LOGIC = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_ip.txt')
BAD_IP_HARDWARE_TXT_DECIMALS = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                                'bad_ip_decimals.txt')
BAD_IP_HARDWARE_TXT_NUM = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                           'bad_ip_num.txt')
BAD_IP_HARDWARE_TXT_STR = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                           'bad_ip_str.txt')
BAD_DISK_HARDWARE_TXT_NAN = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_disk_nan.txt')
BAD_DISK_HARDWARE_TXT_NEG = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_disk_neg.txt')
BAD_VCPU_HARDWARE_TXT_NAN = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_vcpu_nan.txt')
BAD_VCPU_HARDWARE_TXT_NEG = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_vcpu_neg.txt')
BAD_RACK_HARDWARE_TXT_NAN = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_rack_nan.txt')
BAD_RACK_HARDWARE_TXT_NEG = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                             'bad_rack_neg.txt')
BAD_RACK_HARDWARE_TXT_M = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                           'bad_rack_machine.txt')
BAD_RACK_HARDWARE_TXT_M2 = (FIXTURES_DIR / 'fail' / 'config' / 'hardware' /
                            'bad_rack_machine2.txt')


TEST_JSON = Path(__file__).parent / 'fixtures' / 'state' / 'test.json'


def read_file(path):
    """
    loads a file from a pathlib.Path and returns the lines of the file.
    """
    lines = []
    with path.open() as read_only_file:
        lines = read_only_file.readlines()

    return lines
