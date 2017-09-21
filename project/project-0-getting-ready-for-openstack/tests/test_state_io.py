"""
Tests aggiestack.state_io.py, which handles reading config files, storing them
as JSON, and reading JSON files to keep state. 
"""

import pprint
import pytest

from aggiestack.config_io import read_hardware_config_file

from tests import FIXTURES_DIR, read_file

def test_read_hardware():
    filepath = FIXTURES_DIR / 'success' / 'hardware-config.txt'
    data = read_hardware_config_file(str(filepath.absolute()))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(data)

    assert data['m1']['ip'] == '128.0.0.1'
    assert data['calvin']['mem'] == 8
    assert data['hobbes']['disk'] == 64
    assert data['dora']['vcpu'] == 16

def test_read_images():
    pass