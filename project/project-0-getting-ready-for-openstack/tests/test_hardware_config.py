import pytest

from aggiestack.config_io import _check_hardware_config_file_format

def test_correct_hardware_config():
    f = open('./fixtures/success/hardware-config.txt')
    lines = f.readlines()
    results = _check_hardware_config_file_format(lines)
    print (results[1])
    assert(results[0] is True)