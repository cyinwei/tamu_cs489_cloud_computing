"""
Tests the loading of a valid .txt config file and checks we can load the data
as a dict.
"""


import pprint

from lib.utils.io_helpers import read_config_file, read_hardware_config_file
from lib.settings import (
    IMAGE_KEYS, FLAVOR_KEYS
)
from lib.utils.check_config_inputs import (
    check_flavor_config_file,
    check_image_config_file
)
from tests import (
    HARDWARE_CONFIG_TXT,
    IMAGE_CONFIG_TXT,
    FLAVOR_CONFIG_TXT
)


def test_read_hardware():
    """
    Tests if we can load a correct hardware config file and convert it to a
    dict.
    """
    filepath = HARDWARE_CONFIG_TXT
    (success, data) = read_hardware_config_file(filepath)
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(data)

    assert success is True
    assert data['machines']['m1']['ip'] == '128.0.0.1'
    assert data['machines']['calvin']['mem'] == 8
    assert data['machines']['hobbes']['disk'] == 64
    assert data['machines']['dora']['vcpu'] == 16
    assert data['racks']['r1']['cache size'] == 40960


def test_read_images():
    """
    Tests if we can load a correct images config file and convert it to a
    dict.
    """
    filepath = IMAGE_CONFIG_TXT
    (success, data) = read_config_file(filepath,
                                       IMAGE_KEYS,
                                       check_image_config_file)
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
    filepath = FLAVOR_CONFIG_TXT
    (success, data) = read_config_file(filepath,
                                       FLAVOR_KEYS,
                                       check_flavor_config_file)
    pprinter = pprint.PrettyPrinter(indent=4)
    pprinter.pprint(data)

    assert success is True
    assert data['small']['mem'] == 1
    assert data['medium']['disk'] == 2
    assert data['xlarge']['vcpu'] == 8
