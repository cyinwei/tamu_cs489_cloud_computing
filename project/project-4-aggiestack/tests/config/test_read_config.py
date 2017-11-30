"""
Tests the loading of a valid .txt config file and checks we can load the data
as a dict.
"""


import pprint

from lib.utils.io_helpers import read_config_file
from lib.settings import (
    HARDWARE_KEYS, IMAGE_KEYS, FLAVOR_KEYS
)
from lib.utils.check_config_inputs import (
    check_hardware_config_file,
    check_image_config_file,
    check_flavor_config_file
)

from tests import FIXTURES_DIR

def test_read_hardware():
    """
    Tests if we can load a correct hardware config file and convert it to a
    dict.
    """
    filepath = FIXTURES_DIR / 'success' / 'hardware-config.txt'
    (success, data, err_msg) = read_config_file(filepath,
                                                HARDWARE_KEYS,
                                                check_hardware_config_file)
    print(err_msg)
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(data)

    assert success is True
    assert data['m1']['ip'] == '128.0.0.1'
    assert data['calvin']['mem'] == 8
    assert data['hobbes']['disk'] == 64
    assert data['dora']['vcpu'] == 16

def test_read_images():
    """
    Tests if we can load a correct images config file and convert it to a
    dict.
    """
    filepath = FIXTURES_DIR / 'success' / 'images-config.txt'
    (success, data, err_msg) = read_config_file(filepath,
                                                IMAGE_KEYS,
                                                check_image_config_file)
    print(err_msg)
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(data)

    assert success is True
    assert data['linux-ubuntu']['path'] == '/images/linux-ubuntu-v1.0.img'
    assert data['linux-sles']['path'] == '/images/old-image.img'
    assert data['linux-ubuntu-16']['path'] == '/images/linux-ubuntu-16.img'

def test_read_flavors():
    """
    Tests if we can load a correct flavor config file and convert it to a
    dict.
    """
    filepath = FIXTURES_DIR / 'success' / 'flavor-config.txt'
    (success, data, err_msg) = read_config_file(filepath,
                                                FLAVOR_KEYS,
                                                check_flavor_config_file)
    print(err_msg)
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(data)

    assert success is True
    assert data['small']['mem'] == 1
    assert data['medium']['disk'] == 2
    assert data['xlarge']['vcpu'] == 8
